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

# --- Platine ----------------------------------------------------------------
# Alles aus hardware/pcb/pcb.py und den Footprints in HCP.pretty. Die Platine ist
# noch nicht gefertigt; ändert sich dort etwas, ändert es sich hier mit.

pcb_length, pcb_width, pcb_thickness = 65.0, 44.5, 1.6
# H1..H4 in KiCad-Koordinaten (von der linken oberen Ecke), Ø3.2 für M3
pcb_holes = [(3.5, 16.5), (62.2, 3.5), (39.9, 40.5), (61.0, 34.0)]
pcb_hole_diameter = 3.2

# Bauhöhe über der Platinenoberseite, die das Gehäuse freihält. Das höchste
# Bauteil ist laut Händlerangaben der LM2596 mit seinen Elkos (~13 mm) auf
# Stiften, dicht gefolgt vom gesockelten ESP32 mit USB-C-Buchse.
# UNGEPRÜFT: alle Modulhöhen stammen aus Händlerbildern, siehe Mockups unten.
parts_height = 16
headroom = 5  # Luft zwischen höchstem Bauteil und Deckel
# Lötstellen und Stiftenden unter der Platine, deutlich unter standoff_height
solder_tail_height = 2

# --- Befestigung ------------------------------------------------------------
# Ruthex-Gewindeeinsätze wie bei der Ventilsteuerung (Datenblatt-Spalten d3, L, W)
Heatset = namedtuple("Heatset", "hole_diameter length min_wall")
heatset_m3 = Heatset(4.0, 5.7, 1.6)

standoff_wall = 2.0
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


column_diameter = standoff_diameter(heatset_m3)  # Ecksäulen für den Deckel

# --- Gehäuse ----------------------------------------------------------------

# Wandstärken als Vielfache der Extrusionsbreite (0.4), siehe cad/best-practice.md
wall_thickness = 3.2  # 8 Bahnen, gilt auch für den Boden
lid_thickness = 3.6  # 9 Bahnen; das Hex-Muster nimmt dem Deckel Steifigkeit
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


def kicad(x, y):
    """KiCad-Platinenkoordinaten (links oben, y nach unten) -> Gehäuse-XY."""
    return pcb_x + x - pcb_length / 2, pcb_y - (y - pcb_width / 2)


# Öffnung für den 6P6C-Stecker in der +Y-Wand, mittig vor J1. Breiter und höher
# als die Buchse, damit deren Front die Öffnung füllt und die Rastnase Platz hat.
# UNGEPRÜFT: 95001-Buchsen sind etwa 12.2 breit und 13.3 hoch; Stecker 9.65 breit.
jack_width, jack_depth, jack_height = 12.2, 13.0, 13.3
jack_x = kicad(9.0, 0.0)[0]
jack_hole_width = jack_width + 2  # 1 mm Luft je Seite
jack_hole_height = 15  # ab Platinenoberseite, deckt Buchse plus Toleranz
jack_hole_z = pcb_top + jack_hole_height / 2
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
# Nur für den Viewer und die Einbauprobe im Test, nicht für die STLs. Grundflächen
# aus den Footprints (F.Fab), Höhen aus Händlerangaben. (KiCad-Mitte x, y, Größe
# dx, dy nach Drehung, Höhe über der Platinenoberseite.)
# UNGEPRÜFT: Höhen. PS1 sitzt auf seinen Stiften ~2 mm über der Platine, U1 ist
# gesockelt (Buchsenleiste 8.5 + Platine 1.6 + USB-C 3.5).
module_features = {
    "J1 6P6C": (9.0, 6.5, jack_width, jack_depth, jack_height),
    "PS1 LM2596": (38.45, 12.25, 43.5, 21.5, 15),
    "U2 RS485": (19.5, 34.0, 34.0, 18.0, 9),
    "U1 ESP32-C3": (53.4, 34.0, 22.52, 18.0, 14),
    "JP1": (63.0, 9.27, 2.54, 5.08, 9),
}

# 6P6C-Stecker, steckt in J1 und ragt durch die Wandöffnung nach außen. Rastnase
# gedrückt gedacht (8 mm hoch), mittig in der Buchsenhöhe.
plug_width, plug_height, plug_length = 9.65, 8.0, 21.0
plug_outside = plug_length - jack_depth + spacing_top + wall_thickness  # Überstand außen


def edges_in_box(part, lo, hi):
    """Kanten, deren Mittelpunkt in der Box zwischen `lo` und `hi` liegt."""
    return (
        part.edges()
        .filter_by_position(Axis.X, lo[0], hi[0])
        .filter_by_position(Axis.Y, lo[1], hi[1])
        .filter_by_position(Axis.Z, lo[2], hi[2])
    )


def standoff_positions():
    return [kicad(x, y) for x, y in pcb_holes]


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
    with BuildPart() as pcb:
        with Locations((pcb_x, pcb_y, pcb_bottom)):
            Box(pcb_length, pcb_width, pcb_thickness, align=base)
        with Locations(*[(x, y, pcb_bottom) for x, y in standoff_positions()]):
            Cylinder(pcb_hole_diameter / 2, pcb_thickness, align=base, mode=Mode.SUBTRACT)
        # Lötstellen und Stiftenden unter der Platine, pauschal als Platte
        with Locations((pcb_x, pcb_y, pcb_bottom - solder_tail_height)):
            Box(pcb_length - 2 * standoff_diameter(heatset_m3), pcb_width - 2 * standoff_diameter(heatset_m3),
                solder_tail_height, align=base)

    mockups = {"pcb": pcb.part}
    for name, (kx, ky, dx, dy, h) in module_features.items():
        x, y = kicad(kx, ky)
        with BuildPart() as module:
            with Locations((x, y, pcb_top)):
                Box(dx, dy, h, align=base)
        mockups[name] = module.part

    # Stecker: von der Buchsenrückwand aus nach +Y durch die Wand
    jack_back_y = kicad(9.0, jack_depth)[1]
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
    )
