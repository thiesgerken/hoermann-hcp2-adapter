# TODO

Offene Punkte vor der Fertigung und Inbetriebnahme. Erledigtes wird gestrichen, nicht gelöscht.

## Blocker für die Bestellung der Platine

### J1, HCP2-Buchse (heikelster Punkt)

Der Footprint `RJ12_95001_6P6C` beruht auf Händlerzeichnungen zweier Schwestermodelle, nicht auf einem Datenblatt der gekauften Buchse. Falsch wären im schlimmsten Fall Zapfenabstand, Stiftreihen und Pin-1-Lage gleichzeitig.

- [ ] Gelieferte Buchse vermessen: Gehäusebreite, Tiefe ab Frontfläche, Zapfendurchmesser und -abstand, Abstand Frontfläche zu Zapfen, Abstand Zapfen zu erster Stiftreihe, Reihenabstand, Stiftversatz, Stiftdurchmesser. Sollwerte im Footprint: 12,2 / 13,0 / Ø2,4 / 12,0 / 6,0 / 2,3 / 2,54 / 1,02 / Ø0,9 mm.
- [ ] Kontaktfolge durchmessen: 1:1-Kabel einstecken, Durchgang von Steckerkontakt 1 bis 6 auf die PCB-Stifte. Erwartet: Pin 1 in Draufsicht links in der kantennahen Reihe, Pin 2 rechts daneben in der hinteren Reihe.
- [ ] Papiertest: `hoermann-hcp-adapter-pcb.pdf` im Maßstab 1:1 drucken, Buchse auf die F.Cu-Seite stecken. Dauert fünf Minuten und fängt jeden groben Fehler.
- [ ] Falls das Muster abweicht oder erst spät kommt: auf eine Buchse mit Datenblatt und KiCad-Footprint wechseln, zum Beispiel Amphenol 54601-906LF (`Connector_RJ:RJ12_Amphenol_54601-x06_Horizontal`). Dann Footprint in `HCP.pretty` austauschen und J1-Routing in `pcb.py` anpassen.

### Übrige Footprints

- [ ] PS1 LM2596 HW-411: Eckpads (Soll ±20,45 × ±9,15 mm um die Mitte) und Löcher (Soll ±15,35 × ±8,4 mm, Ø3) am Modul nachmessen. Werte stammen aus einem Händlerfoto.
- [ ] U2 RS485-Modul: Padpositionen (TTL 2,54 mm, Bus 5,08 mm, jeweils zentriert) und Pinreihenfolge beider Seiten am Modul prüfen. Werte stammen aus einem Händlerfoto.
- [ ] U1 ESP32-C3 Super Mini: Reihenabstand 15,24 mm und Pinseite (5V/GND/3V3 rechts bei USB oben, Bauteilseite) am Board prüfen.
- [ ] Papiertest 1:1 für alle vier Module.

### Schaltung

- [ ] D-005 entscheiden: Verpol-, Überspannungs- und ESD-Schutz am HCP-Eingang. Aktuell gibt es keinen.
- [ ] Prüfen, ob U2 mit 3,3 V zuverlässig läuft und der 3V3-Regler des Super Mini die Reserve hat (D-007).
- [ ] Modultyp des RS485-Transceivers und Busspannungsfestigkeit am gelieferten U2 ablesen.

## Vor der ersten Inbetriebnahme

- [ ] PS1 ohne Last an 25 V auf 5,0 V einstellen, Einschwingen und Überschwingen beim Einschalten messen.
- [ ] Gesamtstrom beim Booten und mit WLAN messen, deutlich unter der Hörmann-Grenze von 350 mA.
- [ ] Widerstand zwischen A und B am stromlosen U2 messen (integrierter 120-Ohm-Abschluss).
- [ ] Isolation zwischen TTL-Masse und Busseite von U2 messen.
- [ ] W1 6P6C-Kabel: sechs Adern, 1:1 und ohne Kurzschluss.
- [ ] ESPHome-Konfiguration mit `hcp` Komponente, UART auf GPIO21/GPIO20, 57600 8E1.

## Später

- [ ] Gehäuse. Aussparungen für J1 an der oberen Kante und USB-C von U1 an der rechten Kante, Höhe der Elkos auf PS1 (etwa 13 mm) beachten.
- [ ] Entscheiden, ob `generated/` weiter im Repo liegt oder nur die Gerber als Release-Artefakt.
