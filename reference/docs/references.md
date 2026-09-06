# Sources and references

Sources are grouped by authority. Vendor claims are not treated as manufacturer datasheets.

## Primary sources

| Topic | Source | Used for |
|---|---|---|
| ESPHome Hörmann HCP | <https://esphome.io/components/cover/hoermann_hcp/> | Supported openers, HCP2 pinout, 25 V supply, 120 Ω termination, BUS scan, and operating warnings |
| ESPHome UART | <https://esphome.io/components/uart/> | 57600 baud, even parity, and one stop bit |
| ESP32-C3 | <https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf> | Electrical limits, GPIO functions, strapping pins, and UART |
| LM2596 | <https://www.ti.com/lit/ds/symlink/lm2596.pdf> | IC limits and reference circuit, provided that the purchased module uses the claimed regulator |

Local copies:

- [Espressif ESP32-C3 datasheet](../datasheets/esp32-c3-espressif-v2.4.pdf)
- [Texas Instruments LM2596 datasheet](../datasheets/lm2596-ti-snvs124g.pdf)
- [ESPHome HCP wiring diagram](../esphome-hoermann-hcp-wiring.svg)

## Manuals for the specific opener

| Document | Local copy | Project relevance |
|---|---|---|
| ProMatic 4 installation, operation, and maintenance, 4511178 B0 / 18-2022 / RE | [PDF](../manuals/hoermann/promatic-4-montage-betrieb-wartung-4511178-b0-18-2022.pdf) | BUS activation, BUS scan, safety, and operating instructions |
| ProMatic 4 functional description and accessories, 4553098 B0 / 21-2022 | [PDF](../manuals/hoermann/promatic-4-funktionen-zubehoer-4553098-b0-21-2022.pdf) | BUS scan, Series 4 accessories, and 350 mA combined limit |
| HOR1-HCP option relay, TR30A117 / 07.2019 | [PDF](../manuals/hoermann/hor1-hcp-tr30a117-07-2019.pdf) | Series 4, 10 m BUS cable limit, and participant status |

Analysis: [Hörmann manual analysis](hoermann-manuals.md)

## Reference implementations and form-factor sources

| Topic | Source | Limitation |
|---|---|---|
| HCPBridge | <https://github.com/hkiam/HCPBridge> | Protocol and implementation comparison, not a normative hardware specification |
| ESP32-C3 Super Mini | <https://github.com/sigmdel/supermini_esp32c3_sketches> | Community documentation for a common form factor; generic board variants can differ |
| Super Mini community datasheet | [local PDF](../datasheets/esp32-c3-supermini-community.pdf) | Confirm pinout and dimensions on the delivered board |

## Vendor sources

Complete local index: [reference/README.md](../README.md)

| Part | Source | Local archive |
|---|---|---|
| 6P6C cable | <https://www.aliexpress.com/item/1005005913976427.html> | [archive](../aliexpress-1005005913976427/) |
| 120 Ω resistor | <https://www.aliexpress.com/item/1005007375826162.html> | [archive](../aliexpress-1005007375826162/) |
| Isolated TTL-to-RS485 module | <https://www.aliexpress.com/item/1005010178764203.html> | [archive](../aliexpress-1005010178764203/) |
| LM2596 module | <https://www.aliexpress.com/item/1005006362601789.html> | [archive](../aliexpress-1005006362601789/) |
| ESP32-C3 Super Mini | <https://www.aliexpress.com/item/1005005967641936.html> | [archive](../aliexpress-1005005967641936/) |
| Selected 6P6C jack | <https://www.aliexpress.com/item/1005003078110991.html> | [archive](../aliexpress-1005003078110991/) |

## Source rules

- A manufacturer datasheet outranks a vendor drawing.
- A vendor drawing outranks assumptions inferred from product photos.
- Measurements of the delivered part determine the footprint.
- Document discrepancies between sources and measurements instead of silently correcting them.
- Retain the order link, markings, datasheet, pinout, and footprint evidence for every approved module.
- Archive AI-generated vendor summaries, but do not use them as technical sources.
