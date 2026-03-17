---
name: file-categorization
description: Reusable logic for categorizing files as Command, Agent, Skill, or Documentation based on structure and content analysis
---

# File Categorization Skill

## When to Use This Skill

- Processing files in integration pipelines
- Scanning directories for file organization
- Auto-routing files to appropriate locations
- Generating file inventory reports
- Validating repository structure

## What This Skill Does

Analyzes file structure and content to accurately categorize files into:
- **Commands** - Slash command definitions
- **Agents** - Agent configuration files
- **Skills** - Reusable workflow automation
- **Documentation** - General markdown documentation
- **Other** - Uncategorized files requiring manual review

## Categorization Logic

### Step 1: Filename Pattern Matching

**Commands**:
- Filename matches `*-command.md` or `*command.md`
- Located in `.claude/commands/` directory
- Filename uses verb-noun pattern (e.g., `integration-scan.md`)

**Agents**:
- Filename matches `*-agent.md` or `*agent.md`
- Located in `agents-templates/` directory
- Contains role-based names (architect, builder, validator, etc.)

**Skills**:
- Filename is `SKILL.md` or `*-SKILL.md` or `*-skill.md`
- Located in `skills/*/` directories
- Contains workflow automation content

**Documentation**:
- Standard `.md` files
- Located in `docs/` directory
- Contains reference or tutorial content

### Step 2: Frontmatter Analysis

Read the YAML frontmatter (if present) to identify:

**Command Indicators**:
```yaml
---
description: "..."
allowed-tools: [...]
author: "..."
version: "X.Y"
---
```

**Skill Indicators**:
```yaml
---
name: skill-name
description: "..."
---
```

**Agent Indicators** (less structured, more prose):
```markdown
## Agent Identity
**Role**: [Agent Role]
**Version**: X.Y.Z
**Purpose**: [Purpose description]
```

### Step 3: Content Structure Analysis

**Commands have**:
- Workflow sections with numbered steps
- Bash command examples (prefixed with `!`)
- `allowed-tools` restrictions
- Usage examples

**Agents have**:
- Core Responsibilities section
- Allowed Tools and Permissions section
- Workflow Patterns section
- Context Management section

**Skills have**:
- "When to Use" section
- "What This Skill Does" section
- Step-by-step process descriptions
- Examples with real data

**Documentation has**:
- Standard markdown structure
- Tutorial or reference content
- No executable workflows
- Educational purpose

### Step 4: Keyword Detection

Scan content for category-specific keywords:

**Command Keywords**:
- `!bash`, `!git`, `!npm`, etc. (shell commands)
- "allowed-tools"
- "Usage:", "Workflow:", "Steps:"
- Command-line patterns

**Agent Keywords**:
- "Core Responsibilities"
- "Workflow Patterns"
- "Context Management"
- "Orchestrator", "Sub-Agent"
- "Handoff", "Delegation"

**Skill Keywords**:
- "When to Use"
- "What This Skill Does"
- "Skill" in self-references
- Reusable workflow language

**Documentation Keywords**:
- "Introduction", "Overview", "Guide"
- "Tutorial", "Reference", "Best Practices"
- Educational/explanatory language

## Categorization Algorithm

```
function categorizeFile(filePath, content):
  // Phase 1: Filename and location
  if filename matches command patterns OR in .claude/commands/:
    category = "Command"
    confidence = "High"

  else if filename == "SKILL.md" OR in skills/*/:
    category = "Skill"
    confidence = "High"

  else if in agents-templates/:
    category = "Agent"
    confidence = "High"

  else if in docs/:
    category = "Documentation"
    confidence = "Medium"

  // Phase 2: Frontmatter analysis (refine)
  frontmatter = extractYAML(content)
  if frontmatter contains "allowed-tools" AND "version":
    category = "Command"
    confidence = "High"

  else if frontmatter contains "name" (no allowed-tools):
    category = "Skill"
    confidence = "High"

  // Phase 3: Content structure (if still uncertain)
  if confidence != "High":
    if content contains "## Agent Identity":
      category = "Agent"
      confidence = "High"

    else if content contains "## When to Use":
      category = "Skill"
      confidence = "Medium"

    else if content contains "!bash" OR "!git":
      category = "Command"
      confidence = "Medium"

  // Phase 4: Fallback
  if category == null:
    category = "Other"
    confidence = "Low"
    reason = "Unable to determine category, manual review needed"

  return {category, confidence, reasoning}
```

## Output Format

For each categorized file, return:

