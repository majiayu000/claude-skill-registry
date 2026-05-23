---
name: commit-validator
description: Validates commit messages against Conventional Commits specification using programmatic validation. Replaces the git-conventional-commit-messages text file with a tool that provides instant feedback.
version: 1.0.0
model: haiku
invoked_by: both
user_invocable: true
tools: [Read, Grep, Bash]
best_practices:
  - Validate early in pre-commit hooks
  - Provide clear error messages
  - Enforce in CI/CD pipelines
error_handling: graceful
streaming: supported
---

<identity>
Commit Message Validator - Programmatically validates commit messages against the [Conventional Commits](https://www.conventionalcommits.org/) specification.
</identity>

<capabilities>
- Before committing code
- In pre-commit hooks
- In CI/CD pipelines
- During code review
- To enforce team standards
</capabilities>

<instructions>
<execution_process>

### Step 1: Validate Commit Message

Validate a commit message string against Conventional Commits format:

**Format**: `<type>(<scope>): <subject>`

**Types**:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes
- `build`: Build system changes
- `revert`: Reverting a previous commit

**Validation Rules**:

1. Must start with type (required)
2. Scope is optional (in parentheses)
3. Subject is required (after colon and space)
4. Use imperative, present tense ("add" not "added")
5. Don't capitalize first letter
6. No period at end
7. Can include body and footer (separated by blank line)
   </execution_process>
   </instructions>

<examples>
<code_example>
**Implementation**

Use this regex pattern for validation:

```javascript
const CONVENTIONAL_COMMIT_REGEX =
  /^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\(.+\))?: .{1,72}/;

function validateCommitMessage(message) {
  const lines = message.trim().split('\n');
  const header = lines[0];

  // Check format
  if (!CONVENTIONAL_COMMIT_REGEX.test(header)) {
    return {
      valid: false,
      error: 'Commit message does not follow Conventional Commits format',
    };
  }

  // Check length
  if (header.length > 72) {
    return {
      valid: false,
      error: 'Commit header exceeds 72 characters',
    };
  }

  return { valid: true };
}
```

</code_example>

<code_example>
**Valid Examples**:

```
feat(auth): add OAuth2 login support
fix(api): resolve timeout issue in user endpoint
docs(readme): update installation instructions
refactor(components): extract common button logic
test(utils): add unit tests for date formatting
```

</code_example>

<code_example>
**Invalid Examples**:

```
Added new feature  # Missing type
feat:new feature   # Missing space after colon
FEAT: Add feature  # Type should be lowercase
feat: Added feature  # Should use imperative tense
```

</code_example>

<code_example>
**Pre-commit Hook** (`.git/hooks/pre-commit`):

```bash
#!/bin/bash
commit_msg=$(git log -1 --pretty=%B)
if ! node .claude/tools/validate-commit.mjs "$commit_msg"; then
  echo "Commit message validation failed"
  exit 1
fi
```

</code_example>

<code_example>
**CI/CD Integration**:

```yaml
# .github/workflows/validate-commits.yml
- name: Validate commit messages
  run: |
    git log origin/main..HEAD --pretty=%B | while read msg; do
      node .claude/tools/validate-commit.mjs "$msg" || exit 1
    done
```

</code_example>
</examples>

<examples>
<formatting_example>
**Output Format**

Returns structured validation result:

```json
{
  "valid": true,
  "type": "feat",
  "scope": "auth",
  "subject": "add OAuth2 login support",
  "warnings": []
}
```

Or for invalid messages:

```json
{
  "valid": false,
  "error": "Commit message does not follow Conventional Commits format",
  "suggestions": [
    "Use format: <type>(<scope>): <subject>",
    "Valid types: feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert"
  ]
}
```

</formatting_example>
</examples>

<examples>
<usage_example>
**Example Commands**:

```bash
# Validate a commit message
node .claude/tools/validate-commit.mjs "feat(auth): implement jwt login"

# Validate from stdin (e.g. in a hook)
echo "fix: incorrect variable name" | node .claude/tools/validate-commit.mjs
```

</usage_example>
</examples>

<instructions>
<best_practices>
1. **Validate Early**: Check commit messages before pushing
2. **Provide Feedback**: Show clear error messages with suggestions
3. **Enforce in CI**: Add validation to CI/CD pipelines
4. **Team Training**: Educate team on Conventional Commits format
5. **Tool Integration**: Integrate with Git hooks and IDEs
</best_practices>
</instructions>

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
