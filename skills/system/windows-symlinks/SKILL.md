---
name: windows-symlinks
description: Create directory junctions and symbolic links in Windows without admin privileges. Use when user wants to create symlinks, mirror directories, sync folders, or create directory links in Windows. Handles both junctions (no admin required) and symlinks (admin required).
license: MIT
---

# Windows Directory Junctions & Symbolic Links

Create and manage directory junctions and symbolic links in Windows environments. Junctions provide symlink-like functionality without requiring administrator privileges.

**Requirements:** Windows Vista or later (junctions), Windows 10+ recommended

## Quick Reference

**Junction (No admin required):**

```powershell
New-Item -ItemType Junction -Path 'target\path' -Target (Resolve-Path 'source\path').Path
```

**Symbolic Link (Admin required):**

```powershell
New-Item -ItemType SymbolicLink -Path 'target\path' -Target 'source\path'
```

## Key Differences

| Feature          | Junction                  | Symbolic Link       |
| ---------------- | ------------------------- | ------------------- |
| Admin privileges | Not required              | Required            |
| Works with       | Directories only          | Files & directories |
| Cross-volume     | No                        | Yes                 |
| Relative paths   | No                        | Yes                 |
| Best for         | Local directory mirroring | Flexible linking    |

## Common Patterns

### Pattern 1: Single Junction Creation

Create one junction pointing to a source directory:

```powershell
# Remove existing directory if needed
Remove-Item -Recurse -Force '.\.target\dir' -ErrorAction SilentlyContinue

# Create junction
New-Item -ItemType Junction -Path '.\.target\dir' -Target (Resolve-Path '.\.source\dir').Path
```

**Expected output:**

```
    Directory: G:\path\to\project

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d----l        25/01/2026     15:21                .target
```

Note: The `l` in `d----l` indicates a link.

**Expected output:**

```
    Directory: G:\path\to\project

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d----l        25/01/2026     15:21                .target
```

Note: The `l` in `d----l` indicates a link.

**Use case:** Mirroring a configuration directory to multiple locations (e.g., `.agent/skills` → `.agents/skills`)

### Pattern 2: Multiple Junctions to Same Source

Create multiple junctions all pointing to one source directory:

```bash
cd /path/to/project && powershell -Command "
  Remove-Item -Recurse -Force '.\.agent\skills' -ErrorAction SilentlyContinue;
  New-Item -ItemType Junction -Path '.\.agent\skills' -Target (Resolve-Path '.\.agents\skills').Path;
  Remove-Item -Recurse -Force '.\.cursor\skills' -ErrorAction SilentlyContinue;
  New-Item -ItemType Junction -Path '.\.cursor\skills' -Target (Resolve-Path '.\.agents\skills').Path;
  Remove-Item -Recurse -Force '.\.github\skills' -ErrorAction SilentlyContinue;
  New-Item -ItemType Junction -Path '.\.github\skills' -Target (Resolve-Path '.\.agents\skills').Path
"
```

**Use case:** Synchronizing skill directories across multiple tool configurations (e.g., Cursor, GitHub Copilot, custom agents)

### Pattern 3: Verify Junction Creation

Check that junctions point to the correct source:

```bash
# List junction details
ls -la .agent/skills
ls -la .cursor/skills

# Verify content matches
ls .agents/skills
ls .agent/skills
```

## Verify Junction Works

**Quick Verification:**

```bash
# List junction details (Git Bash)
ls -la .agent/skills

# Check content matches source
ls .agents/skills
ls .agent/skills
```

**PowerShell Verification:**

```powershell
# Check junction properties
Get-Item '.\agent\skills' | Select-Object LinkType, Target

# Compare directory contents
Compare-Object (Get-ChildItem '.\agents\skills') (Get-ChildItem '.\agent\skills')
# No output = directories match perfectly
```

**Bidirectional Test:**

```bash
# Create file through junction
echo "test" > .agent/skills/test.txt

# Verify it appears in source
ls .agents/skills/test.txt
# Should exist!

# Cleanup
rm .agents/skills/test.txt
```

## Error Handling

### Already Exists Error

```
NewItemIOError: ResourceExists
```

**Solution:** Remove the existing item first with `-ErrorAction SilentlyContinue`

### Permission Denied (Symlinks Only)

```
PermissionDenied: NewItemSymbolicLinkElevationRequired
```

**Solution:** Either:

