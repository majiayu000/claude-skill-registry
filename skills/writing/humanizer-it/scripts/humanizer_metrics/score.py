"""Score di pulizia: comprime i segnali deterministici in un solo numero 0-100.

Più alto = il testo si legge più vivo/umano. NON è un detector e NON è una
probabilità di IA: è solo un aggregato di metriche già calcolate (hard ban,
marcatori, ritmo, morfosintassi), restituito come feedback «prima/dopo». Si
appoggia alle soglie già definite in burstiness/morphology e documentate in
eval/RESULTS.md.

Le soglie delle penalità vanno ri-tarate sul corpus italiano A/B (human →
score alto, raw-IA → basso, humanized → in mezzo). Run di calibrazione:
vedi eval/run_eval.py.
"""

from __future__ import annotations

from dataclasses import dataclass

from .burstiness import CV_HUMAN_TARGET
from .morphology import NOMINAL_RATIO_TARGET, PRONOUN_100_TARGET
from .structure import (
    LISTICLE_MIN_ITEMS,
    LISTICLE_SHARE_AI,
    PARA_CV_AI,
    PARA_MIN_COUNT,
)

# Il trattino lungo è un caso a parte: è insieme hard ban e segnale a densità.
# In italiano nativo è raro, ma in citazioni/dialoghi può comparire: nello score
# non lo tagliamo col tetto, lo penalizziamo per densità con tolleranza. Il nome
# deve coincidere con quello in HARD_BANS di markers.py.
EM_DASH_NAME = "Trattino lungo (em-dash «—»)"
COPY_PASTE_CATEGORY = "Copy-paste-artifacts"

# Fasce. Coincidono con le soglie di intervento di SKILL.md.
BAND_CLEAN = 85   # ≥ — le tracce IA non danno fastidio, non intervenire
BAND_EDIT = 60    # ≥ — ritocco mirato; < — riscrittura completa


@dataclass
class ScoreResult:
    score: int                       # 0-100, higher = cleaner
    band: str                        # "clean" | "edit" | "rewrite"
    penalties: list[tuple[str, int]]  # (reason, -points) — the verbose report

    def as_dict(self) -> dict:
        return {
            "score": self.score,
            "band": self.band,
            "penalties": [{"reason": r, "points": p} for r, p in self.penalties],
        }


def _band(score: float) -> str:
    if score >= BAND_CLEAN:
        return "clean"
    if score >= BAND_EDIT:
        return "edit"
    return "rewrite"


def _per100(count: int, words: int) -> float:
    return (count / words * 100) if words else 0.0


def cleanliness_score(report) -> ScoreResult:
    """Calcola lo score 0-100 da un Report già pronto (vedi humanizer_metrics.analyze)."""
    words = report.rhythm.words or 1
    penalties: list[tuple[str, int]] = []
    score = 100.0

    # 1. Phrasal hard bans (em-dash excluded). Unambiguous AI constructs: costly.
    hard_phrase = sum(h.count for h in report.hard_bans if h.marker != EM_DASH_NAME)
    if hard_phrase:
        pen = min(45, 12 * hard_phrase)
        score -= pen
        penalties.append((f"hard bans (phrasal): {hard_phrase}", -pen))

    # 2. Copy-paste artifacts from the chatbot: text literally pasted from an AI response.
    copy_paste = sum(h.count for h in report.markers if h.category == COPY_PASTE_CATEGORY)
    if copy_paste:
        pen = 60
        score -= pen
        penalties.append((f"copy-paste artifacts: {copy_paste}", -pen))

    # 3. Soft markers (copy-paste excluded) by density per 100 words.
    soft = sum(h.count for h in report.markers if h.category != COPY_PASTE_CATEGORY)
    if soft:
        pen = min(30, round(2 * _per100(soft, words)))
        if pen:
            score -= pen
            penalties.append((f"markers: {soft} ({_per100(soft, words):.1f}/100 words)", -pen))

    # 4. Em-dash by density with a ~2-per-100-words tolerance. Weak signal.
    dash_density = _per100(report.rhythm.em_dash, words)
    if dash_density > 2.0:
        pen = min(8, round(3 * (dash_density - 2.0)))
        if pen:
            score -= pen
            penalties.append((f"em-dashes: {report.rhythm.em_dash} ({dash_density:.1f}/100 words)", -pen))

    # 5. Flat rhythm: the lower the CV vs the 0.45 target, the higher the penalty.
    cv = report.rhythm.cv_len
    if report.rhythm.sentences >= 4 and cv < CV_HUMAN_TARGET:
        pen = min(20, round((CV_HUMAN_TARGET - cv) / CV_HUMAN_TARGET * 30))
        if pen:
            score -= pen
            penalties.append((f"flat rhythm (CV={cv}, target ≥{CV_HUMAN_TARGET})", -pen))

    # 6. Nominal style: nominalization density above target = burocratese.
    #    Weak signal and the prime false-positive source (legal/scientific
    #    register is legitimately nominal), so a light, low-capped penalty.
    nr = report.morph.nominal_ratio
    if nr > NOMINAL_RATIO_TARGET:
        pen = min(8, round((nr - NOMINAL_RATIO_TARGET) / 0.02 * 3))
        if pen:
            score -= pen
            penalties.append((f"nominal style ({int(nr*100)}% nominalizations, target ≤{int(NOMINAL_RATIO_TARGET*100)}%)", -pen))

    # 7. Pro-drop violated: redundant tonic subject pronouns (calque of English).
    #    Italian-specific (CORPUS-MARKERS §2.E). Weak signal, well capped.
    pron = report.morph.pronoun_per_100w
    if report.rhythm.sentences >= 4 and pron > PRONOUN_100_TARGET:
        pen = min(8, round((pron - PRONOUN_100_TARGET) * 2))
        if pen:
            score -= pen
            penalties.append((f"pro-drop violated ({pron} pron./100 words, target ≤{PRONOUN_100_TARGET})", -pen))

    # 8. Document-level: paragraphs uniform in length (paragraph burstiness).
    #    Fires only on text with enough paragraphs, otherwise inert (short prose).
    st = report.structure
    if st.paragraphs >= PARA_MIN_COUNT and st.para_cv < PARA_CV_AI:
        pen = min(10, round((PARA_CV_AI - st.para_cv) / PARA_CV_AI * 20))
        if pen:
            score -= pen
            penalties.append((f"uniform paragraphs (CV={st.para_cv}, target ≥{PARA_CV_AI})", -pen))

    # 9. Document-level: listicle signature (abundance of identical items). Inert on
    #    prose without lists, hits templated guides/posts.
    if st.list_items >= LISTICLE_MIN_ITEMS and st.listicle_share > LISTICLE_SHARE_AI:
        pen = min(12, round((st.listicle_share - LISTICLE_SHARE_AI) * 30))
        if pen:
            score -= pen
            penalties.append((f"listicle ({st.list_items} items, {int(st.listicle_share*100)}% of lines)", -pen))

    final = max(0, min(100, round(score)))
    return ScoreResult(score=final, band=_band(final), penalties=penalties)
