# Entscheidungsprotokoll

| ID | Datum | Status | Entscheidung | Begründung oder Freigabebedingung |
|---|---|---|---|---|
| D-001 | 2026-09-05 | beschlossen | Noch kein vollständiger Schaltplan und kein PCB-Layout. Zuerst werden vorhandene Kaufteile dokumentiert und vermessen. | Modulvarianten und Footprints müssen am gelieferten Exemplar geprüft werden. |
| D-002 | 2026-09-05 | beschlossen | Die erste Platine wird eine Trägerplatine für ESP32-C3-, LM2596- und isoliertes RS485-Modul. | Alle drei Module sind bereits gekauft. Eine Integration der Einzel-ICs wäre ein anderes Design. |
| D-003 | 2026-09-05 | beschlossen | J1 ist die ungeschirmte Variante `6P6C` aus AliExpress-Artikel 1005003078110991. | Die Auswahl ist verbindlich. Lochbild und Kontaktfolge werden vor dem PCB-Layout am gelieferten Muster vermessen. |
| D-004 | 2026-09-05 | beschlossen | Die Trägerplatine erhält keinen zusätzlichen 120-Ohm-Abschlusswiderstand und keinen entsprechenden Footprint. | Das ausgewählte RS485-Modul enthält den Abschluss laut Händler bereits. Der Widerstand zwischen A und B wird am Modul trotzdem vor Inbetriebnahme geprüft. |
| D-005 | 2026-09-05 | offen | Umfang von Verpol-, Überspannungs- und ESD-Schutz. | Entscheidung nach elektrischer Prüfung der gelieferten Module und des verfügbaren Platzes. |
| D-006 | 2026-09-05 | beschlossen | Die vom LM2596 kommende 5-V-Versorgung erhält eine trennbare Verbindung `BUS_PWR`. | USB und externe Versorgung des SuperMini dürfen laut Bauformunterlage nicht gleichzeitig verbunden sein. |
| D-007 | 2026-09-05 | beschlossen | Das RS485-Modul wird aus 3,3 V des ESP32-C3 Super Mini versorgt. | Dies vermeidet ein mögliches 5-V-Signal am ESP32-RX. Händler gibt 3,3 V frei, keine gesonderte Prüfung. |
| D-008 | 2026-09-05 | festgestellt | Der erste Aufbau ist nicht vollständig galvanisch getrennt. | Der nicht isolierte LM2596 verbindet die Versorgungsmassen. Das RS485-Modul trennt nur den Signalpfad. |
| D-009 | 2026-09-05 | beschlossen | Der erste Schaltplan wird jetzt aus SKiDL erzeugt, obwohl die Footprints noch offen sind. | Die elektrische Topologie ist bekannt. Ungeprüfte Maße werden nicht benötigt, solange keine Fertigungsfootprints zugewiesen werden. |
| D-010 | 2026-09-05 | vorläufig beschlossen | Ein vollständig gerouteter PCB-Entwurf wird mit klar gekennzeichneten Platzhalter-Footprints erzeugt. | Damit können Boardgröße, Platzierung und Routing früh geprüft werden. Fertigungsfreigabe erfolgt erst nach Vermessung aller Kaufteile und Festlegung der Schutzbeschaltung. |
| D-011 | 2026-09-05 | vorläufig beschlossen | Das PCB verwendet 65 × 44,5 mm mit echten Modul-Footprints statt Platzhaltern. J1 nutzt den KiCad-Footprint des Amphenol 54601 (gleiches Lochbild wie der 95001-Typ), PS1/U2/U1 eigene Footprints aus Händlermaßen. Befestigung über die PS1-Löcher und ein Loch unter U1. | Platz nicht verschwenden, Buchse am Rand. Maße aus Händlerfotos werden vor Fertigung am gelieferten Teil bestätigt. |
| D-012 | 2026-09-05 | beschlossen | Schaltplan und PCB werden ohne SKiDL direkt als KiCad-Dateien aus `design.py` erzeugt. ERC, DRC und Netzliste laufen über `kicad-cli`. | Der SKiDL-Umweg brauchte Regex-Nachbearbeitung für ein lesbares Layout. Die direkte Erzeugung ist kürzer und ergibt einen sauberen Plan. |
| D-013 | 2026-09-05 | beschlossen | J1 bekommt einen eigenen Footprint `RJ12_95001_6P6C` nach den Händlerzeichnungen statt des Amphenol-54601-Footprints. | Die 95001-Familie hat 1,02-mm-Stiftversatz und Zapfen im Abstand der Gehäusebreite, der Amphenol-Footprint 1,27 mm und 10,16 mm. Beide sind nicht austauschbar. |

Neue Entscheidungen erhalten eine fortlaufende ID. Änderungen werden als neuer Eintrag dokumentiert, damit die ursprüngliche Begründung erhalten bleibt.
