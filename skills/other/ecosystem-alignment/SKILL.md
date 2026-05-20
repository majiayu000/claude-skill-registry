---
name: ecosystem-alignment
description: Upstream version checking, agentskills.io spec compliance audit, Claude Code feature gap analysis. Activates on updates, version checks, or alignment work.
version: 1.0.0
---

# Ecosystem Alignment

Activates when checking upstream compatibility, auditing spec compliance, or aligning with platform updates.

## When to Trigger

- Claude Code version update detected
- User mentions "alignment", "upstream", "spec compliance", "version check"
- New agentskills.io spec changes published
- GSD upstream (get-shit-done) version update

## Checklist

### 1. Version Check
```bash
claude --version                    # Claude Code
npm list get-shit-done 2>/dev/null  # GSD upstream
```

### 2. Skill Description Compliance
```bash
for f in .claude/skills/*/SKILL.md; do
  desc=$(sed -n 's/^description: //p' "$f" | head -1)
  len=${#desc}
  [ $len -gt 250 ] && echo "OVER ($len): $f"
done
```
agentskills.io enforces 250-character maximum.

### 3. Hook System Audit
- Check all hook files exist (no dead references)
- Verify CJS syntax (not ESM `import` in .js files)
- Test each hook executes without error
- Check for new hook types in platform (PostCompact, FileChanged, PermissionDenied, etc.)

### 4. Feature Gap Analysis
- Compare our skill/agent/team patterns against platform capabilities
- Identify platform features we're not using
- Identify our extensions that go beyond the platform
- Document alignment opportunities

### 5. Binary String Analysis
```bash
strings $(which claude) | grep -oP '"(skill|hook|agent|team|memory|worktree)[^"]*"' | sort -u
```
Identify new internal patterns from the installed binary.

## Output

Produce an alignment report documenting:
- Current versions (Claude Code, GSD, agentskills.io)
- Spec compliance status (all skills under 250 chars?)
- Hook health (dead refs, ESM issues, missing types)
- Feature gaps (what we should adopt, what we extend beyond)
- Action items ranked by priority
