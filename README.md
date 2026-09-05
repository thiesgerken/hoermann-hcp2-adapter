# Hörmann HCP ESP32 Adapter

Planungsprojekt für einen ESPHome-Adapter am HCP2-Bus eines Hörmann Serie-4-Torantriebs.

## Status

Ein ausführbarer Schaltplan und ein vollständig gerouteter, vorläufiger PCB-Entwurf liegen vor. Die PCB-Footprints sind Platzhalter auf Basis der Händlerangaben und ausdrücklich nicht zur Fertigung freigegeben. Mechanische Prüfungen und die Schutzbeschaltung stehen noch aus.

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
- KiCad-Projekt: [`hardware/kicad/hoermann-hcp-adapter.kicad_pro`](hardware/kicad/hoermann-hcp-adapter.kicad_pro)
- editierbares PCB: [`hardware/kicad/hoermann-hcp-adapter.kicad_pcb`](hardware/kicad/hoermann-hcp-adapter.kicad_pcb)
- gerenderte Oberseite: [`hardware/kicad/hoermann-hcp-adapter-pcb.png`](hardware/kicad/hoermann-hcp-adapter-pcb.png)

Erzeugung:

```sh
uv run python hardware/kicad/pcb.py
```

Der Entwurf verwendet eine zweilagige Platine mit 100 × 70 mm, vier M3-Bohrungen, 0,35-mm-Signalleitungen und 0,8-mm-Versorgungsleitungen. Alle neun Netze sind geroutet. Der KiCad-DRC meldet keine Fehler und keine offenen Verbindungen. Die verbleibenden neun Warnungen betreffen ausschließlich die absichtlich lokalen, noch nicht freigegebenen Footprint-Platzhalter.

Dieser Stand darf nicht gefertigt werden. Insbesondere J1 verwendet bis zur Vermessung nur eine generische 1×6-Lochreihe. Die Padabstände von PS1 und U2 sowie der Reihenabstand von U1 sind ebenfalls am gelieferten Exemplar zu bestätigen. Der Warntext `PROVISIONAL - VERIFY ALL FOOTPRINTS` steht deshalb direkt auf dem Silkscreen.

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
