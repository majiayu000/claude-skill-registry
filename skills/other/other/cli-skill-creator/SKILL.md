---
name: cli-skill-creator
description: This skill should be used when creating a skill for a CLI tool. Use when users ask to document a command-line tool, create CLI guidance, or build a skill for terminal commands. Essential for systematically introspecting CLI tools through help text, man pages, GitHub repos, and online research, then organizing findings into effective skill documentation.
---

# CLI Skill Creator

## Overview

This skill guides the creation of comprehensive skills for command-line interface (CLI) tools. It provides a systematic workflow for introspecting CLI tools through multiple sources (help text, manual pages, GitHub repositories, online research), extracting mental models and command patterns, and organizing findings into effective skill documentation using the skill-creator skill.

## When to Use This Skill

Invoke this skill when users:

- Ask to create a skill for a CLI tool (e.g., "Create a skill for docker", "Document kubectl")
- Request comprehensive CLI documentation or guidance
- Want to understand a CLI tool's mental model and structure
- Need to organize CLI knowledge for consistent use
- Ask about documenting command-line tools systematically

## Core Workflow

Creating a CLI skill follows a systematic seven-step process that gathers comprehensive information before organizing it into skill documentation.

### Step 1: CLI Identification & Availability Check

**Objectives:**

- Verify CLI tool is installed or accessible
- Determine tool version and variant
- Identify documentation sources
- Assess open-source availability

**Actions:**

1. **Check installation and version**

   ```bash
   <cli-tool> --version
   which <cli-tool>
   ```

2. **Identify tool characteristics**
   - Name and official name (if different)
   - Current version
   - Primary purpose/domain
   - Open source or proprietary

3. **Locate documentation sources**
   - Official website/documentation
   - GitHub repository (if open source)
   - Man pages availability
   - Community resources

**Output:** Tool profile including version, purpose, and available documentation sources.

### Step 2: Comprehensive Help Text Introspection

**Objectives:**

- Map command hierarchy and structure
- Extract all commands, subcommands, and flags
- Capture examples from help text
- Identify command patterns (verb-noun, noun-verb, flat)

**Reference:** Load `references/help-text-patterns.md` for detailed parsing guidance.

**Actions:**

1. **Extract top-level help**

   ```bash
   <cli-tool> --help
   <cli-tool> -h
   <cli-tool> help
   <cli-tool>  # (no args, if applicable)
   ```

2. **Map command hierarchy**
   - Identify all subcommands
   - Determine nesting depth
   - Note command organization pattern

3. **Document each command/subcommand**

   ```bash
   # For each discovered command
   <cli-tool> <command> --help
   <cli-tool> <command> <subcommand> --help
   ```

4. **Extract key information**
   - Command purpose and description
   - Required vs optional arguments
   - Flags and their descriptions
   - Usage examples
   - Default behaviors

5. **Identify patterns**
   - Flag naming conventions
   - Argument patterns
   - Output format options
   - Common options across commands

**Output:** Structured command reference with hierarchy, all commands documented, examples extracted, and patterns identified.

### Step 3: GitHub Repository Analysis (if open-source)

**Objectives:**

- Understand implementation patterns
- Find real-world usage examples
- Identify common user pain points
- Discover undocumented features or gotchas

**Reference:** Load `references/help-text-patterns.md` section "GitHub Repository Analysis" for detailed guidance.

**Actions:**

1. **Clone repository** (if accessible and reasonable size)

   ```bash
   git clone --depth 1 https://github.com/<org>/<repo>
   ```

2. **Examine documentation structure**
   - README.md - Quick start, core concepts
   - docs/ or doc/ - Detailed documentation
   - examples/ - Usage examples
   - CONTRIBUTING.md - Development patterns
   - man/ - Man page sources

3. **Analyze code structure**
   - CLI framework used (Cobra, Click, Commander, Clap, etc.)
   - Command file organization
   - Main entry point
   - Subcommand implementations

