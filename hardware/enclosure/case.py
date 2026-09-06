"""Gehäuse für den Hörmann-HCP2-Adapter (Trägerplatine aus ../pcb).

Zwei Teile: `bottom` (Wanne) und `top` (Deckel mit Hex-Lüftungsmuster, in vier
Ecksäulen verschraubt). Nicht wasserdicht, deshalb keine Nut und kein Wulst wie
bei der Ventilsteuerung: der Deckel liegt plan auf dem Wandrand.

Eine einzige Öffnung, für den 6P6C-Stecker an J1. USB-C von U1 bleibt innen;
zum Flashen kommt der Deckel ab, JP1 liegt ohnehin innen.

Koordinaten: Bodenplatte zentriert in der XY-Ebene, Wände wachsen in +Z. Die
Platine liegt so, wie das KiCad-Rendering sie zeigt: J1-Kante nach +Y, USB-Kante
nach +X. `kicad()` rechnet Platinenkoordinaten (Ursprung links oben, y nach unten)
in Gehäusekoordinaten um, damit die Zahlen aus pcb.py direkt verwendbar bleiben.

    uv run python hardware/enclosure/case.py           STLs exportieren
    uv run python hardware/enclosure/case.py --show    in den ocp_vscode-Viewer
                                              (vorher: uv run python -m ocp_vscode)
    uv run python hardware/enclosure/case.py --png     preview-*.png rendern
"""

import math
import re
import sys
from collections import namedtuple
from pathlib import Path

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Cylinder,
    GeomType,
    HexLocations,
    Location,
    Locations,
    Mode,
    Plane,
    Rectangle,
    RegularPolygon,
    extrude,
    fillet,
)

from outputs import write_outputs

# Platinenmaße, Lochbild und Modulpositionen kommen direkt aus dem PCB-Generator,
# die Modulumrisse aus dessen Footprints. Eine Layoutänderung dort landet so ohne
# Abschreiben hier.
PCB_DIR = Path(__file__).resolve().parent.parent / "pcb"
sys.path.insert(0, str(PCB_DIR))
import pcb  # noqa: E402

# --- Platine ----------------------------------------------------------------

pcb_length, pcb_width = pcb.BOARD_W, pcb.BOARD_H
pcb_thickness = 1.6
# Die Referenzen mit Befestigungsloch-Footprint; unter jedem steht ein Sockel.
# Die Platine hat drei davon: in der rechten oberen Ecke war neben den PS1-Pads
# kein Platz für einen Sockel, die Ecke liegt auf der Leiste an der +Y-Wand.
# test_case.py prüft, dass um jedes Loch genug lötfreie Unterseite ist.
standoff_refs = [ref for ref, fp in pcb.FOOTPRINTS.items() if fp.startswith("MountingHole")]

# Bauhöhe über der Platinenoberseite, die das Gehäuse freihält. Das höchste
# Bauteil ist laut Händlerangaben der LM2596 mit seinen Elkos (~13 mm) auf
# Stiften, dicht gefolgt vom gesockelten ESP32 mit USB-C-Buchse.
# UNGEPRÜFT: alle Modulhöhen stammen aus Händlerbildern, siehe Mockups unten.
parts_height = 16
headroom = 4  # Luft zwischen höchstem Bauteil und Deckel
# Lötstellen und Stiftenden unter der Platine, deutlich unter standoff_height
solder_tail_height = 2

# --- Befestigung ------------------------------------------------------------
# Ruthex-Gewindeeinsätze wie bei der Ventilsteuerung (Datenblatt-Spalten d3, L, W)
Heatset = namedtuple("Heatset", "hole_diameter length min_wall")
heatset_m3 = Heatset(4.0, 5.7, 1.6)

standoff_wall = 2.0  # über dem Ruthex-Minimum 1.6, siehe test_case.py
column_wall = 2.0
# Höher als die Bohrung tief ist, damit die ganz im Sockel bleibt. Die Platine
# braucht nur solder_tail_height darunter; die Einsatzlänge gibt das Maß vor.
standoff_height = 7.2
# Kleiner als bei der Ventilsteuerung: der Sockel an H2 steht 0.5 mm über die
# Platinenkante und damit dicht an der +Y-Wand, eine 2er-Kehle liefe in die Wand.
standoff_fillet = 1.0


