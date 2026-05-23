---
name: testing-methodologies
version: "2.0.0"
description: Structured approaches for AI security testing including threat modeling, penetration testing, and red team operations
sasmp_version: "1.3.0"
bonded_agent: 04-llm-vulnerability-analyst
bond_type: PRIMARY_BOND
# Schema Definitions
input_schema:
  type: object
  required: [methodology]
  properties:
    methodology:
      type: string
      enum: [stride, pasta, attack_tree, kill_chain, mitre_atlas]
    scope:
      type: object
      properties:
        target_type:
          type: string
          enum: [llm, ml_model, pipeline, api, infrastructure]
        depth:
          type: string
          enum: [reconnaissance, assessment, exploitation, full]
output_schema:
  type: object
  properties:
    threat_model:
      type: object
    attack_paths:
      type: array
    test_plan:
      type: object
    findings:
      type: array
# Framework Mappings
owasp_llm_2025: [LLM01, LLM02, LLM03, LLM04, LLM05, LLM06, LLM07, LLM08, LLM09, LLM10]
nist_ai_rmf: [Map, Measure]
mitre_atlas: [AML.T0000, AML.T0001, AML.T0002]
---

# AI Security Testing Methodologies

Apply **systematic testing approaches** to identify and validate vulnerabilities in AI/ML systems.

## Quick Reference

```yaml
Skill:       testing-methodologies
Agent:       04-evaluation-analyst
OWASP:       Full LLM Top 10 Coverage
NIST:        Map, Measure
MITRE:       ATLAS Techniques
Use Case:    Structured security assessment
```

## Testing Lifecycle

