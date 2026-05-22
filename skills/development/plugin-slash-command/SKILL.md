---
name: plugin-slash-command
description: Generate new Navigator slash commands following project conventions. Use when user says "add slash command", "create command", "new /nav command", or "add /nav:[name] command".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
version: 1.0.0
---

# Navigator Slash Command Generator

Generate new slash commands for the Navigator plugin following established conventions and patterns.

## When to Invoke

Auto-invoke when user says:
- "Add a slash command for..."
- "Create a new /nav:[name] command"
- "Generate slash command..."
- "Add /nav:[feature] command"
- "New Navigator command for..."

## What This Does

1. Asks for command details (name, purpose, complexity)
2. Analyzes existing commands for pattern matching
3. Generates command markdown file with proper structure
4. Validates YAML frontmatter and formatting
5. Shows usage example

## Execution Steps

### Step 1: Gather Command Requirements

Ask user:
- **Command name** (kebab-case, without /nav: prefix)
  - Example: "marker", "compact", "update-doc"
- **Command purpose** (one sentence description)
  - Example: "Create context markers to save conversation state"
- **Command complexity**:
  - Simple: Single action, minimal steps (e.g., marker)
  - Medium: Multiple steps, some logic (e.g., compact)
  - Complex: Multi-phase execution, integrations (e.g., init, start)
- **User-facing or internal**?
  - User-facing: Part of standard Navigator workflow
  - Internal: For plugin development/maintenance

### Step 2: Analyze Similar Commands

Use Task agent to find similar commands:
```
"Find existing Navigator commands similar to [purpose]:
 - Commands in commands/*.md
 - Similar complexity level
 - Common structure patterns
 - Return 2-3 best examples"
```

**What to extract from examples**:
- Section structure (What This Does, When to Use, etc.)
- Tone and style (conversational, 2nd person)
- Emoji usage patterns
- Example format
- Troubleshooting patterns

### Step 3: Design Command Structure

Based on complexity level:

**Simple commands**:
```
- YAML frontmatter (description)
- Title
- What This Does (2-3 sentences)
- Usage (basic syntax + examples)
- When to Use (2-3 scenarios)
- Expected Output
- Troubleshooting (2-3 common issues)
- Closing statement
```

**Medium commands**:
```
- YAML frontmatter
- Title + overview
- What This Does (detailed explanation)
- When to Use (5-6 scenarios with examples)
- Usage / Execution Steps
- Output Format
- Integration notes (if applicable)
- Troubleshooting (4-5 issues)
- Best Practices
- Closing statement
```

**Complex commands**:
```
- YAML frontmatter
- Title + comprehensive overview
- What This Does (with comparisons)
- Execution Plan (multi-step)
- Pre-flight checks
- Step-by-step implementation
- Validation steps
- Integration with PM tools (if applicable)
- Success criteria
- Troubleshooting (comprehensive)
- Edge cases
- Performance notes
- Closing statement
```

### Step 4: Generate Command File

**Use predefined function**: `functions/command_generator.py`

```python
# Generates command markdown following Navigator conventions
generate_command(
    name="[command-name]",
    description="[one-line purpose]",
    complexity="simple|medium|complex",
    sections={
        "what_this_does": "...",
        "when_to_use": [...],
        "usage": "...",
        "execution_steps": [...],
        "troubleshooting": [...]
    }
)
```

**File location**: `commands/[command-name].md`

