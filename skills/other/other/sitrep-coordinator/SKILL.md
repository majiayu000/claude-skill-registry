---
name: sitrep-coordinator
description: Military-style Situation Report (SITREP) generation for multi-agent coordination. Creates structured status updates with completed/in-progress/blocked sections, authorization codes, handoff protocols, and clear next actions. Optimized for complex project management across multiple AI agents and human operators.
---

# SITREP Coordinator

Expert in military-style Situation Report (SITREP) generation for coordinating complex projects across multiple AI agents, human operators, and distributed teams. Provides structured, actionable status updates following military communication protocols adapted for software development and technical project management.

## Core Competencies

### 1. SITREP Structure & Format
- **Standard Format**: Consistent header, situation, completed, in-progress, blocked, next actions
- **Authorization Codes**: Unique identifiers for mission tracking and handoff validation
- **Status Indicators**: Color-coded traffic light system (🟢 GREEN, 🟡 YELLOW, 🔴 RED)
- **Timestamp Precision**: ISO 8601 or military time formats
- **Concise Communication**: Maximum information density, minimum verbosity

### 2. Multi-Agent Coordination
- **Handoff Protocols**: Clear task transfer between agents with context preservation
- **Role Identification**: Explicit agent/operator roles and responsibilities
- **Dependency Tracking**: Inter-agent dependencies and sequencing requirements
- **Conflict Resolution**: Identifying and escalating coordination issues
- **Context Sharing**: Minimum viable context for effective handoffs

### 3. Status Tracking & Metrics
- **Completion Tracking**: Granular task completion with percentage estimates
- **Blocker Identification**: Root cause analysis and owner assignment
- **Timeline Management**: ETA updates and deadline tracking
- **Quality Gates**: Pass/fail criteria for phase transitions
- **Risk Assessment**: Identifying and communicating risks early

### 4. Escalation & Decision Support
- **Go/No-Go Criteria**: Clear decision frameworks for phase gates
- **Escalation Triggers**: When to escalate vs. when to proceed
- **Decision Requests**: Structured options presentation for stakeholder decisions
- **Risk Communication**: Impact/probability assessment for issues
- **Recommendation Format**: Actionable recommendations with rationale

## SITREP Template

```markdown
# 🎖️ SITREP: [PROJECT-NAME]-[PHASE]-[DATE]

**DATE:** [ISO 8601 timestamp]  
**OPERATOR:** [Agent/Human Name]  
**AUTH CODE:** [UNIQUE-ID]  
**STATUS:** [🟢 GREEN / 🟡 YELLOW / 🔴 RED]

---

## SITUATION

**MISSION:** [One-sentence mission statement]  
**PHASE:** [Current phase/sprint/milestone]  
**PRIORITY:** [Priority level and context]

---

## COMPLETED (Last [Timeframe])

✅ **[Task Category 1]**
- Subtask 1 details
- Subtask 2 details
- Impact/outcome

✅ **[Task Category 2]**
- Subtask details
- Metrics achieved

---

## IN PROGRESS

🔄 **[Task Category]**
- Current status (XX% complete)
- ETA: [timestamp]
- Owner: [Agent/Person]
- Dependencies: [List]

---

## BLOCKED

**NONE** / **[Blocker Category]**
- Issue description
- Impact: [High/Medium/Low]
- Owner for resolution: [Name]
- Escalation required: [Yes/No]

---

## KEY ACCOMPLISHMENTS

[Bullet list of significant achievements this period]

---

## METRICS

[Quantitative progress indicators]

---

## NEXT ACTIONS (IMMEDIATE)

[Prioritized list of next 24-48h actions]

---

## COORDINATION

**Handoff Points:**
- [Agent/Person]: [What/When]

**Dependencies:**
- [Waiting on / Blocking]

---

## ASSESSMENT

**Mission Status:** [Status summary]  
**Quality:** [Quality indicator]  
**Ready State:** [GREEN/YELLOW/RED - readiness for next phase]

---

## [STAKEHOLDER] REQUESTS

**[Specific requests or decisions needed]**

Options:
1. [Option 1]
2. [Option 2]
3. [Option 3]

---

**SITREP ENDS**

**Operator:** [Name]  
**Next SITREP:** [When/Trigger]  
**Contact:** [How to reach]
```

## Implementation Guidelines

### When to Generate a SITREP