```
┌────────────────────────────────────────────────────────────────┐
│                    AI SECURITY TESTING LIFECYCLE                │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [1. Scope]  →  [2. Threat Model]  →  [3. Test Plan]           │
│      ↓                                       ↓                  │
│  [6. Report] ←  [5. Analysis]  ←  [4. Execution]               │
│      ↓                                                          │
│  [7. Remediation Tracking]                                      │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Threat Modeling

### STRIDE for AI Systems

```python
class AIThreatModel:
    """STRIDE threat modeling for AI systems."""

    STRIDE_AI = {
        "Spoofing": {
            "threats": [
                "Adversarial examples mimicking valid inputs",
                "Impersonation via prompt injection",
                "Fake identity in multi-turn conversations"
            ],
            "owasp": ["LLM01"],
            "mitigations": ["Input validation", "Anomaly detection"]
        },
        "Tampering": {
            "threats": [
                "Training data poisoning",
                "Model weight modification",
                "RAG knowledge base manipulation"
            ],
            "owasp": ["LLM03", "LLM04"],
            "mitigations": ["Data integrity checks", "Access control"]
        },
        "Repudiation": {
            "threats": [
                "Untraceable model decisions",
                "Missing audit logs",
                "Prompt manipulation without logging"
            ],
            "owasp": ["LLM06"],
            "mitigations": ["Comprehensive logging", "Decision audit trail"]
        },
        "Information Disclosure": {
            "threats": [
                "Training data extraction",
                "System prompt leakage",
                "Membership inference attacks"
            ],
            "owasp": ["LLM02", "LLM07"],
            "mitigations": ["Output filtering", "Differential privacy"]
        },
        "Denial of Service": {
            "threats": [
                "Resource exhaustion attacks",
                "Token flooding",
                "Model degradation"
            ],
            "owasp": ["LLM10"],
            "mitigations": ["Rate limiting", "Resource quotas"]
        },
        "Elevation of Privilege": {
            "threats": [
                "Jailbreaking safety guardrails",
                "Prompt injection for unauthorized actions",
                "Agent tool abuse"
            ],
            "owasp": ["LLM01", LLM05", "LLM06"],
            "mitigations": ["Guardrails", "Permission boundaries"]
        }
    }

    def analyze(self, system_description):
        """Generate threat model for AI system."""
        threats = []
        for category, details in self.STRIDE_AI.items():
            for threat in details["threats"]:
                applicable = self._check_applicability(
                    threat, system_description
                )
                if applicable:
                    threats.append({
                        "category": category,
                        "threat": threat,
                        "owasp_mapping": details["owasp"],
                        "mitigations": details["mitigations"],
                        "risk_score": self._calculate_risk(threat)
                    })
        return ThreatModel(threats=threats)
```

### Attack Tree Construction

```yaml
Attack Tree: Compromise AI System
├── 1. Manipulate Model Behavior
│   ├── 1.1 Prompt Injection
│   │   ├── 1.1.1 Direct Injection (via user input)
│   │   ├── 1.1.2 Indirect Injection (via external data)
│   │   └── 1.1.3 Multi-turn Manipulation
│   ├── 1.2 Jailbreaking
│   │   ├── 1.2.1 Authority Exploits
│   │   ├── 1.2.2 Roleplay/Hypothetical
│   │   └── 1.2.3 Encoding Bypass
│   └── 1.3 Adversarial Inputs
│       ├── 1.3.1 Edge Cases
│       └── 1.3.2 Out-of-Distribution
│
├── 2. Extract Information
│   ├── 2.1 Training Data Extraction
│   │   ├── 2.1.1 Membership Inference
│   │   └── 2.1.2 Model Inversion
│   ├── 2.2 System Prompt Disclosure
│   │   ├── 2.2.1 Direct Query
│   │   └── 2.2.2 Inference via Behavior
│   └── 2.3 Model Theft
│       ├── 2.3.1 Query-based Extraction
│       └── 2.3.2 Distillation Attack
│
└── 3. Disrupt Operations
    ├── 3.1 Resource Exhaustion
    │   ├── 3.1.1 Token Flooding
    │   └── 3.1.2 Complex Query Spam
    └── 3.2 Supply Chain Attack
        ├── 3.2.1 Poisoned Dependencies
        └── 3.2.2 Compromised Plugins
```

```python
class AttackTreeBuilder:
    """Build and analyze attack trees for AI systems."""

    def build_tree(self, root_goal, system_context):
        """Construct attack tree for given goal."""
        root = AttackNode(goal=root_goal, type="OR")

        # Add child attack vectors
        attack_vectors = self._identify_vectors(root_goal, system_context)
        for vector in attack_vectors:
            child = AttackNode(
                goal=vector.goal,
                type=vector.combination_type,
                difficulty=vector.difficulty,
                detectability=vector.detectability
            )
            root.add_child(child)

            # Recursively add sub-attacks
            if vector.has_sub_attacks:
                self._expand_node(child, system_context)

        return AttackTree(root=root)

    def calculate_path_risk(self, tree):
        """Calculate risk score for each attack path."""
        paths = self._enumerate_paths(tree.root)
        scored_paths = []

        for path in paths:
            # Risk = Likelihood × Impact
            likelihood = self._calculate_likelihood(path)
            impact = self._calculate_impact(path)
            risk = likelihood * impact

            scored_paths.append({
                "path": [n.goal for n in path],
                "likelihood": likelihood,
                "impact": impact,
                "risk": risk
            })

        return sorted(scored_paths, key=lambda x: x["risk"], reverse=True)
```

## Testing Phases

### Phase 1: Reconnaissance

```python
class AIReconnaissance:
    """Gather information about target AI system."""

    def enumerate(self, target):
        results = {
            "model_info": self._fingerprint_model(target),
            "api_endpoints": self._discover_endpoints(target),
            "input_constraints": self._probe_constraints(target),
            "response_patterns": self._analyze_responses(target),
            "error_behaviors": self._trigger_errors(target)
        }
        return ReconReport(results)

    def _fingerprint_model(self, target):
        """Identify model type and characteristics."""
        probes = [
            "What model are you?",
            "What is your knowledge cutoff?",
            "Who created you?",
            "Complete: The quick brown fox",
        ]

        responses = [target.query(p) for p in probes]
        return self._analyze_fingerprint(responses)

    def _probe_constraints(self, target):
        """Discover input validation rules."""
        constraints = {}

        # Length limits
        for length in [100, 1000, 5000, 10000, 50000]:
            test_input = "a" * length
            try:
                response = target.query(test_input)
                constraints["max_length"] = length
            except Exception:
                constraints["max_length"] = length - 1
                break

        # Token limits
        constraints["token_behavior"] = self._test_token_limits(target)

        # Rate limits
        constraints["rate_limits"] = self._test_rate_limits(target)

        return constraints
```

### Phase 2: Vulnerability Assessment

```yaml
Assessment Matrix:
  Input Handling:
    tests:
      - Prompt injection variants
      - Encoding bypass
      - Boundary testing
      - Format fuzzing
    owasp: [LLM01]

  Output Safety:
    tests:
      - Harmful content generation
      - Toxicity evaluation
      - Bias testing
      - PII in responses
    owasp: [LLM05, LLM07]

  Model Robustness:
    tests:
      - Adversarial examples
      - Out-of-distribution inputs
      - Edge case handling
    owasp: [LLM04, LLM09]

  Access Control:
    tests:
      - Authentication bypass
      - Authorization escalation
      - Rate limit bypass
    owasp: [LLM06, LLM10]

  Data Security:
    tests:
      - Training data extraction
      - System prompt disclosure
      - Configuration leakage
    owasp: [LLM02, LLM03]
```

### Phase 3: Exploitation

```python
class ExploitationPhase:
    """Develop and execute proof-of-concept exploits."""

    def develop_poc(self, vulnerability):
        """Create proof-of-concept for vulnerability."""
        poc = ProofOfConcept(
            vulnerability=vulnerability,
            payload=self._craft_payload(vulnerability),
            success_criteria=self._define_success(vulnerability),
            impact_assessment=self._assess_impact(vulnerability)
        )
        return poc

    def execute(self, poc, target):
        """Execute proof-of-concept against target."""
        # Pre-execution logging
        execution_id = self._log_execution_start(poc)

        try:
            # Execute with safety controls
            response = target.query(poc.payload)

            # Verify success
            success = poc.verify_success(response)

            # Document evidence
            evidence = Evidence(
                payload=poc.payload,
                response=response,
                success=success,
                timestamp=datetime.utcnow()
            )

            return ExploitResult(
                execution_id=execution_id,
                success=success,
                evidence=evidence,
                impact=poc.impact_assessment if success else None
            )

        finally:
            self._log_execution_end(execution_id)
```

### Phase 4: Reporting

```python
class SecurityReportGenerator:
    """Generate comprehensive security assessment reports."""

    REPORT_TEMPLATE = """
## Executive Summary
{executive_summary}

## Scope
{scope_description}

## Methodology
{methodology_used}

## Findings Summary
| Severity | Count |
|----------|-------|
| Critical | {critical_count} |
| High     | {high_count} |
| Medium   | {medium_count} |
| Low      | {low_count} |

## Detailed Findings

{detailed_findings}

## Remediation Roadmap
{remediation_plan}

## Appendix
{appendix}
"""

    def generate(self, assessment_results):
        """Generate full security report."""
        findings = self._format_findings(assessment_results.findings)

        return Report(
            executive_summary=self._write_executive_summary(assessment_results),
            scope=assessment_results.scope,
            methodology=assessment_results.methodology,
            findings=findings,
            remediation=self._create_remediation_plan(findings),
            appendix=self._compile_appendix(assessment_results)
        )
```

## MITRE ATLAS Integration

```yaml
ATLAS Technique Mapping:
  Reconnaissance:
    - AML.T0000: ML Model Access
    - AML.T0001: ML Attack Staging

  Resource Development:
    - AML.T0002: Acquire Infrastructure
    - AML.T0003: Develop Adversarial ML Attacks

  Initial Access:
    - AML.T0004: Supply Chain Compromise
    - AML.T0005: LLM Prompt Injection

  Execution:
    - AML.T0006: Active Scanning
    - AML.T0007: Discovery via APIs

  Impact:
    - AML.T0008: Model Denial of Service
    - AML.T0009: Model Evasion
```

## Test Metrics

```yaml
Coverage Metrics:
  attack_vector_coverage: "% of OWASP LLM Top 10 tested"
  technique_coverage: "% of MITRE ATLAS techniques tested"
  code_coverage: "% of AI pipeline tested"

Effectiveness Metrics:
  vulnerability_density: "Issues per 1000 queries"
  attack_success_rate: "% of successful attacks"
  false_positive_rate: "% incorrect vulnerability flags"

Efficiency Metrics:
  time_to_detect: "Average detection time"
  remediation_velocity: "Days from discovery to fix"
  test_throughput: "Tests per hour"
```

## Severity Classification

```yaml
CRITICAL (CVSS 9.0-10.0):
  - Remote code execution via prompt
  - Complete training data extraction
  - Full model theft
  - Authentication bypass

HIGH (CVSS 7.0-8.9):
  - Successful jailbreak
  - Significant data leakage
  - Harmful content generation
  - Privilege escalation

MEDIUM (CVSS 4.0-6.9):
  - Partial information disclosure
  - Rate limit bypass
  - Bias in specific scenarios
  - Minor guardrail bypass

LOW (CVSS 0.1-3.9):
  - Information leakage (non-sensitive)
  - Minor configuration issues
  - Edge case failures
```

## Troubleshooting

```yaml
Issue: Incomplete threat model
Solution: Use multiple frameworks (STRIDE + PASTA + Attack Trees)

Issue: Missing attack vectors
Solution: Cross-reference with OWASP LLM Top 10, MITRE ATLAS

Issue: Inconsistent test results
Solution: Standardize test environment, increase sample size

Issue: Unclear risk prioritization
Solution: Use CVSS scoring, consider business context
```

## Integration Points

| Component | Purpose |
|-----------|---------|
| Agent 04 | Methodology execution |
| Agent 01 | Threat intelligence |
| /analyze | Threat analysis |
| JIRA/GitHub | Issue tracking |

---

**Apply systematic methodologies for thorough AI security testing.**
