"""Generate the carrier PCB from the footprints in HCP.pretty and the net model in design.py.

Placement and routing are explicit coordinates. Run the file to rebuild the KiCad project
in generated/, run KiCad DRC on it and render previews.
"""
import json
import math
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

from design import EXPECTED_CONNECTIONS

SOURCE_DIR = Path(__file__).parent
LIBRARY_DIR = SOURCE_DIR / "HCP.pretty"
OUTPUT_DIR = SOURCE_DIR / "generated"
BOARD_PATH = OUTPUT_DIR / "hoermann-hcp-adapter.kicad_pcb"
PROJECT_PATH = OUTPUT_DIR / "hoermann-hcp-adapter.kicad_pro"
FP_LIB_TABLE_PATH = OUTPUT_DIR / "fp-lib-table"
PREVIEW_TOP_PATH = OUTPUT_DIR / "hoermann-hcp-adapter-pcb-top.png"
PREVIEW_BOTTOM_PATH = OUTPUT_DIR / "hoermann-hcp-adapter-pcb-bottom.png"
PDF_PATH = OUTPUT_DIR / "hoermann-hcp-adapter-pcb.pdf"
DRC_PATH = OUTPUT_DIR / "hoermann-hcp-adapter-drc.json"

BOARD_W, BOARD_H = 65.0, 44.5
SIGNAL, POWER = 0.5, 0.8

NET_NAMES = tuple(EXPECTED_CONNECTIONS)
NET_IDS = {name: index for index, name in enumerate(NET_NAMES, start=1)}
PIN_NETS = {
    pin_id: net_name
    for net_name, pin_ids in EXPECTED_CONNECTIONS.items()
    for pin_id in pin_ids
}

FOOTPRINTS = {
    "J1": "RJ12_Amphenol_54601-x06_Horizontal",
    "PS1": "LM2596_HW-411",
    "JP1": "PinHeader_1x02_P2.54mm_Vertical",
    "U1": "ESP32-C3_SuperMini",
    "U2": "RS485_Isolated_34x18",
    "H1": "MountingHole_3.2mm_NoCourtyard",
}

# (x, y, rotation). J1 opening faces the top edge, PS1 IN side towards J1, U2 bus side
# on the left edge under J1, U1 with USB towards U2 and the antenna at the right edge.
# Roughly 2 mm between module outlines and 1.5 mm to the board edge.
PLACEMENT = {
    "J1": (11.28, 16.77, 180),
    "PS1": (38.45, 12.25, 0),
    "JP1": (63.0, 8.0, 0),
    "U2": (19.5, 34.0, 180),
    "U1": (52.26, 34.0, 90),
    "H1": (52.26, 37.5, 0),
}
REFERENCE_POSITIONS = {
    "J1": (8.1, 19.3),
    "PS1": (38.45, 19.2),
    "JP1": (63.0, 4.7),
    "U2": (19.5, 27.5),
    "U1": (55.2, 30.5),
}
VALUES = {
    "J1": "HCP2 6P6C",
    "PS1": "LM2596 HW-411",
    "JP1": "BUS_PWR",
    "U1": "ESP32-C3 Super Mini",
    "U2": "Isolated RS485",
    "H1": "M3",
}

