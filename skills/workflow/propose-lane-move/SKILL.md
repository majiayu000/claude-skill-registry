---
name: propose-lane-move
description: Propose lane transitions for Business OS cards based on stage document evidence and completion criteria.
---

# Propose Lane Move

Analyze a Business OS card's current state and propose a lane transition based on evidence from stage documents and completion criteria. The agent proposes; Pete approves and executes the move.

## Operating Mode

**READ-ONLY ANALYSIS + PROPOSAL**

**Allowed:**
- Read card data via agent API
- Read all stage documents via agent API
- Analyze evidence against lane transition criteria
- Update card's `Proposed-Lane` field via API PATCH

**Not allowed:**
- Moving card to new lane (Pete does this via UI after approval)
- Creating stage documents (use `/work-idea` for that)
- Modifying lane transition rules

## Inputs

**Required:**
- Card ID (e.g., `BRIK-ENG-0001`)

**Optional:**
- Target lane (if Pete has a specific lane in mind; otherwise agent recommends)

## Lane Transition Criteria

### From Inbox → Fact-finding
- **Evidence required:** None (always allowed)
- **Action:** Agent creates `fact-find` stage doc via `/work-idea` (API-backed)

### From Fact-finding → Planned
- **Evidence required:**
  - Fact-finding stage doc exists and contains findings
  - Key questions answered or marked as assumptions
  - Blast radius understood
  - Evidence sources documented (measurement, customer-input, repo-diff, experiment, etc.)
- **Recommendation:** Create plan (separate task) before proposing move

### From Planned → In progress
- **Evidence required:**
  - Plan stage doc exists with clear acceptance criteria
  - Dependencies resolved (no blocking cards)
  - Owner assigned
  - Confidence ≥80% (if measurable)

### From In progress → Done
- **Evidence required:**
  - All acceptance criteria met
  - Tests passing
  - Code changes committed
  - No open blockers

### From In progress → Blocked
- **Evidence required:**
  - Blocker documented in stage doc or comments
  - Blocker card created and linked (if applicable)

### From Done → Reflected
- **Evidence required:**
  - Reflection stage doc created with outcomes, learnings, metrics
  - Any follow-up cards created
  - Business plan updated (if applicable)

### From any lane → Inbox (reset)
- **Evidence required:** Fundamental change in approach or requirements
- **Recommendation:** Document reason in comments

### Archiving (Dropped/Retired)
- **Not handled by this skill** - use archive mechanism separately

## Workflow

1. **Read card + stage docs via agent API**
   ```json
   {
     "method": "GET",
     "url": "${BOS_AGENT_API_BASE_URL}/api/agent/cards/BRIK-ENG-0001",
     "headers": { "X-Agent-API-Key": "${BOS_AGENT_API_KEY}" }
   }
   ```
   ```json
   {
     "method": "GET",
     "url": "${BOS_AGENT_API_BASE_URL}/api/agent/stage-docs?cardId=BRIK-ENG-0001",
     "headers": { "X-Agent-API-Key": "${BOS_AGENT_API_KEY}" }
   }
   ```

2. **Analyze current lane and evidence**
   - Check what stage docs exist
   - Verify evidence completeness against criteria above
   - Check for blockers (Dependencies field, comments)

3. **Determine eligible target lanes**
   - Based on current lane and available evidence
   - Consider forward progression (Inbox → ... → Reflected)
   - Consider lateral moves (In progress → Blocked, back to Planned)

4. **Propose lane**
   - Update card's `Proposed-Lane` field via API PATCH
   - Add comment explaining rationale and evidence references
   - Example:
     ```markdown
     ## Lane Move Proposal: Fact-finding → Planned

     **Evidence:**
     - Fact-finding stage doc complete (API stage `fact-find`)
     - Key questions answered in FAQ section
     - Blast radius: Medium (affects 3 files in `apps/brikette/src/components/`)
     - Evidence sources: repo-diff (commit abc123), measurement (page load reduced 200ms)

     **Recommendation:** Create plan doc before moving to Planned lane.
     ```

5. **Persist proposal via API**
   ```json
   {
     "method": "PATCH",
     "url": "${BOS_AGENT_API_BASE_URL}/api/agent/cards/BRIK-ENG-0001",
     "headers": {
       "X-Agent-API-Key": "${BOS_AGENT_API_KEY}",
       "Content-Type": "application/json"
     },
     "body": {
       "baseEntitySha": "<entitySha from GET>",
       "patch": { "Proposed-Lane": "Planned" }
     }
   }
   ```

   **Conflict handling:** if PATCH returns 409, refetch and retry once. If it conflicts again, stop and surface the error.

## Evidence Quality Checks

Before proposing a move, verify:

- **Evidence sources are typed** (use evidence type enum from BOS-26)
- **Evidence is specific** (links to files, commits, metrics, not vague statements)
- **Evidence is recent** (prefer data from last 30 days for active cards)
- **Assumptions are explicit** (mark any unknowns clearly)

## Edge Cases

### Card has multiple blockers
- Propose `In progress → Blocked`
- List all blockers in proposal comment
- Recommend creating blocker cards if they don't exist

### Evidence is weak/missing
- Do NOT propose move
- Recommend specific evidence gathering steps
- Example: "Run performance benchmarks before proposing Done"

### Proposed-Lane already set
- Check if proposal is still valid
- If new evidence warrants different lane, update proposal
- If proposal is stale (>7 days), recommend refreshing

### Dependencies unresolved
- Do NOT propose `Planned → In progress`
- List unresolved dependency card IDs
- Check dependency card status and estimate timeline

## Integration with Other Skills

- Use `/work-idea` to create Fact-finding stage doc before proposing Inbox → Fact-finding
- Use `/scan-repo` to gather repo evidence for proposals
- Follow up proposal with `/update-business-plan` if lane move affects strategy

## Example Session

```
User: /propose-lane-move BRIK-ENG-0001

Agent:
I'll analyze BRIK-ENG-0001 and propose a lane move.

[Reads card: currently in Fact-finding lane]
[Reads stage docs: fact-find stage exists]
[Checks evidence: contains repo-diff evidence, measurement data, clear findings]

Based on the analysis:

**Current lane:** Fact-finding
**Proposed lane:** Planned
**Evidence:**
- Fact-finding stage doc complete with 3 key findings
- Evidence: repo-diff (8 files analyzed), measurement (200ms improvement confirmed)
- No blocking dependencies identified
- Blast radius: Medium (3 components in apps/brikette)

**Next steps:**
1. Create plan stage doc with acceptance criteria
2. Pete reviews and approves via card edit UI
3. Move to Planned lane

I'll now update the card's Proposed-Lane field.

[Commits change with agent identity]

Done! Proposal added to BRIK-ENG-0001. Pete can review in the card detail view.
```

## Error Handling

- **Card not found:** Return clear error with card ID
- **No stage docs:** Recommend starting with Fact-finding
- **Insufficient evidence:** List specific missing evidence, don't propose move
- **Invalid target lane:** Explain lane progression rules

## Phase 0 Constraints

- Pete-only approval (no automated approvals)
- Agent identity used for all proposal commits
- UI shows Proposed-Lane but Pete must manually update Lane field
- Fail-closed: if API is unavailable or conflicts after retry, stop and surface the error
- No notification system (Pete checks boards manually)

## Success Metrics

- Proposals approved without modification: >80%
- Evidence completeness: All proposals reference specific stage doc sections
- Proposal turnaround: <2 days from proposal to approval (Pete's discretion)
