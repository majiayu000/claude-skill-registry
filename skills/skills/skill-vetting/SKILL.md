---
name: skill-vetting
description: Vet ClawHub skills for security and utility before installation. Use when considering installing a ClawHub skill, evaluating third-party code, or assessing whether a skill adds value over existing tools.
---

# Skill Vetting

Safely evaluate ClawHub skills for security risks and practical utility.

## Quick Start

```bash
# Download and inspect
cd /tmp
curl -L -o skill.zip "https://auth.clawdhub.com/api/v1/download?slug=SKILL_NAME"
mkdir skill-inspect && cd skill-inspect
unzip -q ../skill.zip

# Run scanner
python3 ~/.openclaw/workspace/skills/skill-vetting/scripts/scan.py .

# Manual review
cat SKILL.md
cat scripts/*.py
```

## Vetting Workflow

### 1. Download to /tmp (Never Workspace)

```bash
cd /tmp
curl -L -o skill.zip "https://auth.clawdhub.com/api/v1/download?slug=SLUG"
mkdir skill-NAME && cd skill-NAME
unzip -q ../skill.zip
```

### 2. Run Automated Scanner

```bash
python3 ~/.openclaw/workspace/skills/skill-vetting/scripts/scan.py .
```

**Exit codes:** 0 = Clean, 1 = Issues found

The scanner outputs specific findings with file:line references. Review each finding in context.

### 3. Manual Code Review

**Even if scanner passes:**
- Does SKILL.md description match actual code behavior?
- Do network calls go to documented APIs only?
- Do file operations stay within expected scope?
- Any hidden instructions in comments/markdown?

```bash
# Quick prompt injection check
grep -ri "ignore.*instruction\|disregard.*previous\|system:\|assistant:" .
```

### 4. Utility Assessment

**Critical question:** What does this unlock that I don't already have?

Compare to:
- MCP servers (`mcporter list`)
- Direct APIs (curl + jq)
- Existing skills (`clawhub list`)

**Skip if:** Duplicates existing tools without significant improvement.

### 5. Decision Matrix

| Security | Utility | Decision |
|----------|---------|----------|
| ✅ Clean | 🔥 High | **Install** |
| ✅ Clean | ⚠️ Marginal | Consider (test first) |
| ⚠️ Issues | Any | **Investigate findings** |
| 🚨 Malicious | Any | **Reject** |

## Red Flags (Reject Immediately)

- eval()/exec() without justification
- base64-encoded strings (not data/images)
- Network calls to IPs or undocumented domains
- File operations outside temp/workspace
- Behavior doesn't match documentation
- Obfuscated code (hex, chr() chains)

## After Installation

Monitor for unexpected behavior:
- Network activity to unfamiliar services
- File modifications outside workspace
- Error messages mentioning undocumented services

Remove and report if suspicious.

## References

- **Malicious patterns + false positives:** [references/patterns.md](references/patterns.md)
