# Gekaufte Module und Hilfsteile

Die Angaben in diesem Dokument stammen aus Händlerseiten, Produktbildern und den verlinkten Datenblättern. Vor der Freigabe für Schaltplan und PCB gelten die Messungen am gelieferten Exemplar.

## ESP32-C3 Super Mini

- AliExpress: <https://de.aliexpress.com/item/1005005967641936.html>
- Händlerbezeichnung: TENSTAR ROBOT ESP32-C3 SuperMini
- Bauform: 16 Pins, je acht Pins pro Seite, Raster 2,54 mm
- Abmessungen der verbreiteten Referenzbauform: 22,52 × 18 mm
- USB-C, BOOT- und RESET-Taster, Keramikantenne
- ESP32-C3, 4 MB Flash laut Referenzunterlage
- Die blaue Board-LED liegt bei der verbreiteten Bauform auf GPIO8.

Übliche Pinfolge bei USB-C nach oben:

| Linke Seite, oben nach unten | Rechte Seite, oben nach unten |
|---|---|
| 5V | GPIO5 |
| GND | GPIO6 |
| 3V3 | GPIO7 |
| GPIO4 | GPIO8 |
| GPIO3 | GPIO9 |
| GPIO2 | GPIO10 |
| GPIO1 | GPIO20 |
| GPIO0 | GPIO21 |

Für den vorläufigen Schaltplan ist GPIO21 als UART-TX und GPIO20 als UART-RX festgelegt. Beide werden in ESPHome explizit konfiguriert und am Board geprüft.

Offene Prüfungen:

1. Außenmaße, Pinleistenabstand und Pinbeschriftung des gelieferten Boards messen.
2. GPIO20 und GPIO21 als UART bei 57600 Baud, gerader Parität und einem Stopbit testen.
3. Stromaufnahme beim Booten, bei WLAN-Verbindung und im Betrieb messen.
4. Verhalten von 5V-Pin und USB-VBUS prüfen. Laut Community-Unterlage dürfen externe Versorgung und USB nicht gleichzeitig angeschlossen werden.
5. WLAN-Empfang im vorgesehenen Gehäuse prüfen und den Antennenbereich auf der Trägerplatine freihalten.

Lokale Unterlagen:

- [Offizielles ESP32-C3-Datenblatt](../hardware/datasheets/esp32-c3-espressif-v2.4.pdf)
- [Community-Datenblatt für die SuperMini-Bauform](../hardware/datasheets/esp32-c3-supermini-community.pdf)
- [Archiv der Händlerseite](../hardware/reference/aliexpress-1005005967641936/)

## LM2596-Abwärtswandlermodul

- AliExpress: <https://de.aliexpress.com/item/1005006362601789.html>
- Aufdruck auf Produktbildern: `LM2596 DC-DC HW-411`
- Regleraufschrift: `LM2596S ADJ`
- Anschlüsse: IN+, IN-, OUT+, OUT-
- Einstellbarer Ausgang über Trimmer `103`
- Ungefähre Außenmaße aus Händlerbildern: 45 × 22 × 13 mm
- Sichtbare Kondensatoren: Eingang 100 µF/50 V, Ausgang 220 µF/35 V

Die Händlerangabe von 46 V Eingang wird nicht als Grenzwert übernommen. Das TI-Datenblatt nennt 40 V als empfohlene maximale Eingangsspannung und 45 V als absoluten Grenzwert des ICs. Die etwa 25 V des HCP-Busses liegen darunter. Bestückung, Layout, Kondensatoren und Schutz des Billigmoduls bleiben trotzdem separat zu bewerten.

Vorgesehener Betrieb:

1. Modul ohne ESP32 an ungefähr 25 V speisen.
2. Ausgang mit dem Trimmer auf 5,0 V einstellen.
3. Ausgang unter Last und während Ein- und Ausschalten messen.
4. Erst danach den ESP32 anschließen.

Offene Prüfungen:

- Außenmaße und mögliche Befestigungsbohrungen vermessen.
- Ruhestrom, Anlaufzeit und Temperatur bei realer Last messen.
- Ausgangsüberschwingen beim Einschalten ausschließen.
- Schutz gegen Verpolung, Transienten und Fehler des Trimmers festlegen.
- Eine trennbare Verbindung `BUS_PWR` vorsehen, damit USB und externe 5-V-Versorgung nicht gleichzeitig anliegen.

Lokale Unterlagen:

