---
name: process-mapper
description: Map workflows, extract SOPs, and identify automation opportunities through systematic process capture and AI tractability assessment. Use when documenting workflows, creating SOPs, conducting process discovery interviews, or analyzing automation opportunities. Grounds the SOP-first doctrine in tacit knowledge documentation and structured analysis.
license: Complete terms in LICENSE.txt
---

# Process Mapper Skill

Systematic workflow for discovering, documenting, and analyzing processes. Implements user's SOP-first doctrine: **"You can't automate what you can't see."**

## Core Philosophy

**From user's work:**
> "When I sit with a person or team to start working through how they can work out where and how to apply AI into their job, I often like to start with a common task or value stream, and talk through—or more often than not, document—the SOP for that value stream."

**Three truths:**
1. **Shadow processes are real processes** (what actually happens ≠ org chart)
2. **Tacit knowledge is documentable** (capture decision *points*, not decision *logic*)
3. **Structure enables automation** (visibility → AI opportunities)

---

## Core Workflow

### 1. Diagnostic: Assess Current State

**Determine SOP state:**

Load `references/discovery-methodology.md` for framework

**State 1: Fiction**
- SOPs exist but nobody follows them
- Beautiful docs, zero usage
- Aspirational not actual

**State 2: Nonexistent**
- No documentation
- Tribal knowledge
- "Just ask Sarah"

**State 3: Accurate**
- Docs match reality
- Referenced regularly
- Updated when process changes

**Action by state:**
- Fiction → Archive and start fresh
- Nonexistent → Begin discovery (most common)
- Accurate → Use for automation analysis

---

### 2. Process Discovery Interview

**If starting from State 2 (Nonexistent), conduct discovery:**

**Setup:**
- Identify process owner (person who actually does this)
- Secure 45-90 minutes uninterrupted
- Frame: "Show me what actually happens, not what should happen"
- Get screen access to tools they use

**Five-round interview sequence:**

Load `references/discovery-methodology.md` for detailed questions. Brief framework:

**Round 1: High-Level Flow** - Get end-to-end sequence (5-10 major steps, trigger, endpoint, duration)

**Round 2: Step Decomposition** - Break into substeps (inputs, tools, transformations). Look for copy-paste, manual entry, system switching.

**Round 3: Decision Points** - Identify where judgment is required. Distinguish explicit rules from tacit judgment (labeled black box pattern).

**Round 4: Edge Cases & Exceptions** - Understand failure modes, workarounds, frequency. High exceptions = process might be wrong.

**Round 5: Context Dependencies** - Identify tacit knowledge (domain knowledge, institutional knowledge, relationships). Reveals automation tractability.

---

### 3. Process Documentation

**Choose format based on process characteristics:**

**Format 1: Linear SOP** (≤10 steps, minimal branching)
- Sequential steps with actions/tools/inputs
- Quality checks
- Common issues

**Format 2: Decision Tree** (multiple paths, branching logic)
- Entry conditions
- Path A/B/C with criteria
- Decision matrix

**Format 3: Swimlane** (multi-role, handoffs important)
- Who does what when
- Handoff points
- Role responsibilities

**Format 4: Visual Diagram** (complex flows)
- Mermaid flowchart
- System integrations
- Exception paths

Load `assets/visual-templates.md` for specific templates

**Documentation principles:**
- Capture **actual** current state (not aspirational)
- Mark tacit knowledge points with ⚡
- Note context dependencies with 🧠
- Flag frequent failures with ⚠️
- Include frequency/volume data
- Validate with process owner

---

### 4. Complexity Classification

**Map each process step to Tractability Grid (9 zones):**

Load `references/automation-framework.md` for full framework and detailed assessment criteria.

**Two dimensions:**
1. **Context Dependence:** Low (algorithmic, no expertise) → High (tacit judgment, relationships)
2. **Task Complexity:** Simple (≤5 steps, single system) → Complex (15+ steps, multiple systems)

**Assessment questions:** Could intern do this with instructions? How many steps/systems/decisions?

---

### 5. Automation Opportunity Analysis

**Plot each step on 9-zone grid** (see `references/automation-framework.md` for visual):
- **Zones 1-2 (Green):** High automation (85-75% success) - RPA, quick wins
- **Zones 3-5 (Yellow):** Medium (60-40%) - AI copilots, human-in-loop
- **Zones 6-9 (Red):** Low (<25%) - Avoid core automation, support tasks only

### 6. Prioritization & ROI