def heatset_hole_depth(insert):
    return insert.length + 1  # Datenblatt: Bohrtiefe L + 1 mm


def standoff_diameter(insert):
    return insert.hole_diameter + 2 * standoff_wall


column_diameter = heatset_m3.hole_diameter + 2 * column_wall  # Ecksäulen für den Deckel

# --- Gehäuse ----------------------------------------------------------------

# Wandstärken als Vielfache der Extrusionsbreite (0.4), siehe cad/best-practice.md.
# Dünner als bei der Ventilsteuerung: kleine Box, innen, keine Dichtfläche, die
# plan bleiben muss.
wall_thickness = 2.4  # 6 Bahnen, gilt auch für den Boden
lid_thickness = 2.8  # 7 Bahnen; das Hex-Muster nimmt Steifigkeit, die Senkung braucht 0.8 Rest
corner_radius = 6

# Seitlich so viel Luft, dass die Ecksäulen an den Platinenecken vorbeilaufen:
# die Platine ist bis in die Ecken bestückt, Aussparungen kommen nicht in Frage.
# Die Säule reicht `column_reach` weit in die Ecke hinein (siehe unten), der
# Rest ist Spiel. test_case.py rechnet das nach.
spacing_side = 9  # ±X
# Die Buchse sitzt bündig an der Platinenkante; die Wand soll so nah stehen,
# dass der Stecker sicher einrastet und die Rastnase erreichbar bleibt.
spacing_top = 2.0  # +Y, Buchsenfront bis Wandinnenseite
spacing_bottom = 3  # -Y

case_length = pcb_length + 2 * spacing_side
case_width = pcb_width + spacing_top + spacing_bottom
case_height = standoff_height + pcb_thickness + parts_height + headroom

outer_length = case_length + 2 * wall_thickness
outer_width = case_width + 2 * wall_thickness

floor_top = wall_thickness / 2  # Oberseite der Bodenplatte
rim = floor_top + case_height  # Oberkante der Wände
pcb_bottom = floor_top + standoff_height
pcb_top = pcb_bottom + pcb_thickness

# Platinenmitte im Gehäuse
pcb_x = 0.0
pcb_y = case_width / 2 - spacing_top - pcb_width / 2


# Leiste unter der +Y-Platinenkante, von Säule zu Säule: trägt die Ecke ohne
# Sockel (H2) und die Buchse gegen das Einstecken. Greift ledge_under weit unter
# die Platine; die nächsten Lötstellen (PS1) liegen 3.1 mm hinter der Kante.
ledge_under = 1.5
ledge_depth = spacing_top + ledge_under
ledge_gap_side = 0.4  # Abstand der Leistenenden zur Steckeröffnung


def kicad(x, y):
    """KiCad-Platinenkoordinaten (links oben, y nach unten) -> Gehäuse-XY."""
    return pcb_x + x - pcb_length / 2, pcb_y - (y - pcb_width / 2)


# Öffnung für den 6P6C-Stecker in der +Y-Wand, mittig vor J1. Grundfläche der
# Buchse kommt aus dem Footprint (weiter unten), die Höhe aus der Händlerzeichnung
# der gekauften Buchse (hardware/reference/.../drawing-6p6c.webp, "53-6p6c").
# Die Rastnase zeigt zur Platine: der Hebel des Steckers läuft unter dem
# Steckerkörper nach außen und braucht unter der Buchsenfront Platz.
jack_height = 11.65  # Körper über der Platine, laut Zeichnung
jack_hole_side = 1.0  # Luft je Seite neben der Buchse
jack_hole_above = 2.0  # über der Buchse
jack_hole_below = 3.0  # unter der Buchsenfront, für den Rasthebel
jack_hole_fillet = 2.0

# --- Deckel -----------------------------------------------------------------

