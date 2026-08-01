---
name: ccpm-skill-creator
description: Creates custom CCPM skills from request to deployment with proper templates,
  safety guardrails, and integration patterns. Auto-activates when user mentions "create
  skill", "custom workflow", "team spe
---

---
name: ccpm-skill-creator
description: Creates custom CCPM skills from request to deployment with proper templates, safety guardrails, and integration patterns. Auto-activates when user mentions "create skill", "custom workflow", "team specific", "extend CCPM", "codify team practice", or "reusable pattern". Guides through purpose definition (what skill does), activation triggers (when it runs), CCPM integration points, and safety rules. Provides three skill templates: Team Workflow (codify practices), Safety Enforcement (add checks), and Integration Skills (custom tools). Creates directory structure, frontmatter metadata, multi-phase instructions, and supporting docs. Tests skill activation before deployment and suggests improvements.
---

# CCPM Skill Creator

Meta-skill for creating new CCPM skills with proper structure and conventions.

## When to Use

This skill auto-activates when:

- User asks: **"create skill"**, **"custom workflow"**, **"team specific"**, **"extend CCPM"**
- User wants to codify team practices
- Creating project-specific workflows
- Building reusable PM patterns

## What This Skill Creates

### CCPM Skill Template

A properly structured skill that follows CCPM conventions:

```yaml
---
name: your-skill-name
description: Clear description with trigger phrases and CCPM integration points (max 1024 chars)
allowed-tools: optional-tools-if-restricted
---

# Your Skill Display Name

Brief overview of what this skill does.

## When to Use

Auto-activates when:
- Trigger phrase 1
- Trigger phrase 2
- CCPM command execution

## Integration with CCPM

### Commands
List CCPM commands this skill works with

### Hooks
List CCPM hooks this skill complements

### Other Skills
List CCPM skills this works alongside

## Instructions

Step-by-step guidance for Claude

## Examples

Concrete examples with CCPM context

## Safety Considerations

External system write rules if applicable
```

## Creating a New Skill

### Step-by-Step Process

**Step 1: Define Purpose**

```
User: "Create a skill for our deployment workflow"

Claude: [ccpm-skill-creator activates]

Let's create a custom CCPM skill for your deployment workflow.

First, let me understand the purpose:

Questions:
1. What does this skill do?
   → "Automates deployment checklist and notifications"

2. When should it activate?
   → "When deploying to staging or production"

3. Which CCPM commands does it work with?
   → "/ccpm:done for production deploys"

4. Does it write to external systems?
   → "Yes - posts to Slack, updates Jira"

5. Is it team-specific or project-specific?
   → "Team-specific - all projects use same deployment process"

Got it! Creating deployment workflow skill...
```

**Step 2: Generate Skill Structure**

```
Creating skill: acme-deployment

Directory structure:
skills/acme-deployment/
├── SKILL.md (main skill definition)
├── deployment-checklist.md (reference doc)
└── environments.md (staging vs production)

Generating SKILL.md with CCPM integration...
```

**Step 3: Add CCPM Integration**

```yaml
---
name: acme-deployment
description: Automates Acme Corp deployment workflow with environment-specific checklists, Slack notifications, and Jira updates. Auto-activates when deploying to staging/production or running /ccpm:done. Enforces deployment checklist completion before external notifications.
---

# Acme Deployment Workflow

Custom deployment workflow for Acme Corp projects.

## When to Use

Auto-activates when:
- User mentions: "deploy to staging", "deploy to production", "ship it"
- Running `/ccpm:done` command
- Creating release PR

## Integration with CCPM

### Commands
- `/ccpm:done` - Triggers deployment checklist
- `/ccpm:verify` - Pre-deployment verification

### Skills
- `external-system-safety` - Confirms Slack/Jira writes
- `ccpm-code-review` - Ensures verification before deploy

## Instructions

### Deployment Checklist

Before any deployment:
1. ✅ All tests passing
2. ✅ Security scan complete
3. ✅ Performance benchmarks met
4. ✅ Database migrations tested
5. ✅ Rollback plan documented

### Staging Deployment

1. Run pre-deploy verification
2. Deploy to staging environment
3. Run smoke tests
4. Post to #engineering Slack
5. Update Jira with staging link

### Production Deployment

1. **REQUIRE CONFIRMATION** (safety critical)
2. Final verification check
3. Deploy to production
4. Run health checks
5. Post to #general Slack (with confirmation)
6. Update Jira to "Released" (with confirmation)
7. Celebrate! 🎉

### Safety Rules

**⛔ NEVER without confirmation:**
- Production deployments
- Slack posts to #general channel
- Jira status to "Released"

**✅ Always allowed:**
- Staging deployments
- Slack posts to #engineering
- Read operations

See [SAFETY_RULES.md](../../commands/SAFETY_RULES.md)

## Examples

[Team-specific deployment examples]
```

