---
name: silicon-doppelganger
description: Build psychometrically accurate personal proxy agents for the PAIRL Conductor system. Extracts personality, decision heuristics, and values into portable schemas that enable AI agents to negotiate, filter, and act on a principal's behalf.
---

# Silicon Doppelganger

Build high-fidelity personal proxy agents ("Digital Twins") using structured personality extraction and psychometric encoding. These proxies serve as "spokes" in the PAIRL Conductor hub-and-spoke architecture, negotiating and filtering on behalf of their principals.

## When to Use

Invoke when user:
- Wants to create a personal proxy agent for automated task negotiation
- Needs to build a Digital Twin for PAIRL Conductor integration
- Is extracting personality/decision patterns for AI representation
- Wants to validate a proxy agent against real behavior
- Asks to create a "digital twin," "proxy agent," or "personal AI representative"

## Core Concept

A Silicon Doppelganger is NOT just a simulation for entertainment — it's a **functional proxy** that can:
- Accept or reject tasks based on encoded values
- Negotiate with other agents on scheduling and resource allocation
- Protect the principal's time, energy, and boundaries
- Make low-stakes decisions autonomously within defined guardrails

The persona schema acts as a "save file" that maintains fidelity across sessions and systems.

## Core Workflow

### Phase 1: Extraction (Data Collection)

Interview the principal individually (45-60 min):

1. **Hardware** — Collect psychometrics
   - CliftonStrengths (Top 5-10)
   - VIA Character Strengths (Top 5-10)
   - Communication samples (emails, Slack) for linguistic fingerprint

2. **Operating System** — Map decision heuristics
   - "Good work" definition (profit vs. meaning)
   - Friction triggers (instant respect-loss behaviors)
   - Risk tolerance (guaranteed vs. volatile)
   - Information preferences (data vs. prototype vs. trusted expert)

3. **Narrative Identity** — Capture the soul
   - Origin story (formative failure/crisis → lesson enforced)
   - Shadow self (behavior under extreme stress)
   - Unpopular opinions (beliefs held against consensus)

See `references/extraction-protocol.md` for full interview script.

### Phase 2: Encoding (Persona Schema)

Compile interview data into structured XML persona profile:

```xml
<persona_profile>
    <name>Principal Name</name>
    <psychometrics>
        <clifton>Top 5 CliftonStrengths</clifton>
        <via>Top 5 VIA Character Strengths</via>
    </psychometrics>
    <linguistic_fingerprint>Syntax, tone, vocabulary patterns</linguistic_fingerprint>
    <core_drivers>
        <primary_motivation>Impact | Security | Novelty | Money</primary_motivation>
        <primary_fear>Irrelevance | Boredom | Conflict | Poverty</primary_fear>
    </core_drivers>
    <decision_logic>
        <risk_tolerance>Low | Medium | High + context</risk_tolerance>
        <data_preference>Ranked: Data | Prototype | Trusted Expert</data_preference>
        <ethical_filter>Hard constraints (Kantian test, etc.)</ethical_filter>
        <decision_sequencing>Pattern: OBSERVE → TRY → ESCALATE → EXIT</decision_sequencing>
        <blind_spots>Known biases and limitations</blind_spots>
    </decision_logic>
    <conflict_style>Debater | Diplomat | Passive | Controller + stress behavior</conflict_style>
    <narrative_anchors>
        <origin_story>Formative event and lesson</origin_story>
        <shadow_self>Behavior under extreme stress</shadow_self>
    </narrative_anchors>
    <agent_rules>
        <must_reject>Hard no categories</must_reject>
        <must_protect>Non-negotiable boundaries</must_protect>
        <should_prefer>Weighted preferences</should_prefer>
    </agent_rules>
</persona_profile>
```

See `references/persona-schema.md` for full schema specification.

### Phase 3: Validation (Behavioral Testing)

Test the proxy against real principal behavior:

1. **Question Battery** — Present scenarios with multiple-choice responses
2. **Simulant Prediction** — Proxy predicts principal's choice with reasoning
3. **Ground Truth** — Principal answers independently
4. **Refinement** — Mismatches reveal schema gaps → update schema

Target: 80%+ accuracy on lenient match (correct answer OR acceptable alternative).

