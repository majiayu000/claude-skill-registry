---
name: managing-slash-commands
description: Creates, analyzes, updates, and improves slash commands including YAML frontmatter, argument handling, and command authoring workflows. Use when user asks how slash commands work, explaining command syntax and arguments, understanding command structure, describing command vs skill differences, asked to create a new slash command, evaluate existing commands for improvements, optimize commands for effectiveness, suggest converting current logic into a command, update outdated command information, or when user mentions command validation, best practices, or supporting files.
---

# Managing Slash Commands

This skill enables comprehensive management of slash commands including creation, analysis, improvement, and maintenance.

## When to Use This Skill

Activate this skill when:
- User requests creation of a new slash command
- User asks to analyze or evaluate an existing slash command
- User inquires whether current conversation logic should become a slash command
- User requests updates to outdated slash command information
- User mentions "slash command", "command file", "/command" in context of creation/improvement
- You identify that a simple, reusable prompt would benefit from being a slash command

## Core Workflows

### Workflow 1: Creating a New Slash Command

When creating a new slash command, follow this structured approach:

#### Step 1: Requirements Gathering
- Identify the command's primary purpose
- Determine if it needs arguments ($ARGUMENTS, $1, $2, etc.)
- Assess if bash execution is needed (! prefix)
- Verify this should be a command, not a skill (simple prompt vs. complex workflow)
- Load creation-guide.md for detailed decision matrix

#### Step 2: Command Design
- Choose descriptive command name (lowercase-with-hyphens, verb-noun format preferred)
- Write the prompt content (clear, direct instructions)
- Plan frontmatter fields:
  - description: Brief explanation for /help display
  - allowed-tools: If bash execution needed
  - argument-hint: Document expected arguments
  - model: If specific model required
  - (optional) Include thinking keywords if extended reasoning needed
- Determine argument pattern (none, $ARGUMENTS, or $1/$2/etc.)

#### Step 3: Implementation
- Choose location:
  - Project: `.claude/commands/` (team-shared)
  - Personal: `~/.claude/commands/` (user-specific)
- Use Write tool to create command-name.md file
- Add YAML frontmatter if needed (optional for simple commands)
- Write prompt content following best practices from best-practices.md
- Use Read tool to verify created file

#### Step 4: Validation
- Use Quick Validation Checklist (below) for validation
- Load validation-checklist.md for comprehensive validation if needed

#### Step 5: Testing
- For script-based commands: test script independently first
- If Python script: consider using python-best-practices skill to validate script quality
- If prompt content is complex: consider using managing-prompts skill to validate prompt engineering
- Test invocation: /command-name [args]
- Verify argument substitution works correctly
- Check bash execution if applicable
- Validate output matches expectations
- Test edge cases (missing arguments, invalid input, etc.)

### Workflow 2: Analyzing Existing Slash Commands

When evaluating an existing slash command for improvements:

#### Step 1: Load and Review
- Use Read tool to read the complete command file
- Identify frontmatter fields present
- Check for argument usage patterns
- Note bash execution patterns
- List any file references (@file.txt)

#### Step 2: Evaluate Quality
Load best-practices.md and evaluate:
- **Clarity**: Is the prompt clear and direct?
- **Specificity**: Does it provide enough context?
- **Arguments**: Are arguments used effectively?
- **Frontmatter**: Is metadata appropriate and complete?
- **Bash Usage**: Are bash commands necessary and properly restricted?
- **Prompt Engineering**: Does it follow Claude best practices?
  - For comprehensive prompt analysis, consider using managing-prompts skill

#### Step 3: Identify Improvements
Categorize findings:
- **Critical Issues**: Broken syntax, invalid YAML, security concerns
- **Major Improvements**: Unclear prompt, missing description, poor argument handling
- **Minor Enhancements**: Better wording, examples in comments, clearer structure

#### Step 4: Recommendations
Provide specific, actionable suggestions:
- What to change
- Why it improves the command
- How to implement the change
- Priority level (critical/major/minor)

