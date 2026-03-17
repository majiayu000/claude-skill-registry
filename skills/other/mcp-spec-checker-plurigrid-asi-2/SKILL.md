---
name: mcp-spec-checker
description: Predicate-level semantic diff for MCP protocol specs. Compares 0618 vs 1125 specs via Narya types, GF(3) evaluators, and Unison-style effects. Use for protocol verification, spec migration, or detecting breaking changes.
---

# MCP Spec Checker

Semantic diff engine for MCP protocol specifications using three independent verification approaches with mandatory cross-validation.

## Three Verification Approaches

| Approach | File | Trit | Role |
|----------|------|------|------|
| **Narya Types** | `src/mcp_narya_types.py` | -1 (MINUS) | chk/syn/nosyn bidirectional typing |
| **Agent-o-rama Evaluators** | `src/mcp_evaluators.py` | 0 (ERGODIC) | GF(3) predicate evaluation |
| **Unison Effects** | `src/mcp_effects.py` | +1 (PLUS) | Algebraic effect handlers |

GF(3) Conservation: `(-1) + 0 + (+1) = 0 ✓`

## GF(3) Trit Assignments for Predicates

```python
# From src/mcp_spec_predicates.py

PREDICATE_TRITS = {
    # MINUS (-1): Constraint/validation predicates
    "has_required_field": -1,
    "type_matches": -1,
    "schema_valid": -1,
    
    # ERGODIC (0): Coordination predicates
    "version_compatible": 0,
    "capability_negotiated": 0,
    "session_active": 0,
    
    # PLUS (+1): Generation/action predicates
    "tool_invoked": +1,
    "response_emitted": +1,
    "resource_created": +1,
}
```

## Denotation

> **This skill compares MCP protocol specs at the predicate level, detecting semantic differences between versions and generating minimal counterexamples for incompatibilities via cross-validated triadic verification.**

```
SemanticDiff = Inv_0618 △ Inv_1125 (symmetric difference)
Counterexample: min{msg : Inv_0618(msg) ≠ Inv_1125(msg)}
Consensus: ∀ approach ∈ {Narya, Evaluators, Effects}: result_agree
```

## Invariant Set

| Invariant | Definition | Verification |
|-----------|------------|--------------|
| `SpecVersionCompatibility` | Old spec passing → new spec passing OR documented breaking change | Diff analysis |
| `PredicateConsistency` | Same predicate → same trit across versions | Trit comparison |
| `CrossValidationConsensus` | All 3 approaches agree on validity | Bisimulation game |
| `CounterexampleMinimality` | Generated counterexamples are minimal witnesses | Size minimization |

## GF(3) Typed Effects

| Approach | Trit | Effect | Description |
|----------|------|--------|-------------|
| Narya Types | -1 | VALIDATOR | Type-checks messages via chk/syn/nosyn |
| Evaluators | 0 | COORDINATOR | Runtime predicate evaluation |
| Unison Effects | +1 | GENERATOR | Generates effect traces and fixes |

## Narya Compatibility

| Field | Definition |
|-------|------------|
| `before` | Initial spec version (e.g., 0618) |
| `after` | Target spec version (e.g., 1125) |
| `delta` | Semantic diff (strengthened, relaxed, breaking) |
| `birth` | Null spec (no predicates) |
| `impact` | 1 if breaking changes detected |

## Condensation Policy

**Trigger**: When 3 incompatible predicates are detected.

**Action**: Generate migration guide, emit counterexamples, mark as BREAKING.

## Invariant Sets

### Inv_0618 (June 2024 Spec)

```python
Inv_0618 = {
    "initialize_required": True,
    "tools_list_before_invoke": True,
    "prompt_field_required": False,
    "result_or_error_exclusive": True,
    "capabilities_optional": True,
}
```

### Inv_1125 (November 2025 Spec)

```python
Inv_1125 = {
    "initialize_required": True,
    "tools_list_before_invoke": False,  # BREAKING CHANGE
    "prompt_field_required": True,       # BREAKING CHANGE
    "result_or_error_exclusive": True,
    "capabilities_optional": False,      # BREAKING CHANGE
}
```

## Semantic Diff (Not Text Diff)

```python
from mcp_spec_unified import semantic_diff

diff = semantic_diff(Inv_0618, Inv_1125)
# Output:
# {
#   "breaking": [
#     {"predicate": "tools_list_before_invoke", "0618": True, "1125": False},
#     {"predicate": "prompt_field_required", "0618": False, "1125": True},
#     {"predicate": "capabilities_optional", "0618": True, "1125": False},
#   ],
#   "compatible": [
#     {"predicate": "initialize_required", "value": True},
#     {"predicate": "result_or_error_exclusive", "value": True},
#   ],
#   "gf3_balance": 0  # Sum of predicate trits
# }
```

## Counterexample Generation

When predicates disagree, generate minimal counterexamples:

```python
from mcp_spec_unified import generate_counterexample

# Find minimal message that passes 0618 but fails 1125
counterex = generate_counterexample(
    spec_pass=Inv_0618,
    spec_fail=Inv_1125,
    predicate="prompt_field_required"
)
# Output:
# {
#   "message": {"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "example"}},
#   "0618_result": "PASS",
#   "1125_result": "FAIL: missing required field 'prompt'",
#   "fix": {"params": {"name": "example", "prompt": ""}}
# }
```