4. **Review tests for usage patterns**
   - Integration tests show common workflows
   - Unit tests reveal edge cases
   - Test fixtures show example inputs
   - Assertions reveal expected outputs

5. **Mine issues and discussions**
   - Search for `label:question` - Common user questions
   - Search for `label:documentation` - Doc gaps
   - Look for "How do I..." - Workflow questions
   - Find repeated issues - Common pain points

6. **Check shell completions** (reveal command structure)
   - completions/ or scripts/ directory
   - Shell completion files show all commands/flags

**Output:** Implementation insights, real-world usage examples, common pain points, and undocumented behaviors.

### Step 4: Manual Page Parsing (if available)

**Objectives:**

- Extract comprehensive command documentation
- Capture formal syntax descriptions
- Identify related commands
- Note historical context or design rationale

**Reference:** Load `references/help-text-patterns.md` section "Manual Page Parsing" for detailed guidance.

**Actions:**

1. **Check man page availability**

   ```bash
   man <cli-tool>
   man -k <cli-tool>  # Search for related pages
   ```

2. **Extract key sections**
   - NAME - Command identity
   - SYNOPSIS - Formal syntax
   - DESCRIPTION - Detailed explanation
   - OPTIONS - Comprehensive flag documentation
   - EXAMPLES - Usage examples
   - SEE ALSO - Related commands
   - BUGS - Known issues

3. **Export for analysis**

   ```bash
   # Export to plain text
   man <cli-tool> | col -b > man_<cli-tool>.txt

   # Extract specific sections
   man <cli-tool> | grep -A 50 "^OPTIONS"
   man <cli-tool> | grep -A 30 "^EXAMPLES"
   ```

4. **Check for subcommand man pages**
   ```bash
   man <cli-tool>-<subcommand>
   ```

**Output:** Formal command documentation, comprehensive option descriptions, and usage examples from man pages.

### Step 5: Online Research & Best Practices

**Objectives:**

- Discover community best practices
- Find common workflows and patterns
- Identify integration points with other tools
- Learn from tutorials and guides

**Actions:**

1. **Search for official documentation**
   - Official website documentation
   - API documentation (if CLI wraps an API)
   - Architecture guides
   - Best practices guides

2. **Find community resources**
   - Blog posts about advanced usage
   - Tutorial sites (Medium, Dev.to, etc.)
   - Video tutorials (YouTube)
   - Conference talks

3. **Check Q&A sites**
   - Stack Overflow common questions
   - Reddit discussions
   - GitHub Discussions
   - Tool-specific forums

4. **Identify integration patterns**
   - How does it work with Git?
   - CI/CD integration patterns
   - Editor/IDE integrations
   - Companion tools

5. **Look for comparisons**
   - "X vs Y" articles (reveals strengths/differences)
   - Migration guides (reveals mental model differences)
   - "Awesome X" lists (reveals ecosystem)

**Output:** Community best practices, common workflows, integration patterns, and ecosystem understanding.

### Step 6: Material Organization & Structure Design

**Objectives:**

- Synthesize findings into coherent mental model
- Identify command structure pattern
- Organize content by user task/workflow
- Determine skill structure (workflow-based, command-based, etc.)

**Reference:** Load `references/skill-templates.md` for guidance.

**Actions:**

1. **Extract core mental model**
   - What are the fundamental concepts? (resources, actions, state)
   - How does the tool want users to think?
   - What abstractions does it use?
   - What's the command hierarchy philosophy?

2. **Identify command structure pattern**
   - Flat (single-level commands)
   - Noun-Verb (resource-action)
   - Verb-Noun (action-resource)
   - Hybrid (mix of patterns)

3. **Map common workflows**
   - What are the 5-10 most common tasks?
   - What's the getting-started workflow?
   - What are the advanced workflows?
   - What operations are risky/destructive?

