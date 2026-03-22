---
name: af-agentflow-framework-development
description: Use when creating or modifying AgentFlow framework components - agents, skills, commands, hooks, modules, or documentation structure. Covers V2 architecture patterns, namespace rules, skill/agent templates, module registry, and framework documentation standards.

# AgentFlow documentation fields
title: AgentFlow Framework Development
created: 2025-12-03
updated: 2026-02-20
last_checked: 2026-02-20
tags: [skill, expertise, framework, development, meta, modules]
parent: ../README.md
---

# AgentFlow Framework Development

## When to Use This Skill

Load this skill when you need to:
- Create or modify agents, skills, commands, or hooks
- Add or modify modules in the module registry
- Create integration guides for cross-module concerns
- Create or update module validation specs
- Understand framework component structure and V2 architecture
- Apply namespace rules and documentation standards

## Rules (FOLLOW THESE)

### Namespace Rules
1. **All framework components** use `af-` prefix (agents, skills, commands)
2. **Project-specific components** never use `af-` prefix
3. **Never mix** framework and project components in same file

### Documentation Rules
4. **All framework files** require complete frontmatter (title, created, updated, tags, parent)
5. **Bidirectional linking** is mandatory - parent lists children, child references parent
6. **Run docs-quality-agent** after any framework changes
7. **Update dates** when modifying files (updated, last_checked)

### Size Rules
8. **Agents must be lightweight** (~50 lines of procedure)
9. **Skills must be directive** (rules + workflows, not reference dumps)
10. **Skills must be under 300 lines** (target: 150-200)
11. **Skills link to comprehensive docs** for depth

### Structure Rules
12. **Agents reference skills** for domain knowledge (use backticks: `af-skill-name`)
13. **Agents have clear I/O** specifications (inputs, outputs)
14. **Skills use MUST/SHOULD/MAY** directives for clarity
15. **Commands validate arguments** and provide usage examples

### Validation Rules
16. **Test components** before considering them complete
17. **Validate documentation** with scripts (frontmatter, links)
18. **Restart Claude Code** after creating new skills
19. **Verify invocation** for agents and commands

### Module Rules
20. **All modules** are declared in `docs/reference/module-registry.yml`
21. **Core modules** are always installed (agentflow, linear, git, documentation, doppler)
22. **Optional modules** are selected during Discovery and installed before Refinement
23. **Every module** must have: `name`, `description`, `skill`, `validation_spec`, `depends_on`
24. **Integration guides** are created when two modules interact (e.g., cognito + SES)
25. **Validation specs** are Playwright tests in `templates/setup/validation/specs/`
26. **Run `validate-module-registry.ts`** after any registry change (169+ checks)

---

## Workflows

### Workflow: Adding a New Agent

**When:** You need a specialized subagent for a specific domain

