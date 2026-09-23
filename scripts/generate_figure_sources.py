"""Erzeugt die Quell-SVGs der Buch-Abbildungen (Welle 1) in figures-src/.

value-proposition-canvas.svg ist handgeschrieben und wird hier nicht erzeugt.
Danach: uv run scripts/build_figures.py (bettet die Schrift ein, schreibt images/).

Aufruf: uv run scripts/generate_figure_sources.py
"""
import math, random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figures-src"

INK = "#16182c"; SOFT = "#555a6e"; DESC = "#3d4255"; PAPER = "#faf9f4"
RULE = "#e2dfd6"; NEUT = "#efece3"; OCH_T = "#f6ecd8"; TER_T = "#f6e4dc"; SLA_T = "#e6e9ef"
OCH = "#c08a3e"; TER = "#b85a3a"; LINE = "#8f8a7c"
C_BLUE = "#3f63a8"; C_OCH = "#b98232"

STYLE = f"""  <style>
    /*@FONT@*/
    text {{ font-family: Geist, 'Helvetica Neue', Arial, sans-serif; }}
    .h   {{ font-size: 17px; font-weight: 600; fill: {INK}; letter-spacing: -0.01em; }}
    .sub {{ font-size: 13px; fill: {SOFT}; }}
    .n   {{ font-size: 15px; font-weight: 600; fill: {INK}; }}
    .d   {{ font-size: 13.5px; fill: {DESC}; }}
    .s   {{ font-size: 12.5px; fill: {SOFT}; }}
    .big {{ font-size: 24px; font-weight: 600; fill: {INK}; letter-spacing: -0.02em; }}
    .num {{ font-size: 12px; font-weight: 600; fill: {PAPER}; }}
    .mono {{ font-family: 'Geist Mono', ui-monospace, Menlo, monospace; font-size: 12.5px; fill: {DESC}; }}
  </style>"""

MARKERS = f"""  <defs>
    <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" fill="{LINE}"/></marker>
    <marker id="ao" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" fill="{OCH}"/></marker>
  </defs>"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, cls="d", anchor="start", extra=""):
    return f'  <text class="{cls}" x="{x:g}" y="{y:g}" text-anchor="{anchor}"{extra}>{esc(s)}</text>'


def lines(x, y, rows, cls="d", anchor="start", lh=18):
    return "\n".join(t(x, y + i * lh, r, cls, anchor) for i, r in enumerate(rows))


def rect(x, y, w, h, fill=NEUT, stroke=INK, sw=1.25, rx=6, extra=""):
    return f'  <rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'


def arrow(x1, y1, x2, y2, color=LINE, marker="ar", sw=1.5, dash=None, both=False):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    ms = f' marker-start="url(#{marker})"' if both else ""
    return f'  <line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{color}" stroke-width="{sw}"{d}{ms} marker-end="url(#{marker})"/>'


def badge(cx, cy, n):
    return f'  <circle cx="{cx:g}" cy="{cy:g}" r="11" fill="{INK}"/>\n' + t(cx, cy + 4.2, str(n), "num", "middle")


def svg(name, w, h, title, desc, body):
    doc = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">
  <title id="t">{esc(title)}</title>
  <desc id="d">{esc(desc)}</desc>
{STYLE}
{MARKERS}
  <rect width="{w}" height="{h}" fill="{PAPER}"/>
{body}
</svg>
"""
    (OUT / f"{name}.svg").write_text(doc, encoding="utf-8")
    print(name)


# ---------------------------------------------------------------- Kundenreise
def kundenreise():
    st = ["Fremde", "Besucher", "Interessenten", "Kunden", "Fürsprecher"]
    tasks = [("Anwerben", ["Suchmaschinenwerbung,", "SEO"]),
             ("Überzeugen", ["Content-Marketing"]),
             ("Gewinnen", ["Angebot,", "Conversion"]),
             ("Binden", ["Service,", "Community"])]
    cx = [75 + 155 * i for i in range(5)]
    fills = ["#f3f0e8", "#efe6d3", "#ead9b9", "#e2c894", OCH]
    b = []
    for i, s in enumerate(st):
        b.append(rect(cx[i] - 60, 20, 120, 46, fills[i], INK, 1.25, 23))
        b.append(t(cx[i], 48, s, "n", "middle", f' style="fill:{PAPER if i == 4 else INK}"' if i == 4 else ""))
    for i in range(4):
        b.append(arrow(cx[i] + 63, 43, cx[i + 1] - 66, 43))
        m = (cx[i] + cx[i + 1]) / 2
        b.append(f'  <path d="M{cx[i]+8},92 L{cx[i]+8},100 L{cx[i+1]-8},100 L{cx[i+1]-8},92" fill="none" stroke="{RULE}" stroke-width="1.5"/>')
        b.append(t(m, 126, tasks[i][0], "n", "middle"))
        b.append(lines(m, 147, tasks[i][1], "s", "middle", 17))
    svg("kundenreise", 770, 190, "Kundenreise von Fremden zu Fürsprechern",
        "Fünf Stationen von links nach rechts: Fremde, Besucher, Interessenten, Kunden, Fürsprecher. Zwischen den Stationen stehen die Marketingaufgaben: Anwerben mit Suchmaschinenwerbung und SEO, Überzeugen mit Content-Marketing, Gewinnen mit Angebot und Conversion, Binden mit Service und Community.",
        "\n".join(b))


