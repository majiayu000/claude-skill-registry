---
name: interpret-feedback
description: "Interpret third-party feedback by running parallel internal and peer interpretations to surface intent, correctness concerns, and ambiguities. Use when the user asks to \"interpret feedback\", \"interpret comments\", \"what does this feedback mean\", \"clarify reviewer intent\", \"understand this review\", or \"interpret these suggestions\"."
---

# Interpret Feedback

Run two independent interpretations of third-party feedback in parallel (internal + codex peer), then reconcile into enriched items with clear intent summaries. Designed for feedback where the author's intent is ambiguous or the correctness of suggestions is uncertain.

## Step 1: Identify Feedback Items

Determine the feedback to interpret:

- If feedback items are in conversation context, use them
- If a file path or URL was provided, read or fetch the content
- If called by another skill, use the items passed in

For each item, collect whatever context is available: code snippets, diffs, surrounding discussion, file paths, line numbers. More context produces better interpretation.

## Step 2: Run Two Interpretations in Parallel

Launch two Agent tool calls in a single message (`model: "opus"`, do not set `run_in_background`):

### Internal Interpretation

Spawn a subagent with the feedback items and all available context. Instruct it to:

1. Read all referenced code and surrounding context
2. For each feedback item, produce:
   - **Intent**: What the feedback author most likely wants changed and why (one to two sentences)
   - **Correctness**: Whether the suggestion is technically sound — flag concerns if the reviewer may be mistaken, with evidence
   - **Ambiguity**: Note where the intent is unclear or where multiple valid readings exist
3. Return structured results per item

### Run `/peer-review` Skill

Spawn a subagent whose prompt includes the feedback items, all available context, and the following review prompt, and instructs it to invoke `/peer-review` via the Skill tool:

```
<task>
Interpret the following third-party feedback items. For each item, determine: what the author most likely wants changed and why, whether the suggestion is technically sound, and where the phrasing is ambiguous enough to support multiple valid readings.
</task>

<dig_deeper_nudge>
Do not take feedback at face value. Check whether the author's stated concern matches the code reality. Look for cases where the reviewer misread the code, confused two similar constructs, or applied a general rule that does not fit this specific context.
</dig_deeper_nudge>

<structured_output_contract>
For each feedback item, return:
1. Intent — what the author most likely wants changed and why (one to two sentences)
2. Correctness — whether the suggestion is technically sound. If not, explain what the reviewer likely misunderstood, with evidence from the code
3. Ambiguity — if the intent supports multiple valid readings, list each reading and which has stronger evidence
4. Confidence — high (clear intent, sound suggestion), medium (likely intent but some uncertainty), or low (genuinely ambiguous or likely incorrect)
</structured_output_contract>
```

## Step 3: Reconciliation

Merge the two interpretations for each feedback item:

| Agreement | Action |
|-----------|--------|
| **Both agree** on intent and correctness | High confidence. Use the shared interpretation. |
| **Intent agrees, correctness differs** | Flag the correctness concern with both perspectives. |
| **Intent disagrees** | Flag as ambiguous. Present both readings and note which has stronger evidence. |

## Step 4: Output Enriched Items

For each feedback item, output the original feedback followed by the interpretation:

```
### Item <N>: <short label>

**Original:** <feedback text, truncated if long>
**File:** <path:line if applicable>

**Intent:** <reconciled interpretation of what the author wants>
**Correctness:** <sound | concern: <explanation>>
**Confidence:** <high | medium | low>
**Ambiguity:** <none | <description of unclear aspects>>

<If interpreters disagreed, show both perspectives>
```

After all items, add a summary:

```
## Interpretation Summary

- Total items: <N>
- High confidence: <N>
- Correctness concerns: <N>
- Ambiguous intent: <N>
```

## Rules

- If either interpretation agent is unavailable or returns malformed output, proceed with results from the remaining agent.
