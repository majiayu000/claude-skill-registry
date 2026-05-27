---
name: codex-ask
description: Ask OpenAI Codex questions about code to understand implementations, architecture, patterns, and debugging. Use when the user asks how code works, where something is implemented, what patterns are used, or needs to understand existing code. Requires Codex CLI installed.
allowed-tools: Bash, Read, Grep, Glob
---

# Codex Ask Skill

Use OpenAI Codex CLI to answer questions about code without making modifications. This is a **read-only** analysis skill.

## When to Use

- User asks "how does X work?"
- User wants to find where something is implemented
- User needs to understand architecture or patterns
- User is debugging and needs to understand code flow
- User asks "what does this code do?"

## Prerequisites

Verify Codex CLI is available:

```bash
codex --version  # Should display installed version
```

## Basic Usage

### Step 1: Parse the Question

Extract what the user wants to know. Good questions include:

- File/component context
- Specific functionality
- Desired answer format

### Step 2: Execute Codex Query

Run Codex in read-only mode:

```bash
codex --sandbox=read-only exec "Answer this question about the codebase: [QUESTION]

Provide:
1. Direct answer to the question
2. Specific file paths and line numbers
3. Code examples from the actual codebase
4. Related concepts or dependencies

Do NOT make any changes - this is read-only analysis."
```

### Step 3: Present Answer

Format the response with:

- **Summary**: 1-2 sentence direct answer
- **Details**: In-depth explanation
- **File References**: Specific paths with line numbers
- **Code Examples**: Relevant snippets
- **Related Info**: Dependencies, gotchas, context

## Example Queries

### Understanding Flow

```bash
codex --sandbox=read-only exec "Explain how user authentication works in this app. Include all files involved, the complete flow, and security measures. Do NOT modify code."
```

### Finding Implementation

```bash
codex --sandbox=read-only exec "Where is email validation implemented? Show all locations with file paths and line numbers. Do NOT modify code."
```

### Architecture Questions

```bash
codex --sandbox=read-only exec "What's the overall architecture of this application? Describe patterns used, component organization, and data flow. Do NOT modify code."
```

### Debugging

```bash
codex --sandbox=read-only exec "What could cause 'Cannot read property of undefined' in UserProfile component? Analyze potential causes with specific line references. Do NOT modify code."
```

## Output Format

Structure answers like this:

````markdown
## Answer: [Question]

### Summary

[Direct answer in 1-2 sentences]

### Details

[Comprehensive explanation]

### File References

- `src/auth/login.ts:45-67` - Login handler implementation
- `src/middleware/auth.ts:23` - Authentication middleware

### Code Examples

```typescript
// From src/auth/login.ts:45
export async function handleLogin(credentials: Credentials) {
  // ... code snippet ...
}
```
````

### Related Information

- Uses JWT for token management
- Session timeout is 24 hours
- See `src/config/auth.ts` for configuration

```

## Best Practices

✅ **DO:**
- Always include file paths with line numbers
- Show actual code from the codebase
- Explain "why" not just "what"
- Mention related files or concepts
- Verify Codex returned accurate information

❌ **DON'T:**
- Make or suggest code changes (use codex-exec for that)
- Execute code or run tests
- Modify files
- Assume information without verification

## Verification

After getting Codex's response:
1. Verify file paths exist and are correct
2. Check line numbers are accurate
3. Confirm code examples match current code
4. Add any missing context from your knowledge

## Error Handling

**If Codex not found:**
```

Codex CLI is not available. Ensure it's installed and in your PATH.

```

**If answer is unclear:**
- Ask a more specific question
- Provide more context (file names, features)
- Break complex questions into smaller parts

## Related Skills

- **codex-exec**: For making code changes
- **codex-review**: For code quality assessment

## Tips for Better Results

1. **Be specific**: "How does JWT validation work in auth middleware?" vs "How does auth work?"
2. **Include context**: "In the user registration flow..."
3. **Specify scope**: "Focus on src/components/..."
4. **Request format**: "Explain with code examples and file paths"

## Limitations

- Cannot execute or test code
- Cannot make modifications
- Limited to static code analysis
- May not understand business logic context
- Cannot access external documentation

---

**Remember**: This skill is READ-ONLY. For code modifications, use the `codex-exec` skill.
```
