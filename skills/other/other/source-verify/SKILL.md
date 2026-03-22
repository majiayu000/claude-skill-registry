---
name: source-verify
description: "This skill should be used when the user asks to 'verify sources', 'check citations', 'fact-check footnotes', 'verify quotes', 'source check', 'are my cites real', 'check for hallucinated citations', or needs to verify that citations in a legal/academic manuscript actually exist and are accurate. Also use when the user wants to check that quoted text actually appears in the cited source."
user-invocable: false
---

# Source Verification

Verify that citations in a manuscript are real, accurate, and that quoted text actually appears in the source. Operates as a domain-specific audit-fix-loop: extract citations, run checks, score, fix, re-check.

**Announce:** "Using source-verify to check citations against Paperpile and source documents."

## What This Skill Checks

```
┌──────────────────────────────────────────────────────────┐
│  CHECK 1: EXISTENCE (mechanical)                          │
│  Does this cited work exist in paperpile.bib?            │
│  → grep paperpile.bib for author + title + year          │
│  → If not found: flag as UNVERIFIED (may still exist)    │
└──────────────────────────────────────────────────────────┘
                        │
                  Exists in bib?
                        ▼
┌──────────────────────────────────────────────────────────┐
│  CHECK 2: ACCURACY (mechanical)                           │
│  Are the citation fields correct?                        │
│  → Compare volume, issue, pages, year against bibtex     │
│  → Flag any mismatches as FIELD_ERROR                    │
└──────────────────────────────────────────────────────────┘
                        │
                  Fields correct?
                        ▼
┌──────────────────────────────────────────────────────────┐
│  CHECK 3: QUOTE VERIFICATION (outsourced to RAG)          │
│  Does the quoted text appear in the source?              │
│  → readwise chat: "Verify this exact quote from [Author] │
│  → rga against downloaded PDF (fallback)                 │
│  → NLM generate-chat against notebook (fallback)         │
│  → Flag QUOTE_NOT_FOUND or QUOTE_MISMATCH               │
└──────────────────────────────────────────────────────────┘
                        │
                  Quotes verified?
                        ▼
┌──────────────────────────────────────────────────────────┐
│  CHECK 4: CLAIM GROUNDING (outsourced to RAG)             │
│  Does the cited source actually support the claim?       │
│  → readwise chat or NLM generate-chat                    │
│  → These systems answer ONLY from source text            │
│  → Flag UNSUPPORTED or CONTRADICTED                      │
└──────────────────────────────────────────────────────────┘
```

**Checks 1-2** run on every invocation (fast, mechanical). **Check 3** runs when the footnote contains a direct quote. **Check 4** runs only when the user explicitly requests claim grounding.

## Independence Architecture

The key insight: **verification must use external ground truth, never the agent's own memory.** Two systems provide this:

```
┌─────────────────────────────────────────────────────────┐
│  VERIFIER HIERARCHY — QUOTES (try in order)              │
│                                                          │
│  1. Readwise highlights — User highlighted the passage.  │
│     readwise-custom highlights --search "quote fragment"  │
│     If found: verified against actual source text.       │
│     Fastest — no download, no LLM.                       │
│                                                          │
│  2. rga (local)    — Download PDF from Drive, search.    │
│     Deterministic text search inside PDFs.               │
│     No pdftotext needed — rga extracts text internally.  │
│                                                          │
│  3. NLM chat       — Add paper to a verification         │
│     notebook, then query.                                │
│     "Find this passage in [source]: '…'"                │
│     Grounded in NLM's ingested sources.                  │
│     Best for: OCR issues, paraphrased quotes.            │
│                                                          │
│  NEVER: Agent's own memory/training data.                │
│  That is the hallucination source, not a verifier.       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  VERIFIER — CLAIM GROUNDING                              │
│                                                          │
│  NLM chat only — requires semantic understanding.        │
│  Readwise highlights are too fragmentary for claims.     │
│  rga is too literal for "does source support claim?"     │
└─────────────────────────────────────────────────────────┘
```

**Why Readwise first for quotes:** The user highlights important passages while reading. If a quote in the manuscript matches a Readwise highlight, it was captured directly from the source — strongest possible verification, zero cost.

