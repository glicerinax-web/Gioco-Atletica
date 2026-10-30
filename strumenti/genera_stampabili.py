#!/usr/bin/env python3
"""Genera le pagine HTML stampabili di "Atletica Strampalata".

Uso:  python3 strumenti/genera_stampabili.py
Scrive in stampabili/html/:
  carte.html, schede.html, gettoni.html,
  plancia-A2.html, plancia-A3.html, plancia-A4-4fogli.html
I PDF si ottengono poi con:  node strumenti/stampa_pdf.js

Il testo delle carte viene letto da CARTE.md e quello degli atleti da
REGOLAMENTO.md (sezione 10): basta modificare i file Markdown e rigenerare.
"""
import html
import os
import re

from illustrazioni import illustrazione

RADICE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
USCITA = os.path.join(RADICE, "stampabili", "html")
PLANCIA_REL = "../../plancia.svg"
PLANCIA_W, PLANCIA_H = 1800, 1420

FONT = "'DejaVu Sans', Arial, Helvetica, sans-serif"
INK = "#1f2a33"

MAZZI = {
    "facilitazione": ("FACILITAZIONE", "#2e8b57", "Scarpetta"),
    "dispetto": ("DISPETTO", "#c8553d", "Scarpetta"),
    "difesa": ("DIFESA", "#2f6fd1", "Scarpetta"),
    "stadio": ("STADIO", "#e08a00", "Stadio"),
    "meteo": ("METEO", "#2a9bb8", "Meteo"),
    "atleta": ("ATLETA", "#6a3fb5", "Atleta"),
}
DORSI = {
    "Scarpetta": ("#2f6f3a", "SCARPETTA", "facilitazioni · dispetti · difese"),
    "Stadio": ("#e08a00", "STADIO", "imprevisti dello stadio"),
    "Meteo": ("#2a9bb8", "METEO", "condizioni di gara"),
    "Atleta": ("#6a3fb5", "ATLETA", "personaggio"),
}