### Workflow 3: Suggesting Command vs. Skill Conversion

When evaluating whether current logic should become a command or skill:

#### Decision Criteria
Use this checklist to decide:

**Choose Slash Command If**:
- [ ] Simple, single prompt (1-2 steps)
- [ ] No supporting files/scripts needed
- [ ] User wants explicit control (manual invocation)
- [ ] Quick template or reminder
- [ ] One file is sufficient

**Choose Skill If**:
- [ ] Complex workflow (3+ steps with validation)
- [ ] Multiple supporting files needed
- [ ] Should activate automatically based on context
- [ ] Domain expertise or structured process required
- [ ] Team needs standardized multi-step approach

**Decision Rule**: If 3+ "Choose Skill" criteria met, recommend skill instead.

#### Conversion Process
If recommending slash command:
1. Identify the reusable prompt pattern
2. Determine argument needs
3. Explain benefits of command approach
4. Outline proposed command structure
5. Offer to create the command if user agrees

If recommending skill:
1. Explain why complexity warrants a skill
2. Suggest using managing-agent-skills skill
3. Outline skill structure benefits

### Workflow 4: Updating Outdated Slash Commands

When updating existing slash commands:

#### Step 1: Identify Outdated Content
- Deprecated tools or features mentioned
- Outdated best practices
- Changed documentation URLs
- New argument patterns available
- Updated model names

#### Step 2: Plan Updates
- Preserve working functionality
- Update tool restrictions if needed
- Modernize prompt engineering approach
  - Consider using managing-prompts skill to apply latest Claude best practices
- Add missing frontmatter fields
- Improve argument handling

#### Step 3: Implement Changes
- Use Edit tool to modify command file
- Update frontmatter if needed
- Revise prompt content
- Test updated command
- Verify all references still valid

#### Step 4: Document Changes
- Note what was updated in comments if significant
- Update description in frontmatter
- Ensure argument-hint reflects current usage

## Progressive Disclosure References

For detailed guidance, refer to these supporting files:

- **best-practices.md**: Comprehensive best practices for command authoring
- **creation-guide.md**: Step-by-step guide with decision matrix and examples
- **validation-checklist.md**: Validation rules for syntax, structure, and quality
- **examples.md**: Annotated command examples from Claude cookbooks
- **argument-patterns.md**: Patterns for handling arguments effectively
- **slashcommand-tool-reference.md**: Reference for SlashCommand tool, plugin commands, and MCP commands (advanced features for programmatic invocation and ecosystem integration)
- **templates/command-template.md**: Template for new command files

Load these files only when detailed guidance is needed for specific tasks.

## Related Skills Integration

This skill integrates with other specialized skills for comprehensive command development:

- **python-best-practices**: Use when creating slash commands with Python helper scripts. Validates script quality, coding standards, and maintainability. Referenced in Testing workflow (Step 5) and Tool Usage Patterns.
- **managing-prompts**: Use when creating or analyzing prompt content within slash commands. Provides Claude prompt engineering, guardrails, context optimization, and hallucination prevention. Referenced in Testing (Step 5), Analysis (Workflow 2), and Updates (Workflow 4).
- **managing-plugins**: Provides detailed information on plugin command structure, distribution, and plugin-scoped command creation. Reference when creating commands for plugin distribution or when working with plugin namespacing (`plugin-name:command-name` pattern).
- **managing-mcps**: Covers MCP server setup, prompt exposure, and MCP command discovery patterns. Reference when working with MCP-exposed commands or when designing commands to complement MCP server capabilities.

## Command Storage Locations

Choose appropriate location:
- **Personal commands**: `~/.claude/commands/` - User-specific, experimental, individual use
- **Project commands**: `.claude/commands/` - Team-shared, committed to git, standardized team use
- **Namespacing**: Use subdirectories for organization (frontend/, backend/, etc.)

## Key Principles