# Deckelschrauben in Ecksäulen, auf der Diagonalen so weit in der Ecke, dass sie
# lid_screw_merge tief in die verrundete Wand einschneiden (sonst berühren sie
# die Wand nur in einer Linie).
lid_screw_merge = 2.0
_corner = corner_radius + lid_screw_merge - column_diameter / 2  # vom Bogenmittelpunkt
lid_screw_x = case_length / 2 - corner_radius + _corner / 2**0.5
lid_screw_y = case_width / 2 - corner_radius + _corner / 2**0.5
lid_screw_positions = [(i * lid_screw_x, j * lid_screw_y) for i in (-1, 1) for j in (-1, 1)]
# Wie weit die Säule von der Innenwand aus in den Innenraum hineinreicht
column_reach = corner_radius - _corner / 2**0.5 + column_diameter / 2
lid_screw_clearance = 3.4  # M3 mit Spiel
lid_cbore_diameter = 6.0
lid_cbore_depth = 2.0

# Lüftung: Sechseck-Löcher im Wabenraster. Die Zelle (Loch plus halber Steg je
# Seite) gibt den Rasterabstand vor, HexLocations tiled RegularPolygon mit
# rotation=0 lückenlos (geprüft: Fläche der Zellen == Summe der Einzelflächen).
vent_hole_flats = 4.0  # Schlüsselweite des Lochs
vent_web = 1.6  # Steg zwischen zwei Löchern, 4 Bahnen
vent_cell_apothem = (vent_hole_flats + vent_web) / 2
vent_hole_apothem = vent_hole_flats / 2
vent_hole_radius = vent_hole_apothem / math.cos(math.pi / 6)  # Eckenradius
# Kein Loch näher als das an der Wandinnenkante oder an einer Schraubensenkung:
# der Rand muss die Auflage auf dem Wandrand und die Schrauben tragen.
vent_margin = 2.0

through = 3 * wall_thickness  # großzügige Länge für Schnitte quer durch eine Wand

# --- Grobmodelle der Hardware -----------------------------------------------
# Nur für den Viewer und die Einbauprobe im Test, nicht für die STLs. Umriss und
# Lage jedes Moduls kommen aus dem F.Fab-Rechteck seines Footprints und aus
# pcb.PLACEMENT; hier stehen nur die Höhen und was über der Platine darauf sitzt.
#
# Aufbauten in Footprint-Koordinaten (KiCad: y nach unten, vor der Drehung) als
# (x, y, dx, dy, z0, h): Mitte, Grundfläche, Unterkante über der Platine, Höhe.
# dx = None heißt Zylinder mit Durchmesser dy.
# UNGEPRÜFT: alle Höhen und die Lage der Aufbauten, aus Händlerbildern geschätzt.
Module = namedtuple("Module", "body_z0 body_height features")
modules = {
    # Buchsenkörper (13.2 × 18 laut Footprint), Front bündig mit der Platinenkante
    "J1": Module(0, jack_height, []),
    # Modulplatine steht auf ihren Stiften; Elkos (100 µF/50 V, 220 µF/35 V) sind
    # das Höchste im Gehäuse, dann Drossel, Regler mit Kühlfahne, Trimmer
    "PS1": Module(2, 1.6, [
        (-13, 3, None, 8.5, 3.6, 11),
        (13, 3, None, 8.5, 3.6, 11),
        (0, 2, 12, 12, 3.6, 7),
        (5, -6, 10, 5, 3.6, 8),
        (-13, -6, 5, 10, 3.6, 6),
    ]),
    # Castellated, liegt flach auf; Bestückung als Block
    "U2": Module(0, 1.6, [(0, 0, 30, 14, 1.6, 7)]),
    # Gesockelt: Buchsenleisten 8.5 mm, darauf die Platine, darauf USB-C (am -y-Ende
    # laut Footprint), Antenne am +y-Ende
    "U1": Module(8.5, 1.6, [
        (-7.62, 0, 2.54, 20.32, 0, 8.5),
        (7.62, 0, 2.54, 20.32, 0, 8.5),
        (0, -9.6, 9, 7.3, 10.1, 3.2),
        (0, 10.3, 7, 2, 10.1, 1),
        (0, 0, 6, 6, 10.1, 1),
    ]),
    # Stiftleiste mit Jumper, Footprint hat kein F.Fab-Rechteck, darum eigener Körper
    "JP1": Module(0, 9, []),
}
module_bodies = {"JP1": (0, 1.27, 2.54, 5.08)}  # (x, y, dx, dy) wo der Footprint keins liefert