**Steps:**
1. Create file: `.claude/agents/af-<domain>-agent.md`
2. Add frontmatter with `name`, `description`, `tools`, `title`, dates, tags, parent
3. Write procedure: Role, Skills Used, Inputs, Procedure, Outputs, Error Handling
4. Keep procedure ~50 lines (load skills, don't duplicate knowledge)
5. Update `.claude/agents/README.md` children array
6. Validate: `npx ts-node .claude/scripts/validate-frontmatter.ts`
7. Test invocation: `Task tool → subagent_type="af-<domain>-agent"`
8. Run docs-quality-agent for comprehensive validation

**Success criteria:**
- ✅ Agent has complete frontmatter and bidirectional links
- ✅ Agent loads skills for domain knowledge
- ✅ Agent can be invoked successfully
- ✅ Validation scripts pass

---

### Workflow: Creating a New Skill

**When:** You need to package domain knowledge for reuse

**Steps:**
1. Create directory: `.claude/skills/af-<name>/`
2. Create file: `.claude/skills/af-<name>/SKILL.md`
3. Add frontmatter with `name`, `description`, `type`, `domain`, dates, tags
4. Structure content: When to Use, Rules (15-20), Workflows (4-5), Examples, Essential Reading
5. Keep under 300 lines (target: 150-200) - move details to comprehensive guide
6. Create guide if needed: `.claude/docs/guides/<domain>-guide.md` (800-1500 lines)
7. Update `.claude/skills/README.md` children array
8. Validate: `npx ts-node .claude/scripts/validate-links.ts`
9. Restart Claude Code session to pick up new skill
10. Test with agent that loads the skill

**Success criteria:**
- ✅ Skill is directive (workflows, rules, examples)
- ✅ Skill is under 300 lines
- ✅ Skill links to comprehensive docs (if needed)
- ✅ Agents can load and use skill successfully

---

### Workflow: Adding a Slash Command

**When:** You need a discoverable entry point for a workflow

**Steps:**
1. Determine category: framework (`/af:`), task (`/task:`), phase-specific
2. Create file: `.claude/commands/<category>/<action>.md`
3. Add frontmatter with `description` (shows in autocomplete), dates, tags
4. Write command body: usage, examples, the prompt that executes
5. Use `$1`, `$2` for positional args or `$ARGUMENTS` for all args
6. Update `.claude/commands/<category>/README.md` children array
7. Test: `/<category>:<action>` should autocomplete and execute
8. Verify arguments work correctly

**Success criteria:**
- ✅ Command appears in autocomplete
- ✅ Command expands and executes correctly
- ✅ Arguments are handled properly
- ✅ Listed in category README

---

### Workflow: Configuring a Hook

**When:** You need automated behavior on specific events

**Steps:**
1. Identify trigger: PreToolUse, PostToolUse, Stop, SubagentStop
2. Create script (if command type): `.claude/hooks/<name>.sh`
3. Write hook logic using hook variables ($TOOL_NAME, $ARGUMENTS, etc.)
4. Configure in `settings.json` with matcher and hook type
5. Test hook fires on correct event
6. Verify output is clear and helpful
7. Document in `.claude/hooks/README.md`

**Success criteria:**
- ✅ Hook fires on correct event
- ✅ Hook provides clear feedback
- ✅ Hook doesn't cause unintended side effects
- ✅ Hook is documented

---

### Workflow: Adding a New Module

**When:** A new technology/concern needs to be installable via the setup process

**Steps:**
1. Choose the right category section in `docs/reference/module-registry.yml`
2. Add the module entry with all required fields:
   ```yaml
   - name: my-module
     description: One-line description of what this module provides
     skill: af-relevant-expertise     # Existing skill for this domain
     guide: guides/path/to-guide.md   # Setup guide (optional for simple modules)
     validation_spec: my-module.spec.ts
     depends_on:
       - git                          # List dependencies
     integrations:                    # Cross-module integration guides (optional)
       - when: [my-module, other-module]
         guide: guides/integrations/my-other.md
   ```
3. Create validation spec: `templates/setup/validation/specs/my-module.spec.ts`
   - Follow existing spec patterns (check CLI tools, config files, project structure)
   - Use `test.todo()` for tests that need external services (never `test.skip()`)
4. Add project entry to `templates/setup/validation/playwright.config.ts`
5. Update `templates/setup/validation/package.json` test scripts
6. Create integration guides if this module interacts with others (see next workflow)
7. Run validation: `npx ts-node scripts/validation/validate-module-registry.ts`
8. If adding a combination, add it under the `combinations:` section

**Success criteria:**
- Registry validation passes (all checks green)
- Validation spec exists and runs against a test project
- Dependencies are correctly declared
- Integration guides exist for all declared integrations

---

### Workflow: Creating an Integration Guide

**When:** Two modules interact and need cross-cutting setup knowledge

**Steps:**
1. Create file: `docs/guides/integrations/<module-a>-<module-b>.md`
2. Add frontmatter (title, created, updated, tags, parent)
3. Structure content:
   - **Problem**: What goes wrong without this guide
   - **Solution**: Step-by-step configuration
   - **Verification**: How to confirm it works
4. Reference the guide in module-registry.yml under `integrations`:
   ```yaml
   integrations:
     - when: [module-a, module-b]
       guide: guides/integrations/module-a-module-b.md
   ```
5. Update `docs/guides/integrations/README.md` children array
6. Run registry validation to confirm guide file exists

**Success criteria:**
- Guide explains the cross-cutting concern clearly
- Referenced in module-registry.yml under correct module(s)
- Listed in integrations README

---

### Workflow: Creating a Module Validation Spec

**When:** A module needs a Playwright spec to verify its setup

**Steps:**
1. Create file: `templates/setup/validation/specs/<module-name>.spec.ts`
2. Import from `@playwright/test` and use `test.describe('<module-name> module', ...)`
3. Read `PROJECT_ROOT` from environment for file path assertions
4. Test categories:
   - **CLI tools**: Verify required CLIs are installed (`which <tool>`)
   - **Config files**: Verify required files exist in project
   - **Project structure**: Verify directories and conventions
   - **External services**: Verify accounts/configs (use `test.todo()` if fragile — never `test.skip()`)
5. Add to `playwright.config.ts`:
   ```typescript
   { name: 'my-module', testMatch: 'specs/my-module.spec.ts' },
   ```
6. Add test script to `package.json`:
   ```json
   "test:my-module": "npx playwright test --project=my-module"
   ```
7. Test against a real project: `PROJECT_ROOT=/path/to/project npm run test:my-module`

**Success criteria:**
- Spec runs and produces clear pass/fail results
- Core module specs always pass on any AgentFlow project
- Optional module specs pass only when that module is installed
- Graceful skips for tests requiring external services

---

## Examples

### Good Example: Lightweight Agent

```markdown
## Procedure

1. **MUST load expertise skill**
   Load `af-bdd-expertise` skill for scenario patterns

2. **MUST read Linear issue**
   Extract requirements and acceptance criteria

3. **MUST transform to Markdown scenarios**
   Follow skill workflow: "Creating Scenarios from Refinement"
   Apply glossary compliance rules

4. **SHOULD validate output**
   Check coverage and test type classification
```

**Why this is good:**
- Agent is thin (~30 lines)
- Loads skill for domain knowledge
- Clear MUST/SHOULD directives
- References skill workflows

### Bad Example: Heavy Agent

```markdown
## Procedure

1. Understand scenario syntax:
   Preconditions: initial state
   Steps: user actions
   [200 lines of scenario reference...]

2. Check glossary for approved terms
   [100 lines explaining glossary...]
```

**Why this is bad:**
- Agent contains reference material (should be in skill)
- No skill loading
- Too verbose (~400 lines)
- Knowledge baked in instead of reusable

---

### Good Example: Directive Skill

```markdown
## Rules (FOLLOW THESE)
1. All test files must end in `.test.ts` or `.spec.ts`
2. Never mock internal code - only external dependencies
3. Tests must be independent (no shared state)

## Workflows
### Workflow: Writing Unit Tests from BDD
1. Read BDD scenario Given/When/Then
2. Create test file: `<feature>.test.ts`
3. Write describe block matching Feature name
4. Write it block for each Scenario
5. Implement Given (setup), When (action), Then (assertions)
6. Run tests: `npm test`
```

**Why this is good:**
- Rules up front
- Step-by-step workflow
- Actionable directives
- Under 200 lines

### Bad Example: Reference-Heavy Skill

```markdown
## Testing in TypeScript

TypeScript provides excellent support for testing...

[500 lines explaining testing concepts, frameworks, patterns...]

Jest is a popular choice because...
Mocha is another option...
```

**Why this is bad:**
- Reads like documentation, not directives
- No clear workflows
- Too long (500+ lines)
- Claude treats as "background reading" and may skip

---

## Essential Reading

**Comprehensive framework development guide:**
- [Framework Development Guide](../../docs/guides/framework-development-guide.md) - Complete guide to creating agents, skills, commands, hooks (1700+ lines)

**Module system:**
- [Module Registry](../../docs/reference/module-registry.yml) - All modules, dependencies, integrations
- [Integration Guides](../../docs/guides/integrations/README.md) - Cross-module setup knowledge
- [Validation Specs](../../templates/setup/validation/specs/) - Playwright module validation tests
- [Registry Validator](../../scripts/validation/validate-module-registry.ts) - 169+ automated checks

**Architecture and standards:**
- [Documentation Standards](../../docs/standards/documentation-standards.md) - Frontmatter and linking requirements
- [Framework Architecture](../../docs/architecture/README.md) - V2 architecture overview
- [Project Structure](../../docs/standards/project-structure.md) - Where files go

**Claude Code official docs:**
- [Skills](https://code.claude.com/docs/en/skills) - Official skills documentation
- [Sub-agents](https://code.claude.com/docs/en/sub-agents) - Official agents documentation
- [Slash Commands](https://code.claude.com/docs/en/slash-commands) - Official commands documentation
- [Hooks](https://code.claude.com/docs/en/hooks) - Official hooks documentation

---

**Remember:**
1. Framework components use `af-` prefix
2. Agents are lightweight, skills are directive
3. Comprehensive details go in guides
4. Always validate and test before considering complete
5. Run docs-quality-agent after framework changes
6. New modules need: registry entry, validation spec, playwright config, package.json script
7. Run `validate-module-registry.ts` after any registry changes
