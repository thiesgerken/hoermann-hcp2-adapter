"""Ausgabe-Helfer für case.py, übernommen aus dem cad-Repo (cad_models).

Ein Modell-Skript baut seine Teile und übergibt sie an `write_outputs()`; alles
weitere (STL, Vorschau, Viewer) ist für alle Modelle gleich.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

from build123d import Color, Compound, ExportSVG, Mesher, export_stl

__all__ = ["preview", "write_outputs"]

PART_COLORS = ["#3f7fbf", "#bf7f3f", "#5f9f5f", "#9f5f9f"]
MOCKUP_COLORS = ["#2f7f6f", "#7f6f2f", "#6f2f7f"]


def preview(shape, path, eye=None):
    """Isometrische Strichzeichnung als PNG, damit man das Teil ohne 3D-Viewer sieht."""
    if eye is None:
        # Abstand an die Teilegröße koppeln, sonst verzerrt die Perspektive
        # kleine Modelle bis zur Unkenntlichkeit
        d = 3 * max(shape.bounding_box().size)
        eye = (0.6 * d, -0.8 * d, 0.7 * d)

    visible, _hidden = shape.project_to_viewport(eye, viewport_up=(0, 0, 1), look_at=(0, 0, 0))
    svg = ExportSVG(scale=2, margin=5)
    svg.add_layer("visible", line_weight=0.5)
    svg.add_shape(visible, layer="visible")
    svg.write(f"{path}.svg")
    # rsvg-convert statt einer Python-Abhängigkeit; ohne es bleibt das SVG liegen
    if shutil.which("rsvg-convert"):
        subprocess.run(["rsvg-convert", "-w", "1000", "-b", "white", f"{path}.svg", "-o", path], check=True)
        os.remove(f"{path}.svg")


def _rgba(hex_color, alpha):
    return Color(*(int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)), alpha)


def write_preview(path, opaque, translucent):
    """Zusammenbau als eine Datei: `preview.stl` mit allem Undurchsichtigen, `preview.3mf`
    zusätzlich mit den durchsichtigen Teilen. STL kennt keine Farben, 3MF trägt RGBA pro
    Objekt; ob ein Viewer das Alpha auch anzeigt, ist seine Sache."""
    export_stl(Compound(children=[shape for shape, _ in opaque.values()]), f"{path}.stl")
    mesher = Mesher()
    for name, (shape, color) in {**opaque, **translucent}.items():
        shape.color = color
        mesher.add_shape(shape, part_number=name)
    mesher.write(f"{path}.3mf")


def write_outputs(parts, directory, argv=None, assembly=None, mockups=None, translucent=()):
    """STLs neben das Skript schreiben; --png rendert Vorschauen, --show öffnet den Viewer.

    `parts` bildet den Dateinamen (ohne Endung) auf das Teil ab.

    `assembly` bildet Teilenamen auf eine `Location` ab, die nur für die Anzeige
    angewendet wird. Ohne das lägen im Viewer alle Teile ineinander, denn STL und
    Vorschau brauchen sie einzeln und druckfertig in der Ausgangslage.

    `mockups` sind Grobmodelle der verbauten Hardware, schon an ihrem Platz. Sie
    gehen in den Viewer und in `preview.stl`/`preview.3mf`, nie in die Teile-STLs:
    nichts davon wird gedruckt.

    `translucent` nennt Teile, die im Viewer und im 3MF halbdurchsichtig sind und in
    `preview.stl` fehlen, typisch der Deckel: undurchsichtig verdeckte er alles.
    """
    argv = sys.argv if argv is None else argv
    directory = Path(directory)

    for name, shape in parts.items():
        bb = shape.bounding_box()
        print(f"{name}.stl  bbox {tuple(round(v, 2) for v in bb.min)} .. {tuple(round(v, 2) for v in bb.max)}"
              f"  volume {shape.volume:.0f}")
        export_stl(shape, str(directory / f"{name}.stl"))
        if "--png" in argv:
            preview(shape, str(directory / f"preview-{name}.png"))

    assembly = assembly or {}
    mockups = mockups or {}
    placed = {name: assembly[name] * shape if name in assembly else shape for name, shape in parts.items()}
    placed.update(mockups)
    # Gedruckte Teile kräftig und deckend, Hardware blass und durchscheinend,
    # damit man durch sie hindurch auf die Wanne sieht
    colors = [PART_COLORS[i % len(PART_COLORS)] for i in range(len(parts))]
    colors += [MOCKUP_COLORS[i % len(MOCKUP_COLORS)] for i in range(len(mockups))]
    alphas = [0.35 if name in translucent else 1.0 for name in parts] + [0.55] * len(mockups)

    if mockups:
        colored = {name: (shape, _rgba(c, a)) for (name, shape), c, a in zip(placed.items(), colors, alphas)}
        write_preview(
            str(directory / "preview"),
            {n: v for n, v in colored.items() if n not in translucent},
            {n: v for n, v in colored.items() if n in translucent},
        )

    if "--show" in argv:
        from ocp_vscode import show

        show(*placed.values(), names=list(placed), colors=colors, alphas=alphas)
