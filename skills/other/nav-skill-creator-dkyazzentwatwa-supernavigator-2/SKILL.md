---
name: nav-skill-creator
description: Analyze codebase patterns and create custom skills for repetitive workflows. Use when project needs automation or pattern enforcement. Auto-invoke when user says "create a skill for...", "automate this workflow", or "we keep doing X manually".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
version: 1.0.0
---

# Navigator Skill Creator

Create project-specific skills by analyzing codebase patterns and automating repetitive workflows.

## When to Invoke

Auto-invoke when user mentions:
- "Create a skill for [pattern]"
- "Automate this workflow"
- "We keep doing X manually"
- "Enforce this pattern"
- "Generate boilerplate for [feature type]"
- "We need consistency for [task type]"

## What This Does

1. Analyzes codebase to understand project patterns
2. Identifies best practices from existing code
3. Generates skill with:
   - Auto-invocation triggers
   - Predefined functions
   - Templates
   - Examples
4. Tests the generated skill
5. Documents the new skill

## Execution Steps

### Step 1: Understand Skill Request

Ask clarifying questions:
- What pattern/workflow to automate?
- What triggers should invoke this skill?
- What output format is expected?
- Are there existing examples in the codebase?

**Example dialogue**:
```
User: "Create a skill for adding React components"
Assistant: "I'll analyze your codebase to understand React component patterns.
- What directory are components in?
- Do you use TypeScript or JavaScript?
- Do you want tests generated automatically?
- Are there style files (CSS/SCSS) per component?"
```

### Step 2: Analyze Codebase Patterns

**Use Task agent to explore** (saves 60-80% tokens):
```
Use Task agent with subagent_type=Explore:
"Find existing [pattern type] in codebase:
 - Locate all [files matching pattern]
 - Identify common structure
 - Extract best practices
 - Find configuration files
 - Return summary of findings"
```

**What to look for**:
- File naming conventions (kebab-case, PascalCase, etc.)
- Directory structure patterns
- Import/export patterns
- Testing patterns
- Configuration patterns
- Documentation patterns

**Example for React components**:
```
Task agent finds:
- Components in src/components/
- PascalCase naming (UserProfile.tsx)
- Co-located tests (UserProfile.test.tsx)
- Props interfaces defined above component
- Export default at bottom
```

### Step 3: Design Skill Structure

**Determine skill metadata**:
```yaml
name: [project]-[pattern-type]
description: [When to auto-invoke + what it does]
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, Task]
version: 1.0.0
```

**Plan directory structure**:
```
skills/[skill-name]/
├── SKILL.md              # Main instructions
├── functions/            # Python helper scripts
│   └── [generator].py
├── examples/             # Reference implementations
│   └── [example].[ext]
└── templates/            # Output format templates
    └── [template].[ext]
```

**Design predefined functions**:
- What repetitive logic can be automated?
- What validation should be enforced?
- What formatting ensures consistency?

**Example functions for frontend-component skill**:
- `component_generator.py` - Generate component boilerplate
- `test_generator.py` - Generate test file
- `style_generator.py` - Generate style file
- `name_validator.py` - Validate component naming

### Step 4: Generate Skill Files

**4.1 Create SKILL.md**

```markdown
---
name: [skill-name]
description: [Auto-invocation triggers + purpose]
allowed-tools: [List of tools]
version: 1.0.0
---

# [Skill Title]

[Brief description of what this skill does]

## When to Invoke

Auto-invoke when user says:
- "[trigger phrase 1]"
- "[trigger phrase 2]"
- "[trigger phrase 3]"

## What This Does

1. [Step 1 overview]
2. [Step 2 overview]
3. [Step 3 overview]

## Execution Steps

### Step 1: [Step Name]

[Detailed instructions for this step]

**Use predefined function**: `functions/[function-name].py`
```

**4.2 Create Predefined Functions**

```python
# functions/[generator].py

def generate_[output](name, config):
    """
    Generate [output type] based on project patterns.

    Args:
        name: [Description]
        config: [Description]

    Returns:
        [output]: [Description]
    """
    # Implementation based on codebase analysis
    pass
```

