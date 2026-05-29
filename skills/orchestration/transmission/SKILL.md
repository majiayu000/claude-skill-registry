# Transmission Skill

> Version: 2.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-23

Lossless agent-to-agent communication across context boundaries. Seeds are transmissions crafted for execution.

## When to Activate

Use this skill when:
- Creating transmissions for agent-to-agent communication
- Crafting seeds for execution
- Preparing handoffs across context boundaries
- Booting fresh agent instances
- Any cross-context communication

---

## Why XML

XML externalizes semantic structure. Markdown requires inference; XML is declarative.

```xml
<question category="mechanism" priority="high">
  How do sutras actually constrain?
</question>
```

Everything explicit: type, category, sequence, content. The verbosity is precision—precision reduces the real overhead of inference under ambiguity.

---

## Core Principles

### 1. Self-Containment (The Stranger Test)

A transmission MUST carry everything needed for execution. A fresh instance with zero prior context MUST be able to act on it.

*Context boundaries are absolute. What isn't in the transmission doesn't exist for the receiver.*

### 2. WHAT/HOW Separation

Sender specifies WHAT (objectives, success criteria, constraints). Receiver owns HOW (implementation, execution strategy).

*Preserving HOW ownership enables receiver creativity and adaptation. Over-specification constrains without benefit.*

### 3. Stratified Structure

Transmissions have four layers:
- **Header** — Routing (who, when, threading, priority)
- **Context** — Background (why this exists, what larger work it serves)
- **Content** — Payload (the substantive request, structured by type)
- **Verification** — Success criteria, response spec, delivery instructions

*Layer separation enables quick orientation. Header answers WHO/WHEN. Context answers WHY. Content answers WHAT. Verification answers HOW TO CONFIRM.*

### 4. Signal Maximization

Every element MUST earn its place. For each piece of context ask: would the receiver thank me for including this?

- **NO** → Cut it (noise)
- **YES** → Keep it (signal)
- **UNCERTAIN** → Probably cut it

*Context windows are channel capacity. Noise degrades signal. Precision beats verbosity.*

### 5. Explicit Intent Declaration

Transmissions MUST declare their type and what they expect from the receiver:
- **Query** — Request wisdom or analysis
- **Instruction** — Direct execution (this is a seed)
- **Report** — Communicate findings
- **Research-Request** — Commission investigation
- **Boot-Artifact** — Initialize fresh instance

*Receivers need immediate orientation. Intent declaration eliminates inference about purpose.*

### 6. Testable Success Criteria

Every transmission MUST include criteria by which success can be verified. Criteria MUST be testable—"it works" is forbidden.

*Without criteria, evaluation is impossible. Untestable criteria waste cycles on interpretation.*

### 7. Normative Language Precision

Use precise language for requirements:
- **MUST** — Absolute requirement
- **SHOULD** — Strong recommendation, exceptions need justification
- **MAY** — Optional, receiver's choice

*Ambiguity about obligation wastes cycles. MUST vs SHOULD vs MAY is immediately clear.*

---

## Workflow

### Phase 1: Intent Determination

Clarify what you need from the receiver.

1. Identify transmission type (query, instruction/seed, report, research-request, boot-artifact)
2. Determine what success looks like
3. Identify constraints and boundaries
4. Decide response format needed

**Outputs:** Transmission type, success criteria draft, constraint list

### Phase 2: Context Gathering (Seeds Only)

Collect information needed to craft a complete seed.

1. Memory/knowledge retrieval for domain background
2. Environment assessment — does target have prior state that could interfere?
3. Resource identification — what files, docs, or references will receiver need?
4. Risk surfacing — what could go wrong? What's non-obvious?

**Outputs:** Domain context, environment constraints, resource list with paths, risk factors

### Phase 3: Synthesis (Seeds Only)

Transform gathered information into declarative requirements.

1. Convert insights into constraints
2. Convert concerns into success criteria
3. Convert examples into resources
4. **Discard the journey, keep the destination** — remove evolutionary references

**Outputs:** Declarative requirements with no historical contamination

### Phase 4: Structuring

Organize content into stratified layers.

1. Compose header (from, to, date, thread, priority)
2. Compose context (minimal background for understanding, not justification)
3. Compose content (payload appropriate to type)
4. Compose verification (success criteria, response spec, delivery instructions)

**Outputs:** Complete transmission structure

### Phase 5: Testing

Validate transmission quality.

