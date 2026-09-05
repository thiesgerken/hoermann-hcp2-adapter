# Hörmann HCP ESP32 Adapter

Planungsprojekt für einen ESPHome-Adapter am HCP2-Bus eines Hörmann Serie-4-Torantriebs.

## Status

Ein ausführbarer Schaltplan und ein vollständig gerouteter, vorläufiger PCB-Entwurf mit echten Modul-Footprints liegen vor. Die Footprint-Geometrie stammt aus Händlerfotos und -zeichnungen und ist erst nach Vermessung der gelieferten Teile zur Fertigung freigegeben. Die Schutzbeschaltung steht noch aus.

## Ziel

Die spätere Trägerplatine soll folgende gekaufte Baugruppen verbinden:

- ESP32-C3 Super Mini mit ESPHome
- einstellbares LM2596-Abwärtswandlermodul für 25 V auf 5 V
- isoliertes TTL-zu-RS485-Modul mit automatischer Richtungsumschaltung
- ungeschirmte 6P6C-Modularbuchse für den Hörmann-HCP2-Bus

Der geplante Signalweg ist:

```text
HCP2 6P6C
  +25 V / GND -> Schutz -> LM2596 -> 5 V -> BUS_PWR -> ESP32-C3
  A+ / B-     -> RS485-Busseite | Isolation | TTL-Seite <-> ESP32-UART
```

Der LM2596 ist nicht galvanisch getrennt. Deshalb teilt der Gesamtadapter trotz isoliertem RS485-Signalpfad die Masse der HCP-Versorgung. Vollständige galvanische Trennung würde zusätzlich einen isolierten DC/DC-Wandler erfordern und ist mit den gekauften Teilen nicht gegeben.

## Dokumentation

- [Bauteile und Beschaffungsstatus](docs/components.md)
- [Gekaufte Module und Hilfsteile](docs/purchased-modules.md)
- [Ausgewählte 6P6C-Buchse](docs/connector-rj12.md)
- [Hörmann-Unterlagen](docs/hoermann-manuals.md)
- [Quellen und Referenzen](docs/references.md)
- [Entscheidungsprotokoll](docs/decisions.md)
- [Lokales Händlerarchiv](hardware/reference/README.md)

IC- und Board-Unterlagen liegen unter `hardware/datasheets/`. Hörmann-Handbücher liegen unter `hardware/manuals/hoermann/`. Archivierte Händlerseiten, Produktbeschreibungen und Bilder liegen unter `hardware/reference/`. SKiDL-Quelle und erzeugte KiCad-Dateien liegen unter `hardware/kicad/`.

## Schaltplanentwurf

- SKiDL-Quelle: [`hardware/kicad/circuit.py`](hardware/kicad/circuit.py)
- editierbarer KiCad-Schaltplan: [`hardware/kicad/hoermann-hcp-adapter.kicad_sch`](hardware/kicad/hoermann-hcp-adapter.kicad_sch)
- KiCad-Netzliste: [`hardware/kicad/hoermann-hcp-adapter.net`](hardware/kicad/hoermann-hcp-adapter.net)
- gerendertes PDF: [`hardware/kicad/hoermann-hcp-adapter.pdf`](hardware/kicad/hoermann-hcp-adapter.pdf)

Erzeugung:

```sh
uv run python hardware/kicad/circuit.py
```

Die Quelle prüft die erwartete Topologie, führt den SKiDL-ERC aus und rendert anschließend mit `kicad-cli` das PDF. Dafür muss KiCad installiert sein. Der Schaltplan enthält noch keine freigegebenen Fertigungsfootprints. Die noch offene Verpol-, Überspannungs- und ESD-Schutzbeschaltung ist nicht stillschweigend durch Annahmen ersetzt worden.

Der erzeugte Schaltplan platziert den ESP32 zentral, ordnet Versorgung und Busmodule räumlich darum an und zeichnet blaue, beschriftete Verbindungslinien. Die elektrischen Netze bleiben über kleine Labels direkt an den Pins definiert und werden zusätzlich gegen die erwartete Pin-Topologie geprüft.