# ---------------------------------------------------------- Planungsprozess
def planungsprozess():
    steps = [["Situationsanalyse"], ["Ziele"], ["Zielgruppen"], ["Strategie und", "Positionierung"],
             ["Kanäle und", "Maßnahmen"], ["Budget"], ["Umsetzung"], ["Controlling"]]
    cx, cy, rx, ry = 385, 245, 265, 185
    b = [f'  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{RULE}" stroke-width="2"/>']
    # Richtungspfeile auf dem Ring (im Uhrzeigersinn), 8->1 in Ochre
    for k in range(8):
        a = math.radians(-90 + 45 * k + 22.5)
        px, py = cx + rx * math.cos(a), cy + ry * math.sin(a)
        tx, ty = -rx * math.sin(a), ry * math.cos(a)
        L = math.hypot(tx, ty); tx, ty = tx / L, ty / L
        col = OCH if k == 7 else LINE
        ang = math.degrees(math.atan2(ty, tx))
        b.append(f'  <path d="M-6,-6 L4,0 L-6,6" transform="translate({px:.1f},{py:.1f}) rotate({ang:.1f})" fill="none" stroke="{col}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    # Ochre-Bogen 8 -> 1
    a0, a1 = math.radians(-135), math.radians(-90)
    p0 = (cx + rx * math.cos(a0), cy + ry * math.sin(a0)); p1 = (cx + rx * math.cos(a1), cy + ry * math.sin(a1))
    b.append(f'  <path d="M{p0[0]:.1f},{p0[1]:.1f} A{rx},{ry} 0 0 1 {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="{OCH}" stroke-width="2.5"/>')
    for k, s in enumerate(steps):
        a = math.radians(-90 + 45 * k)
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        w, h = 160, 50
        fill = OCH_T if k in (0, 7) else NEUT
        b.append(rect(x - w / 2, y - h / 2, w, h, fill, INK, 1.25, 8))
        b.append(badge(x - w / 2 + 20, y, k + 1))
        if len(s) == 1:
            b.append(t(x - w / 2 + 38, y + 5, s[0], "n"))
        else:
            b.append(lines(x - w / 2 + 38, y - 4, s, "n", "start", 17))
    b.append(t(cx, cy - 12, "Die Schritte laufen in Schleifen.", "d", "middle"))
    b.append(t(cx, cy + 8, "Keiner wird übersprungen.", "d", "middle"))
    b.append(t(cx, cy + 36, "Controlling liefert das Lagebild", "s", "middle", f' style="fill:{OCH};font-weight:600"'))
    b.append(t(cx, cy + 53, "für die nächste Runde", "s", "middle", f' style="fill:{OCH};font-weight:600"'))
    svg("planungsprozess", 770, 480, "Planungsprozess in acht Schritten",
        "Acht Schritte auf einem Kreislauf im Uhrzeigersinn: 1 Situationsanalyse, 2 Ziele, 3 Zielgruppen, 4 Strategie und Positionierung, 5 Kanäle und Maßnahmen, 6 Budget, 7 Umsetzung, 8 Controlling. Ein hervorgehobener Bogen führt vom Controlling zurück zur Situationsanalyse: Das Controlling liefert das Lagebild für die nächste Runde.",
        "\n".join(b))


# ------------------------------------------------------------ Marktakteure
def werbemarkt():
    boxes = [("Werbungtreibende", "", "und Agenturen", SLA_T), ("DSP", None, "Einkaufssystem", SLA_T),
             ("Ad Exchange", None, "Handelsplatz", NEUT), ("SSP", None, "Verkaufssystem", OCH_T),
             ("Publisher", None, "und Vermarkter", OCH_T)]
    xs = [10 + 153 * i for i in range(5)]; w = 128; y0 = 64; h = 66
    b = []
    b.append(t(10, 30, "Nachfrage", "h")); b.append(t(10, 48, "kauft Werbeplätze", "sub"))
    b.append(t(750, 30, "Angebot", "h", "end")); b.append(t(750, 48, "verkauft Werbeplätze", "sub", "end"))
    for i, (n1, n2, sub, f) in enumerate(boxes):
        x = xs[i]; c = x + w / 2
        b.append(rect(x, y0, w, h, f, INK, 1.25, 8))
        if n2 is not None and n2 == "":
            b.append(t(c, y0 + 28, n1, "n", "middle", ' style="font-size:13.5px"'))
            b.append(t(c, y0 + 48, sub, "s", "middle"))
        else:
            b.append(t(c, y0 + 28, n1, "n", "middle"))
            b.append(t(c, y0 + 48, sub, "s", "middle"))
    for i in range(2):
        b.append(arrow(xs[i] + w + 3, y0 + h / 2, xs[i + 1] - 4, y0 + h / 2))
    for i in (3, 4):
        b.append(arrow(xs[i] - 3, y0 + h / 2, xs[i - 1] + w + 4, y0 + h / 2))
    b.append(t(xs[2] + w / 2, y0 + h + 22, "Gebote in Millisekunden", "s", "middle"))
    # Messdienstleister
    b.append(rect(xs[1], 176, xs[4] + w - xs[1], 34, "none", LINE, 1.25, 8, ' stroke-dasharray="4 4"'))
    b.append(t((xs[1] + xs[4] + w) / 2, 198, "Messdienstleister prüfen Sichtbarkeit und Umfeld", "s", "middle"))
    # Walled Garden
    gx, gy, gw, gh = 170, 246, 580, 104
    b.append(rect(gx, gy, gw, gh, "#f3f0e8", SOFT, 3, 12))
    b.append(t(gx + 18, gy + 26, "Walled Garden", "n"))
    b.append(t(gx + 132, gy + 26, "Suchmaschinen, soziale Netzwerke, Handelsplattformen", "s"))
    for j, lab in enumerate(["Publisher", "Vermarkter", "Messsystem"]):
        cx0 = gx + 18 + j * 186
        b.append(rect(cx0, gy + 46, 172, 40, PAPER, LINE, 1, 20))
        b.append(t(cx0 + 86, gy + 71, lab, "d", "middle"))
    b.append(t(gx + gw - 4, gy + gh + 22, "alles in einem geschlossenen System", "s", "end"))
    # Direktkauf
    x1 = xs[0] + w / 2
    b.append(f'  <path d="M{x1},{y0+h+2} L{x1},{gy+gh/2} L{gx-4},{gy+gh/2}" fill="none" stroke="{LINE}" stroke-width="1.5" marker-end="url(#ar)"/>')
    b.append(t(x1 + 8, gy + gh / 2 - 8, "direkt buchen", "s"))
    svg("werbemarkt-akteure", 770, 380, "Akteure am Online-Werbemarkt",
        "Oben die Handelskette: Werbungtreibende und Agenturen kaufen über eine Demand-Side-Platform, Publisher und Vermarkter verkaufen über eine Supply-Side-Platform, beide treffen sich am Ad Exchange. Messdienstleister prüfen Sichtbarkeit und Umfeld. Unten ein Walled Garden: Suchmaschinen, soziale Netzwerke und Handelsplattformen sind Publisher, Vermarkter und Messsystem in einem geschlossenen System; Werbungtreibende buchen dort direkt.",
        "\n".join(b))


# ------------------------------------------------------------- Empathy Map
def empathy():
    b = []
    X0, Y0, W, H = 100, 16, 480, 290
    cells = [(X0, Y0, "Denken und Fühlen", ["Was beschäftigt sie wirklich,", "auch unausgesprochen?"], "start", 0),
             (X0 + W / 2, Y0, "Sehen", ["Was nimmt die Person in", "ihrem Umfeld wahr?"], "end", 0),
             (X0, Y0 + H / 2, "Hören", ["Welche Stimmen und Quellen", "beeinflussen sie?"], "start", 1),
             (X0 + W / 2, Y0 + H / 2, "Sagen und Tun", ["Wie verhält sie sich", "nach außen?"], "end", 1)]
    for x, y, n, q, anc, bottom in cells:
        b.append(f'  <rect x="{x:g}" y="{y:g}" width="{W/2:g}" height="{H/2:g}" fill="{NEUT}" stroke="{INK}" stroke-width="1"/>')
        tx = x + 18 if anc == "start" else x + W / 2 - 18
        ty = y + 30 if not bottom else y + H / 2 - 62
        b.append(t(tx, ty, n, "n", anc))
        b.append(lines(tx, ty + 22, q, "d", anc))
    b.append(f'  <rect x="{X0}" y="{Y0}" width="{W}" height="{H}" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    ccx, ccy = X0 + W / 2, Y0 + H / 2
    b.append(f'  <circle cx="{ccx}" cy="{ccy}" r="58" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>')
    b.append(f'  <circle cx="{ccx}" cy="{ccy-20}" r="10" fill="none" stroke="{SOFT}" stroke-width="1.5"/>')
    b.append(f'  <path d="M{ccx-16},{ccy+8} Q{ccx},{ccy-12} {ccx+16},{ccy+8}" fill="none" stroke="{SOFT}" stroke-width="1.5"/>')
    b.append(t(ccx, ccy + 28, "eine konkrete", "s", "middle"))
    b.append(t(ccx, ccy + 43, "Person", "s", "middle"))
    y2 = Y0 + H + 16
    b.append(rect(X0, y2, W / 2 - 6, 60, TER_T, INK, 1.25, 6))
    b.append(t(X0 + 18, y2 + 25, "Pains", "n")); b.append(t(X0 + 18, y2 + 46, "Frustrationen, Ängste", "d"))
    b.append(rect(X0 + W / 2 + 6, y2, W / 2 - 6, 60, OCH_T, INK, 1.25, 6))
    b.append(t(X0 + W / 2 + 24, y2 + 25, "Gains", "n")); b.append(t(X0 + W / 2 + 24, y2 + 46, "Wünsche, Erfolgsmaßstäbe", "d"))
    b.append(arrow(X0 + W + 8, y2 + 30, X0 + W + 40, y2 + 30))
    b.append(lines(X0 + W + 48, y2 + 24, ["ins Kundenprofil", "(Value Proposition", "Canvas)"], "s", "start", 16))
    svg("empathy-map", 770, 400, "Empathy Map",
        "Ein Quadrat mit vier Feldern um eine konkrete Person in der Mitte: Denken und Fühlen (Was beschäftigt sie wirklich, auch unausgesprochen?), Sehen (Was nimmt die Person in ihrem Umfeld wahr?), Hören (Welche Stimmen und Quellen beeinflussen sie?), Sagen und Tun (Wie verhält sie sich nach außen?). Darunter die Felder Pains (Frustrationen, Ängste) und Gains (Wünsche, Erfolgsmaßstäbe); ein Pfeil führt ins Kundenprofil des Value Proposition Canvas.",
        "\n".join(b))


# ------------------------------------------------------ Business Model Canvas
def bmc():
    b = []
    X = [20 + 146 * i for i in range(6)]; T, M, B, E = 70, 190, 310, 392
    L_T, C_T, R_T = SLA_T, OCH_T, NEUT
    def cell(x, y, w, h, fill, name, q):
        out = [f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="1"/>']
        out.append(lines(x + 12, y + 24, name, "n", "start", 17))
        out.append(lines(x + 12, y + 24 + 17 * len(name) + 6, q, "s", "start", 16))
        return "\n".join(out)
    b.append(cell(X[0], T, 146, B - T, L_T, ["Schlüssel-", "partner"], ["Wer hilft uns?"]))
    b.append(cell(X[1], T, 146, M - T, L_T, ["Schlüssel-", "aktivitäten"], ["Was müssen wir tun?"]))
    b.append(cell(X[1], M, 146, B - M, L_T, ["Schlüssel-", "ressourcen"], ["Was brauchen wir", "dafür?"]))
    b.append(cell(X[2], T, 146, B - T, C_T, ["Wertangebote"], ["Welchen Nutzen", "stiften wir?"]))
    b.append(cell(X[3], T, 146, M - T, R_T, ["Kunden-", "beziehungen"], ["Welche Beziehung", "pflegen wir?"]))
    b.append(cell(X[3], M, 146, B - M, R_T, ["Kanäle"], ["Wie erreichen wir", "die Kundschaft?"]))
    b.append(cell(X[4], T, 146, B - T, R_T, ["Kunden-", "segmente"], ["Für wen schaffen", "wir Wert?"]))
    b.append(cell(X[0], B, 365, E - B, L_T, ["Kostenstruktur"], ["Welche Kosten entstehen?"]))
    b.append(cell(385, B, 365, E - B, R_T, ["Einnahmequellen"], ["Wofür wird bezahlt?"]))
    b.append(f'  <rect x="20" y="{T}" width="730" height="{E-T}" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    b.append(f'  <path d="M20,52 L20,46 L312,46 L312,52" fill="none" stroke="{SOFT}" stroke-width="1.2"/>')
    b.append(t(166, 34, "nach innen: was wir dafür brauchen", "s", "middle", ' style="font-weight:600"'))
    b.append(f'  <path d="M458,52 L458,46 L750,46 L750,52" fill="none" stroke="{SOFT}" stroke-width="1.2"/>')
    b.append(t(604, 34, "nach außen: Kundschaft und Erträge", "s", "middle", ' style="font-weight:600"'))
    b.append(t(385, 34, "verbindet", "s", "middle", f' style="font-weight:600;fill:{OCH}"'))
    b.append(arrow(385, 40, 385, 60, OCH, "ao"))
    svg("business-model-canvas", 770, 405, "Business Model Canvas",
        "Das Raster mit neun Bausteinen. Links, nach innen gerichtet: Schlüsselpartner, Schlüsselaktivitäten, Schlüsselressourcen und darunter Kostenstruktur. In der Mitte hervorgehoben: Wertangebote, die beide Seiten verbinden. Rechts, nach außen gerichtet: Kundenbeziehungen, Kanäle, Kundensegmente und darunter Einnahmequellen. Jedes Feld nennt seine Leitfrage.",
        "\n".join(b))


# --------------------------------------------------------------------- STP
def stp():
    rnd = random.Random(7)
    centers = [(60, 70), (160, 60), (70, 165), (165, 165)]
    pts = []
    for ci, (x, y) in enumerate(centers):
        for _ in range(9):
            pts.append((ci, x + rnd.gauss(0, 15), y + rnd.gauss(0, 13)))
    b = []
    PX = [10, 270, 530]; PY = 78; PW, PH = 230, 230
    heads = [("Segmentierung", ["Markt in Gruppen mit", "ähnlichen Bedürfnissen teilen"]),
             ("Targeting", ["Segmente wählen: attraktiv", "und passend zu unseren Stärken"]),
             ("Positionierung", ["in der Wahrnehmung verankern,", "abgegrenzt vom Wettbewerb"])]
    for p in range(3):
        x0 = PX[p]
        b.append(badge(x0 + 11, 22, p + 1))
        b.append(t(x0 + 30, 28, heads[p][0], "h"))
        b.append(lines(x0, 50, heads[p][1], "s", "start", 16))
        b.append(rect(x0, PY, PW, PH, "#f3f0e8", RULE, 1, 10))
        for ci, (cx0, cy0) in enumerate(centers):
            chosen = ci == 1
            if p == 0 or (p == 1) or (p == 2 and chosen):
                stroke = OCH if (p >= 1 and chosen) else LINE
                dash = "" if (p >= 1 and chosen) else ' stroke-dasharray="3 4"'
                b.append(f'  <ellipse cx="{x0+cx0+10}" cy="{PY+cy0+15}" rx="44" ry="38" fill="none" stroke="{stroke}" stroke-width="1.4"{dash}/>')
        for ci, x, y in pts:
            chosen = ci == 1
            if p == 0:
                col = "#8f8a7c"
            elif p == 1:
                col = OCH if chosen else "#cfc9ba"
            else:
                if not chosen:
                    continue
                col = OCH
            b.append(f'  <circle cx="{x0+x+10:.1f}" cy="{PY+y+15:.1f}" r="4.2" fill="{col}"/>')
        if p < 2:
            b.append(arrow(x0 + PW + 6, PY + PH / 2, x0 + PW + 34, PY + PH / 2))
    # Positionierung: Nutzenversprechen
    x0 = PX[2]
    b.append(rect(x0 + 24, PY + 150, 182, 52, PAPER, OCH, 1.5, 8))
    b.append(t(x0 + 115, PY + 172, "klares Nutzenversprechen", "s", "middle"))
    b.append(t(x0 + 115, PY + 189, "für dieses Segment", "s", "middle"))
    b.append(f'  <line x1="{x0+170}" y1="{PY+106}" x2="{x0+150}" y2="{PY+148}" stroke="{OCH}" stroke-width="1.5"/>')
    b.append(t(PX[0], PY + PH + 26, "Kriterien: geografisch, demografisch,", "s"))
    b.append(t(PX[0], PY + PH + 42, "psychografisch, verhaltensbezogen", "s"))
    b.append(t(PX[1], PY + PH + 26, "Leitfragen: Wie attraktiv ist", "s"))
    b.append(t(PX[1], PY + PH + 42, "das Segment? Wie gut passt es?", "s"))
    b.append(t(PX[2], PY + PH + 26, "eigene Lesson", "s"))
    svg("stp-modell", 770, 360, "STP-Modell: Segmentierung, Targeting, Positionierung",
        "Drei Felder mit Punkten, die Menschen im Markt darstellen. 1 Segmentierung: Die Punkte bilden vier Gruppen mit ähnlichen Bedürfnissen, gebildet nach geografischen, demografischen, psychografischen und verhaltensbezogenen Kriterien. 2 Targeting: Eine Gruppe ist hervorgehoben, die übrigen sind blass; Leitfragen sind Attraktivität und Passung. 3 Positionierung: Nur das gewählte Segment bleibt, verbunden mit einem klaren Nutzenversprechen, abgegrenzt vom Wettbewerb.",
        "\n".join(b))


# --------------------------------------------------------- Kennzahlenbaum
def kennzahlenbaum():
    b = []
    cols = [(20, 230, 3, "Frühindikatoren", "zeigen unterwegs die Richtung"),
            (290, 210, 2, "Ergebnisindikator", "misst, ob das Ziel erreicht ist"),
            (540, 210, 1, "Ziel", "mit Kennzahl und Termin")]
    for x, w, n, name, sub in cols:
        b.append(badge(x + 11, 24, n)); b.append(t(x + 30, 30, name, "h")); b.append(t(x, 52, sub, "sub"))
    b.append(rect(20, 72, 230, 56, NEUT)); b.append(lines(36, 96, ["Besuche auf der", "Anmeldeseite"], "d"))
    b.append(rect(20, 146, 230, 56, NEUT)); b.append(lines(36, 170, ["Conversion-Rate vom", "Besuch zur Anmeldung"], "d"))
    b.append(rect(290, 106, 210, 60, NEUT)); b.append(lines(306, 131, ["abgeschlossene", "Anmeldungen (gemessen)"], "d"))
    b.append(rect(540, 106, 210, 60, OCH_T, INK, 1.5)); b.append(t(556, 130, "80 Webinar-Anmeldungen", "n")); b.append(t(556, 150, "bis Ende September", "d"))
    b.append(f'  <path d="M252,100 C272,100 270,136 286,136" fill="none" stroke="{LINE}" stroke-width="1.5" marker-end="url(#ar)"/>')
    b.append(f'  <path d="M252,174 C272,174 270,136 286,136" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    b.append(arrow(502, 136, 536, 136))
    b.append(t(385, 232, "Abgeleitet wird von rechts nach links, gemessen von links nach rechts.", "s", "middle"))
    b.append(arrow(20, 256, 750, 256, SOFT, "ar", 1.2))
    b.append(t(20, 276, "unterwegs, früh sichtbar", "s")); b.append(t(750, 276, "am Ende der Kampagne", "s", "end"))
    b.append(rect(20, 296, 730, 44, "#f3f0e8", RULE, 1, 8))
    b.append(badge(42, 318, 4)); b.append(t(62, 323, "Rhythmus festlegen:", "n"))
    b.append(t(214, 323, "wie oft und aus welcher Datenquelle wir die Werte ablesen", "d"))
    svg("ziel-kennzahlen", 770, 352, "Vom Ziel zur Kennzahl am Webinar-Beispiel",
        "Rechts das Ziel: 80 Webinar-Anmeldungen bis Ende September (Schritt 1). In der Mitte der Ergebnisindikator: gemessene abgeschlossene Anmeldungen (Schritt 2). Links zwei Frühindikatoren: Besuche auf der Anmeldeseite und Conversion-Rate vom Besuch zur Anmeldung (Schritt 3). Pfeile zeigen, dass die Frühindikatoren auf den Ergebnisindikator und dieser auf das Ziel einzahlen. Eine Zeitachse zeigt: Frühindikatoren sind unterwegs sichtbar, der Ergebnisindikator am Ende. Schritt 4: Rhythmus festlegen, wie oft und aus welcher Datenquelle wir ablesen.",
        "\n".join(b))


# ------------------------------------------------------------ Anzeigenrang
def anzeigenrang():
    rows = [("B", 2.00, 8, 16, "1,76 €"), ("C", 3.50, 4, 14, "3,01 €"), ("A", 4.00, 3, 12, "Mindestpreis")]
    b = []
    hy = 30
    b.append(t(20, hy, "Position", "s", "start", ' style="font-weight:600"'))
    b.append(t(170, hy, "Höchstgebot", "s", "start", ' style="font-weight:600"'))
    b.append(t(352, hy, "× Qualität", "s", "middle", ' style="font-weight:600"'))
    b.append(t(410, hy, "= Anzeigenrang", "s", "start", ' style="font-weight:600"'))
    b.append(t(750, hy, "tatsächlicher Klickpreis", "s", "end", ' style="font-weight:600"'))
    b.append(f'  <line x1="20" y1="42" x2="750" y2="42" stroke="{INK}" stroke-width="1.5"/>')
    for i, (who, bid, q, rank, cpc) in enumerate(rows):
        y = 58 + i * 62; cyy = y + 22
        b.append(badge(31, cyy, i + 1))
        b.append(t(52, cyy + 5, f"Anbieter {who}", "n"))
        bw = bid * 27
        b.append(f'  <path d="M170,{y+10} h{bw-4:.1f} a4,4 0 0 1 4,4 v16 a4,4 0 0 1 -4,4 h-{bw-4:.1f} Z" fill="{C_BLUE}"/>')
        b.append(t(170 + bw + 8, cyy + 5, f"{bid:.2f} €".replace(".", ","), "d"))
        b.append(t(352, cyy + 5, str(q), "n", "middle"))
        rw = rank * 14
        b.append(f'  <path d="M410,{y+10} h{rw-4:.1f} a4,4 0 0 1 4,4 v16 a4,4 0 0 1 -4,4 h-{rw-4:.1f} Z" fill="{C_OCH}"/>')
        b.append(t(410 + rw + 8, cyy + 5, str(rank), "n"))
        b.append(t(750, cyy + 5, cpc, "n" if "€" in cpc else "d", "end"))
        b.append(f'  <line x1="20" y1="{y+52}" x2="750" y2="{y+52}" stroke="{RULE}" stroke-width="1"/>')
    b.append(t(20, 268, "Das höchste Gebot (A) landet auf Position 3. B bietet am wenigsten und steht wegen hoher Qualität oben.", "d"))
    b.append(t(20, 290, "Vereinfacht, fiktive Zahlen: Klickpreis = Rang der nächsten Anzeige ÷ eigene Qualität + 0,01 €.", "s"))
    svg("anzeigenrang", 770, 302, "Rechenbeispiel Anzeigenrang",
        "Drei Anbieter in einer vereinfachten Auktion mit fiktiven Zahlen. Position 1: Anbieter B, Höchstgebot 2,00 Euro, Qualität 8, Anzeigenrang 16, Klickpreis 1,76 Euro. Position 2: Anbieter C, 3,50 Euro, Qualität 4, Rang 14, Klickpreis 3,01 Euro. Position 3: Anbieter A, 4,00 Euro, Qualität 3, Rang 12, zahlt den Mindestpreis. Das höchste Gebot landet auf dem letzten Platz. Klickpreis vereinfacht: Rang der nächsten Anzeige geteilt durch eigene Qualität plus 0,01 Euro.",
        "\n".join(b))


# -------------------------------------------------------- Kampagnenstruktur
def kampagne():
    b = []
    lab = [(92, "Kampagne", ["Ziel und Budget"]), (172, "Anzeigengruppe", ["ein eng umrissenes", "Thema"]),
           (300, "Keywords und", ["Anzeigen mit", "passender Zielseite"])]
    for y, n, s in lab:
        b.append(t(20, y, n, "n")); b.append(lines(20, y + 20, s, "s", "start", 16))
    b.append(f'  <line x1="190" y1="20" x2="190" y2="400" stroke="{RULE}" stroke-width="1"/>')
    b.append(t(485, 30, "Google-Ads-Konto", "s", "middle"))
    b.append(arrow(485, 38, 485, 62))
    b.append(rect(375, 66, 220, 50, OCH_T, INK, 1.5, 8))
    b.append(t(485, 88, "Kaffeemaschinen", "n", "middle")); b.append(t(485, 106, "Ziel und Budget", "s", "middle"))
    groups = [(215, "Siebträger", ["siebträgermaschine kaufen", "siebträger dualboiler"], "Siebträger vom Fachhändler", "/siebtraeger"),
              (505, "Vollautomaten", ["kaffeevollautomat kaufen", "vollautomat milchsystem"], "Vollautomaten mit Beratung", "/vollautomaten")]
    for x, name, kws, ad, url in groups:
        w = 245; c = x + w / 2
        b.append(f'  <path d="M485,118 L485,136 L{c},136 L{c},150" fill="none" stroke="{LINE}" stroke-width="1.5" marker-end="url(#ar)"/>')
        b.append(rect(x, 154, w, 46, NEUT, INK, 1.25, 8))
        b.append(t(c, 182, name, "n", "middle"))
        b.append(arrow(c, 202, c, 222))
        b.append(rect(x, 226, w, 170, PAPER, INK, 1.25, 8))
        b.append(t(x + 14, 248, "Keywords", "s", "start", ' style="font-weight:600"'))
        for j, k in enumerate(kws):
            b.append(rect(x + 14, 256 + j * 28, w - 28, 22, "#f3f0e8", RULE, 1, 4))
            b.append(t(x + 22, 271 + j * 28, k, "mono"))
        b.append(t(x + 14, 334, "Anzeigentext", "s", "start", ' style="font-weight:600"'))
        b.append(t(x + 14, 352, ad, "d"))
        b.append(t(x + 14, 376, "Zielseite", "s", "start", ' style="font-weight:600"'))
        b.append(t(x + 84, 376, url, "mono"))
    svg("kampagnenstruktur", 770, 410, "Kampagnenstruktur in Google Ads",
        "Ein Google-Ads-Konto enthält die Kampagne Kaffeemaschinen mit Ziel und Budget. Darunter zwei Anzeigengruppen, Siebträger und Vollautomaten, jeweils ein eng umrissenes Thema. In jeder Anzeigengruppe liegen passende Keywords, ein Anzeigentext und eine eigene Zielseite, etwa siebträgermaschine kaufen, Siebträger vom Fachhändler und die Seite /siebtraeger. Fiktives Beispiel.",
        "\n".join(b))


# ------------------------------------------------------------ Kostenbezug
def kostenbezug():
    b = []
    b.append(rect(285, 16, 200, 56, OCH_T, INK, 1.5, 8))
    b.append(t(385, 40, "Werbekosten der Woche", "s", "middle")); b.append(t(385, 63, "2.000 €", "big", "middle"))
    boxes = [("2.000 € ÷ 1.000 Klicks", "2 €", "CPC", ["Werbekosten je Klick"]),
             ("2.000 € ÷ 40 Bestellungen", "50 €", "Kosten je Bestellung", ["kein Kunden-CAC"]),
             ("2.000 € ÷ 25 Neukunden", "80 €", "Medien-CAC", ["je erstmals kaufende", "Person"]),
             ("4.000 € Umsatz ÷ 2.000 €", "2", "ROAS", ["Umsatz je Werbe-Euro,", "kein Gewinn"])]
    for i, (f, v, n, s) in enumerate(boxes):
        x = 20 + 188 * i; w = 176; c = x + w / 2
        b.append(f'  <path d="M385,74 L385,94 L{c},94 L{c},110" fill="none" stroke="{LINE}" stroke-width="1.5" marker-end="url(#ar)"/>')
        b.append(rect(x, 114, w, 150, NEUT if i < 3 else SLA_T, INK, 1.25, 8))
        b.append(t(c, 138, f, "s", "middle"))
        b.append(t(c, 176, v, "big", "middle"))
        b.append(t(c, 202, n, "n", "middle"))
        b.append(lines(c, 224, s, "s", "middle", 16))
    b.append(t(385, 292, "Gleicher Zähler, andere Nenner: Jede Kennzahl beantwortet eine andere Frage.", "d", "middle"))
    svg("kostenbezug", 770, 304, "Ein Kostenblock, verschiedene Bezugsgrößen",
        "Oben die Werbekosten einer Woche: 2.000 Euro. Darunter vier Kennzahlen aus dem fiktiven Shop-Beispiel: 2.000 Euro geteilt durch 1.000 Klicks ergibt einen CPC von 2 Euro. Geteilt durch 40 Bestellungen ergibt 50 Euro Kosten je Bestellung, kein Kunden-CAC. Geteilt durch 25 Neukunden ergibt einen Medien-CAC von 80 Euro. 4.000 Euro zugeordneter Nettoumsatz geteilt durch 2.000 Euro ergibt einen ROAS von 2, also Umsatz je Werbe-Euro, kein Gewinn.",
        "\n".join(b))


# ------------------------------------------------------------ Attribution
def attribution():
    b = []
    b.append(rect(140, 16, 150, 44, "#f4ead8", C_OCH, 1.5, 22)); b.append(t(215, 43, "Social Media", "n", "middle"))
    b.append(rect(330, 16, 150, 44, "#e3e8f3", C_BLUE, 1.5, 22)); b.append(t(405, 43, "Suchanzeige", "n", "middle"))
    b.append(rect(520, 16, 150, 44, NEUT, INK, 1.25, 22)); b.append(t(595, 43, "Kauf", "n", "middle"))
    b.append(arrow(292, 38, 326, 38)); b.append(arrow(482, 38, 516, 38))
    b.append(t(405, 82, "100 Käufe nehmen genau diesen Weg (fiktives Beispiel)", "s", "middle"))
    sx = 240; sc = 2.5  # 100 Käufe = 250 px
    def seg(x, y, w, col, left=False, right=False):
        return f'  <rect x="{x:g}" y="{y}" width="{w:g}" height="26" rx="4" fill="{col}"/>'
    rows = [("Last-Click", [("Suche", 100, C_BLUE)]),
            ("Gleichmäßig", [("Social", 50, C_OCH), ("Suche", 50, C_BLUE)]),
            ("Beide Werbekonten", [("Social-Konto", 100, C_OCH), ("Such-Konto", 100, C_BLUE)])]
    for i, (name, segs) in enumerate(rows):
        y = 128 + i * 66
        b.append(t(20, y + 18, name, "n"))
        if i == 2:
            b.append(t(20, y + 36, "melden je 100", "s"))
        x = sx
        for lab, v, col in segs:
            w = v * sc
            b.append(seg(x + 1, y, w - 2, col))
            b.append(t(x + w / 2, y - 7, f"{lab} {v}", "s", "middle", f' style="fill:{INK}"'))
            x += w
        if i == 1:
            b.append(t(sx + 100 * sc + 10, y + 18, "Summe 100", "d"))
        if i == 0:
            b.append(t(sx + 100 * sc + 10, y + 18, "Summe 100", "d"))
        if i == 2:
            b.append(t(sx + 200 * sc - 4, y + 44, "keine 200 Käufe", "d", "end", f' style="fill:{TER};font-weight:600"'))
    b.append(f'  <line x1="{sx+100*sc}" y1="112" x2="{sx+100*sc}" y2="{128+2*66+34}" stroke="{INK}" stroke-width="1.25" stroke-dasharray="4 3"/>')
    b.append(t(sx + 100 * sc, 106, "tatsächlich 100 Käufe", "s", "middle", ' style="font-weight:600"'))
    svg("attribution-zurechnung", 770, 312, "Zurechnung verteilt, sie vermehrt nicht",
        "Oben der Weg: Social Media, dann Suchanzeige, dann Kauf; 100 Käufe nehmen diesen Weg. Darunter Balken: Last-Click schreibt der Suche 100 Käufe zu. Eine gleichmäßige Regel gibt Social und Suche je 50, Summe 100. Melden beide Werbekonten je 100, ergibt die Summe 200, eine gestrichelte Linie markiert die tatsächlichen 100 Käufe: Es sind keine 200 Käufe.",
        "\n".join(b))


for f in [kundenreise, planungsprozess, werbemarkt, empathy, bmc, stp, kennzahlenbaum, anzeigenrang, kampagne, kostenbezug, attribution]:
    f()
