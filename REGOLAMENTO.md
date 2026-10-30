# ATLETICA STRAMPALATA — Regolamento

> *Il gioco da tavolo dell'atletica leggera in cui vince il più forte… o quello che ha lanciato la buccia di banana al momento giusto.*

| | |
|---|---|
| **Giocatori** | da 1 a 8 (in solitario si sfida il Record dello Stadio) |
| **Età** | da 8 a 100 anni |
| **Durata** | gara secca 10-15 min · meeting 40-60 min · decathlon 2 ore (anche in due "giornate") |
| **Tipo** | gioco di corsa e di gestione delle risorse, con carte, dadi e molte risate |

---

## Indice

1. [Lo spirito del gioco](#1-lo-spirito-del-gioco)
2. [Contenuto della scatola](#2-contenuto-della-scatola)
3. [La plancia](#3-la-plancia)
4. [I concetti base](#4-i-concetti-base)
5. [Le corse (100, 200, 400, 800, 110 hs, 400 hs)](#5-le-corse)
6. [I concorsi (lungo, alto, peso, giavellotto)](#6-i-concorsi)
7. [Le carte](#7-le-carte)
8. [Punteggi e classifiche](#8-punteggi-e-classifiche)
9. [Le modalità di gioco](#9-le-modalità-di-gioco)
10. [Gli atleti (personaggi opzionali)](#10-gli-atleti-personaggi-opzionali)
11. [Variante Junior (8-10 anni o prima partita)](#11-variante-junior)
12. [Consigli dell'allenatore (strategia)](#12-consigli-dellallenatore)
13. [Scheda segnapunti](#13-scheda-segnapunti)

---

## 1. Lo spirito del gioco

*Atletica Strampalata* porta sul tavolo le dieci discipline più amate dell'atletica leggera. Ogni gara è breve, ma piena di decisioni:

- **quanto spingere** (il Fiato è poco: lo usi adesso o lo tieni per il rettilineo finale?);
- **quali dadi tenere** (tiri sempre 3 dadi, ma ne usi solo alcuni: puoi evitare un ostacolo, finire su una stella o fare un doppio);
- **quando giocare le carte** (una buccia di banana lanciata troppo presto si schiva, una lanciata al momento giusto è leggenda);
- **quanto rischiare** nei concorsi (ancora un passo di rincorsa o rischi il nullo?).

La fortuna c'è, come nello sport vero, ma chi gestisce bene Fiato, dadi e carte vince molto più spesso.

**Regola d'oro dello Stadio:** le carte buffe vanno lette ad alta voce e *interpretate*. Se una carta dice di urlare "Ciao mamma!", lo si urla.

---

## 2. Contenuto della scatola

| Componente | Quantità | A cosa serve |
|---|---|---|
| Plancia dello stadio | 1 | anello, rettilineo di velocità, pedane dei concorsi (vedi `plancia.svg`) |
| Pedine atleta | 8 (8 colori) | i corridori/saltatori/lanciatori |
| Dadi a sei facce | 4 bianchi | 3 per le corse e quasi tutti i concorsi, il 4° per il peso |
| Carte **Scarpetta** | 60 | la mano del giocatore: Facilitazioni (verdi), Dispetti (rossi), Difese (blu) |
| Carte **Stadio** | 16 | imprevisti pescati sulle caselle ★ |
| Carte **Meteo** | 8 | le condizioni di ogni disciplina |
| Carte **Atleta** | 8 | personaggi con un'abilità speciale (opzionali) |
| Segnalini **Borraccia** | 50 | rappresentano Fiato (nelle corse) e Concentrazione (nei concorsi) |
| Gettoni **Grinta** | 40 | riserva di energia per il decathlon (5 a giocatore) |
| Gettoni **Reazione** | 24 | per ogni giocatore: Fulmine, Pronto, Prudente |
| Segnalini **Buccia di Banana** | 3 | si piazzano sulla pista |
| Segnalini **Pozzanghera** | 2 | si piazzano sulla pista |
| Cartellini gialli | 8 | per le false partenze |
| Medaglie (oro, argento, bronzo) | 10 per tipo | premiazioni |
| Blocco segnapunti + matita | 1 | punteggi, misure e Record dello Stadio |

### 2.1 Versione "stampa e gioca"

Tutto il materiale si può stampare a casa dalla cartella [`stampabili/`](stampabili/):

| File | Cosa contiene | Come stamparlo |
|---|---|---|
| `plancia-A2.pdf` / `plancia-A3.pdf` | la plancia su un unico foglio | in copisteria (A2 consigliato) o su stampante A3 |
| `plancia-A4-4fogli.pdf` | la plancia divisa su 4 fogli A4 | stampa al 100 % ("dimensioni effettive"), ritaglia lungo le linee e unisci con nastro adesivo sul retro |
| `carte.pdf` | le 84 carte e le 8 carte Atleta (63 × 88 mm, formato standard) | A4 al 100 %; i dorsi sono nelle ultime pagine (vedi sotto) |
| `schede.pdf` | segnapunti, Record dello Stadio, schede giocatore con promemoria | A4 al 100 % |
| `gettoni.pdf` | Borracce, Grinta, Reazione, banane, pozzanghere, cartellini, medaglie, gettoni Turbo e le 8 pedine da piegare | A4 al 100 %, meglio su cartoncino |

**I dorsi delle carte.** Ogni mazzo comincia su una pagina nuova. Per avere i dorsi stampa, sul retro di ogni pagina, la pagina-dorso del suo mazzo (Scarpetta, Stadio, Meteo o Atleta); in alternativa incolla fronte e retro, oppure usa delle bustine protettive con un cartoncino colorato dietro. Se non ti interessano i dorsi, usa semplicemente il colore della fascia per distinguere i mazzi.

Servono inoltre **4 dadi a sei facce** e una matita. Le pagine HTML da cui sono generati i PDF sono in `stampabili/html/` e si rigenerano con `python3 strumenti/genera_stampabili.py` seguito da `node strumenti/stampa_pdf.js`.

---

## 3. La plancia

La plancia (file `plancia.svg`, rigenerabile con `strumenti/genera_plancia.py`) ha tre zone.

### 3.1 L'Anello (200 m, 400 m, 400 m hs, 800 m)
- 8 corsie, **40 caselle per giro**: ogni casella vale **10 metri**.
- Le caselle delle corsie esterne sono più larghe: la "scaglionatura" è già compensata, quindi **tutti partono e arrivano sulla stessa linea**.
- Si corre in senso antiorario, con il campo alla propria sinistra.
- **Linea d'arrivo** (a scacchi): è anche la partenza di 400, 400 hs e 800. La pedina parte *sulla linea* (casella 0); muovendo di 1 entra nella casella 1.
- **Partenza 200 m**: linea bianca all'inizio della curva sinistra (fine casella 20). Si corrono le caselle 21-40.
- **Linea di rientro 800 m** (tratteggiata azzurra, fine casella 10).
- **Ostacoli dei 400 hs**: caselle 5, 8, 12, 15, 19, 22, 26, 29, 33, 36 (valgono solo nei 400 hs).
- **Caselle ★ Stadio**: 3, 17, 24, 31.

### 3.2 Il Rettilineo di Velocità (100 m e 110 m hs)
- 8 corsie, **22 caselle**: qui ogni casella vale **5 metri** (la velocità pura merita più dettaglio).
- **110 hs**: si parte dai blocchi bianchi prima della casella 1 e si corrono 22 caselle (110 m).
- **100 m**: la pedina parte *sulla casella 2* (linea gialla) e si corrono 20 caselle (100 m).
- **Ostacoli dei 110 hs**: caselle 3, 5, 7, 9, 11, 12, 14, 16, 18, 20.
- **Caselle ★ Stadio**: 6 e 15.

### 3.3 Il Campo (concorsi)
- **Salto in lungo**: rincorsa di 12 caselle, asse di battuta, buca di sabbia, formula della misura.
- **Salto in alto**: materasso e scala delle altezze con il tiro minimo richiesto.
- **Getto del peso**: pedana e settore con le misure da 14 a 24 m.
- **Giavellotto**: pedana di rincorsa e settore con le misure fino a 96 m.

In basso trovi quattro promemoria: Ritmo, Combinazioni, Caselle speciali, Punti.

---

## 4. I concetti base

### 4.1 Tiri sempre 3 dadi
In quasi tutto il gioco si tirano **3 dadi** e poi si **sceglie** quali tenere. La scelta è il cuore strategico del gioco: tenere i due dadi più alti non è sempre la mossa migliore (magari ti fanno fermare su un ostacolo, o rinunci a un doppio che ti farebbe pescare una carta).

### 4.2 Fiato e Concentrazione (Borracce)
- Nelle **corse** le Borracce sono **Fiato**: servono per scattare.
- Nei **concorsi** le Borracce sono **Concentrazione**: 1 Concentrazione = **ritirare un dado a scelta** (una volta per dado, il nuovo risultato vale).
- Non si possono avere più di **8 Borracce**. Il Fiato e la Concentrazione avanzati **si perdono** a fine disciplina.

### 4.3 La mano di carte
- All'inizio della partita ogni giocatore pesca **2 carte Scarpetta**; all'inizio di ogni disciplina ne pesca **1**.
- Limite di mano: **3 carte** (se ne hai di più, scarti subito quelle in eccesso).
- Nel tuo turno puoi giocare **al massimo 1 carta** Facilitazione o Dispetto. Le carte **Difesa** si giocano in qualsiasi momento, anche fuori dal tuo turno.

### 4.4 Il round
Si gioca a **round**: in ogni round ogni atleta fa un turno, nell'ordine delle corsie (corsia 1, poi 2, ecc.). Questo garantisce che tutti abbiano lo stesso numero di turni: è decisivo negli arrivi al fotofinish.

### 4.5 Preparazione della partita
1. Apri la plancia al centro del tavolo e metti accanto i 4 dadi e la riserva di Borracce (la "banca").
2. Mescola separatamente i mazzi **Scarpetta**, **Stadio** e **Meteo** e mettili coperti vicino alla plancia.
3. Ogni giocatore sceglie un colore, prende la pedina, una **scheda giocatore** e i 3 gettoni **Reazione**. Se usate i personaggi (sezione 10), ognuno sceglie o pesca una carta **Atleta**.
4. Ogni giocatore pesca **2 carte Scarpetta**.
5. Scegliete la modalità (sezione 9) e scrivete i nomi sul **segnapunti**. Nel decathlon ognuno prende **5 gettoni Grinta**.
6. Lo **starter** è il giocatore più giovane: dà il via alle corse e legge le carte Meteo.

### 4.6 Quanti dadi si tirano: riepilogo

| Situazione | Dadi tirati | Dadi tenuti |
|---|---|---|
| Corsa — Passo / Corsa / Scatto | 3 | 1 / 2 / 3 |
| Partenza dai blocchi | 1 | — |
| Ostacolo (se ti fermi sopra) | 1 | — |
| Lungo — rincorsa, poi accelerazione e volo | 3, poi 1 alla volta, poi 1 | 2, poi tutti |
| Alto | 3 | 2 |
| Peso | da 1 a 4, a scelta | tutti |
| Giavellotto | 3 | 1 Angolo + 2 Forza |

---

## 5. Le corse

### 5.1 Preparazione
1. Si gira la prima carta **Meteo**: vale per tutta la gara.
2. Ogni giocatore pesca 1 carta Scarpetta.
3. Si assegnano le corsie: nella prima gara a caso; nelle successive **chi è in testa alla classifica sceglie per ultimo** (le corsie centrali 3-6 non hanno vantaggi meccanici, ma il primo a muovere vede meno degli altri: l'ultimo a muovere sa esattamente cosa deve fare).
4. Ogni atleta riceve il **Fiato iniziale**:

| Gara | Caselle | Fiato iniziale | Note |
|---|---|---|---|
| 100 m | 20 (rettilineo) | 2 | |
| 110 m hs | 22 (rettilineo) | 2 | 10 ostacoli |
| 200 m | 20 (anello) | 3 | |
| 400 m | 40 (anello) | 4 | acido lattico nelle ultime 10 caselle |
| 400 m hs | 40 (anello) | 4 | 10 ostacoli + acido lattico |
| 800 m | 80 (2 giri) | 4 | rientro, scia, sorpassi |

### 5.2 La partenza: i blocchi
1. Ogni giocatore sceglie **in segreto** un gettone Reazione e lo tiene chiuso nel pugno.
2. Lo starter (il giocatore più giovane) dice: *"Ai vostri posti… pronti…"* e tutti aprono il pugno al *"VIA!"*.
3. Ognuno tira **1 dado**:

| Reazione | Falsa partenza se esce | Altrimenti |
|---|---|---|
| **Fulmine** | 1 o 2 | avanza subito di **3** caselle |
| **Pronto** | 1 | avanza subito di **1** casella |
| **Prudente** | mai | resta sui blocchi |

**Falsa partenza**: l'atleta prende un **cartellino giallo**, resta sui blocchi e nel primo turno può muovere solo al **Passo**. Un secondo cartellino giallo nella *stessa* disciplina (possibile solo per effetto di carte) significa **squalifica** dalla gara: l'atleta diventa **Tifoso** (vedi 5.9).

> Negli 800 m, gara lunga, la partenza è più tranquilla: chi sceglie Fulmine avanza di 2 invece che di 3.

### 5.3 Il turno di corsa
1. **Carta** (facoltativa): giochi al massimo 1 carta Facilitazione o Dispetto.
2. **Ritmo**: dichiari il ritmo *prima* di tirare.
3. **Tiro**: tiri **3 dadi**.
4. **Scelta**: tieni i dadi permessi dal ritmo e muovi della loro somma.
5. **Casella**: risolvi l'effetto della casella d'arrivo (★, ostacolo, banana, pozzanghera).
6. **Combinazioni**: applichi eventuali combinazioni (vedi 5.4).

| Ritmo | Dadi tenuti | Costo | Bonus |
|---|---|---|---|
| **Passo** | 1 a scelta | — | **+1 Fiato** e **peschi 1 carta** Scarpetta |
| **Corsa** | 2 a scelta | — | — |
| **Scatto** | tutti e 3 | **−2 Fiato** | — |

- Non puoi scattare se non hai abbastanza Fiato.
- **Acido lattico** (400 m e 400 hs): se *inizi* il turno nelle ultime 10 caselle (caselle 31-40), lo Scatto costa **3** Fiato.
- **Movimento obbligatorio**: la somma dei dadi tenuti va mossa tutta (salvo bucce e ingorghi che ti fermano prima). Non si può "frenare": per questo la scelta dei dadi conta.

### 5.4 Le combinazioni di dadi
Le combinazioni **sul tiro** guardano tutti e 3 i dadi tirati; quelle **sui dadi tenuti** solo quelli che hai scelto (quindi le puoi "cercare" o evitare).

| Combinazione | Dove si guarda | Nome | Effetto |
|---|---|---|---|
| Due dadi uguali tra quelli tenuti | dadi tenuti | **Falcata Perfetta** | peschi 1 carta Scarpetta |
| Tre dadi uguali (non 1) | tiro | **In Trance** | muovi la somma di **tutti e 3** i dadi **senza pagare Fiato**, qualunque ritmo avessi dichiarato, e peschi 1 carta |
| Tre 1 | tiro | **Crampo Comico** | non ti muovi; ti massaggi il polpaccio gemendo e recuperi **+2 Fiato** |
| 4-5-6 | tiro | **Vento in Poppa** | +1 Fiato |
| 1-2-3 | tiro | **Inciampo** | −1 Fiato (se ne hai) e dici "Ops!" |

- Le combinazioni **non si sommano**: un tris vale solo come *In Trance* (o *Crampo Comico*), non anche come *Falcata Perfetta*.
- Le combinazioni **sul tiro** si applicano anche se poi non tieni quei dadi.

> Esempio: dichiari Corsa e tiri 5-5-6. Tenendo 5+6 muovi di 11. Tenendo 5+5 muovi di 10 ma fai **Falcata Perfetta** e peschi una carta. A te la scelta!

### 5.5 Le caselle speciali
- **★ Stadio**: se **ti fermi** su una stella peschi una carta **Stadio** e la risolvi subito. Passarci sopra non ha effetto.
- **Ostacolo** (solo 110 hs e 400 hs): se **ti fermi** su una casella con ostacolo, tiri 1 dado:
  - **4-6** passaggio pulito, nessun effetto;
  - **2-3** ostacolo toccato: **DONG!** (va detto) e torni indietro di **1** casella;
  - **1** **Capitombolo**: torni indietro di **3** caselle e devi rialzarti (in piedi, davvero) prima del prossimo turno.
  Passare *sopra* un ostacolo senza fermarsi non ha effetto: per questo scegliere i dadi giusti è fondamentale.
- **Buccia di Banana** (segnalino): chi la **raggiunge o la supera** si ferma **sulla buccia**, scivola (rumore obbligatorio: "Uaaaah!"), toglie il segnalino e nel turno successivo può muovere solo al **Passo**.
- **Pozzanghera** (segnalino): chi **si ferma** sopra perde **2 Fiato** ("SPLASH!"). Il segnalino resta lì fino a fine gara.

### 5.6 Regole speciali dell'800 m
- **Corsia fino al rientro**: nel primo tratto (caselle 1-10) ognuno resta nella propria corsia.
- **Rientro**: dopo aver superato la linea di rientro, la pedina si sposta nelle corsie **1 o 2** (a scelta, se libere) e ci resta fino all'arrivo.
- **Ingorgo**: in ogni casella possono stare al massimo **2 atleti** (uno in corsia 1, uno in corsia 2). Se la casella in cui finiresti è piena, ti fermi nella prima casella libera precedente.
- **Scia**: se finisci il movimento **esattamente una casella dietro** a un avversario (stessa corsia), recuperi **+1 Fiato**: stai risparmiando energie nella sua scia.
- **Campana**: quando il primo atleta passa la linea d'arrivo per la prima volta, lo starter suona la campana (o la imita: "DIN DIN DIN!") e **tutti** recuperano **+1 Fiato**.

### 5.7 L'arrivo e il fotofinish
- Un atleta che raggiunge o supera il traguardo ha finito: si segna **di quante caselle ha superato** l'arrivo (le caselle "di troppo" si contano immaginando che la pista continui).
- Gli atleti arrivati nello **stesso round** si classificano per caselle di troppo: più sono, meglio è.
- In caso di ulteriore parità: **fotofinish**, i giocatori a pari merito tirano 1 dado (chi fa di più vince; sorridere al fotografo è obbligatorio).
- La gara finisce quando sono arrivati tutti (o quando restano solo atleti caduti e Tifosi).

### 5.8 Dispetti e bersagli
- Un Dispetto si gioca nel proprio turno su **un atleta a scelta** in gara.
- I segnalini (banana, pozzanghera) si piazzano su una casella **libera**, nella corsia di un avversario, **da 1 a 6 caselle davanti a lui**.
- Nessuno può essere bersaglio di **più di un Dispetto per round**: il primo che lo colpisce "prenota" il bersaglio.

### 5.9 Tifosi
Un atleta squalificato o eliminato non smette di giocare: diventa **Tifoso** per il resto della disciplina. Nel proprio turno può:
- giocare **1 carta** (anche Facilitazioni su un altro atleta), *oppure*
- fare **la ola** e pescare 1 carta Scarpetta.

Così nessuno, nemmeno a 8 anni, resta a guardare.

### 5.10 Durata degli effetti
- Gli effetti "al prossimo turno" o "al prossimo tiro" valgono **una sola volta** e **scadono a fine disciplina** se non sono stati usati.
- I segnalini Banana e Pozzanghera si tolgono dalla plancia alla fine della gara.
- Se due effetti si contraddicono (per esempio "devi tenere i dadi più bassi" e "scegli tu quali dadi tiene"), vale quello giocato **per ultimo**.

---

## 6. I concorsi

Nei concorsi ogni atleta ha **3 tentativi** (nell'alto valgono regole proprie). Si gioca a round: tutti fanno il 1° tentativo, poi tutti il 2°, poi tutti il 3°. Vale **la misura migliore**.

- **Concentrazione iniziale**: **2 Borracce** (3 nel salto in alto). Ogni Borraccia spesa permette di ritirare un dado.
- Prima di ogni tentativo puoi giocare 1 carta.
- **Doppio 6** tra i dadi tirati: oltre al resto, peschi 1 carta **Stadio** (il pubblico impazzisce).
- La misura di un tentativo **nullo** non conta.

### 6.1 Salto in lungo — "Fin dove ti spingi?"
È una sfida di nervi alla *"ancora una carta?"*.
1. **Rincorsa**: tiri **3 dadi**, ne tieni **2** e metti la pedina sulla casella di rincorsa pari alla somma.
2. **Accelerazione**: puoi tirare **1 dado** e avanzare di quel numero, quante volte vuoi. Se superi la casella **12** (l'asse di battuta) il salto è **NULLO** ("piede oltre l'asse: faccia nella plastilina!").
3. **Stacco**: quando decidi di fermarti, la casella raggiunta è il valore di **Rincorsa** (da 2 a 12).
4. **Volo**: tiri **1 dado** (puoi usare la Concentrazione per ritirarlo).
5. **Misura** = **4 m + (Rincorsa + Volo) × 0,25 m**.

La Concentrazione si può usare su **qualsiasi** dado del salto: sui due della rincorsa, su un dado di accelerazione che ti farebbe superare l'asse, o sul volo.

| Rincorsa + Volo | 8 | 10 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|
| Misura | 6,00 | 6,50 | 7,00 | 7,25 | 7,50 | 7,75 | 8,00 | 8,25 | 8,50 |

**Combinazioni**: un **doppio** tra i dadi della rincorsa è uno **Stacco Perfetto** (+0,25 m).

### 6.2 Salto in alto — "Fosbury o figuraccia"
1. Ogni atleta dichiara l'**altezza d'ingresso** (si può partire anche da 2,00 m o più).
2. Per superare l'asticella tiri **3 dadi** e tieni i **2** migliori: la somma deve raggiungere il **tiro minimo** dell'altezza.

| Altezza | 1,80 | 1,90 | 2,00 | 2,10 | 2,20 | 2,30 | 2,40 | 2,45 |
|---|---|---|---|---|---|---|---|---|
| Tiro minimo | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 12* |

\* a 2,45 m (il record del mondo!) **non** si può usare la Concentrazione.

3. **Doppio tenuto** = **Fosbury Perfetto**: +1 alla somma.
4. Ad ogni altezza hai fino a **3 tentativi**. Puoi **passare** un'altezza (e risparmiare tentativi), ma attenzione: **3 errori consecutivi**, anche su altezze diverse, e sei **eliminato** (diventi Tifoso).
5. La gara prosegue finché resta un solo atleta, che può continuare a salire finché vuole (e finché non sbaglia 3 volte).
6. **Parità**: vince chi ha fatto meno errori all'ultima altezza superata; poi chi ha fatto meno errori in totale.

### 6.3 Getto del peso — "Quanti giri fai?"
1. Scegli quante **rotazioni** fare: tiri da **1 a 4 dadi**.
2. Se esce anche un solo **1** il lancio è **NULLO** ("il peso ti è caduto sul piede / sei uscito dalla pedana"). Puoi usare la Concentrazione per ritirare gli 1.
3. **Misura** = **12 m + (somma dei dadi) × 0,5 m**.

| Dadi | Probabilità di lancio valido | Misura media se valido |
|---|---|---|
| 1 | 83 % | 14 m |
| 2 | 69 % | 16 m |
| 3 | 58 % | 18 m |
| 4 | 48 % | 20 m (massimo 24 m) |

Più rotazioni = più potenza, ma più rischio. Con tre tentativi conviene… dipende da cosa hanno fatto gli altri!

### 6.4 Lancio del giavellotto — "Forza e angolo"
1. Tiri **3 dadi**.
2. **Assegni** 1 dado all'**Angolo** e gli altri 2 alla **Forza** (somma).
3. **Misura** = **Forza × 8 m × fattore Angolo**.

| Dado Angolo | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Fattore | **NULLO** | ×0,7 | ×0,9 | **×1,0** | ×0,9 | ×0,6 |
| Cosa succede | piantato nell'erba a due metri (vicino al piede del giudice) | rasoterra | buono | **angolo perfetto** | buono | dritto verso la luna |

> Esempio: tiri 6-6-1. Se metti l'1 sull'Angolo è nullo. Se metti un 6 sull'Angolo: Forza 7 × 8 × 0,6 = 33,6 m. Brutto, ma almeno è valido… oppure usi una Concentrazione per ritirare l'1!

Arrotonda le misure al decimetro per difetto.

---

## 7. Le carte

L'elenco completo, con effetti e testi umoristici, è nel file [`CARTE.md`](CARTE.md).

### 7.1 Carte Scarpetta (60) — la tua mano
- **Facilitazioni (verdi, 26)**: aiutano te (Scarpe a Molla, Bibita alla Carota, Calzino Portafortuna…).
- **Dispetti (rossi, 24)**: ostacolano un avversario (Buccia di Banana, Gomma da Masticare, Megafono Sbagliato…).
- **Difese (blu, 10)**: si giocano in **qualsiasi momento** per annullare o rimandare un Dispetto (Occhio di Falco, Specchio Riflettente…).

Molte carte hanno un effetto diverso per **Corsa** e per **Concorso**: è scritto sulla carta.

### 7.2 Carte Stadio (16) — gli imprevisti
Si pescano quando ci si **ferma su una ★** o con un **doppio 6** in un concorso. Si risolvono subito e si scartano.

### 7.3 Carte Meteo (8) — le condizioni di gara
Se ne gira una all'inizio di **ogni disciplina**: vale per tutti fino alla fine di quella disciplina.

### 7.4 Mazzi esauriti
Quando un mazzo finisce, si rimescolano gli scarti.

---

## 8. Punteggi e classifiche

### 8.1 Punti per piazzamento (ogni disciplina)

| Posizione | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° |
|---|---|---|---|---|---|---|---|---|
| Punti | 10 | 8 | 6 | 5 | 4 | 3 | 2 | 1 |

- Chi non ha nessuna misura valida, è squalificato o eliminato al primo tentativo: **0 punti**.
- Nei concorsi le parità di misura si risolvono con la **seconda miglior misura**, poi con un dado.
- I primi tre ricevono le **medaglie** (oro, argento, bronzo) e salgono sul podio: è consentito, anzi consigliato, cantare l'inno.

### 8.2 Record dello Stadio
Sul blocco segnapunti c'è una tabella dei **Record dello Stadio**, che restano da una partita all'altra.

| Disciplina | Come si misura | Record di partenza |
|---|---|---|
| 100 / 110 hs / 200 / 400 / 400 hs / 800 | turni impiegati, poi caselle di troppo | 100: 2 turni · 110 hs: 3 · 200: 2 · 400: 4 · 400 hs: 5 · 800: 8 |
| Lungo | metri | 8,00 m |
| Alto | metri | 2,30 m |
| Peso | metri | 21,00 m |
| Giavellotto | metri | 85,0 m |

Chi **batte** un Record dello Stadio guadagna **+2 punti** e scrive il proprio nome sul blocco. Gloria eterna (o fino alla prossima partita).

### 8.3 Gioco in solitario
Si gioca una disciplina o un decathlon da soli, senza Dispetti (si scartano e si ripescano), cercando di battere i Record dello Stadio. Ogni record battuto vale una medaglia d'oro: quante ne porti a casa in un decathlon?

---

## 9. Le modalità di gioco

### 9.1 Gara Secca (1 disciplina · 10-15 min)
Si sceglie una disciplina, si gioca, si premia il podio. Perfetta per imparare o per una rivincita veloce.

### 9.2 Meeting (da 2 a 5 discipline · 30-60 min)
Si scelgono le discipline (o si pescano a caso). Si sommano i punti. Alcuni meeting consigliati:

| Meeting | Discipline | Per chi |
|---|---|---|
| **Sprint Party** | 100 m, 200 m, 110 hs | chi ama le partite rapidissime |
| **Triathlon della Domenica** | 100 m, Lungo, Peso | prima partita in famiglia |
| **Volare!** | Lungo, Alto, Giavellotto | chi ama il rischio |
| **Il Giro della Morte** | 400 m, 400 hs, 800 m | gli strateghi del Fiato |
| **Pentathlon Strampalato** | 110 hs, Lungo, Peso, Alto, 800 m | serata di gioco |

### 9.3 Decathlon (tutte e 10 · 2 ore, anche in due giornate)
Tutti i giocatori gareggiano in tutte le discipline, nell'ordine:

| | Giornata 1 | Giornata 2 |
|---|---|---|
| 1 | 100 m | 110 m hs |
| 2 | Salto in lungo | Giavellotto |
| 3 | Getto del peso | 200 m |
| 4 | Salto in alto | 400 m hs |
| 5 | 400 m | 800 m |

**Regole speciali del Decathlon:**
- **Gettoni Grinta**: ogni giocatore riceve **5 gettoni Grinta** per l'intero decathlon. All'inizio di una disciplina può spenderne **fino a 2**: ognuno vale **+1 Fiato** (corse) o **+1 Concentrazione** (concorsi). Gestirli bene è metà della vittoria: li bruci nei 100 m o li tieni per gli 800?
- **La mano si conserva** da una disciplina all'altra (sempre con limite 3).
- **Pausa tra le giornate**: alla fine della giornata 1 ognuno può scartare le carte che vuole e pescarne altrettante.
- Vince chi ha **più punti** alla fine delle 10 discipline. Parità: vince chi ha più medaglie d'oro, poi d'argento, poi di bronzo.

### 9.4 A squadre (da 4 a 8 giocatori)
Si formano **2, 3 o 4 squadre** (es. 2 squadre da 4, 4 squadre da 2, 2 squadre da 3…). Si gioca un decathlon o un meeting.

**1. Il mercato delle discipline.** Prima di iniziare, ogni squadra si riunisce (anche in segreto, nell'angolo del soggiorno) e **distribuisce le discipline** tra i propri membri, scrivendole sulla scheda:

| Componenti per squadra | Atleti per squadra in ogni disciplina | Posti da assegnare (decathlon) |
|---|---|---|
| 2 | 1 | 10 |
| 3 o 4 | 2 | 20 |

- Ogni membro deve gareggiare in **almeno 3 discipline** e in **non più di 7** (in un meeting: almeno 1).
- Con solo 2 o 3 atleti in pista, i punti sono comunque quelli della tabella 8.1 (10, 8, 6).
- Con i personaggi (sezione 10), assegnare le discipline giuste al personaggio giusto è la prima grande scelta strategica.

**2. Allenatori a bordo pista.** I membri della squadra che **non gareggiano** in una disciplina fanno gli **Allenatori**:
- possono **passare 1 carta** al proprio atleta in gara una volta per disciplina;
- possono giocare carte **Difesa** per proteggere un compagno;
- possono giocare **1 Dispetto per disciplina** contro gli avversari (gli allenatori sono notoriamente furbi).

**3. Punti di squadra.** La squadra somma i punti di tutti i suoi atleti.
- **Spirito di squadra**: a fine partita, se ogni membro della squadra ha vinto almeno una medaglia, la squadra guadagna **+5 punti**.
- **Inno della squadra** (facoltativo ma caldamente consigliato): ogni squadra si inventa un nome e un coro.

### 9.5 Tabella delle durate indicative

| Modalità | 2-3 giocatori | 4-6 giocatori | 7-8 giocatori |
|---|---|---|---|
| Gara secca | 5-10 min | 10 min | 15 min |
| Meeting (3 discipline) | 20 min | 35 min | 45 min |
| Decathlon | 75 min | 110 min | 140 min |

---

## 10. Gli atleti (personaggi opzionali)

Per partite più strategiche ogni giocatore sceglie (o pesca) una carta **Atleta**: ognuno ha un'abilità che lo rende più forte in alcune discipline. Nel decathlon nessuno è forte ovunque!

| Atleta | Specialità | Abilità |
|---|---|---|
| **Saetta Rossi** | Velocista | In partenza, con **Fulmine** fa falsa partenza solo con **1**. |
| **Nonna Pina** | Veterana ("ho corso nel '64, e senza scarpe") | Una volta per disciplina può **ritirare un dado** gratis. |
| **Bruno Bisonte** | Lanciatore | Peso: il primo **1** di ogni lancio si ritira gratis. Giavellotto: **+4 m**. |
| **Lola Libellula** | Saltatrice | Alto: **Fosbury Perfetto** vale **+2**. Lungo: il primo superamento dell'asse di **1** sola casella non è nullo (si ferma sull'asse). |
| **Prof. Ostacolo** | Ostacolista | Quando si ferma su un ostacolo tira **2 dadi** e tiene il migliore. |
| **Mara Mezzofondo** | Mezzofondista | **+2 Fiato** iniziale in 400, 400 hs e 800. |
| **Tobia Tartaruga** | Imperturbabile | **Immune** a banane e pozzanghere. Al Passo muove sempre almeno **4** caselle. |
| **Zeno Furbetto** | Stratega | Limite di mano **4** carte. A inizio disciplina pesca 2 carte e ne scarta 1. |

---

## 11. Variante Junior

Per i più piccoli (8-10 anni) o per la primissima partita:
- **Niente Fiato**: si corre sempre di **Corsa** (3 dadi, se ne tengono 2).
- Ogni atleta ha **1 gettone Turbo** per gara: lo spende per tenere tutti e 3 i dadi.
- Niente carte **Difesa** e niente **Megafono Sbagliato** (si tolgono dal mazzo).
- Nel lungo la rincorsa si ferma automaticamente a 12 (niente nullo per sorpasso dell'asse, ma la sabbia in faccia va comunque mimata).
- Le carte le legge ad alta voce il giocatore più grande al tavolo, con la voce dello speaker dello stadio.

E la **variante Nonni & Nipoti** per le famiglie: in squadra, un nonno e un nipote fanno coppia; il nonno sceglie i dadi, il nipote li tira e decide le carte da giocare.

---

## 12. Consigli dell'allenatore

1. **Il Fiato è tempo.** Nei 400 m lo Scatto nelle ultime 10 caselle costa 3: conviene spendere il Fiato *prima* del rettilineo finale.
2. **Guarda dove atterri.** Negli ostacoli, a volte tenere un 4 e un 2 è meglio che un 6 e un 5: arrivi oltre l'ostacolo senza fermartici sopra.
3. **Le stelle sono una scommessa.** Le carte Stadio sono in media leggermente positive, ma qualche volta ti tolgono una scarpa.
4. **Il Passo non è da pigri.** Una carta e un Fiato in più possono valere più di 3 caselle, soprattutto negli 800 m.
5. **Le banane si piazzano dove l'avversario non può evitarle**: subito davanti a lui (1-2 caselle) non è sempre il massimo, perché raramente si ferma prima; ma 5-6 caselle davanti, proprio dove la media dei dadi lo porta… *splat*.
6. **Una Difesa in mano scoraggia i dispetti.** Anche solo il sospetto che tu l'abbia funziona.
7. **Nel lungo conta il punteggio degli altri.** Se sei primo con 7,50 m, al terzo tentativo fermati presto. Se sei ultimo, rischia tutto!
8. **Nell'alto, passare un'altezza** è il modo migliore per arrivare fresco alle misure che contano.
9. **Nel decathlon pensa alla classifica generale**, non alla singola gara: un 4° posto sicuro vale spesso più di un oro rischioso.

---

## 13. Scheda segnapunti

La versione stampabile (con anche la tabella dei Record dello Stadio e la versione a squadre) è in [`stampabili/schede.pdf`](stampabili/schede.pdf). In alternativa copia questa tabella sul blocco (una colonna per giocatore o squadra).

| Disciplina | Giocatore 1 | Giocatore 2 | Giocatore 3 | Giocatore 4 | Giocatore 5 | Giocatore 6 | Giocatore 7 | Giocatore 8 |
|---|---|---|---|---|---|---|---|---|
| 100 m | | | | | | | | |
| Salto in lungo | | | | | | | | |
| Getto del peso | | | | | | | | |
| Salto in alto | | | | | | | | |
| 400 m | | | | | | | | |
| 110 m hs | | | | | | | | |
| Giavellotto | | | | | | | | |
| 200 m | | | | | | | | |
| 400 m hs | | | | | | | | |
| 800 m | | | | | | | | |
| Record (+2) | | | | | | | | |
| Spirito di squadra (+5) | | | | | | | | |
| **TOTALE** | | | | | | | | |
| Medaglie 🥇 / 🥈 / 🥉 | | | | | | | | |
| Gettoni Grinta rimasti | | | | | | | | |
