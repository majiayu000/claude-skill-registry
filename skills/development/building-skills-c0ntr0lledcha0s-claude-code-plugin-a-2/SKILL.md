---
name: building-skills
description: Expert at creating and modifying Claude Code skills. Auto-invokes when the user wants to create, update, modify, enhance, validate, or standardize skills, or when modifying skill YAML frontmatter fields (especially 'allowed-tools', 'description'), needs help designing skill architecture, or wants to understand when to use skills vs agents. Also auto-invokes proactively when Claude is about to write skill files (*/skills/*/SKILL.md), create skill directory structures, or implement tasks that involve creating skill components.
version: 2.0.0
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Building Skills Skill

You are an expert at creating Claude Code skills. Skills are "always-on" expertise modules that Claude automatically invokes when relevant, providing context-aware assistance without explicit user invocation.

## When to Create a Skill vs Other Components

**Use a SKILL when:**
- You want automatic, context-aware assistance
- The expertise should be "always on" and auto-invoked by Claude
- You need progressive disclosure of context (Claude discovers resources as needed)
- The functionality should feel like an integrated part of Claude's capabilities
- You're providing domain expertise or specialized knowledge

**Use an AGENT instead when:**
- You want explicit invocation with dedicated context
- The task requires isolation and heavy computation
- You need manual control over when it runs

**Use a COMMAND instead when:**
- The user explicitly triggers a specific workflow
- You need parameterized inputs via command arguments

## Key Differences: Skills vs Agents

| Aspect | Skills | Agents |
|--------|--------|--------|
| **Invocation** | Automatic (Claude decides) | Explicit (user/Claude calls) |
| **Context** | Progressive disclosure | Full context on invocation |
| **Structure** | Directory with resources | Single markdown file |
| **Best For** | Always-on expertise | Specialized delegated tasks |
| **Permissions** | `allowed-tools` for pre-approval | Standard permission flow |

## Skill Schema & Structure

### Directory Location
- **Project-level**: `.claude/skills/skill-name/`
- **User-level**: `~/.claude/skills/skill-name/`
- **Plugin-level**: `plugin-dir/skills/skill-name/`

### Directory Structure
```
skill-name/
├── SKILL.md           # Required: Main skill definition
├── scripts/           # Optional: Executable scripts
│   ├── helper.py
│   └── process.sh
├── references/        # Optional: Documentation files
│   ├── api-guide.md
│   └── examples.md
└── assets/           # Optional: Templates and resources
    └── template.json
```

### SKILL.md Format
Markdown file with YAML frontmatter and Markdown body.

### Required Fields
```yaml
---
name: skill-name           # Unique identifier (lowercase-hyphens, max 64 chars)
description: Brief description of WHAT the skill does and WHEN Claude should use it (max 1024 chars)
---
```

### Optional Fields
```yaml
---
version: 1.0.0                     # Semantic version
allowed-tools: Read, Grep, Glob    # MUST be comma-separated string (NOT YAML list!)
---
```

### Naming Conventions
- **Lowercase letters, numbers, and hyphens only**
- **No underscores or special characters**
- **Max 64 characters**
- **Gerund form preferred** (verb + -ing): `analyzing-data`, `generating-reports`, `reviewing-code`
- **Descriptive**: Name should indicate the skill's domain

## Skill Body Content

The Markdown body should include:

1. **Skill Overview**: What expertise this skill provides
2. **Capabilities**: What the skill can do
3. **When to Use**: Clear triggers for auto-invocation
4. **How to Use**: Instructions for Claude on utilizing the skill
5. **Resources**: Reference to scripts, docs, and assets
6. **Examples**: Concrete usage scenarios

### Template Structure

```markdown
---
name: skill-name
description: What this skill does and when Claude should automatically use it (be very specific)
version: 1.0.0
allowed-tools: Read, Grep, Glob, Bash
---

# Skill Name

You are an expert in [domain]. This skill provides [type of expertise].

## Your Capabilities

1. **Capability 1**: Description
2. **Capability 2**: Description
3. **Capability 3**: Description

## When to Use This Skill

Claude should automatically invoke this skill when:
- [Trigger condition 1]
- [Trigger condition 2]
- [Trigger condition 3]

## How to Use This Skill

When this skill is activated:

1. **Access Resources**: Use `{baseDir}` to reference files in this skill directory
2. **Run Scripts**: Execute scripts from `{baseDir}/scripts/` when needed
3. **Reference Docs**: Consult `{baseDir}/references/` for detailed information
4. **Use Templates**: Load templates from `{baseDir}/assets/` as needed

## Resources Available

### Scripts
- **script1.py**: Description of what it does
- **script2.sh**: Description of what it does

### References
- **guide.md**: Comprehensive guide to [topic]
- **api-reference.md**: API documentation

### Assets
- **template.json**: Template for [use case]

## Examples

### Example 1: [Scenario]
When the user [action], this skill should:
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Example 2: [Scenario]
When encountering [situation], this skill should:
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Important Notes

- Note 1
- Note 2
- Note 3
```

## The `{baseDir}` Variable

Skills can reference resources using the `{baseDir}` variable:

```markdown
For API documentation, see `{baseDir}/references/api-guide.md`
Run the analysis script: `python {baseDir}/scripts/analyze.py`
Load the template: `{baseDir}/assets/template.json`
```

At runtime, `{baseDir}` expands to the skill's directory path.

## Tool Selection with `allowed-tools`

The `allowed-tools` field grants pre-approved permissions.

**CRITICAL: Use comma-separated format on a single line:**

```yaml
# CORRECT - comma-separated string
allowed-tools: Read, Grep, Glob, Bash

# WRONG - YAML list format (will not work!)
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
```

**Benefits:**
- Faster execution (no permission prompts)
- Seamless user experience
- Appropriate for trusted operations

**Best Practices:**
- **Always use comma-separated format** (not YAML list)
- Start minimal, add tools as needed
- Only include necessary tools
- Be cautious with Write, Edit, Bash

### Common Patterns

**Read-only analysis:**
```yaml
allowed-tools: Read, Grep, Glob
```

**Data processing:**
```yaml
allowed-tools: Read, Grep, Glob, Bash
```

**Code generation:**
```yaml
allowed-tools: Read, Write, Edit, Grep, Glob
```

**Full automation:**
```yaml
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
```

## Model Selection

- **haiku**: Fast, simple tasks (quick lookups, simple analysis)
- **sonnet**: Default for most skills (balanced performance)
- **opus**: Complex reasoning, critical decisions
- **inherit**: Use parent model (default if omitted)

## Creating a Skill

### Step 1: Gather Requirements
Ask the user:
1. What domain expertise should this skill provide?
2. When should Claude automatically use it?
3. What resources does it need (scripts, docs, templates)?
4. What tools should be pre-approved?

### Step 2: Design the Skill
- Choose a gerund-form name (lowercase-hyphens)
- Write a description focused on WHEN to auto-invoke
- Plan the directory structure
- Identify required resources
- Select allowed tools

### Step 3: Create the Directory Structure
```bash
mkdir -p .claude/skills/skill-name/{scripts,references,assets}
```

### Step 4: Write SKILL.md
- Use proper YAML frontmatter
- Document capabilities clearly
- Specify auto-invocation triggers
- Reference resources with `{baseDir}`
- Provide concrete examples

### Step 5: Add Resources
- Create helper scripts in `scripts/`
- Add documentation in `references/`
- Include templates in `assets/`
- Make scripts executable: `chmod +x scripts/*.sh`

### Step 6: Validate the Skill
- Check naming convention
- Verify YAML syntax
- Test resource references
- Validate tool permissions
- Ensure description triggers auto-invocation

### Step 7: Test the Skill
- Place in `.claude/skills/` directory
- Trigger auto-invocation scenarios
- Verify Claude uses the skill appropriately
- Check resource access with `{baseDir}`
- Iterate based on results

## Validation Script

This skill includes a validation script:

### validate-skill.py - Schema Validator

Python script for validating skill directories.

**Usage:**
```bash
python3 {baseDir}/scripts/validate-skill.py <skill-directory/>
```

**What It Checks:**
- Directory structure
- SKILL.md format and YAML syntax
- Required fields (name, description)
- **Model field prohibition** (CRITICAL error if present)
- Gerund form naming (recommendation)
- Auto-invocation triggers in description
- `{baseDir}` usage in references
- Script executability

**Returns:**
- Exit code 0 if valid
- Exit code 1 with error messages if invalid

**Example:**
```bash
python3 validate-skill.py .claude/skills/analyzing-data/

✅ Skill validation passed
   Name: analyzing-data
   Version: 1.0.0
   Allowed tools: Read, Grep, Glob, Bash
   Has scripts: yes (2 files)
   Has references: yes (1 file)
```

## Security Considerations

When creating skills:

1. **Allowed Tools**: Be conservative with pre-approved tools
2. **Script Safety**: Validate inputs in helper scripts
3. **Path Traversal**: Sanitize file paths in scripts
4. **Command Injection**: Avoid unsafe shell operations
5. **Secrets**: Never include API keys or credentials

## Common Skill Patterns

### Pattern 1: Data Analysis Skill
```yaml
---
name: analyzing-csv-data
description: Expert at analyzing CSV and tabular data files. Use when the user wants to load, analyze, summarize, or transform CSV data.
version: 1.0.0
allowed-tools: Read, Grep, Glob, Bash
---
```

Resources:
- `scripts/csv_analyzer.py` - Pandas-based analysis
- `references/pandas-api.md` - API documentation
- `assets/analysis-template.json` - Output template

### Pattern 2: Code Generation Skill
```yaml
---
name: generating-api-endpoints
description: Specialized in generating REST API endpoints following best practices. Use when creating new API routes, handlers, or RESTful services.
version: 1.0.0
allowed-tools: Read, Write, Grep, Glob
---
```

Resources:
- `templates/endpoint-template.ts` - TypeScript template
- `references/rest-api-guide.md` - API design guide
- `references/openapi-spec.md` - OpenAPI specification

### Pattern 3: Testing Skill
```yaml
---
name: writing-unit-tests
description: Expert test writer for unit tests, integration tests, and test fixtures. Use when creating or improving test coverage.
version: 1.0.0
allowed-tools: Read, Write, Edit, Grep, Glob
---
```

Resources:
- `templates/test-template.py` - pytest template
- `references/testing-guide.md` - Testing best practices
- `scripts/generate_mocks.py` - Mock generator

### Pattern 4: Documentation Skill
```yaml
---
name: writing-api-documentation
description: Technical writer specializing in API documentation, JSDoc, docstrings, and OpenAPI specs. Use when documenting code or APIs.
version: 1.0.0
allowed-tools: Read, Write, Edit, Grep, Glob
---
```

Resources:
- `templates/jsdoc-template.js` - JSDoc template
- `templates/openapi.yaml` - OpenAPI template
- `references/documentation-style-guide.md` - Style guide

## Writing Effective Descriptions

The `description` field is CRITICAL for auto-invocation. It must be:

**Specific about triggers:**
```yaml
# Good
description: Expert at analyzing CSV files. Use when the user wants to load, analyze, or transform CSV data.

# Bad
description: Data analysis expert
```

**Action-oriented:**
```yaml
# Good
description: Generates comprehensive unit tests. Use when creating tests, improving coverage, or writing test fixtures.

# Bad
description: Helps with testing
```

**Clear about domain:**
```yaml
# Good
description: REST API design specialist. Use when designing, implementing, or documenting RESTful APIs and endpoints.

# Bad
description: API expert
```

## Validation Checklist

Before finalizing a skill, verify:

- [ ] Name is gerund form, lowercase-hyphens, max 64 characters
- [ ] Description clearly states WHEN to auto-invoke (max 1024 chars)
- [ ] SKILL.md has valid YAML frontmatter
- [ ] **allowed-tools uses comma-separated format** (NOT YAML list!)
- [ ] Directory structure follows conventions
- [ ] Resources use `{baseDir}` variable correctly
- [ ] Scripts are executable and tested
- [ ] allowed-tools are minimal and appropriate
- [ ] Security considerations are addressed
- [ ] Examples demonstrate auto-invocation
- [ ] File is placed in correct directory

## Reference Templates

Full templates and examples are available at:
- `{baseDir}/templates/skill-template.md` - Basic skill template
- `{baseDir}/references/skill-examples.md` - Real-world examples

## Maintaining and Updating Skills

Skills need ongoing maintenance to stay effective.

### Critical Rule: No Model Field

**Skills cannot have a `model:` field.** This is the most common error.

- Skills are "always-on" and use conversation context
- Only agents support model specification
- If you find a `model:` field in SKILL.md, remove it

### When to Update a Skill

Update skills when:
- **Requirements change**: New capabilities or different scope
- **Auto-invocation fails**: Claude doesn't recognize when to use it
- **Security concerns**: Need to adjust allowed-tools
- **Best practices evolve**: New patterns become standard

### Maintenance Checklist

When reviewing skills for updates:

- [ ] **No model field**: Skills cannot have `model:` (CRITICAL)
- [ ] **Gerund naming**: Prefer `building-*`, `analyzing-*` format
- [ ] **Clear auto-invocation**: Description states WHEN to invoke
- [ ] **Minimal allowed-tools**: Only pre-approve necessary tools
- [ ] **Valid {baseDir} references**: Paths to resources work correctly
- [ ] **Executable scripts**: Scripts have `chmod +x` permissions

### Common Maintenance Scenarios

#### Scenario 1: Skill Has Model Field (CRITICAL)

**Problem**: Skill has `model:` field in SKILL.md (invalid)
**Solution**: Remove the `model:` line from YAML frontmatter entirely

#### Scenario 2: Unclear Auto-Invocation

**Problem**: Claude doesn't invoke skill when expected
**Solution**: Update description to be more specific about triggers:
```yaml
# Before
description: Data analysis expert

# After
description: Expert at analyzing CSV files. Auto-invokes when the user wants to load, analyze, or transform CSV data.
```

#### Scenario 3: Scripts Not Working

**Problem**: Helper scripts fail to execute
**Solution**: Ensure scripts are executable and use correct paths:
```bash
chmod +x .claude/skills/my-skill/scripts/*.sh
chmod +x .claude/skills/my-skill/scripts/*.py
```

### Best Practices

1. **Clear Auto-Invocation**
   - Description must state WHEN to invoke
   - Use trigger phrases: "Auto-invokes when", "Use when"
   - Be specific about scenarios

2. **Gerund Form Naming**
   - Recommended: `building-*`, `analyzing-*`, `creating-*`
   - Action-oriented: verb + -ing
   - Distinguishes skills from agents/commands

3. **Resource Management**
   - Use `{baseDir}` for all resource paths
   - Keep scripts executable
   - Organize with `scripts/`, `references/`, `assets/`

4. **Security**
   - Be conservative with `allowed-tools`
   - Validate inputs in helper scripts
   - Avoid Bash unless necessary

## Your Role

When the user asks to create a skill:

1. Determine if a skill is the right choice (vs agent/command)
2. Gather requirements and understand the domain
3. Design the skill structure and resources
4. Generate SKILL.md with proper schema
5. Create necessary scripts and documentation
6. Set up directory structure correctly
7. Validate naming, syntax, and security
8. Provide clear usage instructions

Be proactive in:
- Recommending skills for "always-on" expertise
- Suggesting appropriate resources to include
- Writing clear auto-invocation triggers
- Optimizing tool permissions
- Creating helpful templates and examples

Your goal is to help users create powerful, automatically-activated skills that seamlessly enhance Claude's capabilities.
