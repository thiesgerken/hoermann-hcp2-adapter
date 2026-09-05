import shutil
import subprocess
import uuid
from pathlib import Path

from design import EXPECTED_CONNECTIONS

OUTPUT_DIR = Path(__file__).parent
BOARD_PATH = OUTPUT_DIR / "hoermann-hcp-adapter.kicad_pcb"
PREVIEW_PATH = OUTPUT_DIR / "hoermann-hcp-adapter-pcb.png"

NET_NAMES = (
    "HCP_GND",
    "HCP_25V",
    "HCP_A_PLUS",
    "HCP_B_MINUS",
    "BUCK_5V",
    "ESP_5V",
    "ESP_3V3",
    "UART_TX_GPIO21",
    "UART_RX_GPIO20",
)
NET_IDS = {name: index for index, name in enumerate(NET_NAMES, start=1)}
PIN_NETS = {
    pin_id: net_name
    for net_name, pin_ids in EXPECTED_CONNECTIONS.items()
    for pin_id in pin_ids
}


def object_uuid(name):
    return uuid.uuid5(uuid.NAMESPACE_URL, f"hoermann-pcb:{name}")


def effects():
    return '(effects (font (size 1 1) (thickness 0.15)))'


def pad(ref, number, x, y, kind="thru_hole"):
    net_name = PIN_NETS.get(f"{ref}.{number}")
    net = f' (net {NET_IDS[net_name]} "{net_name}")' if net_name else ""
    shape = "rect" if str(number) == "1" else "circle"
    if kind == "smd":
        return (
            f'    (pad "{number}" smd {shape} (at {x} {y}) (size 2.0 2.0) '
            f'(layers "F.Cu" "F.Paste" "F.Mask"){net} '
            f'(uuid "{object_uuid(f"{ref}-pad-{number}")}"))\n'
        )
    return (
        f'    (pad "{number}" thru_hole {shape} (at {x} {y}) (size 2.2 2.2) '
        f'(drill 1.0) (layers "*.Cu" "*.Mask"){net} '
        f'(uuid "{object_uuid(f"{ref}-pad-{number}")}"))\n'
    )


def footprint(ref, value, x, y, width, height, pads, note):
    result = (
        f'  (footprint "HCP:{ref}"\n'
        '    (layer "F.Cu")\n'
        f'    (uuid "{object_uuid(ref)}")\n'
        f'    (at {x} {y})\n'
        f'    (property "Reference" "{ref}" (at {width / 2} -3 0) '
        f'(layer "F.SilkS") (uuid "{object_uuid(f"{ref}-reference")}") {effects()})\n'
        f'    (property "Value" "{value}" (at {width / 2} {height + 3} 0) '
        f'(layer "F.Fab") (hide yes) (uuid "{object_uuid(f"{ref}-value")}") {effects()})\n'
        f'    (fp_rect (start -2 -4) (end {width + 2} {height + 4}) '
        f'(stroke (width 0.35) (type default)) (fill none) (layer "F.SilkS") '
        f'(uuid "{object_uuid(f"{ref}-outline")}"))\n'
        f'    (fp_text user "{note}" (at {width / 2} {height / 2} 0) '
        f'(layer "F.Fab") (hide yes) (uuid "{object_uuid(f"{ref}-note")}") '
        '(effects (font (size 0.8 0.8) (thickness 0.12))))\n'
    )
    for number, pad_x, pad_y, kind in pads:
        result += pad(ref, number, pad_x, pad_y, kind)
    return result + "    (attr board_only)\n    (embedded_fonts no)\n  )\n"


def segment(net_name, layer, width, points, index):
    result = ""
    for segment_index, (start, end) in enumerate(zip(points, points[1:])):
        result += (
            f'  (segment (start {start[0]} {start[1]}) (end {end[0]} {end[1]}) '
            f'(width {width}) (layer "{layer}") (net {NET_IDS[net_name]}) '
            f'(uuid "{object_uuid(f"segment-{index}-{segment_index}")}"))\n'
        )
    return result

def via(net_name, x, y, index):
    return (
        f'  (via (at {x} {y}) (size 1.8) (drill 0.8) '
        f'(layers "F.Cu" "B.Cu") (net {NET_IDS[net_name]}) '
        f'(uuid "{object_uuid(f"via-{index}")}"))\n'
    )


