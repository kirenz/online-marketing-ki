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


# ================================================================ Welle 2

# ------------------------------------------------------------ Marketing-Mix
def marketing_mix():
    rows = [("Product", "Produkt", "Customer Value", "Kundennutzen", "Welchen Nutzen hat die Kundschaft?"),
            ("Price", "Preis", "Cost", "Gesamtkosten", "Was kostet es die Kundschaft insgesamt?"),
            ("Place", "Distribution", "Convenience", "Bequemlichkeit", "Wie einfach ist der Zugang?"),
            ("Promotion", "Kommunikation", "Communication", "Dialog", "Wie entsteht ein echter Austausch?")]
    b = [t(20, 30, "Vier P", "h"), t(20, 48, "Sicht des Anbieters", "sub"),
         t(300, 30, "Vier C", "h"), t(300, 48, "Sicht der Kundschaft", "sub"),
         t(530, 48, "Leitfrage", "sub")]
    for i, (p1, p2, c1, c2, q) in enumerate(rows):
        y = 66 + i * 66
        b.append(rect(20, y, 220, 52, SLA_T, INK, 1.25, 8))
        b.append(t(36, y + 22, p1, "n")); b.append(t(36, y + 41, p2, "s"))
        b.append(arrow(246, y + 26, 294, y + 26))
        b.append(rect(300, y, 220, 52, OCH_T, INK, 1.25, 8))
        b.append(t(316, y + 22, c1, "n")); b.append(t(316, y + 41, c2, "s"))
        words = q.split(" "); half = (len(words) + 1) // 2
        b.append(lines(530, y + 22, [" ".join(words[:half]), " ".join(words[half:])], "d", "start", 18))
    b.append(t(20, 350, "Die Hebel wirken nur zusammen: Sie sollen dieselbe Geschichte erzählen.", "d"))
    svg("marketing-mix", 770, 362, "Vier P und vier C",
        "Links die vier P aus Sicht des Anbieters: Product, Price, Place, Promotion. Pfeile führen zu den vier C aus Sicht der Kundschaft: Customer Value (Kundennutzen), Cost (Gesamtkosten), Convenience (Bequemlichkeit), Communication (Dialog). Rechts je eine Leitfrage. Darunter der Satz: Die Hebel wirken nur zusammen.",
        "\n".join(b))