# ------------------------------------------------------------ utilità
def md(testo):
    """Markdown in linea (grassetto, corsivo, codice) -> HTML."""
    t = html.escape(testo.strip(), quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t


def a_capo_sezioni(t):
    """Va a capo prima di ogni "<b>Etichetta</b>:" che non sia all'inizio."""
    return re.sub(r"(?<!^)\s*(<b>[^<]{2,30}</b>:)", r"<br>\1", t)


def celle(riga):
    return [c.strip() for c in riga.strip().strip("|").split("|")]


def pagina_html(titolo, css, corpo, script=""):
    return f"""<!doctype html>
<html lang="it"><head><meta charset="utf-8"><title>{titolo}</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ font-family: {FONT}; color: {INK}; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.pagina {{ page-break-after: always; break-after: page; overflow: hidden; position: relative; }}
.pagina:last-child {{ page-break-after: auto; break-after: auto; }}
{css}
</style></head>
<body>
{corpo}
<script>
{script}
window.__pronto = true;
</script>
</body></html>
"""


def scrivi(nome, contenuto):
    os.makedirs(USCITA, exist_ok=True)
    with open(os.path.join(USCITA, nome), "w", encoding="utf-8") as f:
        f.write(contenuto)
    print("scritto", os.path.join("stampabili", "html", nome))


# ------------------------------------------------------------ lettura dati
def leggi_carte():
    tipo = None
    carte = []
    with open(os.path.join(RADICE, "CARTE.md"), encoding="utf-8") as f:
        for riga in f:
            if riga.startswith("### ") and "Facilitazioni" in riga:
                tipo = "facilitazione"
            elif riga.startswith("### ") and "Dispetti" in riga:
                tipo = "dispetto"
            elif riga.startswith("### ") and "Difese" in riga:
                tipo = "difesa"
            elif riga.startswith("## ") and "STADIO" in riga:
                tipo = "stadio"
            elif riga.startswith("## ") and "METEO" in riga:
                tipo = "meteo"
            elif riga.startswith("## "):
                tipo = None
            if not (tipo and riga.startswith("|")):
                continue
            c = celle(riga)
            if not re.fullmatch(r"[FDXSM]\d+", c[0]):
                continue
            carta = {"tipo": tipo, "codice": c[0], "nome": c[1].strip("*"), "copie": int(c[2])}
            if tipo == "meteo":
                carta["corsa"], carta["concorso"], carta["testo"] = c[3], c[4], c[5]
            else:
                carta["effetto"], carta["testo"] = c[3], c[4]
            carte.append(carta)
    return carte


def leggi_atleti():
    atleti, dentro = [], False
    with open(os.path.join(RADICE, "REGOLAMENTO.md"), encoding="utf-8") as f:
        for riga in f:
            if riga.startswith("## "):
                dentro = riga.startswith("## 10.")
                continue
            if dentro and riga.startswith("| **"):
                c = celle(riga)
                atleti.append({"tipo": "atleta", "codice": f"A{len(atleti) + 1}", "nome": c[0].strip("*"),
                               "specialita": c[1], "abilita": c[2]})
    return atleti


# ------------------------------------------------------------ carte
SIMBOLI = {
    "facilitazione": '<path d="M12 3 L14.5 9 L21 9.5 L16 13.5 L17.5 20 L12 16.5 L6.5 20 L8 13.5 L3 9.5 L9.5 9 Z"/>',
    "dispetto": '<path d="M4 15 C6 6 16 4 21 7 C17 8 12 10 9 16 C8 18 5 18 4 15 Z"/>',
    "difesa": '<path d="M12 3 L20 6 C20 13 17 18 12 21 C7 18 4 13 4 6 Z"/>',
    "stadio": '<path d="M12 3 L14.5 9 L21 9.5 L16 13.5 L17.5 20 L12 16.5 L6.5 20 L8 13.5 L3 9.5 L9.5 9 Z"/>',
    "meteo": '<circle cx="9" cy="9" r="4"/><path d="M7 19 C3 19 3 14 7 14 C8 10 14 10 15 13 C19 12 21 16 18 19 Z"/>',
    "atleta": '<circle cx="13" cy="4.5" r="2.5"/><path d="M12 8 L8 13 L4 13 M12 8 L15 13 L19 14 M12 8 L11 15 L14 21 M11 15 L7 21" '
              'stroke="currentColor" stroke-width="2.4" fill="none" stroke-linecap="round"/>',
}


def simbolo(tipo, colore, dim=7):
    return (f'<svg class="simbolo" viewBox="0 0 24 24" style="width:{dim}mm;height:{dim}mm;color:{colore};fill:{colore}">'
            f'{SIMBOLI[tipo]}</svg>')


def html_carta(c):
    etichetta, colore, mazzo = MAZZI[c["tipo"]]
    if c["tipo"] == "meteo":
        corpo = (f'<div class="sez"><span class="etq">In corsa</span>{md(c["corsa"])}</div>'
                 f'<div class="sez"><span class="etq">Nei concorsi</span>{md(c["concorso"])}</div>')
        testo = md(c["testo"].strip("*"))
    elif c["tipo"] == "atleta":
        corpo = f'<div class="spec">{md(c["specialita"])}</div><div class="sez">{md(c["abilita"])}</div>'
        testo = ""
    else:
        corpo = f'<div class="sez">{a_capo_sezioni(md(c["effetto"]))}</div>'
        testo = md(c["testo"].strip("*"))
    quando = {"facilitazione": "si gioca nel tuo turno, su di te",
              "dispetto": "si gioca nel tuo turno, su un avversario",
              "difesa": "si gioca in qualsiasi momento",
              "stadio": "si pesca fermandosi su una ★",
              "meteo": "vale per tutta la disciplina",
              "atleta": "abilità sempre attiva"}[c["tipo"]]
    return f"""<div class="carta" style="--c:{colore}">
  <div class="testa"><div class="tipo">{etichetta}</div><div class="nome">{html.escape(c["nome"])}</div>{simbolo(c["tipo"], "#fff", 8)}</div>
  <div class="quando">{quando}</div>
  <div class="corpo">{illustrazione(c["codice"])}<div class="effetto">{corpo}</div>{f'<div class="colore">{testo}</div>' if testo else ''}</div>
  <div class="piede"><span>Atletica Strampalata</span><span>{mazzo} · {c["codice"]}</span></div>
</div>"""


def html_dorso(mazzo):
    colore, titolo, sotto = DORSI[mazzo]
    tipo = {"Scarpetta": "facilitazione", "Stadio": "stadio", "Meteo": "meteo", "Atleta": "atleta"}[mazzo]
    return f"""<div class="carta dorso" style="--c:{colore}">
  <div class="cornice">{simbolo(tipo, "#fff", 20)}<div class="d-titolo">{titolo}</div>
  <div class="d-sotto">{sotto}</div><div class="d-gioco">ATLETICA<br>STRAMPALATA</div></div>
</div>"""


def genera_carte():
    carte = leggi_carte()
    atleti = leggi_atleti()
    gruppi = [
        ("Scarpetta", [c for c in carte if MAZZI[c["tipo"]][2] == "Scarpetta"]),
        ("Stadio", [c for c in carte if c["tipo"] == "stadio"]),
        ("Meteo", [c for c in carte if c["tipo"] == "meteo"]),
        ("Atleta", atleti),
    ]
    pagine = []
    for mazzo, elenco in gruppi:
        copie = [c for c in elenco for _ in range(c.get("copie", 1))]
        for i in range(0, len(copie), 9):
            blocco = "".join(html_carta(c) for c in copie[i:i + 9])
            pagine.append(f'<div class="pagina foglio"><div class="griglia">{blocco}</div>'
                          f'<div class="nota">Mazzo {mazzo} · stampa al 100 % · ritaglia lungo le linee grigie</div></div>')
    for mazzo in DORSI:
        blocco = "".join(html_dorso(mazzo) for _ in range(9))
        pagine.append(f'<div class="pagina foglio"><div class="griglia">{blocco}</div>'
                      f'<div class="nota">Dorso {mazzo} · stampalo sul retro delle pagine del mazzo {mazzo}</div></div>')
    css = """
@page { size: A4 portrait; margin: 0; }
.foglio { width: 210mm; height: 297mm; display: flex; align-items: center; justify-content: center; }
.griglia { display: grid; grid-template-columns: repeat(3, 63mm); grid-auto-rows: 88mm; }
.nota { position: absolute; bottom: 5mm; left: 0; right: 0; text-align: center; font-size: 7pt; color: #888; }
.carta { width: 63mm; height: 88mm; outline: 0.2mm solid #9a9a9a; outline-offset: -0.1mm; padding: 2.2mm;
         display: flex; flex-direction: column; background: #fffaf0; }
.testa { background: var(--c); color: #fff; border-radius: 2.5mm 2.5mm 0 0; padding: 1.6mm 2mm 1.8mm; position: relative; }
.testa .simbolo { position: absolute; right: 1.6mm; top: 1.6mm; opacity: .9; }
.tipo { font-size: 6pt; letter-spacing: .4mm; font-weight: bold; opacity: .9; }
.nome { font-size: 11pt; font-weight: bold; line-height: 1.1; margin-top: .4mm; padding-right: 9mm; min-height: 7mm;
        display: flex; align-items: center; }
.quando { font-size: 6pt; text-align: center; color: #fff; background: color-mix(in srgb, var(--c) 75%, #000);
          padding: .5mm 0; }
.corpo { flex: 1; border: .5mm solid var(--c); border-top: 0; border-radius: 0 0 2.5mm 2.5mm; padding: 2mm;
         display: flex; flex-direction: column; overflow: hidden; background: #fff; }
.colore { margin-top: auto !important; }
.corpo { position: relative; }
.illu { display: block; flex: none; width: calc(100% + 4mm); height: 28mm; margin: -2mm -2mm 1.6mm; border-bottom: .4mm solid var(--c); }
.effetto, .colore { position: relative; }
.effetto { font-size: 8.4pt; line-height: 1.28; }
.sez + .sez { margin-top: 1.6mm; }
.etq { display: block; font-size: 6.5pt; font-weight: bold; color: var(--c); text-transform: uppercase; letter-spacing: .3mm; }
.spec { font-size: 8pt; font-style: italic; color: var(--c); margin-bottom: 2mm; font-weight: bold; }
.colore { font-size: 7.2pt; font-style: italic; line-height: 1.25; color: #555; border-top: .3mm dotted #bbb; padding-top: 1.4mm; margin-top: 1.6mm; }
.piede { display: flex; justify-content: space-between; font-size: 5.5pt; color: #999; padding: .8mm .5mm 0; }
.dorso { padding: 2.2mm; background: #fff; }
.cornice { flex: 1; border-radius: 3mm; background: var(--c); color: #fff; display: flex; flex-direction: column;
           align-items: center; justify-content: center; text-align: center;
           background-image: repeating-linear-gradient(45deg, rgba(255,255,255,.08) 0 3mm, transparent 3mm 6mm); }
.d-titolo { font-size: 17pt; font-weight: bold; letter-spacing: .6mm; margin-top: 3mm; }
.d-sotto { font-size: 7pt; margin-top: 1.5mm; opacity: .9; }
.d-gioco { font-size: 8pt; font-weight: bold; margin-top: 8mm; letter-spacing: .4mm; border-top: .3mm solid rgba(255,255,255,.6); padding-top: 2mm; }
"""
    script = """
// Riduce il corpo del testo delle carte troppo piene finché il contenuto entra nella carta.
document.querySelectorAll('.corpo').forEach(function (corpo) {
  var eff = corpo.querySelector('.effetto'), col = corpo.querySelector('.colore');
  var fe = 8.4, fc = 7.2;
  while (corpo.scrollHeight > corpo.clientHeight + 1 && fe > 6) {
    fe -= 0.2; fc = Math.max(5.6, fc - 0.2);
    eff.style.fontSize = fe + 'pt'; if (col) col.style.fontSize = fc + 'pt';
  }
  if (corpo.scrollHeight > corpo.clientHeight + 1) corpo.setAttribute('data-troppo-pieno', '1');
});
"""
    scrivi("carte.html", pagina_html("Atletica Strampalata - Carte", css, "\n".join(pagine), script))


# ------------------------------------------------------------ schede
DISCIPLINE = ["100 m", "Salto in lungo", "Getto del peso", "Salto in alto", "400 m",
              "110 m hs", "Giavellotto", "200 m", "400 m hs", "800 m"]
RECORD = [("100 m", "2 turni"), ("110 m hs", "3 turni"), ("200 m", "2 turni"), ("400 m", "4 turni"),
          ("400 m hs", "5 turni"), ("800 m", "8 turni"), ("Salto in lungo", "8,00 m"), ("Salto in alto", "2,30 m"),
          ("Getto del peso", "21,00 m"), ("Giavellotto", "85,0 m")]


def tabella(intestazioni, righe, classi=""):
    th = "".join(f"<th>{h}</th>" for h in intestazioni)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in righe)
    return f'<table class="{classi}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def scheda_giocatore_fronte():
    fiato = "".join(f'<div class="tacca"><span>{i}</span></div>' for i in range(9))
    grinta = "".join('<div class="quadro"></div>' for _ in range(5))
    return f"""<div class="mezza">
  <div class="sch-testa"><div><b>SCHEDA GIOCATORE</b><br><span class="piccolo">Atletica Strampalata</span></div>
  <div class="campo">Nome<span></span></div></div>
  <div class="riga2"><div class="campo">Colore / corsia<span></span></div><div class="campo">Atleta<span></span></div></div>
  <h3>FIATO (corse) · CONCENTRAZIONE (concorsi)</h3>
  <div class="traccia">{fiato}</div>
  <p class="piccolo">Metti una Borraccia sul valore attuale (massimo 8). A fine disciplina torna a zero.</p>
  <div class="riga2"><div><h3>GRINTA (decathlon)</h3><div class="quadri">{grinta}</div>
  <p class="piccolo">Barra un quadretto per ogni gettone speso: max 2 per disciplina, +1 Fiato o +1 Concentrazione.</p></div>
  <div><h3>CARTELLINO GIALLO</h3><div class="quadri"><div class="quadro giallo"></div></div>
  <p class="piccolo">Il secondo nella stessa gara = squalifica: diventi Tifoso.</p></div></div>
  <h3>IL TURNO DI CORSA</h3>
  <ol><li>Gioca al massimo <b>1 carta</b> (le Difese in qualsiasi momento).</li>
  <li>Dichiara il <b>ritmo</b> e tira <b>3 dadi</b>.</li>
  <li>Tieni i dadi del ritmo e muovi della loro somma (tutta).</li>
  <li>Risolvi la casella: ★, ostacolo, banana, pozzanghera.</li>
  <li>Applica le combinazioni.</li></ol>
  {tabella(["Ritmo", "Dadi tenuti", "Costo / bonus"], [
        ["Passo", "1", "+1 Fiato e peschi 1 carta"], ["Corsa", "2 a scelta", "—"],
        ["Scatto", "tutti e 3", "−2 Fiato (−3 nelle ultime 10 caselle di 400/400 hs)"]], "mini")}
  {tabella(["Combinazione", "Effetto"], [
        ["Doppio tra i dadi tenuti", "<b>Falcata Perfetta</b>: peschi 1 carta"],
        ["Tris sul tiro", "<b>In Trance</b>: muovi la somma dei 3 dadi gratis e peschi 1 carta"],
        ["Tris di 1", "<b>Crampo Comico</b>: fermo, +2 Fiato"],
        ["4-5-6 / 1-2-3", "<b>Vento in Poppa</b> +1 Fiato / <b>Inciampo</b> −1 Fiato"]], "mini")}
</div>"""


