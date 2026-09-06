# Isolated TTL-to-RS485 module

Original listing: <https://www.aliexpress.com/item/1005010178764203.html>

AliExpress item `1005010178764203` describes a galvanically isolated TTL-to-RS485 module for 3.3 V or 5 V with automatic direction control. The vendor claims up to 2 Mbit/s, protection circuitry, and integrated 120 Ω termination. The approximately 34 × 18 mm module has castellated connections and no installed headers.

## Connections and project use

The TTL side is labeled VIN, TX, RX, and GND. The bus side exposes A+, B- or B+ in some images, plus a third earth or unused terminal. U2 connects the ESP32-C3 UART to HCP2 A+ and B-. Leave the third bus terminal open. The planned 3.3 V supply must be verified on the delivered module.

## Archive contents

- `product-description.txt`: readable page text with source URL and retrieval date
- `product-page-raw.html` and `product-page-rendered.html`: raw and rendered product pages
- `gallery-01.webp` through `gallery-06.webp`: vendor images of both sides
- `rendered-image-urls.txt`: image sources from the rendered page

Archived on 2026-09-05. Measure A/B labeling, logic levels, galvanic isolation, and termination resistance on the specific module.