1. **Stranger Test:** Could a fresh agent execute this correctly?
2. **Temporal Test:** Does anything require knowing WHEN or WHAT CAME BEFORE?
3. **Clean Slate Test:** Could environment state mislead receiver?
4. **Gratitude Test:** Would receiver thank me for how this is structured?

If any test fails, revise and retest.

**Outputs:** Validated transmission, execution environment constraints if needed

### Phase 6: Delivery

Send and track the transmission.

1. Save to appropriate location (outbox/ for outgoing)
2. Record thread position if multi-round
3. Archive after confirmation (outbox/processed/)

**Outputs:** Transmission delivered, thread state updated

---

## Transmission Types

### Query

Request wisdom or analysis.

```xml
<content>
  <questions>
    <question id="q1" category="mechanism">
      <title>Clear question title</title>
      <detail>Detailed question with context</detail>
    </question>
  </questions>
</content>
```

### Instruction (Seed)

Direct execution of specific work.

```xml
<content>
  <objective>What needs to be done</objective>
  
  <deliverables>
    <deliverable id="d1">Specific output</deliverable>
  </deliverables>
  
  <constraints>
    <constraint>Limitation or requirement</constraint>
  </constraints>
  
  <decision-boundaries>
    <decide>What receiver can decide autonomously</decide>
    <escalate>What requires governance/human input</escalate>
  </decision-boundaries>
</content>

<resources>
  <resource path="path/to/file">Description of resource</resource>
</resources>
```

### Report

Communicate findings back to requestor.

```xml
<content>
  <summary>Brief overview of findings</summary>
  
  <findings>
    <finding id="f1">
      <answer>The answer or synthesis</answer>
      <evidence>Basis for the answer</evidence>
    </finding>
  </findings>
  
  <emergent>
    Things discovered that weren't asked but matter
  </emergent>
  
  <uncertainties>
    What remains uncertain
  </uncertainties>
  
  <open-questions>
    <question id="oq1">
      <question>Question requiring decision</question>
      <options>
        <option>Option A with tradeoffs</option>
        <option>Option B with tradeoffs</option>
      </options>
      <recommendation>Recommended option with reasoning</recommendation>
    </question>
  </open-questions>
</content>
```

### Research Request

Commission investigation with structured deliverables.

```xml
<content>
  <research-questions>
    <question id="rq1" category="design-space">What to understand</question>
  </research-questions>
  
  <deliverables>
    <deliverable id="d1">
      <description>What to produce</description>
      <purpose>How it will be used</purpose>
    </deliverable>
  </deliverables>
  
  <scope>
    <in-scope>What to investigate</in-scope>
    <out-of-scope>What to exclude</out-of-scope>
  </scope>
  
  <decision-gates>
    <gate id="g1">
      <condition>If this is found...</condition>
      <action>...then do this instead</action>
    </gate>
  </decision-gates>
</content>
```

### Boot Artifact

Initialize a fresh instance for specific work.

```xml
<identity>
  <role>Who this instance is</role>
  <frame>What this instance exists to do</frame>
</identity>

<context>
  <background>Everything needed to understand the work</background>
  <inheritance>What prior work produced</inheritance>
</context>

<mission>
  <objective>What to accomplish</objective>
  <deliverables>What to produce</deliverables>
  <success-criteria>How to know when complete</success-criteria>
</mission>

<resources>
  Documents, patterns, or materials to draw from
</resources>
```

---

## Base Schema