4. **Organize findings by category**
   - Core concepts and terminology
   - Command reference (grouped logically)
   - Workflow patterns (numbered for reference)
   - Configuration and setup
   - Integration patterns
   - Troubleshooting common issues

5. **Choose skill structure** (load `references/skill-templates.md`)
   - **Workflow-based**: For sequential, process-oriented tools
   - **Command-based**: For tools with many discrete operations
   - **Hybrid**: Combine patterns (most common)

6. **Decide what goes where**
   - **skill.md**: Overview, core concepts, common operations, when to load references
   - **references/<tool>\_reference.md**: Complete command reference, all workflows, detailed examples
   - Additional reference files if needed (e.g., for GraphQL API, specialized features)

**Output:** Structured content outline organized by user task/workflow, clear mental model summary, and skill structure plan.

### Step 7: Invoke skill-creator Skill

**Objectives:**

- Generate skill directory structure
- Create skill.md and reference documentation
- Package skill for distribution
- Validate completeness

**Actions:**

1. **Prepare structured brief for skill-creator**

   Organize all gathered material into a comprehensive brief including:
   - **CLI Profile**
     - Name, version, purpose
     - Command structure pattern
     - Open source status and GitHub URL

   - **Core Mental Model**
     - Fundamental concepts (2-5 key concepts)
     - How users should think about the tool
     - Key terminology and definitions

   - **Command Reference Material**
     - Organized by category/domain
     - All commands with syntax and examples
     - Common flags and options
     - Command relationships

   - **Workflow Patterns**
     - 5-10 common workflows
     - Step-by-step with commands
     - When to use each pattern

   - **Integration Points**
     - Other tools it works with
     - CI/CD integration
     - File formats, protocols

   - **Configuration**
     - Config file locations
     - Key settings
     - Environment variables

   - **Troubleshooting**
     - Common issues and solutions
     - Diagnostic commands
     - Error patterns

2. **Invoke skill-creator skill**

   Use the Skill tool to invoke skill-creator:

   ```
   Skill: skill-creator

   Prompt: Create a skill for <cli-tool-name> with the following structure and content:

   [Provide the complete structured brief from step 1]

   Structure the skill using [workflow-based/command-based/hybrid] approach.

   The skill.md should include:
   - Overview and when to use this skill
   - Core concepts: [list key concepts]
   - Common operations organized by [category structure]
   - Reference to comprehensive command reference in references/

   Create references/<tool>_reference.md with:
   - Complete mental model explanation
   - Full command reference organized by [organization scheme]
   - Workflow patterns 1-N
   - Configuration, integration, and troubleshooting sections

   Follow the patterns from existing CLI skills like gh, graphite, and erk.
   ```

3. **Review generated skill**
   - Check skill.md structure and clarity
   - Verify reference documentation completeness
   - Ensure examples are accurate
   - Test commands if possible

4. **Iterate if needed**
   - Refine unclear sections
   - Add missing examples
   - Improve organization
   - Fill gaps in documentation

5. **Package skill** (if ready for distribution)
   ```bash
   python scripts/package_skill.py .claude/skills/<cli-tool-name>
   ```

**Output:** Complete, packaged skill ready for use and distribution.

## CLI Introspection Techniques

### Help Text Parsing Strategies

**Progressive help discovery:**

1. Start with top-level help to understand overall structure
2. Enumerate all subcommands
3. Get help for each subcommand
4. Identify nested subcommands
5. Document all discovered commands

**Information extraction:**

- **Command syntax**: Usage line shows required vs optional
- **Descriptions**: What each command/flag does
- **Examples**: Copy verbatim from help text
- **Defaults**: Note default values for flags
- **Aliases**: Note short forms (e.g., `-h` for `--help`)

**Pattern recognition:**

- Flag naming: Single-letter vs long-form consistency
- Argument conventions: `<required>` vs `[optional]`
- Subcommand organization: Grouped by domain/resource
- Output options: `--json`, `--plain`, `--format`

