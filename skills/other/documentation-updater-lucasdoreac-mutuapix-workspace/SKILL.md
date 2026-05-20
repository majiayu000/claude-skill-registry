---
name: Documentation Updater
description: Automatically updates CLAUDE.md and related documentation when new features, configurations, or best practices are discovered during development sessions
version: 1.0.0
allowed-tools: [Read, Edit, Write, Grep, Bash]
---

# Documentation Updater Skill

## Overview

This skill implements a **self-improving documentation system** for the MutuaPIX project. It automatically:
- Detects when new information is discovered during sessions
- Updates CLAUDE.md with new commands, patterns, and configurations
- Maintains skills documentation (SKILL.md files)
- Tracks version history of documentation changes

## Core Principle: Progressive Disclosure

Documentation follows the **progressive disclosure pattern**:
1. **Quick Reference** - Essential commands and patterns in CLAUDE.md
2. **Detailed Guides** - In-depth explanation in SKILL.md files
3. **Context Files** - Supporting documentation (README, audit reports, etc.)

## Auto-Update Triggers

The system should update documentation when:

### 1. New Commands Discovered

**Trigger:** Running a bash command that solves a problem and should be remembered

**Example:**
```bash
# During session, you run:
ssh root@138.199.162.115 'cd /var/www/mutuapix-frontend-production && rm -rf .next && npm run build'

# Auto-update CLAUDE.md:
## Quick Commands > Frontend > Build
# Clear cache and rebuild
ssh root@138.199.162.115 'cd /var/www/mutuapix-frontend-production && rm -rf .next && npm run build'
```

### 2. New Configuration Patterns

**Trigger:** Discovering environment variable requirements or configuration settings

**Example:**
```bash
# Discovered: NEXT_PUBLIC_NODE_ENV required for production
# Auto-update: CLAUDE.md > Environment Variables section
```

### 3. Security Vulnerabilities Found

**Trigger:** Identifying security issues during code review or testing

**Example:**
```bash
# Found: authStore initializes with mock user
# Auto-create: SECURITY_AUDIT_[DATE].md
# Auto-update: CLAUDE.md > Security > Known Issues
```

### 4. New Skills Created

**Trigger:** Creating a new SKILL.md file

**Example:**
```bash
# Created: .claude/skills/pix-validation/SKILL.md
# Auto-update: CLAUDE.md > Available Skills section
```

### 5. Workflow Improvements

**Trigger:** Discovering better way to perform existing task

**Example:**
```bash
# Old way: Manual file transfer
# New way: rsync with specific flags
# Auto-update: CLAUDE.md > Deployment section
```

## Update Workflow

### Step 1: Detect Update Trigger

```typescript
interface UpdateTrigger {
  type: 'command' | 'config' | 'security' | 'skill' | 'workflow';
  source: string;              // Where was this discovered?
  content: string;             // What should be documented?
  priority: 'low' | 'medium' | 'high' | 'critical';
  relatedFiles: string[];      // Which files are affected?
}
```

### Step 2: Determine Update Location

**Decision Tree:**
```
Is it a quick command/reference?
  YES → Update CLAUDE.md > Quick Commands
  NO → Continue

Is it detailed technical knowledge?
  YES → Update or create SKILL.md
  NO → Continue

Is it a security issue?
  YES → Create SECURITY_AUDIT_[DATE].md + update CLAUDE.md
  NO → Continue

Is it project-specific documentation?
  YES → Update README.md or docs/
  NO → Log for future review
```

### Step 3: Format Update

**CLAUDE.md Updates:**
```markdown
## Section Title

### Subsection (if needed)

**Description:** Brief explanation of what/why

**Command/Pattern:**
```bash
# Comment explaining what this does
command here
```

**Related Files:** `path/to/file.ext`

**Added:** 2025-10-16 (Track when added)
```

**SKILL.md Updates:**
```markdown
## Version History

- **1.1.0** (2025-10-16): [Description of update]
  - Added: Feature X
  - Fixed: Issue Y
  - Updated: Section Z
```

### Step 4: Verify Update

**Checklist:**
- [ ] Is the information accurate?
- [ ] Is it concise (CLAUDE.md sections should be <200 words)?
- [ ] Is it actionable (commands can be copy-pasted)?
- [ ] Is it versioned (date added, version number)?
- [ ] Are related files cross-referenced?

### Step 5: Commit Changes