# Points are absolute board coordinates. Pad centres are computed from the footprints
# and checked against the route vertices in check_routes().
ROUTES = (
    ("HCP_25V", "F.Cu", SIGNAL, ((4.93, 14.23), (6.2, 15.5), (6.2, 16.77), (6.2, 11.5))),
    ("HCP_25V", "F.Cu", POWER, ((6.2, 11.5), (6.2, 3.1), (18.0, 3.1))),
    ("HCP_GND", "F.Cu", SIGNAL, ((10.01, 14.23), (11.28, 15.5), (11.28, 16.77))),
    ("HCP_GND", "F.Cu", POWER, ((11.28, 16.77), (11.28, 21.4), (18.0, 21.4), (18.0, 23.9), (58.9, 23.9), (58.9, 21.4))),
    ("HCP_GND", "F.Cu", POWER, ((45.91, 23.9), (45.91, 26.38))),
    ("HCP_GND", "F.Cu", SIGNAL, ((45.91, 26.38), (45.91, 30.19), (36.5, 30.19))),
    ("BUCK_5V", "F.Cu", POWER, ((58.9, 3.1), (63.0, 7.2), (63.0, 8.0))),
    ("ESP_5V", "B.Cu", POWER, ((63.0, 10.54), (63.0, 24.6), (43.37, 24.6), (43.37, 26.38))),
    ("ESP_3V3", "F.Cu", SIGNAL, ((48.45, 26.38), (48.45, 31.5))),
    ("ESP_3V3", "B.Cu", SIGNAL, ((48.45, 31.5), (48.45, 34.0))),
    ("ESP_3V3", "F.Cu", SIGNAL, ((48.45, 34.0), (48.45, 37.81), (36.5, 37.81))),
    ("UART_RX_GPIO20", "F.Cu", SIGNAL, ((58.61, 41.62), (58.61, 32.73), (36.5, 32.73))),
    ("UART_TX_GPIO21", "B.Cu", SIGNAL, ((61.15, 41.62), (61.15, 38.5), (57.92, 35.27), (38.5, 35.27))),
    ("UART_TX_GPIO21", "F.Cu", SIGNAL, ((38.5, 35.27), (36.5, 35.27))),
    ("HCP_B_MINUS", "F.Cu", SIGNAL, ((8.74, 16.77), (8.74, 22.5), (5.1, 26.14), (5.1, 32.5), (3.6, 34.0), (2.5, 34.0))),
    ("HCP_A_PLUS", "B.Cu", SIGNAL, ((7.47, 14.23), (7.47, 39.08))),
    ("HCP_A_PLUS", "F.Cu", SIGNAL, ((7.47, 39.08), (2.5, 39.08))),
)
VIAS = (
    ("ESP_3V3", 48.45, 31.5),
    ("ESP_3V3", 48.45, 34.0),
    ("UART_TX_GPIO21", 38.5, 35.27),
    ("HCP_A_PLUS", 7.47, 39.08),
)
# (text, x, y, rotation, size, layer). Back-side texts are mirrored so they read
# correctly when looking at the bottom of the board.
SILK_TEXTS = (
    ("Hörmann v1.0", 8.1, 20.5, 0, 0.8, "F.SilkS"),
    ("VERIFY FOOTPRINTS", 8.1, 21.7, 0, 0.8, "F.SilkS"),
    ("VERIFY J1 PIN1", 8.1, 22.9, 0, 0.8, "F.SilkS"),
    ("1", 13.0, 16.77, 0, 0.8, "F.SilkS"),
    ("6", 3.3, 14.23, 0, 0.8, "F.SilkS"),
    ("BUS", 63.0, 13.0, 0, 0.8, "F.SilkS"),
    ("PWR", 63.0, 14.1, 0, 0.8, "F.SilkS"),
    ("DISCONNECT", 62.4, 19.6, 90, 0.8, "F.SilkS"),
    ("FOR USB", 63.6, 19.6, 90, 0.8, "F.SilkS"),
    ("USB", 41.7, 34.0, 90, 0.8, "F.SilkS"),
    ("ANT", 64.45, 34.0, 90, 0.8, "F.SilkS"),
    ("Hörmann HCP2 Adapter v1.0", 25.0, 30.5, 0, 1.5, "B.SilkS"),
    ("(C) 2026 Thies Gerken", 25.0, 33.5, 0, 1.2, "B.SilkS"),
)


def object_uuid(name):
    return uuid.uuid5(uuid.NAMESPACE_URL, f"hoermann-pcb:{name}")


def sexp_block(text, start):
    depth = 0
    quoted = False
    for index in range(start, len(text)):
        character = text[index]
        if character == '"' and text[index - 1] != "\\":
            quoted = not quoted
        elif not quoted and character == "(":
            depth += 1
        elif not quoted and character == ")":
            depth -= 1
            if depth == 0:
                return index + 1
    raise RuntimeError("Unterminated S-expression")


def rotate(x, y, degrees):
    # KiCad footprint rotation: positive is counter-clockwise on screen with y pointing down.
    angle = math.radians(degrees)
    return x * math.cos(angle) + y * math.sin(angle), -x * math.sin(angle) + y * math.cos(angle)


def pad_positions(footprint_text, x, y, rotation):
    positions = {}
    for match in re.finditer(r'\(pad "([^"]+)" \w+ \w+\s*\(at (-?[\d.]+) (-?[\d.]+)', footprint_text):
        number, px, py = match.group(1), float(match.group(2)), float(match.group(3))
        if number:
            dx, dy = rotate(px, py, rotation)
            positions[number] = (round(x + dx, 2), round(y + dy, 2))
    return positions


