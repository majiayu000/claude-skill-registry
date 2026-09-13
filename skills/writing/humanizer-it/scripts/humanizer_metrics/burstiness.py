"""Ritmo e tipografia: ciò che la skill ordina di misurare per dispersione.

Copre i punti della checklist «variabilità della lunghezza delle frasi — non la
media, ma la DISPERSIONE» e «zero trattini lunghi». La burstiness qui è un proxy
statistico, non il detector stesso: alta dispersione delle lunghezze di frase
correla con la scrittura umana (SKILL.md, «Cosa colgono i detector»).
"""

from __future__ import annotations

import re
import statistics
from dataclasses import dataclass

from .segmentation import sentenize, word_count


@dataclass
class RhythmStats:
    sentences: int
    words: int
    mean_len: float          # lunghezza media della frase in parole
    stdev_len: float         # deviazione standard della lunghezza
    cv_len: float            # coefficiente di variazione = stdev/mean (indicatore principale)
    min_len: int
    max_len: int
    short_share: float       # quota di frasi < 5 parole
    long_share: float        # quota di frasi > 25 parole
    em_dash: int             # trattini lunghi «—»
    ellipsis: int            # punti di sospensione
    parentheses: int         # incisi tra parentesi
    questions: int           # frasi interrogative

    def as_dict(self) -> dict:
        return self.__dict__.copy()


def rhythm(text: str) -> RhythmStats:
    sents = sentenize(text)
    lengths = [word_count(s) for s in sents]
    lengths = [n for n in lengths if n > 0]
    n = len(lengths)
    total_words = sum(lengths)

    mean = statistics.mean(lengths) if lengths else 0.0
    stdev = statistics.pstdev(lengths) if n > 1 else 0.0
    cv = (stdev / mean) if mean else 0.0

    return RhythmStats(
        sentences=n,
        words=total_words,
        mean_len=round(mean, 1),
        stdev_len=round(stdev, 1),
        cv_len=round(cv, 3),
        min_len=min(lengths) if lengths else 0,
        max_len=max(lengths) if lengths else 0,
        short_share=round(sum(1 for x in lengths if x < 5) / n, 3) if n else 0.0,
        long_share=round(sum(1 for x in lengths if x > 25) / n, 3) if n else 0.0,
        em_dash=text.count("—"),
        ellipsis=text.count("…") + len(re.findall(r"\.\.\.", text)),
        parentheses=text.count("("),
        questions=sum(1 for s in sents if s.rstrip().endswith("?")),
    )


# Soglie euristiche (da ri-calibrare sull'italiano, vedi eval/RESULTS.md).
# cv_len < 0.35 = ritmo troppo piatto, indizio IA. Il testo umano di solito > 0.45.
CV_AI_THRESHOLD = 0.35
CV_HUMAN_TARGET = 0.45


def rhythm_verdict(s: RhythmStats) -> str:
    if s.em_dash > 0:
        dash = f"⚠ {s.em_dash} em-dashes (norm 0)"
    else:
        dash = "✓ dashes clean"
    if s.cv_len < CV_AI_THRESHOLD:
        rhythm_v = f"⚠ flat rhythm (CV={s.cv_len}, target ≥{CV_HUMAN_TARGET})"
    else:
        rhythm_v = f"✓ varied rhythm (CV={s.cv_len})"
    return f"{rhythm_v}; {dash}"
