# Gehäuse

Gedrucktes Gehäuse für die Trägerplatine aus [`../pcb`](../pcb).
Parametrisch in Python mit [build123d](https://build123d.readthedocs.io), nach dem
Muster der Ventilsteuerungs-Gehäuse im `cad`-Repo, deren
[best-practice.md](../../../cad/best-practice.md) hier durchgängig gilt.

Zwei Teile: `bottom.stl` (Wanne) und `top.stl` (Deckel mit Hex-Lüftungsmuster),
verschraubt mit vier M3 in Ruthex-Gewindeeinsätzen in den Ecksäulen. Nicht
wasserdicht, deshalb ohne Nut und Wulst. **89.4 × 55.9 × 36.6 mm** außen,
83 × 49.5 × 29.8 mm innen.

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
beider Teile.

**Live-Viewer:** einmal in einem eigenen Terminal starten und offen lassen:

```
uv run python -m ocp_vscode
```

Dann <http://127.0.0.1:3939/viewer> im Browser öffnen (oder die *OCP CAD Viewer*
Extension in VS Code). Jeder `--show` ersetzt das Modell an Ort und Stelle, die
Kamera bleibt stehen. Der Viewer zeigt Wanne, aufgesetzten Deckel und halbtransparente
Grobmodelle der Platine, der fünf Module und eines eingesteckten 6P6C-Steckers.

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
| Wand, Boden | 3.2 mm (8 × 0.4 Extrusionsbreite) |
| Deckel | 3.6 mm |
| Platine | 65 × 44.5 × 1.6, Löcher H1..H4 aus `pcb.py`, Ø3.2 |
| Sockel | Ø8 × 7.2 mm, Ø4.0 × 6.7 Sackloch für Ruthex M3, 1 mm Fußkehle |
| Luft um die Platine | 9 mm seitlich (±X), 2 mm zur Buchse (+Y), 3 mm (−Y) |
| Bauhöhe über Platine | 16 mm reserviert, 5 mm Luft zum Deckel |
| Steckeröffnung | 14.2 × 15 mm, r2, ab Platinenoberseite, mittig vor J1 |
| Lüftung | Sechsecke SW 4 mm, 1.6 mm Steg, 2 mm Rand zum Wandrand und zu den Senkungen |
| Deckelschrauben | 4 × M3, Ø3.4 Durchgang, Ø6 × 2 Senkung |

## Entscheidungen

**9 mm seitliche Luft** klingt viel, ist aber die Ecksäule: die Platine ist bis in
alle vier Ecken bestückt, also muss die Säule neben der Platinenkante stehen statt
über ihrer Ecke. Wer die Box schmaler will, verlegt die Deckelschrauben oder
kürzt `column_reach` über einen kleineren `corner_radius`.

**Nur eine Öffnung.** USB-C bleibt innen: zum Flashen kommt der Deckel ab, und JP1
(`BUS_PWR` trennen bevor USB dran kommt) liegt sowieso innen. Ein USB-Ausschnitt
wäre eine Zeile in `build_bottom()`, wenn er doch gebraucht wird.

**Sockel 7.2 mm hoch** wegen der Einsatzlänge, nicht wegen der Lötstellen (2 mm).
Wie bei der Ventilsteuerung: die Bohrung muss im Sockel bleiben, der Boden ist zu dünn.

**Fußkehle 1 mm statt 2**: der Sockel an H2 steht 0.5 mm über die Platinenkante und
damit 1.5 mm vor der +Y-Wand. `test_case.py` prüft, dass keine Kehle in Wand oder
Säule läuft.

**Hex-Muster nur im Deckel.** Warme Luft steigt, und die Wände bleiben steif. Das
Raster wird auf den Innenraum beschnitten, damit der Deckel auf dem Wandrand
vollflächig aufliegt und die Schraubensenkungen Fleisch behalten.

## Vor dem Druck

- Modulhöhen messen: LM2596 mit Elkos auf seinen Stiften, gesockelter ESP32 mit
  USB-C, Buchse J1. Größter Wert plus Luft gegen `parts_height` halten.
- Buchse J1 messen (Breite, Höhe, Tiefe ab Front) und `jack_*` anpassen; die
  Öffnung ist auf 12.2 × 13.3 ausgelegt.
- 6P6C-Stecker probeweise durch die Öffnung stecken: Rastnase muss erreichbar sein,
  der Stecker steht rechnerisch 13 mm aus der Wand.
- PETG oder PLA ist egal, es steht innen an der Garagenwand.

## Dateien

```
case.py        Modell; Parameterblock oben, alles Weitere abgeleitet
test_case.py   Maßketten und Einbauprobe der Grobmodelle
outputs.py     STL/PNG/Viewer, Kopie aus dem cad-Repo (cad_models)
```