**4.3 Create Examples**

```
examples/
└── [reference-implementation].[ext]
    - Real example from codebase (best practice)
    - Shows expected structure
    - Demonstrates conventions
```

**4.4 Create Templates**

```
templates/
└── [output-template].[ext]
    - Skeleton structure with placeholders
    - ${VAR_NAME} for substitution
    - Comments explaining sections
```

### Step 5: Test Generated Skill

**5.1 Verify skill loads**:
```bash
# In project root
grep -r "name: [skill-name]" skills/
```

**5.2 Test auto-invocation**:
```
In Claude Code conversation:
"[Use one of the auto-invoke trigger phrases]"

Expected: Skill should be detected and loaded
```

**5.3 Test execution**:
- Run through skill steps
- Verify functions work correctly
- Check output matches template
- Validate generated code follows patterns

**5.4 Iterate if needed**:
- Fix function bugs
- Improve templates
- Add missing examples
- Clarify instructions

### Step 6: Document New Skill

**Update project documentation**:

1. **CLAUDE.md** - Add to skills section:
```markdown
#### [Skill Name]
**Auto-invoke**: "[trigger phrase]"
**Purpose**: [What it does]
**Generates**: [Output type]
```

2. **README.md** - Add to skills list:
```markdown
- **[skill-name]**: [Brief description]
```

3. **.agent/system/plugin-patterns.md** - Add to skill registry:
```markdown
### [Skill Name]
**Created**: [Date]
**Pattern**: [What pattern it enforces]
**Functions**: [List of predefined functions]
```

**Register in plugin.json** (if applicable):
```json
{
  "skills": [
    {
      "name": "[skill-name]",
      "path": "skills/[skill-name]/SKILL.md"
    }
  ]
}
```

---

## Example Workflows

### Example 1: Create Skill for Adding API Endpoints

**User**: "Create a skill for adding REST API endpoints"

**Execution**:

1. **Clarify**:
   - Which framework? (Express, Fastify, etc.)
   - Where are routes defined?
   - Authentication required?
   - Testing strategy?

2. **Analyze** (via Task agent):
   ```
   Find existing API endpoints:
   - Routes in api/routes/
   - Controllers in api/controllers/
   - Middleware in api/middleware/
   - Tests in tests/api/
   ```

3. **Design**:
   ```yaml
   name: backend-api-endpoint
   description: Add new REST API endpoint following project conventions. Use when user says "add endpoint", "create API", or "new route".
   allowed-tools: Read, Write, Edit, Grep, Glob, Bash
   ```

4. **Generate**:
   ```
   skills/backend-api-endpoint/
   ├── SKILL.md
   ├── functions/
   │   ├── endpoint_generator.py
   │   └── route_validator.py
   ├── examples/
   │   └── user-endpoint.ts
   └── templates/
       ├── route-template.ts
       └── test-template.spec.ts
   ```

5. **Test**:
   ```
   User: "Add a POST /posts endpoint"
   Skill: Auto-invoked, generates route + controller + test
   Verify: Files follow project conventions
   ```

6. **Document**: Update CLAUDE.md, README.md, plugin-patterns.md

### Example 2: Create Skill for React Components

**User**: "Automate creating new React components"

**Execution**:

1. **Clarify**:
   - TypeScript or JavaScript?
   - Functional or class components?
   - Style approach? (CSS modules, styled-components, etc.)
   - Test library? (Jest, React Testing Library, etc.)

2. **Analyze** (via Task agent):
   ```
   Find React components:
   - Components in src/components/
   - PascalCase naming
   - TypeScript (.tsx)
   - CSS modules (.module.css)
   - Tests with RTL
   ```

3. **Design**:
   ```yaml
   name: frontend-component
   description: Create new React component with TypeScript, styles, and tests. Use when user says "create component", "add component", or "new React component".
   allowed-tools: Read, Write, Edit, Grep, Glob, Bash
   ```

