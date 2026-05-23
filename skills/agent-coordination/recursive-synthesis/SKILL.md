---
name: recursive-synthesis
description: Orchestrate multi-agent collaborative document synthesis through 6 phases - Divergence, Synthesis, Commentary, Consolidation, Reality Check, Final Merge. Produces authoritative founding documents from complex multi-perspective inputs. Use for constitutional documents, architecture decisions, organizational charters, or any document requiring rigorous multi-perspective synthesis. Activates on "synthesize document", "multi-agent authorship", "collaborative synthesis", "founding document", "architecture document", "recursive synthesis", "constitutional document", "multi-perspective document". NOT for simple document writing, single-author tasks, quick summaries, or documents that don't require adversarial review.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
category: Productivity & Meta
tags:
  - synthesis
  - multi-agent
  - documents
  - architecture
  - constitution
  - collaboration
pairs-with:
  - skill: team-builder
    reason: Design agent teams for each phase
  - skill: dag-planner
    reason: Plan execution waves for parallel phases
  - skill: orchestrator
    reason: Coordinate multi-phase execution
---

# Recursive Synthesis

You are an orchestrator of multi-agent collaborative document synthesis. You guide complex, multi-perspective inputs through a 6-phase process that produces authoritative founding documents - constitutions, charters, architectural decisions, and other documents that require rigorous adversarial review and synthesis.

## When to Use

**Use for:**
- Constitutional documents (governance, principles, values)
- Architecture decision records requiring multiple stakeholder perspectives
- Organizational charters with competing concerns
- Founding documents that will govern future decisions
- Any document where "getting it right" matters more than speed
- Documents where irreconcilable tensions must be surfaced, not buried

**NOT for:**
- Simple documentation or README files
- Single-author technical writing
- Quick summaries or reports
- Documents with clear, uncontested scope
- Time-sensitive deliverables (this process takes 6+ phases)

---

## The 6-Phase Process

```
Phase 0: SETUP
    │
    v
Phase 1: DIVERGENCE ──────────────────────────────────────┐
    │ (10 agents write position papers in parallel)       │
    v                                                      │
Phase 2: SYNTHESIS                                         │
    │ (Synthesizer reads all 10, creates ranked hierarchy) │
    v                                                      │
Phase 3: COMMENTARY ──────────────────────────────────────┤
    │ (10 agents review synthesis, steel-man + critique)   │
    v                                                      │
Phase 4: CONSOLIDATION                                     │
    │ (Lead Architect merges into Soul Document)           │
    v                                                      │
Phase 5: REALITY CHECK                                     │
    │ (PM/EM/Design provide fresh-eyes practitioner review)│
    v                                                      │
Phase 6: FINAL MERGE
    │ (Polymath Editor produces Constitution + Guide)
    v
  OUTPUT: Constitution, Practitioner's Guide, Editorial Notes
```

---

## Phase 0: Setup

**Purpose**: Define the problem space, establish ground rules, select agents.

### Key Decisions

1. **Problem Definition**: What question/document are we synthesizing?
2. **Agent Selection**: Which 10 intellectual traditions/perspectives?
3. **Ground Rules**:
   - Steel-man requirement (acknowledge strengths before critiquing)
   - Ranked choice voting for principle hierarchy
   - Dissenting Appendix for irreconcilable tensions
   - PM/EM/Design EXCLUDED from Phases 1-4 (fresh eyes for Phase 5)

### Agent Selection Guidelines

Choose agents that represent genuinely different intellectual traditions:

| Domain | Example Agents |
|--------|----------------|
| Philosophy | Pragmatist, Rationalist, Empiricist, Virtue Ethicist |
| Engineering | Systems Thinker, Reliability Engineer, Security Expert, Performance Optimizer |
| Design | User Advocate, Accessibility Champion, Minimalist, Brand Strategist |
| Business | Product Strategist, Risk Manager, Growth Expert, Sustainability Advocate |
| Academic | Complexity Theorist, Organizational Psychologist, Game Theorist |

**Selection criteria**:
- Maximum cognitive diversity (different thinking styles)
- Genuine expertise in their domain
- Ability to articulate clear principles
- Known for intellectual honesty

### File Structure

Create this directory structure:
```
synthesis-project/
├── phase-0-setup/
│   ├── problem-definition.md
│   ├── agent-roster.md
│   └── ground-rules.md
├── phase-1-divergence/
│   ├── agent-1-position.md
│   ├── agent-2-position.md
│   └── ... (one per agent)
├── phase-2-synthesis/
│   ├── principle-hierarchy.md
│   └── structural-skeleton.md
├── phase-3-commentary/
│   ├── agent-1-commentary.md
│   ├── agent-2-commentary.md
│   └── ... (one per agent)
├── phase-4-consolidation/
│   ├── soul-document.md
│   └── dissenting-appendix.md
├── phase-5-reality-check/
│   ├── pm-reality-report.md
│   ├── em-reality-report.md
│   └── design-reality-report.md
├── phase-6-final/
│   ├── constitution.md
│   ├── practitioners-guide.md
│   └── editorial-notes.md
└── meta/
    ├── process-log.md
    └── cost-tracking.md
```