def scheda_giocatore_retro():
    return f"""<div class="mezza">
  <div class="sch-testa"><div><b>PROMEMORIA CONCORSI</b><br><span class="piccolo">3 tentativi · vale il migliore · 2 Concentrazione (3 nell'alto)</span></div></div>
  <h3>SALTO IN LUNGO</h3>
  <p>Rincorsa: 3 dadi, ne tieni 2. Poi tira 1 dado alla volta finché vuoi: oltre la casella 12 è <b>nullo</b>.
  Volo: 1 dado. Doppio nella rincorsa: +0,25 m.</p>
  <p class="formula">Misura = 4 m + (Rincorsa + Volo) × 0,25 m</p>
  <h3>SALTO IN ALTO</h3>
  <p>3 dadi, tieni i 2 migliori: la somma deve raggiungere il tiro minimo. Doppio tenuto: +1.
  3 errori consecutivi = eliminato. Puoi passare un'altezza.</p>
  {tabella(["Altezza", "1,80", "1,90", "2,00", "2,10", "2,20", "2,30", "2,40", "2,45*"],
           [["Tiro minimo", "6", "7", "8", "9", "10", "11", "12", "12"]], "mini centro")}
  <p class="piccolo">* a 2,45 m non si usa la Concentrazione.</p>
  <h3>GETTO DEL PESO</h3>
  <p>Scegli quanti dadi tirare (da 1 a 4). Anche un solo <b>1</b> = nullo.</p>
  <p class="formula">Misura = 12 m + somma × 0,5 m</p>
  <h3>GIAVELLOTTO</h3>
  <p>3 dadi: 1 sull'Angolo, 2 sulla Forza (somma).</p>
  <p class="formula">Misura = Forza × 8 m × fattore Angolo</p>
  {tabella(["Angolo", "1", "2", "3", "4", "5", "6"], [["Fattore", "nullo", "×0,7", "×0,9", "×1,0", "×0,9", "×0,6"]], "mini centro")}
  <h3>LE MIE MISURE</h3>
  {tabella(["Disciplina", "1° tentativo", "2° tentativo", "3° tentativo", "Migliore"],
           [[d, "", "", "", ""] for d in ("Lungo", "Peso", "Giavellotto")], "mini righe-alte")}
  {tabella(["Alto", "", "", "", "", "", "", "", ""], [["Esiti (O / X / –)", "", "", "", "", "", "", "", ""]], "mini righe-alte")}
</div>"""


