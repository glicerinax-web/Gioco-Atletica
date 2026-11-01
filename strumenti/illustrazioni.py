"""Illustrazioni cartoon delle carte di "Atletica Strampalata".

Ogni illustrazione è un SVG vettoriale (viewBox 240 x 100) composto con un piccolo
kit di elementi: sfondi, l'atleta (con pose ed espressioni) e gli oggetti di scena.
illustrazione(codice) restituisce l'SVG della carta con quel codice (F1, D3, S5, A2...).
"""
import math

W, H = 240, 100
TERRA = 84                  # linea del terreno
OUT = "#2b2b2b"             # contorno
PELLI = ["#f6c9a0", "#d9a074", "#a8693f", "#ffd9b8", "#7a4a2a", "#e8b48a"]
CANOTTE = ["#e63946", "#2f6fd1", "#2a9d8f", "#ffb703", "#6a3fb5", "#ff70a6", "#f4a261", "#1f2a33"]


# ============================================================ utilità
def g(contenuto, x=0, y=0, s=1.0, r=0, flip=False):
    sx = -s if flip else s
    return f'<g transform="translate({x:.1f} {y:.1f}) rotate({r}) scale({sx} {s})">{contenuto}</g>'


def linea(p1, p2, colore, w):
    return (f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" '
            f'stroke="{colore}" stroke-width="{w}" stroke-linecap="round"/>')


def arto(punti, colore, w=5.5):
    """Arto con contorno: spezzata spessa scura sotto, colore sopra."""
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in punti)
    return (f'<polyline points="{pts}" fill="none" stroke="{OUT}" stroke-width="{w + 2.4}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<polyline points="{pts}" fill="none" stroke="{colore}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def testo(x, y, t, size=11, colore=OUT, peso="bold", r=0, contorno=None, anchor="middle"):
    st = f' stroke="{contorno}" stroke-width="3" paint-order="stroke"' if contorno else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{peso}" fill="{colore}" text-anchor="{anchor}"'
            f' font-family="DejaVu Sans, Arial, sans-serif" transform="rotate({r} {x} {y})"{st}>{t}</text>')


def stella(cx, cy, r, colore="#ffd23f", rot=0):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = math.radians(-90 + rot + i * 36)
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{colore}" stroke="{OUT}" stroke-width="1.2" stroke-linejoin="round"/>'


def stelline(cx, cy, n=3, r=14):
    return "".join(stella(cx + r * math.cos(a), cy + r * 0.5 * math.sin(a), 3.5, rot=i * 20)
                   for i, a in enumerate(math.radians(-90 + k * 360 / n) for k in range(n)))


def linee_moto(x, y, n=3, lung=22, passo=7, colore="#ffffff", verso=-1):
    return "".join(linea((x, y + i * passo), (x + verso * (lung - i * 4), y + i * passo), colore, 2.2) for i in range(n))


def nuvoletta(x, y, w, h, t, size=9, coda=(0, 1)):
    """Fumetto con coda verso il basso-sinistra (coda=(dx, dy) direzione)."""
    cx, cy = x + w / 2, y + h
    tx, ty = cx - 6 + coda[0] * 10, cy + 8 * coda[1]
    return (f'<path d="M{cx - 7},{cy - 1} L{tx},{ty} L{cx + 3},{cy - 1} Z" fill="#fff" stroke="{OUT}" stroke-width="1.5"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="#fff" stroke="{OUT}" stroke-width="1.5"/>'
            f'<rect x="{cx - 6}" y="{cy - 3}" width="9" height="3" fill="#fff"/>'
            + testo(cx, y + h / 2 + size * 0.36, t, size))


# ============================================================ sfondi
def sfondo(tipo="pista", cielo="#bfe6ff"):
    s = f'<rect width="{W}" height="{H}" fill="{cielo}"/>'
    if tipo in ("pista", "stadio"):
        if tipo == "stadio":
            s += spalti(0, 18, W, 40)
        s += f'<rect y="{TERRA - 14}" width="{W}" height="{H}" fill="#d0583f"/>'
        for y in (TERRA - 4, TERRA + 7):
            s += linea((0, y), (W, y), "#f3d9cf", 1.4)
    elif tipo == "campo":
        s += f'<rect y="{TERRA - 10}" width="{W}" height="{H}" fill="#6dbb5a"/>'
        for x in range(0, W, 30):
            s += f'<rect x="{x}" y="{TERRA - 10}" width="15" height="{H}" fill="#62ad50"/>'
    elif tipo == "notte":
        s = f'<rect width="{W}" height="{H}" fill="#1d2a4d"/>'
        for i, (x, y) in enumerate([(20, 14), (60, 30), (95, 10), (150, 22), (210, 12), (230, 40), (125, 40)]):
            s += f'<circle cx="{x}" cy="{y}" r="{1.2 + (i % 2)}" fill="#fff"/>'
        s += f'<rect y="{TERRA - 14}" width="{W}" height="{H}" fill="#6b3a2e"/>'
        s += linea((0, TERRA - 4), (W, TERRA - 4), "#8e5a4c", 1.4)
    return s


