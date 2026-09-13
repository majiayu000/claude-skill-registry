"""Metriche strutturali a livello di documento: burstiness dei paragrafi e firma «listicle».

Completa burstiness.py (lì il ritmo delle FRASI) con ciò che i detector valutano
a LIVELLO DI DOCUMENTO: paragrafi tutti della stessa lunghezza ed elenchi
ripetitivi tradiscono la generazione a stampo, anche quando ogni singola frase è
stata ripulita.

Questi segnali colpiscono il testo multi-sezione / listicle (post, guide). Sulla
prosa in blocco unico restano inerti (pochi paragrafi, niente elenchi) e non
portano penalità nello score, quindi non toccano la calibrazione del corpus.
"""

from __future__ import annotations

import re
import statistics
from dataclasses import dataclass

from .segmentation import sentenize

# Riga-voce di elenco: marcatore «- * •» oppure «1. / 1)» a inizio riga.
_LIST_RE = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+\S")


@dataclass
class StructureStats:
    paragraphs: int          # numero di paragrafi non vuoti (separatore = riga vuota)
    para_mean_sent: float    # lunghezza media del paragrafo in frasi
    para_cv: float           # coefficiente di variazione delle lunghezze (burstiness paragrafi)
    list_items: int          # righe-voce di elenco
    listicle_share: float    # quota di righe-voce tra le righe non vuote

    def as_dict(self) -> dict:
        return self.__dict__.copy()


def structure_stats(text: str) -> StructureStats:
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    sent_lens = [len(sentenize(p)) for p in paras]
    sent_lens = [n for n in sent_lens if n > 0]
    n = len(sent_lens)

    mean = statistics.mean(sent_lens) if sent_lens else 0.0
    stdev = statistics.pstdev(sent_lens) if n > 1 else 0.0
    cv = (stdev / mean) if mean else 0.0

    lines = [ln for ln in text.splitlines() if ln.strip()]
    list_items = sum(1 for ln in lines if _LIST_RE.match(ln))
    share = (list_items / len(lines)) if lines else 0.0

    return StructureStats(
        paragraphs=n,
        para_mean_sent=round(mean, 1),
        para_cv=round(cv, 3),
        list_items=list_items,
        listicle_share=round(share, 3),
    )


# Soglie (euristica, coerente con la logica di burstiness.py per le frasi).
# Scattano solo su testo abbastanza lungo/strutturato, per non penalizzare la
# prosa breve di uno-due paragrafi.
PARA_CV_AI = 0.35          # sotto = paragrafi troppo uniformi per lunghezza
PARA_MIN_COUNT = 6         # su pochi paragrafi corti il cv è inaffidabile (campione
                           # piccolo): giudichiamo il ritmo dei paragrafi solo su testo lungo
LISTICLE_SHARE_AI = 0.30   # quota di righe-voce superiore = testo «listicle»
LISTICLE_MIN_ITEMS = 6     # e non meno di tante voci (soglia di stampo)


def structure_verdict(s: StructureStats) -> str:
    parts = []
    if s.paragraphs >= PARA_MIN_COUNT and s.para_cv < PARA_CV_AI:
        parts.append(f"⚠ uniform paragraphs (CV={s.para_cv}, target ≥{PARA_CV_AI})")
    else:
        parts.append(f"✓ paragraphs: {s.paragraphs}, CV={s.para_cv}")
    if s.list_items >= LISTICLE_MIN_ITEMS and s.listicle_share > LISTICLE_SHARE_AI:
        parts.append(f"⚠ listicle ({s.list_items} items, {int(s.listicle_share*100)}% of lines)")
    elif s.list_items:
        parts.append(f"list items: {s.list_items}")
    return "; ".join(parts)