**Why NLM for claims:** Claim grounding requires understanding what the source argues, not just matching strings. NLM chat answers from ingested full text with semantic comprehension.

## Scope

| Source Type | Checks Available | Ground Truth |
|-------------|-----------------|-------------|
| **Journal articles** | 1, 2, 3, 4 | `paperpile.bib` + Drive PDFs + Readwise highlights |
| **Books / book chapters** | 1, 2, 3, 4 | `paperpile.bib` + Drive PDFs |
| **Working papers** | 1, 2, 3, 4 | `paperpile.bib` + Drive PDFs |
| **SEC releases / regulations** | 1 (partial) | May be in bib as MISC entries |
| **Federal case citations** | 1 (existence only) | WRDS `fjc_litigation.civil` (13.5M cases) + `audit_corp_legal` |
| **Statutes** | NOT COVERED | No ground truth database wired up |

### Federal Case Verification via WRDS

The FJC Integrated Database (`fjc_litigation.civil`) contains all federal civil cases with plaintiff/defendant names, docket numbers, filing dates, districts, and nature-of-suit codes. Use it to verify that cited cases actually exist:

```bash
# Connect via SSH tunnel to WRDS
ssh wrds "echo \"SELECT plaintiff, defendant, docket, district, filedate
FROM fjc_litigation.civil
WHERE plaintiff ILIKE '%smith%' AND defendant ILIKE '%jones%'
AND filedate BETWEEN '2018-01-01' AND '2020-12-31'
LIMIT 10;\" | psql -h wrds-pgdata.wharton.upenn.edu -p 9737 -d wrds"
```

**Matching strategy for case cites:**
- Extract plaintiff and defendant names from the citation (e.g., "Smith v. Jones")
- Search `fjc_litigation.civil` with `ILIKE` on both fields
- Confirm year matches `filedate`
- For securities cases, filter `nos = 850` (nature of suit: securities/commodities)

**Audit Analytics** (`audit_corp_legal.f14_lit_legal_case`) provides corporate legal cases with settlement amounts, exposure dates, and docket numbers — useful for verifying securities litigation specifically.

**Limitations:**
- `casename` field is sparsely populated — match on `plaintiff`/`defendant` instead
- State court cases are NOT covered (federal only)
- Appellate case names may differ from trial court names
- Very recent cases may have a lag before appearing in the database

Statutes are not yet verifiable — no structured database wired up. Flag as `SKIPPED_NO_GROUND_TRUTH`.

<EXTREMELY-IMPORTANT>
## Iron Law: Mechanical Checks Before LLM Checks

**NEVER skip Checks 1-2 to jump straight to LLM-based verification.**

Mechanical checks against `paperpile.bib` are deterministic and free. They catch the most common hallucinations (invented papers, wrong volume/pages) without any LLM judgment. Running LLM checks without running mechanical checks first is wasting expensive calls on problems a grep would catch.

**Skipping the paperpile.bib check is NOT HELPFUL — the user publishes with unverified citations that may be hallucinated.**
</EXTREMELY-IMPORTANT>

## Step 0: Prerequisites

### Download paperpile.bib

The bibtex file lives on Google Drive and must be downloaded fresh each run:

```bash
# Download paperpile.bib from Drive
gws drive files get --account eddyhu@gmail.com \
  --params '{"fileId": "1yxibJLr1-kF_gcf3UA6QlU5ulXgR50kX", "alt": "media"}' \
  -o /tmp/paperpile.bib
```

**Always download fresh** — the user may have added new papers since the last run.

### Extract Footnotes

If the manuscript is DOCX, extract footnotes to structured text first. Use the bluebook-audit extraction infrastructure or `python-docx`:

```bash
# Quick extraction via python-docx
pixi exec --spec python-docx -- python3 -c "
import docx, json, sys
doc = docx.Document(sys.argv[1])
fns = []
for i, fn in enumerate(doc.part.element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}footnote')):
    fn_id = fn.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
    if fn_id and int(fn_id) > 0:
        text = ' '.join(p.text or '' for p in fn.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
        fns.append({'id': int(fn_id), 'text': text.strip()})
json.dump(fns, sys.stdout, indent=2)
" manuscript.docx > /tmp/footnotes.json
```

For plain text or markdown manuscripts, extract lines that look like footnotes (numbered references at the bottom or inline citations).

