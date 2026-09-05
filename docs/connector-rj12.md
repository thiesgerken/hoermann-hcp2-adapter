# Ausgewählte 6P6C-Buchse

## Festlegung

Für J1 wird AliExpress-Artikel `1005003078110991` in der Händleroption **`6P6C` ohne Abschirmung** verwendet.

Nicht bestellen:

- `4P4C`
- `6P4C`
- `6P6C mit Abschirmung`
- `8P8C`

Das zur Option `6P6C` gehörende Händlerbild zeigt sechs Kontakte und eine ungeschirmte, rechtwinklige THT-Buchse. Der Anbieter nennt keinen belastbaren Hersteller und keine eindeutige Hersteller-Teilenummer. Pin 1, Lochbild und Abmessungen müssen deshalb am gelieferten Exemplar bestimmt werden.

## Quelle

- Händler: AliExpress
- Artikelnummer: `1005003078110991`
- Produkttitel: `10PCS RJ11 Telefon Buchse Gebogene Pin 95001 4P4C 6P6C 6P4C 8P8C Weibliche Jack PCB Stecker`
- Ausgewählte Option: `6P6C`
- Kanonischer Link: <https://de.aliexpress.com/item/1005003078110991.html>
- Abgerufen: 2026-09-05

Lokale Kopien:

- [Archivierte Produktbeschreibung](../hardware/reference/aliexpress-1005003078110991/product-description.txt)
- [Gerenderte Produktseite](../hardware/reference/aliexpress-1005003078110991/product-page-rendered.html)
- [Beschriftete SKU-Liste](../hardware/reference/aliexpress-1005003078110991/sku-options.txt)
- [SKU-Bild der ausgewählten Variante](../hardware/reference/aliexpress-1005003078110991/sku-6p6c-unshielded.avif)
- [Händlerzeichnung der 8P8C-Variante](../hardware/reference/aliexpress-1005003078110991/drawing-8p8c-variant.png) mit Pinnummern und PCB-Layout

Die allgemeinen Galeriebilder zeigen verschiedene Varianten. Sie dürfen nicht als Footprint-Nachweis für die ausgewählte Option verwendet werden.

## Footprint

`HCP:RJ12_95001_6P6C` in `hardware/pcb/HCP.pretty/` folgt der 95001-Familie: Frontfläche bündig mit der Platinenkante, zwei Zapfen Ø2,4 mm im Abstand 12 mm, 6 mm hinter der Kante. Die Kontaktstifte stehen in zwei Reihen 8,3 und 10,84 mm hinter der Kante, 1,02 mm versetzt, Pin 1 in Draufsicht links. Der Zapfenabstand stammt aus der [Zeichnung der nicht gewählten 6P6C-Buchse](../hardware/reference/aliexpress-1005008379850389/mechanical-drawing.webp); die 8P8C-Zeichnung des gewählten Händlers zeigt dasselbe Muster mit 15 mm.

## Elektrische HCP2-Belegung

Die folgende Belegung stammt aus der ESPHome-HCP-Dokumentation. Sie stammt nicht vom Buchsenanbieter.

| Steckkontakt | HCP2-Signal |
|---:|---|
| 1 | GND |
| 2 | GND |
| 3 | B- |
| 4 | A+ |
| 5 | +25 V |
| 6 | +25 V |

Die PCB-Pinnummerierung wird erst nach Prüfung der Kontaktfolge festgelegt. Entscheidend ist die Ansicht auf die Stecköffnung, nicht die möglicherweise spiegelverkehrte Lötseite.

## Abnahmekriterien vor PCB-Freigabe

- Gelieferte Variante besitzt sechs bestückte Kontakte und keine Abschirmung.
- Ein 6P6C-Stecker rastet mechanisch ein.
- Breite, Tiefe, Höhe, Kontaktpositionen und Kunststoffzapfen sind vermessen.
- Die Kontaktfolge ist mit einem eingesteckten 1:1-Kabel durchgemessen.
- Pin 1 ist im KiCad-Symbol, Footprint, Schaltplan und Silkscreen aus derselben Ansicht definiert.
- Der Stecker zeigt am späteren Platinenrand in die gewünschte Richtung.
- Das verwendete Kabel ist nachweislich 1:1 verdrahtet.
