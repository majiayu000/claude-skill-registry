---
name: skill-maker
description: Generate new Claude Code skills with proper structure and standards. Use when the user requests skill creation, wants to generate a new skill, or mentions creating custom Claude Code functionality. Activated by phrases like "create a skill", "generate a skill", "make a new skill", or "build a skill for".
---

# Skill Maker

## Purpose

This skill generates properly structured Claude Code skills following official documentation standards. It ensures all generated skills conform to required conventions, including YAML frontmatter syntax, directory organization, naming conventions, and quality standards.

## Instructions

When invoked, execute the following systematic procedure:

### 1. Requirements Gathering Phase

Before generating any skill, collect the following essential information through structured inquiry:

**Required Information**:
- **Primary Function**: What is the core capability or task the skill shall perform?
- **Activation Triggers**: What keywords, file types, or contexts should invoke this skill?
- **Tool Requirements**: Which Claude Code tools are necessary? (Read, Write, Edit, Bash, Grep, Glob, WebFetch, Task, etc.)
- **External Dependencies**: Does the skill require external packages, libraries, or system utilities?
- **Scope Boundaries**: What is explicitly out-of-scope for this skill?

**Clarifying Questions to Ask When Information is Insufficient**:

If the user provides a vague or incomplete request, employ targeted questioning:

1. **Functional Clarity**:
   - "What specific problem or task shall this skill address?"
   - "What inputs will the skill receive, and what outputs should it produce?"
   - "Are there existing workflows or examples that illustrate the desired functionality?"

2. **Activation Context**:
   - "What phrases or keywords should trigger this skill's activation?"
   - "Are there specific file types or extensions associated with this skill?"
   - "In what project contexts would this skill be most useful?"

3. **Tool Restrictions**:
   - "Should this skill have unrestricted tool access, or require limitations?"
   - "Are there security considerations requiring tool restrictions?"
   - "Does the skill need to modify files, or is read-only access sufficient?"

4. **Dependencies and Prerequisites**:
   - "Does this functionality require external libraries or system commands?"
   - "Are there platform-specific considerations (Windows, macOS, Linux)?"
   - "What should occur if dependencies are not installed?"

5. **Scope Refinement**:
   - "Should this skill handle error cases, or focus on the primary workflow?"
   - "Are there edge cases or variations that require explicit handling?"
   - "Would this skill benefit from additional reference documentation or examples?"

### 2. Skill Design Phase

Based on gathered requirements, formulate the skill architecture:

**Name Generation**:
- Convert functional description to kebab-case format
- Ensure maximum 64-character length
- Use descriptive, domain-relevant terminology
- Examples: `pdf-processor`, `code-reviewer`, `api-client-generator`

**Description Engineering**:
- Maximum 1024 characters
- Include explicit functional capabilities
- Specify clear activation triggers with domain terminology
- Reference file types, tool categories, or operational contexts
- Follow pattern: "[What it does]. Use when [activation scenarios]."

**Tool Selection**:
- Identify minimum required tool set for functionality
- Apply `allowed-tools` restriction if security or scope dictates
- Omit `allowed-tools` field for unrestricted access

**File Structure Planning**:
- `SKILL.md`: Always required (primary skill definition)
- `reference.md`: Optional (for advanced usage, detailed API documentation)
- `examples.md`: Optional (for comprehensive usage examples)
- `scripts/`: Optional (for helper utilities or automation scripts)
- `templates/`: Optional (for reusable file templates or scaffolding)

### 3. Skill Generation Phase

Create the skill files systematically:

**Step 3.1**: Create skill directory structure
```bash
mkdir -p .claude/skills/[skill-name]
```

**Step 3.2**: Generate SKILL.md with valid YAML frontmatter

Ensure strict adherence to syntax:
- Opening delimiter `---` on line 1
- Closing delimiter `---` before markdown content
- Valid YAML formatting (spaces only, no tabs)
- Properly quoted strings containing special characters

**Step 3.3**: Compose instructional content

Instructions section shall employ:
- Numbered procedural steps for sequential operations
- Code examples with explicit syntax
- Expected input/output specifications
- Error handling guidance where relevant
- Clear, unambiguous language suitable for model execution

