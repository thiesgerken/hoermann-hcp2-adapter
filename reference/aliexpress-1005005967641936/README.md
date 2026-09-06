# ESP32-C3 Super Mini

Original listing: <https://www.aliexpress.com/item/1005005967641936.html>

AliExpress item `1005005967641936` sells a TENSTAR ROBOT ESP32-C3 Super Mini development board with Wi-Fi, Bluetooth, and USB-C. The project board has 16 pins in two rows at 2.54 mm pitch. The common reference form factor measures approximately 22.52 × 18 mm.

## Project use

U1 runs ESPHome. GPIO21 is assigned to UART TX and GPIO20 to UART RX. The board receives 5 V through its pin and provisionally powers the RS485 module from 3.3 V. External 5 V and USB must not be connected simultaneously, so the PCB includes the `BUS_PWR` jumper.

## Archive contents

- `product-description.txt`: readable page text with source URL and retrieval date
- `product-page-raw.html` and `product-page-rendered.html`: raw and rendered product pages
- `gallery-01.webp` through `gallery-06.webp`: vendor images of the board
- `rendered-image-urls.txt`: image sources from the rendered page

Archived on 2026-09-05. Clearly erroneous automated vendor claims, such as a 1 V supply specification, are not accepted as technical data.
