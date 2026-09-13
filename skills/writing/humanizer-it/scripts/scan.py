#!/usr/bin/env python3
"""Scanner CLI: passa il testo attraverso le metriche deterministiche di humanizer-it.

Uso (dalla radice del repo; per la skill installata il path è: <cartella skill>/scripts/scan.py):
    python skills/humanizer-it/scripts/scan.py path/to/text.txt
    echo "il tuo testo" | python skills/humanizer-it/scripts/scan.py -
    python skills/humanizer-it/scripts/scan.py text.txt --json

È la metà «macchina» della modalità «Audit». Per l'umanizzazione completa
(semantica, voce, riscrittura) serve la skill stessa: questo scanner evidenzia
solo i marcatori grep-abili e calcola le metriche che un LLM non sa misurare a
occhio. Zero dipendenze: gira col solo Python stdlib.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from humanizer_metrics import analyze, cleanliness_score
from humanizer_metrics.burstiness import rhythm_verdict
from humanizer_metrics.markers import marker_verdict
from humanizer_metrics.morphology import morph_verdict
from humanizer_metrics.structure import structure_verdict


def _read(src: str) -> str:
    if src == "-":
        return sys.stdin.read()
    return Path(src).read_text(encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Scanner deterministico di marcatori IA (humanizer-it)")
    ap.add_argument("source", help="file di testo oppure '-' per stdin")
    ap.add_argument("--json", action="store_true", help="output in JSON")
    args = ap.parse_args()

    text = _read(args.source)
    rep = analyze(text)
    sc = cleanliness_score(rep)

    if args.json:
        out = rep.as_dict()
        out["score"] = sc.as_dict()
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 1 if rep.hard_ban_count else 0

    print(f"=== humanizer-it scan: {args.source} ===\n")

    print(f"CLEANLINESS: {sc.score}/100  [{sc.band}]")
    print("  (≥85 clean · 60-84 targeted edit · <60 rewrite)")
    for reason, pts in sc.penalties:
        print(f"  {pts:+d}  {reason}")
    print()

    print("HARD BANS:")
    if rep.hard_bans:
        for h in rep.hard_bans:
            print(f"  ⛔ {h.marker} ×{h.count}")
    else:
        print("  ✓ clean")
    print()

    print(f"Markers (quick scanner): {marker_verdict(rep.markers)}")
    for h in sorted(rep.markers, key=lambda x: -x.count)[:12]:
        print(f"  • [{h.category}] «{h.marker}» ×{h.count}")
    print()

    print("Rhythm / typography:")
    print(f"  {rhythm_verdict(rep.rhythm)}")
    print(f"  sentences: {rep.rhythm.sentences}, mean length: {rep.rhythm.mean_len} "
          f"(min {rep.rhythm.min_len} / max {rep.rhythm.max_len}), CV: {rep.rhythm.cv_len}")
    print(f"  ellipses: {rep.rhythm.ellipsis}, parentheses: {rep.rhythm.parentheses}, "
          f"questions: {rep.rhythm.questions}")
    print()

    print("Morphosyntax:")
    print(f"  {morph_verdict(rep.morph)}")
    print(f"  words: {rep.morph.words}, nominalizations: {rep.morph.nominalizations}, "
          f"subject pron.: {rep.morph.subject_pronouns}, clitics ci/ne: {rep.morph.clitics_ci_ne}")
    print()

    print("Structure (document level):")
    print(f"  {structure_verdict(rep.structure)}")

    # Exit code: non-zero if there are HARD BANS — handy for CI/pre-commit.
    return 1 if rep.hard_ban_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
