---
name: synthesize
description: Produce a structured synthesis with summary, recommendation, confidence, and categorized open questions. Use as the final step after research, evaluate, and critique.
allowed-tools: [Read]
---

# Synthesize

Based on everything we have discussed, produce a structured synthesis.

## Persona

If a persona or role was used throughout this analysis, frame the synthesis for that audience:
- Recommendation should resonate with that persona's priorities
- Tradeoffs should reflect what that persona cares about
- Open questions should be ones that persona would ask

The synthesis is the deliverable. Make it useful for the person who needs to act.

## Structure

### Summary
Two to three sentences. What is the core situation and what matters most?

### Critique Integration
Did the critique phase change or refine the recommendation? Summarize what the critique surfaced and how it influenced the final direction. If the critique identified fatal flaws, state how they are addressed. If it did not change the recommendation, explain why the original direction survived scrutiny.

### Recommendation
What should be done? Be direct. If there are options, rank them.

**Confidence: High / Medium / Low**

State why. What evidence supports this confidence level? What would raise or lower it?

### Key Tradeoffs
What are you accepting by going this direction? What is being sacrificed or risked?

### Assumptions That Survived Scrutiny
List the key assumptions that were tested during evaluate and critique and held up. These are the load bearing beliefs underlying the recommendation. If any of these prove wrong, the recommendation should be revisited.

### Open Questions

Categorize unresolved questions into three types:

**Answerable with more research**: Questions that could be resolved with additional investigation, data gathering, or expert consultation.

**Requires future information**: Questions that depend on events or outcomes that have not happened yet. These need monitoring, not more analysis.

**Fundamentally uncertain**: Questions where reasonable people will disagree regardless of evidence. These require a judgment call and should be acknowledged as such.

---

Keep it tight. This is raw material for decisions, not a polished document.

---

After the synthesis, add:

**Ready to commit? Run `/analysis:decide` to lock in your decision.**
