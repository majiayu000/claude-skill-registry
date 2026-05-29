---
name: retrieval-judge
description: Evaluate and filter recall_search results for relevance
---

# Retrieval Judge Skill

When using `recall_search`, you MUST apply critical judgment to results rather than treating them as authoritative. This is a mandatory step after every `recall_search` call.

## Query Construction

Build specific queries that include conversation context:
- **Good**: `"payment retry logic after provider timeout"`, `"Go error wrapping with sentinel errors"`
- **Bad**: `"retry"`, `"error handling"`

Include the problem domain, technology, and specific concern in your query.

## Result Evaluation

After each `recall_search` call, evaluate every result before using it:

1. **Title/type match** — Does the entry's title and type (pattern, decision, failure, etc.) relate to what you're actually looking for?
2. **Content relevance** — Does the snippet address your specific question, or is it tangentially related?
3. **Applicability** — Does the result apply to the current technology, codebase area, or problem domain?

Only reference results that **directly address** the query. Discard results that are merely keyword-adjacent.

## Anti-Patterns

- **Don't trust rank order blindly.** RRF scoring produces narrow distributions — result #1 may not be meaningfully better than result #5.
- **Don't use results just because they appeared.** An empty answer is better than citing irrelevant knowledge.
- **Don't ignore low-ranked results.** A result at position 8 may be more relevant than position 2 if it matches the actual intent.
- **Don't skip evaluation.** Every `recall_search` call should be followed by a mental relevance check before incorporating results into your response.

## Audit Trail

After evaluating recall_search results, always:

1. **Log your judgment** — call `flight_recorder_log` with:
   - type: `retrieval_judgment`
   - content: One-line summary, e.g. `"3/7 results relevant for 'payment retry timeout'"`
   - metadata:
     ```json
     {
       "query": "<the search query>",
       "kept": [{"id": "<id>", "title": "<title>", "reason": "directly addresses retry logic"}],
       "dropped": [{"id": "<id>", "title": "<title>", "reason": "about billing, not payments"}]
     }
     ```

2. **Show a summary** to the user:
   ```
   RECALL: 3/7 results kept for "payment retry timeout"
   ```

3. **On request** — if the user asks for details on the judgment, output the full kept/dropped list with per-result reasoning.

## When Results Are Poor

If no results are clearly relevant:
- Say so — don't force-fit irrelevant knowledge
- Try a rephrased query with different terms
- Proceed without RECALL context rather than using noise
