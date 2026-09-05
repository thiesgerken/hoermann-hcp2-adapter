import os
import re
import shutil
import subprocess
import uuid
from pathlib import Path
from design import EXPECTED_CONNECTIONS

OUTPUT_DIR = Path(__file__).parent
LIBRARY_DIR = OUTPUT_DIR / "libraries"

# SKiDL imports every supported KiCad backend. Point all of them at the vendored symbols.
for version in ("", "6", "7", "8", "9", "10"):
    key = "KICAD_SYMBOL_DIR" if not version else f"KICAD{version}_SYMBOL_DIR"
    os.environ.setdefault(key, str(LIBRARY_DIR))

import skidl
from skidl import KICAD10, ERC, Net, Part, Pin, generate_netlist, generate_schematic
from skidl.logger import stop_log_file_output

skidl.lib_search_paths[KICAD10] = [str(LIBRARY_DIR)]
stop_log_file_output()

def render_pdf(schematic_path):
    kicad_cli = shutil.which("kicad-cli")
    if not kicad_cli:
        macos_cli = Path("/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli")
        if macos_cli.is_file():
            kicad_cli = str(macos_cli)
        else:
            raise RuntimeError("kicad-cli is required to render the schematic PDF")

    pdf_path = schematic_path.with_suffix(".pdf")
    subprocess.run(
        [
            kicad_cli,
            "sch",
            "export",
            "pdf",
            "--output",
            str(pdf_path),
            str(schematic_path),
        ],
        check=True,
    )
    return pdf_path

GLOBAL_LABEL_PATTERN = re.compile(
    r'  \(global_label "(?P<name>[^"]+)"\n'
    r".*?"
    r"    \(uuid [^)]+\)\)",
    re.DOTALL,
)
SYMBOL_INSTANCE_START = re.compile(r"^  \(symbol\n    \(lib_id ", re.MULTILINE)
POSITION_PATTERN = re.compile(r"\(at (-?[0-9.]+) (-?[0-9.]+)( [^)]+)\)")
MODULE_POSITIONS = {
    "J1": (75.0, 105.0),
    "PS1": (105.0, 60.0),
    "JP1": (145.0, 60.0),
    "U1": (150.0, 105.0),
    "U2": (110.0, 105.0),
}


def sexp_block(text, start):
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(text)):
        character = text[index]
        if escaped:
            escaped = False
        elif quoted and character == "\\":
            escaped = True
        elif character == '"':
            quoted = not quoted
        elif not quoted and character == "(":
            depth += 1
        elif not quoted and character == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1], index + 1
    raise RuntimeError("Unterminated S-expression in generated KiCad schematic")


def shift_positions(block, offset):
    offset_x, offset_y = offset
    return POSITION_PATTERN.sub(
        lambda match: (
            f"(at {float(match.group(1)) + offset_x:.2f} "
            f"{float(match.group(2)) + offset_y:.2f}{match.group(3)})"
        ),
        block,
    )


