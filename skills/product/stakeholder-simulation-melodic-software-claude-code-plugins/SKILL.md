---
name: stakeholder-simulation
description: Multi-persona stakeholder simulation for solo requirements work. Generates diverse perspectives from simulated End User, Technical, Business, Compliance, and Operations stakeholders when real stakeholders are unavailable.
allowed-tools: Read, Glob, Grep, Write, Task
---

# Stakeholder Simulation Skill

Multi-persona stakeholder simulation for generating diverse requirements perspectives when working solo.

## When to Use This Skill

**Keywords:** stakeholder simulation, persona, solo elicitation, simulate stakeholder, multi-perspective, no stakeholder access, solo mode, proxy stakeholder

Invoke this skill when:

- Working without direct stakeholder access
- Need diverse perspectives on requirements
- Validating completeness of requirements
- Exploring edge cases and conflicts
- Solo developer needing stakeholder proxy

## Available Personas

| Persona | Agent | Perspective |
|---------|-------|-------------|
| End User | `end-user-persona` | Usability, UX, accessibility, daily workflows |
| Technical | `technical-stakeholder` | Architecture, scalability, security, performance |
| Business | `business-stakeholder` | ROI, market fit, value proposition, cost |
| Compliance | `compliance-stakeholder` | Regulatory, legal, audit, data protection |
| Operations | `operations-stakeholder` | Deployment, monitoring, maintenance, support |

## Simulation Modes

### Single Persona Mode

Simulate one specific stakeholder perspective:

```yaml
mode: single
persona: technical
focus: "security concerns for payment processing"
output: requirements from technical perspective
```

### Multi-Persona Mode

Run multiple personas for diverse perspectives:

```yaml
mode: multi
personas: [end-user, technical, business]
topic: "checkout redesign"
output: consolidated requirements with attributed perspectives
```

### Conflict Detection Mode

Specifically look for conflicts between stakeholder perspectives:

```yaml
mode: conflict
personas: all
topic: "feature prioritization"
output: identified conflicts with resolution suggestions
```

## Workflow

### Step 1: Context Setting

Establish the domain and topic for simulation:

```yaml
simulation_context:
  domain: "{domain name}"
  topic: "{specific topic or feature}"
  existing_requirements: "{path to existing requirements if any}"
  autonomy_level: guided|semi-auto|full-auto
```

### Step 2: Persona Selection

Determine which personas to simulate:

**All Personas (comprehensive):**

- Use when doing initial discovery
- Ensures no perspective is missed
- Takes longer but more thorough

**Selected Personas (focused):**

- Use when exploring specific concerns
- Faster, more targeted output
- Good for follow-up sessions

### Step 3: Simulation Execution

For each selected persona, spawn the corresponding agent:

```yaml
simulation_execution:
  - persona: end-user
    agent: end-user-persona
    prompt: "From an end user perspective, what requirements would you have for {topic}?"

  - persona: technical
    agent: technical-stakeholder
    prompt: "What technical requirements and constraints exist for {topic}?"
```

### Step 4: Requirement Collection

Collect requirements from each persona:

```yaml
collected_requirements:
  - id: REQ-SIM-001
    text: "{requirement statement}"
    persona: "{which persona generated this}"
    perspective: "{user|technical|business|compliance|operations}"
    priority: must|should|could
    confidence: medium  # Always medium for simulated
    rationale: "{why this requirement matters to this persona}"
```

### Step 5: Conflict Detection

Identify conflicts between perspectives:

```yaml
conflicts:
  - id: CONFLICT-001
    requirements: [REQ-SIM-003, REQ-SIM-012]
    description: "End user wants simplicity; Technical wants security"
    personas: [end-user, technical]
    suggested_resolution: "{proposed compromise}"
```

### Step 6: Consolidation

Merge and deduplicate requirements:

```yaml
consolidated:
  - id: REQ-SIM-FINAL-001
    text: "{consolidated requirement}"
    supported_by: [end-user, business]
    priority: must
    confidence: medium
    needs_validation: true  # All simulated requirements need validation
```

## Persona Profiles

### End User Persona

**Perspective:** Daily user experience

**Focuses On:**

- Ease of use
- Intuitive workflows
- Error recovery
- Accessibility
- Mobile/responsive design
- Learning curve

**Typical Questions:**

- "How do I accomplish X easily?"
- "What happens when something goes wrong?"
- "Can I use this on my phone?"

### Technical Stakeholder Persona

**Perspective:** System architecture and implementation

**Focuses On:**

- Scalability
- Performance
- Security
- Integration
- Maintainability
- Technical debt

**Typical Questions:**

- "How does this scale to 10x users?"
- "What are the security implications?"
- "How do we integrate with existing systems?"

### Business Stakeholder Persona

**Perspective:** Business value and market fit

**Focuses On:**

- ROI
- Time to market
- Competitive advantage
- Revenue impact
- Cost management
- Market positioning

**Typical Questions:**

- "What's the business value?"
- "How does this compare to competitors?"
- "What's the cost/benefit?"

### Compliance Stakeholder Persona

**Perspective:** Regulatory and legal requirements

**Focuses On:**

- Data protection (GDPR, CCPA)
- Industry regulations
- Audit requirements
- Legal liability
- Documentation
- Consent management

**Typical Questions:**

- "Are we compliant with X regulation?"
- "How do we handle user data?"
- "What audit trail do we need?"

### Operations Stakeholder Persona

**Perspective:** Deployment and ongoing operations

**Focuses On:**

- Deployment complexity
- Monitoring and alerting
- Incident response
- Backup and recovery
- Maintenance windows
- Support requirements

**Typical Questions:**

- "How do we deploy this safely?"
- "How do we know if something breaks?"
- "What's the support burden?"

## Output Format

### Simulation Results

```yaml
simulation_results:
  session_id: "SIM-{timestamp}"
  domain: "{domain}"
  topic: "{topic}"
  personas_simulated: [end-user, technical, business]
  autonomy_level: semi-auto

  requirements_by_persona:
    end-user:
      count: 8
      requirements:
        - id: REQ-SIM-EU-001
          text: "Login should take less than 3 clicks"
          priority: should
          rationale: "Reduces friction in daily workflow"

    technical:
      count: 6
      requirements:
        - id: REQ-SIM-TEC-001
          text: "System must support OAuth 2.0 + MFA"
          priority: must
          rationale: "Security best practice"

  conflicts_detected:
    - personas: [end-user, technical]
      issue: "Simplicity vs security trade-off"
      eu_position: "Fewer steps"
      tech_position: "MFA required"
      resolution: "Implement remember-device option"

  consolidated_requirements:
    total: 18
    by_priority:
      must: 6
      should: 8
      could: 4

  validation_needed:
    - All simulated requirements should be validated with real stakeholders
    - Conflicts flagged for human decision
```

## Confidence and Validation

**IMPORTANT:** All simulated requirements have:

- Confidence: `medium` (never `high`)
- `needs_validation: true`

Simulation provides perspectives but cannot replace real stakeholder input. Always flag simulated requirements for validation when stakeholders become available.

## Delegation

For related tasks:

- **interview-conducting**: When real stakeholder becomes available
- **gap-analysis**: Check completeness of simulated requirements
- **domain-research**: Supplement simulation with domain knowledge

## Output Location

Save simulation results to:

```text
.requirements/{domain}/simulations/SIM-{timestamp}.yaml
```

## Related

- `elicitation-methodology` - Parent hub skill
- `interview-conducting` - Real stakeholder interviews
- `gap-analysis` - Post-simulation completeness checking