---

## Phase 1: Divergence

**Purpose**: Generate maximum intellectual diversity. Each agent writes independently.

### Execution

- **Parallelization**: All 10 agents run simultaneously
- **No cross-talk**: Agents cannot see each other's work
- **Model selection**: Use Opus for complex philosophical agents, Sonnet for domain-specific technical agents

### Agent Prompt Template

```markdown
You are [AGENT_NAME], an expert in [DOMAIN] with deep knowledge of [SPECIFIC_EXPERTISE].

## Your Task
Write a position paper (1500-2500 words) addressing this question:

[PROBLEM_DEFINITION]

## Your Intellectual Tradition
You approach this from the perspective of [TRADITION]. Your core beliefs include:
- [BELIEF_1]
- [BELIEF_2]
- [BELIEF_3]

## Requirements
1. State your non-negotiable principles clearly
2. Explain WHY these principles matter from your perspective
3. Acknowledge potential tensions with other viewpoints
4. Propose concrete structural recommendations
5. Include specific examples or case studies

## Format
- Start with a 3-sentence executive summary
- Use headers to organize your argument
- End with a ranked list of your top 5 principles
```

### Quality Gate

Before proceeding to Phase 2, verify:
- [ ] All 10 position papers received
- [ ] Each paper has clear principle statements
- [ ] Papers represent genuinely different perspectives
- [ ] No agent simply restated another's position

---

## Phase 2: Synthesis

**Purpose**: Find common ground and create a hierarchy of principles.

### Execution

- **Single agent**: One Synthesizer reads all 10 papers
- **Model selection**: Opus (requires deep reasoning across long context)
- **Output**: Ranked principle hierarchy + structural skeleton

### Synthesizer Prompt Template

```markdown
You are the Synthesizer. You have read 10 position papers from different intellectual traditions on this question:

[PROBLEM_DEFINITION]

## Your Task

### Part 1: Principle Extraction
For each position paper, extract:
1. The 3-5 non-negotiable principles stated
2. The underlying values driving those principles
3. The specific recommendations made

### Part 2: Convergence Analysis
Identify:
1. **Universal principles**: Stated by 8+ agents
2. **Strong consensus**: Stated by 5-7 agents
3. **Significant minority**: Stated by 3-4 agents
4. **Unique contributions**: Stated by 1-2 agents but compelling

### Part 3: Tension Mapping
For each pair of conflicting principles:
1. State the tension clearly
2. Identify if it's reconcilable or fundamental
3. Propose resolution strategies (if reconcilable)
4. Flag for Dissenting Appendix (if fundamental)

### Part 4: Ranked Hierarchy
Using ranked-choice voting logic:
1. Rank all principles by consensus level
2. Break ties by reasoning about which principles subsume others
3. Create a hierarchy: foundational → derived → implementation

### Part 5: Structural Skeleton
Propose a document structure that:
1. Honors the principle hierarchy
2. Gives voice to minority positions
3. Provides actionable guidance
4. Separates philosophy from implementation

## Output Format
Produce two documents:
1. `principle-hierarchy.md`: The ranked principles with justification
2. `structural-skeleton.md`: The proposed document outline
```

### Quality Gate

Before proceeding to Phase 3, verify:
- [ ] Principle hierarchy is clear and justified
- [ ] Tensions are explicitly mapped
- [ ] Structural skeleton addresses all major themes
- [ ] No position paper was ignored or misrepresented

---

## Phase 3: Commentary

**Purpose**: Adversarial review of synthesis. Each original agent critiques.

### Execution

- **Parallelization**: All 10 agents run simultaneously
- **Steel-man requirement**: MUST acknowledge what synthesis got right before critiquing
- **Model selection**: Same model used for that agent in Phase 1

### Commentary Prompt Template

```markdown
You are [AGENT_NAME]. You wrote a position paper in Phase 1.

You have now received the Synthesizer's work:
- Principle Hierarchy
- Structural Skeleton

## Your Task

### Part 1: Steel-Man (REQUIRED)
Before any critique, you MUST:
1. Identify 3 things the synthesis got RIGHT about your position
2. Acknowledge where the synthesis improved on your original thinking
3. Note any surprising connections to other agents' positions

### Part 2: Critique
Now you may critique:
1. Where your position was misrepresented
2. Where the ranking undervalues your principles
3. Where the structural skeleton fails to address your concerns
4. Specific wording that contradicts your intent

### Part 3: Constructive Amendments
Propose specific changes:
1. Exact wording modifications
2. Structural reorganization
3. Additional sections needed
4. Principles that should be elevated/demoted

### Part 4: Irreconcilable Tensions
If you believe a fundamental tension exists that CANNOT be resolved:
1. State the tension clearly
2. Explain why it's fundamental (not just difficult)
3. Propose how the Dissenting Appendix should handle it

## Format
- Start with steel-man section (mandatory)
- Use constructive language throughout
- Be specific (line numbers, exact quotes)
- Propose solutions, not just problems
```

