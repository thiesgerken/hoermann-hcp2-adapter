# Bauteile

Dieses Dokument erfasst nur konkrete Kaufteile. Ein generischer Chipname ersetzt weder die genaue Modulvariante noch deren gemessenen Footprint.

## Statuswerte

- `Kandidat`: noch nicht bestellt oder nicht verbindlich ausgewählt
- `Ausgewählt`: verbindlich festgelegt, aber noch nicht geliefert oder vermessen
- `Vorhanden`: gekauft, aber noch nicht elektrisch und mechanisch geprüft
- `Vermessen`: Pinout und Maße am realen Teil bestätigt
- `Freigegeben`: für Schaltplan und PCB festgelegt

## Bauteilliste

| Ref. | Funktion | Konkretes Teil | Status | Unterlagen | Offene Prüfung |
|---|---|---|---|---|---|
| J1 | HCP2-Buchse | 95001-artige Modularbuchse, Händleroption `6P6C` ohne Abschirmung, AliExpress 1005003078110991 | Ausgewählt | [Buchsendokumentation](connector-rj12.md), [Händlerarchiv](../hardware/reference/aliexpress-1005003078110991/) | Maße, Lochbild, Kontaktfolge und mechanische Passung am Muster bestätigen |
| W1 | HCP2-Kabel | 6P6C-Stecker auf 6P6C-Stecker, AliExpress 1005005913976427 | Vorhanden | [Modulnotiz](purchased-modules.md#6p6c-kabel), [Händlerarchiv](../hardware/reference/aliexpress-1005005913976427/) | Länge dokumentieren, sechs Kontakte und 1:1-Durchgang messen |
| U1 | Controller | TENSTAR ROBOT ESP32-C3 Super Mini, AliExpress 1005005967641936 | Vorhanden | [Modulnotiz](purchased-modules.md#esp32-c3-super-mini), [offizielles Datenblatt](../hardware/datasheets/esp32-c3-espressif-v2.4.pdf), [Bauformreferenz](../hardware/datasheets/esp32-c3-supermini-community.pdf) | Bauform, Pinout, UART, Stromaufnahme, USB-VBUS und WLAN am Exemplar prüfen |
| PS1 | 25 V auf 5 V | LM2596 DC-DC HW-411, einstellbar, AliExpress 1005006362601789 | Vorhanden | [Modulnotiz](purchased-modules.md#lm2596-abwärtswandlermodul), [TI-Datenblatt](../hardware/datasheets/lm2596-ti-snvs124g.pdf) | auf 5,0 V einstellen, Abmessungen, Lastverhalten, Anlaufzeit und Überschwingen messen |
| U2 | RS485 | isoliertes 3,3-V/5-V-TTL-zu-RS485-Modul mit automatischer Richtung, AliExpress 1005010178764203 | Vorhanden | [Modulnotiz](purchased-modules.md#isoliertes-ttl-zu-rs485-modul), [Händlerarchiv](../hardware/reference/aliexpress-1005010178764203/) | Pinout, 3,3-V-Betrieb, Isolation, A/B-Bezeichnung und integrierten Abschluss messen |

## Offene Prüfungen

Stehen in [TODO.md](../TODO.md).
