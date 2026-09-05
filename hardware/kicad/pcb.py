"""Generate the carrier PCB from the footprints in HCP.pretty and the net model in design.py.

Placement and routing are explicit coordinates. Run the file to rebuild the board,
run KiCad DRC on it and render a preview PNG.
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

OUTPUT_DIR = Path(__file__).parent
LIBRARY_DIR = OUTPUT_DIR / "HCP.pretty"
BOARD_PATH = OUTPUT_DIR / "hoermann-hcp-adapter.kicad_pcb"
PREVIEW_PATH = OUTPUT_DIR / "hoermann-hcp-adapter-pcb.png"
DRC_PATH = OUTPUT_DIR / "hoermann-hcp-adapter-drc.json"

BOARD_W, BOARD_H = 63.0, 42.0
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
PLACEMENT = {
    "J1": (10.78, 16.77, 180),
    "PS1": (36.95, 11.55, 0),
    "JP1": (60.8, 7.5, 0),
    "U2": (19.0, 32.5, 180),
    "U1": (49.55, 32.5, 90),
    "H1": (49.55, 36.0, 0),
}
REFERENCE_POSITIONS = {
    "J1": (7.6, 19.0),
    "PS1": (36.95, 18.5),
    "JP1": (60.8, 4.2),
    "U2": (19.0, 26.0),
    "U1": (52.5, 29.0),
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
    ("HCP_25V", "F.Cu", SIGNAL, ((4.43, 14.23), (5.7, 15.5), (5.7, 16.77), (5.7, 11.5))),
    ("HCP_25V", "F.Cu", POWER, ((5.7, 11.5), (5.7, 2.4), (16.5, 2.4))),
    ("HCP_GND", "F.Cu", SIGNAL, ((9.51, 14.23), (10.78, 15.5), (10.78, 16.77))),
    ("HCP_GND", "F.Cu", POWER, ((10.78, 16.77), (10.78, 20.7), (16.5, 20.7), (16.5, 22.6), (57.4, 22.6), (57.4, 20.7))),
    ("HCP_GND", "F.Cu", POWER, ((43.2, 22.6), (43.2, 24.88))),
    ("HCP_GND", "F.Cu", SIGNAL, ((43.2, 24.88), (43.2, 28.69), (36.0, 28.69))),
    ("BUCK_5V", "F.Cu", POWER, ((57.4, 2.4), (60.8, 5.8), (60.8, 7.5))),
    ("ESP_5V", "B.Cu", POWER, ((60.8, 10.04), (60.8, 23.3), (40.66, 23.3), (40.66, 24.88))),
    ("ESP_3V3", "F.Cu", SIGNAL, ((45.74, 24.88), (45.74, 30.0))),
    ("ESP_3V3", "B.Cu", SIGNAL, ((45.74, 30.0), (45.74, 32.5))),
    ("ESP_3V3", "F.Cu", SIGNAL, ((45.74, 32.5), (45.74, 36.31), (36.0, 36.31))),
    ("UART_RX_GPIO20", "F.Cu", SIGNAL, ((55.9, 40.12), (55.9, 31.23), (36.0, 31.23))),
    ("UART_TX_GPIO21", "B.Cu", SIGNAL, ((58.44, 40.12), (58.44, 37.0), (55.21, 33.77), (38.0, 33.77))),
    ("UART_TX_GPIO21", "F.Cu", SIGNAL, ((38.0, 33.77), (36.0, 33.77))),
    ("HCP_B_MINUS", "F.Cu", SIGNAL, ((8.24, 16.77), (8.24, 21.0), (4.6, 24.64), (4.6, 31.0), (3.1, 32.5), (2.0, 32.5))),
    ("HCP_A_PLUS", "B.Cu", SIGNAL, ((6.97, 14.23), (6.97, 37.58))),
    ("HCP_A_PLUS", "F.Cu", SIGNAL, ((6.97, 37.58), (2.0, 37.58))),
)
VIAS = (
    ("ESP_3V3", 45.74, 30.0),
    ("ESP_3V3", 45.74, 32.5),
    ("UART_TX_GPIO21", 38.0, 33.77),
    ("HCP_A_PLUS", 6.97, 37.58),
)
SILK_TEXTS = (
    ("HCP2-ESP32 v0.1", 7.6, 20.2, 0, 0.8),
    ("VERIFY FOOTPRINTS", 7.6, 21.3, 0, 0.8),
    ("VERIFY J1 PIN1", 7.6, 22.4, 0, 0.8),
    ("1", 12.5, 16.77, 0, 0.8),
    ("6", 2.8, 14.23, 0, 0.8),
    ("BUS", 60.8, 12.7, 0, 0.8),
    ("PWR", 60.8, 13.8, 0, 0.8),
    ("USB", 39.1, 32.5, 90, 0.8),
    ("ANT", 61.9, 32.5, 90, 0.8),
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
    for index, (text, x, y, rotation, size) in enumerate(SILK_TEXTS):
        board += (
            f'  (gr_text "{text}" (at {x} {y} {rotation}) (layer "F.SilkS") '
            f'(uuid "{object_uuid(f"text-{index}")}") '
            f"(effects (font (size {size} {size}) (thickness 0.15))))\n"
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


def render_preview():
    subprocess.run(
        [kicad_cli(), "pcb", "render", "--output", str(PREVIEW_PATH), "--width", "1600",
         "--height", "1100", "--side", "top", "--quality", "high", str(BOARD_PATH)],
        check=True,
    )


if __name__ == "__main__":
    build_board()
    run_drc()
    render_preview()
