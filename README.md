# Hörmann HCP ESP32 Adapter

Planungsprojekt für einen ESPHome-Adapter am HCP2-Bus eines Hörmann Serie-4-Torantriebs.

## Status

Ein ausführbarer Schaltplan und ein vollständig gerouteter, vorläufiger PCB-Entwurf mit echten Modul-Footprints liegen vor. Die Footprint-Geometrie stammt aus Händlerfotos und -zeichnungen und ist erst nach Vermessung der gelieferten Teile zur Fertigung freigegeben. Auf eine eigene Schutzbeschaltung wird verzichtet (D-005, D-014).

## Ziel

Die spätere Trägerplatine soll folgende gekaufte Baugruppen verbinden:

- ESP32-C3 Super Mini mit ESPHome
- einstellbares LM2596-Abwärtswandlermodul für 25 V auf 5 V
- isoliertes TTL-zu-RS485-Modul mit automatischer Richtungsumschaltung
- ungeschirmte 6P6C-Modularbuchse für den Hörmann-HCP2-Bus

Der geplante Signalweg ist:

```text
HCP2 6P6C
  +25 V / GND -> LM2596 -> 5 V -> BUS_PWR -> ESP32-C3
  A+ / B-     -> RS485-Busseite | Isolation | TTL-Seite <-> ESP32-UART
```

Der LM2596 ist nicht galvanisch getrennt. Deshalb teilt der Gesamtadapter trotz isoliertem RS485-Signalpfad die Masse der HCP-Versorgung. Vollständige galvanische Trennung würde zusätzlich einen isolierten DC/DC-Wandler erfordern und ist mit den gekauften Teilen nicht gegeben.

## Dokumentation

- [Offene Punkte](TODO.md)
- [Gehäuse](hardware/enclosure/README.md)
- [Bauteile und Beschaffungsstatus](docs/components.md)
- [Gekaufte Module und Hilfsteile](docs/purchased-modules.md)
- [Ausgewählte 6P6C-Buchse](docs/connector-rj12.md)
- [Hörmann-Unterlagen](docs/hoermann-manuals.md)
- [Quellen und Referenzen](docs/references.md)
- [Entscheidungsprotokoll](docs/decisions.md)
- [Lokales Händlerarchiv](hardware/reference/README.md)

IC- und Board-Unterlagen liegen unter `hardware/datasheets/`. Hörmann-Handbücher liegen unter `hardware/manuals/hoermann/`. Archivierte Händlerseiten, Produktbeschreibungen und Bilder liegen unter `hardware/reference/`. Schaltplan- und PCB-Generator sowie Footprints liegen unter `hardware/pcb/`, alle daraus erzeugten KiCad-Dateien unter `hardware/pcb/generated/`. Das gedruckte Gehäuse (build123d) liegt unter `hardware/enclosure/`.

## Schaltplan

- Generator: [`hardware/pcb/schematic.py`](hardware/pcb/schematic.py)
- gemeinsames Netzmodell: [`hardware/pcb/design.py`](hardware/pcb/design.py)
- editierbarer KiCad-Schaltplan: [`hardware/pcb/generated/hcp.kicad_sch`](hardware/pcb/generated/hcp.kicad_sch)
- KiCad-Netzliste: [`hardware/pcb/generated/hcp.net`](hardware/pcb/generated/hcp.net)
- gerendertes PDF: [`hardware/pcb/generated/hcp-schematic.pdf`](hardware/pcb/generated/hcp-schematic.pdf)

Erzeugung:

```sh
uv run python hardware/pcb/schematic.py
```

Der Generator schreibt den Schaltplan mit eigenen Symbolen, Drähten und Netzlabels direkt als `.kicad_sch`, lässt `kicad-cli` den ERC laufen, exportiert die Netzliste, vergleicht sie mit `design.py` und rendert das PDF. Dafür muss KiCad installiert sein.

## Vorläufiger PCB-Entwurf

- Generator: [`hardware/pcb/pcb.py`](hardware/pcb/pcb.py)
- gemeinsames Netzmodell: [`hardware/pcb/design.py`](hardware/pcb/design.py)
- Projekt-Footprints: [`hardware/pcb/HCP.pretty/`](hardware/pcb/HCP.pretty/)
- KiCad-Projekt: [`hardware/pcb/generated/hcp.kicad_pro`](hardware/pcb/generated/hcp.kicad_pro)
- editierbares PCB: [`hardware/pcb/generated/hcp.kicad_pcb`](hardware/pcb/generated/hcp.kicad_pcb)
- gerenderte Oberseite: [`hardware/pcb/generated/hcp-pcb-top.png`](hardware/pcb/generated/hcp-pcb-top.png)
- gerenderte Unterseite: [`hardware/pcb/generated/hcp-pcb-bottom.png`](hardware/pcb/generated/hcp-pcb-bottom.png)
- Lagen-PDF (F.Cu, B.Cu, Silkscreen, Kontur): [`hardware/pcb/generated/hcp-pcb.pdf`](hardware/pcb/generated/hcp-pcb.pdf)
- Gerber und Bohrdaten: [`hardware/pcb/generated/hcp-gerbers.zip`](hardware/pcb/generated/hcp-gerbers.zip)

Erzeugung:

```sh
uv run python hardware/pcb/pcb.py
```

