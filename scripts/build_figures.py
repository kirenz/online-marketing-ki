"""Buch-Abbildungen bauen: figures-src/*.svg -> images/*.svg.

Die fertigen Dateien landen in images/ (Buch) und slides/images/ (Folien).

Die Quell-SVGs enthalten den Platzhalter /*@FONT@*/ im <style>-Block. Das
Skript ersetzt ihn durch eine @font-face-Regel mit eingebettetem Geist
(OFL-Lizenz). So rendern die Abbildungen auch als <img> in Buch, Folien
und Lernplattform in der Buchschrift, ohne externe Anfragen.

Aufruf: uv run scripts/build_figures.py
"""

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "figures-src"
OUTS = [ROOT / "images", ROOT / "slides" / "images"]
FONT = SRC / "fonts" / "geist-latin.woff2"
PLACEHOLDER = "/*@FONT@*/"


def main() -> None:
    font_b64 = base64.b64encode(FONT.read_bytes()).decode("ascii")
    font_face = (
        "@font-face { font-family: 'Geist'; font-weight: 100 900; "
        f"src: url(data:font/woff2;base64,{font_b64}) format('woff2'); }}"
    )
    for src in sorted(SRC.glob("*.svg")):
        svg = src.read_text(encoding="utf-8")
        if PLACEHOLDER not in svg:
            raise SystemExit(f"{src.name}: Platzhalter {PLACEHOLDER} fehlt")
        for out in OUTS:
            out.mkdir(exist_ok=True)
            (out / src.name).write_text(svg.replace(PLACEHOLDER, font_face), encoding="utf-8")
        print(src.name)


if __name__ == "__main__":
    main()
