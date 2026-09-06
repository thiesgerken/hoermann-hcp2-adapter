# Purchased modules and supporting parts

The information below comes from vendor pages, product images, and linked datasheets. Measurements of the delivered samples take precedence before schematic and PCB approval.

## ESP32-C3 Super Mini

- AliExpress: <https://www.aliexpress.com/item/1005005967641936.html>
- Vendor description: TENSTAR ROBOT ESP32-C3 Super Mini
- Form factor: 16 pins, eight per side, 2.54 mm pitch
- Common reference dimensions: 22.52 × 18 mm
- USB-C, BOOT and RESET buttons, ceramic antenna
- ESP32-C3 with 4 MB flash according to the reference document
- The blue onboard LED is connected to GPIO8 on the common form factor

Typical pin order with USB-C at the top:

| Left side, top to bottom | Right side, top to bottom |
|---|---|
| 5V | GPIO5 |
| GND | GPIO6 |
| 3V3 | GPIO7 |
| GPIO4 | GPIO8 |
| GPIO3 | GPIO9 |
| GPIO2 | GPIO10 |
| GPIO1 | GPIO20 |
| GPIO0 | GPIO21 |

The preliminary schematic assigns GPIO21 to UART TX and GPIO20 to UART RX. Configure both explicitly in ESPHome and verify them on the physical board.

Open checks:

1. Measure outer dimensions, header spacing, and pin labels on the delivered board.
2. Test GPIO20 and GPIO21 as UART at 57600 baud, even parity, and one stop bit.
3. Measure current during boot, Wi-Fi association, and normal operation.
4. Verify the behavior of the 5V pin and USB VBUS. Community documentation warns against simultaneous external and USB power.
5. Test Wi-Fi reception in the intended enclosure and keep the antenna region clear on the carrier PCB.

Local documents:

- [Official ESP32-C3 datasheet](../datasheets/esp32-c3-espressif-v2.4.pdf)
- [Community Super Mini form-factor datasheet](../datasheets/esp32-c3-supermini-community.pdf)
- [Vendor archive](../aliexpress-1005005967641936/)

## LM2596 buck converter module

- AliExpress: <https://www.aliexpress.com/item/1005006362601789.html>
- Product marking: `LM2596 DC-DC HW-411`
- Regulator marking: `LM2596S ADJ`
- Connections: IN+, IN-, OUT+, OUT-
- Adjustable output through trimmer `103`
- Approximate vendor dimensions: 45 × 22 × 13 mm
- Visible capacitors: input 100 µF/50 V, output 220 µF/35 V

The vendor's 46 V input claim is not adopted as a design limit. The TI datasheet specifies 40 V as the recommended maximum input and 45 V as the IC absolute maximum. The HCP bus is approximately 25 V, but the low-cost module's population, layout, capacitors, and protection still require separate evaluation.

Intended setup:

1. Power the loose module from approximately 25 V without the ESP32.
2. Adjust the output to 5.0 V.
3. Measure the output under load and during power-on and power-off.
4. Connect the ESP32 only after those checks pass.

Open checks:

- Measure outer dimensions and mounting holes.
- Measure quiescent current, startup time, and temperature at the actual load.
- Exclude startup overshoot.
- Evaluate reverse-polarity, transient, and trimmer-failure behavior.
- Retain a disconnectable `BUS_PWR` link so USB and external 5 V cannot be applied simultaneously.

Local documents:

- [TI LM2596 datasheet](../datasheets/lm2596-ti-snvs124g.pdf)
- [Vendor archive](../aliexpress-1005006362601789/)

## Isolated TTL-to-RS485 module

- AliExpress: <https://www.aliexpress.com/item/1005010178764203.html>
- Vendor description: isolated 3.3 V/5 V TTL-to-RS485 module with automatic direction control
- Approximate dimensions: 34 × 18 × 9 mm
- TTL side at 2.54 mm pitch: VIN, TX, RX, GND
- Bus side at 5.08 mm pitch: A+, B- or B+ in some images, plus a third terminal
- No DE or RE line; direction changes automatically
- Vendor claims: up to 2 Mbit/s, galvanic isolation, TVS, fuse, and integrated 120 Ω termination

The product images do not identify the transceiver reliably enough to establish its permitted bus voltage. One image labels the third bus-side terminal as earth or unused, explicitly not supply ground. Leave it open until labels and continuity are checked on the delivered module.

The preliminary schematic powers the module at 3.3 V to avoid a possible 5 V level at ESP32 RX. Before hardware release, verify reliable 3.3 V operation and sufficient capacity on the Super Mini 3.3 V regulator.

Acceptance checks on the delivered module:

1. Photograph and verify the labels on both sides.
2. Measure DC resistance between A and B with power removed.
3. The module has measured 120 Ω between A and B when unpowered. Do not add another termination resistor to the carrier PCB.
4. Measure the RX output logic level at the selected supply voltage.
5. Verify transmit direction switching and reception at 57600 baud with even parity.
6. Measure galvanic isolation between TTL ground and the bus side.
7. Verify A/B labeling with a known frame or oscilloscope.

Local document: [vendor archive](../aliexpress-1005010178764203/)

## 120 Ω resistor

- AliExpress: <https://www.aliexpress.com/item/1005007375826162.html>
- Purchased variant: 120 Ω, 1 W, 1%, axial metal film
- Use: loose spare and measurement part, not fitted to the carrier PCB

The RS485 module reportedly includes 120 Ω termination. Adding a parallel resistor would produce approximately 60 Ω and load the bus unnecessarily. The PCB therefore has neither the resistor nor a footprint for it.

Local archive: [AliExpress 1005007375826162](../aliexpress-1005007375826162/)

## 6P6C cable

- AliExpress: <https://www.aliexpress.com/item/1005005913976427.html>
- Vendor description: RJ11/RJ12 6P6C plug-to-plug straight-through cable
- Listed lengths: 0.5 m, 1 m, 2 m, 3 m, and 5 m; the purchased length is not yet recorded

Product images are inconsistent and some show only four visible conductors. Verify every cable before connection:

1. Both plugs have six contacts.
2. All six conductors have continuity.
3. Contact 1 maps to contact 1 through contact 6 mapping to contact 6.
4. No adjacent contacts are shorted.

A crossed telephone cable can swap +25 V and GND and must not be used.

Local archive: [AliExpress 1005005913976427](../aliexpress-1005005913976427/)
