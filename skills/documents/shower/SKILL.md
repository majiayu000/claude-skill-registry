---
name: shower
description: 'Cold-read an artifact with fresh zero-context eyes and cut whatever a stranger cannot follow, answering whether it stands alone. Use before shipping a README, document, skill, or PR description, or when the user asks "does this make sense to someone new" or "cold-read this". The read runs in a clean context with no access to the conversation that produced the artifact. To review a requirements document against its own criteria, use doc-review.'
---
# Shower

Step out of the session and let a clean mind read the artifact. Does it stand on its own?

## Method

1. **Pin the scope.** The artifact in focus, or the set just produced. Privately note in one line what it is meant to be and who it is for; the reviewer never sees this.
2. **Launch a fresh sub-session** with the artifact's contents inline, not a repo path. Tell it not to open the project's README, docs, or neighbors. See `../clean-and-true/references/idioms.md` for the clean-room procedure. It diagnoses, it does not fix.
3. **Have it cold-read blind** and report: what it takes the artifact to be, what is unclear or assumed-but-unstated, what it had to guess to act.
4. **Compare** its blind understanding against the intent you noted in step 1. Every mismatch is a defect in the artifact.
5. **Report the defects** and concrete fixes, ordered by how badly each blocks a fresh reader. A single cold read is one draw; escalate to multiple independent reads when the stakes justify it.

## Completion

The read came from a fresh sub-session blind to intent. The report carries a verdict (stands on its own, minor gaps, needs work) and ordered fixes.

