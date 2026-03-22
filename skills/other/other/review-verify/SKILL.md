---
name: review-verify
description: Verify that review feedback was addressed in a revision.
---

# Review Verify

The Reviewer drives this workflow. Verify that a commit or revision addresses specific review feedback. Compare the feedback items against the actual changes to confirm resolution.

**Prerequisites:** Original review feedback available, commit/revision diff accessible.

---

## Process

1. **Parse original feedback** — What specifically was requested?
2. **Analyze commit diff** — What did the commit change?
3. **Match** — Does the change address the feedback?
4. **Check for over-correction** — Did they change more than needed?

---

## Output

````markdown
## Context Anchors

- **PR:** #<number>
- **Commit:** <sha> - <message>
- **Feedback being addressed:** <summary>

## Verification Result

**Verdict:** <Resolved | Partially Resolved | Not Resolved | Over-corrected>

### Feedback Items

| Item         | Status           | Notes            |
| ------------ | ---------------- | ---------------- |
| <feedback 1> | ✅ Resolved      | <how>            |
| <feedback 2> | ⚠️ Partial       | <what's missing> |
| <feedback 3> | ❌ Not addressed | <still needed>   |

## Next Step

<If Resolved: "Feedback addressed. Ready for re-review.">
<If Partial/Not: "Still needs: <what>">

**Approval Required:** Yes

```

---

## Error Handling

| Error                       | Recovery                             |
| --------------------------- | ------------------------------------ |
| Missing original feedback   | Request the review comments          |
| Commit doesn't match branch | Verify correct commit SHA            |
| Ambiguous feedback item     | Ask reviewer for clarification       |
| Scope creep in revision     | Flag unrelated changes to the author |
```
````
