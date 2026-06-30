---
name: cicd-supply-chain
description: Use when attacking or auditing a CI/CD pipeline or software supply chain — pwn requests, poisoned pipeline execution, compromised/mutable-tag actions, dependency confusion, registry worms, runner backdoors, OIDC trust abuse, SLSA/provenance
metadata:
  type: offensive
  phase: weaponize-delivery-exploit
  tools: gato-x, zizmor, octoscan, poutine, raven, trufflehog, gitleaks, cosign, slsa-verifier, gh, glab, syft
  mitre: [T1195.001, T1195.002, T1199, T1525, T1556, T1078.004, T1648]
kill_chain:
  phase: [weaponize, delivery, exploit, actions]
  step: [2, 3, 4, 7]
  attck_tactics: [TA0001, TA0003, TA0004, TA0006, TA0008]
  attck_techniques: [T1195, T1195.001, T1195.002, T1199, T1525, T1556, T1078.004, T1648, T1552.004, T1059]
depends_on: [recon-osint, vulnerability-analysis]
feeds_into: [cloud-security, red-team-ops, initial-access]
inputs: [target_repos, ci_config, registry_namespaces, oidc_trust_policies]
outputs: [pipeline_finding, exfiltrated_secrets, malicious_artifact, attack_path, provenance_gap]
references:
  - references/pipeline-poisoning.md
  - references/action-dependency-compromise.md
  - references/package-registry-attacks.md
  - references/runner-attacks.md
  - references/secrets-oidc-abuse.md
  - references/build-integrity-defense.md
scripts:
  - scripts/workflow_auditor.py
  - scripts/dependency_confusion.py
  - scripts/oidc_trust_auditor.py
  - scripts/malicious_action_scanner.py
  - scripts/runner_recon.sh
  - scripts/provenance_verify.sh
---

# CI/CD Pipeline Poisoning & Supply-Chain Attacks

## When to Activate

- Auditing or attacking GitHub Actions / GitLab CI / Jenkins pipelines for code execution
- Hunting `pull_request_target` / `workflow_run` "pwn requests" and Poisoned Pipeline Execution (PPE)
- Assessing compromised third-party Actions, mutable version tags, and Actions cache poisoning
- Dependency confusion, typo/slopsquatting, and malicious package/install-hook payloads
- Self-hosted / non-ephemeral runner abuse and runner backdoors
- CI secret exfiltration and OIDC cloud-role (AWS/GCP/Azure) trust-policy abuse
- Validating SLSA build provenance and signing gates (defense / blue-team validation)

## Technique Map

| Technique | ATT&CK | CWE | Reference | Script |
|-----------|--------|-----|-----------|--------|
| Pwn request (`pull_request_target` checkout of fork head) | T1195.001 | CWE-269 | references/pipeline-poisoning.md | scripts/workflow_auditor.py |
| Script injection (`${{ github.event.* }}` into `run:`) | T1059 | CWE-94 | references/pipeline-poisoning.md | scripts/workflow_auditor.py |
| Direct / Indirect PPE (workflow or build-file modification) | T1195.001 | CWE-913 | references/pipeline-poisoning.md | scripts/workflow_auditor.py |
| GitLab `.gitlab-ci.yml` poisoning / pipeline-as-user (CVE-2024-6678) | T1648 | CWE-863 | references/pipeline-poisoning.md | scripts/workflow_auditor.py |
| Compromised Action via mutable tag (CVE-2025-30066 tj-actions) | T1195.001 | CWE-494 | references/action-dependency-compromise.md | scripts/malicious_action_scanner.py |
| Transitive Action compromise (CVE-2025-30154 reviewdog) | T1195.001 | CWE-1357 | references/action-dependency-compromise.md | scripts/malicious_action_scanner.py |
| Actions cache poisoning (cross-workflow escalation) | T1525 | CWE-349 | references/action-dependency-compromise.md | scripts/malicious_action_scanner.py |
| Dependency confusion (internal name on public registry) | T1195.002 | CWE-427 | references/package-registry-attacks.md | scripts/dependency_confusion.py |
| Typo / slopsquatting + malicious install hook | T1195.002 | CWE-829 | references/package-registry-attacks.md | scripts/dependency_confusion.py |
| Self-replicating registry worm (Shai-Hulud npm) | T1195.002 | CWE-829 | references/package-registry-attacks.md | scripts/malicious_action_scanner.py |
| Self-hosted / non-ephemeral runner abuse & backdoor | T1199 | CWE-668 | references/runner-attacks.md | scripts/runner_recon.sh |
| Jenkins Script Console RCE (`/script`, CVE-2024-23897) | T1648 | CWE-306 | references/runner-attacks.md | scripts/runner_recon.sh |
| CI secret exfiltration (`toJSON(secrets)`, GhostAction) | T1552.004 | CWE-522 | references/secrets-oidc-abuse.md | scripts/oidc_trust_auditor.py |
| OIDC trust-policy abuse (missing/`*` `sub`, wrong org wildcard) | T1078.004 | CWE-1390 | references/secrets-oidc-abuse.md | scripts/oidc_trust_auditor.py |
| Build provenance / signing gate validation (defense) | T1195 | CWE-347 | references/build-integrity-defense.md | scripts/provenance_verify.sh |