def genera_schede():
    colonne = ["Disciplina"] + [f"Giocatore {i}<div class='nomebox'></div>" for i in range(1, 9)]
    righe = [[d] + [""] * 8 for d in DISCIPLINE]
    righe += [["Record (+2)"] + [""] * 8, ["<b>TOTALE</b>"] + [""] * 8, ["Medaglie oro / arg. / bronzo"] + [""] * 8]
    segnapunti = f"""<div class="pagina orizz">
  <h1>SEGNAPUNTI <span>Atletica Strampalata · gara secca, meeting o decathlon</span></h1>
  {tabella(colonne, righe, "grande totali")}
  <p class="piccolo">Punti per piazzamento: 1° 10 · 2° 8 · 3° 6 · 4° 5 · 5° 4 · 6° 3 · 7° 2 · 8° 1 · nullo o squalifica 0 ·
  Record dello Stadio battuto +2. Parità nel decathlon: più ori, poi più argenti, poi più bronzi.</p></div>"""

    col_sq = ["Disciplina"] + [f"Squadra {i}<div class='nomebox'></div>" for i in range(1, 5)]
    cella = "<div class='atl'>atleta: ____________ punti: ____</div><div class='atl'>atleta: ____________ punti: ____</div>"
    righe_sq = [[d] + [cella] * 4 for d in DISCIPLINE]
    righe_sq += [["Spirito di squadra (+5)"] + [""] * 4, ["<b>TOTALE</b>"] + [""] * 4]
    squadre = f"""<div class="pagina orizz">
  <h1>SEGNAPUNTI A SQUADRE <span>Squadre da 2: un atleta per disciplina · squadre da 3-4: due atleti per disciplina</span></h1>
  {tabella(col_sq, righe_sq, "grande squadre")}
  <p class="piccolo">Ogni membro gareggia in almeno 3 discipline e al massimo 7. Spirito di squadra: +5 se ogni membro ha vinto almeno una medaglia.</p></div>"""

    righe_rec = []
    for d, r in RECORD:
        righe_rec.append([f"<b>{d}</b>", r, "", "", ""])
    record = f"""<div class="pagina orizz">
  <h1>RECORD DELLO STADIO <span>scrivi qui i record battuti: restano da una partita all'altra</span></h1>
  {tabella(["Disciplina", "Record di partenza", "Nuovo record", "Atleta", "Data"], righe_rec, "grande record")}
  <p class="piccolo">Corse: vale il numero di turni impiegati, poi le caselle oltre il traguardo. Chi batte un record guadagna +2 punti.</p></div>"""

    fronte = f'<div class="pagina orizz due">{scheda_giocatore_fronte()}{scheda_giocatore_fronte()}</div>'
    retro = f'<div class="pagina orizz due">{scheda_giocatore_retro()}{scheda_giocatore_retro()}</div>'
    css = """
@page { size: A4 landscape; margin: 0; }
.orizz { width: 297mm; height: 210mm; padding: 10mm 12mm; }
h1 { font-size: 16pt; color: #c8553d; margin-bottom: 4mm; }
h1 span { font-size: 9pt; color: #777; font-weight: normal; margin-left: 3mm; }
table { border-collapse: collapse; width: 100%; }
th, td { border: .3mm solid #9aa; padding: 1mm 1.5mm; font-size: 9pt; text-align: left; vertical-align: middle; }
th { background: #2f6f3a; color: #fff; font-size: 8.5pt; }
.grande td { height: 11mm; }
.grande td:first-child { width: 38mm; font-weight: bold; background: #f4efe2; }
.totali tbody tr:nth-last-child(-n+3) td { background: #fff4c2; }
.nomebox { border-bottom: .3mm solid #fff; height: 5mm; margin-top: 1mm; }
.squadre td { height: 13mm; font-size: 7.5pt; color: #888; }
.squadre .atl + .atl { margin-top: 1.2mm; }
.squadre tbody tr:nth-last-child(-n+2) td { background: #fff4c2; }
.record td { height: 13mm; }
.record td:nth-child(2) { color: #777; width: 32mm; }
.piccolo { font-size: 8pt; color: #666; margin-top: 2mm; }
.due { display: flex; gap: 0; padding: 0; }
.mezza { width: 148.5mm; height: 210mm; padding: 8mm 9mm; border-right: .3mm dashed #bbb; font-size: 9.6pt; }
.mezza:last-child { border-right: 0; }
.mezza h3 { font-size: 9.4pt; color: #fff; background: #c8553d; padding: .8mm 2mm; margin: 2.6mm 0 1.4mm; border-radius: 1mm; }
.mezza p { line-height: 1.3; }
.mezza ol { padding-left: 5mm; line-height: 1.35; }
.sch-testa { display: flex; justify-content: space-between; align-items: flex-end; gap: 4mm; border-bottom: .6mm solid #c8553d; padding-bottom: 1.5mm; }
.sch-testa b { font-size: 13pt; color: #c8553d; }
.campo { font-size: 7pt; color: #777; flex: 1; display: flex; flex-direction: column; }
.campo span { border-bottom: .3mm solid #999; height: 6mm; }
.riga2 { display: flex; gap: 5mm; margin-top: 2mm; }
.riga2 > * { flex: 1; }
.traccia { display: flex; gap: 1.5mm; }
.tacca { flex: 1; height: 13.5mm; border: .5mm solid #2f6fd1; border-radius: 50%; display: flex; align-items: center;
         justify-content: center; font-weight: bold; font-size: 11pt; color: #2f6fd1; }
.quadri { display: flex; gap: 2mm; }
.quadro { width: 8mm; height: 8mm; border: .5mm solid #c8553d; border-radius: 1mm; }
.quadro.giallo { border-color: #c9a400; background: #fff4a8; }
.mini { margin-top: 1.5mm; }
.mini th, .mini td { font-size: 8.4pt; padding: 1.1mm 1.4mm; }
.mini th { background: #555; }
.centro th, .centro td { text-align: center; }
.righe-alte td { height: 8.5mm; }
.formula { background: #fff4c2; border-left: 1mm solid #e08a00; padding: 1mm 2mm; margin-top: 1mm; font-weight: bold; }
"""
    corpo = "\n".join([segnapunti, squadre, record, fronte, retro, fronte, retro, fronte, retro, fronte, retro])
    scrivi("schede.html", pagina_html("Atletica Strampalata - Schede", css, corpo))


