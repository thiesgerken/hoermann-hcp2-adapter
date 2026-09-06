# Gehäuse

Gedrucktes Gehäuse für die Trägerplatine aus [`../pcb`](../pcb).
Parametrisch in Python mit [build123d](https://build123d.readthedocs.io), nach dem
Muster der Ventilsteuerungs-Gehäuse im `cad`-Repo, deren
[best-practice.md](../../../cad/best-practice.md) hier durchgängig gilt.

Zwei Teile: `bottom.stl` (Wanne) und `top.stl` (Deckel mit Hex-Lüftungsmuster),
verschraubt mit vier M3 in Ruthex-Gewindeeinsätzen in den Ecksäulen. Die Platine
sitzt auf den drei Sockeln unter H1, H3 und H4 und liegt an der Buchsenkante auf
einer Leiste. Nicht wasserdicht, deshalb ohne Nut und Wulst.
**87.8 × 54.3 × 34.0 mm** außen, 83 × 49.5 × 28.8 mm innen.

Platinenmaße, Lochbild und Modullagen liest `case.py` direkt aus
[`../pcb/pcb.py`](../pcb/pcb.py) und den Footprints in `HCP.pretty`; von Hand
gepflegt sind nur die Bauhöhen und die groben Aufbauten der Module.

> Entwurf. Die Platine ist noch nicht gefertigt, alle Modulhöhen stammen aus
> Händlerangaben (im Code mit `UNGEPRÜFT` markiert). Vor dem Druck die gelieferten
> Module messen und die Werte im Parameterblock von `case.py` nachziehen.

## Workflow

```
uv sync                                        # einmal, holt build123d und ocp-vscode
uv run python hardware/enclosure/case.py                # STLs schreiben
uv run python hardware/enclosure/case.py --show         # zusätzlich in den Live-Viewer
uv run python hardware/enclosure/case.py --png          # zusätzlich preview-*.png rendern
uv run python hardware/enclosure/test_case.py           # Maßketten prüfen
```

Ausgabe landet immer neben dem Skript. Jeder Lauf druckt Bounding-Box und Volumen
beider Teile und schreibt zusätzlich den Zusammenbau: `preview.stl` (Wanne mit
Platine, Modulen und Stecker, für jeden STL-Viewer) und `preview.3mf` (dasselbe plus
Deckel, alle Objekte benannt und gefärbt, Deckel und Hardware mit Alpha; ob ein
Viewer die Transparenz anzeigt, hängt vom Viewer ab).

**Live-Viewer:** einmal in einem eigenen Terminal starten und offen lassen:

```
uv run python -m ocp_vscode
```

Dann <http://127.0.0.1:3939/viewer> im Browser öffnen (oder die *OCP CAD Viewer*
Extension in VS Code). Jeder `--show` ersetzt das Modell an Ort und Stelle, die
Kamera bleibt stehen. Der Viewer zeigt Wanne, aufgesetzten Deckel und halbtransparente
Grobmodelle: die Platine mit allen Bohrungen und Lötstellen, die fünf Module (Umriss
aus dem Footprint, Aufbauten als Klötze und Zylinder) und einen eingesteckten
6P6C-Stecker. Deckel im Baum ausblenden, dann sieht man hinein.

`--png` rendert isometrische Strichzeichnungen ohne verdeckte Kanten, braucht
`rsvg-convert` (`brew install librsvg`). Die PNGs sind gitignored.

## Layout

Draufsicht, +Y oben. Die Platine liegt wie im KiCad-Rendering: J1 an der +Y-Wand,
USB-C von U1 zeigt nach +X (ohne Öffnung).

```
          ╡ 6P6C ╞
   ┌─────────────────────────────┐
   │ o                         o │   o = Ecksäule mit M3-Einsatz
   │   [J1] [   PS1 LM2596   ]JP1│
   │   [ U2 RS485 ] [U1 ESP32-C3]│
   │ o                         o │
   └─────────────────────────────┘
```

## Maße

| | |
|---|---|
| Wand, Boden | 2.4 mm (6 × 0.4 Extrusionsbreite) |
| Deckel | 2.8 mm |
| Platine | 65 × 44.5 × 1.6, Lochbild aus `pcb.py`, Ø3.2 |
| Sockel | 3 × Ø8 × 7.2 mm unter H1, H3, H4; Ø4.0 × 6.7 Sackloch für Ruthex M3, 1 mm Fußkehle |
| Leiste | an der +Y-Wand von Säule zu Säule, unterbrochen vor der Buchse; 3.5 mm tief (1.5 mm unter der Platinenkante), bis Platinenunterkante |
| Luft um die Platine | 9 mm seitlich (±X), 2 mm zur Buchse (+Y), 3 mm (−Y) |
| Bauhöhe über Platine | 16 mm reserviert, 4 mm Luft zum Deckel |
| Buchse J1 | 13.2 × 18 mm aus dem Footprint, 11.65 hoch laut Händlerzeichnung, Rastnase zur Platine |
| Steckeröffnung | 15.2 × 16.65 mm, r2, von 3 mm unter bis 2 mm über der Buchse, mittig vor J1 |
| Lüftung | Sechsecke SW 4 mm, 1.6 mm Steg, 2 mm Rand zum Wandrand und zu den Senkungen |
| Deckelschrauben | 4 × M3, Ø3.4 Durchgang, Ø6 × 2 Senkung |

