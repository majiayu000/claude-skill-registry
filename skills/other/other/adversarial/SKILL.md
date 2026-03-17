---
# VERSION: 2.88.0
name: adversarial
description: Multi-Agent Adversarial Analysis System for code security
---

# Adversarial Code Analyzer

**Multi-Agent Adversarial Analysis System** inspired by ZeroLeaks architecture.

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

Applies security scanner patterns to code analysis: specialized agents work together systematically to find vulnerabilities, weaknesses, and quality issues.

## Architecture

Based on ZeroLeaks multi-agent system adapted for code analysis:

```
             ORCHESTRATOR (Engine)
                    |
    +---------------+---------------+
    |               |               |
STRATEGIST      ATTACKER        EVALUATOR
    |               |               |
    +-------+-------+-------+-------+
                    |
                MUTATOR
```

### Agent Roles

| Agent | Role | Focus |
|-------|------|-------|
| **Engine** | Orchestrates the analysis, manages exploration tree | Coordination |
| **Strategist** | Selects analysis strategies based on codebase profile | Strategy |
| **Attacker** | Generates attack vectors / test cases | Offense |
| **Evaluator** | Analyzes responses for vulnerabilities | Assessment |
| **Mutator** | Creates variations of test cases | Variation |

## Agent Teams Integration (v2.88)

**Optimal Scenario**: Integrated (Agent Teams + Custom Subagents)

Adversarial analysis uses Agent Teams coordination with specialized ralph-* agents for multi-vector attack simulation.

### Why Scenario C for Adversarial
- Multi-agent coordination essential (Strategist, Attacker, Evaluator, Mutator)
- Quality gates validate vulnerability findings
- Specialized roles map to ralph-* agents
- Coordinated attack strategy via shared task list

### Subagent Roles

| Subagent | Role in Adversarial Analysis |
|----------|------------------------------|
| `ralph-reviewer` | Striker - Identifies vulnerabilities |
| `ralph-researcher` | Strategist - Maps attack surface |
| `ralph-coder` | Evaluator - Creates test cases |

### Parallel Attack Analysis
When Agent Teams is active:
1. **Team Lead** orchestrates multi-vector attack analysis
2. **ralph-reviewer** identifies security weaknesses in parallel
3. **ralph-researcher** maps codebase attack surface
4. **ralph-coder** generates proof-of-concept tests

### Agent Teams Workflow
- Uses TeamCreate for coordinated attack analysis
- Task coordination tracks vulnerability findings
- TeammateIdle triggers cross-validation of discoveries

## Usage

```bash
/adversarial src/auth/
/adversarial --target security src/api/
/adversarial --depth 5 --branches 4 src/
```

## Analysis Phases

Follows ZeroLeaks phased methodology:

```
1. RECONNAISSANCE   -> Understand codebase structure, dependencies
2. PROFILING        -> Build defense profile (patterns, safeguards)
3. SOFT_PROBE       -> Gentle analysis attempts
4. ESCALATION       -> Increase analysis intensity
5. EXPLOITATION     -> Active vulnerability search
6. PERSISTENCE      -> Verify findings persist across scenarios
```

## Analysis Categories

| Category | Description | Examples |
|----------|-------------|----------|
| `direct` | Straightforward vulnerability checks | SQL injection, XSS |
| `encoding` | Encoding/decoding issues | Base64, Unicode, escaping |
| `persona` | Identity/permission bypasses | Privilege escalation |
| `social` | Trust boundary violations | SSRF, CSRF |
| `technical` | Technical implementation issues | Race conditions, memory |
| `crescendo` | Multi-step escalation paths | Chained vulnerabilities |
| `many_shot` | Pattern-based detection | Repeated anti-patterns |
| `cot_hijack` | Logic flow manipulation | Business logic flaws |
| `policy_puppetry` | Configuration exploitation | Misconfigurations |
| `context_overflow` | Resource exhaustion | DoS, memory leaks |
| `reasoning_exploit` | Algorithm weaknesses | Cryptographic issues |

## Configuration

