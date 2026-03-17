---
name: slashcommandcreator
description: Autonomous meta-skill for creating high-quality custom slash commands using 5-phase workflow with multi-agent validation and quality gates. Use when user requests new slash command, reusable prompt automation, or wants to convert repetitive workflows into documented commands.
version: 1.0.0
license: MIT
model: claude-opus-4-5
trigger: SlashCommandCreator
---

# SlashCommandCreator Skill

## Purpose

Create production-ready custom slash commands following ai-agents quality standards.

## Triggers

- `create slash command for [purpose]`
- `SlashCommandCreator: [description]`
- `design slash command that [does something]`

## When to Use

- User requests "create slash command for [purpose]"
- Repetitive prompts identified in workflow
- Converting manual workflows to automation
- Need reusable, documented command patterns

## 5-Phase Workflow

### Phase 1: Discovery & Analysis

**Agent Mode**: Analyst

**Tasks**:

1. Clarify user intent: What prompt is being repeated?
2. Search existing commands: `ls .claude/commands/**/*.md`
3. Decision: Slash command vs skill (see decision matrix in CLAUDE.md)
4. Apply 11 thinking models from skillcreator framework
5. Document findings in `.agents/analysis/slashcommand-[name]-analysis.md`

**Deliverable**: Analysis document with recommendation

### Phase 2: Design

**Agent Mode**: Architect

**Tasks**:

1. Command naming (namespace conventions)
2. Argument design:
   - Simple commands: use `$ARGUMENTS`
   - Complex commands: use `$1`, `$2`, `$3` (positional)
3. Frontmatter schema:
   - `description` (trigger-based per creator-001)
   - `argument-hint` (if using arguments)
   - `allowed-tools` (if using bash commands with `!` or file references with `@`)
   - `model` (opus for complex reasoning)
   - `disable-model-invocation` (if pure prompt template)
4. Dynamic context evaluation:
   - Bash execution (`!git log --oneline -5`)
   - File references (`@.agents/HANDOFF.md`)
5. Extended thinking evaluation:
   - Add `ultrathink` keyword for complex reasoning (>5 steps)
   - Token budget consideration (<31,999 tokens)

**Deliverable**: Design specification with frontmatter + prompt

### Phase 3: Multi-Agent Validation

**Agent Mode**: Orchestrator (coordinates 4 agents)

**Agents**:

1. **Security**:
   - Review `allowed-tools` constraints
   - Flag overly permissive wildcards
   - Verify bash commands are safe

2. **Architect**:
   - Check for duplication (similar existing commands)
   - Verify appropriate scope (not too broad/narrow)
   - Validate namespace conventions

3. **Independent-Thinker**:
   - Challenge necessity: Is this really needed?
   - Propose alternatives
   - Question assumptions

4. **Critic**:
   - Frontmatter completeness check
   - Trigger-based description validation
   - Argument-hint clarity

**Unanimous Approval Required**: All 4 agents must approve.

<!-- WHY: Ensures no single agent dimension (security, scope, necessity, completeness)
     is overlooked. Prevents security vulnerabilities from passing due to focus on
     functionality alone. Pattern proven by skillcreator 3.2.0 multi-agent synthesis. -->

**Invocation Pattern**:

```python
# Security review
Task(subagent_type="security", prompt="Review allowed-tools for command: [spec]")

# Architecture review
Task(subagent_type="architect", prompt="Check for duplication: [spec]")

# Challenge necessity
Task(subagent_type="independent-thinker", prompt="Is this command truly needed? [spec]")

# Frontmatter completeness
Task(subagent_type="critic", prompt="Validate frontmatter completeness: [spec]")
```

**Deliverable**: Validation report with approvals or revision requests

### Phase 4: Implementation

**Agent Mode**: Implementer

**Tasks**:

1. Run `python3 .claude/skills/slashcommandcreator/scripts/new_slash_command.py`
2. Create `.claude/commands/[namespace]/[command].md`
3. Write frontmatter + prompt body
4. Test invocation with sample arguments
5. Update command catalog (if exists)

**Deliverable**: Working slash command file

### Phase 5: Quality Gates (Automatic)

**Agent Mode**: Implementer (automatic validation)

**Tasks**:

1. Run `python3 .claude/skills/slashcommandcreator/scripts/validate_slash_command.py --path [file]`
2. Fix violations if any
3. Re-run validation until exit code 0
4. Commit with conventional commit message

**Deliverable**: Validated slash command ready for use

## Invocation Examples

```text
SlashCommandCreator: create command for exporting Forgetful memories to JSON

SlashCommandCreator: design slash command for running security audit

create slash command that summarizes recent PR comments
```

## Decision Matrix: Slash Command vs Skill

**Use Slash Command When**:

- Prompt is <200 lines
- No multi-step conditional logic
- Simple argument substitution
- No external script orchestration

**Use Skill When**:

- Prompt is >200 lines
- Multi-agent coordination required
- Complex scripting logic
- Requires dedicated tests

## Verification/Success Criteria

Before marking complete:

- [ ] Frontmatter has `description` (trigger-based)
- [ ] Frontmatter has `argument-hint` (if uses arguments)
- [ ] Frontmatter has `allowed-tools` (if uses bash/file refs)
- [ ] No overly permissive wildcards in `allowed-tools`
- [ ] Description follows trigger-based pattern (creator-001)
- [ ] File is <200 lines (or converted to skill)
- [ ] Passes `markdownlint-cli2` validation
- [ ] Passes `validate_slash_command.py` validation
- [ ] Tested with sample arguments
- [ ] Committed with conventional commit message

**Success Criteria:**

| Metric | Target |
|--------|--------|
| Validation | Exit code 0 from validate_slash_command.py |
| Testing | Command runs without errors with sample arguments |
| Documentation | Description clearly explains when to use command |
| Security | All bash/file refs have explicit allowed-tools entries |

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Creating commands > 200 lines | Too complex for slash command format | Convert to a skill instead |
| Overly permissive `allowed-tools` wildcards | Security risk | List specific tools needed |
| Skipping multi-agent validation | Miss security, scope, or necessity issues | Run all 4 validation agents |
| Duplicate commands for similar purposes | Confusing discoverability | Check existing commands first |
| Generic description without trigger keywords | Model cannot find the command | Include specific "Use when" phrases |

## Quality Gates Checklist

All checks from Verification section plus:

- [ ] Multi-agent approval (security, architect, independent-thinker, critic)
- [ ] No duplication with existing commands
- [ ] Appropriate scope (not too broad/narrow)
- [ ] Frontmatter completeness validated

## Scripts

### new_slash_command.py

Creates a new slash command from a template.

```bash
python3 .claude/skills/slashcommandcreator/scripts/new_slash_command.py --name <name> --description <desc>
```

### validate_slash_command.py

Validates slash command structure and frontmatter.

```bash
python3 .claude/skills/slashcommandcreator/scripts/validate_slash_command.py <skill-dir>
```

## References

- `.agents/analysis/custom-slash-commands-research.md`
- `.agents/planning/slashcommandcreator-skill-spec.md`
- `.serena/memories/slashcommand-best-practices.md`
