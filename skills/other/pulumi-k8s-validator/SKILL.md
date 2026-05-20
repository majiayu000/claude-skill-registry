---
name: pulumi-k8s-validator
type: standard
depth: base
description: >-
  Validates Pulumi Kubernetes TypeScript infrastructure via type checks, preview diffs, security audits, and production readiness. Use when auditing existing .ts files with @pulumi/kubernetes resources. Does NOT generate new resources.
---

# [H1][PULUMI-K8S-VALIDATOR]
>**Dictum:** *Validation is read-only analysis -- never modify files.*

<br>

Analyze infrastructure code, propose improvements. Does NOT modify files.

**Provider:** current stable `@pulumi/kubernetes` | **K8s:** 1.32-1.35 | **Canonical:** `infrastructure/src/deploy.ts` (207 LOC)

| Use this skill                         | Use OTHER skill                                |
| -------------------------------------- | ---------------------------------------------- |
| Validate/audit Pulumi K8s code         | `pulumi-k8s-generator`: Create new resources   |
| Type-check resource definitions        | `k8s-debug`: Debug deployed resources          |
| Security + production readiness review | `dockerfile-validator`: Container image builds |

**Tasks:**
1. Run TypeScript type check: `pnpm exec nx run infrastructure:typecheck`
2. Run `pulumi preview --diff` (flags: `--expect-no-changes`, `--target <urn>`, `--refresh`, `--stack <name>`)
3. Read infrastructure source; check security posture against `references/validation_checklist.md`
4. Read infrastructure source; check production readiness against `references/validation_checklist.md`
5. Generate report per format below

---
## [1][STAGE_DETAILS]
>**Dictum:** *Each stage catches a distinct class of defect.*

<br>

**Guidance:**
- `TypeScript` - Record each error with file, line, and category. Common: wrong field name, missing required field, type mismatch, missing module.
- `Preview` - Interpret diff symbols (`+` create, `-` delete, `~` update, `+-` replace, `-+` replace with downtime). Skip on connection/stack errors; continue to Stage 3.
- `Security` - deploy.ts findings: `_Ops.secret()` wraps all sensitive values (PASS), no pod security context on compute (WARN), no NetworkPolicy (WARN).
- `Readiness` - deploy.ts findings: all probes configured (PASS), resource limits set (PASS), no PDB (WARN), no anti-affinity (WARN), `:latest` on observe images (WARN), no topology spread (INFO).

**Best-Practices:**
- Stages 1 + 3 run in parallel (compiler + source analysis). Stage 2 after Stage 1 passes. Stage 5 after all.
- Never modify files, offer to apply fixes, or prompt user for changes.
- Always load both `references/` files when issues are found.

---
## [2][REPORT_FORMAT]
>**Dictum:** *Structured output enables actionable triage.*

<br>

**Summary table:**

| Stage         | Status | Issues                                  |
| ------------- | ------ | --------------------------------------- |
| 1. TypeScript | [PASS] | 0 errors                                |
| 2. Preview    | [PASS] | 3 resources planned                     |
| 3. Security   | [WARN] | Missing securityContext on 2 containers |
| 4. Readiness  | [WARN] | Missing probes on 1 deployment          |

**Severity classification:**

| Severity  | Checks                                                                                                                        |
| --------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `[ERROR]` | TS errors, preview failures, running as root, privileged, host namespace, missing requests, missing probes, secrets in config |
| `[WARN]`  | Missing security context, no limits, no PDB, no NetworkPolicy, `:latest` image, no anti-affinity, no ServiceAccount           |
| `[INFO]`  | Missing startup probe, topology spread, HPA tuning, Gateway API migration, ValidatingAdmissionPolicy                          |

**Per-issue detail:** file:line, before/after TypeScript, reason, complexity `[Simple]`/`[Medium]`/`[Complex]`.

**Final summary:** project, stack, status, error/warn/info counts, proposed change count, next steps.