def layout_schematic(schematic_path, expected_connections):
    schematic = schematic_path.read_text()
    symbols = {}
    replacements = []
    for match in SYMBOL_INSTANCE_START.finditer(schematic):
        start = match.start() + 2
        block, end = sexp_block(schematic, start)
        reference = re.search(r'\(reference "([^"]+)"\)', block)
        position = re.search(r"^    \(at ([0-9.]+) ([0-9.]+) [^)]+\)", block, re.MULTILINE)
        if not reference or not position:
            raise RuntimeError("Cannot locate symbol reference or position")
        ref = reference.group(1)
        origin = (float(position.group(1)), float(position.group(2)))
        symbols[ref] = origin
        target = MODULE_POSITIONS.get(ref)
        if target:
            offset = (target[0] - origin[0], target[1] - origin[1])
            replacements.append((start, end, shift_positions(block, offset)))

    if set(symbols) != set(MODULE_POSITIONS):
        raise RuntimeError(
            f"Generated symbols differ from layout: expected {sorted(MODULE_POSITIONS)}, "
            f"got {sorted(symbols)}"
        )

    offsets = {
        ref: (target[0] - symbols[ref][0], target[1] - symbols[ref][1])
        for ref, target in MODULE_POSITIONS.items()
    }
    for start, end, replacement in reversed(replacements):
        schematic = schematic[:start] + replacement + schematic[end:]

    assignments = {}
    replacements = []
    for match in GLOBAL_LABEL_PATTERN.finditer(schematic):
        label = match.group(0)
        position = POSITION_PATTERN.search(label)
        if not position:
            raise RuntimeError(f"Cannot locate label position for {match.group('name')}")
        point = (float(position.group(1)), float(position.group(2)))
        ref = min(
            symbols,
            key=lambda candidate: (
                (point[0] - symbols[candidate][0]) ** 2
                + (point[1] - symbols[candidate][1]) ** 2
            ),
        )
        distance = (
            (point[0] - symbols[ref][0]) ** 2
            + (point[1] - symbols[ref][1]) ** 2
        ) ** 0.5
        if distance > 15:
            raise RuntimeError(f"Cannot associate {match.group('name')} label with a symbol")
        assignments.setdefault(match.group("name"), []).append(ref)
        replacements.append(
            (match.start(), match.end(), shift_positions(label, offsets[ref]))
        )

    expected_assignments = {
        net_name: sorted(pin_id.split(".", 1)[0] for pin_id in pin_ids)
        for net_name, pin_ids in expected_connections.items()
    }
    actual_assignments = {
        net_name: sorted(refs) for net_name, refs in assignments.items()
    }
    if actual_assignments != expected_assignments:
        raise RuntimeError(
            f"Generated labels differ from topology: expected {expected_assignments}, "
            f"got {actual_assignments}"
        )
    for start, end, replacement in reversed(replacements):
        schematic = schematic[:start] + replacement + schematic[end:]

    labels_by_net = {}
    for match in GLOBAL_LABEL_PATTERN.finditer(schematic):
        label = match.group(0)
        position = POSITION_PATTERN.search(label)
        labels_by_net.setdefault(match.group("name"), []).append(
            (label, float(position.group(1)), float(position.group(2)))
        )

    def graphic_connection(start, end, net_name, index):
        connection_uuid = uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"hoermann:{net_name}:{index}:{start}:{end}",
        )
        return (
            "  (polyline\n"
            "    (pts\n"
            f"      (xy {start[0]:.2f} {start[1]:.2f})\n"
            f"      (xy {end[0]:.2f} {end[1]:.2f}))\n"
            "    (stroke\n"
            "      (width 0)\n"
            "      (type default))\n"
            "    (fill\n"
            "      (type none))\n"
            f"    (uuid {connection_uuid}))\n"
        )

    moved_labels = []
    connections = []
    for net_index, (net_name, labels) in enumerate(sorted(labels_by_net.items())):
        points = [(x, y) for _, x, y in labels]
        routing_x = min(x for x, _ in points) - 12 - net_index * 4
        routing_ys = sorted({y for _, y in points})

        label = re.sub(
            r"\(at [^)]+\)",
            f"(at {routing_x:.2f} {routing_ys[0]:.2f} 180)",
            labels[0][0],
            count=1,
        )
        moved_labels.append(label.replace("(justify left)", "(justify right)") + "\n")

        segment_index = 0
        for point in points:
            connections.append(
                graphic_connection(
                    point,
                    (routing_x, point[1]),
                    net_name,
                    segment_index,
                )
            )
            segment_index += 1
        for start_y, end_y in zip(routing_ys, routing_ys[1:]):
            connections.append(
                graphic_connection(
                    (routing_x, start_y),
                    (routing_x, end_y),
                    net_name,
                    segment_index,
                )
            )
            segment_index += 1

    # Labels at each pin remain the electrical source of truth. Crossing visible
    # guides are graphics so their geometry cannot accidentally merge two nets.
    schematic = GLOBAL_LABEL_PATTERN.sub(
        lambda match: match.group(0).replace(
            "(size 1.27 1.27)",
            "(size 0.25 0.25)",
        ),
        schematic,
    ).rstrip()
    if not schematic.endswith(")"):
        raise RuntimeError("Generated KiCad schematic has an unexpected structure")
    schematic = (
        schematic[:-1]
        + "\n"
        + "".join(moved_labels)
        + "".join(connections)
        + ")\n"
    )
    schematic_path.write_text(schematic)


