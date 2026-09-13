"""humanizer_metrics — deterministic metrics of text liveliness.

This is the greppable half of SKILL.md's "Audit" mode: what is computed by a
machine, not by the LLM. It serves as a local boost for Claude Code, as the
engine of the eval harness (eval/run_eval.py), and as the skill's own self-test
(scripts/lint_skill.py).

Semantics (calques, irony, translationese, voice) are not caught here — that
needs the skill itself. The scripts don't run in the claude.ai web UI; the skill
does not depend on them.
"""

from __future__ import annotations

from dataclasses import dataclass

from .burstiness import RhythmStats, rhythm, rhythm_verdict
from .markers import (
    MarkerHit,
    marker_verdict,
    scan_hard_bans,
    scan_markers,
)
from .morphology import MorphStats, morph_stats, morph_verdict
from .structure import StructureStats, structure_stats, structure_verdict
from .score import ScoreResult, cleanliness_score

__all__ = [
    "Report",
    "analyze",
    "RhythmStats",
    "MorphStats",
    "StructureStats",
    "MarkerHit",
    "ScoreResult",
    "cleanliness_score",
    "rhythm",
    "morph_stats",
    "structure_stats",
    "scan_hard_bans",
    "scan_markers",
]


@dataclass
class Report:
    hard_bans: list[MarkerHit]
    markers: list[MarkerHit]
    rhythm: RhythmStats
    morph: MorphStats
    structure: StructureStats

    @property
    def hard_ban_count(self) -> int:
        return sum(h.count for h in self.hard_bans)

    @property
    def marker_count(self) -> int:
        return sum(h.count for h in self.markers)

    def as_dict(self) -> dict:
        return {
            "hard_ban_count": self.hard_ban_count,
            "hard_bans": [(h.marker, h.count) for h in self.hard_bans],
            "marker_count": self.marker_count,
            "markers": [(h.category, h.marker, h.count) for h in self.markers],
            "rhythm": self.rhythm.as_dict(),
            "morph": self.morph.as_dict(),
            "structure": self.structure.as_dict(),
        }


def analyze(text: str) -> Report:
    """Full deterministic run over a text."""
    return Report(
        hard_bans=scan_hard_bans(text),
        markers=scan_markers(text),
        rhythm=rhythm(text),
        morph=morph_stats(text),
        structure=structure_stats(text),
    )