def place_footprint(ref):
    name = FOOTPRINTS[ref]
    text = (LIBRARY_DIR / f"{name}.kicad_mod").read_text()
    text = re.sub(r'^\s*\((version|generator|generator_version) [^\n]*\n', "", text, flags=re.MULTILINE)
    text = text.replace(f'(footprint "{name}"', f'(footprint "HCP:{name}"', 1)
    x, y, rotation = PLACEMENT[ref]
    text = text.replace('(layer "F.Cu")', f'(layer "F.Cu")\n  (uuid "{object_uuid(ref)}")\n  (at {x} {y} {rotation})', 1)
    text = re.sub(r'\(property "Reference" "[^"]*"', f'(property "Reference" "{ref}"', text, count=1)
    text = re.sub(r'\(property "Value" "[^"]*"', f'(property "Value" "{VALUES[ref]}"', text, count=1)
    if ref in REFERENCE_POSITIONS:
        # Property positions are footprint-relative; convert the absolute target back.
        rx, ry = REFERENCE_POSITIONS[ref]
        lx, ly = rotate(rx - x, ry - y, -rotation)
        text = re.sub(
            r'(\(property "Reference" "[^"]*"\s*\(at )[^)]*\)',
            lambda m: f"{m.group(1)}{lx:.2f} {ly:.2f} 0)",
            text,
            count=1,
        )

    def add_net(match):
        number = match.group(1)
        net_name = PIN_NETS.get(f"{ref}.{number}")
        end = sexp_block(text, match.start())
        block = text[match.start():end]
        if rotation:
            # Pad angles are stored absolute in board files, so rotated footprints
            # need the footprint angle on every pad to still match their library copy.
            block = re.sub(r"\(at (-?[\d.]+) (-?[\d.]+)\)", rf"(at \1 \2 {rotation})", block, count=1)
        if net_name:
            block = block[:-1] + f' (net {NET_IDS[net_name]} "{net_name}"))'
        return block

    result = ""
    cursor = 0
    for match in re.finditer(r'\(pad "([^"]*)"', text):
        if match.start() < cursor:
            continue
        end = sexp_block(text, match.start())
        result += text[cursor:match.start()] + add_net(match)
        cursor = end
    result += text[cursor:]
    return "  " + result.replace("\n", "\n  ").rstrip() + "\n", pad_positions(text, x, y, rotation)


def check_routes(pads):
    """Every net must touch each of its pads with a route vertex."""
    endpoints = {}
    for net_name, _, _, points in ROUTES:
        endpoints.setdefault(net_name, set()).update(points)
    for net_name, pin_ids in EXPECTED_CONNECTIONS.items():
        for pin_id in pin_ids:
            ref, number = pin_id.split(".")
            position = pads[ref][number]
            if position not in endpoints.get(net_name, ()):
                raise RuntimeError(f"{net_name}: no route ends on {pin_id} at {position}")


def segments(net_name, layer, width, points, index):
    result = ""
    for segment_index, (start, end) in enumerate(zip(points, points[1:])):
        result += (
            f'  (segment (start {start[0]} {start[1]}) (end {end[0]} {end[1]}) '
            f'(width {width}) (layer "{layer}") (net {NET_IDS[net_name]}) '
            f'(uuid "{object_uuid(f"segment-{index}-{segment_index}")}"))\n'
        )
    return result


def write_project():
    OUTPUT_DIR.mkdir(exist_ok=True)
    # H1 deliberately sits under the socketed ESP32, so that DRC check is switched off.
    PROJECT_PATH.write_text(json.dumps({
        "board": {"design_settings": {"rule_severities": {"npth_inside_courtyard": "ignore"}}},
        "meta": {"filename": PROJECT_PATH.name, "version": 3},
    }, indent=2) + "\n")
    FP_LIB_TABLE_PATH.write_text(
        "(fp_lib_table\n  (version 7)\n"
        '  (lib (name "HCP") (type "KiCad") (uri "${KIPRJMOD}/../HCP.pretty") (options "") (descr "Project footprints"))\n'
        ")\n"
    )


