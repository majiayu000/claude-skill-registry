---
name: humanizer
description: Rewrite AI-sounding text into natural, human writing by removing common LLM patterns while preserving meaning and tone.
---

# Humanizer: Remove AI writing patterns

Edit text so it sounds like a real person wrote it: clearer rhythm, stronger specificity, less filler, and no chatbot artifacts. Keep the original meaning, facts, and intent.

## Quick quality checklist

- `name` matches folder name exactly (`humanizer`)
- Examples are copy-paste runnable (Bash + Node.js)
- Rewrites preserve factual claims and scope
- Output includes rewritten text and optional concise change summary
- No invented facts, citations, or sources

## When to use

- User asks to “humanize”, “de-AI”, “make this sound natural”, or “remove AI tone”
- Draft sounds generic, inflated, formulaic, or overly polished
- Content has chatbot artifacts (hedging, servile tone, boilerplate intros/outros)
- You need a tighter, more direct style without changing factual claims

## Required tools / APIs

- No external API required
- Optional local tools for batch editing:
  - `rg` (ripgrep) for pattern detection
  - `node` (v18+) for scripted rewrite pipelines

Install options:

```bash
# Ubuntu/Debian
sudo apt-get install -y ripgrep nodejs npm

# macOS
brew install ripgrep node
```

## Skills

### basic_usage

Use this flow for single passages:

1. Identify AI-patterns in the input
2. Rewrite sentences to simpler constructions
3. Replace vague claims with specific details when provided
4. Keep tone aligned to the user’s context (formal/casual/technical)
5. Return the rewritten text

**Bash (pattern scan):**

```bash
cat input.txt \
  | rg -n -i "\b(additionally|crucial|pivotal|underscores|highlighting|fostering|landscape|testament|vibrant)\b|\b(i hope this helps|let me know if|great question)\b|—|[“”]"
```

**Node.js (simple rule-based humanizer):**

```javascript
function humanizeText(text) {
  const replacements = [
    [/\bIn order to\b/g, "To"],
    [/\bDue to the fact that\b/g, "Because"],
    [/\bAt this point in time\b/g, "Now"],
    [/\bIt is important to note that\b/g, ""],
    [/\bI hope this helps!?\b/gi, ""],
    [/\bLet me know if you'd like.*$/gim, ""],
    [/\bserves as\b/g, "is"],
    [/\bstands as\b/g, "is"],
    [/\bboasts\b/g, "has"],
    [/—/g, ","],
    [/[“”]/g, '"']
  ];

  let output = text;
  for (const [pattern, to] of replacements) {
    output = output.replace(pattern, to);
  }

  return output
    .replace(/\s{2,}/g, " ")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

// Usage:
// const fs = require('node:fs');
// const input = fs.readFileSync('input.txt', 'utf8');
// console.log(humanizeText(input));
```

### robust_usage

Use this for long drafts and production outputs:

- Do a first pass for pattern detection
- Do a second pass for structure/rhythm (mix short + long sentences)
- Remove claims without support ("experts say", "observers note") unless sourced
- Prefer plain verbs (`is/are/has`) over inflated alternatives
- Keep uncertainty only where uncertainty is real

**Bash (batch rewrite starter):**

```bash
#!/usr/bin/env bash
set -euo pipefail

in_file="${1:-input.txt}"
out_file="${2:-output.txt}"

sed -E \
  -e 's/\bIn order to\b/To/g' \
  -e 's/\bDue to the fact that\b/Because/g' \
  -e 's/\bAt this point in time\b/Now/g' \
  -e 's/\bserves as\b/is/g' \
  -e 's/\bstands as\b/is/g' \
  -e 's/\bboasts\b/has/g' \
  -e 's/[“”]/"/g' \
  -e 's/—/,/g' \
  "$in_file" > "$out_file"

echo "Rewritten text saved to: $out_file"
```

**Node.js (pipeline with validation):**

```javascript
import fs from "node:fs/promises";

const bannedPatterns = [
  /\bI hope this helps\b/i,
  /\bLet me know if you'd like\b/i,
  /\bGreat question\b/i,
  /\bAdditionally\b/g,
  /\bcrucial|pivotal|vibrant|testament\b/g
];

function rewrite(text) {
  return text
    .replace(/\bIn order to\b/g, "To")
    .replace(/\bDue to the fact that\b/g, "Because")
    .replace(/\bAt this point in time\b/g, "Now")
    .replace(/\bserves as\b/g, "is")
    .replace(/\bstands as\b/g, "is")
    .replace(/\bboasts\b/g, "has")
    .replace(/—/g, ",")
    .replace(/[“”]/g, '"')
    .replace(/\s{2,}/g, " ")
    .trim();
}

function validate(text) {
  const hits = bannedPatterns.flatMap((pattern) => {
    const m = text.match(pattern);
    return m ? [pattern.toString()] : [];
  });
  return { ok: hits.length === 0, hits };
}

async function main() {
  const inputPath = process.argv[2] || "input.txt";
  const outputPath = process.argv[3] || "output.txt";

  const input = await fs.readFile(inputPath, "utf8");
  const output = rewrite(input);
  const report = validate(output);

  await fs.writeFile(outputPath, output, "utf8");

  if (!report.ok) {
    console.error("Warning: possible AI patterns remain:", report.hits);
    process.exitCode = 2;
  }

  console.log(`Saved: ${outputPath}`);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
```

