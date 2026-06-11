---
name: gh-triage-ru
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: >-
  GitHub issue/PR triage via ru and gh. Use when processing issues, closing PRs
  (no-contributions policy), or bulk triage. Independent verification required.
practices:
- pragmatic-programmer
---
# gh-triage-ru — GitHub Issues/PRs with ru

> **Core Insight:** User reports are hints, not facts. Every bug report, feature request, and PR must be independently verified. Never trust suggested fixes—implement your own solution based on your own analysis.

## The Full Contribution Policy

This is the official policy disclosed to users in READMEs:

> *About Contributions:* Please don't take this the wrong way, but I do not accept outside contributions for any of my projects. I simply don't have the mental bandwidth to review anything, and it's my name on the thing, so I'm responsible for any problems it causes; thus, the risk-reward is highly asymmetric from my perspective. I'd also have to worry about other "stakeholders," which seems unwise for tools I mostly make for myself for free. Feel free to submit issues, and even PRs if you want to illustrate a proposed fix, but know I won't merge them directly. Instead, I'll have Claude or Codex review submissions via `gh` and independently decide whether and how to address them. Bug reports in particular are welcome. Sorry if this offends, but I want to avoid wasted time and hurt feelings. I understand this isn't in sync with the prevailing open-source ethos that seeks community contributions, but it's the only way I can move at this velocity and keep my sanity.

**Translation for agents:** We NEVER merge PRs. Ever. PRs are intel, not contributions. Mine them for ideas, implement yourself, close with explanation.

---

## Quick Start

```bash
# 1. Health check
ru doctor && gh auth status

# 2. Discover open items (2025+ only)
ru review --dry-run --json 2>/dev/null | \
  jq '[.items[] | select(.created_at >= "2025-01-01")]'

# 3. Review each item
gh issue view NUMBER -R owner/repo
gh pr diff NUMBER -R owner/repo  # THE INTEL for PRs

# 4. Verify independently (NEVER trust user claims)
cd /data/projects/REPO
git log --oneline --since="ISSUE_DATE" | head -20  # Already fixed?
grep -r "relevant_function" src/                    # Find the code

# 5. Take action
gh issue close N -R owner/repo -c "Fixed in abc123"
gh pr close N -R owner/repo -c "Thanks! Implemented independently in abc123"
```

---

## Decision Matrix

| Type | Status | Action | Response |
|------|--------|--------|----------|
| Bug, confirmed unfixed | Verified | Fix it | `gh issue close N -c "Fixed in SHA"` |
| Bug, already fixed | Verified | Close | `gh issue close N -c "Fixed in SHA from DATE"` |
| Bug, can't reproduce | Unknown | Ask | Use [REQUEST-INFO.md](references/REQUEST-INFO.md) |
| Bug, pre-2025 | Stale | Close | `gh issue close N -c "Closing as stale"` |
| Feature, simple | Fits scope | Implement | `gh issue close N -c "Implemented in SHA"` |
| Feature, complex | Needs judgment | **SURFACE** | Use [SURFACE-FORMAT.md](references/SURFACE-FORMAT.md) |
| Feature, scope creep | Doesn't fit | Decline | Use [DECLINE-TEMPLATES.md](references/DECLINE-TEMPLATES.md) |
| PR, any | N/A | **NEVER MERGE** | Close + mine for ideas |

---

## The Independent Verification Protocol

This is non-negotiable. Every claim must be verified.

### DO NOT:
- Trust that the bug exists as described
- Trust that the suggested fix is correct
- Trust that reproduction steps work
- Assume the issue is still relevant
- Copy-paste user-provided code fixes

### DO:
- Reproduce bugs yourself
- Check commits since issue date
- Read the actual code
- Verify against official docs
- Test empirically
- Write your OWN fix

### Verification Questions

| Claim Type | How to Verify |
|------------|---------------|
| "X crashes" | Reproduce the crash yourself |
| "X doesn't work" | Define "work", test actual behavior |
| "X should do Y" | Check docs, is this intended? |
| "X is slow" | Benchmark, compare to baseline |
| "X has security issue" | Analyze code path, test exploit |
| "This PR fixes it" | Read diff, understand approach, implement yourself |

### Verification Commands

```bash
cd /data/projects/REPO_NAME

# Check if commits since issue might have fixed it
git log --oneline --since="ISSUE_DATE" | head -20

# Search codebase for relevant code
grep -r "relevant_function" src/

# Read the actual implementation
cat src/relevant_file.rs

# Check current behavior
./target/debug/tool --help

# For API claims, verify against official docs
# (Use WebFetch for official documentation)
```