def build_board():
    board = (
        '(kicad_pcb\n  (version 20241229)\n  (generator "pcbnew")\n  (generator_version "9.0")\n'
        "  (general (thickness 1.6) (legacy_teardrops no))\n  (paper \"A4\")\n"
        '  (layers\n    (0 "F.Cu" signal)\n    (2 "B.Cu" signal)\n'
        '    (9 "F.Adhes" user "F.Adhesive")\n    (11 "B.Adhes" user "B.Adhesive")\n'
        '    (13 "F.Paste" user)\n    (15 "B.Paste" user)\n'
        '    (5 "F.SilkS" user "F.Silkscreen")\n    (7 "B.SilkS" user "B.Silkscreen")\n'
        '    (1 "F.Mask" user)\n    (3 "B.Mask" user)\n'
        '    (17 "Dwgs.User" user "User.Drawings")\n    (19 "Cmts.User" user "User.Comments")\n'
        '    (21 "Eco1.User" user "User.Eco1")\n    (23 "Eco2.User" user "User.Eco2")\n'
        '    (25 "Edge.Cuts" user)\n    (27 "Margin" user)\n'
        '    (31 "F.CrtYd" user "F.Courtyard")\n    (29 "B.CrtYd" user "B.Courtyard")\n'
        '    (35 "F.Fab" user)\n    (33 "B.Fab" user)\n  )\n'
        "  (setup (pad_to_mask_clearance 0) (allow_soldermask_bridges_in_footprints no))\n"
        '  (net 0 "")\n'
    )
    for name, net_id in NET_IDS.items():
        board += f'  (net {net_id} "{name}")\n'

    pads = {}
    for ref in FOOTPRINTS:
        text, positions = place_footprint(ref)
        board += text
        pads[ref] = positions
    check_routes(pads)

    for index, route in enumerate(ROUTES):
        board += segments(*route, index)
    for index, (net_name, x, y) in enumerate(VIAS):
        board += (
            f'  (via (at {x} {y}) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") '
            f'(net {NET_IDS[net_name]}) (uuid "{object_uuid(f"via-{index}")}"))\n'
        )

    board += (
        f'  (gr_rect (start 0 0) (end {BOARD_W} {BOARD_H}) (stroke (width 0.1) (type default)) '
        f'(fill none) (layer "Edge.Cuts") (uuid "{object_uuid("board-outline")}"))\n'
    )
    for index, (text, x, y, rotation, size, layer) in enumerate(SILK_TEXTS):
        mirror = " (justify mirror)" if layer.startswith("B.") else ""
        board += (
            f'  (gr_text "{text}" (at {x} {y} {rotation}) (layer "{layer}") '
            f'(uuid "{object_uuid(f"text-{index}")}") '
            f"(effects (font (size {size} {size}) (thickness 0.15)){mirror}))\n"
        )
    board += "  (embedded_fonts no)\n)\n"
    BOARD_PATH.write_text(board)


def kicad_cli():
    found = shutil.which("kicad-cli") or "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
    if not Path(found).is_file():
        raise RuntimeError("kicad-cli is required")
    return found


def run_drc():
    subprocess.run(
        [kicad_cli(), "pcb", "drc", "--format", "json", "--severity-all",
         "--output", str(DRC_PATH), str(BOARD_PATH)],
        check=True,
    )
    report = json.loads(DRC_PATH.read_text())
    problems = [v for v in report["violations"] if v["severity"] == "error"]
    problems += report["unconnected_items"]
    for item in problems + [v for v in report["violations"] if v["severity"] == "warning"]:
        print(f'{item["severity"]}: {item["type"]}: {item["description"]}', file=sys.stderr)
    if problems:
        raise SystemExit(f"DRC failed with {len(problems)} error(s)")


def render_previews():
    for side, path in (("top", PREVIEW_TOP_PATH), ("bottom", PREVIEW_BOTTOM_PATH)):
        subprocess.run(
            [kicad_cli(), "pcb", "render", "--output", str(path), "--width", "1600",
             "--height", "1100", "--side", side, "--quality", "high", str(BOARD_PATH)],
            check=True,
        )
    subprocess.run(
        [kicad_cli(), "pcb", "export", "pdf", "--output", str(PDF_PATH),
         "--layers", "F.Cu,B.Cu,F.SilkS,B.SilkS,Edge.Cuts", "--mode-multipage",
         "--include-border-title", str(BOARD_PATH)],
        check=True,
    )


if __name__ == "__main__":
    write_project()
    build_board()
    run_drc()
    render_previews()
