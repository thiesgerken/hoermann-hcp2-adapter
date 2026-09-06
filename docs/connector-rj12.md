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

`HCP:RJ12_95001_6P6C` in `hardware/pcb/HCP.pretty/`: Frontfläche bündig mit der Platinenkante, zwei Zapfen Ø2,4 mm im Abstand 12 mm, 6 mm hinter der Kante, Kontaktstifte in zwei Reihen 8,3 und 10,84 mm hinter der Kante mit 1,02 mm Versatz. Zapfen und Reihenmaße stammen aus den Zeichnungen der Buchsenfamilie ([6P6C eines anderen Anbieters](../hardware/reference/aliexpress-1005008379850389/mechanical-drawing.webp), [8P8C dieses Anbieters](../hardware/reference/aliexpress-1005003078110991/drawing-8p8c-variant.png)).

Pinbelegung in Draufsicht (Kante oben): Pin 1 rechts in der hinteren Reihe, Pin 2 links daneben in der vorderen Reihe, weiter abwechselnd bis Pin 6 links vorn. Der Silkscreen markiert Pin 1.

## Fallstrick: Rastnase unten

Die Zeichnungen der Familie zeigen Buchsen mit Rastnasen-Schlitz oben und Kontaktfedern unten. Das Produktfoto der gekauften 6P6C zeigt das Gegenteil: Federn an der oberen Wand der Öffnung, Schlitz zur Platine. Die gekaufte Buchse ist also „latch down". Das spiegelt die Kontaktfolge in der Draufsicht:

- Norm (TIA/FCC): Stecker mit Rastnase unten, Kontakte oben zum Betrachter, Kabel zum Betrachter, Pin 1 links. In eine Buchse mit Schlitz unten geschaut liegt Kontakt 1 daher links.
- Wer von vorn in die Buchse schaut, hat rechts, was in der Draufsicht links liegt. Bei Schlitz unten liegt Kontakt 1 in der Draufsicht also **rechts**.
- Bei einer Buchse mit Schlitz oben (wie in den Zeichnungen) wäre es umgekehrt: Kontakt 1 in der Draufsicht links.

Die Reihenzuordnung stammt aus dem Foto: der in der Frontansicht linke Stift sitzt in der hinteren Reihe. Vorausgesetzt ist, dass jede Kontaktfeder gerade nach hinten auf ihren eigenen Stift führt (keine Kreuzung im Gehäuse), was bei dieser Bauform der Fall ist.

Vor der Bestellung am Muster bestätigen: Schlitz zur Platine, Stift von Kontakt 1 (Draufsicht rechts hinten) mit dem Multimeter zur Feder durchmessen. Bei einem Muster mit Schlitz oben in `RJ12_95001_6P6C.kicad_mod` die Pinnummern spiegeln (1↔6, 2↔5, 3↔4) und die Reihen prüfen.

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