**Deep dive:** [VERIFICATION.md](references/VERIFICATION.md)

---

## PR Handling: Mine, Never Merge

PRs contain intel, not contributions. The workflow:

1. **Read the diff** — This is THE INTEL
2. **Understand their approach** — What problem are they solving? How?
3. **Write YOUR OWN implementation** — Never copy their code
4. **Commit** — No attribution needed for ideas
5. **Close PR with explanation** — Be kind, explain policy

```bash
# View the diff (THE INTEL)
gh pr diff NUMBER -R owner/repo

# Read their approach
gh pr view NUMBER -R owner/repo --comments

# If idea is good:
# 1. Understand their approach
# 2. Write YOUR OWN implementation
# 3. Commit (no attribution needed for ideas)
# 4. Close PR with explanation
```

### PR Close Template

```bash
gh pr close NUMBER -R owner/repo -c "$(cat <<'EOF'
Thanks for the contribution! Per project policy, I don't merge outside PRs, but I reviewed your approach.

[One of:]
- I've implemented a similar fix in abc123
- Noted the idea—may address differently later
- Current behavior is intentional because [reason]

Appreciate you taking the time!
EOF
)"
```

---

## Response Templates

### Bug Fixed

```bash
gh issue close N -R owner/repo -c "$(cat <<'EOF'
Fixed in abc123.

The issue was [brief explanation]. [Any additional context.]
EOF
)"
```

### Bug Already Fixed

```bash
gh issue close N -R owner/repo -c "$(cat <<'EOF'
This was fixed in abc123 (from DATE).

Please update to the latest version. If issue persists after updating, reopen with details.
EOF
)"
```

### Cannot Reproduce

```bash
gh issue comment N -R owner/repo -b "$(cat <<'EOF'
I tried to reproduce this but couldn't. Could you provide:

- Exact steps to reproduce
- OS and version
- Full error output
- Tool version (`tool --version`)

Happy to investigate with more details.
EOF
)"
```

### Stale Issue (Pre-2025)

```bash
gh issue close N -R owner/repo -c "$(cat <<'EOF'
Closing as stale—the codebase has changed significantly.

If this is still relevant with current versions, please open a new issue with fresh reproduction steps.
EOF
)"
```

### Feature Implemented

```bash
gh issue close N -R owner/repo -c "$(cat <<'EOF'
Implemented in abc123.

[Brief description of what was added and how to use it.]
EOF
)"
```

### Feature Declined (Scope Creep)

```bash
gh issue close N -R owner/repo -c "$(cat <<'EOF'
Thanks for the suggestion! After consideration, this would add scope I'm trying to avoid.

[Optional: brief explanation or workaround]

Feel free to fork if you need this functionality.
EOF
)"
```

**More templates:** [DECLINE-TEMPLATES.md](references/DECLINE-TEMPLATES.md) | [REQUEST-INFO.md](references/REQUEST-INFO.md)

---

## Surface Format: When Judgment Required

For complex features, ambiguous issues, or security-related items—surface to user for decision.

### When to Surface

| Situation | Surface? | Why |
|-----------|----------|-----|
| Simple bug, clear fix | No | Just fix it |
| Feature fits, low effort | No | Just do it |
| Complex feature request | **Yes** | Scope implications |
| Interesting PR ideas | **Yes** | Need approval to integrate |
| Ambiguous intended behavior | **Yes** | Could break things |
| Security-related | **Yes** | High stakes |
| Multiple valid approaches | **Yes** | Design decision |
| Breaking changes | **Yes** | User impact |

### Surface Format

```
FEATURE REQUEST REQUIRING JUDGMENT: owner/repo#42

**Request:** "[Title from issue]"

**User's Problem:** [What they're trying to accomplish]

**Analysis:**
+ [Benefit 1]
+ [Benefit 2]
- [Drawback 1]
- [Drawback 2]
- Scope Risk: [What this might lead to]

**Implementation Options:**
1. Full implementation: [What it would take]
2. Simplified version: [Reduced scope alternative]
3. Decline: [Polite response]

**My recommendation:** Option [X] because [reasoning]

**If approved:** I'll implement and close with: "[proposed response]"
```

**More formats:** [SURFACE-FORMAT.md](references/SURFACE-FORMAT.md)

---

## Scope Creep Detection