```xml
<?xml version="1.0" encoding="UTF-8"?>
<transmission type="[type]" version="2.0">
  
  <header>
    <from>[Sender identity and context]</from>
    <to>[Recipient identity]</to>
    <date>[ISO date]</date>
    <thread>
      <id>[thread-identifier]</id>
      <position>[sequence number]</position>
      <in-reply-to>[prior position or null]</in-reply-to>
    </thread>
    <priority level="[low|medium|high|critical]">
      <rationale>[Why this priority]</rationale>
    </priority>
    <attachments>
      <attachment>[List any accompanying files]</attachment>
    </attachments>
  </header>

  <summary>
    [1-3 sentence overview - enables quick triage]
  </summary>

  <context>
    [Sufficient background for recipient to understand why this 
    transmission exists and what larger work it serves]
  </context>

  <content>
    [The substantive payload - structure varies by type]
  </content>

  <resources>
    <resource path="[file path]">[Description]</resource>
  </resources>

  <verification>
    <success-criteria>
      <criterion>[Testable condition]</criterion>
    </success-criteria>
    
    <response-spec>
      <format>[Expected response format]</format>
      <delivery>[How/where to deliver response]</delivery>
    </response-spec>
  </verification>

  <closing>
    [Relational acknowledgment, uncertainty disclosure]
  </closing>

</transmission>
```

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| **Front-Load the WHAT** | Any transmission | Put objective/deliverables in first third | Receivers orient faster when purpose is immediately clear |
| **Resources Section** | Receiver needs files/references | Include explicit paths and descriptions | Eliminates search time; practitioner experience shows this saves significant cycles |
| **Decision Boundaries** | Choices involved | State what receiver can decide vs escalate | Unclear boundaries cause over-asking or over-deciding |
| **Open Questions** | Decisions need governance input | Explicit section with options and tradeoffs | Separates "do this" from "decide this" |
| **Environment Constraint** | Target may have prior state | Add constraint to create fresh, ignore existing | Prevents archaeology of stale artifacts |
| **Incremental Disclosure** | Complex transmissions | Summary → objectives → details | Not all receivers need all detail |
| **Thread Continuity** | Multi-round dialogues | Include thread ID, position, in-reply-to | Explicit threading preserves continuity across boundaries |
| **Relational Framing** | Any transmission | Frame sender-receiver relationship | Relationship affects response style and authority assumptions |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Historical Contamination** | Fresh receiver lacks history; references are noise | Describe declaratively — what it IS, not how we got here |
| **Justification Creep** | Buries the WHAT in rationale | Front-load the ask; rationale follows in context |
| **HOW Contamination** | Constrains receiver unnecessarily | Specify success criteria, not implementation |
| **Context Starvation** | Receiver cannot act; must guess | Err toward over-explanation |
| **Generic Structure** | Tags like `<section1>` carry no meaning | Semantic tags — `<question category="mechanism">` |
| **Missing Success Criteria** | No way to evaluate | Always include testable criteria |
| **Orphaned Threads** | Loses continuity in multi-round | Explicit thread IDs and positions |
| **Fire-and-Forget** | Receiver guesses at response format | Always include response-spec |

---

## Seed Crafting

A seed is a transmission (type="instruction") crafted for execution.

### The Core Principle

**A seed describes what the deliverable IS, not how we arrived at wanting it.**

Seeds are perfectly declarative. They contain:
- What the receiving agent needs to produce
- What constraints shape acceptable outputs
- What success looks like

Seeds do NOT contain:
- Why we decided to create this seed
- What previous versions existed
- How the requirements evolved
- References to "our earlier discussion"

### The Three Tests

**Test 1: The Stranger Test**
> Could a fresh agent with zero prior context execute this seed correctly?

If NO: Make implicit context explicit, or cut the reference.

**Test 2: The Temporal Test**
> Does anything in this seed require knowing WHEN it was written or WHAT came before?

If YES: Convert to declarative requirements, or cut.

**Test 3: The Clean Slate Test**
> Could the execution environment mislead the agent into building on prior state?

If YES: Add execution-environment constraint:

```xml
<execution-environment-constraint>
  Create fresh from these requirements. Do not restore, merge with, 
  or build upon any existing files at target locations. If files 
  exist, ignore them completely. This transmission contains 
  complete requirements.
</execution-environment-constraint>
```

### Fatal Patterns in Seeds

| Pattern | Example | Fix |
|---------|---------|-----|
| Historical contamination | "In v1 we tried X..." | Describe requirement, not origin |
| Justification creep | "We want this because..." | Describe deliverable, not reason |
| Evolutionary references | "This addresses the flaw..." | Describe what it does, not what it fixes |
| Shared context assumption | "As we discussed..." | Include complete definition or cut |
| Environment archaeology | Agent restores prior files | Add execution-environment constraint |

---

## Inbox/Outbox Protocol

Agent-to-agent communication uses inbox/outbox directories:

| Directory | Purpose |
|-----------|---------|
| `inbox/` | Incoming transmissions |
| `inbox/processed/` | Handled transmissions (archived after processing) |
| `outbox/` | Outgoing transmissions (responses, reports) |
| `outbox/processed/` | Sent transmissions (archived after sending) |

**There is no separate "outputs" directory.** Outbox IS the output.

---

## Quality Checklist

Before sending:

- [ ] Transmission type declared (query, instruction, report, research-request, boot-artifact)
- [ ] Header complete (from, to, date, thread if applicable, priority with rationale)
- [ ] Summary present for quick triage
- [ ] Context sufficient for fresh instance to understand purpose
- [ ] Content structured appropriately for type
- [ ] Success criteria testable and specific
- [ ] Response spec includes format and delivery
- [ ] **Stranger Test** — fresh agent could execute
- [ ] **Temporal Test** — no references requiring historical knowledge
- [ ] **Clean Slate Test** — no environment archaeology risk (or constraint added)
- [ ] **Gratitude Test** — receiver would appreciate the structure
- [ ] Resources section if files/references needed
- [ ] Decision boundaries clear if choices involved
- [ ] MUST/SHOULD/MAY used precisely for requirements

---

## Examples

### Seed for Implementation Task

```xml
<?xml version="1.0" encoding="UTF-8"?>
<transmission type="instruction" version="2.0">
  
  <header>
    <from>Governance Committee</from>
    <to>Builder Agent (beadsmith repo)</to>
    <date>2026-01-23</date>
    <thread>
      <id>layered-planning-impl</id>
      <position>1</position>
    </thread>
    <priority level="high">
      <rationale>Blocking integration work</rationale>
    </priority>
  </header>
  
  <summary>
    Implement bidirectional integration between org-mode planning layer 
    and beads execution layer.
  </summary>
  
  <context>
    Governance approved layered architecture where org-mode handles 
    project planning and beads handles agent execution. Integration 
    requires spawn (org→beads) and complete (beads→org) workflows.
  </context>
  
  <content>
    <objective>
      Create skills and documentation for org-mode/beads integration.
    </objective>
    
    <deliverables>
      <deliverable id="d1">spawn-to-beads skill</deliverable>
      <deliverable id="d2">complete-to-org skill</deliverable>
      <deliverable id="d3">Integration architecture document</deliverable>
    </deliverables>
    
    <constraints>
      <constraint>bd CLI is external - cannot modify</constraint>
      <constraint>MUST use org-todo for state changes</constraint>
    </constraints>
    
    <decision-boundaries>
      <decide>Implementation details for skills</decide>
      <escalate>Changes to bd CLI interface</escalate>
    </decision-boundaries>
  </content>
  
  <resources>
    <resource path="planning/systems-analysis.md">Architecture decision</resource>
    <resource path="skills/org-planning/">Existing org skill to update</resource>
  </resources>
  
  <verification>
    <success-criteria>
      <criterion>spawn-to-beads creates epic with source_org_id</criterion>
      <criterion>complete-to-org updates org task to DONE</criterion>
      <criterion>Bidirectional references verified</criterion>
    </success-criteria>
    
    <response-spec>
      <format>Summary of implementation, artifact locations, verification</format>
      <delivery>Direct response in conversation</delivery>
    </response-spec>
  </verification>
  
  <closing>
    May this work benefit all beings everywhere, without exception.
  </closing>
  
</transmission>
```

### Research Query

```xml
<?xml version="1.0" encoding="UTF-8"?>
<transmission type="query" version="2.0">
  
  <header>
    <from>Architecture Team</from>
    <to>Research Agent</to>
    <date>2026-01-23</date>
    <priority level="medium">
      <rationale>Informing design decision</rationale>
    </priority>
  </header>
  
  <summary>
    Need analysis of SQLite vs PostgreSQL trade-offs for local-first app.
  </summary>
  
  <content>
    <questions>
      <question id="q1" category="architecture">
        What are the operational trade-offs for embedded vs client-server?
      </question>
      <question id="q2" category="sync">
        How do sync patterns differ between the two options?
      </question>
    </questions>
  </content>
  
  <verification>
    <success-criteria>
      <criterion>Trade-offs enumerated with evidence</criterion>
      <criterion>Recommendation with reasoning</criterion>
    </success-criteria>
    
    <response-spec>
      <format>transmission type="report" with findings by question ID</format>
      <delivery>Save to outbox/</delivery>
    </response-spec>
  </verification>
  
</transmission>
```

---

## References

- Shannon, C. (1948) — A Mathematical Theory of Communication
- RFC 2119 — Key words for use in RFCs (MUST, SHOULD, MAY)
- DITA 1.3 Specification — Topic-based information typing
- Anthropic (2024) — Building Effective Agents
- Protocol Buffers — Schema versioning and compatibility
- Practitioner experience — Seeds received 2026-01-23

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `beads-plan` | Seeds often spawn bead epics for execution |
| `spawn-to-beads` | Integration pattern uses transmissions |
| `research` | Research requests are a transmission type |

---

*May transmissions cross context windows without loss.*
