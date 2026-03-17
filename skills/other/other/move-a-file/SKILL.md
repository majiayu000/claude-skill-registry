---
name: move-a-file
description: Move or rename a file while automatically updating all references in source code and documentation
---

# Move a File

This skill instructs AI agents on how to safely move or rename files in a codebase
while automatically finding and updating all references to the file in source code,
documentation, and configuration files.

## Inputs

The move-a-file skill takes the following inputs:
- **Old file path**: The current path of the file to move/rename (relative to project root)
- **New file path**: The destination path for the file (relative to project root)
- **Context**: Any additional context about what the file contains or why it's being moved

## Workflow for AI Agents

When this skill is invoked, the AI agent **MUST** follow these steps in order:

### 1. Validate File Paths

Before proceeding, verify that:
- The old file path exists
- The new file path's parent directory exists (or can be created)
- The new file path does not already exist (to avoid overwrites)
- Both paths are relative to the project root

If any validation fails, inform the user and abort.

### 2. Search for All References

Use `rg` (ripgrep) or `grep` to find all references to the file across the codebase.

**IMPORTANT**: Search for multiple patterns to catch all references:

1. **Exact filename**: Search for the exact filename (without path)
   ```bash
   rg --type-add 'docs:*.md' --type-add 'config:*.{yaml,yml,json,toml}' \
      -t md -t config -t py -t js -t sh -t c -t cpp \
      "<filename>"
   ```

2. **Full relative path**: Search for the full path from project root
   ```bash
   rg --type-add 'docs:*.md' --type-add 'config:*.{yaml,yml,json,toml}' \
      -t md -t config -t py -t js -t sh -t c -t cpp \
      "<old-path>"
   ```

3. **Path variations**: Search for common path variations
   - With leading `./`: `"./<old-path>"`
   - Without extension (if applicable): `"<path-without-ext>"`
   - In import statements: `"import.*<filename-without-ext>"`

**Search scope**: Include at minimum:
- Source code files (`.py`, `.js`, `.sh`, `.c`, `.cpp`, etc.)
- Documentation files (`.md`, `.txt`, `.rst`)
- Configuration files (`.yaml`, `.yml`, `.json`, `.toml`)
- Build files (`Makefile`, `CMakeLists.txt`, `package.json`)

### 3. Review and Update References

For each file containing a reference:
- Read the file to understand the context
- Determine the correct new path to use (may be relative to that file's location)
- Update the reference using the `Edit` tool
- Report what was changed in that file

**Path calculation rules**:
- For documentation and config files: usually use paths relative to project root
- For import statements: follow the language's import conventions
- For file system operations: may need relative paths from the current file

### 4. Move the File

After updating all references, move the file:
```bash
git mv "<old-path>" "<new-path>"
```

If the parent directory of the new path doesn't exist:
```bash
mkdir -p "$(dirname '<new-path>')" && git mv "<old-path>" "<new-path>"
```

### 5. Verify and Report

After moving the file:
1. Verify the new file exists: `ls "<new-path>"`
2. Report summary to the user:
   - Old path → New path
   - Number of files updated
   - List of updated files with brief description of changes
   - Any references that might need manual review

## Examples

### Example 1: Renaming a Skill File

**Context:** User wants to rename `git-commit/SKILL.md` to `commit-msg/SKILL.md`

**Workflow:**
```
User: Use move-a-file to rename the git-commit skill to commit-msg

Agent: I'll move the file and update all references.

1. Validating paths...
   - Source exists: claude/skills/git-commit/SKILL.md ✓
   - Destination available: claude/skills/commit-msg/SKILL.md ✓

2. Searching for references to "git-commit"...
   Found references in:
   - claude/skills/CLAUDE.md (2 references)
   - claude/commands/README.md (1 reference)
   - README.md (1 reference)

3. Updating references...
   - claude/skills/CLAUDE.md:79 - Updated skill name reference
   - claude/skills/CLAUDE.md:123 - Updated example path
   - claude/commands/README.md:45 - Updated skill link
   - README.md:67 - Updated workflow reference

4. Moving the file...
   [Runs: mkdir -p claude/skills/commit-msg && git mv claude/skills/git-commit/SKILL.md claude/skills/commit-msg/SKILL.md]

5. Summary:
   Moved: claude/skills/git-commit/SKILL.md → claude/skills/commit-msg/SKILL.md
   Updated 4 references across 3 files
```

### Example 2: Moving Documentation File

**Context:** User wants to reorganize docs by moving a file

**Workflow:**
```
User: Move docs/workflow.md to docs/agent/workflow.md

Agent: I'll move the file and update all references.

1. Validating paths...
   - Source exists: docs/workflow.md ✓
   - Creating parent directory: docs/agent/ ✓

2. Searching for references...
   Found references in:
   - README.md (3 references)
   - docs/index.md (1 reference)
   - claude/skills/plan-guideline/SKILL.md (1 reference)

3. Updating references...
   - README.md:23 - Updated link: [workflow](docs/workflow.md) → [workflow](docs/agent/workflow.md)
   - README.md:45 - Updated link in list
   - README.md:89 - Updated reference in text
   - docs/index.md:12 - Updated link
   - claude/skills/plan-guideline/SKILL.md:234 - Updated documentation reference

4. Moving the file...
   [Runs: mkdir -p docs/agent && git mv docs/workflow.md docs/agent/workflow.md]

5. Summary:
   Moved: docs/workflow.md → docs/agent/workflow.md
   Updated 5 references across 3 files
```

### Example 3: No References Found

**Context:** Moving a new file that hasn't been referenced yet

**Workflow:**
```
User: Move temp/draft.md to docs/draft/implementation.md

Agent: I'll move the file and check for references.

1. Validating paths...
   - Source exists: temp/draft.md ✓
   - Creating parent directory: docs/draft/ ✓

2. Searching for references...
   No references found to "draft.md" or "temp/draft.md"

3. Moving the file...
   [Runs: mkdir -p docs/draft && git mv temp/draft.md docs/draft/implementation.md]

4. Summary:
   Moved: temp/draft.md → docs/draft/implementation.md
   No references needed updating
```

## Important Notes

1. **Always use `git mv`**: This preserves file history in git. Never use regular `mv` command.

2. **Case sensitivity**: File systems may be case-insensitive, but git is case-sensitive.
   Be careful when changing only the case of a filename.

3. **Search thoroughly**: Different files may reference the moved file in different ways.
   Use multiple search patterns to catch all variations.

4. **Path relativity**: When updating references, consider whether the reference should be:
   - Relative to project root
   - Relative to the file containing the reference
   - An absolute path

5. **Import statements**: Programming language imports may need special handling:
   - Python: `from module.submodule import file`
   - JavaScript: `import { func } from './path/to/file'`
   - Shell: `source ./path/to/file.sh`

6. **Glob patterns**: Also search for glob patterns that might match the file:
   - `docs/**/*.md` might be used to reference all markdown files
   - These might need updating if the file moves to a different directory structure

7. **Report uncertainty**: If you find a reference that you're unsure how to update,
   include it in the final report and ask the user to review it manually.

8. **Don't move directories**: This skill is for moving individual files only.
   For moving entire directories, the process is more complex and should be handled separately.
