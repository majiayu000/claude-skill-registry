---
name: slash-command-creator
description: This skill should be used when users want to create custom slash commands for Claude Code. It guides the creation of project-specific or personal slash commands with proper frontmatter, argument handling, and Claude Code standards.
---

# Slash Command Creator Skill

This skill helps create custom slash commands for Claude Code by analyzing requirements and generating properly formatted command files with appropriate frontmatter, argument handling, and execution logic.

## When to Use This Skill

Use this skill when users say:

- "Create a slash command for..."
- "Help me make a custom command"
- "I need a new slash command that..."
- "Can you create a command to..."

## Command Creation Process

### 1. Analyze Command Requirements

First, understand what the command should do:

- Identify the primary purpose and functionality
- Determine if it needs arguments (positional or all arguments)
- Check if it requires special tools (Bash, Read, Write, etc.)
- Decide if it's a project command (.claude/commands/) or personal command (~/.claude/commands/)

### 2. Determine Command Type

Based on requirements, choose the appropriate command pattern:

**Simple Text Expansion**: No arguments, static prompt

```yaml
---
description: Brief description of the command
---
Static prompt text here
```

**Single Argument**: Uses $ARGUMENTS for all input

```yaml
---
description: Description of what the command does
argument-hint: [optional-hint]
allowed-tools: Tool1, Tool2
---
Process $ARGUMENTS here
```

**Positional Arguments**: Uses $1, $2, etc. for specific parameters

```yaml
---
description: Description with parameter roles
argument-hint: [param1] [param2] [optional-param3]
allowed-tools: Tool1, Tool2
---
Process $1 as first parameter, $2 as second, etc.
```

**Bash Integration**: Execute shell commands with `Exclamation mark` prefix

```yaml
---
allowed-tools: Bash(git:*), Bash(npm:*)
description: Command that needs shell execution
---

## Context
- Git: Exclamation mark`git --help`

## Your task
Execute based on the above context
```

**File References**: Include files with `@` prefix

```yaml
---
description: Command that references files
---
Analyze the implementation in @src/components/Button.tsx
Compare @src/old-file.js with @src/new-file.js
```

### 3. Command Templates

Use these common templates as starting points:

#### Component Testing Command

````markdown
---
description: Run tests for a specific component with coverage and debugging
argument-hint: [component-name] [--coverage] [--debug]
allowed-tools: Bash, Read, Glob
---

# Component Testing

Testing component: $1
Options: $2

## Test Execution

1. Find test files for component: $1
2. Run appropriate test command
3. If --coverage flag, generate coverage report
4. If --debug flag, run in debug mode

## Commands to Execute

```bash
npm test -- --testPathPattern=$1 $2
```
````

Check test results and report any failures.

````

#### API Implementation Command
```markdown
---
description: Implement component using provided curl APIs and response data
argument-hint: [component-name] [api-endpoints]
allowed-tools: Read, Write, Bash, WebFetch
---

# API Component Implementation

Create component: $1
Using APIs: $2

## Implementation Steps

1. Parse the provided curl commands to understand:
   - HTTP methods (GET, POST, PUT, DELETE)
   - Request endpoints
   - Headers and authentication
   - Request body structure

2. Analyze response data to understand:
   - Data structure and types
   - Required fields vs optional
   - Error responses

3. Create React component with:
   - TypeScript interfaces for API responses
   - State management for data fetching
   - Loading and error states
   - Proper API integration

4. Follow project patterns:
   - Use @/ path aliases
   - Apply Mitra theme styling
   - Include proper accessibility
   - Handle edge cases

## API Integration Pattern

```typescript
// Example API integration
interface ApiResponse {
  // Define based on provided response
}

const ComponentName = () => {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Implement API call using provided curl
  }, []);

  // Render component
};
````

````

#### Documentation Generation Command
```markdown
---
description: Generate comprehensive documentation for a component
argument-hint: [component-path] [--include-examples]
allowed-tools: Read, Write, Glob
---

# Component Documentation Generator

Generate docs for: $1
Include examples: $2

## Documentation Structure

1. **Component Analysis**:
   - Read component file(s)
   - Identify props and their types
   - Understand component behavior
   - Note any special requirements

2. **Generate Documentation**:
   - Component description
   - Props interface with types and descriptions
   - Usage examples
   - Accessibility notes
   - Styling customization
   - Dependencies

3. **Create README.md** if it doesn't exist
4. **Update existing README.md** if it exists

## Documentation Template

```markdown
# Component Name

