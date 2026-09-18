# Firmware

ESPHome configuration for the adapter, built around the
[Hörmann HCP component](https://esphome.io/components/cover/hoermann_hcp/).

[`hcp.yaml`](hcp.yaml) exposes the door as a cover, the opener light, the vent and
half-open buttons, and a diagnostic sensor for the bus connection. Wi-Fi credentials,
the API key, and the OTA password live in `secrets.yaml`, which is not committed.

## Setup

```sh
cp esphome/secrets.yaml.example esphome/secrets.yaml   # then fill it in
uvx esphome run esphome/hcp.yaml
```

The first flash needs USB. Hold `BOOT`, press and release `RST`, then release `BOOT` to
enter download mode. Disconnect `JP1` while USB is plugged in, because the LM2596 and USB
would otherwise drive the 5 V rail at the same time.

## Provisioning

Credentials can be set three ways, in the order they become available:

1. `improv_serial` over USB, from the browser-based ESPHome installer or the dashboard.
2. The values in `secrets.yaml`, compiled into the firmware.
3. The `Garage Door Setup` access point plus captive portal, which appears 90 s after
   Wi-Fi fails. This is the only path that works with the enclosure closed.

Bluetooth provisioning (`esp32_improv`) is present but commented out. The BLE stack costs
RAM on the ESP32-C3, and the enclosure exposes no button for an authorizer.

## Pins and bus settings

| Setting | Value |
|---|---|
| UART TX | `GPIO20` |
| UART RX | `GPIO21` |
| Baud rate | 57600, 8 data bits, even parity, 1 stop bit |
| Modbus role | Server, address 2 |

`GPIO20` and `GPIO21` are UART0 on the ESP32-C3, so the logger is pinned to
`USB_SERIAL_JTAG`. Leaving it on UART0 would push log output onto the RS485 bus.

The pin assignment looks swapped against the carrier board's net names because U2
labels its TTL pads from its own point of view: its `TX` pad is an output that drives
the ESP32. Measured on the assembled board, `GPIO20` as TX is the combination that
makes the RS485 driver switch on.

> [!CAUTION]
> Every restart drops the Modbus link and leaves the opener unresponsive to all controls,
> including its own wall button, until the opener is power-cycled. This applies to OTA
> updates. Because of that, `reboot_timeout` is `0s` for both the API and Wi-Fi, so the
> device never reboots itself over a lost connection.
