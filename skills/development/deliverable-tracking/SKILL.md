---
name: deliverable-tracking
description: 'Create GitHub Issues for client deliverables in DaveX2001/deliverable-tracking
  repo (discovery: requirements-clarity). Evaluate at requirements-clarity when user
  mentions tracking, deliverables, commi'
---

---
name: deliverable-tracking
description: Create GitHub Issues for client deliverables in DaveX2001/deliverable-tracking repo (discovery: requirements-clarity). Evaluate at requirements-clarity when user mentions tracking, deliverables, commitments, or "create deliverable". Extracts What/Why/Done from conversation context, prompts for missing info via AskUserQuestion, applies dynamic client labels.
---

# Deliverable Tracking

Create structured GitHub Issues for client deliverables after clarity phases establish shared understanding.

## Workflow

### Step 1: Extract from Conversation Context

Review the conversation above to extract:
- **What?** - The deliverable description (from Requirements-Clarity)
- **Why?** - Motivation/importance (from Requirements-Clarity)
- **Definition of Done** - Success criteria (from Evaluation-Clarity)
- **Notes** - Any references, blockers, or context mentioned (optional)
- **Client** - Which client this deliverable is for

### Step 2: Prompt for Missing Info

Use AskUserQuestion to gather any fields not clearly extractable from context:

```
Required fields:
- Client name (for label and title prefix)
- Brief description (for title)
- What (if not clear from conversation)
- Why (if not clear from conversation)
- Definition of Done (if not clear from conversation)

Optional:
- Notes (references, blockers, context)
```

Format questions with 2-4 concrete options when possible. For free-form input, let user select "Other".

### Step 3: Create GitHub Issue

**Title format:** `{Client}: {Brief description}`

**Body format:**
```markdown
## What?
[Deliverable description]

## Why?
[Motivation/importance]

## Definition of Done
[Success criteria - how we know it's complete]

## Notes
[Optional: references, blockers, context]
```

### Step 4: Apply Client Label

Check if client label exists:
```bash
gh label list --repo DaveX2001/deliverable-tracking | grep -i "{client}"
```

If label doesn't exist, create it with client color:
```bash
gh label create "{client}" --repo DaveX2001/deliverable-tracking --color "C5DEF5" --description "{Client} client"
```

Create the issue with label:
```bash
gh issue create --repo DaveX2001/deliverable-tracking \
  --title "{Client}: {Brief description}" \
  --body "{formatted body}" \
  --label "{client}"
```

### Step 5: Confirm Creation

Report the created issue URL back to user.
