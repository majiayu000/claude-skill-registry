---
name: managing-agent-skills
description: Creates, analyzes, updates, and improves Claude Code agent skills including YAML frontmatter, allowed-tools field, progressive disclosure, and skill authoring workflows. Use when user asks how skills work, what agent skills are, explaining skill concepts, understanding SKILL.md structure, describing .md files organization, skill authoring process, asked to create a new skill, evaluate existing skills for improvements, optimize skills for AI/Claude effectiveness, suggest converting current logic into a skill, update outdated skill information, or when user mentions skill validation, best practices, supporting files, skill security, API integration, or technical architecture.
---

# Managing Agent Skills

This skill enables comprehensive management of agent skills including creation, analysis, improvement, and maintenance.

## When to Use This Skill

Activate this skill when:
- User requests creation of a new agent skill
- User asks to analyze or evaluate an existing skill
- User inquires whether current conversation logic should become a skill
- User requests updates to outdated skill information
- User mentions "skill", "agent capability", "reusable workflow" in context of creation/improvement
- You identify that a complex, repeated workflow would benefit from being a skill

## Core Workflows

### Workflow 1: Creating a New Skill

When creating a new skill, follow this structured approach:

#### Step 1: Requirements Gathering
- Identify the skill's primary purpose and domain
- Determine usage triggers and contexts
- Assess complexity level (simple vs. complex workflow)
- Load creation-checklist.md and review "Decision Matrix: Skill vs Slash Command" section to verify this should be a skill

#### Step 2: Skill Design
- Choose descriptive gerund-form name (lowercase-with-hyphens)
- Write specific description including:
  - What the skill does
  - When to use it
  - Key triggers or contexts
  - Informational query triggers matching the domain (how X works, what X is, explaining X)
  - Action triggers matching the skill's actual capabilities (only verbs for what it does)
- Plan file structure:
  - Single SKILL.md for simple capabilities (ONLY required file)
  - Multiple .md files allowed for complex workflows (ANY .md file in root directory is loaded)
  - Progressive disclosure: keep SKILL.md focused, use additional .md files for detailed content
- Determine tool restrictions (optional):
  - Use `allowed-tools` YAML field to restrict which tools Claude can use
  - Format: `allowed-tools: Read, Grep, Glob, Bash` (comma-separated list)
  - Only restrict if skill requires specific tool limitations for safety/functionality
  - If omitted, all tools available
- Identify supporting resources needed (scripts, templates, reference docs, data files)

#### Step 3: Implementation
- Use Write tool to create SKILL.md with YAML frontmatter:
  - Required: `name` and `description` fields
  - Optional: `allowed-tools` field (if tool restrictions needed)
  - Always use forward slashes in paths, even on Windows
- Write core instructions in SKILL.md (target under 5,000 tokens, approximately 500-700 lines)
- Structure content with clear sections: When to Use, Core Workflows, Progressive Disclosure References, Validation
- If content will exceed token limit, load best-practices.md section on progressive disclosure and plan file splitting
- Use Write tool to create additional .md files in root directory (all .md files are loaded)
- Use Write tool to create supporting files in logical organization (scripts/, templates/, resources/)
- Use Read tool to verify all created files

#### Step 4: Validation
- Verify YAML syntax (proper delimiters, no tabs)
- Check name format (lowercase, hyphens, under 64 chars)
- Validate description specificity (under 1024 chars, includes triggers)
- Verify allowed-tools field format if present (comma-separated, valid tool names)
- Confirm token count under 5,000 tokens for SKILL.md (approximately 500-700 lines)
- Load creation-checklist.md Phase 4: Validation and verify all items
- Ensure conciseness (remove redundant information)
- Test description clarity: would it be discoverable among 100+ skills?

#### Step 5: Documentation
- Add usage examples if helpful
- Document any dependencies or requirements
- Include validation/verification steps
- Add troubleshooting guidance if applicable

### Workflow 2: Analyzing Existing Skills

When evaluating an existing skill for improvements:

