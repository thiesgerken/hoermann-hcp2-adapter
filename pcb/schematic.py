"""Generate the KiCad schematic from the net model in design.py.

Symbols, wire routes, and labels use explicit coordinates on the 1.27 mm grid.
The script writes hcp.kicad_sch beside the generator, runs KiCad ERC, exports
the netlist, checks it against EXPECTED_CONNECTIONS, and renders the PDF.
"""
import json
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

from design import EXPECTED_CONNECTIONS, git_version

SOURCE_DIR = Path(__file__).parent
OUTPUT_DIR = SOURCE_DIR
SCHEMATIC_PATH = OUTPUT_DIR / "hcp.kicad_sch"
NETLIST_PATH = OUTPUT_DIR / "hcp.net"
PDF_PATH = OUTPUT_DIR / "hcp-schematic.pdf"
ERC_PATH = OUTPUT_DIR / "hcp-erc.json"
PROJECT_NAME = "hcp"
GND_NET = "HCP_GND"

# Each part: symbol body half width, pins as (number, name, electrical type, side, dy).
# dy is the schematic offset of the pin below the symbol origin, on the 1.27 mm grid.
# Sides only matter for the drawing; the footprints define the real pin positions.
PARTS = {
    "J1": {
        "value": "HCP2 6P6C",
        "footprint": "HCP:RJ12_Amphenol_54601-x06_Horizontal",
        "at": (40.64, 88.9),
        "half_width": 10.16,
        "pins": (
            (6, "+25V", "passive", "right", -6.35),
            (5, "+25V", "power_out", "right", -3.81),
            (4, "A+", "passive", "right", -1.27),
            (3, "B-", "passive", "right", 1.27),
            (2, "GND", "passive", "right", 3.81),
            (1, "GND", "power_out", "right", 6.35),
        ),
    },
    "PS1": {
        "value": "LM2596 HW-411, 5.0 V",
        "footprint": "HCP:LM2596_HW-411",
        "at": (111.76, 63.5),
        "half_width": 10.16,
        "pins": (
            (1, "IN+", "power_in", "left", -2.54),
            (2, "IN-", "passive", "left", 2.54),
            (3, "OUT+", "power_out", "right", -2.54),
            (4, "OUT-", "passive", "right", 2.54),
        ),
    },
    "JP1": {
        "value": "BUS_PWR",
        "footprint": "HCP:PinHeader_1x02_P2.54mm_Vertical",
        "at": (160.02, 60.96),
        "half_width": 5.08,
        "pins": (
            (1, "1", "passive", "left", 0),
            (2, "2", "power_out", "right", 0),
        ),
    },
    "U2": {
        "value": "Isolated RS485, auto direction, 120R",
        "footprint": "HCP:RS485_Isolated_34x18",
        "at": (111.76, 114.3),
        "half_width": 10.16,
        "pins": (
            (5, "A+", "bidirectional", "left", -5.08),
            (6, "B+", "bidirectional", "left", 0),
            (7, "EARTH/NC", "passive", "left", 5.08),
            (1, "VIN", "power_in", "right", -3.81),
            (2, "TX", "input", "right", -1.27),
            (3, "RX", "output", "right", 1.27),
            (4, "GND", "power_in", "right", 3.81),
        ),
    },
    "U1": {
        "value": "ESP32-C3 Super Mini",
        "footprint": "HCP:ESP32-C3_SuperMini",
        "at": (210.82, 104.14),
        "half_width": 12.7,
        "pins": (
            (1, "5V", "power_in", "left", -8.89),
            (5, "3V3", "power_out", "left", -6.35),
            (16, "GPIO21/U0TXD", "output", "left", -1.27),
            (14, "GPIO20/U0RXD", "input", "left", 1.27),
            (3, "GND", "power_in", "left", 6.35),
            (7, "GPIO4", "bidirectional", "right", -8.89),
            (9, "GPIO3", "bidirectional", "right", -6.35),
            (11, "GPIO2", "bidirectional", "right", -3.81),
            (13, "GPIO1", "bidirectional", "right", -1.27),
            (15, "GPIO0", "bidirectional", "right", 1.27),
            (2, "GPIO5", "bidirectional", "right", 3.81),
            (4, "GPIO6", "bidirectional", "right", 6.35),
            (6, "GPIO7", "bidirectional", "right", 8.89),
            (8, "GPIO8/LED", "bidirectional", "right", 11.43),
            (10, "GPIO9/BOOT", "bidirectional", "right", 13.97),
            (12, "GPIO10", "bidirectional", "right", 16.51),
        ),
    },
}
PIN_LENGTH = 2.54

