# /// script
# requires-python = ">=3.10"
# ///
"""Record a hypothesis in the Minoan hypothesis log.

Usage:
    uv run record_hypothesis.py \
      --word "MA-RU" \
      --reading "malāḥu" \
      --meaning "sailor" \
      --root "m-l-ḥ" \
      --confidence SPECULATIVE \
      --evidence "Akkadian malāḫu, Hebrew mallāḥ; maritime context" \
      [--corpus "MA-RU (HT 12, ZA 4)"] \
      [--xref "lexicon.md: Maritime Domain"]
"""

import sys
import argparse
from datetime import date
from pathlib import Path

LOG_PATH = Path(__file__).parent.parent / "references" / "hypothesis-log.md"

VALID_CONFIDENCE = {"CONFIRMED", "PROBABLE", "CANDIDATE", "SPECULATIVE"}

def main():
    parser = argparse.ArgumentParser(description="Record a Minoan hypothesis")
    parser.add_argument("--word", required=True, help="Linear A transliteration")
    parser.add_argument("--reading", required=True, help="Pronunciation")
    parser.add_argument("--meaning", required=True, help="English meaning")
    parser.add_argument("--root", required=True, help="Semitic root")
    parser.add_argument("--confidence", required=True, choices=VALID_CONFIDENCE)
    parser.add_argument("--evidence", required=True, help="Derivation chain")
    parser.add_argument("--corpus", default="—", help="Corpus matches")
    parser.add_argument("--xref", default="—", help="Cross-references")
    args = parser.parse_args()

    today = date.today().isoformat()

    entry = f"""
## {today} — {args.word}

- **Minoan form:** {args.word}
- **Reading:** {args.reading}
- **Meaning:** {args.meaning}
- **Root:** {args.root}
- **Confidence:** {args.confidence}
- **Evidence:** {args.evidence}
- **Corpus matches:** {args.corpus}
- **Cross-references:** {args.xref}
"""

    with open(LOG_PATH, "a") as f:
        f.write(entry)

    print(f"Recorded: {args.word} → {args.reading} ({args.confidence})")
    print(f"Log: {LOG_PATH}")

if __name__ == "__main__":
    main()