# ------------------------------------------------------------ gettoni
def gettone(classe, titolo, sotto="", disegno=""):
    return f'<div class="gettone {classe}">{disegno}<div class="g-t">{titolo}</div><div class="g-s">{sotto}</div></div>'


BORRACCIA = ('<svg viewBox="0 0 20 30" class="dis"><rect x="7" y="1" width="6" height="4" rx="1" fill="#fff"/>'
             '<rect x="4" y="5" width="12" height="23" rx="4" fill="#fff"/><rect x="4" y="13" width="12" height="7" fill="#9fd4ff"/></svg>')
FULMINE = '<svg viewBox="0 0 20 30" class="dis"><path d="M12 1 L3 17 L9 17 L7 29 L17 11 L11 11 Z" fill="#1f2a33"/></svg>'
BANANA = ('<svg viewBox="0 0 40 30" class="dis larga"><path d="M4 8 C8 26 30 28 37 14 C30 20 14 20 9 6 Z" fill="#fff36b" '
          'stroke="#8a6a00" stroke-width="1.4"/><path d="M4 8 L2 5" stroke="#5b3d00" stroke-width="2.4"/></svg>')
POZZA = ('<svg viewBox="0 0 40 30" class="dis larga"><path d="M6 15 C2 8 14 4 20 7 C26 3 38 7 34 15 C39 21 28 27 20 23 '
         'C12 28 1 22 6 15 Z" fill="#7fc4ff" stroke="#fff" stroke-width="1.4"/></svg>')


