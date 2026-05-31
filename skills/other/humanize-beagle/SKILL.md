---
name: humanize-beagle
description: Rewrite AI-generated developer text to sound human — fix inflated language, filler, tautological docs, and robotic tone. Use after review-ai-writing identifies issues.
disable-model-invocation: true
user-invocable: true
dependencies:
  - docs-style
  - review-ai-writing
---

# Humanize

Apply fixes from a previous `review-ai-writing` run with automatic safe/risky classification.

## Usage

```text
/beagle-docs:humanize-beagle [--dry-run] [--all] [--category <name>]
```

**Flags:**
- `--dry-run` - Show what would be fixed without changing files
- `--all` - Fix entire codebase (runs review with --all first)
- `--category <name>` - Only fix specific category: `content|vocabulary|formatting|communication|filler|code_docs`

## Instructions

### Hard gates

Advance past destructive or evidence-bound steps only when each **PASS** is true (commands and artifacts—not “I checked mentally”):

1. **G1 — Safe to edit files** — **PASS:** `git status --porcelain` is empty, **or** `git stash push -u -m "beagle-docs: pre-humanize backup"` exits 0.
2. **G2 — Review input is real JSON with expected shape** — **PASS:** `.beagle/ai-writing-review.json` exists **and** the file parses as JSON with a `git_head` key and a `findings` value that is an array (possibly empty). Use the `jq -e` command in step 3, or the same checks with `json.load` in Python. If this fails, stop with a parse/validation error—do not apply fixes.
3. **G3 — References before rewrites** — **PASS:** For each finding you will edit, the `references/*.md` files required by step 4 for that category/type are read in this session before you change text.
4. **G4 — Per-file validation** — **PASS:** Every modified file passes the step 8 check for its type; otherwise run `git checkout -- "$file"` for that file and do not list it as OK in the summary.
5. **G5 — Delete review file only on full success** — **PASS:** Run `rm .beagle/ai-writing-review.json` only when G4 holds for all files you are keeping unchanged from validation failures (aligns with step 10).

### 1. Parse Arguments

Extract flags from `$ARGUMENTS`:
- `--dry-run` - Preview mode only
- `--all` - Full codebase scan
- `--category <name>` - Filter to specific category

### 2. Pre-flight Safety Checks

```bash
# Check for uncommitted changes
git status --porcelain
```

If working directory is dirty, warn:
```text
Warning: You have uncommitted changes. Creating a git stash before proceeding.
Run `git stash pop` to restore if needed.
```

Create stash if dirty:
```bash
git stash push -u -m "beagle-docs: pre-humanize backup"
```

**G1 PASS:** Either the working tree was already clean, or the stash command exited 0.

### 3. Load Review Results

Check for existing review file:
```bash
cat .beagle/ai-writing-review.json 2>/dev/null
```

**If file missing:**
- If `--all` flag: Run `/beagle-docs:review-ai-writing --all` first
- Otherwise: Fail with: "No review results found. Run `/beagle-docs:review-ai-writing` first."

**If file exists, validate JSON and freshness (G2):**
```bash
# Required shape: parseable JSON with git_head and findings array (may be empty)
jq -e 'has("git_head") and ((.findings // []) | type == "array")' .beagle/ai-writing-review.json >/dev/null 2>&1 \
  || { echo "Invalid or incompatible ai-writing-review.json"; exit 1; }

# Get stored git HEAD from JSON
stored_head=$(jq -r '.git_head' .beagle/ai-writing-review.json)
current_head=$(git rev-parse HEAD)

if [ "$stored_head" != "$current_head" ]; then
  echo "Warning: Review was run at commit $stored_head, but HEAD is now $current_head"
fi
```

If stale, prompt: "Review results are stale. Re-run review? (y/n)"

### 4. Load Reference Material

Read the appropriate reference files based on the findings being fixed:

- Read `references/vocabulary-swaps.md` when applying `ai_vocabulary_high` or `ai_vocabulary_low` fixes
- Read `references/fix-strategies.md` for strategy details and before/after examples for any category
- Read `references/developer-voice.md` for tone/register guidance when rewriting prose

Only load what you need — if fixing only vocabulary, skip the voice guide.

### 5. Filter Findings

If `--category` is set, filter findings to that category only.

Partition remaining findings by `fix_safety`:

**Safe Fixes** (auto-apply):
- `chat_leak` - Delete conversational artifacts
- `cutoff_disclaimer` - Delete knowledge cutoff references
- `filler_phrase` - Delete filler phrases
- `heading_restatement` - Delete restating first sentence
- `emoji_decoration` - Remove emoji from technical text
- `boldface_overuse` - Remove excessive bold formatting
- `ai_vocabulary_high` - Swap high-signal AI words
- `narrating_obvious` - Delete obvious code comments
- `synthetic_opener` - Delete "In today's..." openers
- `sycophantic_tone` - Delete or neutralize praise
- `vague_authority` - Delete unattributed claims
- `excessive_hedging` - Remove qualifiers
- `generic_conclusion` - Delete summary padding
- `copula_avoidance` - Use "is/are" naturally
- `rhetorical_device` - Delete rhetorical questions
- `em_dash_overuse` - Replace formulaic em dashes with commas, parentheses, or colons
- `thematic_break` - Remove horizontal rules before headings
- `title_case_heading` - Convert AI title-case headings to sentence case
- `curly_quotes` - Normalize curly quotes/apostrophes to straight
- `negative_parallelism` - Delete "Not just X, but also Y" filler constructions
- `challenges_and_prospects` - Delete "Despite its... faces challenges..." formulaic wrappers

