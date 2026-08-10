---
name: qa-security-testing
description: "Builds automated security testing pipelines for SAST, DAST, SCA, secret scanning, and containers. Use when integrating scanners into CI or managing security regression gates."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# QA Security Testing

Automated security testing pipelines that integrate scanners into CI/CD, enforce vulnerability gates, and drive findings through remediation. This skill covers the testing automation side of security; for secure design, threat modeling, and architecture review, use [software-security-appsec](../software-security-appsec/SKILL.md).

Start with the quick start workflow below, then dive into specific reference guides. Use current official sources from [data/sources.json](data/sources.json) for tool documentation.

## Quick Start

1. Run a lightweight threat model to identify attack surface and risk areas.
2. Select tools per category (SAST, SCA, DAST, secrets, container/IaC).
3. Integrate into CI with clear gate policies per stage.
4. Establish a triage workflow: confirm, classify, assign, track.
5. Define vulnerability SLAs as a starting policy, then tune them to exploitability, business impact, and compliance obligations.
6. Add security regression tests for every confirmed vulnerability.

## Inputs to Gather

- Application type: web app, API, mobile, CLI, infrastructure.
- Languages, frameworks, and build toolchain.
- Deployment model: containers, serverless, VMs, PaaS.
- Current security tooling and CI platform.
- Compliance requirements: SOC 2, PCI DSS, HIPAA, ISO 27001 if applicable.
- Existing vulnerability management process and acceptable risk thresholds.
- Code hosting platform: GitHub, GitLab, Bitbucket (affects native tool availability).

## Security Testing Categories

### 1. SAST (Static Application Security Testing)

Analyze source code for vulnerabilities without executing it.

- **Recommended tools**: Semgrep (fast, customizable rules, free tier), CodeQL (deep dataflow analysis, GitHub-native), Snyk Code.
- **CI pattern**: run on every PR; a common starter is block merge on high/critical findings, then tune to your risk policy.
- **Key practices**: maintain custom rules for your codebase patterns, manage suppressions with documented reasons, use baseline files to avoid noise from pre-existing findings.
- **Reference**: [references/sast-integration.md](references/sast-integration.md)

### 2. SCA / Dependency Scanning

Detect known vulnerabilities in direct and transitive dependencies.

- **Recommended tools**: Dependabot (GitHub-native, zero config), Snyk Open Source, Renovate + `npm audit` / `pip-audit`, Trivy fs mode.
- **Vulnerability SLAs** (common starting point): critical 24h, high 7d, medium 30d, low 90d. Adjust these to exploitability, asset value, compensating controls, and regulatory commitments.
- **Key practices**: auto-merge patch updates with passing tests, generate SBOMs (CycloneDX or SPDX), track transitive dependency risk.
- **Reference**: [references/dependency-scanning.md](references/dependency-scanning.md)

### 3. DAST (Dynamic Application Security Testing)

Test the running application for vulnerabilities by sending crafted requests.

- **Recommended tools**: ZAP by Checkmarx (open source, automation framework — left OWASP in 2023, same tool), Nuclei (template-based, fast), Burp Suite (manual + CI plugin).
- **CI pattern**: run on staging deploy, not on every PR (too slow). Schedule full scans weekly.
- **Key practices**: configure authenticated scanning, maintain baselines for known findings, scan APIs with OpenAPI specs.
- **Reference**: [references/dast-automation.md](references/dast-automation.md)

### 4. Secret Scanning

Detect credentials, tokens, and keys committed to source code.

- **Recommended tools**: gitleaks (pre-commit + CI), TruffleHog (entropy + regex), GitHub secret scanning (push protection).
- **CI pattern**: hard fail on any active credential or secret material. False positives and documented test fixtures still need an explicit suppression workflow.
- **Key practices**: install pre-commit hooks to catch secrets before push, scan full git history for historical leaks, rotate exposed secrets immediately (removal from code is not sufficient).
- **Reference**: [references/secret-scanning.md](references/secret-scanning.md)

### 5. Container and IaC Scanning

Scan container images and infrastructure-as-code for misconfigurations and CVEs.

- **Recommended tools**: Trivy (containers + IaC + SBOM, single tool), Checkov (Terraform, CloudFormation, Kubernetes). tfsec is deprecated — all checks merged into `trivy config`.
- **CI pattern**: scan on image build; a common starter is block on critical CVEs. Scan IaC on every PR with thresholds matched to environment risk.
- **Key practices**: enforce base image policy (approved images only), scan registry images on schedule, use multi-stage builds to reduce attack surface.
- **Reference**: [references/container-iac-scanning.md](references/container-iac-scanning.md)

### 6. Security Regression Testing

Write test cases that prevent reintroduction of fixed vulnerabilities.

- **Key areas**: auth boundary tests (IDOR, privilege escalation), input validation suites, CORS/CSP/security header verification, business logic abuse cases.
- **CI pattern**: include in standard test suites, run on every PR like functional tests.
- **Reference**: [references/security-regression-testing.md](references/security-regression-testing.md)

