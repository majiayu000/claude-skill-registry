---
context: fork
---

# /rename

Batch rename files matching a pattern, with automatic wiki-link updates.

## Usage

```
/rename <pattern> --remove-prefix "<prefix>"
/rename <pattern> --add-prefix "<prefix>"
/rename <pattern> --replace "<old>" "<new>"
/rename type:<type> --remove-prefix "<prefix>"
/rename --dry-run <any of above>
```

## Examples

```
/rename "Person - *.md" --remove-prefix "Person - "
/rename type:Person --remove-prefix "Person - "
/rename "Meeting - *.md" --replace "Meeting -" "Mtg -"
/rename "Task - *.md" --add-prefix "TODO - "
/rename --dry-run type:Person --remove-prefix "Person - "
```

## Instructions

1. **Parse the command** for:
   - **pattern**: Glob pattern or `type:<type>` to match files
   - **operation**: One of:
     - `--remove-prefix "<prefix>"`: Remove prefix from filenames
     - `--add-prefix "<prefix>"`: Add prefix to filenames
     - `--replace "<old>" "<new>"`: Replace text in filenames
   - **--dry-run**: Preview changes without applying them

2. **Find matching files**:
   - If glob pattern: Use Glob tool to find matching files
   - If `type:<type>`: Search for files with that frontmatter type
   - Exclude templates, MOCs, and special files

3. **Calculate new names**:
   - Apply the requested transformation
   - Sanitise filenames (remove invalid characters)
   - Check for conflicts with existing files
   - Handle duplicates by adding suffix

4. **Preview changes** (always show first):
   ```
   Files to rename: 45

   Examples:
     Person - Jane Doe.md → Jane Doe.md
     Person - Sarah Jones.md → Sarah Jones.md
     ...

   Proceed? (yes/no)
   ```

5. **Update wiki-links** (critical step):
   - Search all vault files for links to renamed files
   - Update `[[Old Name]]` → `[[New Name]]`
   - Update `[[Old Name|alias]]` → `[[New Name|alias]]`
   - Handle both with and without .md extension

6. **Perform renames**:
   - Rename files using git mv (preserves history)
   - Report success/failure for each file
   - Summarise total changes

7. **Post-rename report**:
   ```
   Renamed: 45 files
   Links updated: 127 references in 34 files
   Errors: 0
   ```

## Safety Features

- **Always preview first**: Shows all changes before applying
- **Dry-run mode**: Use `--dry-run` to see changes without applying
- **Git integration**: Uses `git mv` to preserve file history
- **Link updates**: Automatically updates all wiki-links
- **Conflict detection**: Warns if new name already exists
- **Rollback info**: Shows git command to undo if needed

## Common Use Cases

### Remove type prefixes (recommended for cleaner links)
```
/rename type:Person --remove-prefix "Person - "
/rename type:Organisation --remove-prefix "Organisation - "
```

### Standardise naming conventions
```
/rename "Mtg - *.md" --replace "Mtg - " "Meeting - "
/rename "Todo - *.md" --replace "Todo - " "Task - "
```

### Add prefixes to organise
```
/rename type:Adr --add-prefix "ADR - "
```

## Implementation Notes

When executing this skill:

1. **For finding by type**, use:
   ```bash
   grep -l "^type: Person" *.md
   ```
   Or use Grep tool with pattern `^type: Person$`

2. **For updating links**, search for:
   - `[[Old Filename]]`
   - `[[Old Filename|`
   - `[[Old Filename#`

3. **For renaming**, prefer:
   ```bash
   git mv "Old Name.md" "New Name.md"
   ```
   This preserves git history.

4. **For bulk operations**, process in batches to avoid overwhelming the system.

## Related

- [[Page - Claude Code Skills Guide]] - Full skills documentation
- `/orphans` - Find unlinked notes after renaming
- `/broken-links` - Find broken links after renaming
