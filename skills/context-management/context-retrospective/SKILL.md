---
name: context-retrospective
description: Analyze agent-user interaction transcripts to identify context network maintenance needs and guidance improvements. Use after significant agent interactions or to improve context networks.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Context Network Retrospective

## Purpose

Analyze agent-user interaction transcripts to identify context network maintenance needs and guidance improvements. Extract actionable insights for enhancing both network structure and agent instructions.

## Core Principle

**Learn from every interaction.** Each transcript reveals gaps in context, navigation issues, and guidance problems that can be systematically fixed.

---

## Analysis Dimensions

### 1. Knowledge Gap Identification

**Look For:**
- Questions agent couldn't answer from existing context
- Information discovered during task that should be pre-documented
- Repeated lookups of same information
- Agent confusion about structure, relationships, dependencies

**Questions:**
- What foundational knowledge was missing?
- Which relationships weren't documented?
- What context about history, decisions, or constraints was absent?
- Which domain boundaries were unclear?

**Output:** Missing information nodes and relationship gaps

---

### 2. Context Boundary Violations

**Look For:**
- Planning documents created outside context network
- Implementation files placed in context areas
- Agent uncertainty about where to place information
- Mixed concerns within single documents

**Questions:**
- Did agent distinguish context from project artifacts?
- Were "planning stays in context network" rules followed?
- What guidance would prevent future confusion?

**Output:** Boundary violations and guidance improvements needed

---

### 3. Navigation and Discovery Patterns

**Look For:**
- How agent found (or failed to find) information
- Sequences of information access
- Dead ends or inefficient paths
- Information that should have been connected

**Questions:**
- What navigation paths did agent follow?
- Which information should be more discoverable?
- What logical connections were missing?
- What hub documents would improve efficiency?

**Output:** Navigation improvements and missing connections

---

### 4. Task-Context Alignment

**Look For:**
- Mismatches between task needs and available context
- Information at wrong abstraction levels
- Context too detailed or too high-level
- Task patterns revealing organizational weaknesses

**Questions:**
- Was information at appropriate abstraction for the task?
- Did context support decision-making needs?
- Were there cognitive load issues from organization?
- What restructuring would support this task type?

**Output:** Abstraction adjustments and reorganization needs

---

### 5. Relationship Mapping Deficiencies

**Look For:**
- Agent difficulty understanding dependencies
- Missing context about how changes affect other areas
- Lack of clear interface definitions
- Implicit relationships that should be explicit

**Questions:**
- What relationships were implied but not documented?
- Which dependencies were discovered during task?
- What impact relationships were unclear?
- Where would explicit documentation have helped?

**Output:** Missing relationships and documentation needs

---

### 6. Guidance Effectiveness

**Look For:**
- Agent behavior suggesting unclear guidance
- Task approaches deviating from optimal patterns
- Mode switching decisions and appropriateness
- Tool usage relative to restrictions

**Questions:**
- Did agent follow mode-appropriate patterns?
- Were mode transitions handled effectively?
- What guidance was missing or unclear?
- Did restrictions support the purpose?

**Output:** Guidance refinements and rule clarifications

---

## Retrospective Process

### Phase 1: Preparation

1. **Context Gathering**
   - Load current context network state
   - Identify agent mode(s) used
   - Note task type and complexity
   - Review applicable rules

2. **Baseline**
   - Map context available at task start
   - Identify active guidance
   - Note recent network changes
   - Document expected vs. actual behavior

### Phase 2: Transcript Review

1. **Chronological Analysis**
   - Track information seeking patterns
   - Note decision points where context influenced choices
   - Identify struggle points
   - Map actual navigation paths

2. **Critical Incidents**
   - Flag confusion or inefficiency
   - Identify boundary violations
   - Note "rediscovery" of information
   - Mark where better context would have helped

3. **Pattern Recognition**
   - Recurring information needs
   - Systematic gaps in knowledge areas
   - Consistent navigation difficulties
   - Successful context utilization

### Phase 3: Gap Analysis

1. **Information Architecture**
   - Map knowledge coverage gaps
   - Evaluate abstraction appropriateness
   - Assess relationship completeness
   - Review navigation effectiveness

2. **Guidance System**
   - Analyze mode-specific guidance
   - Review boundary rule clarity
   - Evaluate instruction completeness
   - Assess prompt override needs

3. **Prioritization**
   - **Critical:** Caused task failure or significant inefficiency
   - **High:** Required real-time discovery
   - **Medium:** Would enhance efficiency
   - **Low:** Nice-to-have improvements

---

## Analysis Templates

### Knowledge Gap