## Step 1: Check 1 — Citation Existence

For each footnote, extract the cited author(s) and title, then search `paperpile.bib`:

```bash
# Search by author surname
rg -i "author.*Egan" /tmp/paperpile.bib

# Search by title fragment
rg -i "conflicting interests" /tmp/paperpile.bib

# Search by bibtex key pattern
rg "Egan2022" /tmp/paperpile.bib
```

### Matching Strategy

Footnotes use Bluebook-abbreviated journal names; bibtex uses different abbreviations. Match on **author surname + year** first, then confirm with title keywords.

| Footnote Says | Bibtex Has | Match On |
|--------------|-----------|----------|
| Egan, Ge & Tang | `author = {Egan, Mark and Ge, Shan and Tang, Johnny}` | First author surname + year |
| 35 Rev. Fin. Stud. 5334 | `journaltitle = {Rev. Fin. Stud.}, volume = {35}, pages = {5334--5386}` | Volume + first page |
| (2022) | `date = {2022-08-24}` | Year extracted from date |

### Classification

| Result | Classification | Severity |
|--------|---------------|----------|
| Found in bib, fields match | `VERIFIED` | — |
| Found in bib, fields mismatch | `FIELD_ERROR` | HIGH |
| Not found in bib, but is a federal case | Check WRDS `fjc_litigation.civil` | — |
| Not found in bib, but is a statute | `SKIPPED_NO_GROUND_TRUTH` | INFO |
| Not found in bib, is a paper/article | `UNVERIFIED` | CRITICAL |

## Step 2: Check 2 — Field Accuracy

For each `VERIFIED` citation, compare footnote fields against bibtex:

