EXPECTED_CONNECTIONS = {
    "HCP_GND": {"J1.1", "J1.2", "PS1.2", "PS1.4", "U1.3", "U2.4"},
    "HCP_25V": {"J1.5", "J1.6", "PS1.1"},
    "HCP_A_PLUS": {"J1.4", "U2.5"},
    "HCP_B_MINUS": {"J1.3", "U2.6"},
    "BUCK_5V": {"PS1.3", "JP1.1"},
    "ESP_5V": {"JP1.2", "U1.1"},
    "ESP_3V3": {"U1.5", "U2.1"},
    "UART_TX_GPIO21": {"U1.16", "U2.2"},
    "UART_RX_GPIO20": {"U1.14", "U2.3"},
}


def git_version():
    """Short HEAD hash, with -dirty when tracked sources (not generated outputs) changed."""
    import subprocess
    from pathlib import Path

    root = Path(__file__).resolve().parent
    run = lambda *args: subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout
    version = run("rev-parse", "--short", "HEAD").strip()
    if run("status", "--porcelain", "--", ".", ":!hardware/pcb/generated").strip():
        version += "-dirty"
    return version