def spalti(x, y, w, h, braccia=False, onda=None):
    """Tribuna piena di tifosi (teste colorate in file)."""
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#8aa0b3"/>'
    righe = int(h // 11)
    for r in range(righe):
        yy = y + 7 + r * 11
        s += f'<rect x="{x}" y="{yy + 4}" width="{w}" height="3" fill="#6f8496"/>'
        for i, xx in enumerate(range(int(x) + 5 + (r % 2) * 5, int(x + w) - 3, 10)):
            col = CANOTTE[(i * 3 + r) % len(CANOTTE)]
            pelle = PELLI[(i + r) % len(PELLI)]
            alza = braccia or (onda is not None and abs(xx - onda) < 28)
            dy = -3 if alza else 0
            if alza:
                s += linea((xx - 2.5, yy + dy), (xx - 5, yy - 7 + dy), pelle, 1.6) + linea((xx + 2.5, yy + dy), (xx + 5, yy - 7 + dy), pelle, 1.6)
            s += f'<rect x="{xx - 3.5}" y="{yy + dy}" width="7" height="6" rx="2" fill="{col}"/>'
            s += f'<circle cx="{xx}" cy="{yy - 2.5 + dy}" r="3" fill="{pelle}"/>'
    return s


def sole(cx, cy, r=12, faccia="felice", occhiali=False):
    raggi = "".join(linea((cx + (r + 3) * math.cos(a), cy + (r + 3) * math.sin(a)),
                          (cx + (r + 9) * math.cos(a), cy + (r + 9) * math.sin(a)), "#ffb703", 2.6)
                    for a in (math.radians(k * 30) for k in range(12)))
    s = raggi + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffd23f" stroke="{OUT}" stroke-width="1.6"/>'
    if occhiali:
        s += (f'<rect x="{cx - 9}" y="{cy - 5}" width="8" height="5" rx="2" fill="{OUT}"/>'
              f'<rect x="{cx + 1}" y="{cy - 5}" width="8" height="5" rx="2" fill="{OUT}"/>'
              + linea((cx - 1, cy - 3), (cx + 1, cy - 3), OUT, 1.2))
    else:
        s += f'<circle cx="{cx - 4}" cy="{cy - 3}" r="1.5" fill="{OUT}"/><circle cx="{cx + 4}" cy="{cy - 3}" r="1.5" fill="{OUT}"/>'
    if faccia == "sudato":
        s += (f'<path d="M{cx - 4},{cy + 5} Q{cx},{cy + 2} {cx + 4},{cy + 5}" fill="none" stroke="{OUT}" stroke-width="1.5"/>'
              f'<path d="M{cx + 10},{cy - 2} q2,4 0,6 q-2,-2 0,-6z" fill="#7fc4ff" stroke="{OUT}" stroke-width=".8"/>')
    else:
        s += f'<path d="M{cx - 5},{cy + 3} Q{cx},{cy + 8} {cx + 5},{cy + 3}" fill="none" stroke="{OUT}" stroke-width="1.5"/>'
    return s


def nuvola(cx, cy, s=1.0, colore="#ffffff"):
    return g(f'<path d="M-18,8 C-26,8 -26,-4 -16,-4 C-15,-14 0,-16 3,-7 C8,-13 20,-10 18,0 C26,0 26,8 18,8 Z" '
             f'fill="{colore}" stroke="{OUT}" stroke-width="1.5"/>', cx, cy, s)


# ============================================================ l'atleta
POSE = {
    # collo, braccio davanti (gomito, mano), braccio dietro, gamba davanti (ginocchio, piede), gamba dietro
    "corsa": ((5, -17), [(12, -11), (17, -18)], [(-5, -7), (-11, -2)], [(10, 7), (6, 18)], [(-5, 9), (-15, 12)]),
    "fermo": ((0, -18), [(6, -7), (7, 1)], [(-6, -7), (-7, 1)], [(3, 10), (4, 20)], [(-3, 10), (-4, 20)]),
    "braccia_su": ((0, -18), [(8, -24), (12, -32)], [(-8, -24), (-12, -32)], [(4, 10), (5, 20)], [(-4, 10), (-5, 20)]),
    "salta": ((3, -17), [(11, -22), (16, -29)], [(-6, -22), (-9, -30)], [(10, 3), (4, 11)], [(4, 8), (-6, 10)]),
    "saluta": ((0, -18), [(9, -21), (13, -30)], [(-6, -7), (-7, 1)], [(3, 10), (4, 20)], [(-3, 10), (-4, 20)]),
    "tuffo": ((14, -6), [(22, -8), (30, -10)], [(20, -3), (28, -2)], [(-9, 2), (-18, 1)], [(-9, -2), (-19, -5)]),
    "scivola": ((-12, -12), [(-4, -22), (2, -28)], [(-20, -18), (-24, -26)], [(10, -8), (18, -14)], [(8, -2), (17, -4)]),
    "seduto": ((-2, -17), [(6, -8), (12, -4)], [(-7, -8), (-10, -1)], [(9, -2), (18, 2)], [(8, 1), (16, 4)]),
    "cade_avanti": ((15, -9), [(22, -4), (26, 2)], [(13, -2), (16, 4)], [(3, 8), (-2, 15)], [(-6, 5), (-13, 2)]),
    "tira": ((4, -17), [(13, -12), (19, -16)], [(-6, -7), (-12, -4)], [(-4, 9), (-5, 18)], [(-8, 9), (-12, 15)]),
    "pugno": ((1, -18), [(9, -24), (11, -33)], [(-6, -8), (-6, -1)], [(5, 10), (8, 20)], [(-4, 10), (-7, 20)]),
    "saltella": ((0, -18), [(7, -23), (8, -31)], [(-7, -23), (-8, -31)], [(5, 8), (4, 14)], [(-5, 8), (-4, 14)]),
    "zoppo": ((2, -18), [(9, -10), (12, -4)], [(-8, -14), (-14, -12)], [(2, 10), (2, 20)], [(-6, 6), (-2, 2)]),
    "lancia": ((-3, -17), [(-12, -22), (-20, -28)], [(8, -9), (14, -6)], [(8, 9), (12, 19)], [(-5, 10), (-11, 19)]),
    "spinge": ((10, -15), [(17, -14), (24, -16)], [(16, -10), (23, -11)], [(4, 9), (2, 19)], [(-7, 7), (-15, 15)]),
    "dorme": ((0, -18), [(4, -8), (5, 0)], [(-4, -8), (-5, 0)], [(2, 10), (3, 20)], [(-2, 10), (-3, 20)]),
}


def viso(hx, hy, espressione, verso=1):
    d = 3.5 * verso
    e, s = espressione, ""
    occhio = lambda x, y, r=1.6: f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{OUT}"/>'
    if e in ("felice", "determinato", "furbo"):
        if e == "furbo":
            s += linea((hx + d - 5.5, hy - 3), (hx + d - 1.5, hy - 2), OUT, 1.6) + linea((hx + d + 1.5, hy - 2), (hx + d + 5.5, hy - 3), OUT, 1.6)
        else:
            s += occhio(hx + d - 3.5, hy - 2.5) + occhio(hx + d + 3.5, hy - 2.5)
        if e == "determinato":
            s += linea((hx + d - 6, hy - 7), (hx + d - 1.5, hy - 5.5), OUT, 1.5) + linea((hx + d + 1.5, hy - 5.5), (hx + d + 6, hy - 7), OUT, 1.5)
            s += f'<path d="M{hx + d - 4},{hy + 3} L{hx + d + 4},{hy + 3} Q{hx + d},{hy + 8} {hx + d - 4},{hy + 3} Z" fill="#fff" stroke="{OUT}" stroke-width="1.2"/>'
        elif e == "furbo":
            s += f'<path d="M{hx + d - 4},{hy + 4} Q{hx + d + 1},{hy + 6} {hx + d + 5},{hy + 2}" fill="none" stroke="{OUT}" stroke-width="1.5" stroke-linecap="round"/>'
        else:
            s += f'<path d="M{hx + d - 4},{hy + 2.5} Q{hx + d},{hy + 7.5} {hx + d + 4},{hy + 2.5}" fill="#c0392b" stroke="{OUT}" stroke-width="1.3"/>'
    elif e == "sorpreso":
        for ox in (-3.5, 3.5):
            s += f'<circle cx="{hx + d + ox}" cy="{hy - 2.5}" r="2.8" fill="#fff" stroke="{OUT}" stroke-width="1"/>' + occhio(hx + d + ox + verso * .8, hy - 2.5, 1.2)
        s += f'<ellipse cx="{hx + d}" cy="{hy + 4.5}" rx="2.4" ry="3" fill="#7a1f1f" stroke="{OUT}" stroke-width="1"/>'
    elif e == "stanco":
        s += linea((hx + d - 5.5, hy - 2), (hx + d - 1.5, hy - 2), OUT, 1.6) + linea((hx + d + 1.5, hy - 2), (hx + d + 5.5, hy - 2), OUT, 1.6)
        s += f'<path d="M{hx + d - 4},{hy + 4} q2,-2 4,0 q2,2 4,0" fill="none" stroke="{OUT}" stroke-width="1.4"/>'
        s += f'<path d="M{hx - 9 * verso},{hy - 6} q2,4 0,6 q-2,-2 0,-6z" fill="#7fc4ff" stroke="{OUT}" stroke-width=".8"/>'
    elif e == "arrabbiato":
        s += occhio(hx + d - 3.5, hy - 2) + occhio(hx + d + 3.5, hy - 2)
        s += linea((hx + d - 6, hy - 7), (hx + d - 1.5, hy - 4.5), OUT, 1.6) + linea((hx + d + 1.5, hy - 4.5), (hx + d + 6, hy - 7), OUT, 1.6)
        s += f'<path d="M{hx + d - 4},{hy + 5} Q{hx + d},{hy + 2} {hx + d + 4},{hy + 5}" fill="none" stroke="{OUT}" stroke-width="1.5"/>'
    elif e == "dorme":
        for ox in (-3.5, 3.5):
            s += f'<path d="M{hx + d + ox - 2},{hy - 2.5} Q{hx + d + ox},{hy - .5} {hx + d + ox + 2},{hy - 2.5}" fill="none" stroke="{OUT}" stroke-width="1.4"/>'
        s += f'<ellipse cx="{hx + d}" cy="{hy + 4}" rx="1.6" ry="1.2" fill="{OUT}"/>'
    elif e == "dolore":
        s += f'<path d="M{hx + d - 6},{hy - 4} l3,1.5 l-3,1.5" fill="none" stroke="{OUT}" stroke-width="1.4"/>'
        s += f'<path d="M{hx + d + 6},{hy - 4} l-3,1.5 l3,1.5" fill="none" stroke="{OUT}" stroke-width="1.4"/>'
        s += f'<path d="M{hx + d - 4},{hy + 5} Q{hx + d},{hy + 1} {hx + d + 4},{hy + 5} Z" fill="#7a1f1f" stroke="{OUT}" stroke-width="1.2"/>'
    elif e == "occhiolino":
        s += occhio(hx + d - 3.5, hy - 2.5)
        s += f'<path d="M{hx + d + 1.5},{hy - 2} Q{hx + d + 3.5},{hy - 4} {hx + d + 5.5},{hy - 2}" fill="none" stroke="{OUT}" stroke-width="1.5"/>'
        s += f'<path d="M{hx + d - 4},{hy + 2.5} Q{hx + d},{hy + 7.5} {hx + d + 4},{hy + 2.5}" fill="#c0392b" stroke="{OUT}" stroke-width="1.3"/>'
    return s


def capelli(hx, hy, stile, colore, verso=1):
    r = 10.5
    if stile == "corti":
        return f'<path d="M{hx - r},{hy - 1} A{r},{r} 0 0 1 {hx + r},{hy - 1} Q{hx + 3 * verso},{hy - 7} {hx - r},{hy - 1} Z" fill="{colore}" stroke="{OUT}" stroke-width="1.4"/>'
    if stile == "coda":
        cx = hx - 11 * verso
        return (f'<path d="M{cx},{hy - 6} q{-9 * verso},2 {-11 * verso},12 q{6 * verso},-3 {9 * verso},-6 Z" fill="{colore}" stroke="{OUT}" stroke-width="1.3"/>'
                + capelli(hx, hy, "corti", colore, verso))
    if stile == "chignon":
        return (f'<circle cx="{hx - 4 * verso}" cy="{hy - 12}" r="5" fill="{colore}" stroke="{OUT}" stroke-width="1.3"/>'
                + capelli(hx, hy, "corti", colore, verso))
    if stile == "ricci":
        return "".join(f'<circle cx="{hx + 10 * math.cos(a):.1f}" cy="{hy - 3 + 8 * math.sin(a):.1f}" r="4" fill="{colore}" stroke="{OUT}" stroke-width="1.1"/>'
                       for a in (math.radians(-180 + k * 30) for k in range(7)))
    if stile == "punte":
        return f'<path d="M{hx - r},{hy - 2} L{hx - 8},{hy - 14} L{hx - 3},{hy - 8} L{hx},{hy - 16} L{hx + 3},{hy - 8} L{hx + 8},{hy - 14} L{hx + r},{hy - 2} Z" fill="{colore}" stroke="{OUT}" stroke-width="1.3" stroke-linejoin="round"/>'
    return ""


def atleta(x, y, pose="corsa", espr="felice", canotta=0, pelle=0, capello="corti", col_capelli="#3b2a20",
           s=1.0, flip=False, r=0, numero=None, extra=""):
    """Atleta cartoon. (x, y) = anca; in piedi i piedi sono a y + 20*s."""
    collo, ba, bd, ga, gd = POSE[pose]
    pel = PELLI[pelle % len(PELLI)] if isinstance(pelle, int) else pelle
    can = CANOTTE[canotta % len(CANOTTE)] if isinstance(canotta, int) else canotta
    spalla = (collo[0] * 0.85, collo[1] * 0.85)
    testa = (collo[0] * 1.12 + (collo[0] - 0) * 0.0, collo[1] - 11)
    if pose in ("tuffo", "scivola", "cade_avanti"):
        dx, dy = collo[0], collo[1]
        n = math.hypot(dx, dy)
        testa = (collo[0] + dx / n * 10.5, collo[1] + dy / n * 10.5)
    scarpa = lambda p: f'<ellipse cx="{p[0] + 2:.1f}" cy="{p[1] + 1:.1f}" rx="4.6" ry="2.6" fill="#ffffff" stroke="{OUT}" stroke-width="1.3"/>'
    c = ""
    c += arto([(0, 0)] + gd, pel) + scarpa(gd[1])
    c += arto([spalla] + bd, pel)
    c += arto([(0, 0), collo], can, 11)
    c += f'<ellipse cx="0" cy="1.5" rx="7" ry="4.5" fill="{OUT}"/>'
    if numero:
        mx, my = collo[0] * 0.45, collo[1] * 0.45
        c += f'<rect x="{mx - 3.6:.1f}" y="{my - 3:.1f}" width="7.2" height="6" rx="1" fill="#fff" stroke="{OUT}" stroke-width=".7"/>'
        c += testo(mx, my + 2.3, str(numero), 5.5)
    c += f'<circle cx="{testa[0]:.1f}" cy="{testa[1]:.1f}" r="10.5" fill="{pel}" stroke="{OUT}" stroke-width="1.6"/>'
    c += capelli(testa[0], testa[1], capello, col_capelli)
    c += viso(testa[0], testa[1], espr)
    c += arto([(0, 0)] + ga, pel) + scarpa(ga[1])
    c += arto([spalla] + ba, pel)
    c += extra.replace("TX", f"{testa[0]:.1f}").replace("TY", f"{testa[1]:.1f}")
    return g(c, x, y, s, r, flip)


def in_piedi(x, pose="fermo", s=1.0, **kw):
    return atleta(x, TERRA - 2 - 20 * s, pose, s=s, **kw)


# accessori da passare in extra= (TX, TY = centro della testa)
OCCHIALI = ('<circle cx="TX" cy="TY" r="0" fill="none"/>'
            '<g transform="translate(TX TY)"><circle cx="0" cy="-2.5" r="3.2" fill="none" stroke="#2b2b2b" stroke-width="1.2"/>'
            '<circle cx="7" cy="-2.5" r="3.2" fill="none" stroke="#2b2b2b" stroke-width="1.2"/>'
            '<line x1="3.2" y1="-2.5" x2="3.8" y2="-2.5" stroke="#2b2b2b" stroke-width="1.2"/></g>')
OCCHIALI_SOLE = ('<g transform="translate(TX TY)"><rect x="-3" y="-5.5" width="6.5" height="4.5" rx="1.5" fill="#111"/>'
                 '<rect x="4.5" y="-5.5" width="6.5" height="4.5" rx="1.5" fill="#111"/>'
                 '<line x1="-10" y1="-4" x2="11" y2="-4" stroke="#111" stroke-width="1.2"/></g>')
BAFFI = '<g transform="translate(TX TY)"><path d="M-1,1.5 q4,-3 4.5,0 q.5,-3 4.5,0 q-2,3 -4.5,1 q-2.5,2 -4.5,-1z" fill="#5a3b2a"/></g>'
FASCIA = '<g transform="translate(TX TY)"><rect x="-10.6" y="-8" width="21.2" height="3.6" fill="#e63946" stroke="#2b2b2b" stroke-width=".8"/></g>'
CAPPELLINO = ('<g transform="translate(TX TY)"><path d="M-10,-4 A10,9 0 0 1 10,-4 Z" fill="#2f6fd1" stroke="#2b2b2b" stroke-width="1.2"/>'
              '<path d="M8,-5 L18,-4 L8,-2 Z" fill="#2f6fd1" stroke="#2b2b2b" stroke-width="1.2"/></g>')
CONIGLIO = ('<g transform="translate(TX TY)"><ellipse cx="-4" cy="-18" rx="3" ry="8" fill="#fff" stroke="#2b2b2b" stroke-width="1"/>'
            '<ellipse cx="5" cy="-18" rx="3" ry="8" fill="#fff" stroke="#2b2b2b" stroke-width="1"/>'
            '<ellipse cx="-4" cy="-18" rx="1.3" ry="5" fill="#ffb3c6"/><ellipse cx="5" cy="-18" rx="1.3" ry="5" fill="#ffb3c6"/></g>')


# ============================================================ oggetti di scena
def banana(x, y, s=1.0, r=0):
    return g('<path d="M-12,-6 C-9,8 9,9 14,-2 C8,3 -3,3 -8,-8 Z" fill="#ffe14d" stroke="#2b2b2b" stroke-width="1.5" stroke-linejoin="round"/>'
             '<path d="M-12,-6 L-14,-9" stroke="#5b3d00" stroke-width="2.4" stroke-linecap="round"/>'
             '<path d="M-6,2 q-6,5 -12,3 M4,3 q4,6 10,6" fill="none" stroke="#2b2b2b" stroke-width="1.3"/>'
             '<path d="M-6,2 q-6,5 -12,3 L-9,1 Z M4,3 q4,6 10,6 L10,4 Z" fill="#ffe14d"/>', x, y, s, r)


def molla(x, y, h=14):
    pts = [(x, y)]
    for i in range(1, 7):
        pts.append((x + (5 if i % 2 else -5), y + i * h / 7))
    pts.append((x, y + h))
    return arto(pts, "#b8c2cc", 2)


def carota_bottiglia(x, y, s=1.0, r=0):
    return g('<path d="M-6,-14 L6,-14 L2,16 Q0,19 -2,16 Z" fill="#ff8c1a" stroke="#2b2b2b" stroke-width="1.5" stroke-linejoin="round"/>'
             '<path d="M-3,-6 h4 M-2,2 h3 M-1,9 h2" stroke="#c45e00" stroke-width="1.2"/>'
             '<path d="M-2,-14 q-6,-8 -2,-12 q2,6 2,12 q1,-8 6,-10 q0,6 -4,10 Z" fill="#3fae49" stroke="#2b2b2b" stroke-width="1.1"/>'
             '<rect x="-1.2" y="-24" width="2.4" height="8" fill="#fff" stroke="#2b2b2b" stroke-width=".8"/>', x, y, s, r)


def panino(x, y, s=1.0, r=0):
    return g('<path d="M-22,0 Q0,-18 22,0 Z" fill="#e8a85c" stroke="#2b2b2b" stroke-width="1.5"/>'
             '<rect x="-23" y="0" width="46" height="4" rx="2" fill="#ffb3c6" stroke="#2b2b2b" stroke-width="1"/>'
             '<rect x="-22" y="4" width="44" height="4" rx="2" fill="#f78fa7" stroke="#2b2b2b" stroke-width="1"/>'
             '<path d="M-23,8 q4,3 8,0 q4,3 8,0 q4,3 8,0 q4,3 8,0 q4,3 8,0 q3,3 6,0" fill="#7ccd5a" stroke="#2b2b2b" stroke-width="1"/>'
             '<path d="M-22,10 L22,10 Q22,17 0,17 Q-22,17 -22,10 Z" fill="#e8a85c" stroke="#2b2b2b" stroke-width="1.5"/>'
             '<circle cx="-8" cy="-6" r="1" fill="#fff8e0"/><circle cx="3" cy="-8" r="1" fill="#fff8e0"/><circle cx="11" cy="-4" r="1" fill="#fff8e0"/>',
             x, y, s, r)


def ventilatore(x, y, s=1.0):
    pale = "".join(g('<ellipse cx="0" cy="-9" rx="5" ry="9" fill="#9fd4ff" stroke="#2b2b2b" stroke-width="1.2"/>', 0, 0, 1, a) for a in (0, 120, 240))
    return g(f'<rect x="-3" y="10" width="6" height="22" fill="#8a949c" stroke="#2b2b2b" stroke-width="1.2"/>'
             f'<rect x="-11" y="30" width="22" height="5" rx="2" fill="#8a949c" stroke="#2b2b2b" stroke-width="1.2"/>'
             f'<circle cx="0" cy="0" r="19" fill="#eef6fb" stroke="#2b2b2b" stroke-width="1.5"/>{pale}'
             f'<circle cx="0" cy="0" r="3.5" fill="#2b2b2b"/>', x, y, s)


def vento(x, y, s=1.0, colore="#ffffff"):
    return g(f'<path d="M0,0 h30 a6,6 0 1 0 -6,-6 M4,10 h38 a7,7 0 1 1 -7,7 M0,20 h22" fill="none" stroke="{colore}" '
             f'stroke-width="3" stroke-linecap="round"/>', x, y, s)


def calzino(x, y, s=1.0, r=0, puzza=False):
    c = ('<path d="M-6,-16 L6,-16 L6,4 Q6,12 14,12 Q20,12 20,17 Q20,22 12,22 L0,22 Q-6,22 -6,14 Z" fill="#fff" stroke="#2b2b2b" stroke-width="1.5"/>'
         '<rect x="-6" y="-16" width="12" height="4" fill="#e63946"/><rect x="-6" y="-9" width="12" height="3" fill="#2f6fd1"/>'
         '<path d="M-6,-16 L6,-16 L6,4 Q6,12 14,12 Q20,12 20,17 Q20,22 12,22 L0,22 Q-6,22 -6,14 Z" fill="none" stroke="#2b2b2b" stroke-width="1.5"/>')
    if puzza:
        c += ('<path d="M-12,-18 q-4,-6 0,-10 q4,-4 0,-10 M0,-22 q-4,-6 0,-10 q4,-4 0,-10 M12,-18 q-4,-6 0,-10 q4,-4 0,-10" '
              'fill="none" stroke="#7cb342" stroke-width="2" stroke-linecap="round"/>')
    return g(c, x, y, s, r)


def dado(x, y, s=1.0, r=0, valore=6):
    punti = {1: [(0, 0)], 2: [(-4, -4), (4, 4)], 3: [(-4, -4), (0, 0), (4, 4)], 4: [(-4, -4), (4, -4), (-4, 4), (4, 4)],
             5: [(-4, -4), (4, -4), (0, 0), (-4, 4), (4, 4)], 6: [(-4, -4), (4, -4), (-4, 0), (4, 0), (-4, 4), (4, 4)]}[valore]
    c = '<rect x="-9" y="-9" width="18" height="18" rx="4" fill="#fff" stroke="#2b2b2b" stroke-width="1.5"/>'
    c += "".join(f'<circle cx="{px}" cy="{py}" r="1.8" fill="#2b2b2b"/>' for px, py in punti)
    return g(c, x, y, s, r)


def traguardo(x, y0=TERRA - 14, y1=H):
    c = ""
    for i, y in enumerate(range(int(y0), int(y1), 4)):
        c += f'<rect x="{x}" y="{y}" width="4" height="4" fill="{"#111" if i % 2 else "#fff"}"/>'
        c += f'<rect x="{x + 4}" y="{y}" width="4" height="4" fill="{"#fff" if i % 2 else "#111"}"/>'
    return c


def flash(x, y, r=14):
    pts = []
    for i in range(16):
        rr = r if i % 2 == 0 else r * 0.45
        a = math.radians(i * 22.5)
        pts.append(f"{x + rr * math.cos(a):.1f},{y + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="#fff59d" stroke="#ffb703" stroke-width="1.2"/>'


def note(x, y):
    return (g('<ellipse cx="0" cy="0" rx="4" ry="3" fill="#2b2b2b" transform="rotate(-20)"/><line x1="3.6" y1="-1" x2="3.6" y2="-14" stroke="#2b2b2b" stroke-width="1.6"/>'
              '<path d="M3.6,-14 q6,2 5,8" fill="none" stroke="#2b2b2b" stroke-width="1.6"/>', x, y)
            + g('<ellipse cx="0" cy="0" rx="4" ry="3" fill="#2b2b2b" transform="rotate(-20)"/><ellipse cx="11" cy="-3" rx="4" ry="3" fill="#2b2b2b" transform="rotate(-20 11 -3)"/>'
                '<path d="M3.6,-1 L3.6,-15 L14.6,-18 L14.6,-4" fill="none" stroke="#2b2b2b" stroke-width="1.6"/>', x + 22, y - 10))


def stereo(x, y, s=1.0):
    return g('<rect x="-20" y="-12" width="40" height="22" rx="4" fill="#ffb703" stroke="#2b2b2b" stroke-width="1.5"/>'
             '<circle cx="-10" cy="0" r="7" fill="#2b2b2b"/><circle cx="10" cy="0" r="7" fill="#2b2b2b"/>'
             '<circle cx="-10" cy="0" r="3" fill="#8a949c"/><circle cx="10" cy="0" r="3" fill="#8a949c"/>'
             '<path d="M-14,-12 Q0,-24 14,-12" fill="none" stroke="#2b2b2b" stroke-width="2"/>', x, y, s)


def mantello(colore="#e63946"):
    return f'<path d="M3,-15 Q-20,-14 -34,-4 Q-24,0 -30,8 Q-14,2 -2,-8 Z" fill="{colore}" stroke="#2b2b2b" stroke-width="1.5" stroke-linejoin="round"/>'


def gelato(x, y, s=1.0, r=0, gusto="#9ccc65"):
    return g(f'<path d="M-5,0 L5,0 L0,14 Z" fill="#d9a066" stroke="#2b2b2b" stroke-width="1.2"/>'
             f'<circle cx="0" cy="-4" r="6" fill="{gusto}" stroke="#2b2b2b" stroke-width="1.2"/>'
             f'<circle cx="2" cy="-11" r="4.5" fill="#ff9eb5" stroke="#2b2b2b" stroke-width="1.2"/>', x, y, s, r)


def ape(x, y, s=1.0):
    return g('<ellipse cx="-3" cy="-7" rx="5" ry="7" fill="#e3f4ff" stroke="#2b2b2b" stroke-width="1" opacity=".9" transform="rotate(-25 -3 -7)"/>'
             '<ellipse cx="4" cy="-7" rx="5" ry="7" fill="#e3f4ff" stroke="#2b2b2b" stroke-width="1" opacity=".9" transform="rotate(25 4 -7)"/>'
             '<ellipse cx="0" cy="0" rx="10" ry="7" fill="#ffd23f" stroke="#2b2b2b" stroke-width="1.4"/>'
             '<path d="M-3,-6.5 v13 M3,-6.5 v13" stroke="#2b2b2b" stroke-width="2.6"/>'
             '<circle cx="7" cy="-1.5" r="1.4" fill="#2b2b2b"/><path d="M-10,0 l-4,0" stroke="#2b2b2b" stroke-width="1.5"/>', x, y, s)


def megafono(x, y, s=1.0, r=0):
    return g('<path d="M0,-4 L18,-12 L18,12 L0,4 Z" fill="#e63946" stroke="#2b2b2b" stroke-width="1.5" stroke-linejoin="round"/>'
             '<rect x="-6" y="-4" width="7" height="8" rx="1.5" fill="#fff" stroke="#2b2b2b" stroke-width="1.3"/>'
             '<ellipse cx="18" cy="0" rx="3" ry="12" fill="#c62f3b" stroke="#2b2b2b" stroke-width="1.3"/>', x, y, s, r)


def piccione(x, y, s=1.0, flip=False):
    return g('<path d="M-14,2 Q-4,-10 10,-4 L16,-6 L13,-1 Q8,10 -6,8 L-18,10 Z" fill="#9aa5b1" stroke="#2b2b2b" stroke-width="1.4" stroke-linejoin="round"/>'
             '<path d="M-4,-2 Q-12,-22 -22,-18 Q-14,-12 -12,2 Z" fill="#7f8b97" stroke="#2b2b2b" stroke-width="1.3"/>'
             '<path d="M2,-2 Q4,-26 18,-24 Q10,-14 8,-1 Z" fill="#b6c0ca" stroke="#2b2b2b" stroke-width="1.3"/>'
             '<circle cx="11" cy="-5" r="1.4" fill="#2b2b2b"/><path d="M15,-5 l6,1.5 l-6,1.5 z" fill="#ffb703" stroke="#2b2b2b" stroke-width=".8"/>'
             '<path d="M5,-2 q2,4 6,3" fill="none" stroke="#5aa86b" stroke-width="2"/>', x, y, s, 0, flip)


def carta_volante(x, y, s=1.0, r=0, colore="#c8553d"):
    return g(f'<rect x="-7" y="-10" width="14" height="20" rx="2" fill="#fffaf0" stroke="#2b2b2b" stroke-width="1.2"/>'
             f'<rect x="-7" y="-10" width="14" height="6" rx="2" fill="{colore}" stroke="#2b2b2b" stroke-width="1.2"/>', x, y, s, r)


def pozzanghera(x, y, w=50):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{w / 2}" ry="{w / 9}" fill="#5fb0ef" stroke="#2b2b2b" stroke-width="1.4"/>'
            f'<ellipse cx="{x - w / 8}" cy="{y - 1}" rx="{w / 8}" ry="1.5" fill="#bfe3ff"/>')


def schizzi(x, y):
    return "".join(f'<path d="M{x + dx},{y} q{dx / 3},-{10 + abs(dx) / 3} {dx / 1.5},-{14 + abs(dx) / 4}" fill="none" '
                   f'stroke="#5fb0ef" stroke-width="2.4" stroke-linecap="round"/>'
                   f'<circle cx="{x + dx * 1.5:.1f}" cy="{y - 20 - abs(dx) / 3:.1f}" r="2.2" fill="#5fb0ef"/>' for dx in (-16, -6, 6, 16))


def secchiello(x, y, s=1.0):
    return g('<path d="M-8,-8 L8,-8 L6,8 L-6,8 Z" fill="#ff70a6" stroke="#2b2b2b" stroke-width="1.4"/>'
             '<path d="M-8,-8 Q0,-20 8,-8" fill="none" stroke="#2b2b2b" stroke-width="1.4"/>'
             '<ellipse cx="0" cy="-8" rx="8" ry="2" fill="#5fb0ef" stroke="#2b2b2b" stroke-width="1"/>', x, y, s)


def telefono(x, y, s=1.0, r=0):
    return g('<rect x="-6" y="-11" width="12" height="22" rx="2.5" fill="#2b2b2b"/>'
             '<rect x="-4.5" y="-8.5" width="9" height="16" rx="1" fill="#9fd4ff"/>'
             '<circle cx="0" cy="9" r=".9" fill="#888"/>', x, y, s, r)


def borraccia(x, y, s=1.0, r=0, colore="#2f6fd1"):
    return g(f'<rect x="-3" y="-17" width="6" height="5" rx="1" fill="#fff" stroke="#2b2b2b" stroke-width="1.2"/>'
             f'<rect x="-8" y="-13" width="16" height="27" rx="5" fill="{colore}" stroke="#2b2b2b" stroke-width="1.5"/>'
             f'<rect x="-8" y="-3" width="16" height="7" fill="#fff" opacity=".7"/>', x, y, s, r)


def frecce_scambio(x, y):
    return (f'<path d="M{x - 16},{y - 4} Q{x},{y - 18} {x + 16},{y - 4}" fill="none" stroke="#e63946" stroke-width="2.6"/>'
            f'<path d="M{x + 16},{y - 4} l-7,-1 l4,-6 z" fill="#e63946"/>'
            f'<path d="M{x + 16},{y + 6} Q{x},{y + 20} {x - 16},{y + 6}" fill="none" stroke="#2f6fd1" stroke-width="2.6"/>'
            f'<path d="M{x - 16},{y + 6} l7,1 l-4,6 z" fill="#2f6fd1"/>')


def bassotto(x, y, s=1.0, flip=False):
    return g('<path d="M-26,4 Q-30,-2 -24,-6 L18,-6 Q24,-6 24,0 L24,4 Q24,8 18,8 L-20,8 Q-26,8 -26,4 Z" fill="#9c5a2c" stroke="#2b2b2b" stroke-width="1.5"/>'
             '<path d="M-22,8 v6 M-14,8 v6 M12,8 v6 M18,8 v6" stroke="#2b2b2b" stroke-width="3.4" stroke-linecap="round"/>'
             '<path d="M-26,-2 q-8,-6 -6,-12" fill="none" stroke="#2b2b2b" stroke-width="2.6" stroke-linecap="round"/>'
             '<path d="M16,-6 Q16,-18 28,-18 L36,-14 Q40,-10 34,-8 L24,-6 Z" fill="#9c5a2c" stroke="#2b2b2b" stroke-width="1.5"/>'
             '<path d="M22,-17 Q14,-16 16,-5 Q20,-8 22,-13 Z" fill="#6e3b18" stroke="#2b2b2b" stroke-width="1.2"/>'
             '<circle cx="29" cy="-14" r="1.5" fill="#2b2b2b"/><circle cx="37" cy="-12" r="2" fill="#2b2b2b"/>'
             '<path d="M33,-8 q2,5 -1,7" fill="#ff7b9c" stroke="#2b2b2b" stroke-width=".9"/>', x, y, s, 0, flip)


def cuore(x, y, s=1.0, colore="#e63946"):
    return g(f'<path d="M0,6 C-12,-2 -6,-12 0,-5 C6,-12 12,-2 0,6 Z" fill="{colore}" stroke="#2b2b2b" stroke-width="1"/>', x, y, s)


def trombetta(x, y, s=1.0, r=0):
    return g('<path d="M-30,-2 L6,-5 L22,-12 L22,12 L6,5 L-30,2 Z" fill="#ffd23f" stroke="#2b2b2b" stroke-width="1.5" stroke-linejoin="round"/>'
             '<ellipse cx="22" cy="0" rx="3.5" ry="12" fill="#ffb703" stroke="#2b2b2b" stroke-width="1.3"/>', x, y, s, r)


def onde_sonore(x, y, n=3, colore="#e63946"):
    return "".join(f'<path d="M{x + i * 8},{y - 8 - i * 4} Q{x + 6 + i * 8},{y} {x + i * 8},{y + 8 + i * 4}" fill="none" stroke="{colore}" '
                   f'stroke-width="2.4" stroke-linecap="round"/>' for i in range(n))


def fischietto(x, y, s=1.0, r=0):
    return g('<path d="M-14,-6 L4,-6 A9,9 0 1 1 -2,8 L-14,2 Z" fill="#c0c7cf" stroke="#2b2b2b" stroke-width="1.5" stroke-linejoin="round"/>'
             '<circle cx="5" cy="2" r="3.2" fill="#2b2b2b"/><rect x="-14" y="-6" width="5" height="8" fill="#9aa3ab" stroke="#2b2b2b" stroke-width="1"/>'
             '<path d="M12,-4 q8,-6 12,-14" fill="none" stroke="#e63946" stroke-width="1.6"/>', x, y, s, r)


def sasso(x, y, s=1.0):
    return g('<path d="M-6,3 Q-8,-3 -2,-5 Q5,-7 7,-1 Q8,5 1,5 Z" fill="#9e9e9e" stroke="#2b2b2b" stroke-width="1.3"/>'
             '<path d="M-2,-2 q2,-1 3,0" stroke="#e0e0e0" stroke-width="1"/>', x, y, s)


def lente(x, y, s=1.0, contenuto=""):
    return g(f'<line x1="11" y1="11" x2="24" y2="24" stroke="#5a3b2a" stroke-width="5" stroke-linecap="round"/>'
             f'<circle cx="0" cy="0" r="15" fill="#e3f4ff" stroke="#2b2b2b" stroke-width="2.4"/>{contenuto}'
             f'<path d="M-9,-6 a10,10 0 0 1 6,-6" fill="none" stroke="#fff" stroke-width="2"/>', x, y, s)


def falco(x, y, s=1.0):
    return g('<path d="M-22,22 Q-26,-4 -8,-14 Q8,-22 18,-10 Q24,-2 18,8 Q10,22 -22,22 Z" fill="#8d6e63" stroke="#2b2b2b" stroke-width="1.5"/>'
             '<path d="M-8,-14 Q8,-22 18,-10 Q8,-8 -2,-4 Z" fill="#fff" stroke="#2b2b2b" stroke-width="1.2"/>'
             '<path d="M16,-8 Q30,-8 30,2 Q26,-2 20,0 Z" fill="#ffb703" stroke="#2b2b2b" stroke-width="1.4"/>'
             '<circle cx="9" cy="-7" r="6" fill="#ffeb3b" stroke="#2b2b2b" stroke-width="1.3"/><circle cx="11" cy="-7" r="3" fill="#2b2b2b"/>'
             '<circle cx="12" cy="-8.2" r="1" fill="#fff"/><path d="M1,-14 L16,-11" stroke="#2b2b2b" stroke-width="2.4" stroke-linecap="round"/>', x, y, s)


def mano_furtiva(x, y, s=1.0, flip=False, oggetto=""):
    return g(f'<path d="M-40,0 L-8,-3 L-8,5 L-40,8 Z" fill="#2b2b2b"/>{oggetto}'
             f'<ellipse cx="-4" cy="1" rx="7" ry="6" fill="#f6c9a0" stroke="#2b2b2b" stroke-width="1.3"/>', x, y, s, 0, flip)


def specchio(x, y, s=1.0):
    return g('<ellipse cx="0" cy="0" rx="16" ry="24" fill="#d4af37" stroke="#2b2b2b" stroke-width="1.5"/>'
             '<ellipse cx="0" cy="0" rx="12" ry="20" fill="#cfe9ff" stroke="#2b2b2b" stroke-width="1.2"/>'
             '<path d="M-6,-12 l8,-4 M-7,-5 l12,-6" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>'
             '<rect x="-3" y="23" width="6" height="12" fill="#a0782b" stroke="#2b2b2b" stroke-width="1.3"/>'
             '<rect x="-12" y="33" width="24" height="4" rx="2" fill="#a0782b" stroke="#2b2b2b" stroke-width="1.3"/>', x, y, s)


def ombrello(x, y, s=1.0, colore="#e63946"):
    spicchi = "".join(f'<path d="M{-40 + i * 20},0 Q{-30 + i * 20},-6 {-20 + i * 20},0" fill="none" stroke="#2b2b2b" stroke-width="1.2"/>' for i in range(4))
    return g(f'<path d="M-40,0 A40,30 0 0 1 40,0 Z" fill="{colore}" stroke="#2b2b2b" stroke-width="1.5"/>'
             f'<path d="M-10,0 A12,30 0 0 1 10,0" fill="#fff" opacity=".35"/>{spicchi}'
             f'<line x1="0" y1="-30" x2="0" y2="-35" stroke="#2b2b2b" stroke-width="2"/>', x, y, s)


def pioggia(x0, x1, y0, y1, n=16, colore="#5fb0ef"):
    out = ""
    for i in range(n):
        x = x0 + (x1 - x0) * ((i * 37) % 100) / 100
        y = y0 + (y1 - y0) * ((i * 61) % 100) / 100
        out += linea((x, y), (x - 2, y + 6), colore, 1.8)
    return out


def macchina_foto(x, y, s=1.0):
    return g('<rect x="-16" y="-10" width="32" height="22" rx="3" fill="#2b2b2b"/><rect x="-10" y="-15" width="10" height="6" rx="1" fill="#2b2b2b"/>'
             '<circle cx="2" cy="1" r="8" fill="#5a6b7a" stroke="#dfe6ec" stroke-width="2"/><circle cx="2" cy="1" r="3.5" fill="#1b2630"/>'
             '<rect x="9" y="-14" width="7" height="4" fill="#fff"/>', x, y, s)


def telecamera(x, y, s=1.0):
    return g('<rect x="-22" y="-12" width="34" height="22" rx="3" fill="#3d4b57" stroke="#2b2b2b" stroke-width="1.5"/>'
             '<path d="M12,-6 L24,-10 L24,6 L12,2 Z" fill="#2b2b2b"/><circle cx="-14" cy="-17" r="5" fill="#3d4b57" stroke="#2b2b2b" stroke-width="1.3"/>'
             '<circle cx="-2" cy="-17" r="5" fill="#3d4b57" stroke="#2b2b2b" stroke-width="1.3"/>'
             '<circle cx="-16" cy="-4" r="2.4" fill="#e63946"/><text x="-10" y="-1" font-size="6" fill="#fff" font-weight="bold" font-family="DejaVu Sans">REC</text>'
             '<path d="M-6,10 L-14,34 M-6,10 L2,34 M-6,10 L-6,34" stroke="#2b2b2b" stroke-width="2.2"/>', x, y, s)


def gabbiano(x, y, s=1.0, oggetto=""):
    return g('<path d="M-24,-6 Q-12,-16 0,-4 Q12,-16 24,-6 Q12,-10 0,2 Q-12,-10 -24,-6 Z" fill="#fff" stroke="#2b2b2b" stroke-width="1.4"/>'
             '<ellipse cx="0" cy="0" rx="8" ry="5" fill="#fff" stroke="#2b2b2b" stroke-width="1.3"/>'
             '<circle cx="5" cy="-2" r="1.2" fill="#2b2b2b"/><path d="M8,0 l7,2 l-7,1 z" fill="#ffb703" stroke="#2b2b2b" stroke-width=".8"/>'
             + oggetto, x, y, s)


def lumaca(x, y, s=1.0):
    return g('<path d="M-30,20 Q-34,8 -24,8 L24,8 Q34,8 32,20 Z" fill="#a5d66f" stroke="#2b2b2b" stroke-width="1.5"/>'
             '<circle cx="-4" cy="-6" r="20" fill="#f4a261" stroke="#2b2b2b" stroke-width="1.6"/>'
             '<path d="M-4,-6 m0,-14 a14,14 0 1 1 -1,0 m1,6 a8,8 0 1 0 1,0 m-1,4 a3,3 0 1 1 -1,0" fill="none" stroke="#b5651d" stroke-width="2"/>'
             '<path d="M22,8 Q24,-10 26,-22 M30,8 Q32,-8 36,-20" stroke="#2b2b2b" stroke-width="2.2" fill="none"/>'
             '<circle cx="26" cy="-24" r="4" fill="#fff" stroke="#2b2b2b" stroke-width="1.2"/><circle cx="36" cy="-22" r="4" fill="#fff" stroke="#2b2b2b" stroke-width="1.2"/>'
             '<circle cx="27" cy="-24" r="1.6" fill="#2b2b2b"/><circle cx="37" cy="-22" r="1.6" fill="#2b2b2b"/>'
             '<path d="M24,14 Q28,18 32,14" fill="none" stroke="#2b2b2b" stroke-width="1.4"/>'
             '<ellipse cx="22" cy="12" rx="3" ry="2" fill="#ff9eb5"/>', x, y, s)


def microfono(x, y, s=1.0, r=0):
    return g('<rect x="-2" y="0" width="4" height="16" rx="1.5" fill="#2b2b2b"/>'
             '<ellipse cx="0" cy="-4" rx="6" ry="7" fill="#9aa3ab" stroke="#2b2b2b" stroke-width="1.4"/>'
             '<path d="M-5,-6 h10 M-5,-2 h10 M-4,-10 h8" stroke="#5a6570" stroke-width="1"/>', x, y, s, r)


def carretto(x, y, s=1.0):
    righe = "".join(f'<path d="M{-30 + i * 12},-36 L{-24 + i * 12},-36 L{-18 + i * 12},-24 L{-30 + i * 12},-24 Z" fill="{"#e63946" if i % 2 else "#fff"}"/>' for i in range(5))
    return g('<rect x="-30" y="-14" width="60" height="26" rx="4" fill="#fff8e0" stroke="#2b2b2b" stroke-width="1.5"/>'
             f'<path d="M-34,-24 L0,-44 L34,-24 Z" fill="#fff" stroke="#2b2b2b" stroke-width="1.5"/>{righe}'
             '<path d="M-34,-24 L0,-44 L34,-24 Z" fill="none" stroke="#2b2b2b" stroke-width="1.5"/>'
             '<line x1="0" y1="-24" x2="0" y2="-14" stroke="#2b2b2b" stroke-width="2"/>'
             '<circle cx="-18" cy="14" r="7" fill="#2b2b2b"/><circle cx="18" cy="14" r="7" fill="#2b2b2b"/>'
             '<circle cx="-18" cy="14" r="2.5" fill="#bbb"/><circle cx="18" cy="14" r="2.5" fill="#bbb"/>'
             '<text x="0" y="3" font-size="9" font-weight="bold" text-anchor="middle" fill="#e63946" font-family="DejaVu Sans">GELATI</text>'
             + gelato(-20, -20, .7) + gelato(18, -20, .7, gusto="#7b4b2a"), x, y, s)


def palloncino(x, y, s=1.0, colore="#e63946"):
    return g(f'<path d="M0,22 q-4,10 2,18 q4,8 -2,16" fill="none" stroke="#2b2b2b" stroke-width="1"/>'
             f'<ellipse cx="0" cy="0" rx="17" ry="21" fill="{colore}" stroke="#2b2b2b" stroke-width="1.5"/>'
             f'<path d="M-3,21 L3,21 L0,25 Z" fill="{colore}" stroke="#2b2b2b" stroke-width="1"/>'
             f'<ellipse cx="-6" cy="-8" rx="4" ry="7" fill="#fff" opacity=".45"/>', x, y, s)


def tazza(x, y, s=1.0):
    return g('<path d="M-12,-10 L12,-10 L9,10 Q0,14 -9,10 Z" fill="#fff" stroke="#2b2b2b" stroke-width="1.5"/>'
             '<path d="M12,-6 q9,0 7,8 q-2,5 -9,3" fill="none" stroke="#2b2b2b" stroke-width="2"/>'
             '<ellipse cx="0" cy="-10" rx="12" ry="3" fill="#f3d27a" stroke="#2b2b2b" stroke-width="1.2"/>'
             '<path d="M-5,-16 q-3,-5 0,-9 q3,-4 0,-8 M4,-16 q-3,-5 0,-9 q3,-4 0,-8" fill="none" stroke="#bbb" stroke-width="1.6"/>'
             '<line x1="6" y1="-10" x2="10" y2="-26" stroke="#bbb" stroke-width="1"/><rect x="8" y="-30" width="7" height="6" fill="#ffd23f" stroke="#2b2b2b" stroke-width=".8"/>', x, y, s)


def fiore(x, y, s=1.0):
    petali = "".join(f'<ellipse cx="0" cy="-5" rx="2.6" ry="4.5" fill="#fff" stroke="#2b2b2b" stroke-width=".7" transform="rotate({a})"/>' for a in range(0, 360, 45))
    return g(f'{petali}<circle cx="0" cy="0" r="3" fill="#ffd23f" stroke="#2b2b2b" stroke-width=".8"/>', x, y, s)


def scarpa(x, y, s=1.0, r=0):
    return g('<path d="M-16,4 L-14,-8 Q-8,-8 -4,-4 L10,-2 Q18,0 18,6 L18,8 L-16,8 Z" fill="#fff" stroke="#2b2b2b" stroke-width="1.5" stroke-linejoin="round"/>'
             '<path d="M-16,8 L18,8 L18,10 L-16,10 Z" fill="#e63946" stroke="#2b2b2b" stroke-width="1.2"/>'
             '<path d="M-6,-5 l3,5 M-2,-4 l3,5 M2,-3 l3,5" stroke="#2b2b2b" stroke-width="1.2"/>'
             '<path d="M-12,11 v3 M-4,11 v3 M4,11 v3 M12,11 v3" stroke="#555" stroke-width="1.4"/>', x, y, s, r)


def fiamme(x, y, s=1.0):
    return g('<path d="M0,0 Q-14,-4 -30,4 Q-18,0 -24,10 Q-12,4 -10,12 Q-6,6 0,8 Z" fill="#ff7b00" stroke="#2b2b2b" stroke-width="1.2"/>'
             '<path d="M-2,2 Q-12,0 -20,5 Q-12,4 -12,8 Q-6,4 -2,5 Z" fill="#ffd23f"/>', x, y, s)


def moscerino(x, y, s=1.0):
    return g('<ellipse cx="-2" cy="-4" rx="3" ry="4" fill="#e3f4ff" stroke="#2b2b2b" stroke-width=".7"/>'
             '<ellipse cx="3" cy="-4" rx="3" ry="4" fill="#e3f4ff" stroke="#2b2b2b" stroke-width=".7"/>'
             '<ellipse cx="0" cy="0" rx="4" ry="2.6" fill="#2b2b2b"/>'
             '<circle cx="0" cy="5" r="2.2" fill="#ffd23f" stroke="#2b2b2b" stroke-width=".6"/>'
             '<path d="M-2,1 L0,3 L2,1" fill="none" stroke="#e63946" stroke-width=".8"/>', x, y, s)


def termometro(x, y, s=1.0):
    return g('<rect x="-4" y="-30" width="8" height="34" rx="4" fill="#fff" stroke="#2b2b2b" stroke-width="1.4"/>'
             '<rect x="-1.8" y="-26" width="3.6" height="30" fill="#e63946"/>'
             '<circle cx="0" cy="8" r="7" fill="#e63946" stroke="#2b2b2b" stroke-width="1.4"/>'
             '<text x="8" y="-20" font-size="9" font-weight="bold" fill="#e63946" font-family="DejaVu Sans">38°</text>', x, y, s)


def bandiera(x, y, s=1.0, tesa=True):
    tela = ('<path d="M0,-30 L30,-28 L28,-22 L32,-16 L0,-14 Z" fill="#2a9d8f" stroke="#2b2b2b" stroke-width="1.3"/>' if tesa
            else '<path d="M0,-30 Q4,-20 2,-12 L-4,-14 Q-1,-22 -2,-30 Z" fill="#2a9d8f" stroke="#2b2b2b" stroke-width="1.3"/>')
    return g(f'<line x1="0" y1="-32" x2="0" y2="10" stroke="#5a3b2a" stroke-width="2.4"/>{tela}', x, y, s)


def striscione(x, y, w, t, colore="#e63946", size=10):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{size + 6}" fill="{colore}" stroke="#2b2b2b" stroke-width="1.3"/>'
            + testo(x + w / 2, y + size + 1.5, t, size, "#fff"))


