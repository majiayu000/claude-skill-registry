---
name: code-security-audit
description: Perform security audits on code changes, diffs, or branches to find high-confidence exploitable vulnerabilities. Use when asked to "audit security", "review for vulnerabilities", "security scan", "check for security issues", "audit this PR", "review these changes for security", or "find vulnerabilities in diff". Distinct from security-review (which provides secure coding patterns/checklists) — this skill actively audits code changes using a structured methodology with false positive filtering. Includes Python scripts for GitHub Action CI integration and PR evaluation.
---

# Code Security Audit

AI-powered security audit for code changes with false positive filtering. Based on [claude-code-security-review](https://github.com/anthropics/claude-code-security-review).

## Bundled Resources

```
claude-code-security-review/
├── SKILL.md                          # This file — workflow and instructions
├── action.yml                        # GitHub Actions composite action definition
├── claudecode/                       # Python package (imports: from claudecode.*)
│   ├── __init__.py                   # Package init — re-exports main entry points
│   ├── audit.py                      # Entry point — wraps github_action_audit
│   ├── github_action_audit.py        # GitHub Action audit runner (PR fetch, Claude runner, filter pipeline)
│   ├── prompts.py                    # Security audit prompt templates
│   ├── findings_filter.py            # Hard exclusion rules + Claude API false positive filtering
│   ├── claude_api_client.py          # Claude API client for single-finding analysis
│   ├── json_parser.py               # Robust JSON extraction from text (code blocks, nested braces)
│   ├── constants.py                  # Config: model name, timeouts, token limits, exit codes
│   ├── logger.py                     # Stderr logging with GitHub context prefix
│   ├── requirements.txt              # Python deps: anthropic, requests, PyGithub
│   └── evals/                        # Evaluation framework
│       ├── run_eval.py               # CLI: python -m claudecode.evals.run_eval owner/repo#123
│       └── eval_engine.py            # Git worktree management + SAST runner
├── scripts/                          # Standalone scripts (non-Python-package)
│   └── comment-pr-findings.js        # Node.js script to post findings as PR review comments
├── references/                       # Knowledge loaded into context as needed
│   ├── false-positive-filtering.md   # 20 hard exclusions, signal quality criteria, 12 precedents
│   ├── custom-scan-instructions.md   # Industry templates (compliance, finserv, e-commerce, GraphQL)
│   ├── custom-false-positive-filtering.txt   # Example custom FP filtering rules
│   └── custom-security-scan-instructions.txt # Example custom scan categories
└── assets/                           # Files used in output
    └── security-review-command.md    # Claude Code /security-review slash command template
```

## Manual Audit Workflow

Use this when auditing code changes directly (without CI scripts).

### 1. Gather Changes

```bash
git diff --merge-base origin/main        # Branch diff
git diff --cached                         # Staged changes
git diff HEAD~N                           # Last N commits
git diff --name-only origin/main...       # List modified files
```

### 2. Three-Phase Analysis

**Phase 1 — Context Research:** Identify security frameworks, ORMs, auth libraries, sanitization patterns, and trust boundaries in the codebase.

**Phase 2 — Comparative Analysis:** Compare new code against established secure patterns. Flag deviations, inconsistencies, and new attack surfaces.

**Phase 3 — Vulnerability Assessment:** Check each modified file for:

- **Input Validation:** SQL injection, command injection, XXE, template injection, NoSQL injection, path traversal
- **Auth & Authz:** Auth bypass, privilege escalation, session flaws, JWT vulnerabilities
- **Crypto & Secrets:** Hardcoded keys/tokens, weak algorithms, improper key storage
- **Code Execution:** RCE via deserialization, pickle/YAML injection, eval injection, XSS
- **Data Exposure:** Sensitive data logging, PII violations, API leakage, debug exposure

Trace data flow from user inputs to sensitive operations. Look for privilege boundary crossings.

### 3. Filter False Positives

Load [references/false-positive-filtering.md](references/false-positive-filtering.md) and apply all rules. Assign confidence 1-10 per finding; only keep findings with confidence ≥ 8.

For domain-specific categories, load [references/custom-scan-instructions.md](references/custom-scan-instructions.md).

### 4. Output Format

```markdown
# Vuln N: [Category]: `file.ts:42`

* Severity: HIGH | MEDIUM
* Confidence: 8/10
* Description: [What the vulnerability is]
* Exploit Scenario: [Concrete attack path]
* Recommendation: [Specific fix]
```

## GitHub Action Integration

Run automated security audits on PRs via CI. Requires `ANTHROPIC_API_KEY` and `GITHUB_TOKEN`.

### Setup

```bash
pip install -r claudecode/requirements.txt
```

### Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `ANTHROPIC_API_KEY` | Yes | Claude API access |
| `GITHUB_TOKEN` | Yes | GitHub API access for PR data |
| `GITHUB_REPOSITORY` | Yes | `owner/repo` format |
| `PR_NUMBER` | Yes | Pull request number |
| `EXCLUDE_DIRECTORIES` | No | Comma-separated dirs to skip |
| `ENABLE_CLAUDE_FILTERING` | No | `true` to use Claude API for FP filtering |
| `FALSE_POSITIVE_FILTERING_INSTRUCTIONS` | No | Path to custom filtering rules |
| `CUSTOM_SECURITY_SCAN_INSTRUCTIONS` | No | Path to custom scan categories |

### Run

```bash
python claudecode/audit.py
```

Output is JSON with `findings`, `analysis_summary`, and `filtering_summary`.

### GitHub Actions Workflow

```yaml
name: Security Review
permissions:
  pull-requests: write
  contents: read
on:
  pull_request:
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          fetch-depth: 2
      - uses: anthropics/claude-code-security-review@main
        with:
          comment-pr: true
          claude-api-key: ${{ secrets.CLAUDE_API_KEY }}
```

### PR Commenting

Post findings as inline review comments:

```bash
node scripts/comment-pr-findings.js
```

Reads `findings.json` from cwd. Requires `GITHUB_TOKEN` and `GITHUB_EVENT_PATH`.

### Example Customization Files

See `references/` for sample customization files:
- `references/custom-false-positive-filtering.txt` — Template for custom FP filtering rules
- `references/custom-security-scan-instructions.txt` — Template for custom scan categories

## Evaluation Framework

Test the audit against any public PR:

```bash
export ANTHROPIC_API_KEY=sk-...
python -m claudecode.evals.run_eval owner/repo#123 --verbose
```

Results saved to `./eval_results/` as JSON with findings, runtime, and success status.

## Slash Command

Copy [assets/security-review-command.md](assets/security-review-command.md) to `.claude/commands/security-review.md` in any project to enable `/security-review` in Claude Code.

## Key Principles

1. **Minimize false positives** — only flag issues with >80% confidence of exploitability
2. **Skip noise** — no theoretical issues, style concerns, or low-impact findings
3. **Focus on impact** — prioritize unauthorized access, data breaches, system compromise
4. **Only new issues** — do not comment on pre-existing security concerns
5. **Better to miss theoretical issues than flood with false positives**

## Severity Guidelines

- **HIGH**: Directly exploitable → RCE, data breach, auth bypass
- **MEDIUM**: Requires specific conditions but significant impact
- Do NOT report LOW severity findings
