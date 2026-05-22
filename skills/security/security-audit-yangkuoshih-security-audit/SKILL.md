---
name: security-audit
description: >
  Scans source code files for hardcoded secrets, leaked credentials, and
  security vulnerability patterns, then produces a severity-classified audit
  report (Markdown, SARIF, or JSON). Use this skill — not ad-hoc grep — when
  the user wants to: scan for hardcoded secrets or API keys, do a security
  audit, find leaked credentials or tokens, check whether sensitive values were
  committed, run an incremental scan of files changed since a branch, generate
  a SARIF file for GitHub Code Scanning, or get a report of findings grouped by
  Critical / High / Medium / Low. Do NOT use for: fixing individual bugs the
  user has already identified, writing CI/CD pipeline config, checking package
  dependency CVEs (use a dependency scanner for that), or general code review
  without a security focus.
license: Apache-2.0
compatibility: Requires bash and grep for primary scanning, or Python 3 as fallback. Works without shell access in degraded mode.
metadata:
  author: Kuoshih Yang
  version: "0.1.0"
  repository: https://github.com/YangKuoshih/security-audit
---

# Security Audit

Scan a codebase for hardcoded secrets, credentials, API keys, and common security vulnerabilities. Produce a severity-classified report with remediation guidance.

## Path Resolution

Throughout this skill, `${CLAUDE_PLUGIN_ROOT}` refers to the directory where this plugin is installed. Claude Code sets this automatically when loading a plugin. If the variable is not available in your environment, resolve it as the parent directory of the `skills/` folder containing this file (i.e., the repository root of the security-audit plugin).

## Secret Data Safety

**This skill MUST NOT exfiltrate discovered secrets.** All findings are for the user's eyes only — to help them remediate issues in their own codebase.

Rules that apply to ALL phases:

1. **Never read files known or suspected to contain secrets into LLM context.** When Phase 2 flags a file, do NOT use the Read tool to open that file. Work only from the redacted JSONL output.
2. **Never echo, log, or output raw secret values.** All matches in scanner output are already redacted. If you must reference a finding, use the redacted form only.
3. **Never send findings or file contents to external services** — no web fetches, no API calls, no MCP tool calls that transmit finding data outside the local machine.
4. **The report is a local file.** Do not offer to upload, share, or transmit the report. The user decides what to do with it.
5. **No-shell fallback caution:** If you must read source files directly (no shell access), do NOT read files that match dangerous file patterns (`.tfstate`, `.pem`, `.key`, `.p12`, `.pfx`, `.jks`, `credentials.json`, `service-account*.json`). For other files, scan line by line and discard each line's content from your response after checking it — never quote raw secret values in your output.

## Workflow

Execute the following four phases in order. Adapt based on environment capabilities detected in Phase 1.

### Phase 1: Setup

Run a **single** bash command to detect all environment capabilities at once:

```bash
echo "=== ENV ===" && echo "shell-ok" && (git --version 2>/dev/null || echo "git-missing") && (python3 --version 2>/dev/null || python --version 2>/dev/null || echo "python-missing") && echo "=== CONFIG ===" && (cat .security-audit.yml 2>/dev/null || echo "no-config")
```

Parse the output to determine: shell access, git availability, Python command (`python3` or `python`), and config. If `.security-audit.yml` is absent, use defaults:
- Scan mode: `full`
- Excluded dirs: `node_modules`, `venv`, `.git`, `dist`, `build`, `__pycache__`, `.next`, `vendor`, `target`
- Excluded files: `*.min.js`, `*.lock`, `*.map`
- Severity minimum: all
- Output format: markdown

Determine scan mode:
- **Full:** scan all files
- **Incremental:** use `git diff --name-only <base_branch>...HEAD` to get changed files
- **Paths:** scan only specified directories

### Phase 2: Pattern Scanning

**If shell access is available (primary path):**