**Step 3.4**: Generate supporting files (if applicable)

Create `reference.md`, `examples.md`, or utility scripts as determined during design phase.

### 4. Validation Phase

Verify generated artifacts against quality standards:

**Syntax Validation**:
- YAML frontmatter parseable without errors
- Name field conforms to naming conventions
- Description within character limits
- File paths use forward slashes exclusively

**Functionality Validation**:
- Instructions provide clear procedural guidance
- Examples demonstrate realistic usage scenarios
- Tool selections appropriate for stated functionality
- Dependencies explicitly documented

**Quality Validation**:
- Description includes both functional and trigger specifications
- Scope appropriately focused (singular capability)
- Instructions maintain pedagogical clarity
- Supporting files referenced correctly

### 5. Delivery Phase

Present the generated skill to the user with the following information:

**Confirmation Message Template**:
```
Skill "[skill-name]" has been successfully generated at:
.claude/skills/[skill-name]/

**Generated Files**:
- SKILL.md (primary skill definition)
[List additional files if created]

**Activation**: This skill will activate when [describe trigger conditions].

**Next Steps**:
1. Review the generated SKILL.md for accuracy
2. Test activation by formulating queries matching the description triggers
3. Modify instructions if refinements are necessary
4. Add supporting files (reference.md, examples.md) if desired

**Verification Command**:
cat .claude/skills/[skill-name]/SKILL.md
```

## Quality Standards Enforcement

All generated skills shall conform to the following non-negotiable requirements:

1. **Valid YAML Syntax**: Frontmatter must parse without errors
2. **Naming Compliance**: Kebab-case, descriptive, ≤64 characters
3. **Description Specificity**: Must include functional capabilities AND activation triggers
4. **Instructional Clarity**: Procedural steps sufficiently detailed for autonomous execution
5. **File Path Conventions**: Forward slashes exclusively
6. **Dependency Documentation**: External requirements explicitly stated
7. **Focused Scope**: Singular, well-defined capability per skill

## Error Handling

If skill generation encounters issues:

1. **Insufficient Information**: Return to Requirements Gathering Phase with targeted questions
2. **Naming Conflicts**: Check for existing skill with same name; propose alternative
3. **Validation Failures**: Report specific issues (YAML syntax errors, description deficiencies)
4. **Tool Uncertainty**: Request clarification on required capabilities

## Meta-Considerations

This skill-maker itself serves as an exemplar of proper skill construction:
- Focused singular purpose (skill generation)
- Comprehensive description with activation triggers
- Systematic procedural instructions
- Quality validation requirements
- Clear user communication protocols

## Examples

### Example 1: User Provides Complete Specification

**User Request**: "Create a skill for processing CSV files - reading, analyzing, and transforming tabular data. Should activate on CSV-related queries."

**Skill-Maker Response**:
- Directly proceed to generation (sufficient information provided)
- Generate skill named `csv-processor`
- Include Read, Bash tools
- Document pandas/csv module dependencies

### Example 2: User Provides Vague Specification

**User Request**: "Make a skill for documentation."

**Skill-Maker Response**:
- Ask: "What type of documentation should this skill handle? (API docs, README files, code comments, markdown files, etc.)"
- Ask: "What operations should it perform? (generate, validate, transform, extract, etc.)"
- Ask: "What file formats are relevant? (.md, .rst, .html, .pdf, etc.)"
- Await user clarification before proceeding to generation

### Example 3: Security-Sensitive Skill

**User Request**: "Create a skill for analyzing log files without modifying them."

**Skill-Maker Response**:
- Generate with `allowed-tools: Read, Grep, Bash` restriction
- Explicitly document read-only constraint in instructions
- Include validation step preventing write operations

## References

This skill implements standards derived from official Claude Code documentation:
- [Agent Skills Documentation](https://code.claude.com/docs/en/skills.md)

For advanced customization of generated skills, consult the official documentation for:
- Complex tool restriction patterns
- Plugin-based skill distribution
- Multi-file skill architectures
- Integration with MCP servers
