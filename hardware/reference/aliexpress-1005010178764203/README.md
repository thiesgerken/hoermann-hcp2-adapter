# Isoliertes TTL-zu-RS485-Modul

Originalangebot: <https://de.aliexpress.com/item/1005010178764203.html>

AliExpress-Artikel `1005010178764203` beschreibt ein galvanisch isoliertes TTL-zu-RS485-Modul für 3,3 V oder 5 V mit automatischer Richtungsumschaltung. Der Händler nennt bis zu 2 Mbit/s, Schutzbeschaltung und einen integrierten 120-Ohm-Abschluss. Das ungefähr 34 × 18 mm große Modul besitzt castellierte Anschlüsse ohne montierte Stecker.

## Anschlüsse und Verwendung

Die TTL-Seite ist mit VIN, TX, RX und GND beschriftet. Die Busseite führt A+, B- beziehungsweise auf einzelnen Bildern B+ sowie einen dritten Erdungs- oder unbenutzten Anschluss. Im Projekt verbindet U2 den UART des ESP32-C3 mit HCP2 A+ und B-. Der dritte Busanschluss bleibt offen. Die Versorgung mit 3,3 V ist vorläufig und muss am gelieferten Modul bestätigt werden.

## Archivinhalt

- `product-description.txt`: lesbarer Seitentext mit Originalquelle und Abrufdatum
- `product-page-raw.html` und `product-page-rendered.html`: rohe und gerenderte Produktseite
- `gallery-01.webp` bis `gallery-06.webp`: Händlerbilder von Ober- und Unterseite
- `rendered-image-urls.txt`: Bildquellen aus der gerenderten Seite

Archiviert am 2026-09-05. A/B-Bezeichnung, Logikpegel, galvanische Trennung und Abschlusswiderstand müssen am konkreten Modul gemessen werden.