```bash
# Auto-commit documentation updates
git add CLAUDE.md .claude/skills/
git commit -m "docs: auto-update from session [SESSION_ID]

- Added: [brief description]
- Updated: [sections modified]
- Source: [what triggered update]

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## CLAUDE.md Structure

### Required Sections

```markdown
# CLAUDE.md

**Last Updated:** YYYY-MM-DD
**Location:** `/Users/lucascardoso/Desktop/MUTUA/`
**Auto-Update Enabled:** ✅

---

## 🎯 Project Overview
[Brief description, tech stack]

## 🚀 Quick Start Commands
[Most common commands for dev/deploy]

## 🏗️ Architecture
[High-level system design]

## 🔐 Security
[Critical security considerations]

## 📋 Available Skills
[List of SKILL.md files with descriptions]

## ⚙️ Configuration
[Environment variables, important settings]

## 🐛 Troubleshooting
[Common issues and solutions]

## 📚 Documentation References
[Links to detailed docs]

## 🔄 Version History
[Track major CLAUDE.md changes]
```

### Keep It Concise

**❌ BAD (Too verbose):**
```markdown
The MutuaPIX platform uses a comprehensive authentication system
that leverages Laravel Sanctum on the backend for secure token-based
authentication while the frontend utilizes Next.js with Zustand for
state management and localStorage for token persistence...
```

**✅ GOOD (Concise):**
```markdown
## Authentication

**Stack:** Laravel Sanctum (backend) + Zustand (frontend)
**Token Lifetime:** 24 hours
**Login Flow:** CSRF token → POST /api/v1/login → Store JWT

**Quick Test:**
```bash
curl https://api.mutuapix.com/api/v1/health
```

**Details:** See `.claude/skills/authentication-management/SKILL.md`
```

## Skills Discovery

When Claude needs to find a skill:

```bash
# List all available skills
ls -la .claude/skills/