```markdown
### [Filename]
- **Category**: [Command|Agent|Skill|Documentation|Other]
- **Confidence**: [High|Medium|Low]
- **Reasoning**: [Why this category was assigned]
- **Frontmatter**: [✅ Valid | ⚠️ Malformed | ❌ Missing]
- **Required Fields**: [List of found/missing fields]
- **Recommended Location**: [Target directory path]
```

## Example Usage

### Example 1: Categorizing Integration File

**Input**:
```
File: USING-GIT-WORKTREES-SKILL.md
Content:
---
name: using-git-worktrees
description: Creates isolated git worktrees...
---

# Using Git Worktrees

## When to Use
...
```

**Output**:
```markdown
### USING-GIT-WORKTREES-SKILL.md
- **Category**: Skill
- **Confidence**: High
- **Reasoning**: Filename matches skill pattern, frontmatter has 'name' field, content has "When to Use" section
- **Frontmatter**: ✅ Valid
- **Required Fields**: name ✅, description ✅
- **Recommended Location**: skills/using-git-worktrees/SKILL.md
```

### Example 2: Categorizing Command File

**Input**:
```
File: integration-scan.md
Content:
---
description: "Scan and categorize incoming files"
allowed-tools: ["Read", "Bash(find)"]
author: "Claude Command and Control"
version: "1.0"
---

# Integration Scan

## Purpose
...
```

**Output**:
```markdown
### integration-scan.md
- **Category**: Command
- **Confidence**: High
- **Reasoning**: Filename uses verb-noun pattern, frontmatter has 'allowed-tools' and 'version'
- **Frontmatter**: ✅ Valid
- **Required Fields**: description ✅, allowed-tools ✅, author ✅, version ✅
- **Recommended Location**: .claude/commands/integration-scan.md
```

### Example 3: Uncategorizable File

**Input**:
```
File: notes.md
Content:
# Random Notes

Some thoughts about the project...
```

**Output**:
```markdown
### notes.md
- **Category**: Other
- **Confidence**: Low
- **Reasoning**: No frontmatter, no structural indicators, generic content
- **Frontmatter**: ❌ Missing
- **Required Fields**: N/A
- **Recommended Location**: Manual review required
```

## Integration with Commands

### Used By

- `/integration-scan` - Primary categorization logic
- `/integration-process` - Determines target directory
- `/integration-validate` - Validates category-specific structure

### Usage Pattern

```markdown
# In integration-scan command

For each file in /INTEGRATION/incoming:
  1. Read file content
  2. Use file-categorization skill
  3. Extract category and confidence
  4. Include in scan report
  5. Mark for processing if High confidence
  6. Flag for review if Medium/Low confidence
```

## Category-Specific Validation Rules

### Commands
- ✅ MUST have: description, allowed-tools, author, version
- ✅ SHOULD have: workflow steps, usage examples
- ⚠️ Check: Tool permissions not overly broad

### Agents
- ✅ MUST have: Agent Identity, Core Responsibilities, Allowed Tools
- ✅ SHOULD have: Workflow Patterns, Context Management
- ⚠️ Check: Role clearly defined

### Skills
- ✅ MUST have: name, description, "When to Use"
- ✅ SHOULD have: Examples, step-by-step process
- ⚠️ Check: Examples use real data (not placeholders)

### Documentation
- ✅ MUST have: Clear title, structured content
- ✅ SHOULD have: Table of contents, cross-references
- ⚠️ Check: No executable workflows (should be in Command/Skill)

## Error Handling

### Malformed Frontmatter
```
Issue: YAML syntax error
Action: Note in categorization output
Category: "Other" with reason "Invalid frontmatter"
Recommendation: Fix YAML before processing
```

### Conflicting Indicators
```
Issue: Filename says "command" but structure says "skill"
Action: Confidence = "Medium"
Reasoning: "Filename and content indicators conflict"
Recommendation: Manual review
```

### Missing Content
```
Issue: File is empty or too short (<100 chars)
Action: Category = "Other"
Confidence: "Low"
Reasoning: "Insufficient content for categorization"
```

## Testing Recommendations

Test with:
1. **Typical files** - Standard commands, agents, skills
2. **Edge cases** - Mixed indicators, missing frontmatter
3. **Malformed files** - Syntax errors, incomplete content
4. **Ambiguous files** - Could fit multiple categories

Expected accuracy:
- **High confidence**: >95% correct
- **Medium confidence**: >80% correct
- **Low confidence**: Requires manual review

## Version History

**1.0** (2025-11-23)
- Initial file categorization skill
- Four-phase categorization algorithm
- Integration with scan/process commands
- Comprehensive validation rules

---

**Skill Status**: Production Ready
**Accuracy Target**: >95% for High confidence categorizations
**Dependencies**: None (standalone logic)