# Wires as point lists. Every net pin must be the first or last point of some wire.
WIRES = {
    "HCP_25V": (
        ((53.34, 85.09), (60.96, 85.09), (60.96, 60.96), (99.06, 60.96)),
        ((53.34, 82.55), (60.96, 82.55)),
    ),
    GND_NET: (
        ((53.34, 92.71), (58.42, 92.71), (58.42, 101.6)),
        ((53.34, 95.25), (58.42, 95.25)),
        ((99.06, 66.04), (93.98, 66.04), (93.98, 71.12)),
        ((124.46, 66.04), (129.54, 66.04), (129.54, 71.12)),
        ((124.46, 118.11), (129.54, 118.11), (129.54, 123.19)),
        ((195.58, 110.49), (190.5, 110.49), (190.5, 115.57)),
    ),
    "HCP_A_PLUS": (((53.34, 87.63), (66.04, 87.63), (66.04, 109.22), (99.06, 109.22)),),
    "HCP_B_MINUS": (((53.34, 90.17), (63.5, 90.17), (63.5, 114.3), (99.06, 114.3)),),
    "BUCK_5V": (((124.46, 60.96), (152.4, 60.96)),),
    "ESP_5V": (((167.64, 60.96), (185.42, 60.96), (185.42, 95.25), (195.58, 95.25)),),
    "ESP_3V3": (((195.58, 97.79), (180.34, 97.79), (180.34, 110.49), (124.46, 110.49)),),
    "UART_TX_GPIO21": (((195.58, 102.87), (182.88, 102.87), (182.88, 113.03), (124.46, 113.03)),),
    "UART_RX_GPIO20": (((195.58, 105.41), (187.96, 105.41), (187.96, 115.57), (124.46, 115.57)),),
}
# Ground symbols sit at the open end of the GND wires.
GND_SYMBOLS = ((58.42, 101.6), (93.98, 71.12), (129.54, 71.12), (129.54, 123.19), (190.5, 115.57))
# (net, x, y, rotation); the anchor must lie on a wire of that net.
LABELS = (
    ("HCP_25V", 76.2, 60.96, 0),
    ("HCP_A_PLUS", 76.2, 109.22, 0),
    ("HCP_B_MINUS", 76.2, 114.3, 0),
    ("BUCK_5V", 134.62, 60.96, 0),
    ("ESP_5V", 185.42, 78.74, 90),
    ("ESP_3V3", 152.4, 110.49, 0),
    ("UART_TX_GPIO21", 152.4, 113.03, 0),
    ("UART_RX_GPIO20", 152.4, 115.57, 0),
)
NOTES = (
    ("HCP2 bus, 6P6C. Contact numbering per ESPHome HCP documentation.", 25.4, 128.27),
    ("Adjust PS1 to 5.0 V before connecting U1. Open JP1 whenever USB is plugged into U1.", 99.06, 45.72),
    ("U2 is powered from 3V3 so its RX output stays at ESP32 logic level.", 99.06, 132.08),
)


def object_uuid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"hoermann-sch:{name}"))


ROOT_UUID = object_uuid("root")
FONT = "(effects (font (size 1.27 1.27)))"


