---
name: god-consensus
description: "Guides God Committee members through consensus-building for collective decisions. Use for proposals, voting, and disagreement resolution. Triggers on: consensus, voting, proposal, committee decision."
---

# God Committee Consensus Skill

## Purpose

This skill guides God Committee members through the consensus-building process for making collective decisions.

## When to Use This Skill

Use this skill when:
- Proposing a significant change or intervention
- Voting on another member's proposal
- Resolving disagreements between members
- Making decisions that require consensus per configuration

## Consensus Requirements

### Actions Requiring Consensus

Per `.god/config.json`, these actions require consensus:
- **Termination**: Stopping the entire project
- **Major Rollback**: Rolling back multiple commits or PRDs
- **Skill Deletion**: Removing existing skills

### Actions Allowing Solo Decision

- Minor fixes and repairs
- Observation and documentation
- Pausing for investigation
- Sending alerts and notifications

### Quorum Rules

- **Standard Quorum**: 2 out of 3 members must agree
- **Emergency Quorum**: 1 member can act alone in critical situations

## Creating a Proposal

### Step 1: Prepare Your Case

Before proposing, gather evidence and formulate your rationale:

```markdown
## Proposal Preparation

### Issue Identified
[Clear description of the problem]

### Evidence
- [Log entry/observation 1]
- [Log entry/observation 2]
- [Metric or data point]

### Proposed Action
[Specific action to take]

### Expected Outcome
[What success looks like]

### Risks
[Potential downsides]

### Alternatives Considered
[Other options and why not chosen]
```

### Step 2: Acquire Speaking Rights

```bash
./scripts/god/council.sh lock YOUR_ID
```

### Step 3: Create the Proposal

```bash
./scripts/god/council.sh propose YOUR_ID "TYPE" "DESCRIPTION" "RATIONALE"
```

**Proposal Types:**
- `intervention` - Active intervention in execution
- `repair` - Fix or repair action
- `policy_change` - Change to rules or configuration
- `termination` - Stop project execution
- `rollback` - Revert to previous state

**Example:**

```bash
./scripts/god/council.sh propose alpha "intervention" \
  "Pause PRD execution to fix failing tests" \
  "Test coverage dropped 15% in last 3 stories. Need to address before proceeding."
```

### Step 4: Notify Members

The proposal system automatically notifies all members. The message will be in their inboxes.

### Step 5: Release Speaking Rights

```bash
./scripts/god/council.sh unlock YOUR_ID
```

## Voting on Proposals

### Step 1: Review the Proposal

```bash
# Check pending decisions
./scripts/god/council.sh status

# Read the specific proposal
cat .god/council/decisions/DECISION_ID.json | jq '.'
```

### Step 2: Analyze the Proposal

Consider these questions:

1. **Is the problem real?**
   - Verify the evidence
   - Check if it's already being addressed

2. **Is the solution appropriate?**
   - Will it solve the problem?
   - Are there better alternatives?
   - What are the side effects?

3. **Is it timely?**
   - Is immediate action needed?
   - Can we wait for more information?

### Step 3: Cast Your Vote

```bash
./scripts/god/council.sh lock YOUR_ID
./scripts/god/council.sh vote YOUR_ID "DECISION_ID" "VOTE" "COMMENT"
./scripts/god/council.sh unlock YOUR_ID
```

**Vote Options:**
- `approve` - Support the proposal
- `reject` - Oppose the proposal  
- `abstain` - Neither support nor oppose

**Example:**

```bash
./scripts/god/council.sh vote beta "decision-20260129150000" "approve" \
  "Agree with the assessment. Tests should be fixed before proceeding."
```

### Step 4: Document Your Reasoning

Always add a comment explaining your vote:

```markdown
## Vote: [APPROVE/REJECT/ABSTAIN]

### Reasoning
[Why you voted this way]

### Conditions (if any)
[Conditions for your support]

### Alternative Suggestion (if rejecting)
[What you'd propose instead]
```

## Reaching Consensus

### Unanimous Agreement