**Needs Review Fixes** (require confirmation):
- `promotional_language` - Rewrite with specifics
- `formulaic_structure` - Restructure sections
- `synonym_cycling` - Pick consistent term
- `commit_inflation` - Rewrite commit scope
- `tautological_docstring` - Rewrite or delete docstring
- `exhaustive_enumeration` - Trim parameter docs
- `this_noun_verbs` - Rewrite docstring voice
- `ai_vocabulary_low` - Reduce cluster density
- `apologetic_error` - Rewrite error message
- `rule_of_three` - Simplify three-item lists used as filler comprehensiveness
- `inline_header_list` - Restructure boldfaced inline-header vertical lists
- `unnecessary_table` - Convert small tables to prose
- `regression_to_mean` - Restore specific facts replaced by vague praise

### 6. Apply Safe Fixes

If `--dry-run`:
```markdown
## Safe Fixes (would apply automatically)

| # | File | Line | Type | Action |
|---|------|------|------|--------|
| 1 | README.md | 3 | synthetic_opener | Delete "In today's rapidly evolving..." |
| 2 | src/auth.py | 15 | narrating_obvious | Delete "# Check if user exists" |
| 3 | README.md | 42 | ai_vocabulary_high | Replace "utilize" with "use" |
...
```

Otherwise, apply fixes grouped by file to minimize file I/O:

1. Sort findings by file, then by line number (descending, to avoid offset drift)
2. For each file, apply all safe fixes in reverse line order
3. For git artifacts (`git:commit:*`, `git:pr:*`), skip — these can't be auto-fixed. Report them for manual attention.

### 7. Handle Needs Review Fixes

If `--dry-run`, list them:
```markdown
## Needs Review Fixes (would prompt interactively)

| # | File | Line | Type | Original | Suggested |
|---|------|------|------|----------|-----------|
| 4 | README.md | 8 | promotional_language | "powerful, enterprise-grade solution" | "authentication library" |
...
```

Otherwise, for each fix, prompt interactively:

```text
[README.md:8] Promotional language: "powerful, enterprise-grade solution"
Suggested: "authentication library"
(y)es / (n)o / (e)dit / (s)kip all:
```

Track user choices:
- `y` - Apply this fix as suggested
- `n` - Skip this fix
- `e` - User provides custom replacement
- `s` - Skip all remaining interactive fixes

### 8. Validate Results

For each modified markdown file, verify basic validity:

```bash
# Check for broken markdown (unclosed code blocks, broken links)
# Simple check: matching ``` pairs
grep -c '```' "$file" | awk '{print ($1 % 2 == 0) ? "OK" : "WARNING: odd number of code fences"}'
```

For modified source files, check syntax is still valid:

**Python:**
```bash
python3 -c "import ast; ast.parse(open('$file').read())"
```

**TypeScript/JavaScript:**
```bash
npx -y acorn --ecma2020 "$file" > /dev/null 2>&1
```

If validation fails for any file, revert that file:
```bash
git checkout -- "$file"
echo "Reverted $file due to validation failure"
```

### 9. Report Results

```markdown
## Humanize Summary

### Applied Fixes
- [x] README.md:3 - Deleted synthetic opener
- [x] README.md:42 - Replaced "utilize" with "use"
- [x] src/auth.py:15 - Deleted obvious comment

### Interactive Fixes
- [x] README.md:8 - Rewrote promotional language (user approved)
- [ ] docs/guide.md:22 - Skipped by user

### Skipped (Git Artifacts)
- [ ] git:commit:abc1234 - Chat leak in commit message (amend manually)

### Validation
- README.md: OK
- src/auth.py: OK

### Diff Summary
```

```bash
git diff --stat
```

### 10. Cleanup

On successful completion (all validations pass):
```bash
rm .beagle/ai-writing-review.json
```

If any validation fails, keep the file and report:
```text
Review file preserved at .beagle/ai-writing-review.json
Fix issues and re-run, or restore with: git stash pop
```

## Core Principles

1. **Delete first, rewrite second.** Most AI patterns are padding. Removing them improves the text.
2. **Use simple words.** Replace "utilize" with "use", "facilitate" with "help", "implement" with "add".
3. **Keep sentences short.** Break compound sentences. One idea per sentence.
4. **Preserve meaning.** Never change what the text says, only how it says it.
5. **Match the register.** Commit messages are terse. READMEs are conversational. API docs are precise. Read `references/developer-voice.md` for the full register guide.
6. **Don't overcorrect.** A slightly formal sentence is fine. Only fix patterns that read as obviously AI-generated.
7. **Understand regression to the mean.** LLMs produce the most statistically likely output. Specific, unusual facts get replaced with generic, positive descriptions. When humanizing, restore specificity — replace vague praise with concrete details.
8. **Score density, not individual words.** AI vocabulary words co-occur. One or two may be coincidental; a cluster of 3+ is a strong AI tell.

## Example

```bash
# Preview all fixes without applying
/beagle-docs:humanize-beagle --dry-run

# Fix only vocabulary issues
/beagle-docs:humanize-beagle --category vocabulary

# Full codebase scan and fix
/beagle-docs:humanize-beagle --all

# Preview filler fixes only
/beagle-docs:humanize-beagle --category filler --dry-run
```

## Rules

- Always load reference material before applying fixes (step 4); satisfy **G3** per finding
- Never modify files without a clean working tree or a successful stash (**G1**)
- Apply safe fixes in reverse line order to avoid offset drift
- Never auto-fix git artifacts (commits, PRs) — report them for manual action
- Validate every modified file before considering it done (**G4**)
- Revert files that fail validation
- Do not present the step 9 summary as “complete” until step 8 validation has passed for every file you are keeping
- Remove `.beagle/ai-writing-review.json` only after full success (**G5**); if validation failed partway, keep the file and follow step 10
