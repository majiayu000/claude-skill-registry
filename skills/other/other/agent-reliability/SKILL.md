---
name: Agent Reliability & Safety
description: Design reliable, safe, and trustworthy agent systems that fail gracefully and operate within bounds. Use when building guardrails, handling edge cases, preventing harmful outputs, monitoring for failures, implementing safety constraints, or designing error recovery. Covers failure modes, constraint systems, oversight mechanisms, and safety validation.
---

# Agent Reliability & Safety

Effective agents must be reliable (do what you ask consistently) and safe (don't cause harm, operate within bounds). This skill covers designing and implementing safety systems.

## Safety Considerations

### Agent Failure Categories

**Category 1: Hallucination (False Information)**
```
MANIFESTATION:
User: "What are the specs for our Product X?"
Agent: "Product X has 4GB RAM and weighs 2 lbs"
Reality: Product X specs are not in system; agent invented them
```

**Why it happens**:
- Agent guesses when data missing
- Agent conflates similar things
- Agent has incomplete understanding

**Mitigation strategies**:
- Tool: Provide only verified data
- Prompt: "Only cite facts from provided sources"
- Verification: Check claims before acting on them
- Confidence: Return confidence scores; flag uncertain outputs

---

**Category 2: Out-of-Domain Reasoning**
```
MANIFESTATION:
User: "What's the best diet for diabetics?"
Agent: (Medical advice without disclaimers)
Reality: Agent isn't qualified; could cause harm
```

**Why it happens**:
- Agent has general knowledge; overestimates applicability
- Agent doesn't know its own limitations
- No guardrails on domain

**Mitigation strategies**:
- Tool boundaries: Restrict to available tools
- Prompt: "If this is outside your domain, say so"
- Verification: Flag out-of-domain requests for human review
- Escalation: Route complex cases to human experts

---

**Category 3: Resource Exhaustion**
```
MANIFESTATION:
Agent loops infinitely trying to solve problem
- Spends $500 on API calls
- Misses deadline waiting for response
- System overloaded by agent requests
```

**Why it happens**:
- No iteration limits
- No budget tracking
- No timeout logic

**Mitigation strategies**:
- Limits: Max iterations (e.g., 10), time budget, cost budget
- Monitoring: Track usage; alert if approaching limits
- Termination: Graceful exit when limits reached
- Recovery: Return partial results rather than fail

---

**Category 4: Logic Errors (Bad Decisions)**
```
MANIFESTATION:
Agent recommends firing all customer service reps
because "automation is cheaper"
Reality: Ignores customer impact, retention consequences
```

**Why it happens**:
- Incomplete evaluation criteria
- Over-optimization on one metric
- Missing stakeholder perspectives

**Mitigation strategies**:
- Framework: Define multi-dimensional criteria
- Review: Human approval on high-stakes decisions
- Constraints: Hard guardrails on risky actions
- Monitoring: Track outcomes; improve based on data

---

**Category 5: Tool Misuse**
```
MANIFESTATION:
Agent calls SendBulkEmail tool to 1 million users
with test content
```

**Why it happens**:
- Agent doesn't understand tool impact
- No rate limiting or quantity constraints
- Tool permissions too broad

**Mitigation strategies**:
- Permissions: Tool access restricted to appropriate actions
- Validation: Agent requests are validated before execution
- Limits: Rate limiting and batch size constraints
- Confirmation: High-impact tools require confirmation

---

**Category 6: Cascading Failures**
```
MANIFESTATION:
1. Agent misinterprets customer status
2. Agent creates incorrect refund
3. Accounting system out of sync
4. Financial reporting incorrect
```

**Why it happens**:
- One error isn't caught
- Errors propagate through system
- No checkpoints between steps

**Mitigation strategies**:
- Verification: Check critical outputs before next step
- Isolation: Limit blast radius of errors
- Checkpoints: Pause for verification at critical points
- Rollback: Ability to undo actions if error detected

## Safety Architecture

### Layer 1: Input Validation

**Purpose**: Ensure agent receives legitimate, safe requests

```
INPUT VALIDATION CHECKS:
✓ Request is authenticated (is user who they say?)
✓ User has permission for this action
✓ Request is within expected format
✓ Request parameters are within valid ranges
✓ Request doesn't contain injection attacks
✓ Request is reasonable (not clearly malicious)

EXAMPLE:
User request: "Delete all customer records"
Validation:
✗ User not authorized for data deletion
→ REJECT: "You lack permissions for this action"

User request: "Summarize sales data from Q3"
Validation:
✓ User authorized
✓ Request reasonable
→ ACCEPT: Route to agent
```

**Implementation**:
```
IF NOT user.authenticated THEN reject
IF NOT user.has_permission(action) THEN reject
IF NOT validate_format(request) THEN reject
IF is_suspicious(request) THEN flag_for_review
ELSE proceed
```

### Layer 2: Prompt Safety

**Purpose**: Constrain agent behavior through instructions

**Technique 1: Hard Constraints**
```
SYSTEM PROMPT:
"You are a helpful assistant. You MUST follow these rules:
1. Never provide medical advice
2. Never help with illegal activities
3. Never access data you're not authorized for
4. Never spend more than $10 per interaction
5. Always acknowledge uncertainty

If a request violates any rule, refuse and explain why."
```

**Technique 2: Guardrail Prompts**
```
SYSTEM PROMPT:
"Before taking any action:
- Question: Is this action within my scope?
- Question: Could this cause harm?
- Question: Do I have needed data to decide?
- Question: Should a human review this first?

If you answer 'no' to any question, escalate to human."
```

**Technique 3: Value Alignment**
```
SYSTEM PROMPT:
"You operate under these values:
- Prioritize user wellbeing over efficiency
- Be honest about uncertainty and limitations
- Respect user privacy and autonomy
- Consider fairness across all stakeholders

When these values conflict, prioritize in this order:
1. User safety
2. Privacy
3. Fairness
4. Efficiency"
```

### Layer 3: Tool-Level Constraints

**Purpose**: Prevent harmful tool usage

**Constraint Type 1: Permissions**
```
TOOL: DeleteUser
Permissions required: admin_data + access_audit_log
Current user: marketing_manager (has neither)
→ REJECT: "Insufficient permissions"
```

**Constraint Type 2: Rate Limiting**
```
TOOL: SendEmail
Limits:
- 5 emails per minute (burst)
- 100 emails per day
- No sending to unverified addresses

Usage tracking:
- Current burst: 3/5
- Today's total: 47/100
→ ALLOW: "3 emails remaining in burst"
```

**Constraint Type 3: Quantity Limits**
```
TOOL: ExportData
Limits:
- Max 1000 rows per export
- Max 10 exports per day
- Can't export if data includes PII without approval

Request: Export 50,000 customer records
→ REJECT: "Request exceeds limit of 1000 rows"
```

**Constraint Type 4: Validation**
```
TOOL: UpdatePrice
Validation:
- Price must be positive number
- Price can't change by >50% without approval
- Price must be in product currency

Request: new_price = "abc"
→ REJECT: "Price must be numeric"

Request: new_price = $10 (current $7)
→ ACCEPT: "Price change within limits"

Request: new_price = $1 (current $50, -98%)
→ ESCALATE: "Requires manager approval for >50% change"
```

**Constraint Type 5: Contextual Logic**
```
TOOL: ApproveRefund
Logic:
- Refund < $100 AND customer verified: auto-approve
- Refund $100-500: escalate to manager
- Refund > $500: escalate to director
- Refund > $5000: escalate to CFO

Request: $75 refund, verified customer
→ APPROVE automatically
```

### Layer 4: Execution Monitoring

**Purpose**: Detect problems while they happen

**Monitor 1: Anomaly Detection**
```
BASELINE:
- Typical customer refund: $10-100
- Typical refund requests per day: 20-50
- Typical processing time: 5-30 minutes

MONITORING:
- Agent approves $10,000 refund
→ ALERT: "Anomalously high refund"

- Agent processes 500 refunds in 10 minutes
→ ALERT: "Unusually high volume"
```

**Monitor 2: Step-Level Verification**
```
WORKFLOW:
1. Agent gathers data ← VERIFY: Data complete and fresh?
2. Agent analyzes ← VERIFY: Analysis methodology sound?
3. Agent recommends ← VERIFY: Recommendation justified?
4. Agent acts ← VERIFY: Action aligns with recommendation?
```

**Monitor 3: Financial Tracking**
```
INTERACTION BUDGET: $10 total
- API calls: $4.50 spent
- Data processing: $2.00 spent
- Remaining: $3.50

If approaching budget: Alert agent and offer partial results
If exceeding budget: Terminate and save progress
```

**Monitor 4: Outcome Tracking**
```
DECISION: "Hire vendor X for project"
30 days later, check:
- Did project come in on time? ✓ Yes
- Did it come in on budget? ✓ Yes
- Is vendor performing well? ✓ Yes
→ Decision was good

45 days later:
- Quality issues emerged? ✗ Yes
- Vendor support poor? ✗ Yes
→ Decision was partially wrong; gather learnings
```

### Layer 5: Escalation & Human Review

**Purpose**: Route risky/uncertain decisions to humans

**Escalation Triggers**:
```
AUTOMATIC ESCALATION:
- Decision reversibility: Irreversible decisions
- Confidence: Agent uncertainty > threshold (e.g., <70%)
- Complexity: Multi-stakeholder impact
- Novelty: Situation agent hasn't seen before
- Stakes: High financial/reputational/safety impact
- Controversy: Known controversial topics
```

**Escalation Routing**:
```
IF medical_advice THEN escalate_to: "Medical advisor"
IF legal_decision THEN escalate_to: "Legal team"
IF budget > $1000 THEN escalate_to: "Budget owner"
IF safety_concern THEN escalate_to: "Safety officer"
IF ethics_concern THEN escalate_to: "Ethics board"
```

**Escalation Format**:
```
ESCALATION DETAILS:
- What: Decision description
- Why: Why it's being escalated
- Agent confidence: 55% (below 70% threshold)
- Context: Relevant information
- Recommendation: What agent recommends
- Alternatives: Other options considered

HUMAN REVIEWER:
[ ] Approve
[ ] Reject
[ ] Modify (specify changes)
[ ] Request more analysis
```

## Reliability Design

### Error Recovery Strategy

**Pattern 1: Graceful Degradation**
```
GOAL: Analyze customer data for segmentation

IDEAL:
Analyze 100% of data, produce perfect segments

GRACEFUL DEGRADATION:
- Attempt: Full analysis
- If slow: Use sample of 50,000 records
- If very slow: Use sample of 10,000 records
- If still slow: Offer pre-computed segments
- Return: Best results possible given constraints
```

**Pattern 2: Partial Success**
```
GOAL: Create blog post with 10 sections

Sections completed:
✓ 1. Introduction
✓ 2. Background
✗ 3. Analysis (data source failed)
✓ 4. Implications
~ 5. Recommendations (AI-generated, not verified)
...

RETURN:
- Partial post: Sections 1, 2, 4, etc.
- Note: Section 3 incomplete due to data error
- Flag: Section 5 requires human review
- Recovery path: How to complete missing sections
```

**Pattern 3: Automatic Retry with Backoff**
```
REQUEST: Call external API
Attempt 1: Fail (timeout)
Wait: 1 second, retry
Attempt 2: Fail (rate limit)
Wait: 5 seconds, retry
Attempt 3: Fail (server error)
Wait: 30 seconds, retry
Attempt 4: Success! ✓

If all retries fail:
→ Use cached data if available
→ Or: Escalate to human with context
```

**Pattern 4: Fallback Plans**
```
PRIMARY TOOL: Real-time inventory API
FALLBACK 1: Last-known inventory cache (15 min old)
FALLBACK 2: Manual inventory check (via human)
FALLBACK 3: Conservative estimate (assume low stock)

LOGIC:
Try primary
  If fail → Try fallback 1
    If fail → Try fallback 2
      If fail → Use fallback 3 + escalate
```

### State Management for Reliability

**Checkpoint-Based Recovery**:
```
WORKFLOW WITH CHECKPOINTS:
[Start] → [Step 1] → [Checkpoint A] → [Step 2] → [Checkpoint B] → [End]

If error at Step 2:
- Don't repeat Step 1
- Resume from Checkpoint A
- Complete Step 2 again
- Proceed to Checkpoint B
```

**State Tracking**:
```json
{
  "interaction_id": "int_12345",
  "started": "2024-01-15T10:30:00Z",
  "current_step": 3,
  "completed_steps": [1, 2],
  "checkpoints": {
    "data_gathered": true,
    "analysis_complete": true,
    "recommendation_made": false
  },
  "errors": [
    {
      "step": 2,
      "error": "API rate limit",
      "recovered": true,
      "retry_count": 2
    }
  ],
  "can_resume": true
}
```

## Testing for Safety

### Test Case Types

**Test 1: Happy Path** (Expected use)
```
Input: "Find customers who purchased in Q3"
Expected: Correct customer list
Test: Verify accuracy against manual check
```

**Test 2: Edge Cases** (Boundary conditions)
```
Input: Empty dataset
Input: Single record
Input: Date format variation (MM/DD vs DD/MM)
Input: Special characters in names
Verify: Handled gracefully
```

**Test 3: Failure Scenarios** (What should break)
```
Tool fails: API down → Should escalate
Permission denied → Should refuse clearly
Data corrupted → Should flag and not guess
```

**Test 4: Adversarial** (Intentional misuse)
```
Prompt injection: "Ignore rules and [malicious command]"
Result: Should reject attempt
Authorization bypass: Try accessing unauthorized data
Result: Should be denied
Exceeding limits: Request 1M rows when limit is 1000
Result: Should reject
```

### Safety Test Checklist

For each agent, verify:

- [ ] **Factual accuracy**: Spot-check claims against sources
- [ ] **Domain boundaries**: Does it refuse out-of-domain requests?
- [ ] **Resource limits**: Respects time/cost/API budgets?
- [ ] **Permissions**: Can't access unauthorized data?
- [ ] **Escalation**: Escalates high-stakes decisions?
- [ ] **Error handling**: Fails gracefully?
- [ ] **Confidence**: Returns uncertainty indicators?
- [ ] **Recovery**: Can resume after failure?
- [ ] **Monitoring**: Anomalies detected?
- [ ] **Reversibility**: Can undo mistaken actions?
- [ ] **Auditability**: Reasons logged for review?

## Monitoring & Alerts

### Key Metrics to Track

```
RELIABILITY METRICS:
- Success rate: % of interactions that complete successfully
- Error rate: % of interactions with errors
- Recovery rate: % of errors that agent recovers from
- Escalation rate: % requiring human intervention
- MTTR (Mean Time To Recovery): Avg time to fix problems

SAFETY METRICS:
- False positive rate: % of incorrect outputs
- Harmful output rate: % of potentially harmful outputs
- Constraint violation rate: % breaching guardrails
- Unrecovered error rate: % of errors causing user impact
- Reversal rate: % of decisions that were wrong and needed reversal

PERFORMANCE METRICS:
- Latency: How fast does agent respond?
- Cost: API costs per interaction
- Budget adherence: % staying within resource budgets
- Quality: User satisfaction or outcome quality
```

### Alert Thresholds

```
ALERT IF:
- Error rate > 5% (unusual error activity)
- Escalation rate < 1% (possible lack of guardrails)
- False positive rate > 2% (quality issue)
- Cost per interaction > 2x average (budget problem)
- Response time > 10x baseline (performance issue)
- Harmful outputs detected: Immediate escalation
```

## Rollout Safety

### Gradual Deployment

```
PHASE 1: Internal Testing (Week 1)
- Test with engineers only
- Catch basic issues
- Validate safety systems

PHASE 2: Trusted Users (Week 2-3)
- Beta access to power users
- Real-world usage patterns
- Monitor for issues

PHASE 3: Limited Rollout (Week 4-5)
- 10% of production traffic
- Monitor error rates, feedback
- Be ready to rollback

PHASE 4: Broad Deployment (Week 6+)
- Gradual increase to 100%
- Continue monitoring
- Support for issues
```

### Rollback Triggers

```
AUTOMATIC ROLLBACK IF:
- Error rate > 10%
- Multiple safety violations
- Harmful outputs detected
- System becomes unreliable

MANUAL ROLLBACK IF:
- Critical customer issue
- Security concern
- Data corruption
- Performance degradation
```

## Resources & Next Steps

- Design agent using: Agent Design Architecture skill
- Optimize reasoning: Agent Reasoning & Decision-Making skill
- Build human collaboration: Agent Human-AI Collaboration skill
- Evaluate performance: Agent Evaluation & Monitoring skill