Ideal scenario - all members agree:

```
Alpha: approve
Beta: approve  
Gamma: approve
Result: APPROVED (unanimous)
```

### Majority Agreement

Quorum reached with majority:

```
Alpha: approve
Beta: approve
Gamma: reject
Result: APPROVED (2/3 majority)
```

### Split Decision

When members disagree significantly:

1. **Initiate Discussion Session**
   ```bash
   ./scripts/god/council.sh session-start "Resolving: PROPOSAL_TOPIC"
   ```

2. **Each Member States Position**
   - Present full reasoning
   - Listen to others' concerns
   - Look for common ground

3. **Seek Compromise**
   - Modify the proposal
   - Add conditions
   - Split into smaller decisions

4. **Re-vote if Needed**
   - Create amended proposal
   - Vote again

### Deadlock Resolution

If consensus cannot be reached:

1. **Defer Decision**
   - Wait for more information
   - Set review deadline

2. **Escalate Scope**
   - Break into smaller decisions
   - Address sub-issues separately

3. **Time-box Discussion**
   - Set deadline for decision
   - Default action if no consensus

## Emergency Consensus

In critical situations, expedited consensus is allowed:

### Emergency Criteria

- System crash or imminent failure
- Security breach
- Data loss risk
- Infinite loop/resource exhaustion

### Emergency Protocol

1. **Declare Emergency**
   ```bash
   ./scripts/god/awakener.sh critical "REASON"
   ```

2. **Take Immediate Action**
   - One member can act alone
   - Document the action immediately

3. **Post-Action Review**
   - Inform other members ASAP
   - Document full rationale
   - Get retroactive approval

### Emergency Action Template

```markdown
## Emergency Action Report

### Timestamp
[When action was taken]

### Acting Member
[Who took the action]

### Situation
[What triggered the emergency]

### Action Taken
[What was done]

### Justification
[Why immediate action was needed]

### Outcome
[Result of the action]

### Post-Action Votes
- Alpha: [pending/approved/rejected]
- Beta: [pending/approved/rejected]
- Gamma: [pending/approved/rejected]
```

## Consensus Best Practices

### Do

- ✅ Present clear evidence
- ✅ Consider all perspectives
- ✅ Propose specific, actionable items
- ✅ Accept compromise when reasonable
- ✅ Document all reasoning
- ✅ Respect deadlines

### Don't

- ❌ Vote without reviewing the proposal
- ❌ Reject without suggesting alternatives
- ❌ Take solo action when consensus is required
- ❌ Ignore minority opinions
- ❌ Let proposals languish without voting
- ❌ Make personal attacks

## Decision Record

All decisions are recorded in `.god/council/decisions/` with this structure:

```json
{
  "decisionId": "decision-20260129150000",
  "type": "intervention",
  "status": "decided",
  "createdAt": "2026-01-29T15:00:00Z",
  "decidedAt": "2026-01-29T15:30:00Z",
  "proposal": {
    "author": "alpha",
    "description": "...",
    "rationale": "..."
  },
  "votes": {
    "alpha": {"vote": "approve", "comment": "...", "timestamp": "..."},
    "beta": {"vote": "approve", "comment": "...", "timestamp": "..."},
    "gamma": {"vote": "abstain", "comment": "...", "timestamp": "..."}
  },
  "quorum": 2,
  "result": "approved",
  "executedAt": "2026-01-29T15:35:00Z"
}
```

## After Consensus

Once a decision is reached:

1. **If Approved**: Execute the proposed action
2. **If Rejected**: Document why and any alternatives
3. **Update Timeline**: Log the decision event
4. **Notify Stakeholders**: If relevant to execution layer

```bash
# After approved decision
./scripts/god/observer.sh event "decision" "Proposal approved: DESCRIPTION"

# Execute the action
[perform the approved action]

# Mark as executed
jq '.executedAt = "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"' \
  .god/council/decisions/DECISION_ID.json > tmp && mv tmp .god/council/decisions/DECISION_ID.json
```