Brief description of what this component does and when to use it.

## Props Interface

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| propName | string | - | Description of the prop |

## Usage Examples

### Basic Usage
\`\`\`tsx
<ComponentName propName="value" />
\`\`\`

### Advanced Usage
\`\`\`tsx
<ComponentName propName="value" optionalProp={true} />
\`\`\`

## Accessibility

- ARIA labels automatically handled
- Keyboard navigation support
- Screen reader compatibility

## Styling & Customization

Uses CSS variables from the Mitra theme:
- `--color-mitra-blue` for primary elements
- Customizable via style prop

## Dependencies

- React hooks: useState, useEffect
- No external dependencies
````

````

#### Issue Fixing Command
```markdown
---
description: Fix a specific issue by number with automated git workflow
argument-hint: [issue-number] [--branch-name]
allowed-tools: Bash, Read, Edit, Write, WebFetch
---

# Issue Fixer

Fixing issue: #$1
Branch name: $2

## Issue Resolution Process

1. **Fetch Issue Details**:
   - Get issue information from GitHub
   - Understand requirements and acceptance criteria
   - Note any related issues or dependencies

2. **Create Feature Branch**:
   ```bash
   git checkout -b fix/issue-$1
````

3. **Implement Fix**:
   - Locate relevant files
   - Implement solution
   - Follow coding standards
   - Add tests if needed

4. **Verify Fix**:
   - Run existing tests
   - Test the specific issue scenario
   - Check for regressions

5. **Commit Changes**:

   ```bash
   git add .
   git commit -m "fix: Resolve issue #$1 - [brief description]"
   git push -u origin fix/issue-$1
   ```

6. **Create Pull Request** (optional):
   - Link to the original issue
   - Include description of changes
   - Request review if needed

```

### 4. Best Practices for Command Creation

**Frontmatter Requirements**:
- Always include `description` (required for SlashCommand tool)
- Use `argument-hint` to show expected arguments in autocomplete
- Specify `allowed-tools` when command needs specific tools
- Use `model` to override default model if needed

**Argument Handling**:
- Use `$ARGUMENTS` for simple, single-parameter commands
- Use positional arguments ($1, $2, etc.) for structured input
- Provide clear hints in `argument-hint` with square brackets
- Use optional arguments sparingly

**Command Quality**:
- Write clear, actionable instructions
- Include examples when helpful
- Handle edge cases and errors
- Follow existing project conventions
- Use imperative language ("Do X" not "You should do X")

**File Organization**:
- Store project commands in `.claude/commands/`
- Store personal commands in `~/.claude/commands/`
- Use kebab-case for file names
- Group related commands in subdirectories

### 5. Command Validation Checklist

Before finalizing a command, verify:

- [ ] Frontmatter includes required fields
- [ ] Argument placeholders are correct ($1, $2, $ARGUMENTS)
- [ ] File references use @ prefix
- [ ] Bash commands use Exclamation mark prefix in allowed sections
- [ ] Tools are properly declared in allowed-tools
- [ ] Description is clear and concise
- [ ] Argument hint shows expected parameters
- [ ] Command follows project naming conventions
- [ ] File is saved in correct location (.claude/commands/ or ~/.claude/commands/)

### 6. Testing Commands

Test newly created commands by:
1. Running `/help` to see the command in the list
2. Executing the command with sample arguments
3. Verifying it works as expected
4. Checking that it appears in available commands for the SlashCommand tool

### 7. Resources Reference

For complex command patterns, refer to:
- `references/slash-command-examples.md` - Collection of advanced command patterns
- `references/api-integration-templates.md` - Templates for API-related commands
- `references/testing-workflows.md` - Testing and QA command patterns

### 8. Scripts Utility

Use the provided scripts for common tasks:
- `scripts/validate-command.js` - Validate command syntax and frontmatter
- `scripts/test-command.js` - Test command execution with sample inputs
- `scripts/generate-template.js` - Generate command templates for specific patterns
```