def connector(symbol, reference, value, tag, footprint):
    return Part(symbol, symbol, tool=KICAD10, ref=reference, value=value, tag=tag, footprint=footprint)


def configure_pin(part, number, name, function):
    pin = part[str(number)]
    pin.name = name
    pin.func = function


j1 = connector(
    "Conn_01x06",
    "J1",
    "HCP2 6P6C unshielded, AliExpress 1005003078110991",
    "hcp-connector-j1",
    "HCP:RJ12_Amphenol_54601-x06_Horizontal",
)
for number, name, function in (
    (1, "GND", Pin.funcs.PWROUT),
    (2, "GND", Pin.funcs.PASSIVE),
    (3, "B-", Pin.funcs.PASSIVE),
    (4, "A+", Pin.funcs.PASSIVE),
    (5, "+25V", Pin.funcs.PWROUT),
    (6, "+25V", Pin.funcs.PASSIVE),
):
    configure_pin(j1, number, name, function)

ps1 = connector(
    "Conn_01x04",
    "PS1",
    "LM2596 HW-411, adjust to 5.0 V",
    "buck-module-ps1",
    "HCP:LM2596_HW-411",
)
for number, name, function in (
    (1, "IN+", Pin.funcs.PWRIN),
    (2, "IN-", Pin.funcs.PASSIVE),
    (3, "OUT+", Pin.funcs.PWROUT),
    (4, "OUT-", Pin.funcs.PASSIVE),
):
    configure_pin(ps1, number, name, function)

jp1 = connector(
    "Conn_01x02", "JP1", "BUS_PWR", "bus-power-jumper-jp1", "HCP:PinHeader_1x02_P2.54mm_Vertical"
)
configure_pin(jp1, 1, "BUCK_5V", Pin.funcs.PWRIN)
configure_pin(jp1, 2, "ESP_5V", Pin.funcs.PWROUT)

u1 = connector(
    "Conn_02x08_Odd_Even",
    "U1",
    "ESP32-C3 Super Mini",
    "controller-u1",
    "HCP:ESP32-C3_SuperMini",
)
# Odd pins are the 5V/GND/3V3 header, even pins the GPIO5..GPIO21 header, both numbered from
# the USB end. Seen from the component side with USB up, the odd header is on the right.
esp32_pins = (
    (1, "5V", Pin.funcs.PWRIN),
    (3, "GND", Pin.funcs.PWRIN),
    (5, "3V3", Pin.funcs.PWROUT),
    (7, "GPIO4", Pin.funcs.NOCONNECT),
    (9, "GPIO3", Pin.funcs.NOCONNECT),
    (11, "GPIO2", Pin.funcs.NOCONNECT),
    (13, "GPIO1", Pin.funcs.NOCONNECT),
    (15, "GPIO0", Pin.funcs.NOCONNECT),
    (2, "GPIO5", Pin.funcs.NOCONNECT),
    (4, "GPIO6", Pin.funcs.NOCONNECT),
    (6, "GPIO7", Pin.funcs.NOCONNECT),
    (8, "GPIO8", Pin.funcs.NOCONNECT),
    (10, "GPIO9", Pin.funcs.NOCONNECT),
    (12, "GPIO10", Pin.funcs.NOCONNECT),
    (14, "GPIO20/U0RXD", Pin.funcs.INPUT),
    (16, "GPIO21/U0TXD", Pin.funcs.OUTPUT),
)
for pin_definition in esp32_pins:
    configure_pin(u1, *pin_definition)