1. Use junctions instead (`-ItemType Junction`)
2. Run PowerShell as administrator
3. Enable Developer Mode in Windows Settings → Update & Security → For Developers

### Path Not Found

```
Resolve-Path: PathNotFound
```

**Solution:** Ensure source path exists before creating junction

## Verify Junction Works

**Quick Verification:**

```bash
# List junction details (Git Bash)
ls -la .agent/skills

# Check content matches source
ls .agents/skills
ls .agent/skills
```

**PowerShell Verification:**

```powershell
# Check junction properties
Get-Item '.\agent\skills' | Select-Object LinkType, Target

# Compare directory contents
Compare-Object (Get-ChildItem '.\agents\skills') (Get-ChildItem '.\agent\skills')
# No output = directories match perfectly
```

**Bidirectional Test:**

```bash
# Create file through junction
echo "test" > .agent/skills/test.txt

# Verify it appears in source
ls .agents/skills/test.txt
# Should exist!

# Cleanup
rm .agents/skills/test.txt
```

## Best Practices

1. **Prefer junctions for local directory mirroring** - No admin required, simpler to manage
2. **Use absolute paths with Resolve-Path** - Ensures consistent behavior across environments
3. **Clean up before creating** - Remove existing directories/junctions with `-ErrorAction SilentlyContinue`
4. **Verify after creation** - List junction contents to confirm it points correctly
5. **Document the setup** - Note which directories are junctions in project README

## Complete Workflow Example

When user requests: "Create symlinks for my skill directories from .agents to .agent, .cursor, .github, and .opencode"

```bash
cd /path/to/project && powershell -Command "
  # .agent junction
  Remove-Item -Recurse -Force '.\.agent\skills' -ErrorAction SilentlyContinue;
  New-Item -ItemType Junction -Path '.\.agent\skills' -Target (Resolve-Path '.\.agents\skills').Path;

  # .cursor junction
  Remove-Item -Recurse -Force '.\.cursor\skills' -ErrorAction SilentlyContinue;
  New-Item -ItemType Junction -Path '.\.cursor\skills' -Target (Resolve-Path '.\.agents\skills').Path;

  # .github junction
  Remove-Item -Recurse -Force '.\.github\skills' -ErrorAction SilentlyContinue;
  New-Item -ItemType Junction -Path '.\.github\skills' -Target (Resolve-Path '.\.agents\skills').Path;

  # .opencode junction
  Remove-Item -Recurse -Force '.\.opencode\skills' -ErrorAction SilentlyContinue;
  New-Item -ItemType Junction -Path '.\.opencode\skills' -Target (Resolve-Path '.\.agents\skills').Path
"

# Verify all junctions
ls -la .agent/skills .cursor/skills .github/skills .opencode/skills
```

**Result:** All tool-specific skill directories now mirror `.agents/skills`. Any changes to the source directory automatically appear in all locations.

## Git Considerations

Junctions appear as regular directories in Git. To avoid committing duplicate content:

1. **Add junctions to .gitignore:**

   ```gitignore
   .agent/skills
   .cursor/skills
   .github/skills
   .opencode/skills
   ```

2. **Commit only the source directory:**

   ```gitignore
   # Commit this
   .agents/skills/

   # Ignore these (junctions)
   .agent/skills
   .cursor/skills
   .github/skills
   .opencode/skills
   ```

3. **Document setup in README** so team members know to recreate junctions after clone

## Troubleshooting

**Q: Junction shows as symlink in Git Bash but isn't working**  
A: This is normal. Git Bash shows junctions as symlinks (`lrwxrwxrwx`). PowerShell correctly identifies them as `LinkType: Junction`. Verify functionality by listing contents or using PowerShell's `Get-Item` command.

**Q: Changes in junction don't appear in source**  
A: Junctions are bidirectional. Changes in either location affect both. Verify with `ls` commands.

**Q: Can I create junctions across drives?**  
A: No, junctions only work within the same volume. Use symbolic links (requires admin) for cross-drive linking.

**Q: How do I remove a junction?**  
A: Use `Remove-Item` like any directory. This removes the junction but leaves the source intact:

```powershell
Remove-Item '.\.agent\skills'
```

**⚠️ Never use `-Recurse` flag** - this would delete all the source directory contents!

**Q: Do junctions have performance overhead?**  
A: No. Junctions have no performance penalty. File operations through junctions are just as fast as accessing the source directly.
