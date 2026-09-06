# Selected 6P6C jack

## Selection

J1 uses the **unshielded `6P6C`** option from AliExpress item `1005003078110991`.

Do not order the `4P4C`, `6P4C`, shielded `6P6C`, or `8P8C` variants.

The option image shows six contacts and an unshielded right-angle through-hole jack. The vendor provides neither a reliable manufacturer nor an unambiguous manufacturer part number. Confirm pin 1, hole pattern, and all dimensions on the delivered sample.

## Source

- Vendor: AliExpress
- Item: `1005003078110991`
- Listing title: `10PCS RJ11 Telephone Socket Bent Pin 95001 4P4C 6P6C 6P4C 8P8C Female Jack PCB Connector`
- Selected option: `6P6C`
- Canonical URL: <https://www.aliexpress.com/item/1005003078110991.html>
- Retrieved: 2026-09-05

Local copies:

- [archived product description](../aliexpress-1005003078110991/product-description.txt)
- [rendered product page](../aliexpress-1005003078110991/product-page-rendered.html)
- [labeled SKU list](../aliexpress-1005003078110991/sku-options.txt)
- [selected variant image](../aliexpress-1005003078110991/sku-6p6c-unshielded.avif)
- [8P8C variant drawing](../aliexpress-1005003078110991/drawing-8p8c-variant.png), including pin numbers and PCB layout

The generic gallery mixes multiple variants and is not valid footprint evidence for the selected option.

## Footprint

The board uses `HCP:RJ12_Amphenol_54601-x06_Horizontal`, copied from the KiCad library into [`pcb/HCP.pretty/`](../../pcb/HCP.pretty/). The vendor drawing for the purchased 6P6C jack, labeled `53-6p6c`, matches the Amphenol 54601 geometry:

- 13.2 × 18 mm body
- Ø3.2 mm pegs at 10.16 mm spacing
- pegs 8.89 mm behind the pin rows
- Ø0.9 mm pins staggered by 1.27 mm in rows 2.54 mm apart
- pin rows 14.23 mm and 16.77 mm behind the front face

The front face is flush with the PCB edge. In top view with the board edge at the top, pin 1 is at the right of the rear row. Pin 2 is to its left in the front row, alternating through pin 6 at the front left. The silkscreen marks pin 1.

## Latch-down orientation

Drawings for some 95001-family jacks show the latch slot above the opening, contact springs below, and 1.02 mm pin staggering. The purchased 6P6C is a different geometry: latch slot toward the PCB, springs along the upper wall, and 1.27 mm pin staggering. The latch-down orientation mirrors the top-view contact sequence.

- TIA/FCC reference view: plug latch down, contacts up and facing the viewer, cable toward the viewer, pin 1 at left.
- Looking into a latch-down jack from the front, contact 1 is at left.
- Front and top views reverse left and right. Pin 1 is therefore at the right in PCB top view.
- A latch-up jack would place pin 1 at the left in PCB top view.

The Amphenol 54601 `tab down` footprint uses this numbering. Rotating it 180 degrees places pin 1 at the rear right. This assumes each contact spring connects straight back to its corresponding pin, as shown for this geometry.

Confirm on the sample with a continuity meter: latch slot toward the PCB, contact 1 connected to the rear-right pin in PCB top view.

## HCP2 assignment

The assignment below comes from the ESPHome HCP documentation, not the jack vendor.

| Jack contact | HCP2 signal |
|---:|---|
| 1 | GND |
| 2 | GND |
| 3 | B- |
| 4 | A+ |
| 5 | +25 V |
| 6 | +25 V |

The view into the jack opening is authoritative. Do not infer the sequence from a potentially mirrored solder-side view.

## PCB release criteria

- The delivered variant has six fitted contacts and no shield.
- A 6P6C plug latches mechanically.
- Body width, depth, height, contact locations, and plastic pegs are measured.
- Contact order is measured using an inserted straight-through cable.
- Pin 1 uses the same viewing convention in the KiCad symbol, footprint, schematic, and silkscreen.
- The plug faces the intended direction at the PCB edge.
- The selected cable is verified as straight-through.
