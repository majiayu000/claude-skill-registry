---
name: branch
description: Create git branches with naming conventions (prefix/description-hash)
---

# Branch

Create a branch from the current commit.

- Ensure the repo is clean
- Use a `(branch|feat|fix)/` prefix, defaulting to `branch`
- End the branch with the first 8 chars of the current commit
- After the prefix use `wip` (default), `issue-NNN`, the package being worked on, or a url-compatible description
- If no specific user input, use defaults or infer from current work

## Examples

"Start a branch" => `branch/wip-abcd5678`
"Create a branch for constructs" => `feat/constructs-abcd5678`
"Work 144" => `fix/issue-144`
_No input but previous requests dealt with express and lambda_ => `feat/express-lambda-abcd5678`

## User Input

<input>
$ARGUMENTS
</input>
