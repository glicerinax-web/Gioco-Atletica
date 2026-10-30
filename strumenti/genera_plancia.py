#!/usr/bin/env python3
"""Genera la plancia di gioco di "Atletica Strampalata" in formato SVG.

Uso:  python3 genera_plancia.py  [file_di_uscita.svg]
Senza argomenti scrive ../plancia.svg (accanto al regolamento).
"""
import math
import os
import sys

W, H = 1800, 1420

# --- Anello: 8 corsie x 40 caselle (1 casella = 10 m) ---
X1, X2 = 460, 1340          # estremi dei rettilinei
CY = 470                    # centro verticale dell'anello
R0 = 230                    # raggio interno della corsia 1
LW = 24                     # larghezza corsia
LANES = 8
STEP = (X2 - X1) / 10       # lunghezza di una casella sul rettilineo

STARS_RING = {3, 17, 24, 31}
HURDLES_400 = {5, 8, 12, 15, 19, 22, 26, 29, 33, 36}

# --- Rettilineo di velocità: 8 corsie x 22 caselle (1 casella = 5 m) ---
SX, SY = 150, 985
SCW, SLH = 70, 24
STARS_SPRINT = {6, 15}
HURDLES_110 = {3, 5, 7, 9, 11, 12, 14, 16, 18, 20}

TRACK_A = "#c8553d"
TRACK_B = "#b4472f"
GRASS = "#4f9d4a"
GRASS_DARK = "#3f8a3b"
WHITE = "#ffffff"
INK = "#1f2a33"
GOLD = "#ffd23f"
FONT = "DejaVu Sans, Arial, Helvetica, sans-serif"

out = []


def add(s):
    out.append(s)


def text(x, y, s, size=14, fill=INK, weight="normal", anchor="middle", rotate=None, extra=""):
    rot = f' transform="rotate({rotate:.1f} {x:.1f} {y:.1f})"' if rotate is not None else ""
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
        f'text-anchor="{anchor}" dominant-baseline="middle"{rot}{extra}>{s}</text>')