def num(value):
    return f"{round(value, 2):g}"


def on_segment(point, start, end):
    (x, y), (x0, y0), (x1, y1) = point, start, end
    return min(x0, x1) - 1e-6 <= x <= max(x0, x1) + 1e-6 and min(y0, y1) - 1e-6 <= y <= max(y0, y1) + 1e-6


def junctions():
    """T-connections only conduct in KiCad when a junction sits on them."""
    segments = [(net, a, b) for net, wires in WIRES.items() for pts in wires for a, b in zip(pts, pts[1:])]
    result = set()
    for net, wires in WIRES.items():
        for pts in wires:
            for point in (pts[0], pts[-1]):
                for other_net, a, b in segments:
                    if other_net == net and point not in (a, b) and on_segment(point, a, b):
                        result.add(point)
    return sorted(result)


def pin_end(ref, number):
    part = PARTS[ref]
    x, y = part["at"]
    for pin_number, _, _, side, dy in part["pins"]:
        if pin_number == number:
            offset = part["half_width"] + PIN_LENGTH
            return (round(x - offset if side == "left" else x + offset, 2), round(y + dy, 2))
    raise KeyError(f"{ref}.{number}")


def lib_symbol(ref):
    part = PARTS[ref]
    name = f"HCP:{ref}"
    hw = part["half_width"]
    dys = [dy for *_, dy in part["pins"]]
    top, bottom = min(dys) - 2.54, max(dys) + 2.54
    # Library symbols use y pointing up, so schematic offsets are negated here.
    result = (
        f'    (symbol "{name}" (pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)\n'
        f'      (property "Reference" "{ref}" (at 0 {num(-top + 1.27)} 0) {FONT})\n'
        f'      (property "Value" "{part["value"]}" (at 0 {num(-bottom - 1.27)} 0) {FONT})\n'
        f'      (property "Footprint" "{part["footprint"]}" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
        f'      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
        f'      (symbol "{ref}_0_1"\n'
        f"        (rectangle (start {num(-hw)} {num(-top)}) (end {num(hw)} {num(-bottom)}) "
        "(stroke (width 0.254) (type default)) (fill (type background)))\n"
        "      )\n"
        f'      (symbol "{ref}_1_1"\n'
    )
    for number, pin_name, kind, side, dy in part["pins"]:
        x = -(hw + PIN_LENGTH) if side == "left" else hw + PIN_LENGTH
        angle = 0 if side == "left" else 180
        result += (
            f"        (pin {kind} line (at {num(x)} {num(-dy)} {angle}) (length {PIN_LENGTH}) "
            f'(name "{pin_name}" {FONT}) (number "{number}" {FONT}))\n'
        )
    return result + "      )\n    )\n"


def gnd_lib_symbol():
    return (
        f'    (symbol "HCP:{GND_NET}" (power) (pin_numbers hide) (pin_names (offset 0) hide) (exclude_from_sim no) (in_bom no) (on_board no)\n'
        f'      (property "Reference" "#PWR" (at 0 -6.35 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
        f'      (property "Value" "{GND_NET}" (at 0 -3.81 0) {FONT})\n'
        '      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
        '      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
        f'      (symbol "{GND_NET}_0_1"\n'
        "        (polyline (pts (xy 0 0) (xy 0 -1.27)) (stroke (width 0) (type default)) (fill (type none)))\n"
        "        (polyline (pts (xy -1.27 -1.27) (xy 1.27 -1.27)) (stroke (width 0) (type default)) (fill (type none)))\n"
        "        (polyline (pts (xy -0.762 -1.905) (xy 0.762 -1.905)) (stroke (width 0) (type default)) (fill (type none)))\n"
        "        (polyline (pts (xy -0.254 -2.54) (xy 0.254 -2.54)) (stroke (width 0) (type default)) (fill (type none)))\n"
        "      )\n"
        f'      (symbol "{GND_NET}_1_1"\n'
        f'        (pin power_in line (at 0 0 90) (length 0) (name "{GND_NET}" {FONT}) (number "1" {FONT}))\n'
        "      )\n    )\n"
    )