1. **Simplicity**: Commands are for simple, reusable prompts. Complex workflows need skills.
2. **Clarity**: Direct, clear instructions following Claude best practices.
3. **Manual Invocation**: Users explicitly call commands; use skills for automatic activation.
4. **Single File**: One command = one markdown file. No multi-file orchestration.
5. **Arguments**: Use when prompt needs user-provided values ($1, $2, or $ARGUMENTS).
6. **Extended Thinking**: Commands support extended thinking by including thinking keywords for complex reasoning tasks.
7. **Security**: Restrict allowed-tools appropriately for bash execution.

## Using Helper Scripts with Slash Commands

### When to Use Scripts vs Interpreted Logic

Some slash commands benefit from delegating work to Python scripts instead of having Claude interpret and execute logic on every invocation.

#### Use Helper Scripts When:

**Deterministic Operations**:
- Same input always produces same output
- No reasoning or judgment required
- Logic is well-defined and complete

**Context Reduction**:
- Script contains the implementation
- Claude just needs to call the script and format results
- Reduces tokens needed for command execution

**Consistency and Performance**:
- Same analysis every time
- Direct execution vs generating code on the fly
- Complex parsing or analysis (AST traversal, regex patterns)

**Examples of Good Script-Based Commands**:
```bash
# /check-functions - Find functions over length threshold
!python .claude/skills/python-best-practices/scripts/check-function-length.py $1 --threshold 50

# /find-bare-except - Find bare except clauses
!python .claude/skills/python-best-practices/scripts/find-bare-except.py $ARGUMENTS

# /analyze-complexity - Calculate cyclomatic complexity
!python .claude/skills/python-best-practices/scripts/analyze-complexity.py $1
```

#### Keep as Interpreted Logic When:

**Contextual Reasoning**:
- Task requires Claude's judgment or interpretation
- Logic changes based on conversation context
- Natural language understanding needed
- Multiple valid approaches exist

**Flexibility Needed**:
- Output format should adapt to user needs
- Analysis requires explanation and recommendations
- Interactive decision-making required

**Simple Operations**:
- One-time or rare operation
- Trivial logic not worth maintaining a script
- Better expressed as direct prompt

**Examples of Good Interpreted Commands**:
```markdown
# /review-pr - Review pull request (needs judgment)
Review the code changes in this pull request and provide feedback on code quality,
potential bugs, and suggestions for improvement.

# /explain-code - Explain code (needs natural language)
Explain what the following code does in simple terms: $ARGUMENTS

# /suggest-refactor - Suggest refactoring (needs reasoning)
Analyze this code and suggest refactoring opportunities with explanations.
```

### Script Organization

**Location**: Store helper scripts in skill directories or dedicated scripts folder:
```
.claude/
  commands/
    check-functions.md          # Command file
  skills/
    python-best-practices/
      scripts/
        check-function-length.py   # Helper script
        find-bare-except.py
        analyze-complexity.py
  scripts/                       # Alternative: shared scripts
    code-analysis/
      check-function-length.py
```

**Command Structure with Scripts**:
```markdown
---
description: Find Python functions exceeding length threshold
argument-hint: <file_path> [--threshold N]
allowed-tools: Bash
---

!python .claude/skills/python-best-practices/scripts/check-function-length.py $ARGUMENTS

After running the script, format the results and provide recommendations for refactoring
any functions that exceed the threshold.
```

### Best Practices for Helper Scripts

**Script Design**:
- Clear, focused purpose (one script = one analysis)
- Accept arguments via command line
- Return structured output (JSON or formatted text)
- Exit codes: 0 for success, non-zero for errors
- Include usage documentation in script header

**Error Handling**:
```python
#!/usr/bin/env python3
"""
Find functions exceeding length threshold.
Usage: python check-function-length.py <file> [--threshold N]
"""
import sys
import ast

def main():
    if len(sys.argv) < 2:
        print("Usage: python check-function-length.py <file> [--threshold N]", file=sys.stderr)
        sys.exit(1)

    # Implementation...

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
```

**Output Format**:
- Human-readable by default
- Optional `--json` flag for structured output
- Clear error messages to stderr
- Progress info to stderr, results to stdout