def poly(points, fill, stroke=WHITE, sw=1.2):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    add(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def arc_points(cx, cy, r, a1, a2, n=8):
    return [(cx + r * math.cos(math.radians(a1 + (a2 - a1) * t / n)),
             cy + r * math.sin(math.radians(a1 + (a2 - a1) * t / n))) for t in range(n + 1)]


def ring_cell(k, lane):
    """Poligono e centro della casella k (1..40) nella corsia lane (0..7)."""
    ri, ro = R0 + lane * LW, R0 + (lane + 1) * LW
    rm = (ri + ro) / 2
    if 1 <= k <= 10:        # curva destra, dal basso verso l'alto
        a1, a2 = 90 - (k - 1) * 18, 90 - k * 18
        pts = arc_points(X2, CY, ri, a1, a2) + arc_points(X2, CY, ro, a2, a1)
        am = math.radians((a1 + a2) / 2)
        c = (X2 + rm * math.cos(am), CY + rm * math.sin(am))
        ang = (a1 + a2) / 2 + 90
    elif 11 <= k <= 20:     # rettilineo opposto, da destra a sinistra
        xa, xb = X2 - (k - 11) * STEP, X2 - (k - 10) * STEP
        pts = [(xa, CY - ri), (xb, CY - ri), (xb, CY - ro), (xa, CY - ro)]
        c = ((xa + xb) / 2, CY - rm)
        ang = 0
    elif 21 <= k <= 30:     # curva sinistra, dall'alto verso il basso
        a1, a2 = 270 - (k - 21) * 18, 270 - (k - 20) * 18
        pts = arc_points(X1, CY, ri, a1, a2) + arc_points(X1, CY, ro, a2, a1)
        am = math.radians((a1 + a2) / 2)
        c = (X1 + rm * math.cos(am), CY + rm * math.sin(am))
        ang = (a1 + a2) / 2 - 90
    else:                   # rettilineo d'arrivo, da sinistra a destra
        xa, xb = X1 + (k - 31) * STEP, X1 + (k - 30) * STEP
        pts = [(xa, CY + ri), (xb, CY + ri), (xb, CY + ro), (xa, CY + ro)]
        c = ((xa + xb) / 2, CY + rm)
        ang = 0
    return pts, c, ang


def ring_point(k_boundary, r):
    """Punto sul confine tra la casella k e k+1 (k=0 è la linea d'arrivo)."""
    k = k_boundary % 40
    if 0 <= k <= 10:
        a = math.radians(90 - k * 18)
        return X2 + r * math.cos(a), CY + r * math.sin(a)
    if 10 < k <= 20:
        return X2 - (k - 10) * STEP, CY - r
    if 20 < k <= 30:
        a = math.radians(270 - (k - 20) * 18)
        return X1 + r * math.cos(a), CY + r * math.sin(a)
    return X1 + (k - 30) * STEP, CY + r


def star(cx, cy, r, fill=GOLD, stroke=INK):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = math.radians(-90 + i * 36)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    poly(pts, fill, stroke, 0.8)


def hurdle(cx, cy, s=1.0, rotate=0):
    add(f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({rotate:.1f}) scale({s})">'
        f'<rect x="-8" y="-4" width="16" height="5" fill="{WHITE}" stroke="{INK}" stroke-width="0.8"/>'
        f'<rect x="-8" y="-4" width="5" height="5" fill="#222"/>'
        f'<rect x="3" y="-4" width="5" height="5" fill="#222"/>'
        f'<line x1="-7" y1="1" x2="-7" y2="6" stroke="{INK}" stroke-width="1.4"/>'
        f'<line x1="7" y1="1" x2="7" y2="6" stroke="{INK}" stroke-width="1.4"/></g>')


def checker_line(p_in, p_out, squares=8):
    """Linea a scacchi (traguardo) tra due punti."""
    (x0, y0), (x1, y1) = p_in, p_out
    dx, dy = (x1 - x0) / squares, (y1 - y0) / squares
    nx, ny = -dy, dx
    ln = math.hypot(nx, ny) or 1
    nx, ny = nx / ln * 5, ny / ln * 5
    for i in range(squares * 2):
        t0, t1 = i / 2, (i + 1) / 2
        ax, ay = x0 + dx * t0, y0 + dy * t0
        bx, by = x0 + dx * t1, y0 + dy * t1
        for side, col in ((0, "#111" if i % 2 else WHITE), (1, WHITE if i % 2 else "#111")):
            o = -1 if side == 0 else 1
            poly([(ax, ay), (bx, by), (bx + nx * o, by + ny * o), (ax + nx * o, ay + ny * o)], col, col, 0.2)


def box(x, y, w, h, title, lines, color):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#fffaf0" stroke="{color}" stroke-width="3"/>')
    add(f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="12" fill="{color}"/>')
    add(f'<rect x="{x}" y="{y + 18}" width="{w}" height="12" fill="{color}"/>')
    text(x + w / 2, y + 16, title, 16, WHITE, "bold")
    for i, ln in enumerate(lines):
        text(x + 12, y + 48 + i * 19, ln, 13, INK, anchor="start")


# ============================== DISEGNO ==============================
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">')
add(f'<rect width="{W}" height="{H}" fill="#2f6f3a"/>')
add(f'<rect x="10" y="10" width="{W - 20}" height="{H - 20}" rx="24" fill="none" stroke="{GOLD}" stroke-width="4"/>')

# Erba del campo interno (a strisce)
add(f'<clipPath id="campo"><path d="M{X1},{CY - R0} L{X2},{CY - R0} A{R0},{R0} 0 0 1 {X2},{CY + R0} '
    f'L{X1},{CY + R0} A{R0},{R0} 0 0 1 {X1},{CY - R0} Z"/></clipPath>')
add('<g clip-path="url(#campo)">')
for i in range(0, 1400, 60):
    add(f'<rect x="{i}" y="0" width="30" height="{H}" fill="{GRASS if (i // 60) % 2 == 0 else GRASS_DARK}"/>')
    add(f'<rect x="{i + 30}" y="0" width="30" height="{H}" fill="{GRASS_DARK if (i // 60) % 2 == 0 else GRASS}"/>')
add('</g>')

# ---------- Anello ----------
for lane in range(LANES):
    for k in range(1, 41):
        pts, c, ang = ring_cell(k, lane)
        poly(pts, TRACK_A if (k + lane) % 2 else TRACK_B)
for lane in range(LANES):
    for k in range(1, 41):
        pts, (cx, cy), ang = ring_cell(k, lane)
        if k in STARS_RING:
            star(cx, cy, 8)
        elif k in HURDLES_400:
            hurdle(cx, cy, 0.85, ang)

# Numeri delle caselle (sul bordo interno, nell'erba)
for k in range(1, 41):
    _, _, ang = ring_cell(k, 0)
    if 1 <= k <= 10:
        a = math.radians(90 - (k - 0.5) * 18)
        x, y = X2 + (R0 - 13) * math.cos(a), CY + (R0 - 13) * math.sin(a)
    elif k <= 20:
        x, y = X2 - (k - 10.5) * STEP, CY - R0 + 13
    elif k <= 30:
        a = math.radians(270 - (k - 20.5) * 18)
        x, y = X1 + (R0 - 13) * math.cos(a), CY + (R0 - 13) * math.sin(a)
    else:
        x, y = X1 + (k - 30.5) * STEP, CY + R0 - 13
    add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="{WHITE}" opacity="0.9"/>')
    text(x, y + 1, str(k), 11, INK, "bold")

# Numeri di corsia sulla linea di partenza/arrivo
for lane in range(LANES):
    x, y = X2 - 16, CY + R0 + lane * LW + LW / 2
    add(f'<rect x="{x - 9}" y="{y - 9}" width="18" height="18" rx="3" fill="{WHITE}"/>')
    text(x, y + 1, str(lane + 1), 12, INK, "bold")

# Linea d'arrivo (casella 0/40) e partenza dei 200 (casella 20)
checker_line(ring_point(0, R0), ring_point(0, R0 + LANES * LW))
p_in, p_out = ring_point(20, R0), ring_point(20, R0 + LANES * LW)
add(f'<line x1="{p_in[0]:.1f}" y1="{p_in[1]:.1f}" x2="{p_out[0]:.1f}" y2="{p_out[1]:.1f}" stroke="{WHITE}" stroke-width="5"/>')
# Linea di rientro dell'800 (fine casella 10)
p_in, p_out = ring_point(10, R0), ring_point(10, R0 + LANES * LW)
add(f'<line x1="{p_in[0]:.1f}" y1="{p_in[1]:.1f}" x2="{p_out[0]:.1f}" y2="{p_out[1]:.1f}" stroke="#2bb3ff" '
    f'stroke-width="5" stroke-dasharray="10 6"/>')

# Etichette dell'anello
text(X2 + 10, CY + R0 + LANES * LW + 16, "PARTENZA 400 · 400 hs · 800  /  ARRIVO DI TUTTE LE CORSE", 14, WHITE, "bold", "end")
text(X1 - 4, CY - R0 - LANES * LW - 16, "PARTENZA 200 m (scatta da qui: 20 caselle)", 14, WHITE, "bold", "start")
text(X2 + 6, CY - R0 - LANES * LW - 16, "LINEA DI RIENTRO 800 m (corsie 1-2)", 14, "#9fe0ff", "bold", "end")
text(X1 - 300, CY + R0 + LANES * LW + 16, "ANELLO: 1 casella = 10 m · 1 giro = 40 caselle", 14, GOLD, "bold", "start")

# ---------- Campo interno ----------
text(900, 300, "ATLETICA STRAMPALATA", 46, WHITE, "bold", extra=' stroke="#1f2a33" stroke-width="1.5"')
text(900, 342, "il gioco da tavolo dell'atletica leggera (con bucce di banana)", 17, "#fff4c2", "bold")

# Giavellotto: pedana di rincorsa e settore verso sinistra
gx, gy = 600, 470
add(f'<rect x="{gx}" y="{gy - 10}" width="150" height="20" fill="#d9b48f" stroke="{WHITE}" stroke-width="1.5"/>')
add(f'<path d="M{gx},{gy - 14} A20,20 0 0 0 {gx},{gy + 14}" fill="none" stroke="{WHITE}" stroke-width="4"/>')
half = math.radians(14.5)
for dist, r in ((40, 110), (60, 180), (80, 250), (96, 300)):
    x0, y0 = gx - r * math.cos(half), gy - r * math.sin(half)
    x1, y1 = gx - r * math.cos(half), gy + r * math.sin(half)
    add(f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 0 {x1:.1f},{y1:.1f}" fill="none" stroke="{WHITE}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    text(x0 - 2, y0 - 9, f"{dist} m", 11, WHITE, "bold")
for s in (-1, 1):
    add(f'<line x1="{gx}" y1="{gy}" x2="{gx - 310 * math.cos(half):.1f}" y2="{gy + s * 310 * math.sin(half):.1f}" stroke="{WHITE}" stroke-width="2"/>')
text(gx + 75, gy - 26, "GIAVELLOTTO", 15, WHITE, "bold")
text(gx + 75, gy + 30, "Forza x 8 m x Angolo", 12, "#fff4c2", "bold")

# Getto del peso: pedana circolare e settore verso destra
px, py = 1210, 470
add(f'<circle cx="{px}" cy="{py}" r="22" fill="#9aa3ab" stroke="{WHITE}" stroke-width="3"/>')
add(f'<path d="M{px + 18},{py - 12} A22,22 0 0 1 {px + 18},{py + 12}" fill="none" stroke="{WHITE}" stroke-width="5"/>')
half = math.radians(17.5)
for dist, r in ((14, 70), (18, 130), (22, 190), (24, 225)):
    x0, y0 = px + r * math.cos(half), py - r * math.sin(half)
    x1, y1 = px + r * math.cos(half), py + r * math.sin(half)
    add(f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}" fill="none" stroke="{WHITE}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    text(x0 + 2, y0 - 9, f"{dist} m", 11, WHITE, "bold")
for s in (-1, 1):
    add(f'<line x1="{px}" y1="{py}" x2="{px + 235 * math.cos(half):.1f}" y2="{py + s * 235 * math.sin(half):.1f}" stroke="{WHITE}" stroke-width="2"/>')
text(px, py - 42, "GETTO DEL PESO", 15, WHITE, "bold")
text(px, py + 44, "12 m + somma x 0,5 m", 12, "#fff4c2", "bold")
text(px, py + 60, "un 1 = NULLO!", 12, GOLD, "bold")

# Salto in alto: materasso, ritti, asticella e scala delle altezze
add(f'<rect x="830" y="395" width="140" height="60" rx="8" fill="#2f6fd1" stroke="{WHITE}" stroke-width="2"/>')
add(f'<line x1="826" y1="392" x2="974" y2="392" stroke="{GOLD}" stroke-width="4"/>')
add(f'<rect x="822" y="380" width="6" height="22" fill="{WHITE}"/><rect x="972" y="380" width="6" height="22" fill="{WHITE}"/>')
text(900, 425, "SALTO IN ALTO", 14, WHITE, "bold")
heights = [("1,80", "6"), ("1,90", "7"), ("2,00", "8"), ("2,10", "9"), ("2,20", "10"),
           ("2,30", "11"), ("2,40", "12"), ("2,45", "12*")]
add('<rect x="770" y="470" width="260" height="52" rx="6" fill="#fffaf0" opacity="0.95"/>')
for i, (h, t) in enumerate(heights):
    x = 786 + i * 32.5
    text(x, 484, h, 10, INK, "bold")
    text(x, 506, t, 13, "#2f6fd1", "bold")
text(900, 532, "altezza (m) / tiro minimo con 2 dadi su 3 · * senza Concentrazione", 10, WHITE)

# Salto in lungo: rincorsa di 12 caselle, asse di battuta, buca di sabbia
lx, ly, lc = 600, 610, 34
for i in range(12):
    add(f'<rect x="{lx + i * lc}" y="{ly - 14}" width="{lc}" height="28" fill="{TRACK_A if i % 2 else TRACK_B}" stroke="{WHITE}" stroke-width="1"/>')
    text(lx + i * lc + lc / 2, ly + 1, str(i + 1), 12, WHITE, "bold")
ax = lx + 12 * lc
add(f'<rect x="{ax}" y="{ly - 14}" width="9" height="28" fill="{WHITE}" stroke="{INK}" stroke-width="1"/>')
add(f'<rect x="{ax + 9}" y="{ly - 14}" width="12" height="28" fill="#8a8a8a"/>')
add(f'<rect x="{ax + 21}" y="{ly - 26}" width="210" height="52" rx="10" fill="#f2d48a" stroke="#c9a85a" stroke-width="2"/>')
text(ax + 126, ly - 2, "SABBIA", 14, "#8a6a2a", "bold")
text(ax + 126, ly + 14, "4 m + (rincorsa+volo) x 0,25 m", 11, "#6b4f1d", "bold")
text(lx + 9 * lc, ly - 28, "SALTO IN LUNGO · supera la casella 12 = NULLO (faccia nella plastilina)", 13, WHITE, "bold")

# ---------- Rettilineo di velocità (100 m e 110 hs) ----------
add(f'<rect x="{SX - 70}" y="{SY - 50}" width="{22 * SCW + 110}" height="{LANES * SLH + 78}" rx="14" fill="#245a2e" stroke="{GOLD}" stroke-width="2"/>')
text(SX + 11 * SCW, SY - 32, "RETTILINEO DI VELOCITÀ · 100 m e 110 m ostacoli · 1 casella = 5 m", 18, WHITE, "bold")
for lane in range(LANES):
    y = SY + lane * SLH
    for k in range(1, 23):
        x = SX + (k - 1) * SCW
        add(f'<rect x="{x}" y="{y}" width="{SCW}" height="{SLH}" fill="{TRACK_A if (k + lane) % 2 else TRACK_B}" stroke="{WHITE}" stroke-width="1.2"/>')
        if k in STARS_SPRINT:
            star(x + SCW / 2, y + SLH / 2, 8)
        elif k in HURDLES_110:
            hurdle(x + SCW / 2, y + SLH / 2, 0.85)
    add(f'<rect x="{SX - 36}" y="{y + 3}" width="18" height="18" rx="3" fill="{WHITE}"/>')
    text(SX - 27, y + SLH / 2 + 1, str(lane + 1), 12, INK, "bold")
for k in range(1, 23):
    text(SX + (k - 0.5) * SCW, SY - 12, str(k), 12, WHITE, "bold")
# blocchi 110 hs (prima della casella 1), blocchi 100 m (casella 2), arrivo (dopo la 22)
add(f'<line x1="{SX}" y1="{SY}" x2="{SX}" y2="{SY + LANES * SLH}" stroke="{WHITE}" stroke-width="5"/>')
add(f'<line x1="{SX + 2 * SCW}" y1="{SY}" x2="{SX + 2 * SCW}" y2="{SY + LANES * SLH}" stroke="{GOLD}" stroke-width="5"/>')
checker_line((SX + 22 * SCW, SY), (SX + 22 * SCW, SY + LANES * SLH))
text(SX, SY + LANES * SLH + 16, "▲ blocchi 110 hs", 13, WHITE, "bold", "start")
text(SX + 2 * SCW + 4, SY + LANES * SLH + 16, "▲ blocchi 100 m (pedina sulla casella 2)", 13, GOLD, "bold", "start")
text(SX + 22 * SCW, SY + LANES * SLH + 16, "ARRIVO ▲", 13, WHITE, "bold", "end")

# ---------- Legenda e promemoria ----------
by = 1240
box(30, by, 420, 165, "RITMO (tiri sempre 3 dadi)", [
    "PASSO: tieni 1 dado · +1 Fiato · peschi 1 carta",
    "CORSA: tieni 2 dadi a scelta · gratis",
    "SCATTO: tieni tutti e 3 i dadi · -2 Fiato",
    "Ultime 10 caselle di 400/400hs: Scatto -3",
    "Fiato iniziale: 100/110hs 2 · 200 3",
    "400/400hs 4 · 800 4",
], "#c8553d")
box(465, by, 430, 165, "COMBINAZIONI", [
    "Doppio tra i dadi tenuti: FALCATA PERFETTA, +1 carta",
    "Tris sul tiro: IN TRANCE, muovi la somma di 3 gratis",
    "Tris di 1: CRAMPO COMICO, fermo ma +2 Fiato",
    "Scala 4-5-6: VENTO IN POPPA, +1 Fiato",
    "Scala 1-2-3: INCIAMPO, -1 Fiato",
    "Doppio 6 nei concorsi: pesca 1 carta Stadio",
], "#2f6fd1")
box(910, by, 420, 165, "CASELLE SPECIALI", [
    "★  STADIO: fermati qui e pesca una carta Stadio",
    "Ostacolo (solo gare hs): se ti fermi sopra tira 1 dado",
    "    4-6 pulito · 2-3 toccato -1 · 1 CAPITOMBOLO -3",
    "Banana: chi la raggiunge si ferma, cade, poi Passo",
    "Pozzanghera: chi si ferma sopra perde 2 Fiato",
    "800: dopo il rientro solo corsie 1-2",
], "#e08a00")
box(1345, by, 425, 165, "PUNTI PER PIAZZAMENTO", [
    "1° 10 · 2° 8 · 3° 6 · 4° 5",
    "5° 4 · 6° 3 · 7° 2 · 8° 1",
    "Nullo o squalifica: 0 punti",
    "Record dello Stadio battuto: +2 punti",
    "Arrivo nello stesso round: vince chi",
    "supera di più il traguardo (fotofinish)",
], "#6a3fb5")

add('</svg>')

dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plancia.svg")
with open(dest, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("Plancia scritta in", os.path.abspath(dest))