**Step 4: Add Supporting Documentation**

```markdown
# deployment-checklist.md

## Pre-Deployment Verification

- [ ] All CI/CD checks passing
- [ ] Security scan (Snyk) no high/critical issues
- [ ] Performance tests within 10% of baseline
- [ ] Database migrations run in staging
- [ ] Rollback procedure documented

## Staging Deployment

- [ ] Deploy to staging
- [ ] Smoke tests pass
- [ ] Manual QA complete
- [ ] Staging link shared in Slack

## Production Deployment

- [ ] Final verification
- [ ] Backup database (if schema changes)
- [ ] Deploy during maintenance window
- [ ] Health checks all green
- [ ] Rollback tested

## Post-Deployment

- [ ] Monitor error rates (15 minutes)
- [ ] Check performance metrics
- [ ] Update documentation
- [ ] Close Jira tickets
- [ ] Team notification
```

**Step 5: Test Skill**

```
Testing acme-deployment skill...

Test 1: Activation
Input: "Deploy to production"
✅ Skill activates
✅ Shows deployment checklist

Test 2: Safety
Input: "Post to Slack #general"
✅ external-system-safety blocks without confirmation
✅ Requires explicit "yes"

Test 3: Integration
Input: "/ccpm:done WORK-123"
✅ acme-deployment runs deployment checklist
✅ Integrates with completion workflow

All tests passing ✅

Skill ready to use!
```

## Skill Templates

### Template 1: Team Workflow Skill

**Purpose**: Codify team-specific practices

```yaml
---
name: [team]-[workflow]
description: Team-specific workflow for [purpose]. Activates when [triggers]. Integrates with CCPM [commands].
---

# [Team] [Workflow]

## When to Use
[Team-specific triggers]

## Integration with CCPM
[Commands, hooks, skills]

## Instructions
[Team-specific steps]

## Examples
[Team-specific scenarios]
```

### Template 2: Safety Enforcement Skill

**Purpose**: Add additional safety checks

```yaml
---
name: [company]-safety-[area]
description: Enforces [company] safety rules for [area]. Blocks [dangerous operations]. Requires confirmation for [external writes].
allowed-tools: read-file, grep  # Read-only
---

# [Company] Safety - [Area]

## When to Use
Auto-activates for [risky operations]

## Safety Rules
⛔ NEVER: [prohibited actions]
✅ ALWAYS: [required steps]

## Integration with CCPM
Works with external-system-safety

## Instructions
[Safety enforcement steps]
```

### Template 3: Integration Skill

**Purpose**: Integrate with custom tools

```yaml
---
name: [company]-[tool]-integration
description: Integrates CCPM with [company's internal tool]. Syncs [data] between Linear and [tool].
---

# [Company] [Tool] Integration

## When to Use
When syncing with [tool]

## Integration with CCPM
[Which commands trigger sync]

## Instructions
[Integration workflow]

## API Details
[Tool-specific API usage]
```

## Best Practices for Skill Creation

### Do's

- ✅ Use clear, descriptive skill names
- ✅ Include comprehensive trigger phrases
- ✅ Reference CCPM commands explicitly
- ✅ Follow CCPM safety rules
- ✅ Add concrete examples
- ✅ Document external system writes
- ✅ Test skill activation

### Don'ts

- ❌ Create overly broad skills
- ❌ Duplicate existing CCPM functionality
- ❌ Skip safety considerations
- ❌ Forget to document CCPM integration
- ❌ Use vague descriptions
- ❌ Hardcode company-specific values
- ❌ Ignore allowed-tools restrictions

## Skill Naming Conventions

### CCPM-Specific Skills

Prefix with `ccpm-`:
- `ccpm-code-review`
- `ccpm-debugging`
- `ccpm-mcp-management`

### Team-Specific Skills

Prefix with team/company name:
- `acme-deployment`
- `engineering-oncall`
- `mobile-release`