**Mandatory Triggers:**
1. **Phase Transitions**: At the start/end of each project phase
2. **Daily Standups**: For active sprints (morning summary)
3. **Blocker Escalations**: When critical issues arise
4. **Handoff Events**: When transferring work between agents/people
5. **Milestone Completion**: Upon completing major deliverables
6. **Status Requests**: When stakeholders request updates

**Optional Triggers:**
1. **Mid-Phase Check-ins**: 50% completion mark
2. **Risk Identification**: When new risks are discovered
3. **Scope Changes**: When requirements or priorities shift
4. **Resource Changes**: When team/tool availability changes

### Status Color Coding

**🟢 GREEN (On Track):**
- All tasks progressing as planned
- No blockers or risks
- Quality gates passing
- Timeline intact
- Resources adequate

**🟡 YELLOW (Caution):**
- Minor delays or issues
- Manageable blockers
- Some quality concerns
- Timeline at risk but recoverable
- Resources stretched but adequate

**🔴 RED (Critical):**
- Major blockers preventing progress
- Significant quality issues
- Timeline severely at risk
- Resources insufficient
- Escalation required

### Authorization Code Format

```
[PROJECT]-[PHASE]-[AGENT]-[SEQUENCE]

Examples:
HUMMBL-MCP-CASCADE-001
HUMMBL-API-CHATGPT-003
UNIFIED-TIER-CLAUDE-DESK-012
```

**Components:**
- **PROJECT**: Project identifier (uppercase, max 15 chars)
- **PHASE**: Current phase/component (uppercase, max 10 chars)
- **AGENT**: Agent/operator identifier (uppercase, max 10 chars)
- **SEQUENCE**: 3-digit sequential number

### Handoff Protocol

**Sending Agent Responsibilities:**
1. Generate comprehensive SITREP
2. Include authorization code
3. Specify receiving agent explicitly
4. Document all context needed
5. State clear next actions
6. Confirm handoff acceptance

**Receiving Agent Responsibilities:**
1. Acknowledge receipt with auth code
2. Validate context completeness
3. Request clarification if needed
4. Confirm acceptance of tasking
5. Provide ETA for next SITREP

**Handoff Template:**
```markdown
## HANDOFF TO [AGENT]

**Task:** [Clear task statement]  
**Context:** [All necessary background]  
**Deliverables:** [Expected outputs]  
**Timeline:** [Deadline or ETA]  
**Resources:** [What receiver has access to]  
**Success Criteria:** [How to know task is complete]  
**Auth Code:** [HANDOFF-CODE]

**Receiving agent confirms:**
[ ] Context understood
[ ] Resources accessible
[ ] Timeline acceptable
[ ] Success criteria clear
```

## Multi-Agent Coordination Patterns

### Pattern 1: Sequential Handoff
**Use Case:** Tasks that must be completed in order

```
Agent A → SITREP → Agent B → SITREP → Agent C
```

**SITREP Focus:**
- Clear completion criteria for each agent
- Explicit dependencies documented
- Context preservation through chain
- Quality gates between handoffs

### Pattern 2: Parallel Execution
**Use Case:** Independent tasks executed simultaneously

```
Coordinator → SITREP → Agent A
                     → Agent B
                     → Agent C
         
[All report back to Coordinator]
```

**SITREP Focus:**
- No inter-agent dependencies
- Independent completion tracking
- Aggregated status reporting
- Coordination of merge points

### Pattern 3: Iterative Refinement
**Use Case:** Multiple passes for quality improvement

```
Agent A → SITREP → Agent B (Review)
   ↑                    ↓
   └────── Iterate ─────┘
```

**SITREP Focus:**
- Iteration count tracking
- Quality improvement metrics
- Diminishing returns detection
- Exit criteria definition

### Pattern 4: Escalation Chain
**Use Case:** Decision authority hierarchy

```
Agent A → Blocker → SITREP → Team Lead
                              ↓
                         SITREP → Executive
```

**SITREP Focus:**
- Escalation justification
- Impact assessment
- Decision options presented
- Urgency indicators

## Examples

### Example 1: Development Sprint SITREP