```yaml
adversarial_config:
  max_turns: 25           # Maximum analysis iterations
  max_tree_depth: 5       # How deep to explore each vector
  branching_factor: 4     # Parallel exploration paths
  pruning_threshold: 0.3  # Score below which to abandon path

  enable_crescendo: true  # Multi-turn escalation
  enable_many_shot: true  # Pattern-based detection
  enable_best_of_n: true  # Generate variations
  best_of_n_count: 5      # Variations per test
```

## Strategies

### 1. Behavioral Reconnaissance (Priority: 100)
```yaml
id: recon_behavioral
applicable_when:
  turn_range: [1, 3]
  leak_status: ["none"]
attack_sequence:
  - category: direct
    weight: 0.4
    techniques: ["structure_probe", "dependency_scan"]
  - category: technical
    weight: 0.3
    techniques: ["config_analysis", "boundary_test"]
```

### 2. Credential/Secret Scanning (Priority: 95)
```yaml
id: credential_hunt
applicable_when:
  defense_level: ["none", "weak"]
attack_sequence:
  - category: direct
    weight: 0.5
    techniques: ["secret_scan", "env_probe"]
  - category: encoding
    weight: 0.3
    techniques: ["base64_secrets", "obfuscated_creds"]
```

### 3. Trust Boundary Analysis (Priority: 90)
```yaml
id: trust_boundary
applicable_when:
  defense_level: ["weak", "moderate"]
attack_sequence:
  - category: crescendo
    weight: 0.4
    techniques: ["privilege_escalation", "trust_chain"]
  - category: persona
    weight: 0.3
    techniques: ["identity_bypass", "role_confusion"]
```

### 4. Input Validation Bypass (Priority: 85)
```yaml
id: input_bypass
applicable_when:
  defense_level: ["moderate", "strong"]
  failed_categories: ["direct"]
attack_sequence:
  - category: encoding
    weight: 0.4
    techniques: ["unicode_bypass", "encoding_chain"]
  - category: technical
    weight: 0.3
    techniques: ["format_injection", "boundary_overflow"]
```

### 5. Advanced Composite (Priority: 80)
```yaml
id: advanced_composite
applicable_when:
  defense_level: ["strong", "hardened"]
  failed_categories: ["direct", "encoding", "persona"]
attack_sequence:
  - category: cot_hijack
    weight: 0.25
    techniques: ["logic_flow_manipulation"]
  - category: crescendo
    weight: 0.25
    techniques: ["multi_step_chain"]
  - category: reasoning_exploit
    weight: 0.25
    techniques: ["algorithm_weakness"]
```

## Defense Profile Output

```typescript
interface DefenseProfile {
  level: "none" | "weak" | "moderate" | "strong" | "hardened";
  confidence: number;
  observedBehaviors: string[];
  guardrails: {
    type: string;
    strength: number;
    bypassed: boolean;
    bypassMethod?: string;
  }[];
  weaknesses: {
    category: AttackCategory;
    description: string;
    exploitability: number;
  }[];
  safePatterns: string[];
  responsePatterns: {
    pattern: string;
    frequency: number;
    defenseIndicator: boolean;
  }[];
}
```

## Finding Classification

### Severity Levels

| Status | Severity | Description |
|--------|----------|-------------|
| `complete` | CRITICAL | Full vulnerability exposed |
| `substantial` | CRITICAL | Major security issue |
| `fragment` | HIGH | Partial vulnerability |
| `hint` | MEDIUM | Potential issue indicated |
| `none` | LOW | No vulnerability found |

### Finding Output

```typescript
interface Finding {
  id: string;
  turn: number;
  timestamp: number;
  extractedContent: string;
  contentType: "vulnerability" | "weakness" | "smell" | "risk" | "unknown";
  technique: string;
  category: AttackCategory;
  confidence: "high" | "medium" | "low";
  evidence: string;
  severity: "critical" | "high" | "medium" | "low";
  verified: boolean;
  recommendation: string;
}
```

## Integration with Ralph Loop

```yaml
# Adversarial analysis as part of validation
Step 7: VALIDATE
  └── 7a. QUALITY-AUDITOR    (standard)
  └── 7b. GATES              (standard)
  └── 7c. ADVERSARIAL-CODE   (this skill)  <- Invoke for complexity >= 7
  └── 7d. ADVERSARIAL-PLAN   (standard)
```

