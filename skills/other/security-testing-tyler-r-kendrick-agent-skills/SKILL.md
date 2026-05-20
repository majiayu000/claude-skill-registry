---
name: security-testing
description: |
    Use when selecting and configuring security testing tools for your CI/CD pipeline. Covers SAST, DAST, SCA, container scanning, secrets detection, and infrastructure-as-code security scanning with cross-platform tool recommendations.
    USE FOR: SAST, DAST, SCA, Semgrep, SonarQube, CodeQL, Snyk, OWASP ZAP, Burp Suite, Trivy, Falco, GitLeaks, TruffleHog, Checkov, container scanning, secrets scanning, IaC scanning
    DO NOT USE FOR: functional testing (use testing skills), performance testing (use testing/performance-testing), threat modeling (use threat-modeling)
license: MIT
metadata:
  displayName: "Security Testing Tools"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "OWASP Web Security Testing Guide"
    url: "https://owasp.org/www-project-web-security-testing-guide/"
  - title: "NIST SP 800-115 Technical Guide to Information Security Testing"
    url: "https://csrc.nist.gov/publications/detail/sp/800-115/final"
  - title: "Semgrep Documentation"
    url: "https://semgrep.dev/docs/"
---

# Security Testing Tools

## Overview

Security testing spans the entire software delivery pipeline — from the moment code is written through build, deployment, and runtime in production. No single tool or technique is sufficient; effective security testing requires layering multiple approaches at different stages of the pipeline. Static analysis catches coding flaws before execution, dynamic analysis discovers runtime vulnerabilities in deployed applications, composition analysis identifies known vulnerabilities in dependencies, and runtime monitoring detects threats in production. The goal is to create a security testing strategy that is automated, continuous, and integrated into the CI/CD pipeline so that vulnerabilities are caught as early and as cheaply as possible.

## Security Testing Categories

| Category | What It Tests | When | Tools |
|---|---|---|---|
| SAST (Static Application Security Testing) | Source code, bytecode, or binaries for coding flaws | During development and at commit/PR time | Semgrep, SonarQube, CodeQL, Snyk Code |
| DAST (Dynamic Application Security Testing) | Running applications for runtime vulnerabilities | Against staging or pre-production environments | OWASP ZAP, Burp Suite, Nuclei |
| SCA (Software Composition Analysis) | Third-party dependencies for known vulnerabilities | At build time and continuously in production | Snyk, Dependabot, Trivy, Grype + Syft |
| Container Security | Container images and runtime behavior | At build and in production | Trivy, Falco, Sysdig, Aqua |
| Secrets Detection | Code and history for leaked credentials | At commit time (pre-commit hooks) and in CI | TruffleHog, GitLeaks, detect-secrets |
| IaC Security | Infrastructure-as-code templates for misconfigurations | At commit/PR time and before deployment | Checkov, Trivy config, Terrascan, KICS |

## SAST (Static Application Security Testing)

SAST tools analyze source code without executing it, identifying vulnerabilities such as SQL injection, cross-site scripting, buffer overflows, and insecure cryptographic usage. SAST is most effective when integrated into the developer workflow (IDE plugins, PR checks) so that issues are caught before code is merged.