```markdown
# 🎖️ SITREP: HUMMBL-MCP-SPRINT1-NOV1

**DATE:** 2025-11-01T22:00:00Z  
**OPERATOR:** Windsurf Cascade  
**AUTH CODE:** HUMMBL-MCP-CASCADE-001  
**STATUS:** 🟢 GREEN

---

## SITUATION

**MISSION:** MCP Server Phase 0 implementation (29 days)  
**PHASE:** Week 1 - Server scaffold and core endpoints  
**PRIORITY:** #2 (following GitHub framework completion)

---

## COMPLETED (Last 24 Hours)

✅ **Project Initialization**
- TypeScript project scaffold created
- MCP SDK integrated (v1.0.0)
- Development environment configured
- Git repository initialized

✅ **Database Schema**
- D1 SQLite schema designed
- Migration scripts created
- FTS5 full-text search enabled
- Seed data prepared (120 models)

---

## IN PROGRESS

🔄 **MCP Endpoints Implementation**
- Status: 40% complete
- ETA: Nov 3, 2025 EOD
- Owner: Cascade
- Dependencies: None
- Details:
  - Resources endpoints: 2/3 complete
  - Tools endpoints: 1/3 complete
  - Error handling: In progress

---

## BLOCKED

**NONE**

---

## KEY ACCOMPLISHMENTS

- Zero setup issues encountered
- Database latency: <50ms (target <500ms) ✅
- TypeScript strict mode: 100% passing ✅
- Initial telemetry framework operational

---

## METRICS

- Lines of Code: 847
- Test Coverage: 0% (tests planned Week 2)
- Dependencies: 12 (all security audited)
- Build Time: 2.3s

---

## NEXT ACTIONS (IMMEDIATE)

1. Complete remaining resources endpoint (models list)
2. Implement tools endpoints (analyze-perspective, decompose-problem)
3. Add input validation with Zod
4. Write integration tests for completed endpoints
5. Document API in README

---

## COORDINATION

**Handoff Points:**
- None (proceeding independently)

**Status Updates:**
- Daily SITREP during Week 1
- Escalate if any blockers arise

---

## ASSESSMENT

**Mission Status:** On track for Week 1 completion  
**Quality:** High (no technical debt accumulated)  
**Ready State:** 🟢 GREEN - Week 2 prep underway

---

## CHIEF ENGINEER REQUESTS

**None currently - standing by for direction**

---

**SITREP ENDS**

**Operator:** Windsurf Cascade  
**Next SITREP:** Nov 2, 2025 @ 22:00Z  
**Contact:** This session
```

### Example 2: Blocker Escalation SITREP

```markdown
# 🎖️ SITREP: HUMMBL-API-BLOCKER-NOV5

**DATE:** 2025-11-05T14:30:00Z  
**OPERATOR:** Claude Desktop  
**AUTH CODE:** HUMMBL-API-CLAUDE-ESCALATE-001  
**STATUS:** 🔴 RED (BLOCKER)

---

## SITUATION

**MISSION:** HUMMBL API implementation  
**PHASE:** Week 2 - Cloudflare Workers deployment  
**PRIORITY:** Critical blocker requiring decision

---

## COMPLETED (Today)

✅ **API Implementation**
- All 7 endpoints coded and tested locally
- OpenAPI spec complete
- Documentation written

---

## IN PROGRESS

⚠️ **PAUSED** due to blocker

---

## BLOCKED

🔴 **Cloudflare D1 Database Limitations**

**Issue:** D1 database size limit (500MB) insufficient for full BASE120 with metadata

**Impact:** HIGH
- Current data: 620MB with all model descriptions
- Cannot deploy to production without resolution
- Affects all downstream projects (MCP, GPTs)

**Owner:** Requires Chief Engineer decision

**Options:**
1. **Migrate to Cloudflare R2 + Workers KV**
   - Pros: No size limits, similar latency
   - Cons: 2-3 days rework, different query patterns
   - Cost: +$5/month

2. **Compress model descriptions**
   - Pros: No architecture change
   - Cons: Reduced quality, still might hit limit later
   - Cost: 1 day rework

3. **Hybrid: Critical data in D1, full data in R2**
   - Pros: Best of both worlds
   - Cons: 3-4 days rework, complexity increase
   - Cost: +$5/month

**Escalation Required:** YES - Architecture decision needed

---

## CHIEF ENGINEER DECISION REQUIRED

**Question:** Which architecture approach should we take?

**Recommendation:** Option 3 (Hybrid)
- Balances performance and scalability
- Future-proof for BASE240+ expansion
- Acceptable timeline impact (3-4 days)

**Awaiting your directive to proceed.**

---

**SITREP ENDS**

**Operator:** Claude Desktop  
**Next SITREP:** Upon decision or in 4 hours  
**Contact:** This conversation
```

### Example 3: Multi-Agent Handoff SITREP