Der Generator schreibt KiCad-Projekt und `fp-lib-table` nach `generated/`, liest die Footprints aus `HCP.pretty`, platziert und routet sie mit festen Koordinaten, führt den KiCad-DRC aus, rendert beide Seiten als PNG und die Lagen als PDF und packt Gerber- und Excellon-Dateien in ein Zip.

Silkscreen und Schaltplan-Titelblock tragen den kurzen Git-Hash von `HEAD`. Für Fertigungsdaten deshalb zuerst die Quellen committen, dann beide Generatoren laufen lassen und die Ausgaben in einem Folgecommit ablegen. Der DRC meldet keine Fehler, keine Warnungen und keine offenen Verbindungen.

Platine: zweilagig, 65 × 44,5 mm, 0,5-mm-Signal- und 0,8-mm-Versorgungsleitungen, vier Vias.

| Ref. | Footprint | Lage |
|---|---|---|
| J1 | `RJ12_95001_6P6C`, Lochbild der 95001-Familie aus den Händlerzeichnungen (Zapfen Ø2,4 im Abstand 12 mm, Stifte 1,02 mm versetzt in Reihen 8,3 und 10,84 mm hinter der Kante; Rastnase unten, Pin 1 rechts hinten in Draufsicht, siehe Fallstrick in `docs/connector-rj12.md`) | oben links, Frontfläche bündig mit der oberen Platinenkante |
| PS1 | `LM2596_HW-411`, 43,4 × 21,2 mm, Eckpads 39,4 × 17,5 mm (am Modul gemessen), zwei 3,2-mm-Löcher deckungsgleich mit den Modullöchern | oben rechts, IN-Seite zu J1 |
| U2 | `RS485_Isolated_34x18`, SMD-Pads für die Halblöcher | unten links, Busseite an der linken Kante |
| U1 | `ESP32-C3_SuperMini`, 2 × 8 Pins, Reihenabstand 15,24 mm | unten rechts, USB-Ende bündig mit der rechten Kante, Antenne zu U2 |
| JP1 | `PinHeader_1x02_P2.54mm_Vertical` | rechts neben PS1 |
| H1 bis H4 | 3,2-mm-Löcher für M3 ohne Courtyard | (3,5 / 16,5), (62,2 / 3,5), (39,9 / 40,5), (61,0 / 34,0) mm von der linken oberen Ecke; H4 liegt unter dem gesockelten U1, der Schraubenkopf passt zwischen die Steckerleisten |

Befestigung im Gehäuse über H1 bis H4. Die beiden PS1-Löcher liegen zusätzlich deckungsgleich auf der Trägerplatine.

Dieser Stand darf nicht gefertigt werden. Die offenen Prüfungen stehen in [TODO.md](TODO.md).

## Aufbau

Vor dem Bestücken jeder Platine:

1. LM2596-Modul (PS1) lose an etwa 25 V anschließen, ohne Last.
2. Ausgang mit dem Trimmer `103` auf 5,0 V einstellen. Der Trimmer bleibt auf der Platine erreichbar, aber ein falsch eingestellter Wandler darf nie am ESP32 hängen.
3. Ausgang beim Ein- und Ausschalten messen, es darf kein Überschwingen über 5,5 V geben.
4. Erst dann PS1 einlöten. JP1 bleibt offen, bis der Rest bestückt ist.

U1 wird nicht direkt aufgelötet, sondern auf zwei 1×8-Buchsenleisten gesteckt. Das Befestigungsloch H4 liegt unter dem Modul zwischen den Leisten, der Schraubenkopf passt nur unter ein gesockeltes Modul. Reihenfolge: Buchsenleisten löten, Platine im Gehäuse verschrauben, danach den ESP32 einstecken.

## Feste HCP2-Rahmenbedingungen

Laut ESPHome gilt für unterstützte Hörmann Serie-4-Antriebe:

| Pin | Signal |
|---:|---|
| 1 | GND |
| 2 | GND |
| 3 | B- |
| 4 | A+ |
| 5 | +25 V |
| 6 | +25 V |

UART-Konfiguration: 57600 Baud, 8 Datenbits, gerade Parität und ein Stopbit. Modbus läuft auf ESPHome als Server.

## Betriebsrisiken

- Nur HCP2-Geräte der Serie 4 sind im aktuellen Umfang vorgesehen.
- HCP2-Zubehör darf nicht im laufenden Betrieb ein- oder ausgesteckt werden.
- Eine unterbrochene Kommunikation oder ein Neustart des ESPHome-Geräts kann den Antrieb vorübergehend blockieren. Der Fehler wird durch Aus- und Einschalten des Antriebs beseitigt.
- Der Bus stellt seine ungefähr 25 V erst während eines Busscans bereit. Der Adapter muss dann rechtzeitig starten und antworten.
- Die Pinreihenfolge des konkreten Steckers und die 1:1-Belegung des Kabels müssen vor dem ersten Anschluss gemessen werden.
- Das isolierte RS485-Modul macht den Aufbau wegen des nicht isolierten LM2596 nicht insgesamt galvanisch getrennt.
- Der Hörmann-Antrieb erlaubt laut Zubehöranleitung insgesamt maximal 350 mA für Zubehör. Start- und Betriebsstrom des Adapters müssen gemessen werden.
- Das RS485-Modul enthält laut Händler einen integrierten 120-Ohm-Abschluss. Die Platine erhält deshalb keinen zusätzlichen Abschlusswiderstand. Vor Inbetriebnahme wird der Widerstand zwischen A und B am stromlosen Modul geprüft.
