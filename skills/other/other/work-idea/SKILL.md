---
name: work-idea
description: Convert a raw idea from inbox to a worked idea with card and initial Fact-find stage doc using agent APIs.
---

# Work Idea

Transform a raw idea from the inbox into a worked idea, create a corresponding card, and initialize the Fact-find stage document. **All writes go through the agent API (D1 SoT).**

## Operating Mode

**READ + WRITE (API ONLY)**

**Allowed:**
- Read raw idea via `/api/agent/ideas/:id`
- Update idea via `/api/agent/ideas/:id` (move to worked)
- Create card via `/api/agent/cards`
- Create initial Fact-find stage doc via `/api/agent/stage-docs`

**Not allowed:**
- Writing or editing markdown files directly
- Scan-based ID allocation
- Modifying existing cards (use `/propose-lane-move` for lane changes)
- Skipping required fields

**Fail-closed:** If any API call fails, stop and surface the error. Do not write markdown.

## Inputs

**Required:**
- Idea ID (e.g., `BRIK-OPP-0001`)

**Optional:**
- Owner override (default: Pete for Phase 0)
- Business override (if idea is missing or incorrect)

## API Prerequisites

- `BOS_AGENT_API_BASE_URL`
  - Prod: `https://business-os.peter-cowling1976.workers.dev`
  - Local: `http://localhost:3020`
- `BOS_AGENT_API_KEY`
- Header: `X-Agent-API-Key: <value>`

## Worked Idea Quality Rubric

A "worked up" idea must have:

### Required Fields (Idea)
- **Business:** Valid business code (BRIK, PLAT, PIPE, BOS)
- **Status:** "worked"
- **Created-Date:** Original value preserved
- **Content:** Must include a clear summary, opportunity, approach, success criteria, and assumptions

### Scope Clarity
- 1-sentence summary of opportunity
- Impact/value statement
- Clear success criteria or "done" definition

### Completeness Check
- Content is substantive (not placeholder text)
- Business context is clear
- No markdown files written directly

## Workflow

### 1) Read Raw Idea (API)

```json
{
  "method": "GET",
  "url": "${BOS_AGENT_API_BASE_URL}/api/agent/ideas/BRIK-OPP-0001",
  "headers": { "X-Agent-API-Key": "${BOS_AGENT_API_KEY}" }
}
```

If idea does not exist or is not `Status: raw`, stop with error.

### 2) Analyze and Clarify

**Extract/infer business code:**
- Check idea `Business`
- If missing, infer from content
- If unclear, ask Pete

**Clarify scope:**
- Extract core opportunity
- Identify value/impact
- Propose high-level approach
- Add assumptions if scope is uncertain

**Assign owner:**
- Phase 0: default to Pete

### 3) Create Card (API)

Create the card first so you can reference the `cardId` when updating the idea content.

```json
{
  "method": "POST",
  "url": "${BOS_AGENT_API_BASE_URL}/api/agent/cards",
  "headers": {
    "X-Agent-API-Key": "${BOS_AGENT_API_KEY}",
    "Content-Type": "application/json"
  },
  "body": {
    "business": "BRIK",
    "title": "Add user authentication to guide booking flow",
    "description": "Enable users to save preferences and booking history by adding authentication to the guide booking flow.",
    "lane": "Inbox",
    "priority": "P3",
    "owner": "Pete"
  }
}
```

Response:
```json
{ "success": true, "cardId": "BRIK-ENG-0001", "message": "Card created" }
```

### 4) Update Idea → Worked (API)

Use PATCH with JSON Merge Patch and optimistic concurrency. Move location to `worked`, update content, and set Status to `worked`.

```json
{
  "method": "PATCH",
  "url": "${BOS_AGENT_API_BASE_URL}/api/agent/ideas/BRIK-OPP-0001",
  "headers": {
    "X-Agent-API-Key": "${BOS_AGENT_API_KEY}",
    "Content-Type": "application/json"
  },
  "body": {
    "baseEntitySha": "<entitySha from GET>",
    "patch": {
      "Status": "worked",
      "Business": "BRIK",
      "Tags": ["auth", "booking"],
      "location": "worked",
      "content": "# Add user authentication to guide booking flow\n\n## Summary\nEnable users to save their guide preferences and booking history by adding authentication to the Brikette guide booking flow.\n\n## Opportunity\nCurrently users must re-enter information for each booking. Adding authentication would reduce friction and improve conversion.\n\n## Proposed Approach\n1. Integrate platform auth\n2. Optional account creation at booking\n3. User profile with history\n\n## Success Criteria\n- Booking completion rate improves by ≥10%\n- Returning users can auto-fill booking forms\n\n## Assumptions\n- Platform auth is compatible with Brikette\n- No GDPR blockers"
    }
  }
}
```

### 5) Create Initial Fact-find Stage Doc (API)

```json
{
  "method": "POST",
  "url": "${BOS_AGENT_API_BASE_URL}/api/agent/stage-docs",
  "headers": {
    "X-Agent-API-Key": "${BOS_AGENT_API_KEY}",
    "Content-Type": "application/json"
  },
  "body": {
    "cardId": "BRIK-ENG-0001",
    "stage": "fact-find",
    "content": "# Fact-Find: Add user authentication to guide booking flow\n\n## Questions to Answer\n\n1. **User demand:** Do users want account functionality?\n   - Method: Survey recent bookers\n   - Evidence type: customer-input\n\n2. **Technical feasibility:** Can platform auth integrate with Brikette?\n   - Method: Code review\n   - Evidence type: repo-diff\n\n3. **Compliance:** GDPR concerns?\n   - Method: Legal review\n   - Evidence type: legal\n\n4. **Performance:** Will auth slow booking?\n   - Method: Baseline + estimate\n   - Evidence type: measurement\n\n## Findings\n\n_TBD_\n\n## Recommendations\n\n_TBD_"
  }
}
```

## Edge Cases

### Idea already worked
- If Status is not `raw`, stop and return existing state.

### Business code missing or invalid
- Ask Pete. Do not guess.

### Scope too vague
- Ask clarifying questions before creating a card.

### Duplicate opportunity
- Search by Feature-Slug or Plan-Link in existing cards (via `/api/agent/cards?business=...`).

## Integration with Other Skills

- After creating card, recommend `/propose-lane-move` to move to Fact-finding lane
- Use `/fact-find` skill for structured fact-finding

## Example Session (API)

```
User: /work-idea BRIK-OPP-0001

Agent:
1) GET idea via /api/agent/ideas/BRIK-OPP-0001
2) POST /api/agent/cards → cardId
3) PATCH /api/agent/ideas/BRIK-OPP-0001 (Status worked, location worked, new content)
4) POST /api/agent/stage-docs (fact-find)

Done! Card created: BRIK-ENG-0001 (Inbox lane)
Next step: /propose-lane-move BRIK-ENG-0001 to move to Fact-finding
```

## Success Metrics

- Card creation rate: <5 minutes per idea (agent-assisted)
- Rework rate: <10%
- Idea→Card conversion: ≥80% of worked ideas become viable cards

## Phase 0 Constraints

- Pete-supervised (all agent runs are Pete-triggered)
- Agent identity for all API calls
- No direct markdown writes
