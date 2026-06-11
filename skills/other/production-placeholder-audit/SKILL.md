---
name: production-placeholder-audit
user-invocable: false
description: |-
  Use when finding mocks, stubs, fake paths, or placeholders leaking into production code.
  Triggers:
practices:
- design-by-contract
- testability
hexagonal_role: supporting
consumes:
- source-code
- build-config
- test-suite
produces:
- mock-code-findings
context_rel:
- kind: supplier-to
  with: review
- kind: supplier-to
  with: security
skill_api_version: 1
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: execution
  external_dependencies: [rg, git]
  stability: stable
  user_invocable: false
  platforms: [any]
output_contract: "Actionable finding report with severity, file:line, exact evidence, production reachability, user/system impact, and remediation for each confirmed mock/stub/fake/test-leak/placeholder."
---

# production-placeholder-audit

Find implementation artifacts that make production behavior less real than it looks: mocks, stubs, fake paths, test-only modules, inert adapters, placeholder branches, dummy credentials, and comments that imply future behavior while current code silently succeeds.

## Critical Constraints

- **Evidence first.** Every finding needs a concrete file:line, quoted or summarized signal, and a reason it is reachable or relevant. Do not report vibes.
- **Production reachability matters.** Test fixtures under test-only paths are not findings unless they are imported by production code, packaged in a runtime artifact, selected by config, or exposed through a public path.
- **Do not count harmless TODOs alone.** A placeholder is actionable only when behavior is missing, fake, misleading, externally visible, or able to mask failure.
- **Separate suspicious from confirmed.** Keep weak signals in a "needs follow-up" section instead of presenting them as defects.
- **Stay read-only by default.** This skill audits and reports; it does not rewrite code or delete test helpers.

## Workflow / Methodology

### Phase 1: Map the production surface

Identify where production code enters and what gets packaged:

```bash
rg -n --hidden -S "main\\(|entry|router|routes|handler|server|export|module.exports|pub fn main|func main|package|deploy|build|dist|release" .
rg -n --hidden -S "include|exclude|files|testMatch|pytest|go test|cargo test|jest|vitest|mocha|webpack|vite|rollup|tsconfig|package.json|pyproject|Cargo.toml|go.mod" .
```

Record the directories that are production by default (`src/`, `app/`, `cmd/`, `lib/`, `internal/`, deployment configs) and the directories that are test-only by default (`test/`, `tests/`, `fixtures/`, `__mocks__/`, `spec/`). Treat generated and vendored code as out of scope unless it is explicitly shipped or edited in the project.

### Phase 2: Scan for high-signal terms

Start broad, then narrow:

```bash
rg -n --hidden -S "\\b(mock|stub|fake|dummy|fixture|placeholder|todo|hack|temporary|not implemented|no-op|noop|sample|example)\\b" .
rg -n --hidden -S "(__mocks__|test-only|testonly|Mock[A-Z]|Fake[A-Z]|Stub[A-Z]|Dummy[A-Z]|Fixture[A-Z])" .
rg -n --hidden -S "(localhost|127\\.0\\.0\\.1|example\\.com|/tmp/|/dev/null|changeme|password123|api[_-]?key|token)" .
rg -n --hidden -S "(throw new Error\\(['\\\"]TODO|panic!\\(['\\\"]TODO|panic\\(['\\\"]TODO|return null|return nil|return None|return \\{\\}|return \\[\\])" .
```

Then inspect import sites and packaging configs for each suspicious symbol or file:

```bash
rg -n --hidden -S "SuspiciousName|suspicious/path|__mocks__|fixtures?" .
git ls-files
```

### Phase 3: Classify the evidence

Use these finding classes:

| Class | Confirming evidence |
|---|---|
| Production mock/stub | Mock/fake/stub implementation imported, constructed, or selected by production entrypoints |
| Test-only leak | Test helper, fixture, or `__mocks__` module reachable from non-test code or shipped package config |
| Fake path/config | Hard-coded fake URL, local path, dummy token, or sample endpoint in runtime config |
| Evidence-free placeholder | Code claims success, returns empty/default data, or suppresses errors without a real implementation |
| Bypass branch | Env flag, build mode, or feature toggle swaps real behavior for fake behavior in production-capable paths |
| Misleading artifact | Docs, generated output, or API response advertises behavior that code does not implement |

### Phase 4: Prove or dismiss each candidate

For each candidate, answer:

1. Is it under production, test, generated, vendored, or deployment-only scope?
2. What imports, config, route, command, package manifest, or build rule makes it reachable?
3. What user-visible or system-visible behavior is fake, missing, or misleading?
4. What minimal change would remove the risk: delete, gate, rename, move to tests, fail closed, wire real implementation, or document as intentional?

Dismiss candidates that are test-local, explicitly excluded from packages, behind a safe non-production gate, or clearly documented as an intentional simulation.

## Output Specification

Return a markdown report:

```markdown
## Findings

| Severity | Class | Location | Evidence | Reachability | Impact | Recommended fix |
|---|---|---|---|---|---|---|
| High | Production mock/stub | path/file.ext:42 | FakeClient returned for default config | imported by app entrypoint | real API calls never happen | inject real client by default; keep fake in tests |

## Needs Follow-up

- path/file.ext:10: suspicious placeholder, but production reachability is not proven.

## Excluded

- tests/fixtures/user.json: fixture is test-local and not packaged.
```

Severity guide:

- **Critical:** fake behavior can corrupt data, bypass security, report false success, or ship to customers by default.
- **High:** production path uses mock/stub/fake behavior or silently drops required work.
- **Medium:** production-capable config or branch can select fake behavior without strong guardrails.
- **Low:** misleading placeholder with limited blast radius and clear remediation.

## Quality Rubric

- [ ] Each finding has `file:line`, class, evidence, reachability, impact, and fix.
- [ ] Findings distinguish confirmed defects from weak signals.
- [ ] Test-only code is not reported unless production reachability is proven.
- [ ] Placeholder findings describe current behavior, not just a TODO string.
- [ ] Fake paths/config findings identify where the value is loaded or shipped.
- [ ] The report includes explicit exclusions for obvious false positives.
- [ ] Recommendations are actionable and scoped to the smallest safe change.

## Examples

Confirmed finding:

```text
High | Test-only leak | src/client.ts:18 | imports "../tests/fixtures/users" | src/client.ts is exported by package.json "main" | production bundle returns fixture users | move fixture import behind test factory and fail closed when real source is absent
```

Not a finding:

```text
tests/payment.mock.ts is under tests/, only imported by *.test.ts, and excluded from package files.
```

## Troubleshooting

| Problem | Cause | Response |
|---|---|---|
| Too many TODO hits | Text search is too broad | Only keep TODOs tied to runtime behavior, false success, or missing implementation |
| Unsure if code ships | Packaging/build config unclear | Mark as needs follow-up and name the missing proof |
| Mock is intentional | It is gated to tests or local dev | Exclude it and cite the gate |
| Fake endpoint appears in docs | Docs may be examples | Report only if docs drive generated config or production defaults |
| Empty return is idiomatic | Some APIs use empty collections safely | Report only if it masks required behavior or contradicts contract |

## See Also / References

- `review` skill for broader PR/code review.
- `security` skill when fake credentials, bypasses, or auth placeholders affect access control.
- `test` skill when findings need regression tests.
- `refactor` or `implement` skills for follow-up fixes after findings are accepted.