### Decision Framework

Ask these questions:

1. **Is the logic deterministic?**
   - Yes → Consider script
   - No → Interpreted logic

2. **Does it require Claude's reasoning?**
   - Yes → Interpreted logic
   - No → Consider script

3. **Is it reused frequently?**
   - Yes → Script saves context
   - No → Interpreted is fine

4. **Is the logic complex (AST, regex, parsing)?**
   - Yes → Script is more reliable
   - No → Either works

5. **Does output need adaptation?**
   - Yes → Interpreted logic
   - No → Script is consistent

**Rule of thumb**: If you answer "script" to 3+ questions, use a helper script.

## Tool Usage Patterns

When analyzing a command:
1. Use Read tool to read the complete command file
2. Check for YAML frontmatter syntax
3. Identify argument usage patterns
4. Verify bash command restrictions if applicable
5. Check if command uses helper scripts and validate script exists

When creating a command:
1. Use Write tool to create command-name.md file
2. Use Read tool to verify the file after creation
3. Test invocation to ensure it works

When creating a command with helper scripts:
1. Use Write tool to create the script file first
2. Use Bash tool to test script independently
3. If Python script: consider using python-best-practices skill to validate
4. Use Write tool to create command-name.md file
5. If prompt is complex: consider using managing-prompts skill to validate prompt engineering
6. Use Read tool to verify both files
7. Test command invocation end-to-end

When searching for existing commands:
1. Use Glob tool with pattern `**/.claude/commands/**/*.md`
2. Use Grep tool to search for specific patterns in commands
3. Use Read tool to examine candidate commands

## Anti-Patterns to Avoid

- Complex multi-step workflows (use skills instead)
- Multiple supporting files (use skills instead)
- Vague command names like "helper" or "do-thing"
- Missing descriptions in frontmatter
- Overly permissive allowed-tools
- Unrestricted bash execution without allowed-tools
- Commands that should auto-activate (use skills instead)

## Quick Validation Checklist

Before considering a command complete:
- [ ] File named with .md extension
- [ ] Lowercase-with-hyphens naming
- [ ] YAML frontmatter valid if present (delimiters, no tabs)
- [ ] Description clear and helpful (if in frontmatter)
- [ ] Arguments documented in argument-hint (if used)
- [ ] Allowed-tools specified for bash commands (if needed)
- [ ] Helper script exists at specified path (if using !python or !bash)
- [ ] Script tested independently and working (if script-based)
- [ ] Prompt content clear and direct
- [ ] Follows Claude prompting best practices
- [ ] File references use @ prefix correctly
- [ ] Tested and working as expected

## Quick Troubleshooting

Common issues and solutions:

**Command Not Found**
- Check file location: `.claude/commands/` or `~/.claude/commands/`
- Verify .md extension
- Confirm filename matches invocation (lowercase-with-hyphens)
- Restart Claude Code to reload commands

**Arguments Not Substituting**
- Verify placeholder syntax: $1, $2, $ARGUMENTS
- Check for typos in placeholder names
- Test with explicit argument values
- Review argument-hint for documentation

**Bash Commands Not Executing**
- Add allowed-tools in frontmatter
- Prefix bash commands with !
- Verify tool restrictions match actual commands
- Check bash command syntax

**YAML Frontmatter Errors**
- Verify delimiters: `---` at start and end
- Remove tabs (use spaces only)
- Check field syntax: `name: value`
- Validate special characters are quoted if needed

**Command Too Complex**
- Consider converting to skill instead
- Split into multiple simpler commands
- Review decision criteria in Workflow 3
- Load creation-guide.md for guidance

## Output Format

When completing command management tasks, provide:

1. **Summary**: Brief overview of what was done
2. **Files Created/Modified**: List with locations
3. **Key Features**: Highlight important aspects (arguments, bash usage, etc.)
4. **Usage Guidance**: How to invoke the command with examples
5. **Next Steps**: Testing recommendations or follow-up actions