## Entscheidungen

**9 mm seitliche Luft** klingt viel, ist aber die Ecksäule: die Platine ist bis in
alle vier Ecken bestückt, also muss die Säule neben der Platinenkante stehen statt
über ihrer Ecke. Wer die Box schmaler will, verlegt die Deckelschrauben oder
kürzt `column_reach` über einen kleineren `corner_radius`.

**Wände 2.4 statt 3.2.** Die Ventilsteuerung brauchte 3.2 für eine gedichtete
115 × 158-Box im Freien. Hier ist die Box klein, steht innen und nichts muss plan
bleiben; kommerzielle Kleingehäuse liegen bei 2 bis 2.5 mm. Die Ecksäulen schneiden
2 mm in die Wand, bleiben also gerade noch innerhalb der Außenkontur.

**Nur eine Öffnung.** USB-C bleibt innen: zum Flashen kommt der Deckel ab, und JP1
(`BUS_PWR` trennen bevor USB dran kommt) liegt sowieso innen. Ein USB-Ausschnitt
wäre eine Zeile in `build_bottom()`, wenn er doch gebraucht wird.

**Drei Sockel und eine Leiste.** Die Platine hat nur drei Befestigungslöcher: in der
rechten oberen Ecke war neben den PS1-Pads kein Platz für einen Ø8-Sockel, die Ecke
liegt stattdessen auf der Leiste an der +Y-Wand. Ein Sockel trägt die Platine auf
seiner Stirnfläche, also darf dort keine Lötstelle liegen; `test_case.py` rechnet das
für jedes Loch aus den Pads der Footprints nach (Sockelradius plus Padradius plus
0.25 mm). Die erste Fassung der Platine hatte zwei Löcher, die das nicht erfüllten.

**Öffnung reicht unter die Platine.** Die Buchse hat die Rastnase zur Platine, der
Hebel des Steckers läuft also unter dem Steckerkörper nach außen und braucht vor der
Buchsenfront Platz nach unten. Die Leiste ist dort unterbrochen; die Platinenkante
stützt an der Stelle der Sockel H1 direkt daneben.

**Sockel 7.2 mm hoch** wegen der Einsatzlänge, nicht wegen der Lötstellen (2 mm).
Wie bei der Ventilsteuerung: die Bohrung muss im Sockel bleiben, der Boden ist zu dünn.

**Fußkehle 1 mm statt 2**: die Sockel stehen nah an Wand, Leiste und Säulen.
`test_case.py` prüft, dass keine Kehle in etwas hineinläuft.

**Hex-Muster nur im Deckel.** Warme Luft steigt, und die Wände bleiben steif. Das
Raster wird auf den Innenraum beschnitten, damit der Deckel auf dem Wandrand
vollflächig aufliegt und die Schraubensenkungen Fleisch behalten.

## Vor dem Druck

- Modulhöhen messen: LM2596 mit Elkos auf seinen Stiften, gesockelter ESP32 mit
  USB-C, Buchse J1. Größter Wert plus Luft gegen `parts_height` halten.
- Buchsenhöhe am Muster prüfen (11.65 laut Zeichnung, `jack_height`).
- 6P6C-Stecker probeweise durch die Öffnung stecken: die Buchse ist 18 mm tief, der
  Stecker steht damit kaum aus der 4.4 mm Wand plus Luft heraus. Der Rasthebel muss
  von unten erreichbar sein, dafür ist die Öffnung 3 mm unter die Buchse gezogen.
- Platinenecke rechts oben nach dem Einbau auf Spiel prüfen; sie liegt nur auf
  der Leiste.
- PETG oder PLA ist egal, es steht innen an der Garagenwand.

## Dateien

```
case.py        Modell; Parameterblock oben, alles Weitere abgeleitet
test_case.py   Maßketten und Einbauprobe der Grobmodelle
outputs.py     STL/3MF/PNG/Viewer, nach dem cad_models-Helfer aus dem cad-Repo
bottom.stl     Wanne, druckfertig
top.stl        Deckel, druckfertig (liegt auf der Außenseite)
preview.stl    Zusammenbau ohne Deckel, nur zum Anschauen
preview.3mf    Zusammenbau mit Deckel, gefärbt, nur zum Anschauen
```