def genera_gettoni():
    lista = []
    lista += [gettone("borraccia", "BORRACCIA", "Fiato · Concentrazione", BORRACCIA)] * 50
    lista += [gettone("grinta", "GRINTA", "+1 Fiato o Concentr.", FULMINE.replace("#1f2a33", "#fff"))] * 40
    for _ in range(8):
        lista += [gettone("fulmine", "FULMINE", "+3 · falsa con 1-2"), gettone("pronto", "PRONTO", "+1 · falsa con 1"),
                  gettone("prudente", "PRUDENTE", "nessun rischio")]
    lista += [gettone("banana", "BANANA", "si scivola!", BANANA)] * 3
    lista += [gettone("pozza", "POZZANGHERA", "−2 Fiato", POZZA)] * 2
    lista += [gettone("giallo", "CARTELLINO", "falsa partenza", '<div class="cartellino"></div>')] * 8
    lista += [gettone("oro", "1°", "ORO")] * 10 + [gettone("argento", "2°", "ARGENTO")] * 10 + [gettone("bronzo", "3°", "BRONZO")] * 10
    lista += [gettone("turbo", "TURBO", "variante Junior")] * 8
    pagine = []
    for i in range(0, len(lista), 88):
        pagine.append(f'<div class="pagina vert"><div class="griglia-g">{"".join(lista[i:i + 88])}</div>'
                      f'<div class="nota">Gettoni · stampa al 100 % su cartoncino e ritaglia (diametro 22 mm)</div></div>')

    colori = ["#e63946", "#f4a261", "#ffd23f", "#2a9d8f", "#2f6fd1", "#6a3fb5", "#ff70a6", "#1f2a33"]
    sagoma = ('<svg viewBox="0 0 24 24" class="omino"><circle cx="13" cy="4.5" r="2.6" fill="#fff"/>'
              '<path d="M12 8 L8 13 L4 13 M12 8 L15 13 L19 14 M12 8 L11 15 L14 21 M11 15 L7 21" stroke="#fff" '
              'stroke-width="2.6" fill="none" stroke-linecap="round"/></svg>')
    pedine = "".join(f"""<div class="pedina" style="--c:{c}">
  <div class="aletta">incolla</div><div class="faccia capovolta">{sagoma}<b>{i + 1}</b></div>
  <div class="faccia">{sagoma}<b>{i + 1}</b></div><div class="aletta">incolla</div></div>""" for i, c in enumerate(colori))
    pagine.append(f"""<div class="pagina vert pedine-pag">
  <h1>LE 8 PEDINE ATLETA</h1>
  <p>Ritaglia ogni striscia. Piegala a metà tra le due figure (sarà la cima), poi piega le due alette verso l'interno
  e incollale una sull'altra: la pedina sta in piedi da sola, come una tenda. Il numero è la corsia di partenza consigliata.</p>
  <div class="fila">{pedine}</div></div>""")

    css = """
@page { size: A4 portrait; margin: 0; }
.vert { width: 210mm; height: 297mm; display: flex; align-items: center; justify-content: center; }
.griglia-g { display: grid; grid-template-columns: repeat(8, 24mm); grid-auto-rows: 24mm; place-items: center; }
.nota { position: absolute; bottom: 5mm; left: 0; right: 0; text-align: center; font-size: 7pt; color: #888; }
.gettone { width: 22mm; height: 22mm; border-radius: 50%; border: .3mm solid #888; display: flex; flex-direction: column;
           align-items: center; justify-content: center; text-align: center; color: #fff; overflow: hidden; }
.g-t { font-size: 6pt; font-weight: bold; letter-spacing: .2mm; }
.g-s { font-size: 4.3pt; line-height: 1.1; padding: 0 2mm; opacity: .95; }
.dis { width: 7mm; height: 9mm; margin-bottom: .3mm; }
.dis.larga { width: 11mm; height: 8mm; }
.borraccia { background: #2f6fd1; }
.grinta { background: #c8553d; }
.fulmine { background: #ffd23f; color: #1f2a33; }
.fulmine .g-t { font-size: 7pt; }
.pronto { background: #2e8b57; }
.pronto .g-t { font-size: 7pt; }
.prudente { background: #8a949c; }
.prudente .g-t { font-size: 7pt; }
.banana { background: #6b4f1d; }
.pozza { background: #1d5d8a; }
.giallo { background: #333; }
.cartellino { width: 6mm; height: 8mm; background: #ffd23f; border-radius: .6mm; transform: rotate(-10deg); margin-bottom: .6mm; }
.oro, .argento, .bronzo { color: #1f2a33; border-width: .8mm; }
.oro { background: radial-gradient(circle, #ffe680, #d4a017); border-color: #a07800; }
.argento { background: radial-gradient(circle, #f2f2f2, #a9b0b6); border-color: #7c858c; }
.bronzo { background: radial-gradient(circle, #f0b98a, #b26b34); border-color: #7d4a22; }
.oro .g-t, .argento .g-t, .bronzo .g-t { font-size: 13pt; }
.turbo { background: #ff7b00; }
.turbo .g-t { font-size: 7.5pt; }
.pedine-pag { flex-direction: column; padding: 15mm; justify-content: flex-start; }
.pedine-pag h1 { font-size: 16pt; color: #c8553d; }
.pedine-pag p { font-size: 9pt; margin: 3mm 0 8mm; line-height: 1.35; text-align: center; }
.fila { display: flex; gap: 2mm; }
.pedina { width: 22mm; display: flex; flex-direction: column; }
.faccia { height: 34mm; background: var(--c); border: .3mm solid #666; border-top: .3mm dashed #333;
          display: flex; flex-direction: column; align-items: center; justify-content: center; color: #fff; }
.faccia b { font-size: 16pt; }
.capovolta { transform: rotate(180deg); }
.omino { width: 15mm; height: 15mm; }
.aletta { height: 14mm; border: .3mm dashed #333; display: flex; align-items: center; justify-content: center;
          font-size: 6pt; color: #888; background: #f3f3f3; }
"""
    scrivi("gettoni.html", pagina_html("Atletica Strampalata - Gettoni", css, "\n".join(pagine)))


