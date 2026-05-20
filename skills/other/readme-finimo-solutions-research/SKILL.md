---
name: readme
description: Use when creating, updating, or generating README and documentation files for projects and libraries
version: 1.1.0
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
verified: true
lastVerifiedAt: 2026-02-22T00:00:00.000Z
---

# Readme Skill

<identity>
Readme specialist focused on creating clear, comprehensive README files and project documentation. Helps developers write effective project introductions, setup guides, and usage documentation.
</identity>

<capabilities>
- Generate comprehensive README files from project context
- Create clear installation and setup instructions
- Write usage examples and API documentation
- Document project structure and architecture
- Generate table of contents and navigation
- Create contributing guidelines and troubleshooting sections
- Optimize readability with formatting and visual structure
</capabilities>

## When to Use

Use this skill when:

- Creating a new README or documentation file
- Updating existing README with new features
- Documenting project setup, installation, or configuration
- Writing usage examples and API references
- Generating contributing guidelines or quick-start guides
- Improving documentation clarity and structure

## Core Workflow

### Step 1: Gather Project Information

Analyze the project to understand:

1. **Project Purpose**: What problem does it solve?
2. **Target Audience**: Who are the users (developers, users, contributors)?
3. **Key Features**: What makes this project special?
4. **Technical Stack**: Languages, frameworks, dependencies
5. **Project Structure**: How is code organized?

### Step 2: Create README Structure

Use this standard structure:

```markdown
# Project Name

Brief description (1-2 sentences)

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

[Setup instructions]

## Quick Start

[Basic usage example]

## Documentation

[Link to detailed docs]

## API Reference

[Key endpoints/functions]

## Examples

[Working examples]

## Configuration

[Setup options]

## Troubleshooting

[Common issues and solutions]

## Contributing

[How to contribute]

## License

[License information]
```

### Step 3: Write Clear Content

- **Be specific**: Use concrete examples, not vague descriptions
- **Show, don't tell**: Include code examples and screenshots
- **Progressive disclosure**: Start simple, add complexity gradually
- **Organize logically**: Group related information
- **Use formatting**: Headers, lists, code blocks for readability

### Step 4: Add Examples

Include practical, working examples:

- Installation examples
- Basic usage snippets
- Complex feature demonstrations
- Common use cases
- Copy-paste ready code

### Step 5: Verify Quality

Check before completing:

- [ ] Clear project purpose in first paragraph
- [ ] Installation instructions are complete
- [ ] Examples are runnable
- [ ] Table of contents matches sections
- [ ] All links work
- [ ] Formatting is consistent
- [ ] No typos or grammar errors

## README Components Reference

### Project Title and Description

```markdown
# Project Name

One-liner explaining what this project does.

Long paragraph (2-3 sentences) describing problem solved and approach.
```

### Features Section

```markdown
## Features

- ✅ Feature with emoji for visual interest
- ✅ Key capability with brief description
- ✅ Unique advantage over alternatives
```

### Installation

```markdown
## Installation

### Requirements

- Node.js 18+
- pnpm 8+

### Steps

\`\`\`bash
pnpm install project-name
\`\`\`
```

### Quick Start

Keep this minimal (5-10 lines of code max):

```markdown
## Quick Start

\`\`\`javascript
import { feature } from 'project-name';

const result = feature({ option: 'value' });
console.log(result);
\`\`\`
```

### Examples

Make examples realistic and copy-paste ready:

```markdown
## Examples

### Basic Usage

\`\`\`typescript
// Simple example with real output
const instance = new MyClass();
instance.doSomething(); // Output: expected result
\`\`\`

### Advanced Configuration

\`\`\`typescript
// Complex example showing options
const instance = new MyClass({
option1: true,
option2: 'value'
});
\`\`\`
```

## Best Practices

1. **Lead with value**: First paragraph should answer "why should I use this?"
2. **Show working examples**: Code examples should be runnable
3. **Keep installation simple**: Complex setup gets a dedicated guide
4. **Document dependencies**: List what's required upfront
5. **Include screenshots**: Visual examples for UI projects
6. **Write for skimmers**: Use headers so people can scan content
7. **Link to detailed docs**: README is overview, link to full documentation
8. **Keep it current**: Update README when adding features
9. **Be honest about limitations**: What's not covered or not supported
10. **Include contributing guidelines**: How to report issues or submit PRs

## Anti-Patterns

| Pattern              | Problem               | Fix                               |
| -------------------- | --------------------- | --------------------------------- |
| Wall of text         | Impossible to scan    | Use headers and lists             |
| Missing setup        | Readers can't install | Include step-by-step instructions |
| No examples          | Unclear how to use    | Add working code examples         |
| Outdated info        | Misleads users        | Update with releases              |
| Too detailed         | Overwhelming          | Link to full docs instead         |
| No table of contents | Hard to navigate      | Add section links at top          |
| Broken links         | Poor user experience  | Test all external links           |
| Marketing fluff      | Lacks substance       | Focus on what it does, not hype   |

## Iron Laws

1. **ALWAYS** lead with the value proposition — the first paragraph must answer "what problem does this solve?" before any installation or setup instructions.
2. **NEVER** write a Quick Start section longer than 10 lines — if setup requires more, link to a detailed guide rather than overwhelming the first-time reader.
3. **ALWAYS** include working, copy-paste-ready code examples — non-runnable pseudocode examples are worse than no examples because they waste the reader's time.
4. **NEVER** let a README become stale after a feature release — outdated installation commands and broken examples destroy user trust immediately.
5. **ALWAYS** test all external links and code examples before considering the README complete — dead links and broken examples are the most common README failure mode.

## Anti-Patterns

| Anti-Pattern                                             | Why It Fails                                                             | Correct Approach                                                                 |
| -------------------------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| Starting with a long feature list before the description | Readers don't know what the project is, so features are meaningless      | Lead with a 1-2 sentence value proposition before listing features               |
| Using pseudocode or placeholder examples                 | Forces readers to infer the real API; causes frustration and abandonment | Show actual runnable code with real imports, function names, and expected output |
| Putting a 20-step installation guide in Quick Start      | Overwhelming setup drives users away; contradicts "quick" start          | Quick Start must be 1-3 commands; link detailed setup to a separate guide        |
| Writing marketing copy instead of technical facts        | Vague statements like "blazing fast" give no actionable information      | Use specific claims with data: "reduces build time by 40% (measured on 10k LOC)" |
| Not updating README when features change                 | Outdated commands fail silently; users blame the project, not the docs   | Treat README as code: update it in the same PR as every feature change           |

## Integration Points

**Related Skills**:

- `doc-generator` - Automated documentation from code
- `writing-skills` - Writing quality guidelines
- `technical-writer` - Professional documentation agent

**Related Agents**:

- `technical-writer` - Uses this skill for documentation
- `developer` - Writes README for new projects

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern → `.claude/context/memory/learnings.md`
- Issue found → `.claude/context/memory/issues.md`
- Decision made → `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
