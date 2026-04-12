---
name: ice-score
description: "Use to prioritize solutions or opportunities using ICE scoring with evidence-backed confidence."
---

# ICE Score Skill

ICE scoring with integrated confidence meter.

## Workflow

1. **List items to score** (opportunities, solutions, or features).

2. **For each item, score three dimensions (1-10)**:

   **Impact**: How much will this move the target metric?
   - 1-3: Marginal improvement. Nice to have.
   - 4-6: Meaningful improvement. Moves the needle.
   - 7-10: Transformative. Changes the game.
   - Evidence: What data supports this impact estimate?

   **Confidence**: How sure are we about the impact estimate?
   - 1-3: Gut feel. No data. Assumption.
   - 4-6: Some evidence. Indirect signals. Analogous examples.
   - 7-10: Strong evidence. Direct user research. Quantitative data.
   - Evidence: What specific data points back this confidence?

   **Ease**: How easy is this to implement and ship?
   - 1-3: Major effort. Multiple sprints. New capabilities needed.
   - 4-6: Moderate effort. Known patterns. Some complexity.
   - 7-10: Quick win. Existing patterns. Low risk.
   - Evidence: What technical assessment supports this?

3. **Calculate ICE score**: Impact x Confidence x Ease

4. **Rank items** by ICE score.

5. **Apply bias check**: Are high-scoring items benefiting from availability bias, IKEA effect, or anchoring?

6. **Output**:
   ```
   | Item | Impact | Confidence | Ease | ICE | Top Evidence |
   |------|--------|-----------|------|-----|-------------|
   | ...  | X (why) | X (why) | X (why) | XXX | [source] |
   ```

## Rules
- Every score must have a brief justification.
- Confidence of 7+ requires direct evidence (not analogy or assumption).
- If all items score similarly, the scoring criteria need refinement.
- Review for bias after scoring, before acting.

## Canvas Output
Update `canvas/opportunities.yml` with solution ICE scores.
Update `canvas/gist.yml` with idea ICE scores and confidence levels.

## Theory Citations
- Gilad: Evidence-Guided (confidence-backed prioritization)
- Kahneman: Thinking, Fast and Slow (bias in estimation)
