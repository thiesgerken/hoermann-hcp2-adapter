# Components

This document records specific purchased parts. A generic chip name does not replace the exact module variant or its measured footprint.

## Status values

- `Candidate`: not ordered or definitively selected
- `Selected`: definitively selected, but not delivered or measured
- `On hand`: purchased, but not electrically and mechanically verified
- `Measured`: pinout and dimensions confirmed on the physical part
- `Approved`: accepted for the schematic and PCB

## Bill of materials

| Ref. | Function | Specific part | Status | Documentation | Open verification |
|---|---|---|---|---|---|
| J1 | HCP2 jack | 95001-style modular jack, vendor option `6P6C` unshielded, AliExpress 1005003078110991 | Selected | [Jack documentation](connector-rj12.md), [vendor archive](../aliexpress-1005003078110991/) | Confirm dimensions, hole pattern, contact order, and mechanical fit on the sample |
| W1 | HCP2 cable | 6P6C plug-to-plug cable, AliExpress 1005005913976427 | On hand | [Module note](purchased-modules.md#6p6c-cable), [vendor archive](../aliexpress-1005005913976427/) | Record length, confirm six contacts, and measure straight-through continuity |
| U1 | Controller | TENSTAR ROBOT ESP32-C3 Super Mini, AliExpress 1005005967641936 | On hand | [Module note](purchased-modules.md#esp32-c3-super-mini), [official datasheet](../datasheets/esp32-c3-espressif-v2.4.pdf), [form-factor reference](../datasheets/esp32-c3-supermini-community.pdf) | Verify form factor, pinout, UART, current draw, USB VBUS, and Wi-Fi on the sample |
| PS1 | 25 V to 5 V | Adjustable LM2596 DC-DC HW-411, AliExpress 1005006362601789 | On hand | [Module note](purchased-modules.md#lm2596-buck-converter-module), [TI datasheet](../datasheets/lm2596-ti-snvs124g.pdf) | Set to 5.0 V; measure dimensions, load behavior, startup time, and overshoot |
| U2 | RS485 | Isolated 3.3 V/5 V TTL-to-RS485 module with automatic direction control, AliExpress 1005010178764203 | On hand | [Module note](purchased-modules.md#isolated-ttl-to-rs485-module), [vendor archive](../aliexpress-1005010178764203/) | Verify pinout, 3.3 V operation, isolation, A/B labeling, and integrated termination |

## Open checks

See [TODO.md](../../TODO.md).
