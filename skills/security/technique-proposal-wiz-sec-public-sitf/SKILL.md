---
name: technique-proposal
description: Generate a PR-ready technique proposal when an attack step doesn't map to existing SITF techniques. Use after /attack-flow identifies technique gaps.
argument-hint: "<description>" [component]
tools: Read, Grep, Glob
---

# Technique Proposal Generator

Generate a PR-ready technique proposal when an attack step doesn't map to existing SITF techniques.

## Usage

```
/technique-proposal <description> [component]
```

- `description`: Description of the attack step or gap
- `component`: Target component (endpoint, vcs, cicd, registry, production) - optional, will be inferred if omitted

Arguments: $ARGUMENTS

## Instructions

When this skill is invoked:

### Phase 1: Gap Analysis

1. Read `techniques.json` to understand existing techniques.

2. Confirm the gap:
   - Search for semantically similar techniques
   - Verify no existing technique covers this attack step
   - If a match exists, report it and exit

3. **Verify the attack step is within SITF scope** (see Scope Boundaries below)

4. Identify the correct component:
   - endpoint: Developer workstations, IDEs, local tools
   - vcs: Version control systems (GitHub, GitLab, etc.)
   - cicd: CI/CD pipelines, runners, workflows
   - registry: Package registries, container registries
   - production: Production infrastructure **as it relates to supply chain attacks**

5. Determine the attack stage:
   - Initial Access: First foothold in the component
   - Discovery and Lateral Movement: Enumeration, pivoting, credential theft
   - Post-Compromise: Data exfiltration, destruction, persistence

### Scope Boundaries

**SITF covers SDLC infrastructure and software supply chain attacks specifically.** Not all attack steps in an incident warrant new SITF techniques.

#### In Scope (propose technique)
- Attacks on developer workstations, IDEs, and local development tools
- Attacks on version control systems and source code
- Attacks on CI/CD pipelines, runners, and build systems
- Attacks on package/container registries
- Production techniques that are **supply-chain-specific**:
  - Backdooring deployed artifacts to compromise downstream consumers
  - Stealing code signing keys or certificates
  - Modifying release pipelines or deployment configurations
  - Accessing production to pivot back into SDLC systems

#### Out of Scope (do NOT propose technique)
- Generic cloud infrastructure attacks (IAM privilege escalation, cloud misconfigurations)
- Generic container/Kubernetes attacks (pod escape, RBAC abuse, kubelet exploits)
- Generic network attacks (lateral movement via SSH, RDP exploitation)
- Post-exploitation techniques that don't relate to software supply chain

**Example:** If an attacker uses CI/CD as initial access, then pivots to cloud production and uses a Kubernetes privilege escalation technique, the K8s privesc is **out of scope** for SITF. Instead:

1. For attack flows: Mark the step with `"type": "out-of-scope"` and reference the appropriate framework (e.g., "MITRE ATT&CK: Escape to Host - T1611")
2. For technique proposals: Report that the attack step is outside SITF's domain and does not warrant a new technique

**Rationale:** These generic infrastructure techniques are already well-documented in:
- MITRE ATT&CK for Enterprise (Cloud, Containers matrices)
- MITRE ATT&CK for ICS
- Cloud-specific frameworks (AWS Security Maturity Model, Azure Security Benchmark)

SITF adds value by covering the **unique attack surface of SDLC infrastructure** that these frameworks don't address comprehensively.

### Phase 2: Technique ID Assignment

1. Find the highest existing ID for the target component:
   - Endpoint: T-E###
   - VCS: T-V###
   - CI/CD: T-C###
   - Registry: T-R###
   - Production: T-P###

2. Assign the next sequential number.

### Phase 3: Technique Definition

Generate the technique entry following these conventions:

#### Name
- Action-oriented verb phrase
- Match style of existing techniques in same component
- Avoid vendor-specific terms unless unavoidable
- Examples: "Abuse Local AI Tools", "Harvest Local Secrets", "Turn Private Repos Public"

#### Description
- Single sentence describing the attack action
- Focus on what the attacker does, not the impact
- Start with "Attacker..." for consistency

#### Risks
- Focus on **why** this attack is possible (enabling conditions)
- Describe misconfigurations, missing controls, insecure defaults
- Keep each risk as a concise phrase, not a full sentence
- Reference similar risks from related techniques for consistency

#### Controls
- Balance preventive and detective controls
- Reference existing controls from techniques.json for consistency
- Ensure controls are actionable and specific
- Consider both technical and process controls

### Phase 4: Generate Output

Produce a structured proposal with three sections:

#### Section 1: Rationale
Explain:
- What attack behavior this technique covers
- Why existing techniques don't cover it
- Reference to real-world attack(s) demonstrating this technique

#### Section 2: Technique JSON
```json
{
  "id": "T-X###",
  "name": "Technique Name",
  "component": "component-id",
  "stage": "Attack Stage",
  "description": "Attacker does X to achieve Y",
  "risks": [
    "Enabling condition 1",
    "Enabling condition 2"
  ],
  "controls": [
    "Control measure 1",
    "Control measure 2"
  ]
}
```

#### Section 3: PR Description
Markdown-formatted PR description including:
- Title: "Add technique T-X###: Technique Name"
- Summary of the technique
- Real-world references
- Link to related attack flow if applicable

### Phase 5: Validation

Run this checklist before outputting:

```
[ ] Attack step is within SITF scope (SDLC/supply-chain-specific, not generic infra)
[ ] ID follows component naming pattern (T-E/V/C/R/P + number)
[ ] ID doesn't conflict with existing techniques in techniques.json
[ ] Name is action-oriented verb phrase
[ ] Name matches naming style of component's existing techniques
[ ] Stage correctly reflects attack progression semantics
[ ] Description starts with "Attacker..."
[ ] Risks explain enabling conditions, not impacts
[ ] Controls are actionable and specific
[ ] No semantic duplicate of existing technique
[ ] JSON is valid and properly formatted
```

**If scope check fails:** Do not generate a technique proposal. Instead, explain why the attack step is out of scope and recommend the appropriate framework (MITRE ATT&CK, etc.).

### Phase 6: Output Location

1. Display the full proposal in the conversation
2. Optionally create a file at `technique-proposals/<technique-id>.md` if requested

## Example

```
/technique-proposal "Malware invokes AI CLI tools with permission-bypass flags to scan filesystem" endpoint
```

### Example Output

```markdown
## Technique Proposal: T-E019

### Rationale

The s1ngularity attack (August 2025) demonstrated a novel technique where
malware invoked AI CLI tools (Claude, Gemini, Q) with permission-bypass
flags like `--dangerously-skip-permissions` to scan filesystems and catalog
sensitive files.

Existing technique T-E009 (Abuse Local AI Tools) focuses on using AI
assistants to exfiltrate code or inject malicious suggestions via AI
services. It does not cover the scenario where attackers weaponize local
AI tools for automated reconnaissance by exploiting dangerous CLI flags.

### Proposed Addition to techniques.json

{
  "id": "T-E019",
  "name": "Weaponize AI CLI Tools for Reconnaissance",
  "component": "endpoint",
  "stage": "Discovery and Lateral Movement",
  "description": "Attacker invokes AI CLI tools with permission-bypass flags to scan filesystem and catalog sensitive files for exfiltration",
  "risks": [
    "AI CLI tools support dangerous permission-bypass flags",
    "No restrictions on AI tool command-line invocation",
    "AI tools have broad filesystem access",
    "No monitoring of AI tool execution patterns",
    "AI tools can be invoked non-interactively by scripts"
  ],
  "controls": [
    "Disable or remove dangerous permission-bypass flags from AI tools",
    "AI tool invocation monitoring and alerting",
    "Filesystem access restrictions for AI tool processes",
    "EDR detection rules for AI tool abuse patterns",
    "Require interactive confirmation for sensitive AI operations",
    "Application allowlisting for AI tool binaries"
  ]
}

### PR Description

**Add technique T-E019: Weaponize AI CLI Tools for Reconnaissance**

This PR adds a new endpoint technique to cover the weaponization of AI CLI
tools for automated reconnaissance, as demonstrated in the s1ngularity
supply chain attack (August 2025).

The attack showed that malware can invoke AI coding assistants with
permission-bypass flags (e.g., `--dangerously-skip-permissions`, `--yolo`,
`--trust-all-tools`) to recursively scan filesystems and catalog sensitive
files without user interaction.

**References:**
- https://www.wiz.io/blog/s1ngularity-supply-chain-attack
- https://www.stepsecurity.io/blog/supply-chain-security-alert-popular-nx-build-system-package-compromised-with-data-stealing-malware

**Related:** sample-flows/s1ngularity.json
```

## Workflow Integration

This skill is typically used after `/attack-flow` identifies technique gaps:

```
/attack-flow <attack-name>
    ↓
[Gaps identified]
    ↓
/technique-proposal "<gap description>" <component>
    ↓
[Submit PR with proposed technique]
    ↓
[After merge, re-run /attack-flow]
```