def symbol_instance(ref):
    part = PARTS[ref]
    x, y = part["at"]
    dys = [dy for *_, dy in part["pins"]]
    result = (
        f'  (symbol (lib_id "HCP:{ref}") (at {x} {y} 0) (unit 1) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)\n'
        f'    (uuid "{object_uuid(ref)}")\n'
        f'    (property "Reference" "{ref}" (at {x} {num(y + min(dys) - 3.81)} 0) {FONT})\n'
        f'    (property "Value" "{part["value"]}" (at {x} {num(y + max(dys) + 3.81)} 0) {FONT})\n'
        f'    (property "Footprint" "{part["footprint"]}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
        f'    (property "Datasheet" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
    )
    for number, *_ in part["pins"]:
        result += f'    (pin "{number}" (uuid "{object_uuid(f"{ref}-pin-{number}")}"))\n'
    result += (
        f'    (instances (project "{PROJECT_NAME}" (path "/{ROOT_UUID}" (reference "{ref}") (unit 1))))\n'
        "  )\n"
    )
    return result


def gnd_instance(index, x, y):
    ref = f"#PWR{index:02d}"
    return (
        f'  (symbol (lib_id "HCP:{GND_NET}") (at {x} {y} 0) (unit 1) (exclude_from_sim no) (in_bom no) (on_board no) (dnp no)\n'
        f'    (uuid "{object_uuid(ref)}")\n'
        f'    (property "Reference" "{ref}" (at {x} {num(y + 6.35)} 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
        f'    (property "Value" "{GND_NET}" (at {x} {num(y + 4.45)} 0) {FONT})\n'
        f'    (property "Footprint" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
        f'    (property "Datasheet" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
        f'    (pin "1" (uuid "{object_uuid(f"{ref}-pin")}"))\n'
        f'    (instances (project "{PROJECT_NAME}" (path "/{ROOT_UUID}" (reference "{ref}") (unit 1))))\n'
        "  )\n"
    )


def connected_pins():
    return {pin_id for pin_ids in EXPECTED_CONNECTIONS.values() for pin_id in pin_ids}


def check_wires():
    """Every expected pin needs a wire end on it; unexpected wire ends on pins are errors."""
    ends = {}
    for net_name, wires in WIRES.items():
        for points in wires:
            for point in (points[0], points[-1]):
                ends.setdefault(point, set()).add(net_name)
    for net_name, pin_ids in EXPECTED_CONNECTIONS.items():
        for pin_id in pin_ids:
            ref, number = pin_id.split(".")
            point = pin_end(ref, int(number))
            if net_name not in ends.get(point, ()):
                raise RuntimeError(f"{net_name}: no wire ends on {pin_id} at {point}")
    for net_name, x, y, _ in LABELS:
        on_wire = any(
            min(a[0], b[0]) <= x <= max(a[0], b[0]) and min(a[1], b[1]) <= y <= max(a[1], b[1])
            for points in WIRES[net_name]
            for a, b in zip(points, points[1:])
        )
        if not on_wire:
            raise RuntimeError(f"Label {net_name} at ({x}, {y}) is not on one of its wires")


