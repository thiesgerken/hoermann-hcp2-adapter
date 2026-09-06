# TODO

Offene Punkte. Erledigtes wird gelöscht, die Historie steht in Git.

## Platine bestellen: blockiert durch J1

Der Footprint `RJ12_95001_6P6C` beruht auf Händlerzeichnungen zweier Schwestermodelle, nicht auf einem Datenblatt der gekauften Buchse. Die Pinzählung ist geklärt (Händlerzeichnung folgt der TIA-Norm, siehe `docs/connector-rj12.md`), offen ist nur die Mechanik der 6P6C-Variante. Sobald das Muster da ist:

- [ ] Maße prüfen. Soll: Gehäuse 12,2 breit, 13,0 tief ab Front; Zapfen Ø2,4 im Abstand 12,0, 6,0 hinter der Front; erste Stiftreihe 2,3 hinter den Zapfen, Reihenabstand 2,54, Stiftversatz 1,02, Stift Ø0,9.
- [ ] Vor dem Bestücken: nur J1 einlöten, Kabel zum Antrieb stecken, +25 V zwischen den Pads 5/6 (rechts) und 1/2 (links) messen. Stimmt die Polung, stimmt auch die Zählung von A+/B-.
- [ ] Papiertest: `hardware/pcb/generated/hcp-pcb.pdf` 1:1 drucken, Buchse aufstecken.
- [ ] Bei Abweichung: Buchse mit Datenblatt nehmen, etwa Amphenol 54601-906LF (`Connector_RJ:RJ12_Amphenol_54601-x06_Horizontal`), Footprint in `HCP.pretty` tauschen, J1-Routing in `pcb.py` anpassen.

## Inbetriebnahme

- [ ] Widerstand zwischen A und B am stromlosen U2 messen (integrierter 120-Ohm-Abschluss).
- [ ] ESPHome-Konfiguration: `hcp`-Komponente, UART auf GPIO21/GPIO20, 57600 8E1, Logger auf `hardware_uart: USB_SERIAL_JTAG`, sonst geht der Boot-Log über UART0 auf den RS485-Bus.

## Gehäuse

Entwurf in [`hardware/enclosure/`](hardware/enclosure/README.md). Modulhöhen sind Händlerangaben, im Code mit `UNGEPRÜFT` markiert.

- [ ] Modulhöhen am Teil messen und in `modules` eintragen: LM2596 mit Elkos auf seinen Stiften, gesockelter ESP32 mit USB-C, Buchse J1. Größter Wert gegen `parts_height` (16 mm) halten.
- [ ] Buchse J1: Höhe und Lage der Rastnase (oben oder unten) notieren, `jack_height` anpassen. Die Öffnung ist auf 13,3 hoch ausgelegt; Breite und Tiefe kommen aus dem J1-Abschnitt oben.
- [ ] Sockel unter H2: zur Zeit ausgelassen, weil PS1-Pad OUT+ 2,85 mm neben dem Loch liegt und der kleinste Sockel mit Einsatz (Ø7,2) 3,85 bräuchte. Entweder H2 auf der Platine verschieben (etwa auf (62,5 / 8,0), dann JP1 samt Routing nach unten) und in `standoff_refs` aufnehmen, oder H2 streichen; die Ecke liegt dann wie jetzt auf der Leiste.
- [ ] H3 liegt 3,89 mm vom Lötstellenrand eines U1-Pins, der Ø7,2-Sockel braucht 3,85. Entweder H3 auf x = 38,9 schieben (U2-Courtyard endet bei 36,75, keine Leiterbahn im Weg) und `standoff_wall` zurück auf 2,0, oder die 0,3 mm bewusst akzeptieren und in der Gehäuse-README festhalten.
- [ ] Probedruck der Wanne, 6P6C-Stecker durch die Öffnung stecken: Rastnase erreichbar, Stecker steht rechnerisch 12 mm aus der Wand.
- [ ] Entscheiden, ob USB-C von U1 eine Öffnung in der +X-Wand bekommt. Zur Zeit nicht, Flashen nur mit abgenommenem Deckel.
- [ ] Wandbefestigung der Box (Laschen oder Bodenlöcher) festlegen, aktuell keine.