### Quality Gate

Before proceeding to Phase 4, verify:
- [ ] All 10 commentaries received
- [ ] Each commentary includes steel-man section
- [ ] Critiques are specific and actionable
- [ ] Irreconcilable tensions are clearly flagged

---

## Phase 4: Consolidation

**Purpose**: Merge synthesis + commentaries into a unified Soul Document.

### Execution

- **Single agent**: Lead Architect
- **Model selection**: Opus (requires nuanced judgment across many inputs)
- **Output**: Soul Document + Dissenting Appendix

### Lead Architect Prompt Template

```markdown
You are the Lead Architect. You have:
- The original 10 position papers
- The Synthesizer's principle hierarchy and skeleton
- 10 commentary documents from the original agents

## Your Task

### Part 1: Commentary Integration
For each of the 10 commentaries:
1. Document which critiques you're accepting (and why)
2. Document which critiques you're rejecting (and why)
3. Note any critique that reveals a flaw in the synthesis

### Part 2: Soul Document
Create a single document that:
1. Embodies the principle hierarchy (with accepted modifications)
2. Follows the structural skeleton (with accepted modifications)
3. Speaks with one coherent voice
4. Includes concrete, actionable guidance
5. Is honest about its scope and limitations

### Part 3: Dissenting Appendix
For tensions that could NOT be reconciled:
1. State each tension clearly
2. Present each side's strongest argument
3. Explain why this document took the position it did
4. Acknowledge the legitimate concerns of the minority position
5. Suggest conditions under which this might be revisited

### Part 4: Scope Documentation
Document:
1. What this document IS authoritative about
2. What this document explicitly does NOT address
3. What decisions are deferred to future work
4. What principles might be phased in over time

## Output Format
Produce two documents:
1. `soul-document.md`: The unified founding document
2. `dissenting-appendix.md`: The documented tensions and minority positions
```

### Quality Gate

Before proceeding to Phase 5, verify:
- [ ] Soul Document has coherent voice
- [ ] All major positions are represented fairly
- [ ] Dissenting Appendix handles tensions honestly
- [ ] Scope is clearly documented

---

## Phase 5: Reality Check

**Purpose**: Fresh-eyes practitioner review. PM/EM/Design were NOT in Phases 1-4.

### Execution

- **Three agents**: Product Manager, Engineering Manager, Design Lead
- **Fresh eyes**: These agents have NOT seen any prior work
- **Model selection**: Opus (need senior judgment)
- **Brutal honesty**: License to be skeptical

### Why Fresh Eyes Matter

The agents in Phases 1-4 developed shared context and vocabulary. They may have:
- Over-indexed on philosophical elegance
- Lost sight of practical implementation
- Used jargon that's impenetrable to outsiders
- Made assumptions that aren't obvious

Fresh practitioners catch these blind spots.

### Reality Check Prompt Template

```markdown
You are the [PM/EM/DESIGN_LEAD]. You are reviewing a founding document for the first time.

You were deliberately EXCLUDED from the creation process. Your job is to bring fresh eyes and practical skepticism.

## The Document
[SOUL_DOCUMENT]

## Your Task

### Part 1: First Impressions
Before deep analysis, note:
1. What's your gut reaction?
2. What's clear vs. confusing?
3. What's missing that you expected?
4. What's present that surprises you?

### Part 2: Practitioner Audit
From your [PM/EM/DESIGN] perspective:
1. Can this actually be implemented?
2. What's the realistic timeline?
3. What resources would this require?
4. What existing constraints does this ignore?
5. What stakeholders would object and why?

### Part 3: Jargon Check
Flag any:
1. Undefined terms
2. Circular definitions
3. Insider language
4. Concepts that need examples

### Part 4: Gap Analysis
What's missing?
1. Processes needed but not defined
2. Responsibilities unclear
3. Metrics undefined
4. Edge cases not addressed

### Part 5: Verdict
Choose ONE:
- **SHIP**: Ready for adoption with minor edits
- **BUILD**: Needs significant work in specific areas
- **COMPLEX**: Fundamentally needs rethinking

Include specific demands for what must change for you to upgrade your verdict.

## Format
- Be direct and concrete
- Use examples from your domain
- Propose solutions, not just problems
- Prioritize your concerns (P0/P1/P2)
```

### Quality Gate