# ----------------------------------------------------------- Positionierung
def positionierung():
    X0, Y0, W, H = 90, 20, 600, 320
    b = [f'  <rect x="{X0}" y="{Y0}" width="{W}" height="{H}" fill="#f3f0e8" stroke="{RULE}"/>',
         f'  <line x1="{X0+W/2}" y1="{Y0}" x2="{X0+W/2}" y2="{Y0+H}" stroke="{RULE}" stroke-width="1.5"/>',
         f'  <line x1="{X0}" y1="{Y0+H/2}" x2="{X0+W}" y2="{Y0+H/2}" stroke="{RULE}" stroke-width="1.5"/>',
         arrow(X0, Y0 + H + 14, X0 + W, Y0 + H + 14, SOFT, "ar", 1.2),
         t(X0, Y0 + H + 34, "breites Sortiment", "s"), t(X0 + W, Y0 + H + 34, "spezialisiert", "s", "end"),
         t(X0 + W / 2, Y0 + H + 34, "Spezialisierung", "s", "middle", ' style="font-weight:600"'),
         f'  <line x1="{X0-14}" y1="{Y0+H}" x2="{X0-14}" y2="{Y0+6}" stroke="{SOFT}" stroke-width="1.2" marker-end="url(#ar)"/>',
         t(X0 - 22, Y0 + 12, "hoch", "s", "end"), t(X0 - 22, Y0 + H, "niedrig", "s", "end"),
         t(X0 - 22, Y0 + H / 2 + 4, "Preis", "s", "end", ' style="font-weight:600"')]
    comp = [("A", 180, 280), ("B", 250, 240), ("C", 215, 100), ("D", 330, 290)]
    for n, x, y in comp:
        b.append(f'  <circle cx="{x}" cy="{y}" r="17" fill="{NEUT}" stroke="{LINE}" stroke-width="1.5"/>')
        b.append(t(x, y + 5, n, "n", "middle", f' style="fill:{SOFT}"'))
    b.append(t(265, 322, "Wettbewerb drängt sich hier", "s", "middle"))
    gx, gy = 580, 100
    b.append(f'  <circle cx="{gx}" cy="{gy}" r="60" fill="{OCH_T}" stroke="{OCH}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    b.append(t(gx, gy - 4, "freier,", "n", "middle")); b.append(t(gx, gy + 15, "attraktiver Platz", "s", "middle"))
    b.append(t(X0, 396, "Die Achsen sind die Dimensionen, die für die Zielgruppe entscheiden. Fiktives Beispiel.", "s"))
    svg("positionierungskarte", 770, 408, "Positionierungskarte",
        "Ein Achsenkreuz mit Spezialisierung (von breitem Sortiment bis spezialisiert) und Preis (von niedrig bis hoch). Vier Wettbewerber A bis D stehen überwiegend im Bereich breit und günstig bis mittel. Oben rechts, spezialisiert und hochpreisig, ist ein freier, attraktiver Platz markiert. Fiktives Beispiel.",
        "\n".join(b))


# ---------------------------------------------------------- Core Web Vitals
def core_web_vitals():
    b = []
    panels = [("LCP", "Largest Contentful Paint", "Ladewahrnehmung", ["Wann erscheint der größte", "sichtbare Inhalt?"]),
              ("INP", "Interaction to Next Paint", "Reaktionsfähigkeit", ["Wie schnell reagiert die Seite", "sichtbar auf Eingaben?"]),
              ("CLS", "Cumulative Layout Shift", "visuelle Stabilität", ["Wie stark verrutschen", "Elemente ungewollt?"])]
    for i, (k, full, what, q) in enumerate(panels):
        x = 20 + 250 * i; w = 230
        b.append(t(x, 30, k, "h")); b.append(t(x + 42, 30, what, "d"))
        b.append(t(x, 50, full, "s"))
        # Browserrahmen
        fy = 66
        b.append(rect(x, fy, w, 190, PAPER, INK, 1.25, 8))
        b.append(f'  <line x1="{x}" y1="{fy+22}" x2="{x+w}" y2="{fy+22}" stroke="{RULE}" stroke-width="1.2"/>')
        for d in range(3):
            b.append(f'  <circle cx="{x+14+d*12}" cy="{fy+11}" r="3.2" fill="{RULE}"/>')
        if i == 0:
            b.append(f'  <rect x="{x+14}" y="{fy+34}" width="{w-28}" height="86" rx="4" fill="{OCH_T}" stroke="{OCH}" stroke-width="1.5"/>')
            b.append(t(x + w / 2, fy + 82, "größter Inhalt", "s", "middle", f' style="fill:{INK}"'))
            for j in range(3):
                b.append(f'  <rect x="{x+14}" y="{fy+132+j*14}" width="{(w-28)*(0.9-0.2*j):.0f}" height="6" rx="3" fill="{RULE}"/>')
        elif i == 1:
            for j in range(4):
                b.append(f'  <rect x="{x+14}" y="{fy+36+j*14}" width="{(w-28)*(0.95-0.15*j):.0f}" height="6" rx="3" fill="{RULE}"/>')
            b.append(f'  <rect x="{x+14}" y="{fy+106}" width="96" height="30" rx="15" fill="{NEUT}" stroke="{INK}" stroke-width="1.2"/>')
            b.append(t(x + 62, fy + 126, "Absenden", "s", "middle", f' style="fill:{INK}"'))
            b.append(f'  <path d="M{x+92},{fy+128} l0,16 l4,-4 l4,8 l3,-1.5 l-4,-8 l6,0 Z" fill="{INK}"/>')
            b.append(f'  <rect x="{x+124}" y="{fy+106}" width="{w-138}" height="30" rx="4" fill="{OCH_T}" stroke="{OCH}" stroke-width="1.5"/>')
            b.append(t(x + 124 + (w - 138) / 2, fy + 126, "Reaktion", "s", "middle", f' style="fill:{INK}"'))
            b.append(arrow(x + 112, fy + 121, x + 121, fy + 121, OCH, "ao", 1.5))
        else:
            b.append(f'  <rect x="{x+14}" y="{fy+34}" width="{w-28}" height="30" rx="15" fill="none" stroke="{LINE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
            b.append(t(x + w / 2, fy + 54, "hier wollten wir klicken", "s", "middle"))
            b.append(f'  <rect x="{x+14}" y="{fy+72}" width="{w-28}" height="44" rx="4" fill="{TER_T}" stroke="{TER}" stroke-width="1.5"/>')
            b.append(t(x + w / 2, fy + 99, "nachgeladenes Banner", "s", "middle", f' style="fill:{INK}"'))
            b.append(f'  <rect x="{x+14}" y="{fy+124}" width="{w-28}" height="30" rx="15" fill="{NEUT}" stroke="{INK}" stroke-width="1.2"/>')
            b.append(t(x + w / 2, fy + 144, "Schaltfläche", "s", "middle", f' style="fill:{INK}"'))
            b.append(arrow(x + w - 22, fy + 66, x + w - 22, fy + 120, TER, "ar", 1.5))
        b.append(lines(x, fy + 216, q, "d", "start", 18))
    b.append(t(20, 340, "Konkrete Zielwerte legt Google fest und passt sie an; wir schlagen sie in der aktuellen Dokumentation nach.", "s"))
    svg("core-web-vitals", 770, 352, "Die drei Core Web Vitals",
        "Drei stilisierte Browserfenster. LCP, Largest Contentful Paint, Ladewahrnehmung: Ein großer Inhaltsblock ist hervorgehoben; Frage: Wann erscheint der größte sichtbare Inhalt? INP, Interaction to Next Paint, Reaktionsfähigkeit: Ein Klick auf Absenden führt zu einer sichtbaren Reaktion; Frage: Wie schnell reagiert die Seite sichtbar auf Eingaben? CLS, Cumulative Layout Shift, visuelle Stabilität: Ein nachgeladenes Banner schiebt eine Schaltfläche nach unten; Frage: Wie stark verrutschen Elemente ungewollt? Hinweis: Zielwerte in der aktuellen Dokumentation nachschlagen.",
        "\n".join(b))


# ------------------------------------------------------------ Suchintention
def suchintention():
    cards = [("Informieren", "etwas verstehen wollen", "was ist ein siebträger", "Ratgeber-Text", NEUT),
             ("Navigieren", "eine bestimmte Seite ansteuern", "kaffeehaus müller login", "die gesuchte Seite", NEUT),
             ("Kommerziell vergleichen", "Optionen abwägen", "siebträger oder vollautomat", "Vergleich", OCH_T),
             ("Transaktional handeln", "kaufen oder buchen", "siebträger kaufen", "Produktseite", OCH_T)]
    b = []
    for i, (n, d, q, fmt, f) in enumerate(cards):
        x = 20 + (i % 2) * 370; y = 16 + (i // 2) * 168; w = 360; h = 154
        b.append(rect(x, y, w, h, f, INK, 1.25, 8))
        b.append(t(x + 18, y + 30, n, "n")); b.append(t(x + 18, y + 50, d, "s"))
        b.append(rect(x + 18, y + 64, w - 36, 32, PAPER, RULE, 1, 16))
        b.append(f'  <circle cx="{x+36}" cy="{y+80}" r="5.5" fill="none" stroke="{SOFT}" stroke-width="1.5"/><line x1="{x+40}" y1="{y+84}" x2="{x+45}" y2="{y+89}" stroke="{SOFT}" stroke-width="1.5"/>')
        b.append(t(x + 54, y + 85, q, "mono"))
        b.append(t(x + 18, y + 128, "passendes Format:", "s")); b.append(t(x + 136, y + 128, fmt, "n", "start", ' style="font-size:14px"'))
    b.append(t(20, 358, "Das Format folgt der Absicht, nicht umgekehrt. Beispielsuchen fiktiv.", "s"))
    svg("suchintention", 770, 368, "Vier Suchintentionen",
        "Vier Karten. Informieren, etwas verstehen wollen, Beispielsuche: was ist ein siebträger, passendes Format: Ratgeber-Text. Navigieren, eine bestimmte Seite ansteuern, Beispiel: kaffeehaus müller login, Format: die gesuchte Seite. Kommerziell vergleichen, Optionen abwägen, Beispiel: siebträger oder vollautomat, Format: Vergleich. Transaktional handeln, kaufen oder buchen, Beispiel: siebträger kaufen, Format: Produktseite.",
        "\n".join(b))


# ------------------------------------------------------------ Quality Score
def quality_score():
    b = []
    stations = [(20, "Suchanfrage", "siebträger kaufen", True), (275, "Anzeige", "Siebträger vom Fachhändler", False), (530, "Zielseite", "/siebtraeger", True)]
    for x, n, ex, mono in stations:
        b.append(rect(x, 20, 220, 64, NEUT, INK, 1.25, 8))
        b.append(t(x + 16, 44, n, "n"))
        b.append(t(x + 16, 68, ex, "mono" if mono else "d"))
    b.append(arrow(243, 52, 271, 52)); b.append(arrow(498, 52, 526, 52))
    b.append(t(512, 40, "Klick", "s", "middle"))
    comps = [(150, "Anzeigenrelevanz", "Passt der Anzeigentext zur Suche?", ["Begriffe aus dem Keyword", "im Anzeigentext, enge", "Anzeigengruppen"], (130, 262)),
             (385, "Erwartete Klickrate", "Wie wahrscheinlich ist ein Klick?", ["Suchbegriff aufgreifen,", "klarer Nutzen, eindeutige", "Handlungsaufforderung"], (385, 385)),
             (640, "Zielseiten-Erfahrung", "Hilft die Seite nach dem Klick?", ["schnell, übersichtlich,", "inhaltlich passend"], (640, 640))]
    for cx0, n, q, lever, (fx1, fx2) in comps:
        x = cx0 - 115
        b.append(f'  <path d="M{fx1},92 L{fx1},104 L{fx2},104 L{fx2},92" fill="none" stroke="{OCH}" stroke-width="1.5"/>' if fx1 != fx2 else f'  <line x1="{fx1}" y1="92" x2="{fx1}" y2="104" stroke="{OCH}" stroke-width="1.5"/>')
        b.append(f'  <line x1="{cx0}" y1="104" x2="{cx0}" y2="118" stroke="{OCH}" stroke-width="1.5"/>')
        b.append(rect(x, 120, 230, 70, OCH_T, INK, 1.25, 8))
        b.append(t(x + 14, 144, n, "n")); b.append(t(x + 14, 166, q, "s"))
        b.append(t(x + 14, 216, "Hebel", "s", "start", ' style="font-weight:600"'))
        b.append(lines(x + 14, 236, lever, "d", "start", 18))
    b.append(rect(20, 300, 730, 40, "#f3f0e8", RULE, 1, 8))
    b.append(t(36, 325, "Quality Score 1 bis 10: Diagnosewert. Wir verbessern die drei Komponenten, nicht die Zahl.", "d"))
    svg("quality-score", 770, 352, "Drei Komponenten des Quality Score",
        "Oben der Weg Suchanfrage (siebträger kaufen), Anzeige (Siebträger vom Fachhändler), nach dem Klick die Zielseite (/siebtraeger). Darunter drei Komponenten mit Hebeln: Anzeigenrelevanz zwischen Suche und Anzeige, Hebel: Begriffe aus dem Keyword im Anzeigentext, enge Anzeigengruppen. Erwartete Klickrate an der Anzeige, Hebel: Suchbegriff aufgreifen, klarer Nutzen, eindeutige Handlungsaufforderung. Zielseiten-Erfahrung, Hebel: schnell, übersichtlich, inhaltlich passend. Unten: Quality Score 1 bis 10 ist ein Diagnosewert; verbessert werden die Komponenten.",
        "\n".join(b))


# ---------------------------------------------------- Markenaufbau/Aktivierung
def marke_aktivierung():
    b = []
    b.append(rect(20, 20, 360, 176, SLA_T, INK, 1.25, 8))
    b.append(t(40, 50, "Markenaufbau", "h"))
    b.append(lines(40, 80, ["wirkt langfristig", "spricht eine breite Zielgruppe an", "sorgt dafür, dass wir überhaupt", "in Erwägung gezogen werden"], "d", "start", 22))
    b.append(rect(390, 20, 360, 176, OCH_T, INK, 1.25, 8))
    b.append(t(410, 50, "Aktivierung", "h"))
    b.append(lines(410, 80, ["wirkt kurzfristig", "spricht kaufbereite Kontakte an", "löst Handlungen aus, etwa", "Anfragen oder Anmeldungen"], "d", "start", 22))
    b.append(t(20, 232, "Budget", "n"))
    b.append(f'  <rect x="90" y="216" width="330" height="26" rx="4" fill="{C_BLUE}"/>')
    b.append(f'  <rect x="422" y="216" width="328" height="26" rx="4" fill="{C_OCH}"/>')
    b.append(t(255, 262, "Markenaufbau, ungefähr die Hälfte", "s", "middle", f' style="fill:{INK}"'))
    b.append(t(586, 262, "Aktivierung, ungefähr die Hälfte", "s", "middle", f' style="fill:{INK}"'))
    b.append(t(20, 296, "Orientierung aus untersuchten B2B-Kampagnen (Binet und Field), keine feste Regel. Kaufzyklus, Bekanntheit,", "s"))
    b.append(t(20, 313, "Ziel und Messhorizont bestimmen die konkrete Aufteilung.", "s"))
    svg("marke-aktivierung", 770, 326, "Markenaufbau und Aktivierung",
        "Zwei Kästen. Markenaufbau: wirkt langfristig, spricht eine breite Zielgruppe an, sorgt dafür, dass wir in Erwägung gezogen werden. Aktivierung: wirkt kurzfristig, spricht kaufbereite Kontakte an, löst Handlungen wie Anfragen oder Anmeldungen aus. Darunter ein Budgetbalken, ungefähr hälftig geteilt. Hinweis: Orientierung aus untersuchten B2B-Kampagnen nach Binet und Field, keine feste Regel.",
        "\n".join(b))


# ---------------------------------------------------------------- GA4-Events
def ga4_events():
    b = []
    b.append(t(20, 30, "Events", "h")); b.append(t(20, 48, "jede erfasste Handlung", "sub"))
    ev = ["page_view", "scroll", "click", "file_download", "generate_lead", "purchase"]
    for i, e in enumerate(ev):
        y = 64 + i * 40; key = e in ("generate_lead", "purchase")
        b.append(rect(20, y, 180, 30, OCH_T if key else NEUT, OCH if key else LINE, 1.5 if key else 1, 15))
        b.append(t(36, y + 20, e, "mono"))
    b.append(t(250, 30, "Parameter", "h")); b.append(t(250, 48, "liefern den Kontext", "sub"))
    b.append(rect(250, 264, 250, 72, PAPER, INK, 1.25, 8))
    b.append(t(264, 286, "purchase", "mono")); b.append(t(264, 306, "Bestellwert: 89 €", "d")); b.append(t(264, 326, "Artikel: Mahlwerk", "d"))
    b.append(rect(250, 184, 250, 72, PAPER, INK, 1.25, 8))
    b.append(t(264, 206, "generate_lead", "mono")); b.append(t(264, 226, "Formular: Kontakt", "d")); b.append(t(264, 246, "Seite: /beratung", "d"))
    b.append(arrow(203, 239, 246, 222)); b.append(arrow(203, 279, 246, 296))
    b.append(t(250, 90, "Ein Event nennt die Art", "d")); b.append(t(250, 108, "der Handlung, Parameter", "d")); b.append(t(250, 126, "beschreiben sie genauer.", "d"))
    b.append(t(550, 30, "Schlüsselereignisse", "h")); b.append(t(550, 48, "bewusst markierte Zielhandlungen", "sub"))
    b.append(rect(550, 184, 200, 152, OCH_T, INK, 1.5, 8))
    b.append(t(566, 210, "Anfrage", "n")); b.append(t(566, 230, "aus generate_lead", "s"))
    b.append(t(566, 268, "Kauf", "n")); b.append(t(566, 288, "aus purchase", "s"))
    b.append(t(566, 322, "Steuerungsgrößen", "s", "start", f' style="font-weight:600;fill:{OCH}"'))
    b.append(arrow(503, 260, 546, 260, OCH, "ao"))
    svg("ga4-events", 770, 350, "Vom Event zum Schlüsselereignis in GA4",
        "Links sechs Events: page_view, scroll, click, file_download, generate_lead, purchase; die letzten beiden sind hervorgehoben. In der Mitte Beispiele für Parameter: generate_lead mit Formular Kontakt und Seite /beratung, purchase mit Bestellwert 89 Euro und Artikel Mahlwerk. Rechts die Schlüsselereignisse Anfrage und Kauf als Steuerungsgrößen. Fiktive Werte.",
        "\n".join(b))


# --------------------------------------------------------------- Prompting
def prompt_bausteine():
    b = []
    parts = [("Rolle", "Verhalte dich als erfahrene SEO-Beraterin.", C_BLUE),
             ("Aufgabe", "Bewerte den folgenden Seitentitel und schlage", C_OCH),
             (None, "drei Alternativen mit höchstens 60 Zeichen vor.", C_OCH),
             ("Kontext", "<kontext> Fachhandel für Siebträger, Zielgruppe:", "#6b7a52"),
             (None, "Einsteiger mit kleinem Budget </kontext>", "#6b7a52"),
             ("Beispiel", "Orientiere dich an diesem Stil:", TER),
             (None, "„Siebträger für Einsteiger: ehrlich verglichen“", TER)]
    b.append(rect(20, 16, 730, 260, PAPER, INK, 1.25, 10))
    b.append(t(40, 44, "Prompt", "s", "start", ' style="font-weight:600"'))
    y = 78
    for lab, line, col in parts:
        if lab:
            y += 8
            b.append(t(40, y, lab, "n", "start", f' style="fill:{col}"'))
        b.append(f'  <rect x="160" y="{y-15}" width="4" height="22" fill="{col}"/>')
        b.append(t(176, y, line, "mono", "start", ' style="font-size:14px"'))
        y += 26
    b.append(t(20, 304, "Vier Bausteine: klare Aufgabe, Rolle, abgegrenzter Kontext, Beispiel im Zielstil. Beispiel fiktiv.", "s"))
    svg("prompt-bausteine", 770, 316, "Vier Bausteine eines Prompts",
        "Ein Beispielprompt, dessen Zeilen links nach Baustein markiert sind. Rolle: Verhalte dich als erfahrene SEO-Beraterin. Aufgabe: Bewerte den folgenden Seitentitel und schlage drei Alternativen mit höchstens 60 Zeichen vor. Kontext in Kontext-Tags: Fachhandel für Siebträger, Zielgruppe Einsteiger mit kleinem Budget. Beispiel: Orientiere dich an diesem Stil, gefolgt von einem Mustertitel.",
        "\n".join(b))


# ------------------------------------------------------------------ COMPASS
def compass():
    comps = [("C", "Context", "Kontext", 0), ("O", "Objective", "Ziel", 0), ("M", "Mode", "Rolle/Modus", 1),
             ("P", "People of Interest", "Zielgruppe", 1), ("A", "Attitude", "Tonfall", 2), ("S", "Style", "Stil", 2),
             ("S", "Specifications", "Spezifikationen", 3)]
    groups = [("Fundament", "worum es geht", OCH_T), ("Perspektive", "wer spricht, für wen", SLA_T),
              ("Klang", "wie es klingt", NEUT), ("Rahmen", "Regeln, Grenzen", TER_T)]
    b = []
    w = 100; gap = 5; x0 = 20
    xs = [x0 + i * (w + gap) for i in range(7)]
    spans = {0: (0, 1), 1: (2, 3), 2: (4, 5), 3: (6, 6)}
    for g, (a, e) in spans.items():
        gx1, gx2 = xs[a], xs[e] + w
        b.append(f'  <path d="M{gx1},34 L{gx1},28 L{gx2},28 L{gx2},34" fill="none" stroke="{SOFT}" stroke-width="1.2"/>')
        b.append(t((gx1 + gx2) / 2, 20, groups[g][0], "s", "middle", ' style="font-weight:600"'))
    for i, (L, en, de, g) in enumerate(comps):
        x = xs[i]
        b.append(rect(x, 44, w, 150, groups[g][2], INK, 1.25, 8))
        b.append(t(x + w / 2, 104, L, "big", "middle", ' style="font-size:44px"'))
        enl = en.split(" ") if len(en) > 12 else [en]
        if len(enl) > 1:
            enl = [" ".join(enl[:1]), " ".join(enl[1:])]
        b.append(lines(x + w / 2, 140, enl, "n", "middle", 17) if en != "Specifications" else t(x + w / 2, 140, en, "n", "middle", ' style="font-size:13px"'))
        b.append(t(x + w / 2, 140 + 17 * len(enl) + 4, de, "s", "middle"))
    for g, (a, e) in spans.items():
        b.append(t((xs[a] + xs[e] + w) / 2, 216, groups[g][1], "s", "middle"))
    b.append(t(20, 250, "Bei kurzen Fragen genügen oft Kontext und Ziel. Je sichtbarer das Ergebnis, desto vollständiger die Liste.", "d"))
    svg("compass", 760, 262, "Die sieben Komponenten von COMPASS",
        "Sieben Kacheln mit den Buchstaben C O M P A S S: Context (Kontext), Objective (Ziel), Mode (Rolle oder Modus), People of Interest (Zielgruppe), Attitude (Tonfall), Style (Stil), Specifications (Spezifikationen). Gruppiert in Fundament (Context, Objective), Perspektive (Mode, People of Interest), Klang (Attitude, Style) und Rahmen (Specifications). Hinweis: Bei kurzen Fragen genügen oft Kontext und Ziel.",
        "\n".join(b))


# ---------------------------------------------------------- Chat bis Agent
def chat_agent():
    b = []
    cols = [("Chat", "einzelne Prompts in einem KI-Fenster", ["Anzeige in fünf", "Varianten texten"], 0),
            ("Assistent", "Anweisungen direkt im Programm", ["In Word einen", "Berichtsentwurf erstellen"], 1),
            ("Agent", "Ziel vorgeben, Teilschritte laufen selbst", ["Meeting vorbereiten", "lassen"], 2)]
    for x, (n, d, ex, i) in zip([20, 270, 520], cols):
        top = 150 - i * 50
        b.append(rect(x, top, 230, 314 - top, [NEUT, SLA_T, OCH_T][i], INK, 1.25, 8))
        b.append(t(x + 16, top + 28, n, "h"))
        dl = d.split(", ") if ", " in d else [d]
        words = d.split(" "); half = (len(words) + 1) // 2
        b.append(lines(x + 16, top + 50, [" ".join(words[:half]), " ".join(words[half:])], "s", "start", 16))
        b.append(t(x + 16, 262, "Beispiel", "s", "start", ' style="font-weight:600"'))
        b.append(lines(x + 16, 280, ex, "d", "start", 18))
    # Agentenschleife
    loop = ["Teilschritte planen", "mit Werkzeugen ausführen", "Entwurf zur Freigabe"]
    for j, s in enumerate(loop):
        yy = 150 + j * 28
        b.append(rect(536, yy - 16, 198, 24, PAPER, OCH, 1.2, 12))
        b.append(t(548, yy, s, "s", "start", f' style="fill:{INK}"'))
    b.append(arrow(20, 344, 750, 344, SOFT, "ar", 1.2))
    b.append(t(20, 364, "mehr Autonomie", "s", "start", ' style="font-weight:600"'))
    b.append(t(750, 364, "mehr Aufsicht: prüfen, Rechte begrenzen, Verantwortung bleibt bei uns", "s", "end", f' style="font-weight:600;fill:{TER}"'))
    svg("chat-assistent-agent", 770, 376, "Chat, Assistent, Agent",
        "Drei ansteigende Stufen. Chat: einzelne Prompts in einem KI-Fenster, Beispiel Anzeige in fünf Varianten texten. Assistent: Anweisungen direkt im Programm, Beispiel in Word einen Berichtsentwurf erstellen. Agent: Ziel vorgeben, Teilschritte laufen selbst, mit den Schritten Teilschritte planen, mit Werkzeugen ausführen, Entwurf zur Freigabe; Beispiel Meeting vorbereiten lassen. Ein Pfeil darunter: mehr Autonomie verlangt mehr Aufsicht, die Verantwortung bleibt bei uns.",
        "\n".join(b))


# -------------------------------------------------------- Einwilligung Tracking
def einwilligung():
    b = []
    b.append(rect(235, 14, 300, 50, NEUT, INK, 1.25, 8))
    b.append(t(385, 36, "Informationen auf dem Endgerät", "n", "middle")); b.append(t(385, 55, "speichern oder auslesen", "s", "middle"))
    b.append(arrow(385, 66, 385, 88))
    b.append(f'  <path d="M385,92 L535,130 L385,168 L235,130 Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.25"/>')
    b.append(t(385, 126, "unbedingt erforderlich für den", "s", "middle", f' style="fill:{INK}"'))
    b.append(t(385, 142, "ausdrücklich gewünschten Dienst?", "s", "middle", f' style="fill:{INK}"'))
    b.append(f'  <path d="M235,130 L130,130 L130,196" fill="none" stroke="{LINE}" stroke-width="1.5" marker-end="url(#ar)"/>')
    b.append(t(182, 122, "ja", "s", "middle", ' style="font-weight:600"'))
    b.append(f'  <path d="M535,130 L640,130 L640,196" fill="none" stroke="{LINE}" stroke-width="1.5" marker-end="url(#ar)"/>')
    b.append(t(588, 122, "nein", "s", "middle", ' style="font-weight:600"'))
    b.append(rect(20, 200, 220, 80, SLA_T, INK, 1.25, 8))
    b.append(t(36, 226, "ohne Einwilligung zulässig", "n", "start", ' style="font-size:14px"'))
    b.append(t(36, 248, "z. B. Warenkorb im Shop", "d")); b.append(t(36, 268, "§ 25 TDDDG", "s"))
    b.append(rect(460, 200, 290, 80, TER_T, INK, 1.25, 8))
    b.append(t(476, 226, "Einwilligung nötig", "n", "start", ' style="font-size:14px"'))
    b.append(t(476, 248, "z. B. Reichweitenmessung,", "d")); b.append(t(476, 268, "Werbe-Cookies", "d"))
    b.append(arrow(605, 282, 605, 304))
    b.append(rect(460, 308, 290, 148, PAPER, INK, 1.25, 8))
    b.append(t(476, 332, "Wirksam einwilligen lassen", "n", "start", ' style="font-size:14px"'))
    req = [("aktive Handlung, kein vorangekreuztes", "Kästchen (EuGH, Planet49)", None),
           ("Ablehnen so einfach wie Zustimmen,", "Widerruf so leicht wie Zustimmung", "(EDSA, DSK)")]
    yy = 354
    for a1, a2, a3 in req:
        b.append(f'  <circle cx="{481}" cy="{yy-4}" r="2.5" fill="{TER}"/>')
        b.append(t(490, yy, a1, "s", "start", f' style="fill:{DESC}"')); b.append(t(490, yy + 16, a2, "s", "start", f' style="fill:{DESC}"'))
        if a3:
            b.append(t(490, yy + 32, a3, "s", "start", f' style="fill:{DESC}"'))
        yy += 40
    b.append(rect(20, 308, 420, 148, "#f3f0e8", RULE, 1, 8))
    b.append(t(36, 332, "Consent-Management-Lösung", "n", "start", ' style="font-size:14px"'))
    b.append(lines(36, 354, ["protokolliert die Entscheidungen", "und steuert, welche Werkzeuge", "überhaupt laden"], "d", "start", 19))
    b.append(arrow(456, 374, 444, 374, LINE, "ar", 1.5))
    b.append(t(20, 482, "Vereinfachte Übersicht nach dem Kapiteltext; die DSGVO gilt daneben weiter.", "s"))
    svg("einwilligung-tracking", 770, 494, "Einwilligung beim Tracking",
        "Entscheidungsweg: Werden Informationen auf dem Endgerät gespeichert oder ausgelesen, fragt sich, ob das für den ausdrücklich gewünschten Dienst unbedingt erforderlich ist. Ja: ohne Einwilligung zulässig, zum Beispiel der Warenkorb im Shop, Paragraf 25 TDDDG. Nein: Einwilligung nötig, zum Beispiel Reichweitenmessung und Werbe-Cookies. Wirksam wird sie durch eine aktive Handlung ohne vorangekreuztes Kästchen (EuGH, Planet49); Ablehnen muss so einfach sein wie Zustimmen und der Widerruf so leicht wie die Zustimmung (EDSA, DSK). Eine Consent-Management-Lösung protokolliert die Entscheidungen und steuert, welche Werkzeuge laden. Vereinfachte Übersicht; die DSGVO gilt daneben weiter.",
        "\n".join(b))


ALL = [kundenreise, planungsprozess, werbemarkt, empathy, bmc, stp, kennzahlenbaum, anzeigenrang, kampagne, kostenbezug, attribution,
       marketing_mix, positionierung, core_web_vitals, suchintention, quality_score, marke_aktivierung, ga4_events,
       prompt_bausteine, compass, chat_agent, einwilligung]

if __name__ == "__main__":
    for f in ALL:
        f()