def build_schematic():
    check_wires()
    OUTPUT_DIR.mkdir(exist_ok=True)
    text = (
        '(kicad_sch (version 20231120) (generator "hoermann-schematic") (generator_version "1")\n'
        f'  (uuid "{ROOT_UUID}")\n  (paper "A4")\n'
        f'  (title_block (title "Hörmann HCP2 ESP32-C3 Adapter") (date "2026-09-05") (rev "{git_version()}") '
        '(company "Thies Gerken"))\n'
        "  (lib_symbols\n"
    )
    for ref in PARTS:
        text += lib_symbol(ref)
    text += gnd_lib_symbol() + "  )\n"
    for ref in PARTS:
        text += symbol_instance(ref)
    for index, (x, y) in enumerate(GND_SYMBOLS, start=1):
        text += gnd_instance(index, x, y)
    for net_name, wires in WIRES.items():
        for wire_index, points in enumerate(wires):
            for segment_index, (start, end) in enumerate(zip(points, points[1:])):
                text += (
                    f"  (wire (pts (xy {start[0]} {start[1]}) (xy {end[0]} {end[1]})) "
                    f"(stroke (width 0) (type default)) "
                    f'(uuid "{object_uuid(f"wire-{net_name}-{wire_index}-{segment_index}")}"))\n'
                )
    for x, y in junctions():
        text += f'  (junction (at {x} {y}) (diameter 0) (color 0 0 0 0) (uuid "{object_uuid(f"junction-{x}-{y}")}"))\n'
    for net_name, x, y, rotation in LABELS:
        text += (
            f'  (label "{net_name}" (at {x} {y} {rotation}) (fields_autoplaced yes) '
            f'(effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "{object_uuid(f"label-{net_name}")}"))\n'
        )
    used = connected_pins()
    for ref, part in PARTS.items():
        for number, *_ in part["pins"]:
            if f"{ref}.{number}" not in used:
                x, y = pin_end(ref, number)
                text += f'  (no_connect (at {x} {y}) (uuid "{object_uuid(f"nc-{ref}-{number}")}"))\n'
    for index, (note, x, y) in enumerate(NOTES):
        text += (
            f'  (text "{note}" (exclude_from_sim no) (at {x} {y} 0) '
            f'(effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "{object_uuid(f"note-{index}")}"))\n'
        )
    text += '  (sheet_instances (path "/" (page "1")))\n)\n'
    SCHEMATIC_PATH.write_text(text)


def kicad_cli():
    found = shutil.which("kicad-cli") or "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
    if not Path(found).is_file():
        raise RuntimeError("kicad-cli is required")
    return found


def run_erc():
    subprocess.run(
        [kicad_cli(), "sch", "erc", "--format", "json", "--severity-all", "--output", str(ERC_PATH),
         str(SCHEMATIC_PATH)],
        check=True,
    )
    violations = [v for sheet in json.loads(ERC_PATH.read_text())["sheets"] for v in sheet["violations"]]
    for item in violations:
        print(f'{item["severity"]}: {item["type"]}: {item["description"]}', file=sys.stderr)
    if any(item["severity"] == "error" for item in violations):
        raise SystemExit("ERC failed")


def export_netlist():
    subprocess.run(
        [kicad_cli(), "sch", "export", "netlist", "--format", "kicadsexpr", "--output", str(NETLIST_PATH),
         str(SCHEMATIC_PATH)],
        check=True,
    )
    netlist = NETLIST_PATH.read_text()
    actual = {}
    for block in re.split(r"\n\t\t\(net\n", netlist.split("(nets", 1)[1])[1:]:
        name = re.search(r'\(name "([^"]+)"\)', block).group(1).lstrip("/")
        if name.startswith("unconnected-"):
            continue
        nodes = re.findall(r'\(ref "([^"]+)"\)\s*\(pin "([^"]+)"\)', block)
        actual[name] = {f"{ref}.{pin}" for ref, pin in nodes}
    if actual != EXPECTED_CONNECTIONS:
        raise RuntimeError(f"Netlist differs from design.py:\n{actual}\nvs\n{EXPECTED_CONNECTIONS}")


def render_pdf():
    subprocess.run(
        [kicad_cli(), "sch", "export", "pdf", "--output", str(PDF_PATH), str(SCHEMATIC_PATH)],
        check=True,
    )


if __name__ == "__main__":
    build_schematic()
    run_erc()
    export_netlist()
    render_pdf()
