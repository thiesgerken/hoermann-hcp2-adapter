# TODO

Offene Punkte. Erledigtes wird gelöscht, die Historie steht in Git.

## Platine bestellen: blockiert durch J1

Der Footprint `RJ12_95001_6P6C` beruht auf Händlerzeichnungen zweier Schwestermodelle, nicht auf einem Datenblatt der gekauften Buchse. Sobald das Muster da ist:

- [ ] Maße prüfen. Soll: Gehäuse 12,2 breit, 13,0 tief ab Front; Zapfen Ø2,4 im Abstand 12,0, 6,0 hinter der Front; erste Stiftreihe 2,3 hinter den Zapfen, Reihenabstand 2,54, Stiftversatz 1,02, Stift Ø0,9.
- [ ] Kontaktfolge mit 1:1-Kabel durchmessen. Soll: Pin 1 in Draufsicht links in der kantennahen Reihe, Pin 2 rechts daneben in der hinteren Reihe.
- [ ] Papiertest: `hardware/pcb/generated/hcp-pcb.pdf` 1:1 drucken, Buchse aufstecken.
- [ ] Bei Abweichung: Buchse mit Datenblatt nehmen, etwa Amphenol 54601-906LF (`Connector_RJ:RJ12_Amphenol_54601-x06_Horizontal`), Footprint in `HCP.pretty` tauschen, J1-Routing in `pcb.py` anpassen.

## Inbetriebnahme

- [ ] Widerstand zwischen A und B am stromlosen U2 messen (integrierter 120-Ohm-Abschluss).
- [ ] ESPHome-Konfiguration: `hcp`-Komponente, UART auf GPIO21/GPIO20, 57600 8E1, Logger auf `hardware_uart: USB_SERIAL_JTAG`, sonst geht der Boot-Log über UART0 auf den RS485-Bus.

## Gehäuse

Entwurf in [`hardware/enclosure/`](hardware/enclosure/README.md). Modulhöhen sind Händlerangaben, im Code mit `UNGEPRÜFT` markiert.

- [ ] Modulhöhen am Teil messen und in `modules` eintragen: LM2596 mit Elkos auf seinen Stiften, gesockelter ESP32 mit USB-C, Buchse J1. Größter Wert gegen `parts_height` (16 mm) halten.
- [ ] Buchse J1 messen (Breite, Höhe, Tiefe ab Front) und `jack_*` anpassen; die Öffnung ist auf 12,2 × 13,3 ausgelegt. Lage der Rastnase (oben oder unten) notieren.
- [ ] Sockel unter H2: zur Zeit ausgelassen, weil das PS1-Pad OUT+ zu nah liegt. Entscheiden, ob H2 auf der Platine wandert oder der Sockel dort entfällt, dann `standoff_refs` und `standoff_wall` in `case.py` nachziehen.
- [ ] Probedruck der Wanne, 6P6C-Stecker durch die Öffnung stecken: Rastnase erreichbar, Stecker steht rechnerisch 12 mm aus der Wand.
- [ ] Entscheiden, ob USB-C von U1 eine Öffnung in der +X-Wand bekommt. Zur Zeit nicht, Flashen nur mit abgenommenem Deckel.
- [ ] Wandbefestigung der Box (Laschen oder Bodenlöcher) festlegen, aktuell keine.
- [ ] Insert-Reserve prüfen: Sockel 7,2 mm hoch wegen der Ruthex-M3-Einsätze, Platine bräuchte nur 2 mm. Kürzerer Einsatz spart Bauhöhe.
