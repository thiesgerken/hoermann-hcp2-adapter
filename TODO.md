# TODO

Offene Punkte. Erledigtes wird gelöscht, die Historie steht in Git.

## Inbetriebnahme

- [ ] ESPHome-Konfiguration: `hcp`-Komponente, UART auf GPIO21/GPIO20, 57600 8E1, Logger auf `hardware_uart: USB_SERIAL_JTAG`, sonst geht der Boot-Log über UART0 auf den RS485-Bus.

## Gehäuse

Entwurf in [`hardware/enclosure/`](hardware/enclosure/README.md). Modulhöhen sind Händlerangaben, im Code mit `UNGEPRÜFT` markiert.

- [ ] Modulhöhen am Teil messen und in `modules` eintragen: LM2596 mit Elkos auf seinen Stiften, gesockelter ESP32 mit USB-C, Buchse J1. Größter Wert gegen `parts_height` (16 mm) halten.
- [ ] Buchsenhöhe am Muster prüfen (11,65 laut Zeichnung, `jack_height` in `case.py`).
- [ ] Probedruck der Wanne, 6P6C-Stecker durch die Öffnung stecken: Rasthebel von unten erreichbar? Die Buchse ist 18 mm tief, der Stecker steht kaum aus der Wand. Sonst `jack_hole_below` vergrößern oder `spacing_top` verkleinern.
- [ ] Wandbefestigung der Box (Laschen oder Bodenlöcher) festlegen, aktuell keine.