Load `references/help-text-patterns.md` for comprehensive parsing guidance including regex patterns, format variations, and special cases.

### GitHub Analysis Strategies

**Quick reconnaissance:**

- README.md overview
- Documentation directory structure
- Examples directory
- Contributing guide

**Deep analysis:**

- Command implementation files (reveals structure)
- Test files (reveals usage patterns)
- Issues (reveals pain points)
- Discussions (reveals community questions)

**Framework detection:**

Different CLI frameworks reveal structure differently:

- **Cobra (Go)**: `cmd/` directory with file per command
- **Click (Python)**: Decorators on functions
- **Commander (Node.js)**: Fluent API chains
- **Clap (Rust)**: Struct definitions or builder pattern

Load `references/help-text-patterns.md` section "GitHub Repository Analysis" for detailed code reading strategies.

### Mental Model Extraction

**Ask these questions while introspecting:**

1. **Core abstractions**: What are the primary "things" this CLI manipulates?
2. **Action patterns**: What verbs/actions does it support?
3. **State management**: Does it track state? Where?
4. **Hierarchy**: Is there a parent-child relationship between concepts?
5. **Workflows**: What are the common sequences of operations?

**Look for explicit mental model explanations:**

- README "How it works" sections
- Documentation "Concepts" pages
- Architecture diagrams
- Design rationale documents

**Infer from command structure:**

- Noun-verb suggests resource-oriented model
- Verb-noun suggests action-oriented model
- Flat structure suggests simple, single-purpose tool
- Deep nesting suggests complex domain model

## Skill Structure Guidance

### Choosing the Right Structure

Load `references/skill-templates.md` for complete templates and examples.

**Workflow-based** (use when):

- Clear sequential processes
- Most tasks follow similar steps
- Getting-started focus important
- Example: Deployment tools, CI/CD tools

**Command-based** (use when):

- Many discrete, independent operations
- Users need command reference
- Operations don't follow fixed sequence
- Example: File manipulation tools, utilities

**Hybrid** (use when - most common):

- Mix of common workflows and discrete operations
- Need both getting-started and comprehensive reference
- Example: gh, docker, kubectl, git

### Content Distribution: skill.md vs references/

**skill.md should contain:**

- Clear description triggering skill use
- Overview of tool purpose
- Core concepts (2-5 key concepts)
- When to load references
- Common operations (high-level guidance)
- Workflow decision guidance
- Integration overview

**references/<tool>\_reference.md should contain:**

- Comprehensive mental model
- Complete command reference
- All workflow patterns (numbered)
- Full configuration documentation
- Detailed troubleshooting
- Integration details
- Advanced usage

**Additional reference files (when needed):**

- Separate file for specialized APIs (e.g., GraphQL)
- Separate file for large schema references
- Separate file for extensive configuration options

### Organizing Command Reference

**Best practices:**

1. **Group by domain/resource** (not alphabetically)
   - Groups related commands together
   - Matches user mental model
   - Example: "Pull Request Commands", "Issue Commands"

2. **Order by frequency of use**
   - Most common operations first
   - Advanced features later
   - Matches progressive learning

3. **Include for each command:**
   - Purpose (one sentence)
   - Syntax with placeholders
   - Key flags (not exhaustive, link to help)
   - 2-3 examples (simple to complex)
   - Related commands

4. **Use consistent formatting:**
   - Code blocks for commands
   - Tables for flag reference
   - Numbered workflows
   - Clear section headers

### Writing Effective Workflow Patterns

**Pattern structure:**

````markdown
### Pattern N: <Descriptive-Name>

**Use case:** When to use this workflow

**Steps:**

1. <Step name>
   <Explanation>
   ```bash
   <command>
````

2. <Next step>
   ...

**Complete example:**

```bash
# <Scenario>
<full-workflow>
```

**Variations:** Alternative approaches

```

**Pattern best practices:**

