---
name: review-and-promote-traces
description: Judge flagged trace outputs and promote judged items back to datasets. Use when an evaluation run requires human judgment or when review queue items need to be judged for promotion into the dataset.
---

# Review and Promote Traces

Use this skill for the judgment and promotion loop after trace evaluation.

## Interactive Q&A protocol (mandatory)

<HARD-GATE>
BEFORE the first scoping question, search for a structured question tool (e.g., `AskUserQuestion` or similar interactive widget) and load it. Use that tool for EVERY scoping question. Fall back to plain-text lettered options ONLY if no such tool exists in the environment.
</HARD-GATE>

If context is unclear, ask one question at a time using the structured question tool (loaded per the HARD-GATE above).

Example question structure:

```
What do you want to review first?
A) One specific run
B) Pending queue triage across runs
```

Rules:
- Ask one question per message.
- Use the structured question tool for every question. Structure each with a short header, 2-4 options with labels and descriptions, and place the recommended option first. Do not add "(Recommended)" or similar annotations to option labels.
- Ask one follow-up when needed, then continue.

## Workflow

1. If needed, flag evaluated run:
   - Use `flag_review_item` with `run_id`.
2. Retrieve review items:
   - Use `list_review_items` with pagination.
3. Collect human judgments:
   - Present review items to the user and ask for judgment one item at a time when needed.
   - Capture `judgment_value` and optional `notes` for each item.
   - Use the structured question tool (loaded per the HARD-GATE above) to present options that match the live evaluation setup:
     - Binary example:
       - A) Pass
       - B) Fail
     - Categorical example:
       - A) <option 1>
       - B) <option 2>
       - C) <option 3>
     - Continuous example:
       - A) Enter numeric value (within configured range)
       - B) Skip this item for now
   - If valid options are unclear, look them up before asking:
     1) Inspect `list_review_items` payload for item result details and expected value hints.
     2) Use `get_result(run_id)` for run-level context and chain outputs.
     3) If evaluation id is available in run metadata, call `get_evaluation(evaluation_id)` and read config/judgment criteria to derive valid judgment options.
   - When options remain ambiguous after lookup, ask one clarification question using the structured question tool before proceeding.
4. Submit judgments:
   - For each target item, call `judge_review_item`.
   - Pass the user-provided `judgment_value` and optional `notes` into `judge_review_item`.
   - Include notes when judgment context matters.
5. Promote judged outputs:
   - Use `add_reviewed_items_to_dataset` with `run_id`.
6. Report result:
   - number of items judged
   - promotion status and row counts
   - any skipped or blocked items

## Queue-wide triage guidance

- Group by run and status first.
- Prioritize high-impact runs or oldest pending runs.
- Keep an audit trail of judgment rationale in notes.

## Scopes reference

- `list_review_items` requires `review:read`
- `flag_review_item`, `judge_review_item`, and `add_reviewed_items_to_dataset` require `review:write`

If a scope error occurs, ask the user to create a key with the missing scope in Truesight Settings.