## Vorläufiger PCB-Entwurf

- Generator: [`hardware/kicad/pcb.py`](hardware/kicad/pcb.py)
- gemeinsames Netzmodell: [`hardware/kicad/design.py`](hardware/kicad/design.py)
- Projekt-Footprints: [`hardware/kicad/HCP.pretty/`](hardware/kicad/HCP.pretty/)
- KiCad-Projekt: [`hardware/kicad/hoermann-hcp-adapter.kicad_pro`](hardware/kicad/hoermann-hcp-adapter.kicad_pro)
- editierbares PCB: [`hardware/kicad/hoermann-hcp-adapter.kicad_pcb`](hardware/kicad/hoermann-hcp-adapter.kicad_pcb)
- gerenderte Oberseite: [`hardware/kicad/hoermann-hcp-adapter-pcb.png`](hardware/kicad/hoermann-hcp-adapter-pcb.png)
- gerenderte Unterseite: [`hardware/kicad/hoermann-hcp-adapter-pcb-bottom.png`](hardware/kicad/hoermann-hcp-adapter-pcb-bottom.png)
- Lagen-PDF (F.Cu, B.Cu, Silkscreen, Kontur): [`hardware/kicad/hoermann-hcp-adapter-pcb.pdf`](hardware/kicad/hoermann-hcp-adapter-pcb.pdf)

Erzeugung:

```sh
uv run python hardware/kicad/pcb.py
```

Der Generator liest die Footprints aus `HCP.pretty`, platziert und routet sie mit festen Koordinaten, führt den KiCad-DRC aus und rendert beide Seiten als PNG sowie die Lagen als PDF. Der DRC meldet keine Fehler, keine Warnungen und keine offenen Verbindungen.

Platine: zweilagig, 65 × 44,5 mm, 0,5-mm-Signal- und 0,8-mm-Versorgungsleitungen, vier Vias.

| Ref. | Footprint | Lage |
|---|---|---|
| J1 | `RJ12_Amphenol_54601-x06_Horizontal` (KiCad-Bibliothek, Lochbild des 95001-Typs) | oben links, Stecköffnung an der oberen Platinenkante |
| PS1 | `LM2596_HW-411`, 43,5 × 21,5 mm, Eckpads, zwei 3,2-mm-Löcher deckungsgleich mit den Modullöchern | oben rechts, IN-Seite zu J1 |
| U2 | `RS485_Isolated_34x18`, SMD-Pads für die Halblöcher | unten links, Busseite an der linken Kante |
| U1 | `ESP32-C3_SuperMini`, 2 × 8 Pins, Reihenabstand 15,24 mm | unten rechts, USB zu U2, Antenne an der rechten Kante |
| JP1 | `PinHeader_1x02_P2.54mm_Vertical` | rechts neben PS1 |
| H1 | 3,2-mm-Loch ohne Courtyard | unter U1, zwischen den Steckerleisten |

Befestigung: die beiden PS1-Löcher und H1. Eigene Eckbohrungen entfallen, weil sie nur Fläche kosten.

Dieser Stand darf nicht gefertigt werden. Vor der Freigabe am gelieferten Teil zu prüfen:

- J1: Kontaktfolge und Pin 1. Eine gespiegelte Zählung würde +25 V und GND vertauschen. Die Silkscreen-Markierungen `1` und `6` zeigen die im Layout angenommene Zählung.
- PS1: Pad- und Lochpositionen (aus Händlerfoto gemessen, Lochabstand 30,7 × 16,8 mm laut Händlerzeichnung).
- U2: Padpositionen und Pinreihenfolge beider Seiten (aus Händlerfoto gemessen, 2,54 mm TTL, 5,08 mm Bus, jeweils zentriert).
- U1: Reihenabstand 15,24 mm laut Bauformunterlage, Pinseite laut Produktfoto. Die USB-Buchse zeigt zu U2 und ist im eingebauten Zustand nicht nutzbar.

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
