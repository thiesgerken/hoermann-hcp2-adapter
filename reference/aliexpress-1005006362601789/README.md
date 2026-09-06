# LM2596 buck converter module

Original listing: <https://www.aliexpress.com/item/1005006362601789.html>

AliExpress item `1005006362601789` describes an adjustable LM2596S buck converter in the HW-411 form factor. The vendor specifies 3.2 to 46 V input, 1.25 to 35 V output, up to 3 A, and up to 92% efficiency. These limits are not accepted as design data without verification.

## Project use

PS1 converts the approximately 25 V HCP2 supply to 5.0 V. The available module measures 43.4 × 21.2 mm, with four corner pads spaced 39.4 × 17.5 mm. Before soldering, adjust the output to 5.0 V without the ESP32 connected and test for overshoot.

## Archive contents

- `product-description.txt`: readable page text with source URL and retrieval date
- `product-page-raw.html` and `product-page-rendered.html`: raw and rendered product pages
- `gallery-01.webp` through `gallery-06.webp`: vendor images of both sides
- `rendered-image-urls.txt`: image sources from the rendered page

Archived on 2026-09-05. The TI regulator datasheet and measurements of the specific module take precedence over vendor claims.