# ------------------------------------------------------------ plancia
def genera_plancia_formati():
    rapporto = PLANCIA_W / PLANCIA_H
    for nome, (fw, fh) in {"A2": (594, 420), "A3": (420, 297)}.items():
        h = fh - 20
        w = min(fw - 20, h * rapporto)
        h = w / rapporto
        css = f"""@page {{ size: {fw}mm {fh}mm; margin: 0; }}
.foglio {{ width: {fw}mm; height: {fh}mm; display: flex; align-items: center; justify-content: center; }}
img {{ width: {w:.1f}mm; height: {h:.1f}mm; }}"""
        corpo = f'<div class="pagina foglio"><img src="{PLANCIA_REL}" alt="Plancia"></div>'
        scrivi(f"plancia-{nome}.html", pagina_html(f"Plancia {nome}", css, corpo))

    # 4 fogli A4 orizzontali: la plancia è divisa in 2 x 2 riquadri
    tile_h = 190.0
    tot_h = tile_h * 2
    tot_w = tot_h * rapporto
    tile_w = tot_w / 2
    nomi = {(0, 0): "in alto a sinistra", (1, 0): "in alto a destra", (0, 1): "in basso a sinistra", (1, 1): "in basso a destra"}
    pagine = []
    for n, (c, r) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1)), start=1):
        lati = {"destra": c == 0, "sinistra": c == 1, "basso": r == 0, "alto": r == 1}
        linee = "".join(f'<div class="taglio {k}"></div>' for k, v in lati.items() if v)
        pagine.append(f"""<div class="pagina foglio">
  <div class="contenitore"><div class="riquadro"><img src="{PLANCIA_REL}" style="left:{-c * tile_w:.2f}mm; top:{-r * tile_h:.2f}mm"></div>{linee}</div>
  <div class="etichetta">Foglio {n} di 4 · {nomi[(c, r)]} · ritaglia sulle linee rosse e unisci con nastro adesivo sul retro</div>
</div>""")
    css = f"""@page {{ size: A4 landscape; margin: 0; }}
.foglio {{ width: 297mm; height: 210mm; display: flex; align-items: center; justify-content: center; }}
.riquadro {{ width: {tile_w:.2f}mm; height: {tile_h:.2f}mm; overflow: hidden; position: relative; outline: .2mm solid #ccc; }}
.riquadro img {{ position: absolute; width: {tot_w:.2f}mm; height: {tot_h:.2f}mm; }}
.contenitore {{ position: relative; }}
.taglio {{ position: absolute; background: #e00; }}
.taglio.destra {{ right: -.2mm; top: -6mm; bottom: -6mm; width: .4mm; }}
.taglio.sinistra {{ left: -.2mm; top: -6mm; bottom: -6mm; width: .4mm; }}
.taglio.basso {{ bottom: -.2mm; left: -6mm; right: -6mm; height: .4mm; }}
.taglio.alto {{ top: -.2mm; left: -6mm; right: -6mm; height: .4mm; }}
.etichetta {{ position: absolute; bottom: 4mm; left: 0; right: 0; text-align: center; font-size: 8pt; color: #666; }}"""
    scrivi("plancia-A4-4fogli.html", pagina_html("Plancia su 4 fogli A4", css, "\n".join(pagine)))


if __name__ == "__main__":
    genera_carte()
    genera_schede()
    genera_gettoni()
    genera_plancia_formati()
