# TODO

Offene Punkte vor der Fertigung und Inbetriebnahme. Erledigtes wird gestrichen, nicht gelöscht.

## Blocker für die Bestellung der Platine

### J1, HCP2-Buchse (heikelster Punkt)

Der Footprint `RJ12_95001_6P6C` beruht auf Händlerzeichnungen zweier Schwestermodelle, nicht auf einem Datenblatt der gekauften Buchse. Falsch wären im schlimmsten Fall Zapfenabstand, Stiftreihen und Pin-1-Lage gleichzeitig.

- [ ] Gelieferte Buchse vermessen: Gehäusebreite, Tiefe ab Frontfläche, Zapfendurchmesser und -abstand, Abstand Frontfläche zu Zapfen, Abstand Zapfen zu erster Stiftreihe, Reihenabstand, Stiftversatz, Stiftdurchmesser. Sollwerte im Footprint: 12,2 / 13,0 / Ø2,4 / 12,0 / 6,0 / 2,3 / 2,54 / 1,02 / Ø0,9 mm.
- [ ] Kontaktfolge durchmessen: 1:1-Kabel einstecken, Durchgang von Steckerkontakt 1 bis 6 auf die PCB-Stifte. Erwartet: Pin 1 in Draufsicht links in der kantennahen Reihe, Pin 2 rechts daneben in der hinteren Reihe.
- [ ] Papiertest: `hcp-pcb.pdf` im Maßstab 1:1 drucken, Buchse auf die F.Cu-Seite stecken. Dauert fünf Minuten und fängt jeden groben Fehler.
- [ ] Falls das Muster abweicht oder erst spät kommt: auf eine Buchse mit Datenblatt und KiCad-Footprint wechseln, zum Beispiel Amphenol 54601-906LF (`Connector_RJ:RJ12_Amphenol_54601-x06_Horizontal`). Dann Footprint in `HCP.pretty` austauschen und J1-Routing in `pcb.py` anpassen.

### Übrige Footprints

- [x] PS1 LM2596 HW-411: Platine 43,4 × 21,2, Eckpads 39,4 × 17,5 mm am Modul gemessen und übernommen. Löcher 30,7 × 16,8 laut Händlerzeichnung.
- [x] U2 RS485-Modul: Platinenmaß und Padbild stimmen mit dem Modul überein.
- [x] U1 ESP32-C3 Super Mini: Reihenabstand und Pinseite am Board bestätigt.

## Weitere Aufgaben

- [ ] Widerstand zwischen A und B am stromlosen U2 messen (integrierter 120-Ohm-Abschluss).
- [ ] ESPHome-Konfiguration mit `hcp` Komponente, UART auf GPIO21/GPIO20, 57600 8E1. Logger auf `hardware_uart: USB_SERIAL_JTAG` legen, sonst geht der Boot-Log über UART0 auf den RS485-Bus.

## Gehäuse

Entwurf in [`hardware/enclosure/`](hardware/enclosure/README.md). Alle Modulhöhen sind Händlerangaben, im Code mit `UNGEPRÜFT` markiert.

- [ ] Modulhöhen am Teil messen und in `modules` eintragen: LM2596 mit Elkos auf seinen Stiften, gesockelter ESP32 mit USB-C, Buchse J1. Größter Wert gegen `parts_height` (16 mm) halten.
- [ ] Buchse J1 messen (Breite, Höhe, Tiefe ab Front) und `jack_*` anpassen; die Öffnung ist auf 12,2 × 13,3 ausgelegt. Lage der Rastnase (oben oder unten) notieren.
- [ ] Nach Entscheidung zu H2/H3 (siehe oben) `standoff_refs` und `standoff_wall` in `case.py` nachziehen.
- [ ] Probedruck der Wanne, 6P6C-Stecker durch die Öffnung stecken: Rastnase erreichbar, Stecker steht rechnerisch 12 mm aus der Wand.
- [ ] Entscheiden, ob USB-C von U1 eine Öffnung in der +X-Wand bekommt. Zur Zeit nicht, Flashen nur mit abgenommenem Deckel.
- [ ] Wandbefestigung der Box (Laschen oder Bodenlöcher) festlegen, aktuell keine.
- [ ] Insert-Reserve prüfen: Sockel 7,2 mm hoch wegen der Ruthex-M3-Einsätze, Platine bräuchte nur 2 mm. Kürzerer Einsatz spart Bauhöhe.