## Quick Start

```bash
# 0. Recon: enumerate workflows, triggers, used actions across an org (read-only token)
gh repo list ORG --limit 1000 --json nameWithOwner -q '.[].nameWithOwner' > repos.txt
python3 scripts/workflow_auditor.py --repos repos.txt --token "$GH_TOKEN" --out findings.json

# 1. Static audit any cloned repo for pwn-requests + injection sinks (offline, no token)
git clone https://github.com/ORG/REPO && python3 scripts/workflow_auditor.py --path REPO

# 2. Flag risky/mutable third-party Action refs (unpinned tags = supply-chain exposure)
python3 scripts/malicious_action_scanner.py --path REPO --check-pins --check-known-bad

# 3. Dependency confusion: find internal names not registered on public registries
python3 scripts/dependency_confusion.py --manifest REPO/package.json --registry npm
python3 scripts/dependency_confusion.py --manifest REPO/requirements.txt --registry pypi

# 4. OIDC abuse: audit AWS IAM trust policies tied to GitHub's OIDC provider
python3 scripts/oidc_trust_auditor.py --provider github --cloud aws --profile target

# 5. Runner recon (run ON a compromised self-hosted runner during an engagement)
bash scripts/runner_recon.sh

# 6. Defensive validation: verify SLSA provenance + cosign signature before promote
bash scripts/provenance_verify.sh --image ghcr.io/org/app:tag --repo org/app
```

Recommended OSS tooling: `gato-x` (offensive GHA enumeration/PPE), `zizmor`/`octoscan`/`poutine`/`raven`
(static workflow analysis), `step-security/harden-runner` (egress control), `cosign`+`slsa-verifier` (gates).

## OPSEC & Detection (summary)

| Technique | Telemetry / IOC | Detection (Sigma/EDR) | OPSEC note |
|-----------|-----------------|------------------------|------------|
| Pwn request / PPE | Fork PR triggering privileged run; new `.github/workflows/*` in PR; outbound to non-allowlisted host | GH audit log `workflows`; Sigma on runner egress to new domains; zizmor in CI | Payload runs in build log; public-repo logs are world-readable — assume detection |
| Compromised Action / mutable tag | Action ref resolves to new SHA; tag force-push event; base64 in action source | Diff resolved SHA vs lockfile; alert on tag re-point in audit log | Tag re-point is logged org-side; SHA-pin victims are immune |
| Cache poisoning | Cache key written by read-only/low-priv job, restored by release job | Monitor `actions/cache` save/restore key ownership; provenance mismatch | Survives across workflows; harder to attribute than direct edit |
| Dependency confusion | Install-time outbound from build host; package version anomaly (very high ver) | EDR proc-tree `npm/pip` -> `curl/node -e`; registry telemetry | Higher public version wins resolver; noisy if scoped registries enforced |
| Registry worm (Shai-Hulud) | `bundle.js` postinstall; `trufflehog filesystem /`; public `Shai-Hulud` repo; `shai-hulud-workflow.yml` | EDR: npm child spawns trufflehog/git push; Sigma on workflow file creation | Self-propagating = loud and fast; burns the maintainer token |
| Runner backdoor | Rogue runner registration; persistent proc on host; outbound only to github.com | Runner-host EDR; GH audit `self_hosted_runner` events; one-job-per-runner | Traffic blends with github.com; non-ephemeral = persistence |
| Secret exfil / `toJSON(secrets)` | `${{ toJSON(secrets) }}` in run step; POST of base64 to webhook | Static scan for `toJSON(secrets)`; egress allowlist | GitHub masks `***` in logs — encoding evades the mask |
| OIDC trust abuse | `AssumeRoleWithWebIdentity`; CloudTrail `userName` = `repo:org/repo:ref` | CloudTrail filter on federated principals; IAM Access Analyzer external findings | Short-lived creds, attributed to repo in logs; AWS blocks new bad policies (Jun 2025) |

## Deep Dives

- references/pipeline-poisoning.md — Pwn requests, PPE (direct/indirect), script injection, GitLab/Jenkins pipeline poisoning, with vulnerable+fixed YAML and a working exploit PR payload.
- references/action-dependency-compromise.md — Third-party Action compromise, mutable git tags, the tj-actions (CVE-2025-30066) / reviewdog (CVE-2025-30154) chain, and Actions cache poisoning; SHA-pinning detection.
- references/package-registry-attacks.md — Dependency confusion, typo/slopsquatting, malicious install hooks, and the Shai-Hulud self-replicating npm worm with concrete IOCs.
- references/runner-attacks.md — Self-hosted / non-ephemeral runner abuse, JIT/ephemeral hardening, runner backdoors, and Jenkins Script Console RCE.
- references/secrets-oidc-abuse.md — CI secret enumeration/exfiltration (GhostAction), `toJSON(secrets)`, and AWS/GCP/Azure OIDC trust-policy misconfigurations.
- references/build-integrity-defense.md — SLSA provenance, in-toto attestations, Sigstore/cosign keyless signing, slsa-verifier gates, and admission-control enforcement (the defensive counterweight).