## Pattern checklist

Scan and remove these classes when they appear:

1. Significance inflation and legacy framing
2. Notability/media name-dropping without context
3. Superficial `-ing` chains
4. Promotional/advertisement wording
5. Vague attribution ("experts say")
6. Formulaic “challenges/future prospects” sections
7. Overused AI vocabulary (e.g., pivotal, underscores, tapestry)
8. Copula avoidance (`serves as`, `stands as` instead of `is`)
9. Negative parallelism (`not just X, but Y`)
10. Rule-of-three overuse
11. Excessive synonym cycling
12. False ranges (`from X to Y` without meaningful scale)
13. Em-dash overuse
14. Mechanical boldface emphasis
15. Inline-header bullet artifacts
16. Title Case heading overuse where sentence case fits
17. Emoji decoration in formal content
18. Curly quotes when straight quotes are expected
19. Chatbot collaboration artifacts
20. Knowledge-cutoff disclaimers left in final copy
21. Sycophantic/servile tone
22. Filler phrase bloat
23. Excessive hedging
24. Generic upbeat conclusions with no substance

## Output format

Return:

- `rewritten_text` (string, required): final humanized draft
- `changes` (array of strings, optional): 3-8 concise bullets on major edits
- `warnings` (array of strings, optional): unresolved vagueness or missing source details

Example:

```json
{
  "rewritten_text": "The policy may affect outcomes, especially in smaller teams.",
  "changes": [
    "Removed filler phrase: 'It is important to note that'",
    "Replaced vague hedge 'could potentially possibly' with 'may'"
  ],
  "warnings": [
    "Claim about impact scale remains unsourced in original text"
  ]
}
```

Error shape:

```json
{
  "error": "input_too_short",
  "message": "Need at least one full sentence to humanize reliably.",
  "fix": "Provide a longer passage or combine short fragments into a paragraph."
}
```

## Rate limits / Best practices

- Use a maximum of 2 rewrite passes (pattern pass + voice pass) to avoid over-editing
- Keep domain terms and named entities unchanged unless the user asks for simplification
- Preserve formatting intent (headings, bullets, quote blocks) unless clearly broken
- If source claims are vague, keep wording conservative and surface a warning instead of inventing specifics
- Read output aloud mentally: if rhythm sounds robotic, vary sentence length and cadence

## Agent prompt

```text
You have the humanizer skill. When the user asks to make text sound natural:

1) Read the full draft and detect AI writing patterns.
2) Rewrite to preserve meaning, facts, and intended tone.
3) Prefer specific, concrete language over vague significance claims.
4) Remove chatbot artifacts, filler, and over-hedging.
5) Use simple constructions (is/are/has) where they read better.
6) Vary sentence rhythm so the text sounds spoken by a real person.
7) Return the rewritten text. Optionally add a brief bullet summary of key changes.

Never invent facts. If a claim is vague and no source is provided, keep it conservative.
```

## Troubleshooting

**Rewrite feels too flat**
- Symptom: Text is clean but soulless
- Fix: Add natural opinion/stance where context allows; vary rhythm and sentence length

**Meaning drifted from original**
- Symptom: New version sounds better but changes claims
- Fix: Re-run with strict requirement: preserve factual claims and scope sentence-by-sentence

**Output still sounds AI-generated**
- Symptom: Frequent abstract words and formulaic transitions remain
- Fix: Run pattern scan first, then rewrite only flagged spans; avoid global synonym swaps

## Validation workflow

Use this quick gate before returning output:

1. Compare original vs rewritten sentence-by-sentence for factual equivalence
2. Verify no unsupported new specifics were introduced
3. Check for leftover chatbot artifacts (`I hope this helps`, `Let me know if`)
4. Ensure rhythm variety (not all sentences same length)
5. Return `warnings` for unresolved ambiguities

## See also

- [../web-interface-guidelines-review/SKILL.md](../web-interface-guidelines-review/SKILL.md) — Improve clarity and structure of user-facing copy
- [../json-and-csv-data-transformation/SKILL.md](../json-and-csv-data-transformation/SKILL.md) — Transform and validate large text datasets before rewrite passes

## Reference

- Source inspiration: https://skills.sh/blader/humanizer/humanizer
- Pattern basis: Wikipedia "Signs of AI writing" (WikiProject AI Cleanup)