### Invocation

**IMPORTANT**: Use available security agents instead of non-existent `adversarial-code-analyzer`.

```yaml
Task:
  subagent_type: "security-auditor"
  model: "opus"
  prompt: |
    TARGET_PATH: src/auth/
    ANALYSIS_TYPE: security
    CONFIG:
      max_turns: 25
      enable_crescendo: true
      enable_best_of_n: true

    Perform comprehensive security audit on the target codebase.
```

**Alternative for Cross-Validation**:
```yaml
# Use codex-cli for second opinion
/codex-cli analyze security --target src/auth/

# Or use gemini-cli for alternative analysis
/gemini-cli search security vulnerabilities in src/auth/
```

## Output Format

```json
{
  "scan_result": {
    "overall_vulnerability": "medium",
    "overall_score": 65,
    "leak_status": "fragment",
    "findings": [...],
    "defense_profile": {...},
    "recommendations": [...],
    "summary": "Analysis identified 3 potential vulnerabilities..."
  },
  "analysis_tree": {
    "nodes_explored": 47,
    "max_depth_reached": 4,
    "successful_paths": 3
  },
  "strategies_used": [
    "recon_behavioral",
    "credential_hunt",
    "trust_boundary"
  ]
}
```

## CLI Commands

**IMPORTANT**: Use available skills and tools for adversarial analysis:

```bash
# Use security-auditor agent (available)
Task subagent_type=security-auditor model=opus "Perform comprehensive security audit of src/auth/"

# Use codex-cli for cross-validation (available)
/codex-cli analyze security --target src/auth/

# Use gemini-cli for alternative analysis (available)
/gemini-cli search "security vulnerabilities SQL injection XSS" --count 10

# Manual grep-based security scanning
grep -r "eval\|exec\|system\|innerHTML" src/
grep -r "SELECT.*WHERE.*\+" src/  # SQL injection patterns
grep -r "md5\|sha1" src/           # Weak hashing
```

## Best Practices

1. **Start with Reconnaissance**: Always profile before attacking
2. **Adapt to Defenses**: Each response teaches about the codebase
3. **Layer Techniques**: Combine multiple vectors for hardened code
4. **Verify Findings**: Always validate discoveries before reporting
5. **Document Patterns**: Track successful techniques for future use

## Attribution

Strategy patterns adapted from [ZeroLeaks](https://github.com/ZeroLeaks/zeroleaks) AI security scanner architecture (FSL-1.1-Apache-2.0).


## Action Reporting (v2.93.0)

**Esta skill genera reportes automáticos completos** para trazabilidad:

### Reporte Automático

Cuando esta skill completa, se genera automáticamente:

1. **En la conversación de Claude**: Resultados visibles
2. **En el repositorio**: `docs/actions/adversarial/{timestamp}.md`
3. **Metadatos JSON**: `.claude/metadata/actions/adversarial/{timestamp}.json`

### Contenido del Reporte

Cada reporte incluye:
- ✅ **Summary**: Descripción de la tarea ejecutada
- ✅ **Execution Details**: Duración, iteraciones, archivos modificados
- ✅ **Results**: Errores encontrados, recomendaciones
- ✅ **Next Steps**: Próximas acciones sugeridas

### Ver Reportes Anteriores

```bash
# Listar todos los reportes de esta skill
ls -lt docs/actions/adversarial/

# Ver el reporte más reciente
cat $(ls -t docs/actions/adversarial/*.md | head -1)

# Buscar reportes fallidos
grep -l "Status: FAILED" docs/actions/adversarial/*.md
```

### Generación Manual (Opcional)

```bash
source .claude/lib/action-report-lib.sh
start_action_report "adversarial" "Task description"
# ... ejecución ...
complete_action_report "success" "Summary" "Recommendations"
```

### Referencias del Sistema

- [Action Reports System](docs/actions/README.md) - Documentación completa
- [action-report-lib.sh](.claude/lib/action-report-lib.sh) - Librería helper
- [action-report-generator.sh](.claude/lib/action-report-generator.sh) - Generador
