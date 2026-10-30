# 🏃 ATLETICA STRAMPALATA

**Il gioco da tavolo dell'atletica leggera — con dadi, carte e bucce di banana.**
1-8 giocatori · 8-100 anni · da 10 minuti (gara secca) a 2 ore (decathlon)

![La plancia di gioco](plancia.svg)

## Le 10 discipline

| Corse (sull'anello o sul rettilineo) | Concorsi (sul campo) |
|---|---|
| 100 m · 200 m · 400 m · 800 m | Salto in lungo · Salto in alto |
| 110 m ostacoli · 400 m ostacoli | Getto del peso · Lancio del giavellotto |

## Il gioco in 30 secondi

- **Tiri sempre 3 dadi, ma scegli quali tenere.** Al *Passo* ne tieni 1 (e recuperi Fiato e peschi una carta), di *Corsa* 2, in *Scatto* tutti e 3 (ma costa Fiato). Così decidi dove atterrare: evitare un ostacolo, prendere una stella, fare un doppio.
- **Combinazioni di dadi**: il doppio tenuto è una *Falcata Perfetta* (peschi una carta), il tris è *In Trance*, il tris di 1 un *Crampo Comico*, la scala 1-2-3 un *Inciampo*…
- **Il Fiato è poco**: quando scatti? Nei 400 m l'acido lattico rende lo scatto finale più caro, negli 800 m conta stare in scia.
- **Concorsi "rischia o fermati"**: nel lungo spingi la rincorsa senza superare l'asse, nel peso scegli quante rotazioni (dadi) fare sapendo che un 1 è nullo, nel giavellotto dividi i dadi tra Forza e Angolo, nell'alto decidi quali altezze passare.
- **Carte Scarpetta** per aiutarti (*Scarpe a Molla*, *Calzino Portafortuna*…), per fare dispetti (*Buccia di Banana*, *Megafono Sbagliato*, *Piccione Ladro*…) o per difenderti (*Occhio di Falco*, *Specchio Riflettente*).
- **Carte Stadio** e **Meteo** per imprevisti e condizioni di gara: la mascotte che ti abbraccia, il fotografo, il cane invasore, l'acquazzone.

## Modalità

Gara secca · Meeting (2-5 discipline) · **Decathlon** (tutti in tutte e 10, con i gettoni Grinta da dosare) · **A squadre** (mercato delle discipline e allenatori a bordo pista) · Solitario contro i Record dello Stadio · Variante Junior e Nonni & Nipoti.

## File

| File | Contenuto |
|---|---|
| [`REGOLAMENTO.md`](REGOLAMENTO.md) | Regolamento completo, modalità, personaggi, strategia, scheda segnapunti |
| [`CARTE.md`](CARTE.md) | Tutte le 84 carte (Scarpetta, Stadio, Meteo) con effetti e testi |
| [`plancia.svg`](plancia.svg) | La plancia stampabile (1800 × 1420, vettoriale: si stampa in qualunque formato) |
| [`strumenti/genera_plancia.py`](strumenti/genera_plancia.py) | Script che rigenera la plancia (`python3 strumenti/genera_plancia.py`) |
| [`stampabili/`](stampabili/) | **Stampa e gioca**: plancia in PDF (A2, A3 o 4 fogli A4), 84 carte + 8 carte Atleta con i dorsi, segnapunti, Record dello Stadio, schede giocatore, gettoni e pedine da piegare |
| [`strumenti/genera_stampabili.py`](strumenti/genera_stampabili.py) + [`strumenti/stampa_pdf.js`](strumenti/stampa_pdf.js) | Rigenerano i materiali stampabili leggendo `CARTE.md` e `REGOLAMENTO.md` (servono Python 3 e Node con Playwright) |

## Stampa e gioca

1. Stampa la plancia: `stampabili/plancia-A2.pdf` in copisteria, oppure `stampabili/plancia-A4-4fogli.pdf` a casa (4 fogli da unire).
2. Stampa `stampabili/carte.pdf` (meglio su cartoncino) e ritaglia le carte; i dorsi sono nelle ultime 4 pagine.
3. Stampa `stampabili/gettoni.pdf` e `stampabili/schede.pdf`.
4. Procurati 4 dadi e una matita. Tutto al 100 % ("dimensioni effettive"), mai "adatta alla pagina".

Le istruzioni complete sono nella sezione 2.1 del regolamento.