# 6P6C-Stecker, steckt bis zur Buchsenrückwand in J1 und ragt durch die
# Wandöffnung. Rastnase gedrückt gedacht (8 mm hoch), mittig in der Buchsenhöhe.
# UNGEPRÜFT: wie weit der Körper wirklich aus der Wand steht, zeigt erst der
# Probedruck; bei 18 mm tiefer Buchse und 4.4 mm Wand plus Luft ist es wenig.
plug_width, plug_height, plug_length = 9.65, 8.0, 21.0


def footprint_text(ref):
    return (pcb.LIBRARY_DIR / f"{pcb.FOOTPRINTS[ref]}.kicad_mod").read_text()


def footprint_body(ref):
    """(x, y, dx, dy) der F.Fab-Zeichnung, in Footprint-Koordinaten: Bounding Box
    aller Linien und Rechtecke auf der Lage. KiCad-Bibliotheks-Footprints zeichnen
    den Umriss aus Linien, die eigenen aus einem Rechteck; beides landet hier."""
    if ref in module_bodies:
        return module_bodies[ref]
    xs, ys = [], []
    text = " ".join(footprint_text(ref).split())  # KiCad 8 bricht Primitive über mehrere Zeilen
    for m in re.finditer(r'\(fp_(?:line|rect) \(start (-?[\d.]+) (-?[\d.]+)\) \(end (-?[\d.]+) (-?[\d.]+)\).*?\(layer "([^"]+)"\)', text):
        if m.group(5) == "F.Fab":
            xs += [float(m.group(1)), float(m.group(3))]
            ys += [float(m.group(2)), float(m.group(4))]
    assert xs, f"{ref}: keine F.Fab-Zeichnung im Footprint"
    return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, max(xs) - min(xs), max(ys) - min(ys)


def module_extent(ref):
    """(xmin, xmax, ymin, ymax) des Modulkörpers in Gehäuse-XY."""
    bx, by, bdx, bdy = footprint_body(ref)
    cx, cy = placed(ref, bx, by)
    dx, dy = placed_size(ref, bdx, bdy)
    return cx - dx / 2, cx + dx / 2, cy - dy / 2, cy + dy / 2


def footprint_drills(ref):
    """[(x, y, drill, pad, plated)] aller Bohrungen des Footprints. `pad` ist die
    Padgröße, also der Platz, den die Lötstelle unter der Platine einnimmt."""
    return [
        (float(x), float(y), float(d), max(float(sx), float(sy)), kind == "thru_hole")
        for kind, x, y, sx, sy, d in re.findall(
            r'\(pad "[^"]*" (thru_hole|np_thru_hole) \w+\s*\(at (-?[\d.]+) (-?[\d.]+)[^)]*\)\s*'
            r'\(size ([\d.]+) ([\d.]+)\)\s*\(drill ([\d.]+)',
            footprint_text(ref),
        )
    ]


def placed(ref, x, y):
    """Footprint-Koordinaten -> Gehäuse-XY, mit Drehung und Lage aus pcb.PLACEMENT."""
    px, py, rotation = pcb.PLACEMENT[ref]
    dx, dy = pcb.rotate(x, y, rotation)
    return kicad(px + dx, py + dy)


def placed_size(ref, dx, dy):
    return (dy, dx) if pcb.PLACEMENT[ref][2] % 180 else (dx, dy)


def standoff_positions():
    return [placed(ref, 0, 0) for ref in standoff_refs]


# Buchse J1 in Gehäusekoordinaten; die Front liegt an der +Y-Platinenkante
_j1 = module_extent("J1")
jack_x = (_j1[0] + _j1[1]) / 2
jack_width = _j1[1] - _j1[0]
jack_depth = _j1[3] - _j1[2]
jack_back_y = _j1[2]
jack_hole_width = jack_width + 2 * jack_hole_side
jack_hole_height = jack_hole_below + jack_height + jack_hole_above
jack_hole_z = pcb_top - jack_hole_below + jack_hole_height / 2


def edges_in_box(part, lo, hi):
    """Kanten, deren Mittelpunkt in der Box zwischen `lo` und `hi` liegt."""
    return (
        part.edges()
        .filter_by_position(Axis.X, lo[0], hi[0])
        .filter_by_position(Axis.Y, lo[1], hi[1])
        .filter_by_position(Axis.Z, lo[2], hi[2])
    )