**Priority quadrants** (Pain × Feasibility):
- **P1 - Quick Wins:** High pain, easy (Zones 1-2) - Do immediately
- **P2 - Strategic:** High pain, hard (Zones 3-5) - Worth investment
- **P3 - Efficiency:** Low pain, easy - Do when capacity available
- **P4 - Avoid:** Low pain, hard (Zones 6-9) - Not worth effort

**ROI:** Payback Period = Cost / (Hours Saved × Rate + Error Reduction)

### 7. Output Delivery

**Standard deliverables:** Process Map (visual), SOP Document (written), Automation Analysis (zone classifications, priorities, ROI), Implementation Roadmap (phased plan)

**Optional:** Interview transcript, validation notes, comparative analysis, metrics dashboard

---

## The Labeled Black Box Pattern

**Critical technique:** Document THAT a decision exists, not HOW it's made (when tacit).

Load `references/documentation-patterns.md` for detailed examples and template.

**Core principle:** Name decision points even when logic is tacit. Enables process visibility, appropriate handoffs, training focus, and future automation planning.

---

## Movement Strategy

**Key insight:** Can't automate high-context zones directly. Build infrastructure to move problems to lower zones.

Load `references/documentation-patterns.md` for case study (Air India: Zone 8 → Zone 2, 97% accuracy).

**Infrastructure path:** Zone 8→5 (frameworks), Zone 5→2 (explicit logic), Zone 2→1 (eliminate manual steps)

---

## Quality Signals

**Good process map has:**
- [ ] Actual current state (not aspirational)
- [ ] All decision points identified
- [ ] Tacit knowledge points marked (⚡)
- [ ] Context dependencies noted (🧠)
- [ ] Exception paths included
- [ ] Validated by process owner
- [ ] Frequency/volume data
- [ ] Pain points documented
- [ ] Clear start and end
- [ ] Realistic time estimates

**Red flags:**
- Too neat (probably fictional)
- No exceptions (incomplete)
- No pain points (not real discovery)
- No tacit knowledge points (missed shadow process)
- Can't estimate frequency (no data)
- Process owner says "that's not quite right"

---

## Integration Points

**With `concept-forge`:**
- Test automation hypotheses dialectically
- Challenge zone classifications
- Refine through multiple perspectives

**With `strategy-to-artifact`:**
- Process map → Presentation deck
- Automation roadmap → Executive one-pager
- Business case → Slide deck

**With `research-to-essay`:**
- Process patterns → Substack post on SOP doctrine
- Case studies → Long-form analysis

**With user's voice (from `research-to-essay`):**
- Use dialogue structure in documentation
- Employ concrete examples (Air India vs Air Canada)
- Include practitioner stance ("In my experience...")
- Show recursive refinement ("Let me be more precise...")

---

## Common Process Types

**Approval Workflows:** Zones 1-2 (rule-based) or 4-5 (judgment). High automation potential for rules.

**Data Processing:** Zones 1-3. Very high automation if algorithmic.

**Customer Service:** Zones 4-8. Medium automation (copilot model).

**Reporting:** Zones 1-3 (structured) or 5-7 (insights). High for gathering, medium for analysis.

**Coordination:** Zones 4-9 (relationship-dependent). Low for core, high for supporting tasks.

---

## Anti-Patterns

**Don't:**
- Map aspirational process (document what actually happens)
- Skip validation with process owner (will be wrong)
- Try to capture tacit HOW (use labeled black box)
- Force Zone 8-9 into automation (will fail)
- Ignore shadow processes (they're the real process)
- Over-document (keep it actionable)
- Create one-time map (processes evolve, keep updated)

**Do:**
- Start with actual current state
- Validate iteratively
- Document decision points even when logic is tacit
- Acknowledge complexity honestly
- Focus on high-ROI opportunities
- Build movement infrastructure
- Update as process changes

---

## Success Metrics

**Process mapping succeeds when:**
- Process owner says "Yes, that's exactly what we do"
- New team members can follow documented process
- Automation opportunities clearly identified
- ROI estimates are validated
- Quick wins deliver promised value
- Documentation is referenced regularly (not ignored)

**Automation analysis succeeds when:**
- Zone classifications match reality
- Prioritization aligns with business value
- Implementation follows plan
- Expected savings materialize
- User adoption high (not forced)

---

## Example Triggers

- "Map our customer onboarding process"
- "Document how we handle support tickets"
- "Where can we apply AI to our workflow?"
- "Create SOP for expense approval"
- "Show me where automation makes sense"
- "Why does this process keep breaking?"
- "Help me understand what my team actually does"
- "Walk me through your typical day"