u2 = connector(
    "Conn_01x07",
    "U2",
    "Isolated auto-direction RS485, onboard 120R",
    "rs485-module-u2",
    "HCP:RS485_Isolated_34x18",
)
for number, name, function in (
    (1, "VIN", Pin.funcs.PWRIN),
    (2, "TX", Pin.funcs.INPUT),
    (3, "RX", Pin.funcs.OUTPUT),
    (4, "GND", Pin.funcs.PWRIN),
    (5, "A+", Pin.funcs.BIDIR),
    (6, "B-", Pin.funcs.BIDIR),
    (7, "EARTH/NC", Pin.funcs.NOCONNECT),
):
    configure_pin(u2, number, name, function)

hcp_gnd = Net("HCP_GND")
hcp_25v = Net("HCP_25V")
hcp_a = Net("HCP_A_PLUS")
hcp_b = Net("HCP_B_MINUS")
buck_5v = Net("BUCK_5V")
esp_5v = Net("ESP_5V")
esp_3v3 = Net("ESP_3V3")
uart_tx = Net("UART_TX_GPIO21")
uart_rx = Net("UART_RX_GPIO20")
for net in (hcp_gnd, hcp_25v, hcp_a, hcp_b, buck_5v, esp_5v, esp_3v3, uart_tx, uart_rx):
    net.stub = True


hcp_gnd += j1[1, 2], ps1[2, 4], u1[3], u2[4]
hcp_25v += j1[5, 6], ps1[1]
hcp_a += j1[4], u2[5]
hcp_b += j1[3], u2[6]
buck_5v += ps1[3], jp1[1]
esp_5v += jp1[2], u1[1]
esp_3v3 += u1[5], u2[1]
uart_tx += u1[16], u2[2]
uart_rx += u2[3], u1[14]


def connected_pin_ids(net):
    return {f"{pin.part.ref}.{pin.num}" for pin in net.get_pins()}


expected_topology = {
    hcp_gnd: EXPECTED_CONNECTIONS["HCP_GND"],
    hcp_25v: EXPECTED_CONNECTIONS["HCP_25V"],
    hcp_a: EXPECTED_CONNECTIONS["HCP_A_PLUS"],
    hcp_b: EXPECTED_CONNECTIONS["HCP_B_MINUS"],
    buck_5v: EXPECTED_CONNECTIONS["BUCK_5V"],
    esp_5v: EXPECTED_CONNECTIONS["ESP_5V"],
    esp_3v3: EXPECTED_CONNECTIONS["ESP_3V3"],
    uart_tx: EXPECTED_CONNECTIONS["UART_TX_GPIO21"],
    uart_rx: EXPECTED_CONNECTIONS["UART_RX_GPIO20"],
}

for net, expected_pins in expected_topology.items():
    actual_pins = connected_pin_ids(net)
    if actual_pins != expected_pins:
        raise RuntimeError(f"{net.name}: expected {sorted(expected_pins)}, got {sorted(actual_pins)}")

ERC()
generate_netlist(
    file=str(OUTPUT_DIR / "hoermann-hcp-adapter.net"),
    tool=KICAD10,
    do_backup=False,
)
schematic_path = OUTPUT_DIR / "hoermann-hcp-adapter.kicad_sch"
generate_schematic(
    filepath=str(OUTPUT_DIR),
    top_name=schematic_path.stem,
    title="Hörmann HCP2 ESP32-C3 Adapter",
    flatness=1.0,
    auto_stub=False,
    tool=KICAD10,
)
layout_schematic(
    schematic_path,
    {net.name: expected_pins for net, expected_pins in expected_topology.items()},
)
render_pdf(schematic_path)