```markdown
## Gap: [Name]

**Discovery Context:** [When/how revealed]
**Task Impact:** [How it affected completion]
**Information Type:** [Domain/Process/Relationship/Decision criteria]
**Recommended Action:** [Specific node or relationship to add]
**Priority:** [Critical/High/Medium/Low]
**Related Gaps:** [Connected gaps]
```

### Navigation Issue

```markdown
## Issue: [Name]

**Problem Pattern:** [What difficulty occurred]
**Information Sought:** [What agent wanted]
**Current Path:** [How agent actually found it]
**Optimal Path:** [How it should be discoverable]
**Recommended Improvement:** [Specific changes]
**Affected Tasks:** [What else would benefit]
```

### Guidance Assessment

```markdown
## Guidance: [Mode/Rule Area]

**Expected Behavior:** [What guidance should produce]
**Actual Behavior:** [What agent did]
**Deviation Analysis:** [Why different]
**Guidance Clarity:** [Current clarity level]
**Recommended Changes:** [Specific modifications]
**Test Scenarios:** [How to validate]
```

---

## Quality Metrics

### Completeness
- **Information Coverage:** % of questions answerable from context
- **Relationship Completeness:** Documented vs. discovered relationships
- **Navigation Efficiency:** Steps vs. optimal paths
- **Boundary Compliance:** % correct domain placements

### Effectiveness
- **Task Completion Quality:** Success rate with available context
- **Agent Confidence:** Frequency of uncertainty expressions
- **Context Utilization:** % of relevant context actually used
- **Discovery vs. Lookup:** New discoveries vs. existing use

### Evolution
- **Context Network Growth:** New nodes/relationships rate
- **Guidance Refinement:** Rule update frequency
- **Pattern Recognition:** Recurring improvement themes
- **System Maturity:** Decreasing structural changes

---

## Common Patterns & Solutions

| Pattern | Solution |
|---------|----------|
| Repeatedly seeks same info | Create hub document, improve linking |
| Confusion about file placement | Enhance boundary guidance with examples |
| Task context scattered | Create task-specific entry points |
| Decisions without consulting context | Strengthen "consult before action" guidance |
| Info not at right abstraction | Multi-layered nodes with progressive disclosure |

---

## Implementation Priority

**Phase 1: Critical Infrastructure**
- Fix boundary violations
- Add missing foundational knowledge
- Repair broken relationships

**Phase 2: Navigation Enhancement**
- Improve discoverability
- Create hub documents
- Strengthen cross-domain connections

**Phase 3: Guidance Refinement**
- Update mode-specific instructions
- Clarify ambiguous rules
- Enhance prompts for common tasks

**Phase 4: Optimization**
- Fine-tune abstraction levels
- Optimize for discovered workflows
- Enhance metadata systems

---

## Anti-Patterns

### 1. The Blame Game
**Pattern:** Attributing interaction failures to agent capability rather than context gaps. "The agent should have known..."
**Why it fails:** Agents operate from context. If context is incomplete, even capable agents fail. Blaming agents prevents systemic improvement.
**Fix:** Assume context gaps first. Ask "what information would have prevented this?" before "why didn't the agent figure it out?"

### 2. The Completeness Illusion
**Pattern:** Believing context networks can capture everything. Adding more and more information hoping to prevent all failures.
**Why it fails:** Context networks grow without bound. Navigation becomes impossible. Signal-to-noise ratio degrades. Maintenance becomes unsustainable.
**Fix:** Focus on high-impact gaps. Prioritize what actually caused failures. Remove outdated information as aggressively as you add new.

### 3. The Surface Fix
**Pattern:** Fixing the specific issue without identifying the pattern. Adding a fact that was missing without asking why it was missing.
**Why it fails:** Treats symptoms, not causes. The same class of gap will appear elsewhere. Whack-a-mole maintenance.
**Fix:** Classify gaps by type. If the gap is "missing relationship documentation," the fix is improving relationship capture, not adding one relationship.

### 4. The Retrospective-Only
**Pattern:** Running retrospectives but never implementing changes. Analysis paralysis or action avoidance.
**Why it fails:** Insight without action produces no improvement. Accumulating analysis without implementation wastes the analysis effort.
**Fix:** Every retrospective must produce at least one actionable change. Schedule implementation before finishing retrospective.

### 5. The Guidance Overdose
**Pattern:** Adding more rules and restrictions after every failure. Context networks become constraint lists.
**Why it fails:** Excessive guidance produces paralysis. Agents become afraid to act. Guidance conflicts emerge. Nobody reads the rules.
**Fix:** Before adding guidance, consider removing it. Simplify before complexifying. Test if clearer boundaries achieve more than more rules.

## Integration Points

**Inbound:**
- After any significant agent interaction
- After task failures or inefficiencies
- During context network maintenance

**Outbound:**
- To context network updates
- To guidance/instruction improvements

**Complementary:**
- Context Networks framework
- Agent mode configurations
