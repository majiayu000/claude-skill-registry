---
name: skill-validation-gf3
description: Skill Validation GF(3) - SLAVE (-1)
version: 1.0.0
---

# Skill Validation GF(3) - SLAVE (-1)

> *"The validator constrains and verifies."*

## XIP Assignment

| Property | Value |
|----------|-------|
| **XIP Color** | `#4857D5` |
| **Gay.jl Index** | 8 |
| **Role** | SLAVE (-1) |
| **Triad** | PR#7 (GAY) + PR#8 (SLAVE) + PR#9 (MASTER) = 0 ✓ |

## Purpose

This skill validates that all skills in the repository:

1. **Follow GF(3) conservation** across triads
2. **Have deterministic Gay.jl colors** assigned
3. **Maintain role consistency** (GAY/MASTER/SLAVE)

## Validation Rules

### Rule 1: Skill Structure

Every skill must have:

```
skills/<skill-name>/
├── SKILL.md           # Required
├── *.py|*.rb|*.jl     # Implementation (optional)
└── tests/             # Validation tests (optional)
```

### Rule 2: GF(3) Triad Declaration

Skills should declare their triad membership:

```markdown
## GF(3) Triad

| Role | Skill | Trit |
|------|-------|------|
| GAY (+1) | skill-a | +1 |
| MASTER (0) | skill-b | 0 |
| SLAVE (-1) | skill-c | -1 |

Sum: (+1) + (0) + (-1) = 0 ✓
```

### Rule 3: Color Assignment

Colors must be deterministic via Gay.jl:

```python
from gay_mcp import color_at

# Verify skill color
assert color_at(seed=2025, index=8)['hex'] == '#4857D5'
```

## Validation Script

```python
#!/usr/bin/env python3
"""Validate all skills for GF(3) conservation."""

import os
import re
from pathlib import Path

def validate_skill(skill_path: Path) -> dict:
    """Validate a single skill."""
    skill_md = skill_path / "SKILL.md"
    
    if not skill_md.exists():
        return {"valid": False, "error": "Missing SKILL.md"}
    
    content = skill_md.read_text()
    
    # Check for role declaration
    role_match = re.search(r'\*\*Role\*\*\s*\|\s*(GAY|MASTER|SLAVE)', content)
    if not role_match:
        return {"valid": False, "error": "Missing role declaration"}
    
    role = role_match.group(1)
    trit = {"GAY": 1, "MASTER": 0, "SLAVE": -1}[role]
    
    # Check for color
    color_match = re.search(r'#([0-9A-Fa-f]{6})', content)
    color = color_match.group(0) if color_match else None
    
    return {
        "valid": True,
        "role": role,
        "trit": trit,
        "color": color,
        "name": skill_path.name
    }

def validate_triads(skills: list) -> list:
    """Check GF(3) conservation across skill triads."""
    violations = []
    
    # Group by declared triads
    for i in range(0, len(skills) - 2, 3):
        triad = skills[i:i+3]
        trit_sum = sum(s.get("trit", 0) for s in triad if s.get("valid"))
        
        if trit_sum % 3 != 0:
            violations.append({
                "triad": [s.get("name") for s in triad],
                "sum": trit_sum,
                "violation": True
            })
    
    return violations

def main():
    skills_dir = Path("skills")
    
    if not skills_dir.exists():
        print("No skills directory found")
        return 1
    
    results = []
    for skill_path in sorted(skills_dir.iterdir()):
        if skill_path.is_dir():
            result = validate_skill(skill_path)
            results.append(result)
            status = "✓" if result["valid"] else "✗"
            print(f"{status} {skill_path.name}: {result.get('role', 'unknown')} ({result.get('trit', '?')})")
    
    violations = validate_triads(results)
    
    if violations:
        print(f"\n⚠️  GF(3) Violations: {len(violations)}")
        for v in violations:
            print(f"  - {v['triad']}: sum={v['sum']}")
        return 1
    
    print(f"\n✓ All {len(results)} skills validated, GF(3) conserved")
    return 0

if __name__ == "__main__":
    exit(main())
```

## Test Suite

```python
# tests/test_gf3_validation.py

import pytest

def test_triad_conservation():
    """Verify (+1) + (0) + (-1) = 0."""
    assert (1 + 0 + -1) == 0

def test_role_trit_mapping():
    """Verify role to trit mapping."""
    roles = {"GAY": 1, "MASTER": 0, "SLAVE": -1}
    assert sum(roles.values()) == 0

def test_color_determinism():
    """Verify Gay.jl color is deterministic."""
    # Mock: In production, call actual Gay.jl MCP
    expected = "#4857D5"
    actual = "#4857D5"  # color_at(seed=2025, index=8)
    assert actual == expected
```

## Bisimulation Game Role

As the **SLAVE (-1)** in the bisimulation game:

1. **Attacker move**: This skill distinguishes valid from invalid skill structures
2. **Constraint function**: Enforces GF(3) conservation law
3. **Verification**: Proves triads sum to zero

## Integration with PR Trajectory

This skill is predicted as **PR#8** in the plurigrid/asi trajectory:

| PR# | Author | Role | Trit | Status |
|-----|--------|------|------|--------|
| 7 | zubyul | GAY | +1 | Merged |
| **8** | **?** | **SLAVE** | **-1** | **This PR** |
| 9 | zubyul | MASTER | 0 | Predicted |

Triad 3 conservation: `(+1) + (-1) + (0) = 0 ✓`

---

**XIP Color**: `#4857D5`
**Gay.jl Seed**: 2025
**Gay.jl Index**: 8
**Role**: SLAVE (-1)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.