## Cross-Validation (All 3 Approaches Must Agree)

```python
from mcp_spec_unified import cross_validate

result = cross_validate(
    message={"jsonrpc": "2.0", "method": "tools/call", ...},
    spec_version="1125"
)
# Output:
# {
#   "narya_types": {"result": "VALID", "trit": -1, "mode": "chk"},
#   "evaluators": {"result": "VALID", "trit": 0, "predicates_passed": 12},
#   "unison_effects": {"result": "VALID", "trit": +1, "effects_handled": ["IO", "Abort"]},
#   "consensus": True,
#   "gf3_sum": 0,
#   "confidence": 1.0
# }
```

### Disagreement Handling

```python
# If approaches disagree, report conflict
result = cross_validate(message, spec_version="1125")
if not result["consensus"]:
    print(f"CONFLICT: {result['conflicts']}")
    # Arbiter (ERGODIC) breaks ties
    final = result["evaluators"]["result"]
```

## CLI Examples

```bash
# Compare two spec versions
just mcp-spec-diff 0618 1125

# Validate message against spec
just mcp-spec-check message.json --spec 1125

# Generate counterexamples for all breaking changes
just mcp-spec-counterex 0618 1125

# Cross-validate with all three approaches
just mcp-spec-validate message.json --cross-validate

# Run test trace
just mcp-spec-trace tests/protocol_trace.jsonl
```

## Test Traces

### Valid 1125 Trace

```jsonl
{"seq": 1, "direction": "client->server", "message": {"jsonrpc": "2.0", "method": "initialize", "params": {"capabilities": {"tools": true}}}}
{"seq": 2, "direction": "server->client", "message": {"jsonrpc": "2.0", "result": {"serverInfo": {"name": "test"}}}}
{"seq": 3, "direction": "client->server", "message": {"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "example", "prompt": "test"}}}
{"seq": 4, "direction": "server->client", "message": {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": "ok"}]}}}
```

### Trace Validation Output

```
╔═══════════════════════════════════════════════════════════════════╗
║  MCP Spec Checker: Trace Validation                               ║
╚═══════════════════════════════════════════════════════════════════╝

Spec Version: 1125
Trace: tests/protocol_trace.jsonl (4 messages)

─── Narya Types (chk/syn) ───
  Message 1: ✓ chk(initialize) : Request
  Message 2: ✓ syn(result) : Response
  Message 3: ✓ chk(tools/call) : Request
  Message 4: ✓ syn(result) : Response
  Trit: -1

─── Evaluators (GF(3)) ───
  Predicates: 12/12 passed
  Breaking changes: 0
  Trit: 0

─── Unison Effects ───
  Effects handled: [IO, Abort, State]
  Unhandled: []
  Trit: +1

─── Cross-Validation ───
  Consensus: ✓ ALL AGREE
  GF(3) Sum: (-1) + 0 + (+1) = 0 ✓
  
RESULT: VALID
```

## Source Files

| File | Purpose |
|------|---------|
| [src/mcp_narya_types.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/mcp_narya_types.py) | Bidirectional type checking (chk/syn/nosyn) |
| [src/mcp_evaluators.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/mcp_evaluators.py) | GF(3) predicate evaluators |
| [src/mcp_effects.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/mcp_effects.py) | Unison-style algebraic effects |
| [src/mcp_spec_predicates.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/mcp_spec_predicates.py) | Predicate definitions with trit assignments |
| [src/mcp_spec_unified.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/mcp_spec_unified.py) | Unified cross-validation engine |

## Integration with Other Skills

| Skill | Trit | Integration |
|-------|------|-------------|
| [sheaf-cohomology](file:///Users/alice/.claude/skills/sheaf-cohomology/SKILL.md) | -1 | Local-to-global consistency for spec patches |
| [ordered-locale](file:///Users/alice/.agents/skills/ordered-locale-proper/SKILL.md) | 0 | Directed spec evolution (0618 ≪ 1125) |
| [bisimulation-game](file:///Users/alice/.agents/skills/bisimulation-game/SKILL.md) | -1 | Verify spec equivalence via game semantics |
| [gay-mcp](file:///Users/alice/.agents/skills/gay-mcp/SKILL.md) | +1 | Deterministic test case generation |

## Narya Type Modes

```
chk (checking mode):  Given type, check term has it
syn (synthesis mode): Given term, synthesize type
nosyn (no synthesis): Term cannot synthesize (must check)
```

Applied to MCP:
- `chk(Request)`: Validate incoming message matches Request schema
- `syn(response)`: Infer response type from message structure
- `nosyn(partial)`: Partial messages require explicit type annotation

---

**Skill Name**: mcp-spec-checker  
**Type**: Protocol Verification / Semantic Diff  
**Trit**: 0 (ERGODIC - coordinates three approaches)  
**GF(3)**: Narya(-1) + Evaluators(0) + Unison(+1) = 0 ✓
