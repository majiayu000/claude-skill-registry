"""Marcatori lessicali del testo IA: HARD BANS e scanner rapido (italiano).

Le wordlist sono estratte uno-a-uno da SKILL.md (sezioni «Ban assoluti» e
«Scanner rapido: parole-marcatore dell'IA»). È la metà deterministica e
grep-abile della modalità «Audit»: ciò che non richiede un LLM. La semantica
(calchi, ironia, translationese) qui NON viene colta per principio: per quella
serve la skill stessa.

Fonte di verità = SKILL.md. Aggiornando ban/marcatori, modifica entrambi i file;
scripts/lint_skill.py verifica che gli elenchi non divergano per numero di voci.

Calibrazione fondata su CORPUS-MARKERS-IT (25.06.2026): il nucleo ✅ è misurato
su fonti italiane; lo strato candidato (calchi dall'inglese ancora da validare
con un madrelingua) sta nello scanner, non nei ban assoluti — così un singolo
calco plausibile non fa fallire il testo.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# --- HARD BANS -----------------------------------------------------------
# Costrutti a divieto assoluto. Ognuno è (nome, regex). Regex
# case-insensitive, sulle forme flesse dove è sicuro.
#
# Criterio di inclusione: solo costrutti multi-parola ad alta specificità e
# basso tasso di falsi positivi, ✅ misurati su fonti italiane (vedi
# CORPUS-MARKERS-IT §1 «Nucleo» e §4). I connettivi singoli (inoltre, tuttavia…)
# NON sono ban: sono parole italiane normali, il segnale lo dà la DENSITÀ —
# stanno nello scanner.
HARD_BANS: list[tuple[str, str]] = [
    # Parallelismo negativo — la firma GPT più forte (Pangram + Esposito:
    # 3-4 su 300 parole = «radar IA»). Calco di «not only… but also».
    ("Non solo X, ma anche Y", r"\bnon\s+solo\b[^.!?]{1,60}?\b(ma|bensì)\s+anche\b"),
    ("Non si tratta (solo) di X, ma di Y",
     r"\bnon\s+si\s+tratta\b[^.!?]{1,60}?\b(ma|bensì)\b"),
    # Richiede la virgola: il parallelismo retorico la usa («Non è un costo, è
    # un investimento»). Senza virgola si evitano falsi positivi su frasi di
    # coordinazione («non è qui ma è arrivato»).
    ("Non è X, (ma) è Y", r"\bnon\s+è\b[^.!?]{1,40},\s*(ma\s+)?è\b"),
    # «gioca/svolge un ruolo cruciale/fondamentale/chiave» — calco di
    # «plays a crucial role».
    ("Gioca/svolge un ruolo cruciale/fondamentale/chiave",
     r"\b(gioc|svolg)\w+\s+un\s+ruolo\s+(cruciale|fondamentale|chiave|centrale|importante|decisivo)\b"),
    # Conclusioni formulaiche — marcatore top, solo a inizio frase/clausola.
    ("In conclusione / In sintesi / In definitiva / Per concludere / Riassumendo",
     r"(?:^|[.!?…:;]\s+)\s*(in\s+conclusione|in\s+sintesi|in\s+definitiva|per\s+concludere|riassumendo|tirando\s+le\s+somme)\b"),
    # «Transizioni vuote» metatestuali, documentate (navigaweb).
    ("È importante notare/sottolineare che",
     r"\bè\s+importante\s+(notare|sottolineare|ricordare|evidenziare)\s+che\b"),
    ("Va notato/detto/sottolineato che",
     r"\bva\s+(notato|detto|sottolineato|ricordato|evidenziato)\s+che\b"),
    ("È interessante notare che", r"\bè\s+interessante\s+notare\s+che\b"),
    ("Vale la pena ricordare/sottolineare/notare",
     r"\bvale\s+la\s+pena\s+(di\s+)?(ricordare|sottolineare|notare|evidenziare|menzionare)\b"),
    # Trattino lungo (em-dash): in italiano nativo è raro, quindi sospetto —
    # marcatore PIÙ forte che in inglese (navigaweb, geopop, aranzulla).
    ("Trattino lungo (em-dash «—»)", r"—"),
    # Calco «harness/unlock the (full) potential».
    ("Sfruttare/sbloccare il (pieno) potenziale",
     r"\b(sfrutta\w+|sblocca\w+|liberare?)\s+(il\s+|tutto\s+il\s+)?(pieno\s+)?potenziale\b"),
    # Apertura vuota #1 (calco «in today's world / in the digital age»).
    ("Nel mondo di oggi / Nell'era digitale / Al giorno d'oggi",
     r"\b(nel\s+mondo\s+di\s+oggi|nell['’]era\s+digitale|al\s+giorno\s+d['’]oggi|ai\s+giorni\s+nostri)\b"),
    # Variante apertura vuota: «in un mondo/contesto/scenario sempre più …».
    ("In un mondo/contesto/scenario sempre più …",
     r"\bin\s+un\s+(mondo|contesto|scenario|panorama|mercato)\s+sempre\s+più\b"),
    # Cliché motivazionale (calco «take it to the next level»).
    ("Portare al livello successivo / al prossimo livello",
     r"\b(portare|porta|portano|spingere|spinge)\s+[^.!?]{0,30}?\bal\s+(livello\s+successivo|prossimo\s+livello)\b"),
    # Timbro marketing a informatività nulla (calco «open new horizons»).
    ("Aprire nuovi orizzonti / scenari / prospettive",
     r"\b(apr\w+|spalanca\w+|dischiud\w+)\s+(nuov\w+\s+)?(orizzont\w+|scenari\w*|prospettiv\w+|possibilità)\b"),
]

# --- Scanner rapido: categorie di parole-marcatore ----------------------
# Valori = frasi per ricerca sottostringa (case-insensitive). Alcune sono
# radici, per catturare le forme flesse. Una voce con prefisso "re:" è
# trattata come regex; le altre come sottostringa letterale.
SCANNER: dict[str, list[str]] = {
    # Sovraccarico di connettivi: parole italiane normali, il segnale è la
    # DENSITÀ + regolarità posizionale (fastweb, navigaweb, aranzulla).
    "Connectives": [
        "inoltre", "tuttavia", "pertanto", "di conseguenza", "dunque",
        "quindi", "infatti", "ciononostante", "nondimeno",
    ],
    # Calchi strutturali / translationese (Treccani «IA-taliano»; De Cesare
    # «impronte algoritmiche dell'inglese»).
    "Calques/Translationese": [
        "basato su", "basati su", "in termini di", "a livello di",
        "quando si tratta di", "d'altra parte", "dall'altra parte",
        "in tal senso", "in questo senso", "al fine di",
    ],
    # Inflazione / aggettivi abusati (hwupgrade, fastweb, Pangram).
    "Inflation": [
        "cruciale", "fondamentale", "rivoluzionari", "innovativ",
        "all'avanguardia", "senza precedenti", "di vitale importanza",
        "di fondamentale importanza", "straordinari", "imprescindibil",
    ],
    # Aperture vuote (calchi «in today's world»). Strato candidato ⚠️.
    "Empty-openings": [
        "nel mondo di oggi", "nell'era digitale", "al giorno d'oggi",
        "nel panorama attuale", "nel panorama", "nello scenario",
        "non è un segreto che", "nell'odierno", "ai giorni nostri",
    ],
    # Artefatti chatbot — strato candidato (calchi dall'inglese, §2.D).
    "Chatbot": [
        "ottima domanda", "certamente!", "spero che questo ti sia utile",
        "spero ti sia utile", "sono qui per aiutarti",
        "fammi sapere se hai bisogno", "come modello di intelligenza artificiale",
        "in qualità di ia", "in quanto ia", "non esitare a chiedere",
        "con piacere!",
    ],
    # Calchi motivazionali (esplorare/delve, harness, navigate, journey —
    # top Pangram, navigaweb, Max Planck).
    "Motivational-calques": [
        "esplorare", "approfondire", "addentrarsi", "navigare nel",
        "navigare attraverso", "un viaggio alla scoperta",
        "portare al livello successivo", "al prossimo livello",
        "spingersi oltre", "abbracciare il", "intraprendere un viaggio",
    ],
    # Formule-conclusioni (anche fuori posizione iniziale → qui per densità).
    "Conclusion-formulas": [
        "in conclusione", "in sintesi", "in definitiva", "per concludere",
        "riassumendo", "in breve", "tirando le somme", "per riassumere",
    ],
    # Contestualizzatori.
    "Contextualizers": [
        "in un contesto", "alla luce di", "sullo sfondo di",
        "tenendo conto", "considerando", "tenuto conto", "alla luce delle",
    ],
    # Soluzioni-marketing (hwupgrade).
    "Marketing-solutions": [
        "soluzione completa", "soluzione efficace", "soluzione su misura",
        "soluzione chiavi in mano", "approccio olistico",
        "approccio su misura", "soluzioni innovative", "valore aggiunto",
    ],
    # Falsi amici / calchi semantici (it.wikipedia, Terminologia etc.) +
    # tecno-anglicismi. A semantic calque: the wrong sense borrowed from English.
    "False-friends": [
        "eventualmente", "attualmente", "implementare", "performante",
        "supportare", "processare", "omittare", "evidenze", "asset",
        "deliverable", "committment", "schedulare", "triggerare",
    ],
    # Hedge modali.
    "Modal-hedges": [
        "può rappresentare", "può contribuire", "potrebbe essere utile",
        "è in grado di", "mira a", "si propone di", "permette di",
        "consente di ottenere",
    ],
    # Calchi col gerundio (superficial -ing analyses: «evidenziando come…»).
    "Gerund-calques": [
        "evidenziando come", "sottolineando l'importanza", "dimostrando che",
        "permettendo di", "garantendo che", "offrendo un", "rendendolo",
    ],
    # Parallelismi (sottostringhe per misurare la DENSITÀ del costrutto;
    # i ban assoluti sopra colpiscono la forma completa).
    "Parallelisms": ["non solo", "non si tratta", "non è tanto"],
    # Truismi autorevoli.
    "Truisms": [
        "è importante ricordare che", "alla fine dei conti", "in fin dei conti",
        "per sua natura", "a tutti gli effetti", "in ultima analisi",
    ],
    # Decoro a emoji.
    "Emoji-decor": ["⚡", "✨", "🎯", "🔥", "💡", "🚀"],
    # Tracce tecniche di copia dall'interfaccia del chatbot. Indizi univoci:
    # in un testo umano non compaiono. LINGUISTICAMENTE NEUTRE — identiche al
    # RU, tenute verbatim. Prefisso "re:" = regex, il resto = sottostringa.
    "Copy-paste-artifacts": [
        ":contentReference", "oai_citation", "utm_source=chatgpt.com",
        "utm_source=openai", "grok_card://", "attached_file://",
        "vertexaisearch.cloud.google.com/grounding-api-redirect",
        "](sandbox:/mnt/data/", "attributableIndex",
        r"re:oaicite:\d+",
        r"re:turn\d+(?:search|fetch|file)\d+",          # turnNsearchN e simili
        r"re:citeturn\d+[a-z]+\d+",                     # etichetta-citazione unita
        r"re:【\d+(?::\d+)?†source】",                    # OpenAI Assistants
        r"re:\[citation:\d+\]",                         # stile Perplexity
        r"re:[\ue200-\ue204]",                       # separatori-citazione invisibili ChatGPT
        r"re:</?think>",                                # residui di reasoning DeepSeek ecc.
    ],
}

# Suffissi di nominalizzazioni deverbali (stile nominale / burocratese) che la
# skill ordina di riaprire in verbi. Misurati in morphology.py.
NOMINALIZATION_SUFFIXES = ("zione", "zioni", "mento", "menti", "ità", "aggio", "anza", "enza")


@dataclass
class MarkerHit:
    category: str
    marker: str
    count: int
    positions: list[int] = field(default_factory=list)


def _find_all(text: str, needle_regex: str) -> list[int]:
    return [m.start() for m in re.finditer(needle_regex, text, re.IGNORECASE)]


def scan_hard_bans(text: str) -> list[MarkerHit]:
    """Trova i costrutti dei HARD BANS. Qualsiasi occorrenza = fallimento."""
    hits: list[MarkerHit] = []
    for name, pat in HARD_BANS:
        pos = _find_all(text, pat)
        if pos:
            hits.append(MarkerHit("HARD BAN", name, len(pos), pos))
    return hits


def scan_markers(text: str) -> list[MarkerHit]:
    """Esegue le categorie dello scanner rapido. Ritorna solo le occorrenze.

    Una voce col prefisso "re:" è trattata come espressione regolare,
    le altre come sottostringa letterale (case-insensitive).
    """
    hits: list[MarkerHit] = []
    for cat, phrases in SCANNER.items():
        for phrase in phrases:
            pat = phrase[3:] if phrase.startswith("re:") else re.escape(phrase)
            pos = _find_all(text, pat)
            if pos:
                hits.append(MarkerHit(cat, phrase.removeprefix("re:"), len(pos), pos))
    return hits


def marker_verdict(marker_hits: list[MarkerHit]) -> str:
    """Scale from SKILL.md: 0-2 clean, 3-5 suspicious, 6+ AI.
    A copy-paste artifact = unambiguous evidence: immediate verdict, off-scale."""
    if any(h.category == "Copy-paste-artifacts" for h in marker_hits):
        return "copy-paste artifacts from a chatbot: text pasted from an AI response"
    total = sum(h.count for h in marker_hits)
    if total <= 2:
        return f"{total} — probably clean text"
    if total <= 5:
        return f"{total} — suspicious"
    return f"{total} — AI generation highly likely"
