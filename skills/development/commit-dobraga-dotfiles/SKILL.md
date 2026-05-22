---
name: commit
description: Analyzes staged changes and generates a high-quality, conventional commit message, then executes the commit.
---

# Smart Commit Skill

When I say "commit this" or "generate a commit message," follow this workflow:

## 1. Intelligence Gathering
* **Run** `git diff --cached` to see exactly what is being committed.
* **Identify Change Type**: Determine if it is a `feat`, `fix`, `docs`, `style`, `refactor`, `test`, or `chore`.
* **Analyze Scope**: Identify the specific module or component affected (e.g., `api`, `models`, `ui`).

## 2. Generate the Message
Follow the **Conventional Commits** specification:

```text
<type>(<scope>): <short summary in imperative mood>

[optional body: explain the WHY, not just the WHAT]

[optional footer: relate to Issue IDs, e.g., Closes #123]

```

don't add Co-Authored-By on message

## 3. Execution

1. **Present** the generated message to the user.
2. **Run** `git commit -m "[message]"` (or `-m "[subject]" -m "[body]"` for multi-line).

## 4. The Gotcha

**Warning**: Remind the user if they are committing too many unrelated changes at once (non-atomic commits). If the diff is too large, suggest splitting it into two separate commits.


### Why this works for you
* **Context Aware**: Because it runs `git diff --cached`, it knows exactly what you've staged, unlike generic AI tools that look at your whole folder.
* **Structured**: It forces the "Conventional Commit" format, which makes your `git log` look professional and machine-readable.

### Example Interaction
**User:** "Claude, commit these Pydantic changes."

**Claude:**
> **Proposed Message**:
> `feat(models): implement Pydantic v2 validation for User schema`
> 
> `Updated UserRecord to inherit from BaseModel and added EmailStr validation for the email field. This prevents malformed data from reaching the service layer.`
>