- [TI-Datenblatt des LM2596](../hardware/datasheets/lm2596-ti-snvs124g.pdf)
- [Archiv der Händlerseite](../hardware/reference/aliexpress-1005006362601789/)

## Isoliertes TTL-zu-RS485-Modul

- AliExpress: <https://de.aliexpress.com/item/1005010178764203.html>
- Händlerbezeichnung: isoliertes 3,3-V/5-V-TTL-zu-RS485-Modul mit automatischer Richtungsumschaltung
- Ungefähre Außenmaße: 34 × 18 × 9 mm
- TTL-Seite im 2,54-mm-Raster: VIN, TX, RX, GND
- Busseite im 5,08-mm-Raster: A+, B- beziehungsweise auf einzelnen Bildern B+, sowie ein dritter Anschluss
- Keine DE- oder RE-Leitung, Richtungssteuerung erfolgt automatisch
- Händlerangabe: bis 2 Mbit/s, galvanische Trennung, TVS, Sicherung und integrierter 120-Ohm-Abschluss

Die genaue Transceiver-Bestückung und ihre zulässige Busspannung sind aus den Händlerbildern nicht belastbar lesbar. Der dritte Anschluss auf der Busseite wird in einem Produktbild als Erde oder unbenutzt bezeichnet und ausdrücklich nicht als Versorgung-Minus. Er bleibt offen, bis Beschriftung und Durchgang am gelieferten Modul geprüft sind.

Im vorläufigen Schaltplan wird das Modul mit 3,3 V betrieben. Damit wird ein möglicher 5-V-Pegel am RX-Ausgang vermieden. Vor der Hardwarefreigabe wird geprüft, ob das Modul bei 3,3 V zuverlässig arbeitet und ob der 3,3-V-Regler des SuperMini genügend Reserve hat.

Abnahme am gelieferten Modul:

1. Pinbeschriftung beider Seiten fotografieren und durchmessen.
2. Gleichstromwiderstand zwischen A und B im stromlosen Zustand messen.
3. Gemessen am stromlosen Modul: 120 Ohm zwischen A und B. Die Trägerplatine ergänzt keinen weiteren Abschlusswiderstand.
4. Logikpegel am RX-Ausgang bei gewählter Versorgung messen.
5. Sendeumschaltung und Empfang bei 57600 Baud mit gerader Parität prüfen.
6. Galvanische Trennung zwischen TTL-Masse und Busseite messen.
7. A/B-Bezeichnung mit einem bekannten Telegramm oder Oszilloskop verifizieren.

Lokale Unterlagen:

- [Archiv der Händlerseite](../hardware/reference/aliexpress-1005010178764203/)

## 120-Ohm-Widerstand

- AliExpress: <https://de.aliexpress.com/item/1005007375826162.html>
- Gekaufte Variante: 120 Ohm, 1 W, 1 Prozent, Metallfilm, axial
- Verwendung: nicht für die Trägerplatine vorgesehen

Die Trägerplatine erhält keinen zusätzlichen Abschlusswiderstand und keinen dafür vorgesehenen Footprint. Das RS485-Modul enthält laut Händler bereits 120 Ohm. Ein paralleler Widerstand würde ungefähr 60 Ohm ergeben und den Bus unnötig belasten. Der gekaufte Widerstand bleibt daher ein loses Ersatz- und Messteil.

Lokales Archiv: [AliExpress 1005007375826162](../hardware/reference/aliexpress-1005007375826162/)

## 6P6C-Kabel

- AliExpress: <https://de.aliexpress.com/item/1005005913976427.html>
- Händlerbezeichnung: RJ11/RJ12 6P6C, Stecker auf Stecker, gerade Verdrahtung
- Angeboten werden 0,5 m, 1 m, 2 m, 3 m und 5 m. Die gekaufte Länge ist noch nicht dokumentiert.

Die Produktbilder sind nicht konsistent. Einige zeigen nur vier sichtbare Adern. Jedes verwendete Kabel wird deshalb vor dem Anschluss geprüft:

1. Beide Stecker besitzen sechs Kontakte.
2. Alle sechs Adern haben Durchgang.
3. Kontakt 1 führt auf Kontakt 1, entsprechend bis Kontakt 6.
4. Es gibt keine Kurzschlüsse zwischen benachbarten Kontakten.

Ein gedrehtes Telefonkabel kann +25 V und GND vertauschen und darf nicht verwendet werden.

Lokales Archiv: [AliExpress 1005005913976427](../hardware/reference/aliexpress-1005005913976427/)