#### Step 1: Load and Review
- Use Read tool to read the complete SKILL.md file
- Use Glob tool to list all files in the skill directory with pattern `**/*`
- Count the line length of SKILL.md
- Identify number of workflows and major sections
- List all files referenced in SKILL.md

#### Step 2: Apply Analysis Framework
Load analysis-framework.md now and follow its detailed evaluation process. The framework systematically covers:
- **Description Quality**: Specificity and trigger keywords
- **Name Appropriateness**: Format validation and clarity
- **Content Organization**: Structure and progressive disclosure
- **Conciseness**: Redundancy and essential information
- **Best Practices Compliance**: Alignment with best-practices.md
- **Outdated Information**: Time-sensitive content identification
- **File Structure**: Organization and file splitting needs
- **Tool Restrictions**: Appropriateness of allowed-tools

#### Step 3: Identify Improvements
Categorize findings:
- **Critical Issues**: Broken functionality, invalid YAML, incorrect triggers
- **Major Improvements**: Poor organization, unclear description, missing validation
- **Minor Enhancements**: Style improvements, better examples, clearer wording

#### Step 4: Recommendations
Provide specific, actionable improvement suggestions with:
- What to change
- Why it improves the skill
- How to implement the change
- Priority level (critical/major/minor)

### Workflow 3: Suggesting Skill Conversion

When evaluating whether current logic should become a skill:

#### Decision Criteria
Evaluate each criterion below as a checklist. Convert to skill if 3+ criteria are met:

- [ ] Logic is complex (multiple steps, validation loops, structured workflow)
- [ ] It will be reused across multiple conversations
- [ ] It requires specialized domain knowledge
- [ ] Multiple supporting files/scripts would be beneficial
- [ ] Team needs standardized approach to this task

**Decision Rule:**
- If 3+ checked → Create skill (proceed to Workflow 1)
- If 0-2 checked → Keep as inline logic

Keep as inline logic when:
- One-time or rarely repeated task
- Simple, straightforward operation
- No supporting resources needed
- Context-specific to current conversation

#### Suggestion Process
1. Identify reusable patterns in current conversation
2. Assess complexity and reusability
3. If appropriate, explain benefits of skill conversion
4. Outline proposed skill structure
5. Offer to create the skill if user agrees

### Workflow 4: Updating Outdated Skills

When updating existing skills:

#### Step 1: Identify Outdated Content
- Time-sensitive information that has changed
- Deprecated tools or approaches
- New best practices not reflected
- Missing features that now exist

#### Step 2: Plan Updates
- Preserve working functionality
- Use "Old patterns" sections for deprecated approaches (avoid dates)
- Update documentation to reflect current state
- Maintain backward compatibility where possible

#### Step 3: Implement Changes
- Edit SKILL.md or supporting files
- Test that updates work correctly
- Verify YAML frontmatter still valid
- Update any affected references

#### Step 4: Document Changes
- Note what was updated and why
- Include version history if significant change
- Update examples if needed

## Progressive Disclosure References

For detailed guidance, refer to these supporting files:

- **best-practices.md**: Comprehensive best practices for skill authoring
- **creation-checklist.md**: Step-by-step checklist for creating new skills
- **analysis-framework.md**: Detailed framework for evaluating existing skills
- **examples-creation.md**: Examples for Workflow 1 - naming, descriptions, structure patterns
- **examples-analysis.md**: Examples for Workflow 2 - common mistakes, quality assessment
- **examples-improvement-descriptions.md**: Examples for improving descriptions, names, and triggers
- **examples-improvement-content.md**: Examples for improving content quality and workflows
- **examples-improvement-structure.md**: Examples for improving file organization and progressive disclosure
- **quick-reference.md**: Fast validation cheat sheet for rapid checks
- **templates/skill-template.md**: Template for new SKILL.md files

Load these files only when detailed guidance is needed for specific tasks.

## Skill Storage Locations

