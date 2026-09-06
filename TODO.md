# TODO

Offene Punkte. Erledigtes wird gelöscht, die Historie steht in Git.

## Inbetriebnahme

- [ ] ESPHome-Konfiguration: `hcp`-Komponente, UART auf GPIO21/GPIO20, 57600 8E1, Logger auf `hardware_uart: USB_SERIAL_JTAG`, sonst geht der Boot-Log über UART0 auf den RS485-Bus.

## Gehäuse

Entwurf in [`hardware/enclosure/`](hardware/enclosure/README.md). Modulhöhen sind Händlerangaben, im Code mit `UNGEPRÜFT` markiert.

- [ ] Modulhöhen am Teil messen und in `modules` eintragen: LM2596 mit Elkos auf seinen Stiften, gesockelter ESP32 mit USB-C, Buchse J1. Größter Wert gegen `parts_height` (16 mm) halten.
- [ ] Buchse J1 laut Händlerzeichnung 13,2 breit, 18 tief, 11,65 hoch, Rastnase unten (zur Platine). `jack_*` in `case.py` darauf anpassen, die Öffnung ist noch auf 13,3 hoch ausgelegt.
- [ ] H3 liegt jetzt auf x = 38,9 und H2 ist gestrichen. In `case.py` `standoff_wall` auf 2,0 zurücksetzen und den Kommentar zu H2 anpassen.
- [ ] Probedruck der Wanne, 6P6C-Stecker durch die Öffnung stecken: Rastnase erreichbar, Stecker steht rechnerisch 12 mm aus der Wand.
- [ ] Entscheiden, ob USB-C von U1 eine Öffnung in der +X-Wand bekommt. Zur Zeit nicht, Flashen nur mit abgenommenem Deckel.
- [ ] Wandbefestigung der Box (Laschen oder Bodenlöcher) festlegen, aktuell keine.
