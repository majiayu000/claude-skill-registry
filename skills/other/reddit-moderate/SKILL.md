---
name: reddit-moderate
description: "Reddit moderation via PRAW: fetch modqueue, classify reports, take actions."
user-invocable: false
argument-hint: "[--auto] [--dry-run]"
agent: python-general-engineer
allowed-tools:
  - Bash
  - Read
routing:
  triggers:
    - "moderate Reddit"
    - "modqueue"
    - "Reddit reports"
    - "Reddit moderation"
    - "check reports"
  category: process
  pairs_with:
    - content-engine
---

# Reddit Moderate

On-demand Reddit community moderation powered by PRAW. Fetches your modqueue,
classifies content against subreddit rules and author history using LLM-powered
report classification, and executes mod actions you confirm.

## Modes

| Mode | Invocation | Behavior |
|------|-----------|----------|
| **Interactive** | `/reddit-moderate` | Fetch queue, classify, present with analysis, you confirm actions |
| **Auto** | `/loop 10m /reddit-moderate --auto` | Fetch queue, classify, auto-action high-confidence items, flag rest |
| **Dry-run** | `/reddit-moderate --dry-run` | Fetch queue, classify, show recommendations without acting |

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| Classifying items, category definitions, confidence thresholds | `classification-prompt.md` | Routes to the matching deep reference |
| Prompt template, untrusted content handling, prompt injection defense | `classification-prompt.md` | Routes to the matching deep reference |
| Action mapping by confidence level, config.json format | `classification-prompt.md` | Routes to the matching deep reference |
| Per-item classification steps, repeat offender check, mass-report detection | `classification-prompt.md` | Routes to the matching deep reference |
| Script subcommands, flags, usage examples | `script-commands.md` | Routes to the matching deep reference |
| Exit codes, error troubleshooting | `script-commands.md` | Routes to the matching deep reference |
| Scan commands, setup commands, queue/report commands | `script-commands.md` | Routes to the matching deep reference |
| Subreddit data directory structure, file purposes | `context-loading.md` | Routes to the matching deep reference |
| Setup flow for new subreddits, bootstrapping | `context-loading.md` | Routes to the matching deep reference |
| Credentials, prerequisites, dry-run default | `context-loading.md` | Routes to the matching deep reference |
| Context loading sequence, missing file handling | `context-loading.md` | Routes to the matching deep reference |

## Instructions

### Interactive Mode (default)

**Phase 1: FETCH** -- Get the modqueue with classification prompts.

```bash
python3 skills/content/reddit-moderate/scripts/reddit-mod.py queue --json --limit 25 | python3 skills/content/reddit-moderate/scripts/reddit-mod.py classify
```

This pipes modqueue items through the classify subcommand, which loads subreddit
context from `reddit-data/{subreddit}/` and assembles a classification prompt for
each item. The output is a JSON array where each result contains item metadata,
heuristic flags (`mass_report_flag`, `repeat_offender_count`), and a `prompt`
field with the fully rendered classification prompt.

The classify subcommand is a prompt assembler only; it does not call any LLM.
Fields `classification`, `confidence`, and `reasoning` are null/empty placeholders
for the LLM to fill in Phase 2.

Read the output. For each item, read the `prompt` field and classify it.

**Phase 2: CLASSIFY** -- For each item, read the rendered classification prompt
and assign a classification. The prompt contains all subreddit context, rules,
author history, and report signals. Classify as one of: `FALSE_REPORT`,
`VALID_REPORT`, `MASS_REPORT_ABUSE`, `SPAM`, `BAN_RECOMMENDED`, `NEEDS_HUMAN_REVIEW`.

Assign a confidence score (0-100) and one-sentence reasoning for each item.

> Load `references/classification-prompt.md` for category definitions, the full
> prompt template, per-item classification steps, and confidence thresholds.

**Phase 3: PRESENT** -- For each modqueue item, present a summary grouped by
classification. Include the classification label and confidence:

```
Item 1: [t3_abc123] "Post title here"
  Author: u/username (score: 5, reports: 2)
  Report reasons: "spam", "off-topic"
  Body: [first 200 chars of content]
  Classification: VALID_REPORT (confidence: 92%)
  Reasoning: Author history shows 5 promotional posts in 7 days with no
             community engagement. Violates subreddit rules against self-promotion.
  Recommendation: REMOVE (reason: Rule 3)

Item 2: [t1_def456] "Comment text here"
  Author: u/other_user (score: 12, reports: 1)
  Report reason: "rude"
  Classification: FALSE_REPORT (confidence: 88%)
  Reasoning: Sarcastic but within community norms. Report appears frivolous.
  Recommendation: APPROVE
```

**Phase 4: CONFIRM** -- Ask the user to confirm or override recommendations.
Wait for user input. Wait for explicit user confirmation before proceeding.

**Phase 5: ACT** -- Execute confirmed actions:

```bash
python3 skills/content/reddit-moderate/scripts/reddit-mod.py approve --id t1_def456
python3 skills/content/reddit-moderate/scripts/reddit-mod.py remove --id t3_abc123 --reason "Rule 3: Self-promotion"
```

Report results after each action.

> Load `references/script-commands.md` for all subcommand flags and examples.

### Auto Mode (for /loop)

When invoked with `--auto` argument or when the user says "auto mode":

1. Fetch queue and build classification prompts:
   ```bash
   python3 skills/content/reddit-moderate/scripts/reddit-mod.py queue --auto --since-minutes 15 --json | python3 skills/content/reddit-moderate/scripts/reddit-mod.py classify
   ```

2. For each item, read the rendered `prompt` field and classify it using
   the categories and confidence scoring from `references/classification-prompt.md`.

3. For items meeting the confidence threshold:
   - `FALSE_REPORT` / `MASS_REPORT_ABUSE` => approve
   - `SPAM` => remove as spam
   - `VALID_REPORT` => remove with generated reason
   - `BAN_RECOMMENDED` => **always skip** (requires human review regardless of confidence)

4. For items below the confidence threshold => skip (leave for human review).

5. Output a summary of actions taken, items skipped, and classifications.

**Critical auto-mode rules:**
- Always require human review before banning users
- Always require human review before locking threads
- When in doubt, SKIP; false negatives are better than false positives
- Log every auto-action for the user to review later

### Proactive Scan Mode

Scan recent posts/comments for rule violations that were not reported:

```bash
python3 skills/content/reddit-moderate/scripts/reddit-mod.py scan --json --classify --limit 50 --since-hours 24
```

With `--classify`, the scan output includes classification prompts. Read each
prompt and classify the item. Items with `scan_flags` (job_ad_pattern,
training_vendor_pattern, possible_non_english) have heuristic signals that
supplement the LLM classification.

Same confidence thresholds and safety rules as auto mode apply.

## Reference Loading

Load these references when the task matches the signal:

| Signal / Task | Reference File |
|---------------|----------------|
| Classifying items, category definitions, confidence thresholds | `references/classification-prompt.md` |
| Prompt template, untrusted content handling, prompt injection defense | `references/classification-prompt.md` |
| Action mapping by confidence level, config.json format | `references/classification-prompt.md` |
| Per-item classification steps, repeat offender check, mass-report detection | `references/classification-prompt.md` |
| Script subcommands, flags, usage examples | `references/script-commands.md` |
| Exit codes, error troubleshooting | `references/script-commands.md` |
| Scan commands, setup commands, queue/report commands | `references/script-commands.md` |
| Subreddit data directory structure, file purposes | `references/context-loading.md` |
| Setup flow for new subreddits, bootstrapping | `references/context-loading.md` |
| Credentials, prerequisites, dry-run default | `references/context-loading.md` |
| Context loading sequence, missing file handling | `references/context-loading.md` |

## References

This skill uses these shared patterns:
- [Untrusted Content Handling](../shared-patterns/untrusted-content-handling.md) - Prompt injection defense for all Reddit content fed into LLM classification