**Structure**:
1. YAML frontmatter with description
2. Title (# Command Name - Navigator Context)
3. Overview paragraph (what user is doing)
4. Content sections (based on complexity)
5. Closing statement (emoji + key takeaway)

### Step 5: Validate Generated Command

**Use predefined function**: `functions/command_validator.py`

Checks:
- [ ] YAML frontmatter is valid
- [ ] Description field exists and is clear
- [ ] Markdown structure is correct
- [ ] All sections have content
- [ ] Code blocks are properly formatted
- [ ] Examples are realistic
- [ ] Troubleshooting addresses real issues
- [ ] Tone matches Navigator style (conversational, helpful)
- [ ] Emoji usage is consistent with other commands
- [ ] File name matches command name (kebab-case)

### Step 6: Show Usage Example

Display:
```
✅ Slash Command Created: /nav:[command-name]

File: commands/[command-name].md
Lines: [count]
Complexity: [simple/medium/complex]

Try it:
/nav:[command-name]

What it does:
[brief description]

Next steps:
1. Test the command manually
2. Update plugin documentation if public-facing
3. Add to CLAUDE.md command list if needed
```

---

## Example Workflows

### Example 1: Simple Command

**User**: "Add a slash command for showing Navigator version"

**Execution**:

1. **Gather requirements**:
   ```
   Name: version
   Purpose: Display current Navigator plugin version
   Complexity: Simple
   Type: User-facing
   ```

2. **Analyze similar** (via Task agent):
   ```
   Found similar: marker.md (simple, informational)
   Pattern: Short description → Usage → When to use → Output
   ```

3. **Design structure**:
   ```
   - Frontmatter
   - Title: "Navigator Version Info"
   - What This Does: 1 paragraph
   - Usage: Basic syntax
   - When to Use: 2-3 scenarios
   - Output Format: Example
   - Closing statement
   ```

4. **Generate**: `commands/version.md`
   ```markdown
   ---
   description: Display Navigator plugin version and system info
   ---

   # Navigator Version Info

   Check which version of Navigator you're running.

   ## What This Does

   Displays the current Navigator plugin version, Claude Code version, and system configuration.

   ## Usage

   ```bash
   /nav:version
   ```

   ## When to Use

   **Reporting issues**:
   - Include version info in bug reports
   - Help maintainers reproduce issues

   **Checking updates**:
   - See if you're on latest version
   - Compare with marketplace version

   **System diagnostics**:
   - Verify plugin installed correctly
   - Check configuration loaded

   ## Output Format

   ```
   Navigator Plugin
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Version: 2.2.0
   Installed: /Users/you/.claude/plugins/jitd
   Config: .agent/.nav-config.json

   System:
   - Claude Code: 1.5.0
   - Project: /Users/you/project
   - Platform: darwin
   ```

   **Keep your Navigator up to date for latest features** 🚀
   ```

5. **Validate**: ✅ All checks pass

6. **Show usage**:
   ```
   ✅ Slash Command Created: /nav:version

   File: commands/version.md
   Lines: 45
   Complexity: Simple

   Try it: /nav:version
   ```

### Example 2: Medium Command

**User**: "Create a command for archiving old task documentation"

**Execution**:

1. **Gather requirements**:
   ```
   Name: archive-tasks
   Purpose: Move completed tasks to archive directory
   Complexity: Medium (file operations, validation)
   Type: User-facing
   ```

2. **Analyze similar**:
   ```
   Found: markers.md (file management, user selection)
   Found: compact.md (multi-step process)
   Pattern: Overview → Execution Plan → Steps → Validation
   ```

3. **Design structure**:
   ```
   - Frontmatter
   - Title + overview
   - What This Does (comparison with manual approach)
   - When to Use (5 scenarios)
   - Execution Plan (Step 1-4)
   - Output Format
   - Troubleshooting (4 issues)
   - Best Practices
   - Closing
   ```

4. **Generate**: `commands/archive-tasks.md` (full content)

5. **Validate**: ✅ All checks pass

6. **Show usage**: Command ready to use

---

## Output Format

**After generating command, show**:

```
✅ Slash Command Created: /nav:[name]

Structure:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 commands/[name].md

Sections:
✅ YAML frontmatter
✅ Title and overview
✅ What This Does
✅ When to Use ([N] scenarios)
✅ Usage / Execution Plan
✅ [Additional sections based on complexity]
✅ Troubleshooting
✅ Closing statement
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Command: /nav:[name]
Purpose: [brief description]
Lines: [count]

Test it:
/nav:[name]

Documentation:
- Add to README.md if user-facing
- Update CLAUDE.md command list
- Add to plugin.json if needed
```

---

## Best Practices

### Command Naming
- Use kebab-case (marker, update-doc, archive-tasks)
- Be specific but concise (not too generic, not too verbose)
- Match feature purpose (nav:compact for compacting)
- Avoid abbreviations unless very common

### Description Writing
- One sentence, clear purpose
- Action-oriented ("Create", "Display", "Update")
- Mention key benefit or what it does
- Under 100 characters

### Content Structure
- Start with user perspective ("You are...")
- Use 2nd person ("your task", "you can")
- Include realistic examples
- Show expected output
- Address common issues in troubleshooting

### Tone and Style
- Conversational and helpful
- Use emojis for visual markers (✅❌📖🚀)
- Bold key terms and actions
- Code blocks for all commands/output
- Bullet lists for readability

### Examples Quality
- Real-world scenarios (not toy examples)
- Show before/after when relevant
- Include expected output
- Cover common use cases
- Demonstrate Navigator benefits

### Troubleshooting Section
- Address real issues users might encounter
- Provide specific solutions (not generic advice)
- Include verification commands
- Link to related docs if helpful

---

## Common Command Patterns

### Informational Commands
**Pattern**: Simple structure, quick output
**Examples**: version, status, list
**Sections**: Description → Usage → Output

### Action Commands
**Pattern**: Execute something, show result
**Examples**: marker, compact, archive
**Sections**: Description → Execution → Validation → Result

### Setup/Configuration Commands
**Pattern**: Multi-step process, checks
**Examples**: init, migrate, setup
**Sections**: Pre-flight → Steps → Validation → Troubleshooting

### Management Commands
**Pattern**: User selection, operations, feedback
**Examples**: markers (list/load), tasks (list/select)
**Sections**: Overview → Modes → Operations → Results

---

## Troubleshooting

### Generated Command Too Short

**Problem**: Command content is sparse, missing sections

**Solutions**:
1. Increase complexity level (simple → medium)
2. Add more scenarios to "When to Use"
3. Expand troubleshooting section (more common issues)
4. Add Best Practices section
5. Include more examples

### Command Doesn't Match Navigator Style

**Problem**: Tone or structure feels off

**Solutions**:
1. Re-analyze example commands (marker.md, compact.md)
2. Check emoji usage (should match existing patterns)
3. Verify 2nd person perspective ("You are...")
4. Ensure conversational tone (not technical manual)
5. Add personality to closing statement

### YAML Validation Fails

**Problem**: Invalid frontmatter

**Solutions**:
1. Check YAML syntax (proper indentation)
2. Ensure `description` field exists
3. Verify no special characters break parsing
4. Test with: `python -c "import yaml; yaml.safe_load(open('commands/[name].md').read().split('---')[1])"`

### Examples Are Too Generic

**Problem**: Examples don't feel realistic

**Solutions**:
1. Base examples on actual Navigator usage
2. Use real file paths (not /path/to/file)
3. Show actual output format (not [output here])
4. Include context (why user would run this)

---

## Success Criteria

**This skill succeeds when**:
- [ ] Generated command file is syntactically valid
- [ ] YAML frontmatter passes validation
- [ ] All required sections present
- [ ] Tone matches Navigator style (conversational, helpful)
- [ ] Examples are realistic and useful
- [ ] Troubleshooting addresses real issues
- [ ] Command can be invoked in Claude Code
- [ ] Minimal manual editing needed (<10% of content)

---

**The plugin-slash-command skill automates Navigator command creation, ensuring consistency and saving development time** 🔧
