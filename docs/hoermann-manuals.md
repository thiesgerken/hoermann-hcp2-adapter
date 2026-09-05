# Hörmann-Unterlagen

Die folgenden vom Projekt bereitgestellten Anleitungen liegen unverändert unter `hardware/`. Sie sind die Primärquellen für den konkreten ProMatic-4-Antrieb und sein Zubehör.

## ProMatic 4, Montage, Betrieb und Wartung

- Datei: [promatic-4-montage-betrieb-wartung-4511178-b0-18-2022.pdf](../hardware/manuals/hoermann/promatic-4-montage-betrieb-wartung-4511178-b0-18-2022.pdf)
- Dokumentnummer: `4511178 B0`
- Ausgabe: `18-2022 / RE`
- Sprache: Deutsch
- Titel: Garagentor-Antrieb, Anleitung für Montage, Betrieb und Wartung

Für dieses Projekt relevante Stellen:

- Kapitel 5.5 beschreibt DIL-Schalter C für interne Beleuchtung, BUS und Vorwarnung.
- Kapitel 5.10 beschreibt den BUS-Scan.
- Beim BUS-Scan wird angeschlossenes Zubehör gelöscht und neu erkannt.
- HOR 1-HCP und UAP 1-HCP werden als Zubehör für Serie 4 genannt.
- Elektroarbeiten und Netzspannungsbereiche sind Fachkräften vorbehalten.

## ProMatic 4, Funktionsbeschreibung und Zubehör

- Datei: [promatic-4-funktionen-zubehoer-4553098-b0-21-2022.pdf](../hardware/manuals/hoermann/promatic-4-funktionen-zubehoer-4553098-b0-21-2022.pdf)
- Dokumentnummer: `4553098 B0`
- Ausgabe: `21-2022`
- Titel: Garagentor-Antrieb, Funktionsbeschreibung und Zubehör
- Sprachen: mehrsprachig, Deutsch beginnt auf Seite 2

Für dieses Projekt relevante Stellen:

- Kapitel 3.9: Die BUS-Buchse ist für Zubehör mit Sonderfunktionen vorgesehen.
- BUS-Scan: Teilnehmer anschließen, DIL-Schalter H von OFF nach ON und wieder nach OFF schieben.
- Beim Scan wird Zubehör am BUS gelöscht und neu erkannt.
- Kapitel 4 nennt eine maximale Gesamtbelastung des Antriebs durch Zubehör von 350 mA.
- Zubehör der Serie 3 benötigt den HCP-Adapter HAP 1.
- HOR 1-HCP und UAP 1-HCP sind ausdrücklich als HCP-Zubehör aufgeführt.

Die 350 mA sind die Gesamtgrenze für Zubehör, nicht automatisch die zulässige Stromaufnahme unseres einzelnen Adapters. Der reale Startstrom von ESP32, RS485-Modul und LM2596 muss deutlich darunter liegen und während des BUS-Scans geprüft werden.

## HOR1-HCP Optionsrelais

- Datei: [hor1-hcp-tr30a117-07-2019.pdf](../hardware/manuals/hoermann/hor1-hcp-tr30a117-07-2019.pdf)
- Dokumentnummer: `TR30A117`
- Ausgabe: `07.2019`
- Produkt: `HOR1-HCP`

Für dieses Projekt relevante Stellen:

- Das Anschlussbild nennt Serie 4 und eine maximale BUS-Leitungslänge von 10 m.
- Der BUS-Teilnehmer wird über die BUS-Verbindung am Antrieb angeschlossen.
- Status-LED: Grün blinkend bedeutet nicht angemeldet, Grün dauerhaft bedeutet angemeldet, Rot dreimal blinkend bedeutet BUS-Scan.
- Das Relais ist für maximal 2,5 A bei 30 V DC beziehungsweise 500 W bei 250 V AC angegeben. Diese Relaiswerte sind für die Adapterelektronik nicht relevant.

## Zusammengeführte Entwurfsgrenzen

| Grenze | Quelle | Folgerung |
|---|---|---|
| Nur Serie 4 | ProMatic- und HOR1-HCP-Unterlagen, ESPHome | Kein Anspruch auf Kompatibilität mit Serie 3 |
| Zubehör gesamt maximal 350 mA | Funktionsbeschreibung, Kapitel 4 | Start- und Betriebsstrom des Adapters messen |
| BUS-Leitung maximal 10 m | HOR1-HCP-Anschlussbild | Kabellänge des Aufbaus dokumentieren |
| Zubehör wird beim Scan neu erkannt | beide ProMatic-Unterlagen | Adapter vor dem Scan anschließen und während des Scans bootfähig halten |
| Kein Arbeiten unter Netzspannung | Sicherheitskapitel | Vor Montage Netzstecker und gegebenenfalls Not-Akku trennen |

Die exakte HCP2-Kontaktbelegung und UART-Parameter stammen aus der ESPHome-HCP-Dokumentation. Die Hörmann-Unterlagen bestätigen BUS-Anschluss, Serie 4 und Scanablauf, enthalten in den ausgelesenen Textpassagen aber keine belastbare sechspolige Signalbelegung.
