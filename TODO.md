# TODO

Offene Punkte. Erledigtes wird gelöscht, die Historie steht in Git.

## Platine bestellen: J1 am Muster bestätigen

Footprint `RJ12_Amphenol_54601-x06_Horizontal`, Maße aus der Händlerzeichnung der gekauften Buchse, Ausrichtung (Rastnase unten, Pin 1 rechts hinten in Draufsicht) aus Zeichnung und Foto. Fallstrick in `docs/connector-rj12.md`. Sobald das Muster da ist:

- [ ] Papiertest: `hardware/pcb/generated/hcp-pcb.pdf` 1:1 drucken, Buchse aufstecken (Zapfen Ø3,2 im Abstand 10,16, Stifte 1,27 versetzt).
- [ ] Rastnasen-Schlitz zur Platine (unten). Falls oben: Pinnummern im Footprint spiegeln.
- [ ] Stift von Kontakt 1 durchmessen: in Draufsicht rechts, hintere Reihe. Kontakt 1 ist bei Schlitz unten von vorn gesehen links.
- [ ] Vor dem Bestücken: nur J1 einlöten, Kabel zum Antrieb stecken, +25 V zwischen den Pads 5/6 (links) und 1/2 (rechts) messen.

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