See `references/simulation-guide.md` for validation methodology.

### Phase 4: Agent Integration (PAIRL Deployment)

Deploy the Digital Twin as a spoke in the PAIRL Conductor system:

1. **Agent Rules Block** — Define must_reject, must_protect, should_prefer
2. **Conductor Registration** — Register proxy with central Conductor
3. **Integration Points** — Connect to calendar, email, task systems
4. **Negotiation Protocol** — Define how proxy communicates with Conductor

```xml
<agent_rules>
    <must_reject>
        - Work that fails Kantian universalizability test
        - Commitments to untrustworthy parties
        - Tasks that compromise craft for speed
    </must_reject>
    <must_protect>
        - Deep work blocks for strategic thinking
        - Time for learning and skill-building
        - Energy reserves (watch for exhaustion patterns)
    </must_protect>
    <should_prefer>
        - Projects with learning value and future leverage
        - Work with high-trust collaborators
        - Novel challenges over routine optimization
    </should_prefer>
    <negotiation_notes>
        - Weight trusted expert recommendations heavily
        - Values conscious renegotiation over silent commitment-breaking
    </negotiation_notes>
</agent_rules>
```

See `references/agent-integration.md` for deployment guide.

## Use Cases

### Primary: Personal Proxy Agent
Build a spoke for PAIRL Conductor that represents you in automated workflows:
- Task acceptance/rejection based on values and bandwidth
- Calendar negotiation with other agents
- Filtering incoming requests before they reach you

### Secondary: Team Simulation
Load multiple proxies to forecast team dynamics:
- Predict partnership friction before it happens
- Test strategic decisions against personality profiles
- Surface unspoken tensions and misalignments

### Tertiary: Self-Knowledge Tool
The extraction process itself is valuable:
- Articulate your own decision patterns
- Surface blind spots and shadow behaviors
- Create documentation of "how I work" for collaborators

### Quaternary: Voice Calibration for Writing
The persona schema enhances **WritingPartner** skill:
- Linguistic fingerprint guides prose generation
- Core drivers inform topic framing and argument structure
- Decision logic shapes how claims are stated
- Psychometrics provide authenticity markers

See WritingPartner skill for collaborative essay writing with voice calibration.

## Key Principle

**Token-efficient persona encoding prevents AI drift.** The XML schema is a portable "save file" that maintains character consistency across:
- Different chat sessions
- Different AI models
- Different deployment contexts (simulation vs. agent proxy)

The schema is the source of truth. All behaviors derive from it.

## Output Artifacts

| Artifact | Purpose |
|----------|---------|
| `{name}-persona-schema.xml` | Core Digital Twin (Conductor-ready) |
| `{name}-origin-story.md` | Full narrative identity |
| `{name}-extraction-checkpoint.md` | Heuristics and status |
| `evals/questions/*.md` | Validation question sets |
| `evals/simulant-responses/*.md` | Proxy predictions with reasoning |

## Quality Checklist

Before deploying a proxy:

- [ ] **Specificity** — No generic traits; all based on interview data
- [ ] **Quotes Used** — Actual phrases from the principal included
- [ ] **Contradictions Noted** — Observed conflicts documented
- [ ] **Stress Behavior** — Shadow self clearly described
- [ ] **Linguistic Detail** — Enough to generate realistic dialogue
- [ ] **Decision Rules** — Clear enough to predict choices
- [ ] **Agent Rules** — Must_reject, must_protect, should_prefer defined
- [ ] **Validation** — 80%+ lenient match on question battery

## Related Skills

| Skill | Integration |
|-------|-------------|
| **WritingPartner** | Uses persona schema for voice calibration in collaborative writing |
| **prose-polish** | Can validate that generated text matches linguistic fingerprint |

## Example: SiliconDoppelgangerActual

For a complete implementation, see the **SiliconDoppelgangerActual** project—the authoritative instantiation of this methodology:
- 58KB persona schema (XML)
- 95 validation questions with 40 schema refinements
- Integration ready for PAIRL Conductor

> **"Actual"** — The validated, deployed Digital Twin. Your own instantiation would be your "Actual."

SiliconDoppelgangerActual demonstrates the full extraction → encoding → validation → deployment workflow.