## CI Gate Design

Treat gate thresholds as organization policy, not universal defaults. Severity alone is not enough; combine scanner severity with exploitability, reachability, asset sensitivity, and business impact.

| Stage | Tools | Gate Policy |
|-------|-------|-------------|
| Pre-merge (every PR) | SAST + secret scanning + dependency audit | Common starter: block on high/critical SAST, active secrets, and critical/high exploitable CVEs |
| Pre-deploy (staging) | DAST on staging + container scan | Common starter: block on high/critical confirmed DAST findings and critical container CVEs |
| Scheduled (weekly) | Full DAST scan, dependency review, registry scan | Findings feed into triage backlog |
| Release | All gates green + SLA compliance check | Block release when open findings violate the org's release policy or SLA commitments |

## Vulnerability Management Workflow

1. **Triage**: confirm finding is real, classify severity **and exploitability**. Severity (CVSS)
   alone is not triage — combine it with EPSS (probability of real-world exploitation) and
   reachability (can your build actually hit the vulnerable path) before setting priority. See
   [references/owasp-top-10-coverage.md § Triage: Severity vs. Exploitability vs.
   Reachability](references/owasp-top-10-coverage.md#triage-severity-vs-exploitability-vs-reachability)
   for the full model and worked rules of thumb.
2. **Track**: record in issue tracker with severity, EPSS/reachability context, SLA deadline, and remediation plan.
3. **Remediate**: fix, verify fix with regression test, close finding.
4. **Suppress**: if false positive, document reason and reviewer. Review suppressions quarterly — see
   [references/owasp-top-10-coverage.md § False-Positive Economics](references/owasp-top-10-coverage.md#false-positive-economics)
   for why unmanaged false positives cost more than the noise itself.
5. **Measure**: track mean time to remediate, open vulnerability count by severity, scan coverage percentage.
6. **Escalate to human testing when scanners cannot see the risk**: business-logic abuse, exploit
   chains across multiple low-severity findings, and freshly re-architected surfaces need a pen-test
   or red-team engagement, not another scanner run — see [references/owasp-top-10-coverage.md § When
   Pen-Testing Beats Scanning](references/owasp-top-10-coverage.md#when-pen-testing-beats-scanning).

## Quick Reference

| Category | Recommended Tool | CI Stage | Gate Policy |
|----------|-----------------|----------|-------------|
| SAST | Semgrep | Every PR | Common starter: block high/critical |
| SCA | Dependabot + Trivy | Every PR | Common starter: block critical/high exploitable CVE |
| DAST | ZAP / Nuclei | Staging deploy | Common starter: block high/critical confirmed findings |
| Secrets | gitleaks | Every PR + pre-commit | Fail on active secret material |
| Containers | Trivy | Image build | Common starter: block critical CVE |
| IaC | Checkov / Trivy | Every PR | Common starter: block high/critical misconfigurations |
| Regression | Custom test suites | Every PR | Standard test pass/fail |

## Decision Tree

```text
Starting security testing pipeline:
    │
    ├─ New project, no security tooling?
    │   └─ Start with: SAST (Semgrep) + secret scanning (gitleaks) + SCA (Dependabot)
    │       └─ These three give the best signal-to-effort ratio
    │
    ├─ Have SAST/SCA, need runtime testing?
    │   └─ Add DAST: ZAP on staging + Nuclei for targeted templates
    │
    ├─ Running containers?
    │   └─ Add Trivy for image scanning + base image policy
    │
    ├─ Using Terraform/CloudFormation/Kubernetes?
    │   └─ Add Checkov or Trivy IaC scanning on every PR
    │
    ├─ Compliance requirement (SOC 2, PCI, HIPAA)?
    │   └─ Full pipeline + SBOM generation + evidence retention + SLA tracking
    │
    └─ Past security incidents?
        └─ Write regression tests for each, add to standard test suite
```

## Do / Avoid

**Do**:
- Start with SAST + secrets + SCA — cheapest signal, highest coverage.
- Triage findings before enabling CI blocking to avoid developer frustration.
- Tune block thresholds and SLAs to the business risk model instead of copying canned defaults blindly.
- Maintain suppressions with documented reasons and periodic review.
- Rotate any detected secret immediately; removing from code is not enough.
- Write regression tests for every confirmed vulnerability.
- Test authentication boundaries explicitly (IDOR, privilege escalation, tenant isolation).

**Avoid**:
- Blocking CI on every finding without initial triage and baseline.
- Running full DAST scans on every PR (too slow, use staging deploys).
- Treating scanner output as ground truth without human verification.
- Scanning without a remediation workflow (findings without owners rot).
- Ignoring transitive dependency vulnerabilities.
- Storing suppression rules without documented justification.

## Scripts

| Script | Purpose |
|--------|---------|
| [scripts/vuln_tracker.py](scripts/vuln_tracker.py) | Vulnerability tracker and security posture scorer |

Run from the `qa-security-testing/` directory:

```bash
# Overall security posture: counts by severity, SLA rate, overdue items, score
python scripts/vuln_tracker.py status --input data/sample-vulnerabilities.json
```

```bash
# SLA compliance check: list overdue items with days overdue
python scripts/vuln_tracker.py sla --input data/sample-vulnerabilities.json
```

```bash
# Scanner coverage across attack surfaces: flag gaps
python scripts/vuln_tracker.py coverage --input data/sample-scan-coverage.json
```

```bash
# Full Markdown security testing report
python scripts/vuln_tracker.py report \
  --input data/sample-vulnerabilities.json \
  --coverage data/sample-scan-coverage.json \
  --output report.md
```

## Resources

| Resource | Purpose |
|----------|---------|
| [references/sast-integration.md](references/sast-integration.md) | Semgrep and CodeQL setup, custom rules, CI integration |
| [references/dast-automation.md](references/dast-automation.md) | ZAP (by Checkmarx) and Nuclei automation, authenticated scanning |
| [references/dependency-scanning.md](references/dependency-scanning.md) | SCA tools, vulnerability SLAs, SBOM generation |
| [references/secret-scanning.md](references/secret-scanning.md) | gitleaks setup, pre-commit hooks, remediation workflow |
| [references/container-iac-scanning.md](references/container-iac-scanning.md) | Trivy and Checkov for containers and IaC |
| [references/security-regression-testing.md](references/security-regression-testing.md) | Writing security test cases for past vulnerabilities |
| [references/supply-chain-security.md](references/supply-chain-security.md) | SLSA v1.1 build levels, Sigstore/Cosign keyless signing, in-toto attestations, SBOM signing, GitHub provenance, npm/PyPI sigstore |
| [references/owasp-top-10-coverage.md](references/owasp-top-10-coverage.md) | CI scanner mapping for OWASP API Top 10 (2023), OWASP LLM Top 10 v2 (2025), OWASP Top 10 for Agentic Applications (2026, ASI01-10), and OWASP Top 10:2025; notes on ASVS 5.0; plus the severity/exploitability/reachability triage model, pen-test-vs-scanning judgment, and false-positive economics |
| [data/sources.json](data/sources.json) | Curated external sources and documentation links |
| [data/sample-vulnerabilities.json](data/sample-vulnerabilities.json) | Sample B2B SaaS vulnerability list for vuln_tracker.py |
| [data/sample-scan-coverage.json](data/sample-scan-coverage.json) | Sample scanner coverage map for vuln_tracker.py |

## Templates

| Template | Purpose |
|----------|---------|
| [assets/template-security-test-plan.md](assets/template-security-test-plan.md) | Security testing scope, tool selection, and gate policy |
| [assets/template-security-gate-checklist.md](assets/template-security-gate-checklist.md) | Pre-merge, pre-deploy, and release gate checklist |
| [assets/template-vulnerability-sla.md](assets/template-vulnerability-sla.md) | Severity-based SLA table with escalation paths |

## ASCII Flow

```text
Security testing request
  -> Identify attack surface, asset value, compliance needs, and release stage
  -> Select SAST, SCA, secrets, DAST, container, and IaC checks by risk
  -> Wire CI gates with severity, exploitability, and suppression policy
  -> Triage findings: confirm, classify, assign, and set SLA
  -> Add regression tests for confirmed vulnerabilities
  -> Publish evidence for merge, deploy, and release decisions
```

## Navigation

- `## Vulnerability Management Workflow`, `## Decision Tree`, and `## Do / Avoid` for the main sequence
- `## Scripts`, `## Resources`, and `## Templates` for deeper materials and automation
- `## Related Skills` for AppSec, CI, and testing-strategy handoffs
- Game theory (scan scheduling, fuzz seed selection, red-team iteration, BAS): [references/game-theory-applied.md](references/game-theory-applied.md)

## Related Skills

| Skill | Purpose |
|-------|---------|
| [software-security-appsec](../software-security-appsec/SKILL.md) | Secure design, threat modeling, and security review |
| [qa-testing-strategy](../qa-testing-strategy/SKILL.md) | Risk-based test strategy |
| [qa-api-testing-contracts](../qa-api-testing-contracts/SKILL.md) | API contract and security testing |
| [ops-devops-platform](../ops-devops-platform/SKILL.md) | CI/CD pipeline design |
| [dev-dependency-management](../dev-dependency-management/SKILL.md) | Dependency management and update policy |
| [qa-resilience](../qa-resilience/SKILL.md) | Failure mode testing |

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Use web search or web fetch to verify current external facts, versions, pricing, deadlines, regulations, or platform behavior before final answers.
- Prefer primary sources; report source links and dates for volatile information.
- If web access is unavailable, state the limitation and mark guidance as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