Choose appropriate location:
- **Personal skills**: `~/.claude/skills/` - User-specific, experimental, individual workflows
- **Project skills**: `.claude/skills/` - Team-shared, committed to git, standardized workflows

## Key Principles

1. **Conciseness**: Context window is shared resource. Only include information not already known.
2. **Specificity**: Descriptions must enable discovery. Be concrete about triggers and usage.
3. **Progressive Disclosure**: Keep SKILL.md under 5,000 tokens (approx 500-700 lines). Split complex content into separate .md files.
4. **Cross-Platform Paths**: ALWAYS use forward slashes `/` in file paths, even on Windows. Never use backslashes.
5. **Focused Capability**: One skill, one domain. Don't create overly broad skills.
6. **Validation First**: Always validate before finalizing. Use checklists.
7. **Model-Specific Tuning**:
   - **Haiku**: Needs more detail and explicit guidance
   - **Sonnet**: Balanced - standard level of detail works well
   - **Opus**: Avoid over-explaining - can infer from context
8. **Security First**: Only use skills from trusted sources. Audit third-party skills thoroughly.

## Technical Architecture

Understanding how skills work internally helps create more effective skills:

### Skill Structure & File Organization

**Required:**
- `SKILL.md`: Core instructions with YAML frontmatter (name, description, optional allowed-tools)