### Project-Specific Skills

Store in `.claude/skills/` (not plugin):
- `ecommerce-checkout`
- `auth-migration`
- `analytics-pipeline`

## Integration Patterns

### Pattern 1: Command Integration

**Skill activates alongside CCPM command**:

```yaml
---
name: team-pr-template
description: Adds team-specific PR template when running /ccpm:done
---

# Team PR Template

## Integration with CCPM

Works with `/ccpm:done`:
1. CCPM creates base PR
2. This skill adds team-specific template
3. Template includes:
   - Testing checklist
   - Security review
   - Performance impact
   - Documentation updates
```

### Pattern 2: Hook Complement

**Skill provides context for hook**:

```yaml
---
name: team-tdd-guide
description: Provides team-specific TDD guidance when tdd-enforcer hook blocks writes
---

# Team TDD Guide

## Integration with CCPM

Complements `tdd-enforcer` hook:
- Hook: Blocks write without tests
- This skill: Explains team's TDD patterns
- Together: Enforcement + education
```

### Pattern 3: Safety Layer

**Skill adds extra safety checks**:

```yaml
---
name: fintech-compliance
description: Enforces financial compliance rules on top of CCPM safety rules
---

# FinTech Compliance

## Integration with CCPM

Works with `external-system-safety`:
- external-system-safety: Confirms all external writes
- This skill: Adds finance-specific checks
  - Audit logging required
  - Dual approval for prod changes
  - Compliance documentation
```

## Examples

### Example 1: Creating Deployment Skill

```
User: "Create a skill for our deployment workflow"

Claude: [ccpm-skill-creator activates]

I'll help you create a custom deployment skill.

Questions:
1. What deployment environments do you have?
2. What checks are required before deployment?
3. Who should be notified on deployment?
4. Any external systems to update?

[After gathering requirements]

Creating skill: acme-deployment

Files created:
✅ skills/acme-deployment/SKILL.md
✅ skills/acme-deployment/checklist.md
✅ skills/acme-deployment/environments.md

Skill includes:
- Environment-specific workflows (staging vs prod)
- Pre-deployment checklist
- Slack notification integration
- Jira status updates
- Safety confirmations for production

Test the skill by saying: "Deploy to staging"

Would you like to review the skill before using it?
```

### Example 2: Creating Team Workflow

```
User: "Create a skill for our code review process"

Claude: [ccpm-skill-creator activates]

Creating team code review skill...

I see CCPM already has `ccpm-code-review` for verification.
Your custom skill can add team-specific practices on top.

Template created:
```yaml
---
name: acme-code-review
description: Acme Corp code review standards. Adds team-specific checks to ccpm-code-review. Requires architecture review for database changes, security review for auth code, and performance review for critical paths.
---

# Acme Code Review Standards

## Integration with CCPM

Extends `ccpm-code-review` with team rules:
- Database changes → Architecture review required
- Auth code → Security review required
- Critical path → Performance review required

## Instructions

[Team-specific review criteria]
```

Would you like to add more team-specific rules?
```

## Skill Distribution

### Team Skills (Version Control)

```bash
# Store in project repository
git add .claude/skills/team-deployment/
git commit -m "Add team deployment skill"
git push

# Team members get skill automatically
git pull  # Skill now available
```

### Company Skills (Shared Repository)

```bash
# Create shared skills repository
# company-claude-skills/
# ├── deployment/
# ├── security/
# └── integration/

# Team members symlink or copy
ln -s ~/company-claude-skills/* ~/.claude/skills/
```

### Community Skills (Plugin)

```bash
# Package as Claude Code plugin
# .claude-plugin/
# ├── plugin.json
# └── skills/
#     └── your-skill/

# Publish to Claude Code marketplace
# Others can install via Claude Code
```

## Summary

This skill helps you:

- ✅ Create custom CCPM skills
- ✅ Follow CCPM conventions
- ✅ Integrate with commands/hooks
- ✅ Enforce safety rules
- ✅ Share with team
- ✅ Build extensible PM workflows

**Philosophy**: Codify team knowledge, make workflows repeatable, extend CCPM for your needs.

---

**Source**: Adapted from [claudekit-skills/skill-creator](https://github.com/mrgoonie/claudekit-skills)
**License**: MIT
**CCPM Integration**: Skill development, team customization, community contributions