Run the Python scanner (preferred — faster, includes entropy detection). Combine scanner + tech stack detection into a **single** bash call to minimize tool call overhead:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/security-audit/scripts/scan-secrets.py" --target "<target_dir>" --patterns "${CLAUDE_PLUGIN_ROOT}/skills/security-audit/scripts/patterns.dat" --output "<output_file>" && echo "=== TECHSTACK ===" && ls -1 package.json requirements.txt pyproject.toml go.mod pom.xml build.gradle Gemfile Dockerfile docker-compose.yml 2>/dev/null; find . -maxdepth 2 -name '*.tf' -print -quit 2>/dev/null
```

Use `python3` or `python` depending on what is available. For incremental mode, add `--base-branch <branch>`.

If Python is not available, fall back to the bash scanner:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/security-audit/scripts/scan-secrets.sh" "<target_dir>" "${CLAUDE_PLUGIN_ROOT}/skills/security-audit/scripts/patterns.dat" "<output_file>" && echo "=== TECHSTACK ===" && ls -1 package.json requirements.txt pyproject.toml go.mod pom.xml build.gradle Gemfile Dockerfile docker-compose.yml 2>/dev/null; find . -maxdepth 2 -name '*.tf' -print -quit 2>/dev/null
```

For incremental mode, add `--base-branch <branch>`.

**If no shell access (fallback path):**

Read files directly and apply pattern knowledge from `references/secret-patterns.md` and `references/vulnerability-patterns.md`. **Important: follow Secret Data Safety rules** — skip files matching dangerous file patterns entirely (`.tfstate`, `.pem`, `.key`, `.p12`, `.pfx`, `.jks`, `credentials.json`, `service-account*.json`) and flag them as file-level findings without reading their contents. For other files, scan for:
- Known secret formats (AWS keys, GitHub tokens, private keys, etc.)
- Vulnerability patterns (SQL injection sinks, XSS vectors, weak crypto)
- High-entropy strings that may be secrets

When a secret is found, **redact it immediately** — never include the raw value in your output. Output findings in the same format: file, line number, redacted match, pattern name, base severity.

### Phase 2b: Dangerous File Type Scan

This phase runs automatically as part of the scanner scripts (both bash and Python). It detects files that should never be committed to git, regardless of their contents.

**How it works:** Uses `git ls-files --cached` to check only tracked files. Gitignored files are NOT flagged. Results are appended to the same output file as Phase 2 findings, using `line: 0` to indicate file-level findings.

**Detected file types:** Terraform state (`.tfstate`), private keys (`.pem`, `.key`, `.p12`, `.pfx`), Java keystores (`.jks`), cloud credentials (`credentials.json`, `service-account*.json`), Terraform cache (`.terraform/`), database files (`.sqlite`, `.db`), Terraform output files, and files with "secret" in the name.

See `references/secret-patterns.md` § Dangerous File Types for the complete list with pattern IDs and descriptions.

**If no shell access (fallback path):**

Use `git ls-files --cached` knowledge to ask the user about tracked files matching dangerous patterns. Flag any matches with `line: 0` and `match: "(entire file)"` in findings.

### Phase 3: LLM Analysis

**Performance guidelines for this phase:**
- Do NOT read `references/secret-patterns.md`, `references/vulnerability-patterns.md`, or `references/severity-guide.md` unless you encounter a finding you cannot classify from the information in this file. The key rules are summarized below.
- Do NOT read source files for secret findings — work from scanner output only.
- You MAY read ~10 lines of source for **vulnerability** findings to assess exploitability.
- Combine all Phase 3 reasoning into a single analysis pass — do not iterate findings one at a time with separate tool calls.

Read the **redacted** findings JSONL output file **once** (single Read tool call). Perform all analysis below from that single read — do not re-read the file. Follow Secret Data Safety rules — work from scanner output only, not original source files, for secret findings.

#### 3a. Tech Stack Detection

