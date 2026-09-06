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

### Befestigungslöcher

Gefunden von `hardware/enclosure/test_case.py`, das die Sockel gegen die Lötstellen aus den Footprints rechnet.

- [ ] H2 (62,2 / 3,5) liegt 3,3 mm neben PS1-Pad 3. Kein Sockel mit Gewindeeinsatz passt dorthin (Ø7,2 wäre das Minimum). Entweder H2 auf etwa (62,5 / 8,0) und dafür JP1 samt `BUCK_5V`/`ESP_5V`-Routing und Silkscreen nach unten schieben, oder H2 streichen und die Ecke auf der Leiste im Gehäuse liegen lassen. Das Gehäuse geht bis dahin vom Streichen aus.
- [ ] H3 (39,9 / 40,5) liegt 4,7 mm neben einem U1-Stift, reicht nur für Ø7,2-Sockel. Auf x = 38,9 schieben (U2-Courtyard endet bei 36,75, keine Leiterbahn im Weg), dann kann `standoff_wall` im Gehäuse zurück auf 2,0.

## Weitere Aufgaben

- [ ] Widerstand zwischen A und B am stromlosen U2 messen (integrierter 120-Ohm-Abschluss).
- [ ] ESPHome-Konfiguration mit `hcp` Komponente, UART auf GPIO21/GPIO20, 57600 8E1.

## Gehäuse

Entwurf in [`hardware/enclosure/`](hardware/enclosure/README.md). Alle Modulhöhen sind Händlerangaben, im Code mit `UNGEPRÜFT` markiert.

- [ ] Modulhöhen am Teil messen und in `modules` eintragen: LM2596 mit Elkos auf seinen Stiften, gesockelter ESP32 mit USB-C, Buchse J1. Größter Wert gegen `parts_height` (16 mm) halten.
- [ ] Buchse J1 messen (Breite, Höhe, Tiefe ab Front) und `jack_*` anpassen; die Öffnung ist auf 12,2 × 13,3 ausgelegt. Lage der Rastnase (oben oder unten) notieren.
- [ ] Nach Entscheidung zu H2/H3 (siehe oben) `standoff_refs` und `standoff_wall` in `case.py` nachziehen.
- [ ] Probedruck der Wanne, 6P6C-Stecker durch die Öffnung stecken: Rastnase erreichbar, Stecker steht rechnerisch 13 mm aus der Wand.
- [ ] Entscheiden, ob USB-C von U1 eine Öffnung in der +X-Wand bekommt. Zur Zeit nicht, Flashen nur mit abgenommenem Deckel.
- [ ] Wandbefestigung der Box (Laschen oder Bodenlöcher) festlegen, aktuell keine.
- [ ] Insert-Reserve prüfen: Sockel 7,2 mm hoch wegen der Ruthex-M3-Einsätze, Platine bräuchte nur 2 mm. Kürzerer Einsatz spart Bauhöhe.