# Search skills by keyword
grep -r "PIX validation" .claude/skills/*/SKILL.md

# Read specific skill
cat .claude/skills/pix-validation/SKILL.md
```

**Auto-discovery:** Skills are automatically discovered from:
1. `.claude/skills/` (project-level)
2. `~/.claude/skills/` (personal)
3. Plugin-provided skills

## Update Examples

### Example 1: New Environment Variable Discovered

**Trigger:**
```bash
# During debugging, discovered NEXT_PUBLIC_NODE_ENV is required
```

**Auto-Update CLAUDE.md:**
```markdown
## Environment Variables

### Frontend Production (.env.production on VPS)

```bash
NEXT_PUBLIC_NODE_ENV=production          # ⚠️ CRITICAL: Required for security
NEXT_PUBLIC_API_URL=https://api.mutuapix.com
NEXT_PUBLIC_USE_AUTH_MOCK=false
```

**Why NEXT_PUBLIC_NODE_ENV is Critical:**
- `process.env.NODE_ENV` is undefined in Next.js client-side code
- Mock authentication relies on this for environment detection
- Missing this variable = security bypass in production!

**Added:** 2025-10-16
**Related Files:** `frontend/src/lib/env.ts`, `frontend/src/stores/authStore.ts`
```

### Example 2: New Deployment Command

**Trigger:**
```bash
# Discovered that clearing .next cache is required for env var changes
ssh root@138.199.162.115 'cd /var/www/mutuapix-frontend-production && rm -rf .next && npm run build && pm2 restart mutuapix-frontend'
```

**Auto-Update CLAUDE.md:**
```markdown
## Deployment

### Frontend Deployment (Environment Variable Changes)

**⚠️ IMPORTANT:** When updating `.env.production`, must clear cache before rebuild!

```bash
# 1. Update .env.production on VPS
ssh root@138.199.162.115 'echo "NEXT_PUBLIC_NODE_ENV=production" >> /var/www/mutuapix-frontend-production/.env.production'

# 2. Clear cache + rebuild + restart
ssh root@138.199.162.115 'cd /var/www/mutuapix-frontend-production && rm -rf .next && npm run build && pm2 restart mutuapix-frontend'

# 3. Verify
curl -I https://matrix.mutuapix.com/login
```

**Why Clear Cache:**
Next.js caches compiled bundles. Without clearing `.next/`, old environment variables persist.

**Added:** 2025-10-16
```

### Example 3: Security Issue Found

**Trigger:**
```typescript
// Discovered: authStore has default mock user
// File: frontend/src/stores/authStore.ts:91-96
user: devLocalUser,           // ❌ VULNERABILITY
```

**Auto-Create:** `SECURITY_AUDIT_2025_10_16.md` (full report)

**Auto-Update CLAUDE.md:**
```markdown
## Security

### Known Issues

**🔴 CRITICAL: Default Mock User in authStore** (Found: 2025-10-16)

**Issue:** `authStore` initializes with authenticated mock admin user by default.

**Risk:** If localStorage is empty, user appears logged in without credentials.

**Fix:** See `AUTHENTICATION_AUDIT_REPORT.md` Section "Remediation Plan > Phase 1"

**Status:** 🟡 Pending fix

**Related Files:**
- `frontend/src/stores/authStore.ts:91-96`
- `.claude/skills/authentication-management/SKILL.md`
```

## Self-Improvement Loop

### Phase 1: Discovery
- Claude encounters new information during session
- Flags it as potential documentation update

### Phase 2: Validation
- Is this information accurate?
- Is it useful for future sessions?
- Where should it be documented?

### Phase 3: Update
- Edit CLAUDE.md or create/update SKILL.md
- Follow formatting guidelines
- Add version history entry

### Phase 4: Verification
- Read updated documentation
- Verify it's clear and actionable
- Check for consistency with existing docs

### Phase 5: Commit
- Create git commit with descriptive message
- Tag with "docs:" prefix for auto-tracking

## Metrics & Tracking

### Documentation Health Metrics

```typescript
interface DocHealthMetrics {
  claudeMdSize: number;              // Bytes (target: <50KB)
  skillsCount: number;               // Number of SKILL.md files
  lastUpdated: Date;                 // Most recent update
  staleSections: string[];           // Sections >90 days old
  brokenLinks: string[];             // Dead file references
  todoItems: number;                 // Unresolved TODOs in docs
}
```

### Update Frequency

**Target:**
- CLAUDE.md: Updated after every significant session (new feature, bug fix, deployment)
- SKILL.md: Updated when skill scope changes (version bump)
- Security docs: Updated immediately when vulnerability found

### Quality Checks

Before updating CLAUDE.md, verify:
- [ ] Total file size <50KB (concise documentation)
- [ ] No duplicate information across sections
- [ ] All commands tested and work
- [ ] All file paths are valid
- [ ] No sensitive data (passwords, API keys)
- [ ] Version history entry added

## Integration with Claude Sessions

### At Session Start

1. Read CLAUDE.md to understand project context
2. Load relevant SKILL.md files based on user's task
3. Check for stale documentation (>30 days old)

### During Session

1. Note when new information is discovered
2. Flag for documentation update
3. Continue with task (don't interrupt flow)

### At Session End

1. Review flagged documentation updates
2. Apply updates to CLAUDE.md and/or SKILL.md
3. Commit changes with descriptive message
4. Summary of documentation changes for user

### User Prompt for Updates

When user says:
- "Update CLAUDE.md with this" → Apply update immediately
- "Remember this for next time" → Add to appropriate doc
- "This is important" → Flag as high priority for CLAUDE.md
- "Document this workflow" → Create or update SKILL.md

## Best Practices

### DO:
✅ Keep CLAUDE.md concise (<50KB total)
✅ Use bullet points over paragraphs
✅ Include copy-pasteable commands
✅ Cross-reference detailed docs in SKILL.md
✅ Add dates to new entries
✅ Version bump SKILL.md when updating

### DON'T:
❌ Duplicate information across files
❌ Include verbose explanations in CLAUDE.md
❌ Commit broken/untested commands
❌ Leave TODOs unresolved for >7 days
❌ Remove historical information (archive instead)

## Related Files

**Core Documentation:**
- `CLAUDE.md` - Main project guide (you are here)
- `.claude/skills/*/SKILL.md` - Detailed skill documentation
- `README.md` - Public-facing project readme

**Audit Reports:**
- `AUTHENTICATION_AUDIT_REPORT.md` - Security audit (2025-10-16)
- `VPS_AUDIT_REPORT.md` - Infrastructure audit
- `CLEANUP_EXECUTION_REPORT.md` - VPS cleanup log

**Legacy:**
- `WORKFLOW_RULES_FOR_CLAUDE.md` - Git workflow rules
- `docs/` - Additional project documentation

## Version History

- **1.0.0** (2025-10-16): Initial documentation updater skill
  - Defined auto-update triggers
  - Established update workflow
  - Created documentation structure guidelines
  - Implemented self-improvement loop
