# Google Ads Scripts Skills for Claude

A Claude Code skill for writing, debugging, and shipping Google Ads Scripts
(`AdsApp` / `AdsManagerApp`) correctly on the first try.

This skill is opinionated reference material for Claude. It teaches the model
the parts of Google Ads Scripts that are not obvious from the public docs:

- The `AdsApp.mutate()` escape hatch and the exact payload shapes that work
  for resources the SDK does not wrap (demographic exclusions, asset group
  signals, etc.).
- The "field's contents don't match" error and how to avoid it.
- Well-known criterion IDs for age, gender, parental status, income, device.
- MCC `executeInParallel` rules (top-level functions, string returns).
- Preview-mode quirks (`createLabel` doesn't persist, `applyLabel` then
  throws).
- Idempotency patterns: labels, GAQL pre-checks, catching duplicate errors.

## Install

Clone (or copy) into `~/.claude/skills/google-ads-scripts/`:

```
~/.claude/skills/google-ads-scripts/
├── SKILL.md
├── README.md
├── reference/
│   ├── selectors.md
│   ├── gaql-cheatsheet.md
│   ├── mutate-escape-hatch.md
│   ├── criterion-ids.md
│   ├── mcc-scripts.md
│   ├── idempotency.md
│   ├── gotchas.md
│   └── error-handling.md
├── templates/
│   ├── single-account.js
│   ├── mcc-parallel.js
│   └── mutate-with-search.js
└── examples/
    └── exclude-age-demographic.js
```

Claude Code auto-discovers it on next run.

## How to trigger it

Mention any of these in a prompt and Claude will load the skill:

- "Google Ads Script", "AdsApp", "AdsManagerApp"
- "ads script", "AdWordsApp" (legacy name)
- "automate Google Ads"
- "mutate ad group criterion", "AdsApp.mutate"
- Pasting JavaScript that imports `AdsApp`

The skill is for WRITING scripts. For auditing Google Ads accounts use the
separate `ads-google` skill.

## What's inside

### SKILL.md
The entry point Claude reads first. Workflow rules, the three big patterns
(selectors, GAQL search, mutate), and pointers to detailed reference files.

### reference/
Topic-by-topic deep dives. Claude pulls these in on demand when relevant.

- **selectors.md** — selector field names, operators, date ranges, ordering.
- **gaql-cheatsheet.md** — GAQL syntax: SELECT, FROM, WHERE, segments,
  common resources, micros, validate-only.
- **mutate-escape-hatch.md** — `AdsApp.mutate()` payload shapes for every
  common operation, with verified examples for the resources that bite
  people most.
- **criterion-ids.md** — the global criterion ID tables (ages, genders,
  parental statuses, incomes, devices) you must hard-code in resource
  names.
- **mcc-scripts.md** — `AdsManagerApp`, `executeInParallel`, the
  string-return-value rule, top-level-function rule.
- **idempotency.md** — three patterns (label, pre-check, catch-duplicate)
  and when to combine them.
- **gotchas.md** — preview mode, runtime limits, bid modifier ranges,
  micros vs units, dashed customer IDs, immutable fields, etc.
- **error-handling.md** — interpreting common error messages and the
  retry pattern for transient RPC failures.

### templates/
Starting points to copy and modify.

- **single-account.js** — account-scope script with stats logging, label
  idempotency, preview-safe label apply, error email.
- **mcc-parallel.js** — MCC script using `executeInParallel`, with
  aggregation in `finalize` and error email on failures.
- **mutate-with-search.js** — the read-via-GAQL → write-via-mutate pattern
  with duplicate-error idempotency.

### examples/
Real scripts that have shipped.

- **exclude-age-demographic.js** — exclude an age range from every ad
  group in matching campaigns, with label-based idempotency and the
  mutate escape hatch. Verified working in production.

## Why this exists

Google Ads Scripts has a wrapped SDK that's pleasant for common
operations (pausing keywords, adjusting bids) and silently absent for
many others (demographic exclusions outside video, PMax signals, asset
group operations). When the wrapper is missing you have to drop down to
the raw API via `mutate()`, and the documentation for that is thin and
scattered across:

- The Scripts reference (wrapped surface only).
- The Google Ads API REST reference (correct field names, wrong
  programming model).
- Forum threads (often outdated).

This skill consolidates the working knowledge into one place that Claude
can reason over while writing or debugging a script with you.

## License

MIT. Use freely.