```markdown
# 🎖️ SITREP: UNIFIED-TIER-HANDOFF-NOV1

**DATE:** 2025-11-01T18:00:00Z  
**OPERATOR:** Windsurf Cascade  
**AUTH CODE:** UNIFIED-TIER-CASCADE-HANDOFF-003  
**STATUS:** 🟢 GREEN (HANDOFF)

---

## SITUATION

**MISSION:** Unified Tier Framework GitHub publication  
**PHASE:** Complete - Ready for handoff to Context Engineering  
**PRIORITY:** #1 Complete, transitioning to #2

---

## COMPLETED (Session Summary)

✅ **Full repository published**
- 16 commits
- 32 files
- 13 documentation pages (3,200+ lines)
- All workflows passing (4/4)

✅ **Priority tasks executed**
- Repository topics optimized
- CODEOWNERS created
- CITATION.cff added
- v1.0.0 release published

✅ **Error corrections**
- BASE120 transformations fixed
- Authoritative source validated
- Documentation consistency verified

---

## HANDOFF TO CHIEF ENGINEER

**Deliverables:**
✅ GitHub repo: https://github.com/hummbl-dev/HUMMBL-Unified-Tier-Framework
✅ GitHub Pages: https://hummbl-dev.github.io/HUMMBL-Unified-Tier-Framework/
✅ v1.0.0 release: Published with comprehensive notes
✅ All quality checks: Passing (lint, spell, links, build)

**Status:** MISSION COMPLETE

**Auth Code for Receipt:** UNIFIED-TIER-CASCADE-HANDOFF-003

**Next Priority:** MCP Server Development (Priority #2)
- Authorization received: HUMMBL-MCP-CASCADE-HANDOFF-001
- Ready to begin on your command

---

**SITREP ENDS**

**Operator:** Windsurf Cascade  
**Handoff To:** Chief Engineer  
**Awaiting:** Authorization for Priority #2 kickoff
```

## Quality Checklist

### SITREP Completeness ✅
- [ ] All required header fields present
- [ ] Status indicator matches content
- [ ] Authorization code format correct
- [ ] Completed section has concrete deliverables
- [ ] In-progress has ETA and owner
- [ ] Blockers clearly articulated with owners
- [ ] Next actions are specific and prioritized
- [ ] Coordination points identified

### Communication Quality ✅
- [ ] Maximum 2-page length (conciseness)
- [ ] No ambiguous language
- [ ] All acronyms defined on first use
- [ ] Metrics are quantitative, not qualitative
- [ ] Recommendations have clear rationale
- [ ] Decision points explicitly called out

### Coordination Effectiveness ✅
- [ ] Handoffs have acceptance criteria
- [ ] Dependencies explicitly stated
- [ ] Context sufficient for receiver
- [ ] Resources accessibility confirmed
- [ ] Timeline expectations realistic

## Common Pitfalls & Solutions

### Pitfall 1: Information Overload
**Problem:** SITREP too long, recipients skim and miss critical info  
**Solution:** Use "Executive Summary" section for key points, details below

### Pitfall 2: Unclear Status
**Problem:** Status indicator doesn't match blocker severity  
**Solution:** Follow strict color coding rules; default to more conservative

### Pitfall 3: Missing Context
**Problem:** Handoff fails because receiver lacks necessary background  
**Solution:** Include "Context" section with all assumptions and background

### Pitfall 4: No Clear Next Steps
**Problem:** Recipients unsure what to do after reading SITREP  
**Solution:** Always include "Next Actions" with specific, actionable items

### Pitfall 5: Stale Information
**Problem:** SITREP outdated by the time stakeholders read it  
**Solution:** Include timestamp and "Valid Until" field for time-sensitive reports

## Resources

- **Military SITREP Format**: FM 6-99.2 (U.S. Army Field Manual)
- **Agile Status Reporting**: Scrum Daily Stand-up best practices
- **Incident Management**: ITIL incident reporting standards
- **Project Management**: PMI status reporting guidelines

## Success Criteria

**Effective SITREP achieves:**
1. ✅ Stakeholders understand status in <2 minutes reading time
2. ✅ No follow-up questions needed for clarification
3. ✅ Handoffs execute without context loss
4. ✅ Blockers escalated to correct authority
5. ✅ Next actions clear enough to execute immediately

**SITREP fails if:**
1. ❌ Recipients request clarification on basic facts
2. ❌ Status doesn't match actual project state
3. ❌ Handoffs fail due to missing context
4. ❌ Timeline estimates consistently wrong
5. ❌ Blockers not identified until crisis point