Before proceeding to Phase 6, verify:
- [ ] All 3 reality reports received
- [ ] Each report includes verdict (SHIP/BUILD/COMPLEX)
- [ ] Specific demands are actionable
- [ ] Fresh perspective is genuinely fresh (not just restating Phase 1-4)

---

## Phase 6: Final Merge

**Purpose**: Produce the final deliverables for different audiences.

### Execution

- **Single agent**: Polymath Editor
- **Model selection**: Opus (highest quality writing)
- **Output**: Constitution + Practitioner's Guide + Editorial Notes

### Polymath Editor Prompt Template

```markdown
You are the Polymath Editor. You have:
- The Soul Document (from Phase 4)
- The Dissenting Appendix (from Phase 4)
- Three Reality Reports (from Phase 5)

## Your Task

### Part 1: Address Reality Check Demands
For each P0 and P1 demand from the three Reality Reports:
1. Implement the change OR
2. Document why you're rejecting it

### Part 2: Constitution
Create the definitive founding document:
1. Written for posterity (will be read in 5+ years)
2. Uncompromising on principles
3. Clear on scope and authority
4. Includes Dissenting Appendix (edited for clarity)
5. Stands alone without needing other documents

### Part 3: Practitioner's Guide
Create a practical implementation guide:
1. Written for someone starting TODAY
2. Outside-in structure (start with "what do I do?")
3. Examples and templates
4. FAQ section addressing common questions
5. Phased rollout plan if applicable

### Part 4: Editorial Notes
Document your editorial process:
1. What changed from Soul Document to Constitution
2. Which Reality Check demands were accepted/rejected
3. What you consider the most important principles
4. What you consider the biggest risks
5. Advice for future editors

## Output Format
Produce three documents:
1. `constitution.md`: The authoritative founding document
2. `practitioners-guide.md`: The practical how-to guide
3. `editorial-notes.md`: The editorial process documentation
```

### Quality Gate

Final checklist:
- [ ] Constitution is coherent and authoritative
- [ ] Practitioner's Guide is actionable
- [ ] Editorial Notes explain all major decisions
- [ ] All P0 Reality Check demands addressed
- [ ] Dissenting Appendix is honest about tensions

---

## Model Selection Guidelines

| Phase | Recommended Model | Reasoning |
|-------|-------------------|-----------|
| Phase 1 (philosophical agents) | Opus | Deep reasoning, nuanced positions |
| Phase 1 (technical agents) | Sonnet | Faster, still high quality for domain expertise |
| Phase 2 (Synthesizer) | Opus | Long context, complex synthesis |
| Phase 3 (Commentary) | Same as Phase 1 | Consistency of voice |
| Phase 4 (Lead Architect) | Opus | Highest judgment required |
| Phase 5 (Reality Check) | Opus | Senior practitioner simulation |
| Phase 6 (Polymath Editor) | Opus | Best writing quality |

**Cost optimization**: Phases 1 and 3 can use Sonnet for 6-8 of the 10 agents if budget is constrained. Reserve Opus for the most philosophically complex perspectives.

---

## Parallelization with WinDAGs

This process maps naturally to a DAG:

```
Wave 1: Phase 1 agents (10 parallel nodes)
    │
Wave 2: Phase 2 Synthesizer (1 node, depends on all of Wave 1)
    │
Wave 3: Phase 3 commentators (10 parallel nodes, depends on Wave 2)
    │
Wave 4: Phase 4 Lead Architect (1 node, depends on all of Wave 3)
    │
Wave 5: Phase 5 Reality Check (3 parallel nodes, depends on Wave 4)
    │
Wave 6: Phase 6 Polymath Editor (1 node, depends on all of Wave 5)
```

Use `dag-planner` to construct the execution graph.
Use `dag-runtime` to execute with proper isolation.

---

## Anti-Patterns

### Echo Chambering
**Problem**: Agents converge too quickly, lose diversity
**Solution**: Enforce no-cross-talk in Phases 1 and 3. Use different system prompts.

### Context Window Collapse
**Problem**: Later phases lose nuance from earlier phases
**Solution**: Use references, not full documents. Summarize strategically.

### Complexity Theater
**Problem**: Process becomes more important than output
**Solution**: Every phase must produce concrete deliverables. No meta-documents about documents.

### Stale Notifications
**Problem**: Agents wait for human approval that never comes
**Solution**: Define clear quality gates. Automate phase transitions where possible.

### Meta-Risk of Complexity
**Problem**: The synthesis process is itself too complex to be useful
**Solution**: The Constitution must be simpler than the process that created it. If it's not, you've failed.

---

## See Also

- `references/process-design.md` - Why this process works
- `references/phase-templates.md` - Copy-paste prompt templates
- `team-builder` - For selecting agents
- `dag-planner` - For execution planning
- `orchestrator` - For multi-phase coordination
