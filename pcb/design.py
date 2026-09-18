import sys

# The two board variants differ only in how J1 is wired. The net model, the placement, and
# every route away from J1 are shared.
#
# "cross" follows the jack pinout in the ESPHome documentation. The openers measured for
# this project are mirrored against it, so that board needs a reversed (rollover) cable.
# "straight" mirrors J1 instead and takes a plain 1:1 cable. Each board names the cable it
# wants on its silkscreen.
VARIANTS = ("cross", "straight")

J1_PINS = {
    "cross": {
        "HCP_GND": ("J1.1", "J1.2"),
        "HCP_25V": ("J1.5", "J1.6"),
        "HCP_A_PLUS": ("J1.4",),
        "HCP_B_MINUS": ("J1.3",),
    },
    "straight": {
        "HCP_GND": ("J1.5", "J1.6"),
        "HCP_25V": ("J1.1", "J1.2"),
        "HCP_A_PLUS": ("J1.3",),
        "HCP_B_MINUS": ("J1.4",),
    },
}

SHARED_CONNECTIONS = {
    "HCP_GND": {"PS1.2", "PS1.4", "U1.3", "U2.4"},
    "HCP_25V": {"PS1.1"},
    "HCP_A_PLUS": {"U2.5"},
    "HCP_B_MINUS": {"U2.6"},
    "BUCK_5V": {"PS1.3", "JP1.1"},
    "ESP_5V": {"JP1.2", "U1.1"},
    "ESP_3V3": {"U1.5", "U2.1"},
    "UART_RX_GPIO21": {"U1.16", "U2.2"},
    "UART_TX_GPIO20": {"U1.14", "U2.3"},
}


def connections(variant):
    result = {name: set(pins) for name, pins in SHARED_CONNECTIONS.items()}
    for net_name, pin_ids in J1_PINS[variant].items():
        result[net_name].update(pin_ids)
    return result


def selected_variant():
    """The variant named on the command line, defaulting to the manufactured one."""
    name = sys.argv[1] if len(sys.argv) > 1 else "cross"
    if name not in VARIANTS:
        raise SystemExit(f"unknown variant {name!r}, expected one of {', '.join(VARIANTS)}")
    return name


def git_version():
    """Short hash of HEAD, the commit the generated outputs are based on."""
    import subprocess
    from pathlib import Path

    return subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=Path(__file__).resolve().parent, capture_output=True, text=True, check=True,
    ).stdout.strip()
