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

`HCP:RJ12_Amphenol_54601-x06_Horizontal` (Kopie aus der KiCad-Bibliothek in `hardware/pcb/HCP.pretty/`). Die [Händlerzeichnung der gekauften 6P6C („53-6p6c")](../hardware/reference/aliexpress-1005003078110991/drawing-6p6c.webp) hat exakt die Geometrie des Amphenol 54601: Gehäuse 13,2 × 18 mm, Zapfen Ø3,2 im Abstand 10,16 mm und 8,89 mm hinter den Stiftreihen, Stifte 1,27 mm versetzt in zwei Reihen mit 2,54 mm Abstand, Ø0,9. Die Frontfläche liegt bündig mit der Platinenkante, die Stiftreihen 14,23 und 16,77 mm dahinter.

Pinbelegung in Draufsicht (Kante oben): Pin 1 rechts in der hinteren Reihe, Pin 2 links daneben in der vorderen Reihe, weiter abwechselnd bis Pin 6 links vorn. Der Silkscreen markiert Pin 1.

## Fallstrick: Rastnase unten

Die Zeichnungen der 95001-Familie ([6P6C eines anderen Anbieters](../hardware/reference/aliexpress-1005008379850389/mechanical-drawing.webp), [8P8C dieses Anbieters](../hardware/reference/aliexpress-1005003078110991/drawing-8p8c-variant.png)) zeigen Buchsen mit Rastnasen-Schlitz oben, Kontaktfedern unten und 1,02-mm-Stiftraster. Die gekaufte 6P6C ist eine andere Bauform: Schlitz zur Platine, Federn an der oberen Wand (Zeichnung „53-6p6c" und Produktfoto), 1,27-mm-Raster. Der Schlitz unten spiegelt die Kontaktfolge in der Draufsicht:

- Norm (TIA/FCC): Stecker mit Rastnase unten, Kontakte oben zum Betrachter, Kabel zum Betrachter, Pin 1 links. In eine Buchse mit Schlitz unten geschaut liegt Kontakt 1 daher links.
- Wer von vorn in die Buchse schaut, hat rechts, was in der Draufsicht links liegt. Bei Schlitz unten liegt Kontakt 1 in der Draufsicht also **rechts**.
- Bei einer Buchse mit Schlitz oben wäre es umgekehrt: Kontakt 1 in der Draufsicht links.

Der KiCad-Footprint des Amphenol 54601 („tab down") nummeriert genau so; um 180° gedreht liegt Pin 1 rechts hinten. Vorausgesetzt ist, dass jede Kontaktfeder gerade nach hinten auf ihren eigenen Stift führt, was bei dieser Bauform der Fall ist.

Am Muster bestätigen: Schlitz zur Platine, Stift von Kontakt 1 (Draufsicht rechts hinten) mit dem Multimeter zur Feder durchmessen.

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