| Footnote Field | Bibtex Field | Common Errors |
|---------------|-------------|---------------|
| Volume number | `volume` | Transposed digits |
| Issue/number | `issue` | Often omitted in footnote (OK) |
| Starting page | `pages` (before `--`) | Wrong page, off by one |
| Year | `date` (extract year) | Wrong year |
| Journal name | `journaltitle` | Abbreviation mismatch (check, don't auto-flag) |

Journal abbreviation mismatches are tricky — Bluebook and bibtex use different abbreviation conventions. Flag only when the journal name is clearly wrong (e.g., completely different journal), not when it's a different valid abbreviation of the same journal.

## Step 3: Check 3 — Quote Verification

For footnotes that contain direct quotes (text in quotation marks attributed to a source):

### Tier A: Readwise Highlights (fastest — no download needed)

If the user highlighted the quoted passage in Readwise, it's already verified against the actual source text:

```bash
# Search for the quote text in highlights
readwise-custom highlights --search "quoted text fragment" --limit 10

# Or vector search with author filter
readwise readwise-search-highlights --vector-search-term "quoted text fragment" \
  --full-text-queries '[{"field_name": "document_author", "search_term": "Egan"}]'
```

A matching highlight confirms the quote exists in the source — Readwise captured it directly from the original document. Check that the highlight comes from the correct source (match author/title).

### Tier B: rga (deterministic — download and search)

If the quote isn't in Readwise highlights, download the PDF from Drive and search:

```bash
# Find the PDF using the bibtex `file` field
# e.g., file = {All Papers/E/Egan et al. 2022 - Conflicting Interests...pdf}
gws drive files list --account eddyhu@gmail.com \
  --params '{"q": "name contains \"Egan et al. 2022 - Conflicting\" and mimeType = \"application/pdf\"", "fields": "files(id,name)", "pageSize": 1}'

# Download by file ID
gws drive files get --account eddyhu@gmail.com \
  --params '{"fileId": "<ID>", "alt": "media"}' -o /tmp/source.pdf

# Search for the quote (rga extracts PDF text internally — no pdftotext needed)
rga "the exact quoted text" /tmp/source.pdf
```

If `rga` finds it, the quote is `QUOTE_VERIFIED` — deterministic, no LLM needed.

### Tier C: NLM Chat (semantic fallback)

If `rga` doesn't find an exact match (OCR issues, scanned PDF, or the quote is slightly paraphrased), add the paper to a verification NLM notebook and ask:

```bash
# Create a verification notebook (once per project)
nlm create "Source Verification"

# Add the paper
nlm add <notebook-id> /tmp/source.pdf

# Ask NLM to find the quote
nlm generate-chat <notebook-id> "Find this exact passage in the source: '[quoted text]'. Does it appear verbatim? If the wording differs, show the actual text from the source."
```

NLM chat is grounded in the ingested PDF — it can handle OCR artifacts and minor wording differences that trip up exact string matching.

### Quote Match Classification

| Result | Classification | Severity |
|--------|---------------|----------|
| Found in Readwise highlights | `QUOTE_VERIFIED` | — |
| Exact match found via rga | `QUOTE_VERIFIED` | — |
| NLM confirms match (minor OCR/wording diffs) | `QUOTE_VERIFIED` | — |
| NLM finds similar but different text | `QUOTE_MISMATCH` | MEDIUM |
| Not found in any tier | `QUOTE_NOT_FOUND` | CRITICAL |
| Source PDF not on Drive | `QUOTE_UNCHECKED` | INFO |

## Step 4: Check 4 — Claim Grounding (Optional)

Only run when user explicitly requests deep verification. This checks whether the cited source actually supports the claim being made in the text (not just that the citation exists).

### NLM Chat (grounded in source text)

Claim grounding requires semantic understanding — NLM chat is the right tool because it answers only from ingested sources.

```bash
nlm generate-chat <notebook-id> "The manuscript claims: '[claim from text]' and cites [Author (Year)]. Does the source support this claim? Answer: SUPPORTED, PARTIALLY_SUPPORTED, UNSUPPORTED, or CONTRADICTED. Provide the relevant passage from the source."
```

**Requires:** An NLM notebook with the cited sources loaded. If not already set up:
1. Create a verification notebook: `nlm create "Source Verification — [Project]"`
2. Add papers: download from Drive, then `nlm add <notebook-id> /tmp/source.pdf`
3. Or bulk import: `nlm research "[topic]" --notebook <notebook-id> --source drive`

**Cross-source claims:** When a claim synthesizes multiple papers, add all cited sources to the same notebook. NLM can then cross-reference them in a single query.

### Classification

| Result | Classification | Severity |
|--------|---------------|----------|
| Source supports claim | `CLAIM_SUPPORTED` | — |
| Source partially supports | `CLAIM_PARTIAL` | MEDIUM |
| Source doesn't address claim | `CLAIM_UNSUPPORTED` | HIGH |
| Source contradicts claim | `CLAIM_CONTRADICTED` | CRITICAL |

## Scoring

Score = verified items / total checkable items, scaled to 0-10.

```
checkable = total_footnotes - SKIPPED_NO_GROUND_TRUTH
verified = VERIFIED + QUOTE_VERIFIED + CLAIM_SUPPORTED
score = (verified / checkable) * 10
```

Items with any finding (FIELD_ERROR, QUOTE_NOT_FOUND, UNVERIFIED, etc.) count against the score. QUOTE_UNCHECKED (source PDF unavailable) counts as checkable but not verified — it's an unresolved question, not a pass.

**Default threshold: 9.5/10** (95% of checkable citations verified).

## Audit-Fix Loop Integration

This skill is a domain-specific scorer for the audit-fix-loop pattern. To run iteratively:

```
Skill(skill="ralph-loop:ralph-loop", args="Source-verify [manuscript]. Check all citations against paperpile.bib, verify quotes against source PDFs. --max-iterations 5 --completion-promise SOURCES_9_5")
```

### Iteration Protocol

Each iteration:
1. **Audit**: Run Checks 1-3 on all footnotes (Check 4 only if requested)
2. **Score**: Compute score, record in SCORES.md
3. **Decide**: Score >= 9.5? → output promise. Score < 9.5? → fix.
4. **Fix**: For each finding:
   - `FIELD_ERROR` → correct the volume/pages/year in the manuscript
   - `QUOTE_MISMATCH` → fix the quote to match the source text
   - `QUOTE_NOT_FOUND` → flag for user review (may need to remove quote or find correct source)
   - `UNVERIFIED` → search harder (try more bibtex key variants, try Drive search), or flag for user
   - `CLAIM_UNSUPPORTED` → flag for user review (rewrite claim or find better source)

### State Files

**VERIFY_AUDIT.md** — current verification findings:
```markdown
# Source Verification — Iteration N

## Summary
- Total footnotes: 85
- Checkable: 72 (13 case cites skipped)
- Verified: 68
- Findings: 4
- Score: 9.4/10

## Findings
| FN# | Check | Classification | Severity | Details |
|-----|-------|---------------|----------|---------|
| 12 | Existence | UNVERIFIED | CRITICAL | "Smith (2019)" not found in paperpile.bib |
| 34 | Fields | FIELD_ERROR | HIGH | Vol. 42 in footnote, vol. 44 in bibtex |
| 51 | Quote | QUOTE_MISMATCH | MEDIUM | "effect on returns" vs source: "impact on returns" |
| 67 | Quote | QUOTE_NOT_FOUND | CRITICAL | Quoted text not in cited PDF |
```

**SCORES.md** — score history (append-only):
```markdown
| Iteration | Score | Findings | Key Issues |
|-----------|-------|----------|-----------|
| 1 | 8.2 | 6 | 2 UNVERIFIED, 2 FIELD_ERROR, 2 QUOTE issues |
| 2 | 9.1 | 3 | 1 UNVERIFIED (confirmed real), 2 QUOTE issues |
| 3 | 9.6 | 1 | 1 QUOTE_MISMATCH (minor) |
```

<EXTREMELY-IMPORTANT>
## Iron Law: No Self-Verification

**NEVER verify citations from your own memory or training data. Always use an external ground truth.**

Citation hallucination happens because the LLM confabulates plausible-sounding references. The same LLM will confabulate plausible-sounding verification. Every check must go through an external system:

- **Checks 1-2**: `paperpile.bib` (mechanical grep — deterministic)
- **Checks 3-4**: Readwise chat, `rga`, or NLM chat (grounded in actual source text)
- **NEVER**: "I recall this paper exists" or "That quote sounds right"

**Skipping external source checks is NOT HELPFUL — unverified citations damage the user's credibility when readers check them.**
</EXTREMELY-IMPORTANT>

## Rationalization Table

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "The citation looks right, I don't need to check the bib" | Looking right is how hallucinated citations work — they're designed to look plausible | Grep paperpile.bib. Every time. |
| "rga didn't find the quote but it's probably in there" | If rga can't find it, the quote may be fabricated or paraphrased | Try NLM chat as semantic fallback. If still not found, flag as QUOTE_NOT_FOUND |
| "The volume number is close enough (42 vs 44)" | Wrong volume = wrong citation. A reader following it will find the wrong article. | Fix it to match the bibtex entry |
| "Case cites don't need checking" | Federal cases CAN be checked via WRDS fjc_litigation. State cases are SKIPPED_NO_GROUND_TRUTH. | Check federal cases against FJC database. Skip state cases explicitly. |
| "I'll just check the first few footnotes" | Hallucinated citations cluster in the middle and end where writing fatigue hits | Check ALL footnotes. No sampling. |
| "Claim grounding is overkill" | Only if the user didn't request it. Don't skip it if they did. | Run Check 4 when requested, skip when not |

## Red Flags — STOP If You Catch Yourself:

- **Verifying a citation from memory instead of paperpile.bib** → STOP. Your memory is the hallucination source.
- **Skipping Check 1-2 and jumping to LLM verification** → STOP. Mechanical checks first.
- **Marking a citation VERIFIED without actually finding it in the bib** → STOP. Show the matching bibtex entry.
- **"The quote is close enough"** → STOP. Either it matches or it's a QUOTE_MISMATCH.
- **Running all checks yourself without spawning a fresh audit agent** → STOP. Self-verification is rubber-stamping.

## Why Skipping Hurts the Thing You Care About Most

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|-------------|----------------------|---------------------|
| **Helpfulness** | "I'll save time by not downloading PDFs" | User publishes with fabricated quotes | **Anti-helpful** — you caused a retraction |
| **Competence** | "I know this citation is real" | You confabulated it. It doesn't exist. | **Incompetent** — grep would have caught it |
| **Honesty** | "Close enough to the real quote" | The quote says something different from the source | **Dishonest** — you misrepresented the source |
| **Thoroughness** | "First 10 footnotes checked out, rest are probably fine" | Footnote 47 cites a non-existent paper | **Sloppy** — sampling missed the worst error |