def giudice(x, s=1.0, espr="felice", flip=False, extra=""):
    return in_piedi(x, "fermo", s=s, espr=espr, canotta="#f5f5f5", pelle=3, capello="corti", col_capelli="#888",
                    flip=flip, extra=CAPPELLINO + extra)


def ostacolo(x, y, s=1.0):
    return g('<rect x="-14" y="-16" width="28" height="6" fill="#fff" stroke="#2b2b2b" stroke-width="1.2"/>'
             '<rect x="-14" y="-16" width="7" height="6" fill="#2b2b2b"/><rect x="0" y="-16" width="7" height="6" fill="#2b2b2b"/>'
             '<path d="M-12,-10 V6 M12,-10 V6 M-16,6 H-8 M8,6 H16" stroke="#2b2b2b" stroke-width="2.2"/>', x, y, s)


def peso(x, y, s=1.0):
    return g('<circle cx="0" cy="0" r="9" fill="#5a6570" stroke="#2b2b2b" stroke-width="1.5"/>'
             '<ellipse cx="-3" cy="-3" rx="3" ry="2" fill="#9aa3ab"/>', x, y, s)


def carte_mano(x, y, s=1.0):
    return g("".join(carta_volante(i * 6 - 6, 0, .8, -20 + i * 20, col) for i, col in enumerate(("#2e8b57", "#c8553d", "#2f6fd1"))), x, y, s)


