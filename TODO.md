# Open checks

Open work only. Completed items are deleted because Git retains the history.

## Commissioning

- [ ] Configure ESPHome with the `hcp` component, UART on GPIO21/GPIO20 at 57600 8E1, and the logger on `hardware_uart: USB_SERIAL_JTAG`. Otherwise, the boot log uses UART0 and reaches the RS485 bus.

## Enclosure

The design is in [`enclosure/`](enclosure/README.md). Module heights currently come from vendor data and are marked `UNVERIFIED` in the code.

- [ ] Measure the installed height of each physical module and update `modules`: LM2596 including capacitors while mounted on its pins, socketed ESP32 including USB-C, and jack J1. Compare the largest value against `parts_height` (16 mm).
- [ ] Verify the jack height on the delivered part (11.65 mm in the drawing, `jack_height` in `case.py`).
- [ ] Print a trial tray and insert a 6P6C plug through the opening. Confirm that the latch is reachable from below. The jack is 18 mm deep, so the plug barely projects beyond the wall. Increase `jack_hole_below` or reduce `spacing_top` if required.
- [ ] Choose the enclosure wall-mounting method, either external tabs or holes in the tray floor. The current design has neither.