**Optional:**
- **Any .md files** in root directory are automatically loaded (not just SKILL.md and REFERENCE.md)
- **scripts/**: Executable Python, JavaScript, or shell scripts
- **templates/**: Pre-built files that can be customized (Excel templates, document templates)
- **resources/**: Supporting data files, configuration, assets

### Progressive Disclosure Levels

Skills load in three stages to optimize token usage:

| Stage | Content | Token Cost | When Loaded |
|-------|---------|------------|-------------|
| **Level 1: Metadata** | `name` (64 chars) + `description` (1024 chars) | Minimal | Always visible for skill discovery |
| **Level 2: Instructions** | All .md files | <5,000 tokens recommended | When skill is relevant/activated |
| **Level 3: Resources** | Scripts, templates, data files | As needed | During execution when referenced |

### Runtime Environment

- **Execution**: Skills run in code execution environment with filesystem access
- **Navigation**: Claude navigates skill directory like a filesystem
- **Scripts**: Executed via bash tool - only script output consumes tokens, not the code itself
- **Efficiency**: Scripts are token-efficient for complex logic (code doesn't enter context, just results)

### Skills Are Not Just Markdown

Skills can bundle executable code and data:
- **Python scripts** (`.py`): Data processing, calculations, validations
- **JavaScript** (`.js`): Web-based operations, JSON manipulation
- **Shell scripts** (`.sh`): File operations, system commands
- **Templates** (`.xlsx`, `.docx`, etc.): Pre-built files for customization
- **Data files** (`.json`, `.csv`, `.yaml`): Configuration, reference data

## Security Considerations

**CRITICAL**: Security must be top priority when creating or using skills.

### For Skill Users

**Only use skills from trusted sources:**
- Official Anthropic skills (xlsx, pptx, pdf) are fully vetted
- Custom skills from unknown sources pose risks:
  - Data exfiltration via network calls
  - Unauthorized file system access
  - Credential theft from environment variables
  - Tool misuse (deleting files, modifying system)

**Before using external skills:**
1. Audit all scripts thoroughly (Python, JavaScript, bash)
2. Check for network calls, file operations, environment variable access
3. Verify tool restrictions via `allowed-tools` field
4. Review all file references and paths
5. Test in isolated environment first

### For Skill Creators

**Design with security in mind:**
- Use `allowed-tools` to restrict unnecessary tool access
- Never hardcode API keys, credentials, or secrets
- Validate and sanitize all inputs in scripts
- Document security considerations in SKILL.md
- Use relative or tilde paths (never absolute with usernames)
- Avoid unnecessary file system operations
- Log skill usage for audit trails if compliance required

**Data Privacy:**
- Don't include sensitive data in skill files
- Skills are workspace-specific but review access controls
- Consider data residency requirements for cloud execution

## API Integration

### Using Skills via Anthropic API

Skills integrate with the Messages API through the `container` parameter:

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
            {"type": "custom", "skill_id": "skill_xyz", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{"role": "user", "content": "Your prompt here"}],
    betas=[
        "code-execution-2025-08-25",
        "files-api-2025-04-14",
        "skills-2025-10-02"
    ]
)
```

### Required Beta Headers

Skills require specific beta features:
- `code-execution-2025-08-25`: Enables script execution
- `files-api-2025-04-14`: Enables file upload/download
- `skills-2025-10-02`: Enables skills functionality

### Skill Versioning

- **Anthropic skills**: Date-based versions (e.g., `20251013`)
- **Custom skills**: Epoch timestamp versions (e.g., `1234567890`)
- **Version "latest"**: Always uses most recent version
- **Pinned versions**: Specify exact version for reproducibility

### Files API Integration

Download files generated by skills:

```python
# Extract file IDs from response
file_ids = [block.file.file_id for block in response.content if hasattr(block, 'file')]

# Download files
for file_id in file_ids:
    file_content = client.files.content(file_id)
    # Save or process file_content
```

## Package Dependencies & Runtime Constraints

Different environments have different capabilities:

### claude.ai (Web Interface)
- **Network access**: Yes
- **Package installation**: Can install from npm/PyPI at runtime
- **Use case**: Interactive experimentation, one-time tasks

### Anthropic API (Cloud Execution)
- **Network access**: No
- **Package installation**: No runtime installation
- **Pre-configured only**: Only standard library + pre-installed packages
- **Use case**: Production applications, controlled environments

### Claude Code (Desktop CLI)
- **Network access**: Full network access
- **Package installation**: Possible but discouraged (pollutes global namespace)
- **Best practice**: Use virtual environments or document dependencies
- **Use case**: Local development, file system operations

### Dependency Management Best Practices

1. **Document requirements**: List all package dependencies in skill documentation
2. **Use standard libraries** when possible (no installation needed)
3. **Provide fallbacks**: Graceful degradation if packages unavailable
4. **Test across environments**: Verify skill works in target environment
5. **Version constraints**: Specify minimum versions if APIs changed

## MCP Tool References

When skills use Model Context Protocol (MCP) tools, follow this naming convention:

**Format**: `ServerName:tool_name`

**Example**:
```
BigQuery:bigquery_schema
FileSystem:read_file
WebSearch:search
```

**In skill documentation:**
- Clearly identify MCP tool dependencies
- Document which MCP servers must be configured
- Provide setup instructions for required MCP servers
- Test that MCP tools are available before use

## Skill Composition

Combining multiple skills creates powerful workflows:

### Combining Anthropic + Custom Skills

```python
container={
    "skills": [
        {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
        {"type": "custom", "skill_id": "financial-ratios", "version": "latest"}
    ]
}
```

**Use cases:**
- Financial analysis skill + xlsx skill → Generate analysis spreadsheets
- Brand guidelines skill + pptx skill → Create branded presentations
- Data validation skill + pdf skill → Generate audit reports

### Skill Composition Patterns

**Sequential**: One skill feeds into another
```
Data extraction → Data analysis → Report generation
```

**Parallel**: Multiple skills work on same input
```
Input data → [Skill A: Validation, Skill B: Enrichment, Skill C: Formatting]
```

**Hierarchical**: General skill delegates to specialized skills
```
Project management skill → [Task planning skill, Resource allocation skill, Timeline skill]
```

### Best Practices for Composition

1. **Clear interfaces**: Skills should have well-defined inputs/outputs
2. **No overlap**: Each skill handles distinct responsibilities
3. **Loose coupling**: Skills work independently
4. **Composable design**: Design skills to work alone or combined

## Evaluation-Driven Development

Build evaluations before extensive skill development:

### Why Evaluations First?

- **Clarity**: Forces clear definition of skill goals
- **Validation**: Objective measurement of skill effectiveness
- **Iteration**: Data-driven improvements
- **Regression testing**: Prevents breaking changes

### Evaluation Structure

1. **Test cases**: Representative examples of skill usage
2. **Expected outputs**: Clear success criteria
3. **Rubrics**: Scoring system for quality assessment
4. **Edge cases**: Boundary conditions and error scenarios

### Evaluation Workflow

```
1. Define skill requirements → 2. Create evaluation dataset →
3. Write initial skill → 4. Run evaluations → 5. Iterate based on results
```

### Example Evaluation

For a financial ratio calculator skill:

**Test case**: Company with Revenue $1M, Assets $2M, Debt $500K
**Expected**: ROA = 0.5, Debt-to-Equity = 0.33, Current Ratio calculation
**Rubric**: Accuracy (±0.01), Format (JSON), Interpretation quality (1-5 scale)

## Iterative Development with Claude

Collaborative approach for skill creation:

### Two-Claude Method

**Claude A (Expert)**: Creates and refines the skill
**Claude B (User)**: Tests the skill in real scenarios

### Process

1. **Draft** (Claude A): Create initial skill based on requirements
2. **Test** (Claude B): Use skill in realistic scenarios
3. **Observe** (You): Watch how Claude B interprets and applies skill
4. **Refine** (Claude A): Adjust based on Claude B's behavior
5. **Repeat**: Iterate until skill works naturally

### Observing Claude's Behavior

Pay attention to:
- **Activation**: Does skill load when expected?
- **Interpretation**: Does Claude understand instructions correctly?
- **Tool usage**: Are the right tools being used?
- **Errors**: Where does Claude get confused or fail?
- **Edge cases**: How does Claude handle unexpected inputs?

### Refinement Strategies

- **Add examples** if Claude misunderstands instructions
- **Simplify language** if Claude over-complicates
- **Add constraints** if Claude takes wrong paths
- **Split into sub-skills** if skill tries to do too much
- **Add progressive disclosure** if token usage too high

## Tool Usage Patterns

When analyzing a skill:
1. Use Read tool to read the skill's SKILL.md file
2. Use Glob tool to list all files in skill directory: `**/*`
3. Use Read tool on supporting files as referenced in workflows
4. Estimate token count to verify under 5,000 token target (approximately 500-700 lines)

When creating a skill:
1. Use Write tool to create SKILL.md with YAML frontmatter
2. Use Read tool to verify the file after creation
3. Use Write tool to create supporting files as needed
4. Use Glob tool to verify all files are created correctly

When searching for existing skills:
1. Use Glob tool with pattern `**/*.md` to find all skill files
2. Use Grep tool to search for specific keywords across skills
3. Use Read tool to examine candidate skills

When validating a skill:
1. Use Read tool to load creation-checklist.md for comprehensive validation
2. Use Read tool to load quick-reference.md for rapid pre-flight checks
3. Verify YAML syntax by reading frontmatter carefully (check allowed-tools if present)
4. Estimate token count of SKILL.md to ensure under 5,000 tokens (approximately 500-700 lines)

## Anti-Patterns to Avoid

**Naming & Description:**
- Vague skill names like "helper" or "utils"
- Descriptions without usage triggers
- Missing context about when to use skill

**Content & Organization:**
- Including information already in Claude's training
- Time-sensitive conditionals (use "Old patterns" sections instead)
- Deep nesting of file references (keep one level from SKILL.md)
- Skills with multiple unrelated capabilities
- Over-explaining to Opus (can infer from context)
- Under-explaining to Haiku (needs explicit guidance)

**File Paths & Cross-Platform:**
- Windows-style backslash paths (`C:\Users\...`) - ALWAYS use forward slashes
- Absolute paths with usernames (`/Users/john/...`) - Use relative or tilde paths
- Inconsistent path separators across files

**Tool & Dependency Management:**
- Offering many equivalent options without defaults
- Assuming packages are installed without documentation
- Not specifying environment constraints (claude.ai vs API vs Code)
- Restricting tools unnecessarily via `allowed-tools`

**Logic & Complexity:**
- Punting complex logic to Claude instead of solving in scripts
- Not using scripts for token-heavy operations
- Creating mega-skills instead of composable smaller skills

**Security:**
- Hardcoding credentials, API keys, or secrets
- Not validating/sanitizing inputs in scripts
- Excessive tool permissions via `allowed-tools`
- Including sensitive data in skill files

## Quick Validation Checklist

Use this for rapid pre-flight checks during skill creation or analysis. For comprehensive validation during skill creation, load creation-checklist.md (Phase 4: Validation).

Before considering a skill complete:
- [ ] YAML frontmatter valid (name and description required, allowed-tools optional)
- [ ] Name is gerund form, lowercase-with-hyphens, under 64 chars
- [ ] Description specific, includes triggers, under 1024 chars
- [ ] `allowed-tools` format correct if present (comma-separated, valid tool names)
- [ ] SKILL.md under 5,000 tokens (approximately 500-700 lines)
- [ ] All file paths use forward slashes (even on Windows)
- [ ] No absolute paths with usernames (use relative or tilde paths)
- [ ] Content organized logically with clear sections
- [ ] Progressive disclosure used for complex content (multiple .md files if needed)
- [ ] No redundant or unnecessary information
- [ ] Supporting files appropriately organized (scripts/, templates/, resources/)
- [ ] Examples provided where helpful
- [ ] Dependencies documented with environment constraints
- [ ] Security considerations addressed (no hardcoded secrets)
- [ ] Model-specific guidance considered (Haiku/Sonnet/Opus differences)
- [ ] Follows best practices from best-practices.md

## Quick Troubleshooting

Common issues and fast solutions. Placement after workflows is intentional - learn the process first, then troubleshoot issues.

**Skill Not Loading**
- Check YAML syntax (delimiters `---`, no tabs, required fields present)
- Verify file named exactly `SKILL.md`
- Confirm location: `~/.claude/skills/` or `.claude/skills/`
- Restart Claude Code to reload skills

**Skill Not Activating**
- Add specific trigger keywords to description
- Test with explicit invocation: "use [skill-name] to..."
- Check if description is too vague (add concrete contexts)
- Verify triggers match user language patterns

**SKILL.md Too Long**
- Target: under 5,000 tokens (approximately 500-700 lines)
- Solution: Use progressive disclosure (split into multiple .md files in root directory)
- All .md files in root are loaded automatically
- Move detailed specs to reference.md or domain-specific .md files
- Move examples to examples.md
- Keep workflow in SKILL.md with clear references

**Description Too Vague**
- Must include both "what" and "when"
- Add 3-5 specific trigger keywords
- Include data formats: "JSON files", "API responses", ".md files"
- Include task types: "analyzing", "validating", "processing", "creating"
- Include domain terms: "Claude Code", "agent skills", "YAML frontmatter"

**File Not Found Errors**
- Check all referenced files exist
- Verify paths use forward slashes (Key Principle #4)
- Verify references are one level deep (no file-to-file chains)
- Check for typos in file names
- Ensure scripts have correct file extensions (.py, .js, .sh)

**allowed-tools Not Working**
- Verify comma-separated format: `allowed-tools: Read, Grep, Glob`
- Check tool names are exact (case-sensitive)
- Confirm YAML syntax is valid (no tabs, proper indentation)
- Remove allowed-tools field if not needed (defaults to all tools)

**Skill Too Verbose**
- Remove information Claude already knows (basic programming, standard libraries)
- Keep only company-specific or proprietary knowledge
- Delete redundant explanations
- Challenge every paragraph: "Does Claude need this?"

## Output Format

When completing skill management tasks, provide:

1. **Summary**: Brief overview of what was done
2. **Files Created/Modified**: List with locations
3. **Key Features**: Highlight important aspects
4. **Usage Guidance**: How to use the new/updated skill
5. **Next Steps**: Testing recommendations or follow-up actions
