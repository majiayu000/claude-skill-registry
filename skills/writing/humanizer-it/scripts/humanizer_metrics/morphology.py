"""Morfosintassi italiana: nominalizzazioni, pro-drop, clitici ci/ne.

Sostituisce la metrica RU «rapporto sostantivi/verbi» (pymorphy3) con i
marcatori che CORPUS-MARKERS-IT §2.E indica come specifici dell'italiano e
rilevabili senza POS-tagger, a regex pura (zero dipendenze):

1. Stile nominale / burocratese: densità di nominalizzazioni deverbali
   (-zione, -mento, -ità, -aggio, -anza/-enza). L'IA-taliano abusa del nome
   astratto dove il madrelingua userebbe un verbo (Treccani: «stile nominale»).
2. Pro-drop: l'italiano è lingua a soggetto nullo come il russo. L'IA inserisce
   pronomi soggetto ridondanti (io/tu/lui/lei/noi/voi/loro), calco del soggetto
   obbligatorio inglese. Densità alta = sospetto.
3. Clitici ci/ne: l'IA li SOTTO-usa (`vale la pena` invece di `ne vale la pena`).
   Conteggio basso su testo lungo = segnale (verdetto informativo, non punitivo:
   l'assenza è ambigua).

NB: soglie ancora da calibrare sul corpus A/B (DeSegMa/Profiling-UD, vedi
HANDOFF «sonda di misura»). Finché non sono misurate, sono euristiche dichiarate.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Parola italiana: lettere (con accentate) ed eventuale apostrofo interno (l'IA).
_WORD_RE = re.compile(r"[A-Za-zÀ-ÿ]+(?:['’][A-Za-zÀ-ÿ]+)?")

# Suffissi di nominalizzazioni deverbali (stile nominale). Tenuti ordinati per
# lunghezza decrescente per il match della radice.
_NOMINAL_SUFFIXES = ("zione", "zioni", "mento", "menti", "aggio", "anza", "enza", "ità")

# Pronomi soggetto tonici. `io/tu/noi/voi` sono inequivoci; `lui/lei/loro/egli/
# ella/esso/essa` pure come soggetto. NB: `lei` è anche allocutivo di cortesia,
# `loro` anche possessivo — euristica, non parsing.
_SUBJECT_PRONOUNS = {"io", "tu", "lui", "lei", "noi", "voi", "loro", "egli", "ella", "esso", "essa"}

# Clitici-spia del «vivo» italiano (ci/ne). Conteggio come parole intere.
_CLITICS = {"ci", "ne", "ce"}


@dataclass
class MorphStats:
    words: int
    nominalizations: int       # sostantivi deverbali (potenziale burocratese)
    nominal_ratio: float       # nominalizzazioni / parole
    subject_pronouns: int      # pronomi soggetto tonici ridondanti (pro-drop)
    pronoun_per_100w: float    # densità pronomi soggetto per 100 parole
    clitics_ci_ne: int         # occorrenze di ci/ne/ce (sotto-uso = spia)

    def as_dict(self) -> dict:
        return self.__dict__.copy()


def _words(text: str) -> list[str]:
    return [m.group(0).lower() for m in _WORD_RE.finditer(text)]


def morph_stats(text: str) -> MorphStats:
    words = _words(text)
    total = len(words)
    nominal = sum(1 for w in words if len(w) >= 6 and w.endswith(_NOMINAL_SUFFIXES))
    subj = sum(1 for w in words if w in _SUBJECT_PRONOUNS)
    clit = sum(1 for w in words if w in _CLITICS)

    nominal_ratio = (nominal / total) if total else 0.0
    pron_100 = (subj / total * 100) if total else 0.0

    return MorphStats(
        words=total,
        nominalizations=nominal,
        nominal_ratio=round(nominal_ratio, 3),
        subject_pronouns=subj,
        pronoun_per_100w=round(pron_100, 2),
        clitics_ci_ne=clit,
    )


# Soglie euristiche (da ri-calibrare sul corpus, vedi docstring).
NOMINAL_RATIO_TARGET = 0.07     # >7% di nominalizzazioni = stile nominale sospetto
PRONOUN_100_TARGET = 2.5        # >2.5 pronomi soggetto / 100 parole = pro-drop violato
CLITIC_MIN_PER_300W = 1         # meno di così su testo lungo = sotto-uso clitici


def morph_verdict(s: MorphStats) -> str:
    parts: list[str] = []

    if s.nominal_ratio > NOMINAL_RATIO_TARGET:
        parts.append(
            f"⚠ nominal style ({int(s.nominal_ratio*100)}% nominalizations, "
            f"target ≤{int(NOMINAL_RATIO_TARGET*100)}%; {s.nominalizations} cases)"
        )
    else:
        parts.append(f"✓ nominalizations {int(s.nominal_ratio*100)}% (≤{int(NOMINAL_RATIO_TARGET*100)}%)")

    if s.pronoun_per_100w > PRONOUN_100_TARGET:
        parts.append(
            f"⚠ redundant subject pronouns ({s.pronoun_per_100w}/100 words, "
            f"target ≤{PRONOUN_100_TARGET}; pro-drop violated)"
        )
    else:
        parts.append(f"✓ pro-drop ok ({s.pronoun_per_100w} pron./100 words)")

    # Clitic under-use: informative only on long-enough text.
    if s.words >= 300 and s.clitics_ci_ne < CLITIC_MIN_PER_300W * (s.words // 300):
        parts.append(f"⚠ clitics ci/ne under-used ({s.clitics_ci_ne}) — «dry» text")

    return "; ".join(parts)