def mounting_hole(index, x, y):
    return (
        f'  (footprint "MountingHole:{index}" (layer "F.Cu") '
        f'(uuid "{object_uuid(f"mount-{index}")}") (at {x} {y}) '
        f'(property "Reference" "H{index}" (at 0 -4 0) (layer "F.SilkS") '
        f'(hide yes) (uuid "{object_uuid(f"mount-{index}-ref")}") {effects()}) '
        f'(property "Value" "M3" (at 0 4 0) (layer "F.Fab") (hide yes) '
        f'(uuid "{object_uuid(f"mount-{index}-value")}") {effects()}) '
        f'(pad "" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) '
        f'(layers "*.Cu" "*.Mask") (uuid "{object_uuid(f"mount-{index}-pad")}")) '
        '(attr board_only) (embedded_fonts no))\n'
    )


def build_board():
    j1_pads = [(number, 0, (number - 1) * 2.54, "thru_hole") for number in range(1, 7)]
    ps1_pads = [(1, 0, 0, "thru_hole"), (2, 0, 11, "thru_hole"),
                (3, 40, 0, "thru_hole"), (4, 40, 11, "thru_hole")]
    jp1_pads = [(1, 0, 0, "thru_hole"), (2, 2.54, 0, "thru_hole")]
    u2_pads = [(5, 0, 0, "smd"), (6, 0, 5.08, "smd"), (7, 0, 10.16, "smd"),
               (1, 34, 0, "smd"), (2, 34, 2.54, "smd"),
               (3, 34, 5.08, "smd"), (4, 34, 7.62, "smd")]
    u1_pads = []
    for row in range(8):
        u1_pads.append((1 + row * 2, 0, row * 2.54, "thru_hole"))
        u1_pads.append((2 + row * 2, 15.24, row * 2.54, "thru_hole"))

    board = """(kicad_pcb
  (version 20241229)
  (generator \"pcbnew\")
  (generator_version \"9.0\")
  (general (thickness 1.6) (legacy_teardrops no))
  (paper \"A4\")
  (layers
    (0 \"F.Cu\" signal)
    (2 \"B.Cu\" signal)
    (9 \"F.Adhes\" user \"F.Adhesive\")
    (11 \"B.Adhes\" user \"B.Adhesive\")
    (13 \"F.Paste\" user)
    (15 \"B.Paste\" user)
    (5 \"F.SilkS\" user \"F.Silkscreen\")
    (7 \"B.SilkS\" user \"B.Silkscreen\")
    (1 \"F.Mask\" user)
    (3 \"B.Mask\" user)
    (17 \"Dwgs.User\" user \"User.Drawings\")
    (19 \"Cmts.User\" user \"User.Comments\")
    (21 \"Eco1.User\" user \"User.Eco1\")
    (23 \"Eco2.User\" user \"User.Eco2\")
    (25 \"Edge.Cuts\" user)
    (27 \"Margin\" user)
    (31 \"F.CrtYd\" user \"F.Courtyard\")
    (29 \"B.CrtYd\" user \"B.Courtyard\")
    (35 \"F.Fab\" user)
    (33 \"B.Fab\" user)
  )
  (setup (pad_to_mask_clearance 0) (allow_soldermask_bridges_in_footprints no))
"""
    board += '  (net 0 "")\n'
    for name, net_id in NET_IDS.items():
        board += f'  (net {net_id} "{name}")\n'

    board += footprint("J1", "HCP2 6P6C", 8, 20, 0, 12.7, j1_pads, "VERIFY RJ12")
    board += footprint("PS1", "LM2596 HW-411", 20, 48, 40, 11, ps1_pads, "VERIFY 45x22")
    board += footprint("JP1", "BUS_PWR", 65, 48, 2.54, 0, jp1_pads, "OPEN FOR USB")
    board += footprint("U2", "Isolated RS485", 25, 20, 34, 10.16, u2_pads, "VERIFY 34x18")
    board += footprint("U1", "ESP32-C3 Super Mini", 72, 14, 15.24, 17.78, u1_pads, "ANTENNA CLEAR")
    for index, position in enumerate(((4, 4), (96, 4), (4, 66), (96, 66)), start=1):
        board += mounting_hole(index, *position)

    routes = (
        ("HCP_A_PLUS", "B.Cu", 0.35, ((8, 27.62), (6, 27.62), (6, 15), (23, 15), (23, 20))),
        ("HCP_A_PLUS", "F.Cu", 0.35, ((23, 20), (25, 20))),
        ("HCP_B_MINUS", "B.Cu", 0.35, ((8, 25.08), (23, 25.08))),
        ("HCP_B_MINUS", "F.Cu", 0.35, ((23, 25.08), (25, 25.08))),
        ("HCP_25V", "B.Cu", 0.8, ((8, 32.7), (8, 30.16), (12, 30.16), (12, 48), (20, 48))),
        ("HCP_GND", "F.Cu", 0.8, ((8, 20), (8, 22.54), (10, 22.54), (10, 38), (20, 38))),
        ("HCP_GND", "F.Cu", 0.8, ((20, 38), (55, 38), (59, 38), (68, 38))),
        ("HCP_GND", "F.Cu", 0.8, ((20, 59), (16, 59), (16, 38), (20, 38))),
        ("HCP_GND", "F.Cu", 0.8, ((60, 59), (55, 59), (55, 38))),
        ("HCP_GND", "F.Cu", 0.8, ((59, 27.62), (59, 38))),
        ("HCP_GND", "F.Cu", 0.8, ((72, 16.54), (68, 16.54), (68, 38))),
        ("ESP_3V3", "F.Cu", 0.35, ((59, 20), (61, 20))),
        ("ESP_3V3", "B.Cu", 0.35, ((61, 20), (65, 20), (65, 19.08), (72, 19.08))),
        ("UART_TX_GPIO21", "F.Cu", 0.35, ((59, 22.54), (61, 22.54))),
        ("UART_TX_GPIO21", "B.Cu", 0.35, ((61, 22.54), (55, 22.54), (55, 10), (92, 10), (92, 31.78), (87.24, 31.78))),
        ("UART_RX_GPIO20", "F.Cu", 0.35, ((59, 25.08), (61, 25.08))),
        ("UART_RX_GPIO20", "B.Cu", 0.35, ((61, 25.08), (61, 35), (82, 35), (82, 29.24), (87.24, 29.24))),
        ("BUCK_5V", "F.Cu", 0.8, ((60, 48), (65, 48))),
        ("ESP_5V", "F.Cu", 0.8, ((67.54, 48), (97, 48), (97, 8), (72, 8), (72, 14))),
    )
    for index, (net_name, layer, width, points) in enumerate(routes):
        board += segment(net_name, layer, width, points, index)
    for index, (net_name, x, y) in enumerate(
        (
            ("HCP_A_PLUS", 23, 20),
            ("HCP_B_MINUS", 23, 25.08),
            ("ESP_3V3", 61, 20),
            ("UART_TX_GPIO21", 61, 22.54),
            ("UART_RX_GPIO20", 61, 25.08),
        )
    ):
        board += via(net_name, x, y, index)

    board += (
        f'  (gr_rect (start 0 0) (end 100 70) (stroke (width 0.5) (type default)) '
        f'(fill none) (layer "Edge.Cuts") (uuid "{object_uuid("board-outline")}"))\n'
        f'  (gr_text "PROVISIONAL - VERIFY ALL FOOTPRINTS" (at 50 67) (layer "F.SilkS") '
        f'(uuid "{object_uuid("warning-text")}") '
        '(effects (font (size 1.5 1.5) (thickness 0.3))))\n'
        f'  (gr_text "HCP2 ESP32-C3 ADAPTER" (at 50 4) (layer "F.SilkS") '
        f'(uuid "{object_uuid("title-text")}") '
        '(effects (font (size 1.5 1.5) (thickness 0.3))))\n'
        '  (embedded_fonts no)\n)\n'
    )
    BOARD_PATH.write_text(board)


def render_preview():
    kicad_cli = shutil.which("kicad-cli")
    if not kicad_cli:
        raise RuntimeError("kicad-cli is required to render the PCB preview")
    subprocess.run(
        [
            kicad_cli,
            "pcb",
            "render",
            "--output",
            str(PREVIEW_PATH),
            "--width",
            "1600",
            "--height",
            "1000",
            "--side",
            "top",
            "--quality",
            "high",
            str(BOARD_PATH),
        ],
        check=True,
    )


build_board()
render_preview()