| Tool | Languages | Approach | Cost |
|---|---|---|---|
| Semgrep | 30+ languages | Pattern matching with lightweight, customizable rules | OSS core + commercial (Semgrep AppSec Platform) |
| SonarQube | 10+ languages | Dataflow analysis with taint tracking and quality gates | Community (free) + commercial editions |
| CodeQL | 6+ languages (C/C++, C#, Go, Java, JavaScript, Python, Ruby) | Semantic code analysis using a query language over a code database | Free for open-source projects |
| Snyk Code | All major languages | Machine learning-based analysis with real-time IDE feedback | Freemium (free tier + paid plans) |

### Key Considerations for SAST

- **False positive rate** — Evaluate tools on your actual codebase; pattern-matching tools (Semgrep) tend to have lower false positive rates but may miss deeper dataflow issues.
- **Developer experience** — IDE integration and clear remediation guidance are essential for developer adoption.
- **Custom rules** — The ability to write organization-specific rules (e.g., enforcing internal API usage patterns) is a significant differentiator.

## DAST (Dynamic Application Security Testing)

DAST tools test running applications by sending crafted requests and analyzing responses for evidence of vulnerabilities. DAST finds issues that SAST cannot, such as authentication flaws, server misconfigurations, and runtime injection vulnerabilities.

| Tool | Type | Best For | Cost |
|---|---|---|---|
| OWASP ZAP | Open-source | CI/CD automation, API scanning, baseline scans | Free |
| Burp Suite | Commercial | Manual penetration testing, advanced crawling, Burp extensions | Paid (Professional and Enterprise editions) |
| Nuclei | Open-source | Template-based vulnerability scanning with a large community template library | Free |

### Key Considerations for DAST

- **Authenticated scanning** — Ensure the tool can handle your authentication mechanism (OAuth, JWT, SAML, session cookies) to test authenticated surfaces.
- **API support** — For API-heavy applications, verify the tool can import and scan OpenAPI/Swagger specifications, GraphQL schemas, or gRPC definitions.
- **Scan duration** — Full DAST scans can take hours; use baseline scans in CI and full scans on a scheduled basis.

## SCA (Software Composition Analysis)

SCA tools identify known vulnerabilities (CVEs) in open-source dependencies, generate Software Bills of Materials (SBOMs), and assess license compliance risks. Given that modern applications are 70-90% open-source code, SCA is a critical layer of defense.

| Tool | Languages | SBOM Generation | Cost |
|---|---|---|---|
| Snyk | All major languages and package managers | Yes (CycloneDX, SPDX) | Freemium (free tier + paid plans) |
| Dependabot | GitHub-supported languages and ecosystems | No | Free (built into GitHub) |
| Trivy | All major languages + container images + IaC | Yes (CycloneDX, SPDX) | Free (open-source, Aqua Security) |
| Grype + Syft | All major languages and container images | Yes (Syft generates SBOMs, Grype scans them) | Free (open-source, Anchore) |

### Key Considerations for SCA

- **Reachability analysis** — Advanced SCA tools can determine whether a vulnerable function in a dependency is actually called by your code, dramatically reducing noise.
- **License compliance** — SCA tools can flag dependencies with licenses incompatible with your distribution model (e.g., GPL in a proprietary product).
- **Automated remediation** — Tools like Dependabot and Snyk can automatically open pull requests to upgrade vulnerable dependencies.

## Container Security

Container security covers the entire container lifecycle: building secure images, scanning for vulnerabilities, and monitoring runtime behavior for threats.

| Tool | Capability | Type |
|---|---|---|
| Trivy | Image vulnerability scanning, SBOM generation, misconfiguration detection | Open-source (Aqua Security) |
| Falco | Runtime threat detection using system call monitoring and eBPF | CNCF project (open-source) |
| Sysdig | Full lifecycle container security (scanning, runtime, compliance, forensics) | Commercial |
| Aqua | Full lifecycle container and cloud-native security platform | Commercial |

### Key Considerations for Container Security

- **Base image selection** — Use minimal, hardened base images (distroless, Alpine, Chainguard) to reduce the attack surface.
- **Image signing** — Sign container images with Cosign or Notary to ensure supply chain integrity.
- **Runtime monitoring** — Static scanning alone is insufficient; runtime tools like Falco detect anomalous behavior (unexpected shell execution, network connections, file system modifications) that image scanning cannot.

## Secrets Detection

Secrets detection tools scan code, commit history, and CI/CD artifacts for accidentally committed credentials such as API keys, passwords, tokens, and private keys.

| Tool | Approach | Verification | Speed |
|---|---|---|---|
| TruffleHog | Entropy analysis + pattern matching with active verification of discovered secrets | Yes (actively verifies if secrets are live) | Slower (due to verification) |
| GitLeaks | Pattern and regex-based detection with customizable rules | No | Fast |
| detect-secrets | Pattern-based detection with a baseline file to track known/approved secrets | No | Fast |

### Key Considerations for Secrets Detection

- **Pre-commit hooks** — Run secrets detection as a pre-commit hook to prevent secrets from ever entering version control.
- **Full history scanning** — Regularly scan the entire Git history, not just the latest commit, since secrets committed in the past remain exploitable even after deletion from the current branch.
- **Verification** — TruffleHog's active verification feature confirms whether detected secrets are still valid, helping prioritize remediation.

## IaC Security

Infrastructure-as-code (IaC) security tools analyze Terraform, CloudFormation, Kubernetes manifests, Dockerfiles, and other IaC templates for security misconfigurations before they are deployed.

| Tool | Targets | Type |
|---|---|---|
| Checkov | Terraform, CloudFormation, Kubernetes, Helm, Docker, Ansible, ARM | Open-source (Prisma Cloud / Palo Alto) |
| Trivy config | Terraform, Dockerfile, Kubernetes, CloudFormation, Helm | Open-source (Aqua Security) |
| Terrascan | Terraform, Kubernetes, Helm, CloudFormation, Docker, Azure ARM | Open-source (Tenable) |
| KICS | Terraform, CloudFormation, Kubernetes, Docker, Ansible, OpenAPI, Pulumi | Open-source (Checkmarx) |

### Key Considerations for IaC Security

- **Policy-as-code** — Write custom policies (using Rego, Python, or YAML) to enforce organization-specific standards beyond the built-in checks.
- **Drift detection** — Combine IaC scanning with drift detection to ensure deployed infrastructure matches the scanned templates.
- **Terraform plan scanning** — Scan `terraform plan` output (not just HCL files) to catch issues that only manifest in the plan, such as overly permissive security group rules computed from variables.

## CI/CD Integration

Security testing tools should be integrated into every stage of the CI/CD pipeline. The following diagram illustrates where each tool type runs:

```
+----------+     +----------+     +-----------+     +-------------------+
|  Commit  | --> |  Build   | --> |  Staging  | --> |    Production     |
+----------+     +----------+     +-----------+     +-------------------+
|                |                |                  |
| - SAST         | - SCA          | - DAST           | - Runtime monitoring
| - Secrets      | - Container    | - Authenticated  |   (Falco, Sysdig)
|   detection    |   image scan   |   scanning       | - Continuous SCA
| - IaC scanning | - SBOM         | - API fuzzing    | - Log analysis
| - Pre-commit   |   generation   |                  |
|   hooks        |                |                  |
```

**Shift left, but don't stop there.** Run fast, lightweight checks (SAST, secrets, IaC) at commit time for rapid developer feedback. Run heavier checks (SCA, container scanning) at build time. Run DAST against staging. Continue monitoring in production with runtime security tools and continuous vulnerability scanning.

## Best Practices

- **Layer multiple testing approaches** — no single tool catches everything; combine SAST, DAST, SCA, container scanning, secrets detection, and IaC scanning for comprehensive coverage.
- **Integrate security testing into CI/CD as quality gates** — fail builds on critical and high-severity findings to prevent vulnerable code from reaching production.
- **Tune tools aggressively to reduce false positives** — a noisy tool is an ignored tool; invest time in suppressing false positives and writing custom rules tuned to your codebase.
- **Enable incremental scanning** for SAST tools in pull requests so that developers receive fast feedback on only the code they changed, reserving full scans for nightly or weekly runs.
- **Generate and store SBOMs** for every release using CycloneDX or SPDX format; SBOMs enable rapid impact assessment when new vulnerabilities are disclosed in dependencies.
- **Run secrets detection as a pre-commit hook** and scan the full Git history periodically; secrets committed even briefly remain in Git history and must be rotated immediately upon detection.
- **Keep security tool rulesets and vulnerability databases up to date** — outdated rules miss new vulnerability patterns; automate rule updates as part of your tool maintenance.
- **Track security testing metrics** (findings by severity, mean time to remediate, false positive rate, scan coverage) and report them to engineering leadership to drive continuous improvement.
