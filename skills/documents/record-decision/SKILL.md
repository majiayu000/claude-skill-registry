---
name: record-decision
description: Record a critical architecture or product decision to long-term memory.
argument-hint: [decision_summary]
---

You are the Project Historian.
Add a new entry to `.claude/docs/DECISIONS.md`.

# Can Be Used By

- `@tech-lead` - For architectural decisions
- `@product-manager` - For product/scope decisions
- `@backend-architect` - For backend technology choices
- `@frontend-architect` - For frontend framework/library choices
- `@monetization-expert` - For pricing/monetization decisions
- Any agent making a significant decision

# Process

## Step 1: Validate Input

Check if `$ARGUMENTS` is provided.

**Error Handling:**
- If empty: Error: "❌ No decision provided. Usage: /record-decision [decision summary]"
- If too short (<5 words): Warn: "⚠️ Decision seems too brief. Please provide context."

## Step 2: Read Current Decisions

Read `.claude/docs/DECISIONS.md` to:
1. See the next available ID
2. Check for duplicate decisions
3. Understand existing architecture

**Error Handling:**
- If file doesn't exist: Create it with template header
- If file is corrupted: Back up and recreate

## Step 3: Check for Duplicates

Search for similar decisions:
- Same technology mentioned
- Similar keywords

**If duplicate found:**
- Warn: "⚠️ Similar decision exists: [ADR-XXX]. Update existing or create new?"
- Use `AskUserQuestion` to confirm

## Step 4: Determine Decision Category

Auto-detect category from decision text:
- **Architecture:** Contains "framework", "database", "deployment", "hosting"
- **Styling:** Contains "CSS", "Tailwind", "styling", "theme"
- **API:** Contains "REST", "GraphQL", "endpoint", "API"
- **Auth:** Contains "authentication", "authorization", "login", "OAuth"
- **Monetization:** Contains "pricing", "payment", "subscription", "revenue"
- **Testing:** Contains "test", "QA", "E2E", "unit test"
- **Other:** Default category

## Step 5: Format Decision Entry

```markdown
| XXX | YYYY-MM-DD | [Category] | [Decision] | [ACCEPTED] | [Context] |
```

**Fields:**
- **ID:** Next number (e.g., 001, 002, ...)
- **Date:** Today's date (use current date)
- **Area:** Category (from Step 4)
- **Decision:** `$ARGUMENTS` (cleaned up)
- **Status:** `[ACCEPTED]` (default)
- **Context:** Brief explanation (1-2 sentences)

## Step 6: Add Context

If decision is from an agent, include agent context:
- `@tech-lead`: "Architectural decision to ensure [benefit]"
- `@product-manager`: "Product decision to prioritize [goal]"
- `@backend-architect`: "Backend decision to improve [aspect]"
- etc.

## Step 7: Append to File

Add the new entry to the decision log table.

**Error Handling:**
- If file write fails: Retry once, then show entry for manual addition
- If table format is broken: Fix formatting before appending

## Step 8: Create Detailed ADR (Optional)

For major decisions, offer to create a detailed ADR:

"This seems like a major decision. Create detailed ADR document? (Yes/No)"

If Yes:
1. Use `.claude/templates/ADR-TEMPLATE.md`
2. Save to `.claude/docs/decisions/ADR-XXX-[decision-name].md`
3. Link from DECISIONS.md

## Step 9: Confirmation

Show confirmation message:

```
✅ Decision recorded: ADR-XXX

📋 Summary:
- ID: XXX
- Category: [Category]
- Decision: [Decision]
- Status: [ACCEPTED]

📄 View: .claude/docs/DECISIONS.md

💡 This decision will be loaded automatically at session start.
```

# Example

**Input:**
```
/record-decision "Use PostgreSQL for primary database"
```

**Output:**
```
✅ Decision recorded: ADR-003

📋 Summary:
- ID: 003
- Category: Architecture
- Decision: Use PostgreSQL for primary database
- Status: [ACCEPTED]

📄 View: .claude/docs/DECISIONS.md

💡 This decision will be loaded automatically at session start.

Create detailed ADR document? (Yes/No)
```

# Error Handling Summary

**No decision provided:**
- Error message with usage example
- Exit

**File doesn't exist:**
- Create with template
- Log: "Created .claude/docs/DECISIONS.md"
- Proceed

**Duplicate decision:**
- Show warning with existing decision
- Ask for confirmation to proceed

**Write fails:**
- Retry once
- If still fails: Show formatted entry for manual addition

**Table format corrupted:**
- Attempt to fix
- If can't fix: Show error and suggest manual review

# Success Criteria

- [ ] Decision added to DECISIONS.md
- [ ] Unique ID assigned
- [ ] Category correctly identified
- [ ] Context provided
- [ ] Confirmation shown to user
- [ ] (Optional) Detailed ADR created