| Signal | Why It's Scope Creep |
|--------|---------------------|
| "Also add X while you're at it" | Bundled unrelated request |
| "Support format Y too" | Opens floodgate for formats |
| Requires new dependencies | Maintenance burden |
| Changes core architecture | Risk outweighs benefit |
| "Make it configurable" | Complexity for edge cases |
| "Would be nice if..." | Vague, unbounded request |
| "What if we also..." | Feature creep in disguise |
| "Full parity with X" | Massive scope expansion |

---

## Bulk Processing

```bash
# Get all 2025+ issues
gh issue list -R owner/repo --state open --json number,title,createdAt | \
  jq '.[] | select(.createdAt >= "2025-01-01")'

# Count by repo
ru review --dry-run --json 2>/dev/null | \
  jq 'group_by(.repo) | map({repo: .[0].repo, count: length})'

# Process systematically
for num in $(gh issue list -R owner/repo --state open --json number -q '.[].number'); do
  echo "=== Issue #$num ==="
  gh issue view $num -R owner/repo
  # Analyze, verify, act
done
```

---

## Validation

After triage session:

```bash
# Verify no 2025+ issues remain unaddressed
ru review --dry-run --json 2>/dev/null | \
  jq '[.items[] | select(.created_at >= "2025-01-01" and .state == "open")] | length'
# Should be 0 (or only surfaced items awaiting judgment)

# Verify commits reference issues
git log --oneline --grep="Closes #" -10
git log --oneline --grep="Fixed #" -10
```

---

## Automated Integrity Checks via dsr

GitHub Actions is unreliable (throttling/cutoff). All critical integrity checks run locally via systemd timers and `dsr`.

### ACFS Manifest SHA256 Drift (CRITICAL)

The ACFS `curl | bash` installer breaks when `manifest_index.sh` has a stale SHA256 hash. This has been a recurring crisis. It is now **fully automated**:

```bash
# Check manifest drift (check-only)
/data/projects/agentic_coding_flywheel_setup/scripts/check-manifest-drift.sh --json

# Check and auto-fix (what the timer runs)
/data/projects/agentic_coding_flywheel_setup/scripts/check-manifest-drift.sh --fix

# Systemd timer status (runs every 2h)
systemctl --user status acfs-manifest-drift.timer

# View recent runs
journalctl --user -u acfs-manifest-drift.service --since "24h ago"

# dsr quality gate (manual check)
dsr quality --tool agentic_coding_flywheel_setup
```

**How it works:**
1. Systemd timer fires every 2 hours
2. Script compares `sha256sum acfs.manifest.yaml` against hash in `manifest_index.sh`
3. If mismatch: runs `bun run generate`, commits, pushes automatically
4. ACFS is also registered in `~/.config/dsr/repos.yaml` with manifest-drift as a quality gate

**When triaging ACFS issues:** Always run the drift check first. Many "install fails" issues are caused by manifest drift, not code bugs.

### Adding New Automated Checks

For any repo with recurring integrity issues, the pattern is:

1. **Create a check script** in the repo's `scripts/` directory (exit 0 = ok, exit 1 = drift)
2. **Register in dsr** via `~/.config/dsr/repos.yaml` under `checks:`
3. **Create systemd timer** in `~/.config/systemd/user/` for scheduled runs
4. **Enable**: `systemctl --user enable --now <name>.timer`

---

## References

| Topic | Resource |
|-------|----------|
| Request info templates | [REQUEST-INFO.md](references/REQUEST-INFO.md) |
| Decline templates | [DECLINE-TEMPLATES.md](references/DECLINE-TEMPLATES.md) |
| Surface formats | [SURFACE-FORMAT.md](references/SURFACE-FORMAT.md) |
| gh command reference | [GH-COMMANDS.md](references/GH-COMMANDS.md) |
| Verification deep dive | [VERIFICATION.md](references/VERIFICATION.md) |
| Real-world examples | [REAL-EXAMPLES.md](references/REAL-EXAMPLES.md) |

---

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Merge PRs | Policy violation | Close with explanation |
| Trust user diagnosis | Often wrong | Verify independently |
| Close without response | Bad UX | Always explain why |
| Batch-close stale issues | Loses context | Review each briefly |
| Implement user's exact code | Could be wrong | Write your own version |
| Ignore old issues | May contain valid bugs | Triage by date, close if stale |
| Skip verification | Miss bugs or break things | Always verify empirically |
| Copy PR code | Violates policy spirit | Understand approach, reimplement |