Tech stack detection was already run as part of the Phase 2 scanner command (after `=== TECHSTACK ===` in the output). Parse those results — do NOT run a separate command. Map results to remediation context:
- `package.json` → Node.js (`process.env`, AWS Secrets Manager, GitHub Secrets)
- `requirements.txt` / `pyproject.toml` → Python (`os.environ`, python-dotenv, Vault)
- `go.mod` → Go (`os.Getenv`, Vault, cloud-native secrets)
- `pom.xml` / `build.gradle` → Java (Spring Vault, AWS Secrets Manager)
- `Gemfile` → Ruby (`ENV[]`, dotenv, Rails credentials)
- `*.tf` → Terraform (remote state, variable files, Vault provider)
- `Dockerfile` / `docker-compose.yml` → containerized (Docker secrets, not build args)

Use this context to tailor all remediation advice to the actual stack.

#### 3b. Cross-Finding Correlation

Group related findings before classifying:
- **Same credential, multiple files**: If the same pattern ID matches in multiple files with identical redacted prefixes, consolidate into a single finding with all locations listed. Severity = max of all locations.
- **Related infrastructure**: If Terraform state + Terraform output + cloud credentials are all found, note these form a compound exposure (attacker gets infrastructure map + credentials).
- **Cascading access**: If a cloud provider key + a database connection string are both found, note the blast radius (cloud key may grant broader access than the DB string alone).

#### 3c. Finding Triage

Process ALL findings in a **single reasoning pass** (not one tool call per finding). For each finding (or correlated group):

1. **Filter false positives** using redacted match text and file path context:
   - Discard matches in `test/`, `tests/`, `example/`, `examples/`, `docs/`, `fixtures/` paths with placeholder values
   - For dangerous file-type findings (`line: 0`), check if file is in example/docs/test paths for potential downgrade
   - Framework-specific: Django ORM `.filter()` is safe (parameterized); React JSX `{expr}` auto-escapes; Rails `where(key: val)` is safe; `subprocess.run([list])` without `shell=True` is safe

2. **Classify severity** — start with base severity from scanner, then adjust:
   - **Downgrade one tier** if: test/example/docs path, placeholder value, `.env.development`/`.env.local`/`.env.test`
   - **Upgrade one tier** if: production path (`deploy/`, `infra/`, `.github/workflows/`), vendor-specific prefix match, production URL context
   - Never downgrade below Low; never upgrade above Critical

3. **Assess exploitability** (vuln findings only, batch reads if needed):
   - For vuln findings, you MAY read surrounding code (~10 lines) to assess user input reachability
   - Do NOT read files flagged for secret findings
   - Rate: Exploitable / Likely Exploitable / Needs Investigation / Likely False Positive

4. **Assign confidence**: High (vendor-specific prefix like `AKIA`, `ghp_`, `sk_live_`, or unambiguous file type), Medium (generic pattern needing context), Low (entropy/heuristic match)

#### 3d. Executive Summary

Before the detailed findings, produce a prioritized summary:

1. **Top 3 actions** — the three most impactful things to fix first, with one sentence each explaining why
2. **Blast radius assessment** — what an attacker could access if the worst findings are exploited
3. **Positive observations** — note good security practices observed (e.g., "secrets are properly gitignored", "no production credentials found")

#### 3e. Augmented Findings

After triage, produce an **augmented findings list** by adding fields to each finding:
- `"confidence"`: `"High"`, `"Medium"`, or `"Low"`
- `"context"`: one sentence explaining the severity rating and confidence — e.g., *"Live Stripe key in a production deploy script; no placeholder markers present."*
- `"commit"` (optional, skip for speed unless user requests it): git commit hash and author

**Commit attribution** is expensive and optional. Only run it if the user explicitly requests blame/commit info. When enabled, batch all lookups into a **single** command instead of one per finding:

```bash
# Batch: extract blame for all finding locations at once
while IFS=: read -r file line; do
  git log -1 --format="%h %ae %as" -L "${line},${line}:${file}" 2>/dev/null | head -1
done <<'LOCATIONS'
path/to/file1.py:42
path/to/file2.js:17
LOCATIONS
```

This augmented list is what gets passed to report generation.

### Phase 4: Report Generation

**If shell access is available (Python required):**

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/security-audit/scripts/generate-report.py" "<findings_file>" "<format>" "<output_file>"
```

Supported formats: `markdown`, `sarif`, `json`. Use `-` as output file for stdout.

**If no shell access:**

Format the report directly following this structure:

```markdown
# Security Audit Report

**Scan date:** <date>
**Mode:** <full|incremental>
**Files scanned:** <count>
**Findings:** <N> Critical, <N> High, <N> Medium, <N> Low

---

## Critical (<count>)

### [C-001] <Pattern Name>
- **File:** `<path>:<line>`
- **Commit:** `<hash>` (<date>, <author>) [if git available]
- **Pattern:** <pattern name>
- **Match:** <redacted>
- **Confidence:** <High|Medium|Low>
- **Context:** <LLM assessment>
- **Remediation:** <actionable steps>
```

Group findings by severity (Critical, High, Medium, Low). Assign sequential IDs per severity tier (C-001, H-001, M-001, L-001). **Never echo full secret values — always use the redacted form from scanner output.** For file-level findings (`line: 0`), display as `<path>:0 (entire file)` and include the file-type-specific remediation from `references/secret-patterns.md`.

End with scan metadata: excluded directories, pattern counts, config source.

## Configuration Reference

The skill reads `.security-audit.yml` from the repo root. See `examples/security-audit.yml` for all supported options including:
- `scan.mode` — full, incremental, or paths
- `exclude.directories` / `exclude.files` — skip patterns
- `severity.minimum` — filter output by minimum severity
- `output.format` — markdown, sarif, or json
- `custom_patterns.secrets` — add custom regex patterns
- `custom_patterns.allowlist` — suppress known false positives

**Applying configuration to script invocations:**
- `exclude.directories` → pass as `--exclude-dirs` (comma-separated) to both scanner scripts
- `scan.mode: incremental` + `scan.base_branch` → pass as `--base-branch` to scanner scripts
- `output.format` → pass as the `<format>` argument to `generate-report.py`
- `severity.minimum` — filter applied by the LLM during Phase 3; not a script flag
- `exclude.patterns` (glob patterns) — not supported by the scanner scripts; apply filtering manually before invoking the scripts, or skip files that match during Phase 3 analysis
- `custom_patterns.secrets` — not passed to scanner scripts at runtime; to use custom patterns with the scripts, add them to `scripts/patterns.dat` in the format: `<SEVERITY>\t<id>\t<name>\t<regex>`
- `custom_patterns.allowlist` — applied by the LLM during Phase 3; check each finding's file path and matched value against the allowlist and suppress matching findings

## Additional Resources

### Reference Files

Consult these for detailed patterns and classification rules:
- **`references/secret-patterns.md`** — regex patterns for 20+ secret types organized by severity
- **`references/vulnerability-patterns.md`** — OWASP-style vulnerability detection patterns
- **`references/severity-guide.md`** — severity tier definitions and contextual adjustment rules

### Scripts

- **`scripts/scan-secrets.sh`** — primary bash-based pattern scanner
- **`scripts/scan-secrets.py`** — Python fallback with entropy detection
- **`scripts/patterns.dat`** — compiled patterns file used by scanner scripts
- **`scripts/generate-report.py`** — report formatter (Markdown, SARIF, JSON) with built-in remediation guidance

### Examples

- **`examples/sample-report.md`** — example Markdown report
- **`examples/sample-report.sarif.json`** — example SARIF output
- **`examples/security-audit.yml`** — example configuration file
