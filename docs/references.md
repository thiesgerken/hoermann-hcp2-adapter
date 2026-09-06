# Quellen und Referenzen

Quellen werden nach ihrer Belastbarkeit getrennt. Händlerangaben werden nicht als Herstellerdatenblatt behandelt.

## Primärquellen

| Thema | Quelle | Verwendung |
|---|---|---|
| ESPHome Hörmann HCP | <https://esphome.io/components/cover/hoermann_hcp/> | unterstützte Antriebe, HCP2-Pinout, 25-V-Versorgung, 120-Ohm-Abschluss, BUS-Scan und Betriebswarnungen |
| ESPHome UART | <https://esphome.io/components/uart/> | 57600 Baud, gerade Parität und ein Stopbit |
| ESP32-C3 | <https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf> | elektrische Grenzwerte, GPIO-Funktionen, Strapping-Pins und UART |
| LM2596 | <https://www.ti.com/lit/ds/symlink/lm2596.pdf> | IC-Grenzwerte und Referenzschaltung, sofern das gekaufte Modul tatsächlich diesen Regler verwendet |

Lokale Kopien:

- [ESP32-C3-Datenblatt von Espressif](../hardware/datasheets/esp32-c3-espressif-v2.4.pdf)
- [LM2596-Datenblatt von Texas Instruments](../hardware/datasheets/lm2596-ti-snvs124g.pdf)
- [ESPHome-HCP-Verdrahtungsbild](../hardware/reference/esphome-hoermann-hcp-wiring.svg)

## Unterlagen zum konkreten Antrieb

| Dokument | Lokale Kopie | Projektrelevanz |
|---|---|---|
| ProMatic 4, Montage, Betrieb und Wartung, 4511178 B0 / 18-2022 / RE | [PDF](../hardware/manuals/hoermann/promatic-4-montage-betrieb-wartung-4511178-b0-18-2022.pdf) | BUS-Aktivierung, BUS-Scan, Sicherheits- und Betriebsanweisungen |
| ProMatic 4, Funktionsbeschreibung und Zubehör, 4553098 B0 / 21-2022 | [PDF](../hardware/manuals/hoermann/promatic-4-funktionen-zubehoer-4553098-b0-21-2022.pdf) | BUS-Scan, Serie-4-Zubehör, Gesamtgrenze von 350 mA |
| HOR1-HCP Optionsrelais, TR30A117 / 07.2019 | [PDF](../hardware/manuals/hoermann/hor1-hcp-tr30a117-07-2019.pdf) | Serie 4, BUS-Leitung bis 10 m, Teilnehmerstatus |

Auswertung: [Hörmann-Unterlagen](hoermann-manuals.md)

## Referenzimplementierungen und Bauformquellen

| Thema | Quelle | Einschränkung |
|---|---|---|
| HCPBridge | <https://github.com/hkiam/HCPBridge> | Protokoll- und Aufbauvergleich, keine normative Hardware-Spezifikation |
| ESP32-C3 SuperMini | <https://github.com/sigmdel/supermini_esp32c3_sketches> | Community-Dokumentation für eine verbreitete Bauform, Varianten des generischen Boards sind möglich |
| SuperMini Community-Datenblatt | [lokale PDF](../hardware/datasheets/esp32-c3-supermini-community.pdf) | Pinout und Maße müssen am gelieferten Board bestätigt werden |

## Händlerquellen

Vollständiger lokaler Index: [hardware/reference/README.md](../hardware/reference/README.md)

| Teil | Quelle | Lokales Archiv |
|---|---|---|
| 6P6C-Kabel | <https://de.aliexpress.com/item/1005005913976427.html> | [Archiv](../hardware/reference/aliexpress-1005005913976427/) |
| 120-Ohm-Widerstand | <https://de.aliexpress.com/item/1005007375826162.html> | [Archiv](../hardware/reference/aliexpress-1005007375826162/) |
| isoliertes TTL-zu-RS485-Modul | <https://de.aliexpress.com/item/1005010178764203.html> | [Archiv](../hardware/reference/aliexpress-1005010178764203/) |
| LM2596-Modul | <https://de.aliexpress.com/item/1005006362601789.html> | [Archiv](../hardware/reference/aliexpress-1005006362601789/) |
| ESP32-C3 Super Mini | <https://de.aliexpress.com/item/1005005967641936.html> | [Archiv](../hardware/reference/aliexpress-1005005967641936/) |
| ausgewählte 6P6C-Buchse | <https://de.aliexpress.com/item/1005003078110991.html> | [Archiv](../hardware/reference/aliexpress-1005003078110991/) |

## Quellenregeln

- Herstellerdatenblatt schlägt Händlerzeichnung.
- Händlerzeichnung schlägt eine Annahme aus Produktfotos.
- Gemessene Abmessungen des gelieferten Teils entscheiden über den Footprint.
- Abweichungen zwischen Quelle und Messung werden dokumentiert, nicht still korrigiert.
- Für jede freigegebene Baugruppe werden Bestelllink, Aufschrift, Datenblatt, Pinout und Footprint-Nachweis abgelegt.
- KI-generierte Händlerzusammenfassungen werden archiviert, aber nicht als technische Quelle verwendet.
