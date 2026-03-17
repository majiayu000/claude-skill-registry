---
name: defense-in-depth
description: Multi-layer validation strategy for CFN Loop to prevent "consensus on vapor" and ensure robust, high-quality deliverables
---

# Defense-in-Depth Validation for CFN Loop

## Overview

In the Claude Flow Novice system, defense-in-depth validation prevents low-quality or incomplete work by enforcing rigorous checks at multiple coordination layers.

**Core Principle:** Validate deliverables, confidence, and context at EVERY stage of the CFN Loop workflow.

## Validation Layers in CFN Loop

### Layer 1: Coordinator Context Extraction
**Purpose:** Validate task description and initial context

```bash
# Mandatory fields in context extraction
REQUIRED_FIELDS=(
  "epicGoal"          # 1-2 sentence description
  "inScope"           # Specific, achievable objectives
  "outOfScope"        # Clear boundaries
  "deliverables"      # Exact file paths/names
  "directory"         # Target creation path
  "acceptanceCriteria" # Measurable requirements
)

validate_coordinator_context() {
  for field in "${REQUIRED_FIELDS[@]}"; do
    if [[ -z "${CONTEXT[$field]}" ]]; then
      echo "❌ INVALID: Missing required context field: $field"
      return 1
    fi
  done
}
```

### Layer 2: Orchestrator Agent Spawning Validation
**Purpose:** Ensure agents receive complete, actionable context

```bash
validate_agent_context() {
  # Reference STRAT-025: Explicit Deliverable Tracking
  DELIVERABLES_CHECKLIST=$(
    for file in "${CONTEXT[deliverables]}"; do
      if [[ -f "$file" ]]; then
        echo "✅ $file"
      else
        echo "❌ $file MISSING"
      fi
    done
  )

  # Confidence calculation based on deliverable completion
  COMPLETION_RATE=$(calculate_completion_rate "$DELIVERABLES_CHECKLIST")

  # Enforce low confidence if any deliverables missing
  if (( $(echo "$COMPLETION_RATE < 0.50" | bc -l) )); then
    AGENT_CONFIDENCE=0.25
  fi
}
```

### Layer 3: Loop 2 Validator Quality Gate
**Purpose:** Enforce strict consensus validation

```bash
validate_loop2_consensus() {
  # Reference STRAT-020: Mandatory Deliverable Verification
  if [[ "$DELIVERABLES_CREATED" -eq 0 ]]; then
    echo "❌ NO DELIVERABLES CREATED"
    OVERRIDE_CONSENSUS="ITERATE"
    FEEDBACK="Iteration required: No deliverables produced"
  fi

  # Consensus threshold enforcement
  if (( $(echo "$CONSENSUS_SCORE < 0.90" | bc -l) )); then
    echo "❌ CONSENSUS TOO LOW"
    OVERRIDE_CONSENSUS="ITERATE"
  fi
}
```

### Layer 4: Product Owner Decision Validation
**Purpose:** Final quality and strategic alignment check

```bash
validate_product_owner_decision() {
  # Verify deliverables match epic goals
  STRATEGIC_ALIGNMENT=$(assess_strategic_match)

  if [[ "$STRATEGIC_ALIGNMENT" -lt 0.75 ]]; then
    echo "❌ LOW STRATEGIC ALIGNMENT"
    DECISION="ABORT"
    REASON="Deliverables do not match epic objectives"
  fi
}
```

## Redis-based Quality Coordination

Implement quality gates using Redis pub/sub for zero-token coordination:

```bash
# Quality gate blocking mechanism
redis-cli BLPOP "cfn_loop:quality_gate:$TASK_ID" 0

# Signal quality validation result
redis-cli LPUSH "cfn_loop:quality_result:$TASK_ID" "$VALIDATION_STATUS"
```

## Confidence and Consensus Mapping

**Confidence Thresholds:**
- Gate Threshold: ≥0.75
- Consensus Threshold: ≥0.90
- Product Owner Strategic Alignment: ≥0.85

## Key Insights

1. **Multi-Layer Validation:** Each layer adds a unique validation perspective
2. **Prevent "Consensus on Vapor":** Strict deliverable tracking
3. **Dynamic Iteration:** Automatic re-execution when quality gates fail
4. **Zero-Token Coordination:** Redis pub/sub enables efficient quality management

## Implementation References
- STRAT-020: Mandatory Deliverable Verification
- STRAT-025: Explicit Deliverable Tracking
- PATTERN-022: Agent Lifecycle Management

**Success is not consensus, but verifiable, high-quality deliverables.**