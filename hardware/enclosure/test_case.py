"""Maßketten, die man sonst erst am Druck merkt.

Prüft Beziehungen, nicht Zahlen: das Gehäuse ist noch im Entwurf, die Platine
auch. Läuft direkt: `uv run python hardware/enclosure/test_case.py`.
"""

import math

import case


EXTRUSION = 0.4  # Düsendurchmesser


def approx(a, b, tol=1e-6):
    return abs(a - b) < tol


def test_thicknesses_print_solid():
    for name in ("wall_thickness", "lid_thickness", "standoff_wall", "vent_web"):
        value = getattr(case, name)
        assert approx(value / EXTRUSION, round(value / EXTRUSION), 1e-9), f"{name}={value}"


def test_bottom():
    part = case.build_bottom()
    bb = part.bounding_box()
    assert len(part.solids()) == 1
    assert approx(bb.min.X, -case.outer_length / 2) and approx(bb.max.X, case.outer_length / 2)
    assert approx(bb.min.Y, -case.outer_width / 2) and approx(bb.max.Y, case.outer_width / 2)
    assert approx(bb.min.Z, -case.wall_thickness / 2) and approx(bb.max.Z, case.rim)


def test_top():
    part = case.build_top()
    bb = part.bounding_box()
    assert len(part.solids()) == 1
    assert approx(bb.min.X, -case.outer_length / 2) and approx(bb.max.X, case.outer_length / 2)
    assert approx(bb.min.Z, -case.lid_thickness / 2) and approx(bb.max.Z, case.lid_thickness / 2)
    # Lüftung: Löcher gehen durch, Muster liegt ganz im Innenraum
    assert len(case.vent_locations()) > 50
    for x, y in case.vent_locations():
        assert abs(x) + case.vent_hole_radius < case.case_length / 2
        assert abs(y) + case.vent_hole_radius < case.case_width / 2


def test_heatset():
    insert = case.heatset_m3
    wall = (case.standoff_diameter(insert) - insert.hole_diameter) / 2
    assert wall >= insert.min_wall
    # Bohrung bleibt im Sockel, der Boden ist dafür zu dünn
    assert case.heatset_hole_depth(insert) <= case.standoff_height
    assert case.heatset_hole_depth(insert) < case.case_height
    assert case.standoff_height >= case.solder_tail_height + 1


def test_pcb_clears_columns():
    """Die Platine ist bis in die Ecken bestückt, die Ecksäulen müssen daneben stehen."""
    gap = case.spacing_side - case.column_reach
    assert gap >= 1.5, f"Säule nur {gap:.2f} mm neben der Platinenkante"


def test_standoffs_clear_walls_and_columns():
    """Die Fußkehle braucht Platz, sonst läuft sie in Wand oder Säule."""
    r = case.standoff_diameter(case.heatset_m3) / 2 + case.standoff_fillet
    for x, y in case.standoff_positions():
        assert abs(x) + r <= case.case_length / 2, "Sockel an der ±X-Wand"
        assert abs(y) + r <= case.case_width / 2, "Sockel an der ±Y-Wand"
        for sx, sy in case.lid_screw_positions:
            assert math.dist((x, y), (sx, sy)) >= r + case.column_diameter / 2 - case.standoff_fillet, "Sockel in Ecksäule"


def test_jack_hole():
    assert case.jack_hole_width > case.jack_width
    assert case.jack_hole_height > case.jack_height
    assert case.jack_hole_fillet < min(case.jack_hole_width, case.jack_hole_height) / 2
    # Zwischen Platinenoberseite und Rand
    assert case.jack_hole_z - case.jack_hole_height / 2 >= case.pcb_top - 1e-6
    assert case.jack_hole_z + case.jack_hole_height / 2 < case.rim - 2
    # Stecker ragt außen heraus, sonst kommt man nicht mehr an die Rastnase
    assert case.plug_outside >= 5, f"Stecker nur {case.plug_outside:.1f} mm außen"


def test_lid_screws():
    assert case.lid_cbore_depth + 0.8 <= case.lid_thickness
    assert case.lid_screw_clearance > 3.0
    for x, y in case.vent_locations():
        for sx, sy in case.lid_screw_positions:
            assert math.dist((x, y), (sx, sy)) - case.vent_hole_radius >= case.lid_cbore_diameter / 2 + case.vent_web


def test_mockups_fit():
    bottom = case.build_bottom()
    mocks = case.build_mockups()
    for name, mock in mocks.items():
        overlap = bottom.intersect(mock)
        volume = sum(s.volume for s in overlap.solids()) if overlap is not None else 0.0
        assert volume < 1.0, f"{name} steckt mit {volume:.1f} mm³ in der Wanne"
        if name != "6P6C plug":
            assert mock.bounding_box().max.Z <= case.rim - case.headroom + 1e-6, f"{name} ragt in den Freiraum"
    # Module dürfen sich nicht gegenseitig durchdringen (Platinenlayout stimmig)
    names = [n for n in mocks if n not in ("pcb", "6P6C plug")]
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            overlap = mocks[a].intersect(mocks[b])
            volume = sum(s.volume for s in overlap.solids()) if overlap is not None else 0.0
            assert volume < 1.0, f"{a} und {b} überlappen"
    tallest = max(f[4] for f in case.module_features.values())
    assert tallest <= case.parts_height, f"{tallest} mm Bauteil über {case.parts_height} mm reserviert"


if __name__ == "__main__":
    test_thicknesses_print_solid()
    test_bottom()
    test_top()
    test_heatset()
    test_pcb_clears_columns()
    test_standoffs_clear_walls_and_columns()
    test_jack_hole()
    test_lid_screws()
    test_mockups_fit()
    print("ok")