def build_bottom():
    with BuildPart() as part:
        # Bodenplatte
        with BuildSketch():
            Rectangle(outer_length, outer_width)
        extrude(amount=wall_thickness / 2, both=True)

        # Außenwände
        with BuildSketch(Plane.XY.offset(floor_top)):
            Rectangle(outer_length, outer_width)
            Rectangle(case_length, case_width, mode=Mode.SUBTRACT)
        extrude(amount=case_height)

        fillet(part.edges().filter_by(Axis.Z), corner_radius)

        # Sockel mit Sacklöchern für die Gewindeeinsätze
        posts = standoff_positions()
        with Locations(*[(x, y, floor_top) for x, y in posts]):
            Cylinder(standoff_diameter(heatset_m3) / 2, standoff_height, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations(*[(x, y, floor_top + standoff_height) for x, y in posts]):
            Cylinder(
                heatset_m3.hole_diameter / 2,
                heatset_hole_depth(heatset_m3),
                align=(Align.CENTER, Align.CENTER, Align.MAX),
                mode=Mode.SUBTRACT,
            )

        # Fußkehlen, vor den Ecksäulen, damit nur die vier Sockelkreise gewählt
        # werden. Radius mit prüfen: auf Bodenhöhe liegen auch die Bögen der
        # Eckverrundungen.
        post_radius = standoff_diameter(heatset_m3) / 2
        base_circles = (
            part.edges()
            .filter_by(GeomType.CIRCLE)
            .filter_by_position(Axis.Z, floor_top - 0.01, floor_top + 0.01)
            .filter_by(lambda e: abs(e.radius - post_radius) < 1e-6)
        )
        assert len(base_circles) == len(posts), f"{len(base_circles)} Sockelkreise statt {len(posts)}"
        fillet(base_circles, standoff_fillet)

        # Ecksäulen bis an den Rand, Gewindeeinsatz von oben
        with Locations(*[(x, y, floor_top) for x, y in lid_screw_positions]):
            Cylinder(column_diameter / 2, case_height, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations(*[(x, y, rim) for x, y in lid_screw_positions]):
            Cylinder(
                heatset_m3.hole_diameter / 2,
                heatset_hole_depth(heatset_m3),
                align=(Align.CENTER, Align.CENTER, Align.MAX),
                mode=Mode.SUBTRACT,
            )

        # Auflageleiste an der +Y-Wand, in die Wand hinein und bis in die Achsen
        # der Ecksäulen verlängert, damit sie in die Säulen übergeht. Nicht weiter:
        # ein Kasten bis zur Innenkante träte am Eckradius durch die Außenhaut.
        # Vor der Buchse bleibt sie weg: die Steckeröffnung reicht unter die
        # Platine, und dort stützt ohnehin der Sockel H1 direkt daneben.
        ledge_gap = jack_hole_width + 2 * ledge_gap_side
        for x0, x1 in ((-lid_screw_x, jack_x - ledge_gap / 2), (jack_x + ledge_gap / 2, lid_screw_x)):
            with Locations((x0, case_width / 2 - ledge_depth, floor_top)):
                Box(x1 - x0, ledge_depth + wall_thickness / 2, standoff_height, align=(Align.MIN, Align.MIN, Align.MIN))

        # Steckeröffnung in der +Y-Wand
        with Locations((jack_x, case_width / 2, jack_hole_z)):
            Box(jack_hole_width, through, jack_hole_height, mode=Mode.SUBTRACT)
        eps = 0.1
        corners = edges_in_box(
            part,
            (jack_x - jack_hole_width / 2 - eps, case_width / 2 - eps, jack_hole_z - jack_hole_height / 2 - eps),
            (jack_x + jack_hole_width / 2 + eps, outer_width / 2 + eps, jack_hole_z + jack_hole_height / 2 + eps),
        ).filter_by(Axis.Y)
        assert len(corners) == 4, f"{len(corners)} Lochkanten statt 4"
        fillet(corners, jack_hole_fillet)

    return part.part


def vent_locations():
    """Mittelpunkte der Lüftungslöcher: Wabenraster, beschnitten auf den Innenraum
    abzüglich Rand und Schraubensenkungen."""
    reach = vent_hole_radius + vent_margin
    half_l, half_w = case_length / 2 - reach, case_width / 2 - reach
    r = max(corner_radius - reach, 0)  # Eckradius des zulässigen Bereichs
    keep_out = lid_cbore_diameter / 2 + reach
    nx = int(case_length / (2 * vent_cell_apothem)) + 2
    ny = int(case_width / (vent_cell_apothem * 3**0.5)) + 2
    kept = []
    for loc in HexLocations(vent_cell_apothem, nx, ny):
        x, y = loc.position.X, loc.position.Y
        dx, dy = max(abs(x) - (half_l - r), 0), max(abs(y) - (half_w - r), 0)
        if dx * dx + dy * dy > r * r:
            continue
        if any(math.dist((x, y), s) < keep_out for s in lid_screw_positions):
            continue
        kept.append((x, y))
    return kept


def build_top():
    with BuildPart() as part:
        Box(outer_length, outer_width, lid_thickness)
        fillet(part.edges().filter_by(Axis.Z), corner_radius)

        # Schraubenlöcher, Senkung auf der Außenseite (hier -Z, liegt beim Drucken unten)
        with Locations(*[(x, y, 0) for x, y in lid_screw_positions]):
            Cylinder(lid_screw_clearance / 2, through, mode=Mode.SUBTRACT)
        with Locations(*[(x, y, -lid_thickness / 2) for x, y in lid_screw_positions]):
            Cylinder(
                lid_cbore_diameter / 2,
                lid_cbore_depth,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
                mode=Mode.SUBTRACT,
            )

        # Lüftungslöcher
        with BuildSketch() as vents:
            with Locations(*vent_locations()):
                RegularPolygon(vent_hole_apothem, 6, major_radius=False)
        extrude(amount=lid_thickness, both=True, mode=Mode.SUBTRACT)

    return part.part


def build_mockups():
    base = Align.CENTER, Align.CENTER, Align.MIN
    with BuildPart() as board:
        with Locations((pcb_x, pcb_y, pcb_bottom)):
            Box(pcb_length, pcb_width, pcb_thickness, align=base)
        for ref in pcb.FOOTPRINTS:
            for x, y, drill, pad, plated in footprint_drills(ref):
                cx, cy = placed(ref, x, y)
                with Locations((cx, cy, pcb_bottom)):
                    Cylinder(drill / 2, pcb_thickness, align=base, mode=Mode.SUBTRACT)
                if plated:
                    # Lötstelle unter der Platine, so groß wie das Pad; dort muss
                    # der Sockel Platz lassen
                    with Locations((cx, cy, pcb_bottom - solder_tail_height)):
                        Cylinder(pad / 2, solder_tail_height, align=base)

    mockups = {"pcb": board.part}
    for ref, module in modules.items():
        bx, by, bdx, bdy = footprint_body(ref)
        with BuildPart() as part:
            for x, y, dx, dy, z0, h in [(bx, by, bdx, bdy, module.body_z0, module.body_height), *module.features]:
                cx, cy = placed(ref, x, y)
                with Locations((cx, cy, pcb_top + z0)):
                    if dx is None:
                        Cylinder(dy / 2, h, align=base)
                    else:
                        Box(*placed_size(ref, dx, dy), h, align=base)
        mockups[f"{ref} {pcb.VALUES[ref]}"] = part.part

    # Stecker: von der Buchsenrückwand aus nach +Y durch die Wand
    with BuildPart() as plug:
        with Locations((jack_x, jack_back_y, pcb_top + jack_height / 2)):
            Box(plug_width, plug_length, plug_height, align=(Align.CENTER, Align.MIN, Align.CENTER))
    mockups["6P6C plug"] = plug.part
    return mockups


if __name__ == "__main__":
    print(f"Innenmaß {case_length}x{case_width}x{case_height}, außen {outer_length}x{outer_width}x{rim + wall_thickness / 2 + lid_thickness}")
    write_outputs(
        {"bottom": build_bottom(), "top": build_top()},
        Path(__file__).parent,
        # Deckel umdrehen und auf den Rand setzen
        assembly={"top": Location((0, 0, rim + lid_thickness / 2), (0, 180, 0))},
        mockups=build_mockups(),
        translucent=["top"],
    )
