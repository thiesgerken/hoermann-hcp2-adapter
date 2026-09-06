"""Ausgabe-Helfer für case.py, übernommen aus dem cad-Repo (cad_models).

Ein Modell-Skript baut seine Teile und übergibt sie an `write_outputs()`; alles
weitere (STL, Vorschau, Viewer) ist für alle Modelle gleich.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

from build123d import ExportSVG, export_stl

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


def write_outputs(parts, directory, argv=None, assembly=None, mockups=None):
    """STLs neben das Skript schreiben; --png rendert Vorschauen, --show öffnet den Viewer.

    `parts` bildet den Dateinamen (ohne Endung) auf das Teil ab.

    `assembly` bildet Teilenamen auf eine `Location` ab, die nur für die Anzeige
    angewendet wird. Ohne das lägen im Viewer alle Teile ineinander, denn STL und
    Vorschau brauchen sie einzeln und druckfertig in der Ausgangslage.

    `mockups` sind Grobmodelle der verbauten Hardware, schon an ihrem Platz. Sie
    gehen nur in den Viewer: nichts davon wird gedruckt, also auch nichts davon
    exportiert.
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

    if "--show" in argv:
        from ocp_vscode import show

        assembly = assembly or {}
        placed = {name: assembly[name] * shape if name in assembly else shape for name, shape in parts.items()}
        mockups = mockups or {}
        placed.update(mockups)
        # Gedruckte Teile kräftig und deckend, Hardware blass und durchscheinend,
        # damit man durch sie hindurch auf die Wanne sieht
        colors = [PART_COLORS[i % len(PART_COLORS)] for i in range(len(parts))]
        colors += [MOCKUP_COLORS[i % len(MOCKUP_COLORS)] for i in range(len(mockups))]
        show(*placed.values(), names=list(placed), colors=colors, alphas=[1.0] * len(parts) + [0.55] * len(mockups))