def zzz(x, y):
    return testo(x, y, "z", 8) + testo(x + 7, y - 7, "z", 10) + testo(x + 15, y - 16, "Z", 13)


# ============================================================ le scene
def scena(cod):
    T = TERRA
    if cod == "F1":  # Scarpe a Molla
        a = atleta(118, 48, "salta", "felice", canotta=1, pelle=0, numero=7, s=1.05)
        return (sfondo("pista") + molla(117, 61) + molla(124, 62) + a + linee_moto(98, 72, 3, 18, 5) +
                testo(48, 30, "BOING!", 16, "#ff70a6", r=-12, contorno="#fff") + testo(190, 44, "BOING!", 13, "#ffb703", r=10, contorno="#fff"))
    if cod == "F2":  # Bibita alla Carota
        return (sfondo("stadio") + in_piedi(100, "saluta", s=1.1, espr="felice", canotta=2, pelle=2, capello="ricci", col_capelli="#1b1b1b")
                + carota_bottiglia(115, 33, .9, -40) + stelline(160, 36, 4, 16) + testo(190, 70, "GLU GLU", 11, "#ff8c1a", contorno="#fff"))
    if cod == "F3":  # Panino della Nonna
        return (sfondo("campo") + in_piedi(70, "saluta", s=1.1, espr="felice", canotta=3, pelle=1)
                + panino(112, 50, 1.05) + testo(162, 26, "GNAM!", 16, "#e63946", contorno="#fff")
                + in_piedi(195, "fermo", s=.8, espr="felice", canotta="#9b5de5", pelle=3, capello="chignon", col_capelli="#ccc", extra=OCCHIALI))
    if cod == "F4":  # Vento a Favore
        return (sfondo("stadio") + ventilatore(40, 38, 1.05) + vento(68, 36, .9) + vento(80, 56, .7)
                + atleta(158, T - 22, "corsa", "felice", canotta=4, pelle=3, numero=3, capello="coda", col_capelli="#c47a2c"))
    if cod == "F5":  # Tifo da Stadio
        return (f'<rect width="{W}" height="{H}" fill="#bfe6ff"/>' + spalti(0, 6, W, 64, onda=150)
                + f'<rect y="{T - 14}" width="{W}" height="30" fill="#d0583f"/>'
                + in_piedi(120, "braccia_su", s=1.0, espr="felice", canotta=0, pelle=4, capello="punte", col_capelli="#1b1b1b", numero=1)
                + cuore(84, 50, .9) + cuore(158, 46, .8) + cuore(140, 24, .7))
    if cod == "F6":  # Calzino Portafortuna
        return (sfondo("campo", "#e8f6ff") + calzino(110, 52, 1.6, -8, puzza=True) + stella(58, 34, 9) + stella(176, 26, 7)
                + stella(196, 58, 5) + dado(60, 70, 1.1, 12, 6) + dado(176, 74, 1.1, -10, 6)
                + f'<circle cx="150" cy="30" r="2" fill="#2b2b2b"/><circle cx="80" cy="22" r="2" fill="#2b2b2b"/>')
    if cod == "F7":  # Allenamento Segreto
        return (sfondo("notte") + '<circle cx="200" cy="24" r="12" fill="#fff6c8"/><circle cx="206" cy="20" r="11" fill="#1d2a4d"/>'
                + '<path d="M140,52 L240,38 L240,74 Z" fill="#fff59d" opacity=".35"/>'
                + atleta(118, T - 22, "corsa", "determinato", canotta=7, pelle=1, extra=FASCIA + '<g transform="translate(TX TY)"><circle cx="9" cy="-7" r="3" fill="#fff59d" stroke="#2b2b2b"/></g>')
                + '<rect x="16" y="20" width="34" height="28" fill="#ffe08a" stroke="#2b2b2b" stroke-width="1.5"/>'
                + '<line x1="33" y1="20" x2="33" y2="48" stroke="#2b2b2b" stroke-width="1.5"/>'
                + testo(33, 15, "?!", 11, "#ffe08a"))
    if cod == "F8":  # Tuffo sul Traguardo
        return (sfondo("stadio") + traguardo(150) + atleta(130, T - 20, "tuffo", "determinato", canotta=0, pelle=0, numero=5)
                + flash(205, 30, 15) + macchina_foto(205, 30, .55) + linee_moto(88, 54, 3, 20, 6))
    if cod == "F9":  # Scia del Campione
        return (sfondo("pista") + atleta(162, T - 26, "corsa", "determinato", canotta=7, pelle=4, s=1.25, numero=1)
                + atleta(92, T - 20, "corsa", "furbo", canotta=5, pelle=0, s=.95, capello="coda", col_capelli="#d9a400")
                + linee_moto(126, 34, 4, 40, 7, "#ffffff"))
    if cod == "F10":  # Giudice Distratto
        return (sfondo("pista") + giudice(60, 1.0, "felice", extra='<g transform="translate(TX TY)"><circle cx="-4" cy="-2.5" r="0"/></g>')
                + gelato(76, 46, 1.0, 20) + nuvoletta(84, 6, 80, 16, "Mmm, pistacchio!", 8, (-1, 1))
                + f'<rect x="150" y="{T - 14}" width="6" height="30" fill="#fff"/>' + atleta(170, T - 20, "corsa", "furbo", canotta=1, pelle=2, s=.9))
    if cod == "F11":  # Mantello da Supereroe
        return (sfondo("stadio", "#ffe9a8") + g(mantello(), 120, T - 28, 1.15)
                + atleta(120, T - 28, "spinge", "determinato", canotta=1, pelle=1, s=1.15) + linee_moto(70, 40, 3, 26, 7))
    if cod == "F12":  # Musichetta Motivazionale
        return (sfondo("stadio", "#ffd8a8") + stereo(50, 64, 1.1) + note(66, 34) + note(160, 20)
                + in_piedi(150, "pugno", s=1.1, espr="determinato", canotta=0, pelle=2, capello="corti", extra=FASCIA))
    if cod == "D1":  # Buccia di Banana
        return (sfondo("pista") + banana(112, T - 4, 1.0, 10) + atleta(116, T - 28, "scivola", "sorpreso", canotta=3, pelle=0)
                + stelline(100, 22, 3, 14) + testo(180, 34, "UAAAH!", 15, "#e63946", r=8, contorno="#fff"))
    if cod == "D2":  # Gomma da Masticare
        return (sfondo("pista") + atleta(132, T - 24, "corsa", "dolore", canotta=2, pelle=3)
                + f'<path d="M116,{T - 7} C110,{T - 2} 104,{T - 1} 94,{T}" fill="none" stroke="#ff70a6" stroke-width="4" stroke-linecap="round"/>'
                + f'<ellipse cx="90" cy="{T + 1}" rx="10" ry="3" fill="#ff70a6" stroke="#2b2b2b" stroke-width="1.2"/>'
                + testo(60, 38, "SCIUFF", 12, "#ff70a6", r=-8, contorno="#fff") + testo(190, 30, "SCIUFF", 10, "#ff70a6", r=8, contorno="#fff"))
    if cod == "D3":  # Lacci Annodati
        return (sfondo("pista") + atleta(124, T - 20, "cade_avanti", "sorpreso", canotta=4, pelle=1, s=1.05)
                + f'<path d="M110,{T - 4} q4,-8 10,0 q6,8 10,0" fill="none" stroke="#e63946" stroke-width="2.2"/>'
                + f'<circle cx="120" cy="{T - 4}" r="3" fill="none" stroke="#e63946" stroke-width="2"/>'
                + stelline(160, 50, 3, 12) + testo(60, 34, "OPS!", 15, "#2f6fd1", r=-10, contorno="#fff"))
    if cod == "D4":  # Ape Curiosa
        return (sfondo("campo") + in_piedi(118, "braccia_su", s=1.1, espr="sorpreso", canotta=5, pelle=2, capello="ricci", col_capelli="#2b1b10")
                + '<path d="M70,30 C90,4 160,4 170,26 C178,44 150,50 140,36" fill="none" stroke="#2b2b2b" stroke-width="1.2" stroke-dasharray="3 3"/>'
                + ape(170, 26, 1.0) + testo(205, 50, "BZZZ!", 12, "#ffb703", contorno="#2b2b2b"))
    if cod == "D5":  # Megafono Sbagliato
        return (sfondo("stadio") + in_piedi(56, "fermo", s=1.0, espr="arrabbiato", canotta="#9aa3ab", pelle=5, capello="punte", col_capelli="#7a4a2a")
                + megafono(74, 35, 1.0, -15) + onde_sonore(96, 28, 3)
                + in_piedi(172, "fermo", s=1.0, espr="sorpreso", canotta=1, pelle=0, flip=True)
                + testo(150, 18, "DESTRA!", 9, "#e63946", r=-8, contorno="#fff") + testo(196, 30, "SINISTRA!", 9, "#2f6fd1", r=8, contorno="#fff")
                + testo(158, 42, "?", 14, "#2b2b2b"))
    if cod == "D6":  # Piccione Ladro
        return (sfondo("stadio") + piccione(130, 36, 1.4) + carta_volante(152, 50, .9, 20) + panino(110, 58, .35, -20)
                + linee_moto(98, 26, 3, 24, 6) + testo(200, 24, "CRUUU!", 12, "#2b2b2b", contorno="#fff"))
    if cod == "D7":  # Pozzanghera Portatile
        return (sfondo("pista") + pozzanghera(124, T + 2, 70) + schizzi(124, T - 2) + in_piedi(124, "braccia_su", s=1.0, espr="sorpreso", canotta=2, pelle=4)
                + secchiello(38, T - 6, 1.1) + testo(196, 36, "SPLASH!", 14, "#2f6fd1", contorno="#fff"))
    if cod == "D8":  # Selfie del Tifoso
        return (sfondo("stadio") + in_piedi(150, "fermo", s=1.05, espr="arrabbiato", canotta=0, pelle=1, extra=CONIGLIO)
                + in_piedi(90, "saluta", s=1.0, espr="felice", canotta="#ffb703", pelle=3, capello="ricci", col_capelli="#c47a2c")
                + telefono(104, 22, 1.0, 10) + flash(104, 22, 8) + testo(200, 30, "CLICK!", 11, "#e63946", contorno="#fff"))
    if cod == "D9":  # Scambio di Borracce
        return (sfondo("campo") + borraccia(92, 50, 1.3, -10) + borraccia(150, 50, 1.3, 10) + frecce_scambio(121, 48)
                + testo(121, 92, "OOPS...", 11, "#2b2b2b") + in_piedi(204, "fermo", s=.8, espr="furbo", canotta=6, pelle=5)
                + in_piedi(36, "fermo", s=.8, espr="sorpreso", canotta=1, pelle=0))
    if cod == "D10":  # Cane Invasore
        return (sfondo("stadio") + atleta(170, T - 24, "corsa", "sorpreso", canotta=3, pelle=2, numero=1)
                + bassotto(92, T - 6, 1.05) + linee_moto(56, T - 14, 3, 16, 5) + cuore(60, 30, .9) + cuore(40, 40, .7)
                + testo(122, 30, "BAU!", 13, "#9c5a2c", contorno="#fff"))
    if cod == "D11":  # Trombetta da Stadio
        return (sfondo("stadio") + trombetta(76, 44, 1.2, -6) + onde_sonore(108, 42, 4)
                + in_piedi(180, "fermo", s=1.05, espr="dolore", canotta=5, pelle=1, flip=True,
                           extra='<g transform="translate(TX TY)"><circle cx="-10" cy="0" r="4" fill="#d9a074" stroke="#2b2b2b"/><circle cx="10" cy="0" r="4" fill="#d9a074" stroke="#2b2b2b"/></g>')
                + testo(120, 20, "PEEEEP!", 14, "#e63946", r=-6, contorno="#fff"))
    if cod == "D12":  # Fischietto Finto
        return (sfondo("pista") + fischietto(70, 40, 1.3, -10) + testo(110, 26, "FIIIII!", 13, "#e63946", contorno="#fff")
                + atleta(170, T - 34, "salta", "sorpreso", canotta=6, pelle=3, s=1.0) + stelline(170, 22, 3, 10))
    if cod == "D13":  # Sasso nella Scarpa
        return (sfondo("pista") + in_piedi(80, "zoppo", s=1.1, espr="dolore", canotta=1, pelle=0)
                + lente(176, 46, 1.2, sasso(0, 0, 1.6)) + testo(118, 22, "AHIA!", 13, "#e63946", contorno="#fff"))
    if cod == "X1":  # Occhio di Falco
        return (sfondo("stadio", "#dff3ff") + falco(70, 48, 1.3) + mano_furtiva(200, 56, 1.0, True, banana(-6, -8, .7))
                + '<path d="M104,40 L170,50" stroke="#e63946" stroke-width="2" stroke-dasharray="4 3"/>'
                + testo(130, 26, "TI HO VISTO!", 10, "#e63946", contorno="#fff"))
    if cod == "X2":  # Specchio Riflettente
        return (sfondo("campo", "#eaf6ff") + specchio(170, 40, 1.15) + banana(110, 36, .9, 30)
                + '<path d="M70,60 L146,40" stroke="#2b2b2b" stroke-width="1.6" stroke-dasharray="4 3"/>'
                + '<path d="M146,40 L70,22" stroke="#e63946" stroke-width="2" stroke-dasharray="4 3"/><path d="M72,22 l8,-2 l-3,6 z" fill="#e63946"/>'
                + in_piedi(44, "fermo", s=.9, espr="sorpreso", canotta=6, pelle=2) + testo(110, 90, "BOING!", 11, "#e63946"))
    if cod == "X3":  # Guardia del Corpo
        return (sfondo("stadio") + in_piedi(120, "fermo", s=1.35, espr="arrabbiato", canotta="#1f2a33", pelle=4, capello="", extra=OCCHIALI_SOLE)
                + in_piedi(182, "saluta", s=.75, espr="felice", canotta=2, pelle=0)
                + banana(56, T - 4, .8, -20) + testo(56, 46, "NO!", 13, "#e63946", contorno="#fff"))
    if cod == "X4":  # Ombrello Gigante
        return (sfondo("pista", "#cfd8dc") + nuvola(60, 16, 1.0, "#90a4ae") + nuvola(190, 14, .9, "#90a4ae")
                + pioggia(10, 230, 26, 70, 26) + ombrello(120, 40, 1.3) + f'<line x1="120" y1="40" x2="120" y2="70" stroke="#2b2b2b" stroke-width="2.4"/>'
                + in_piedi(120, "fermo", s=.95, espr="felice", canotta=4, pelle=1) + piccione(205, 58, .6, True))
    if cod == "S1":  # La Ola
        return (f'<rect width="{W}" height="{H}" fill="#bfe6ff"/>' + spalti(0, 8, W, 66, onda=120)
                + f'<rect y="{T - 10}" width="{W}" height="30" fill="#d0583f"/>' + testo(120, 96, "OLAAAA!", 13, "#fff", contorno="#2b2b2b"))
    if cod == "S2":  # Il Fotografo
        return (sfondo("stadio") + in_piedi(68, "fermo", s=1.0, espr="felice", canotta="#9aa3ab", pelle=5, capello="corti", extra=CAPPELLINO)
                + macchina_foto(86, 46, .8) + flash(100, 40, 12)
                + atleta(170, T - 28, "salta", "occhiolino", canotta=5, pelle=0, s=1.0) + testo(214, 28, "CLICK!", 10, "#e63946", contorno="#fff"))
    if cod == "S3":  # Ciao Mamma!
        return (sfondo("stadio") + telecamera(56, 50, 1.1) + in_piedi(156, "saluta", s=1.1, espr="felice", canotta=1, pelle=3, capello="coda", col_capelli="#3b2a20")
                + nuvoletta(170, 6, 66, 18, "CIAO MAMMA!", 8, (-1, 1)))
    if cod == "S4":  # Calzino Perso
        return (sfondo("pista") + gabbiano(150, 26, 1.2, calzino(16, 12, .45, -30)) + in_piedi(80, "zoppo", s=1.0, espr="sorpreso", canotta=0, pelle=2)
                + testo(200, 70, "NOOO!", 12, "#e63946", contorno="#fff"))
    if cod == "S5":  # Mascotte in Pista
        return (sfondo("stadio") + lumaca(120, 52, 1.2) + in_piedi(94, "braccia_su", s=.9, espr="sorpreso", canotta=2, pelle=1)
                + '<path d="M60,40 a18,10 0 1 0 6,-12" fill="none" stroke="#fff" stroke-width="2"/>' + cuore(176, 18, 1.0))
    if cod == "S6":  # Speaker Entusiasta
        return (sfondo("stadio") + '<rect x="20" y="40" width="70" height="44" fill="#5a6570" stroke="#2b2b2b" stroke-width="1.5"/>'
                + atleta(52, 52, "saluta", "determinato", canotta="#e63946", pelle=1, s=.9) + microfono(66, 48, .9, 20)
                + '<rect x="20" y="62" width="70" height="22" fill="#5a6570" stroke="#2b2b2b" stroke-width="1.5"/>'
                + nuvoletta(100, 10, 132, 20, "FENOMENOOOO!", 10, (-1, 1)) + onde_sonore(96, 52, 3))
    if cod == "S7":  # Il Gelataio
        return (sfondo("pista") + carretto(170, 54, 1.0) + in_piedi(60, "fermo", s=.9, espr="felice", canotta=1, pelle=0, flip=True)
                + in_piedi(96, "fermo", s=.9, espr="felice", canotta=4, pelle=2) + cuore(60, 20, .9) + cuore(98, 16, .9))
    if cod == "S8":  # Palloncino in Pista
        return (sfondo("pista") + palloncino(150, 34, 1.1) + atleta(104, T - 26, "scivola", "sorpreso", canotta=3, pelle=4, r=-10)
                + stelline(130, 42, 3, 8) + testo(70, 26, "BOING!", 12, "#e63946", contorno="#fff"))
    if cod == "S9":  # Camomilla nella Borraccia
        return (sfondo("campo", "#dfe7ff") + in_piedi(80, "dorme", s=1.1, espr="dorme", canotta=5, pelle=0) + zzz(100, 26)
                + tazza(170, 60, 1.3) + fiore(206, 76) + fiore(140, 80, .8) + fiore(220, 54, .7))
    if cod == "S10":  # Scarpa Volante
        return (sfondo("stadio") + scarpa(180, 26, 1.1, -25) + linee_moto(160, 30, 3, 26, 6)
                + in_piedi(84, "zoppo", s=1.05, espr="sorpreso", canotta=7, pelle=3) + cuore(130, 50, .8) + cuore(144, 60, .6))
    if cod == "S11":  # Stretching Improvviso
        return (sfondo("campo") + atleta(120, T - 34, "saltella", "felice", canotta=4, pelle=2, s=1.05)
                + '<path d="M96,80 q-6,-10 0,-20 M144,80 q6,-10 0,-20" fill="none" stroke="#fff" stroke-width="2.2"/>'
                + testo(50, 30, "1!", 13, "#e63946", contorno="#fff") + testo(190, 26, "2!", 13, "#2f6fd1", contorno="#fff")
                + testo(205, 64, "3!", 13, "#2a9d8f", contorno="#fff"))
    if cod == "S12":  # Rimonta Epica
        return (sfondo("stadio") + atleta(186, T - 22, "corsa", "sorpreso", canotta=1, pelle=0, s=.9)
                + fiamme(96, T - 22, 1.4) + atleta(120, T - 22, "corsa", "determinato", canotta=0, pelle=2, s=1.05, numero=8)
                + testo(70, 26, "VAIII!", 14, "#ff7b00", contorno="#fff"))
    if cod == "S13":  # Moscerino nell'Occhio
        return (sfondo("campo") + in_piedi(100, "fermo", s=1.25, espr="occhiolino", canotta=6, pelle=1)
                + '<path d="M118,36 q2,6 0,10" fill="none" stroke="#5fb0ef" stroke-width="2.2"/>'
                + lente(180, 40, 1.1, moscerino(0, 0, 2.0)) + testo(56, 30, "UFF!", 12, "#2b2b2b", contorno="#fff"))
    if cod == "M1":  # Giornata Perfetta
        return (sfondo("campo") + sole(70, 34, 16, occhiali=True) + nuvola(170, 26, .9) + nuvola(214, 46, .6)
                + piccione(150, 66, .5) + '<line x1="132" y1="50" x2="168" y2="80" stroke="#e63946" stroke-width="3"/>'
                + '<circle cx="150" cy="65" r="20" fill="none" stroke="#e63946" stroke-width="3"/>')
    if cod == "M2":  # Acquazzone
        pesce = g('<path d="M-12,0 Q0,-10 12,0 Q0,10 -12,0 Z M12,0 l8,-6 v12 z" fill="#ffb703" stroke="#2b2b2b" stroke-width="1.3"/>'
                  '<circle cx="-6" cy="-1" r="1.4" fill="#2b2b2b"/>', 150, 64, 1.2)
        return (sfondo("pista", "#90a4ae") + nuvola(70, 20, 1.3, "#607d8b") + nuvola(180, 16, 1.1, "#607d8b")
                + pioggia(10, 230, 30, 90, 40, "#e3f4ff") + pesce + ombrello(150, 48, .45, "#ff70a6")
                + f'<line x1="150" y1="48" x2="150" y2="60" stroke="#2b2b2b" stroke-width="1.6"/>')
    if cod == "M3":  # Vento alle Spalle
        return (sfondo("pista") + bandiera(36, 60, 1.1) + vento(56, 26, .8) + atleta(150, T - 22, "corsa", "felice", canotta=2, pelle=4, numero=2)
                + '<rect x="186" y="10" width="46" height="16" rx="3" fill="#1f2a33"/>' + testo(209, 22, "+2,1", 11, "#7CFC00"))
    if cod == "M4":  # Caldo Tropicale
        return (sfondo("campo", "#ffcf8a") + sole(48, 28, 16, "sudato") + termometro(212, 52, 1.0)
                + in_piedi(132, "fermo", s=1.1, espr="stanco", canotta=3, pelle=1)
                + f'<ellipse cx="132" cy="{T + 1}" rx="24" ry="3" fill="#5fb0ef" opacity=".8"/>')
    if cod == "M5":  # Vento Contrario
        return (sfondo("pista", "#cfe3ef") + vento(176, 22, -.9, "#7f9aaa") + vento(200, 50, -.7, "#7f9aaa")
                + atleta(110, T - 26, "spinge", "stanco", canotta=1, pelle=0, s=1.05)
                + g(CAPPELLINO.replace("TX", "0").replace("TY", "0"), 44, 38, 1.3, -40) + fischietto(30, 62, .7, 50))
    if cod == "M6":  # Nebbia Fitta
        nebbia = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="12" fill="#eceff1" opacity=".85"/>'
                         for x, y, rx in ((40, 30, 60), (160, 22, 80), (90, 60, 90), (210, 70, 60), (30, 84, 50)))
        return (sfondo("pista", "#cfd8dc") + atleta(150, T - 24, "corsa", "sorpreso", canotta=0, pelle=1, s=.9) + nebbia
                + '<circle cx="72" cy="46" r="3" fill="#fff" stroke="#2b2b2b"/><circle cx="82" cy="46" r="3" fill="#fff" stroke="#2b2b2b"/>'
                + '<circle cx="73" cy="46" r="1.3" fill="#2b2b2b"/><circle cx="83" cy="46" r="1.3" fill="#2b2b2b"/>' + testo(120, 92, "...dove sono?", 9, "#607d8b"))
    if cod == "M7":  # Stadio Pieno
        return (f'<rect width="{W}" height="{H}" fill="#bfe6ff"/>' + spalti(0, 22, W, 62, braccia=True)
                + striscione(52, 4, 136, "TUTTO ESAURITO!", "#e63946", 10))
    # ---- personaggi
    if cod == "A1":  # Saetta Rossi
        return (sfondo("pista", "#fff3c4") + '<path d="M60,6 L36,50 L52,50 L40,94 L80,36 L62,36 L76,6 Z" fill="#ffd23f" stroke="#2b2b2b" stroke-width="1.5"/>'
                + atleta(150, T - 22, "corsa", "determinato", canotta=0, pelle=0, capello="punte", col_capelli="#c0392b", s=1.1, numero=1)
                + linee_moto(110, 40, 4, 34, 7))
    if cod == "A2":  # Nonna Pina
        return (sfondo("pista", "#ffe3f0") + atleta(120, T - 22, "corsa", "felice", canotta="#9b5de5", pelle=3, capello="chignon",
                                                    col_capelli="#d9d9d9", s=1.1, numero=64, extra=OCCHIALI)
                + linee_moto(84, 46, 3, 24, 7) + testo(196, 30, "1964!", 12, "#9b5de5", contorno="#fff"))
    if cod == "A3":  # Bruno Bisonte
        return (sfondo("campo") + in_piedi(110, "lancia", s=1.28, espr="determinato", canotta=7, pelle=4, capello="", extra=BAFFI)
                + peso(70, 18, 1.1) + linee_moto(84, 22, 2, 14, 6, "#2b2b2b", 1) + testo(196, 34, "UGH!", 14, "#2b2b2b", contorno="#fff"))
    if cod == "A4":  # Lola Libellula
        ali = ('<ellipse cx="-10" cy="-26" rx="8" ry="18" fill="#bfe9ff" opacity=".85" stroke="#2b2b2b" stroke-width="1" transform="rotate(-35 -10 -26)"/>'
               '<ellipse cx="-4" cy="-24" rx="7" ry="16" fill="#bfe9ff" opacity=".85" stroke="#2b2b2b" stroke-width="1" transform="rotate(-10 -4 -24)"/>')
        return (sfondo("campo", "#e9f7ff") + '<rect x="160" y="62" width="70" height="22" rx="5" fill="#2f6fd1" stroke="#2b2b2b" stroke-width="1.5"/>'
                + '<line x1="150" y1="44" x2="232" y2="44" stroke="#ffd23f" stroke-width="3"/>'
                + g(ali, 120, 58, 1.1) + atleta(120, 58, "salta", "felice", canotta=5, pelle=2, capello="coda", col_capelli="#1b1b1b", s=1.1, r=-15))
    if cod == "A5":  # Prof. Ostacolo
        return (sfondo("pista") + ostacolo(150, T - 4, 1.5) + atleta(118, 52, "salta", "determinato", canotta="#f5f5f5", pelle=0,
                                                                    capello="corti", col_capelli="#9e9e9e", s=1.05, extra=OCCHIALI + BAFFI)
                + ostacolo(52, T - 4, 1.1))
    if cod == "A6":  # Mara Mezzofondo
        return (sfondo("pista") + atleta(124, T - 22, "corsa", "determinato", canotta=2, pelle=1, capello="coda", col_capelli="#c47a2c",
                                         s=1.1, numero=800, extra=FASCIA) + borraccia(200, 64, .8) + linee_moto(88, 46, 3, 24, 7))
    if cod == "A7":  # Tobia Tartaruga
        guscio = ('<path d="M-6,-20 Q-26,-14 -22,4 Q-14,8 -4,2 Z" fill="#5d9c3a" stroke="#2b2b2b" stroke-width="1.5"/>'
                  '<path d="M-12,-14 l-4,6 l4,6 M-12,-14 l5,4" fill="none" stroke="#2f5e1e" stroke-width="1.4"/>')
        return (sfondo("campo") + g(guscio, 120, T - 22, 1.2) + in_piedi(120, "fermo", s=1.2, espr="felice", canotta=2, pelle=3, capello="")
                + banana(170, T - 2, .8) + pozzanghera(60, T + 2, 46) + testo(200, 30, "zen.", 12, "#2a9d8f", contorno="#fff"))
    if cod == "A8":  # Zeno Furbetto
        return (sfondo("stadio") + in_piedi(110, "saluta", s=1.2, espr="furbo", canotta=6, pelle=4, capello="punte", col_capelli="#1b1b1b")
                + carte_mano(128, 30, 1.2) + testo(186, 50, "eh eh...", 12, "#6a3fb5", contorno="#fff") + dado(190, 74, .9, 15, 6))
    return sfondo("campo")


def illustrazione(cod):
    contenuto = scena(cod)
    return (f'<svg class="illu" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">'
            f'<clipPath id="cl-{cod}"><rect width="{W}" height="{H}" rx="6"/></clipPath>'
            f'<g clip-path="url(#cl-{cod})">{contenuto}</g></svg>')
