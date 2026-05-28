---
name: ground
description: Anchor claims to evidence from authoritative sources. Use when validating assertions, establishing provenance, verifying facts, or ensuring claims are supported by evidence.
argument-hint: "[claim] [sources] [required_strength]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep
context: fork
agent: explore
layer: MODEL
---

## Intent

Verify that claims are supported by evidence from reliable sources. This is the foundation of the Grounded Agency principle - no assertion should be made without evidence anchors.

**Success criteria:**
- Claim evaluated against available evidence
- Evidence sources identified and referenced
- Grounding strength assessed (strong, moderate, weak, ungrounded)
- Evidence gaps explicitly documented

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `claim` | Yes | string | The claim or assertion to ground |
| `sources` | No | array | Evidence sources to check (files, URLs, commands) |
| `required_strength` | No | string | Minimum grounding level: weak, moderate, strong |

## Procedure

1) **Parse the claim**: Understand what is being asserted
   - Identify the core assertion
   - Note any implicit sub-claims
   - Determine what evidence would support it

2) **Identify evidence sources**: Determine where to look
   - Use provided sources if available
   - Identify additional relevant sources
   - Prioritize authoritative sources

3) **Search for evidence**: Look for supporting or contradicting data
   - Read relevant files and documentation
   - Execute commands to gather data
   - Note both supporting and contradicting evidence

4) **Evaluate evidence quality**: Assess reliability of found evidence
   - Consider source authority
   - Check for recency and relevance
   - Note any bias or limitations

5) **Assess grounding strength**: Determine how well claim is supported
   - Strong: multiple authoritative sources agree
   - Moderate: one authoritative source or multiple secondary
   - Weak: indirect or partial evidence
   - Ungrounded: no supporting evidence found

6) **Document gaps**: Note missing evidence
   - What evidence would strengthen grounding?
   - What sources could not be checked?
   - What assumptions remain unverified?

## Output Contract

Return a structured object:

```yaml
grounded: boolean  # Whether claim meets required_strength
claim: string  # The claim being evaluated
strength: string  # strong, moderate, weak, ungrounded
evidence:
  - source: string  # Evidence source
    type: string  # file, url, command, observation
    content: string  # Relevant excerpt
    supports: boolean  # Supports or contradicts claim
    authority: string  # high, medium, low
contradictions:
  - source: string
    content: string
    severity: string  # How seriously it undermines claim
gaps:
  - description: string  # What evidence is missing
    would_provide: string  # What it would establish
confidence: 0..1
evidence_anchors: ["file:line", "url", "command:output"]
assumptions: []
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `grounded` | boolean | Whether claim meets required evidence threshold |
| `strength` | string | Grounding level: strong, moderate, weak, ungrounded |
| `evidence` | array | Supporting evidence with sources and excerpts |
| `contradictions` | array | Evidence that contradicts the claim |
| `gaps` | array | Missing evidence that would strengthen grounding |

## Examples

### Example 1: Ground a Technical Claim

**Input:**
```yaml
claim: "The payment processor uses Stripe API v2023-10-16"
sources:
  - "Gemfile"
  - "config/initializers/stripe.rb"
required_strength: "strong"
```

**Output:**
```yaml
grounded: true
claim: "The payment processor uses Stripe API v2023-10-16"
strength: "strong"
evidence:
  - source: "Gemfile"
    type: "file"
    content: "gem 'stripe', '~> 10.0'"
    supports: true
    authority: "high"
  - source: "config/initializers/stripe.rb"
    type: "file"
    content: "Stripe.api_version = '2023-10-16'"
    supports: true
    authority: "high"
  - source: "Gemfile.lock"
    type: "file"
    content: "stripe (10.1.0)"
    supports: true
    authority: "high"
contradictions: []
gaps:
  - description: "Runtime verification of API version"
    would_provide: "Confirmation that configured version is actually used"
confidence: 0.95
evidence_anchors:
  - "Gemfile:42"
  - "config/initializers/stripe.rb:3"
  - "Gemfile.lock:156"
assumptions:
  - "Configuration is loaded at runtime"
  - "No environment-specific overrides"
```

### Example 2: Partial Grounding

**Input:**
```yaml
claim: "User authentication requires 2FA for all accounts"
sources:
  - "app/models/user.rb"
  - "config/devise.yml"
required_strength: "strong"
```

**Output:**
```yaml
grounded: false
claim: "User authentication requires 2FA for all accounts"
strength: "weak"
evidence:
  - source: "app/models/user.rb"
    type: "file"
    content: "has_one :two_factor_auth"
    supports: true
    authority: "medium"
  - source: "config/devise.yml"
    type: "file"
    content: "two_factor_authentication: enabled: true"
    supports: true
    authority: "high"
contradictions:
  - source: "app/controllers/sessions_controller.rb"
    content: "skip_2fa_for_api_tokens: true"
    severity: "high"
  - source: "app/models/user.rb"
    content: "scope :without_2fa, -> { where(two_factor_enabled: false) }"
    severity: "medium"
gaps:
  - description: "Policy enforcement mechanism"
    would_provide: "Evidence that 2FA is mandatory, not optional"
  - description: "Admin user configuration"
    would_provide: "Whether admin accounts have different requirements"
confidence: 0.40
evidence_anchors:
  - "app/models/user.rb:15"
  - "config/devise.yml:8"
  - "app/controllers/sessions_controller.rb:23"
assumptions:
  - "2FA support exists but enforcement unclear"
```

### Example 3: Ungrounded Claim

**Input:**
```yaml
claim: "The system processes 10,000 requests per second"
sources:
  - "README.md"
  - "docs/architecture.md"
required_strength: "moderate"
```

**Output:**
```yaml
grounded: false
claim: "The system processes 10,000 requests per second"
strength: "ungrounded"
evidence:
  - source: "README.md"
    type: "file"
    content: "High-performance API server"
    supports: false
    authority: "low"
contradictions: []
gaps:
  - description: "Load test results"
    would_provide: "Measured throughput under load"
  - description: "Production metrics"
    would_provide: "Actual request rates and latencies"
  - description: "Benchmark documentation"
    would_provide: "Performance claims with methodology"
confidence: 0.1
evidence_anchors:
  - "README.md:5"
  - "docs/architecture.md (no relevant content)"
assumptions:
  - "No performance data available in provided sources"
```

## Verification

- [ ] Claim is clearly stated
- [ ] At least one evidence source was checked
- [ ] Strength assessment is consistent with evidence
- [ ] Contradictions are noted if found
- [ ] Evidence anchors reference specific locations

**Verification tools:** Read (to verify evidence excerpts)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Never claim something is grounded without evidence
- Note contradicting evidence even if claim seems grounded
- Flag when sources may be outdated
- Do not fabricate evidence

## Composition Patterns

**Commonly follows:**
- `generate` - Ground generated content
- `predict` - Ground prediction assumptions
- `explain` - Ground explanation premises

**Commonly precedes:**
- `verify` - Grounding enables verification
- `audit` - Grounding supports audit trails
- `plan` - Only proceed with grounded information

**Anti-patterns:**
- Never skip grounding for important assertions
- Avoid accepting claims without evidence in planning

**Workflow references:**
- See `reference/workflow_catalog.yaml#world_model_build` for grounding in world models
- Core principle of Grounded Agency - all skills should ground claims