- Start with most common workflows
- Show realistic examples (not foo/bar)
- Include expected output
- Note side effects or state changes
- Link to related patterns
- Mention prerequisites

Load `references/skill-templates.md` for complete workflow pattern template and examples.

## Integration with skill-creator

This skill gathers and organizes CLI material, then delegates to skill-creator for actual skill generation.

**Workflow:**

1. **cli-skill-creator**: Introspects CLI, extracts patterns, organizes material
2. **Handoff**: Provides structured brief to skill-creator
3. **skill-creator**: Generates skill files, validates, packages

**Structured brief format:**

Provide skill-creator with:
- CLI profile (name, version, purpose, structure pattern)
- Core mental model (concepts, terminology)
- Organized command reference material
- Workflow patterns
- Integration points
- Configuration and troubleshooting

**Invocation:**

Use the Skill tool:
```

Skill: skill-creator

Create a skill for <cli-tool> using the following material:
[Complete structured brief]

Use [workflow-based/command-based/hybrid] structure.
Follow patterns from gh/graphite/erk skills.

```

**Advantages of this approach:**

- Separates introspection from generation
- Leverages skill-creator's validation and packaging
- Maintains consistency with other skills
- Allows iterative refinement

## Tips for Different CLI Types

### Modern Subcommand CLIs (gh, docker, kubectl)

**Focus on:**
- Clear command hierarchy
- Workflow patterns (most important)
- Integration with ecosystems
- Progressive examples

**Structure:** Hybrid (workflows + command reference)

### Simple Utility CLIs (jq, curl, grep)

**Focus on:**
- Core functionality explanation
- Common use cases
- Piping and composition
- Flag combinations

**Structure:** Command-based or simple workflow

### API-Wrapper CLIs (aws, gcloud, heroku)

**Focus on:**
- API mapping
- Authentication patterns
- JSON output handling
- Rate limiting

**Structure:** Command-based with workflow patterns

### Legacy CLIs (tar, find, sed)

**Focus on:**
- Modern usage patterns (not all historical options)
- Common gotchas
- Modern alternatives context
- Safety warnings

**Structure:** Workflow-based (guide away from dangerous patterns)

## Quality Checklist

Before finalizing CLI skill:

- [ ] Captured all major commands and subcommands
- [ ] Documented 5-10 common workflow patterns
- [ ] Extracted core mental model clearly
- [ ] Organized by user task (not alphabetically)
- [ ] Included realistic examples with output
- [ ] Noted integration points
- [ ] Documented common gotchas
- [ ] Verified commands actually work
- [ ] Noted CLI version documented
- [ ] Linked to authoritative documentation
- [ ] Followed structure of gh/graphite/erk skills
- [ ] skill.md is concise (<300 lines)
- [ ] references/ contains comprehensive details

## Common Pitfalls

**Avoid:**

1. **Alphabetical organization** - Organize by task/domain instead
2. **Exhaustive flag documentation** - Link to help, show common flags only
3. **Missing mental model** - Always explain how to think about the tool
4. **No workflow patterns** - Users need task-oriented guidance
5. **Untested examples** - Verify all commands actually work
6. **Version agnostic** - Note which version was documented
7. **Missing integration points** - Document how it works with other tools
8. **Poor skill.md description** - Be specific about when to use skill

## Resources

### references/

This skill includes two comprehensive reference documents:

- **help-text-patterns.md** - Practical guidance for parsing help text, man pages, and GitHub repositories. Load when introspecting CLI tools for comprehensive information extraction.

- **skill-templates.md** - Reusable templates for skill structure, command reference, workflows, and sections. Load when organizing material and structuring skill documentation.

**Loading strategy:**

- Load `help-text-patterns.md` during introspection steps (Steps 2-4)
- Load `skill-templates.md` during organization and structure design (Step 6)

These references ensure consistent, comprehensive CLI skill creation following modern best practices.
```