4. **Generate**:
   ```
   skills/frontend-component/
   ├── SKILL.md
   ├── functions/
   │   ├── component_generator.py
   │   ├── test_generator.py
   │   └── style_generator.py
   ├── examples/
   │   ├── Button.tsx
   │   └── Button.test.tsx
   └── templates/
       ├── component-template.tsx
       ├── test-template.test.tsx
       └── style-template.module.css
   ```

5. **Test**:
   ```
   User: "Create a UserProfile component"
   Skill: Auto-invoked, generates component + test + styles
   Verify: Props interface, exports, naming correct
   ```

6. **Document**: Update project docs

---

## Output Format

**After generating skill, show summary**:

```
✅ Skill Created: [skill-name]

Structure:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 skills/[skill-name]/
   ├── SKILL.md
   ├── functions/
   │   └── [N functions created]
   ├── examples/
   │   └── [N examples added]
   └── templates/
       └── [N templates created]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Auto-Invocation Triggers:
- "[trigger 1]"
- "[trigger 2]"
- "[trigger 3]"

Next Steps:
1. Test the skill: "[example trigger phrase]"
2. Iterate if needed
3. Documentation updated

Try it now: "[example usage]"
```

---

## Best Practices

### Pattern Analysis
- Use Task agent for codebase exploration (saves 60-80% tokens)
- Look at 3-5 examples minimum (find patterns vs outliers)
- Identify conventions explicitly followed
- Note edge cases in comments

### Skill Design
- Keep skills focused (one pattern per skill)
- Clear auto-invocation triggers (3-5 phrases)
- Minimal tools needed (add only what's required)
- Progressive disclosure (details in functions, not main instructions)

### Function Creation
- One function = one responsibility
- Type hints and docstrings required
- Handle errors gracefully
- Return structured data (not print statements)

### Template Design
- Use clear placeholders (${VAR_NAME})
- Include comments explaining sections
- Follow project style guide
- Provide sensible defaults

### Testing
- Test with real project context
- Verify auto-invocation works
- Check output against best practices
- Iterate based on actual usage

---

## Common Patterns to Automate

### Backend Patterns
- REST API endpoints
- GraphQL resolvers
- Database migrations
- Background jobs
- Middleware functions
- Authentication guards

### Frontend Patterns
- React/Vue/Svelte components
- Redux/Vuex store modules
- API client functions
- Form validation schemas
- Route definitions
- Style component creation

### Infrastructure Patterns
- Docker service configs
- CI/CD pipeline steps
- Deployment scripts
- Environment configs
- Monitoring setup

### Documentation Patterns
- API documentation
- Component documentation
- Architecture decision records (ADRs)
- Runbook entries
- Changelog entries

---

## Troubleshooting

### Skill Not Auto-Invoking

**Problem**: Skill created but doesn't trigger automatically

**Solutions**:
1. Check description has clear trigger phrases
2. Verify `plugin.json` includes skill registration
3. Reload Claude Code to refresh skill index
4. Test with exact trigger phrase from description

### Functions Not Executing

**Problem**: Predefined functions throw errors

**Solutions**:
1. Check Python syntax is valid
2. Verify function imports are correct
3. Test function independently first
4. Check error messages in execution logs

### Templates Not Matching Output

**Problem**: Generated code doesn't match project conventions

**Solutions**:
1. Re-analyze codebase for missed patterns
2. Update templates with correct structure
3. Add more examples showing variations
4. Validate against linter/formatter

### Skill Too Broad

**Problem**: Skill tries to do too much

**Solutions**:
1. Split into multiple focused skills
2. Remove optional features to separate skills
3. Keep core pattern simple
4. Add extensions as separate skills

---

## Success Criteria

**This skill succeeds when**:
- [ ] New skill auto-invokes correctly
- [ ] Generated output follows project conventions
- [ ] Functions execute without errors
- [ ] Templates produce valid code
- [ ] Examples are clear and relevant
- [ ] Documentation is updated
- [ ] Skill saves time vs manual work

---

**The skill-creator is Navigator's self-improving engine - it learns your patterns and automates them** 🔄