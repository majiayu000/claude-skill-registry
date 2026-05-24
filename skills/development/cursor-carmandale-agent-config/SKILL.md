---
name: cursor
description: "Control Cursor AI code editor via CLI. Open files, folders, diffs, and manage extensions."
---

# Cursor Skill

Use the `cursor` CLI to control the Cursor AI-powered code editor (VS Code fork).

## CLI Location

```bash
/usr/local/bin/cursor
```

## Opening Files and Folders

Open current directory:
```bash
cursor .
```

Open specific file:
```bash
cursor /path/to/file.ts
```

Open file at specific line:
```bash
cursor /path/to/file.ts:42
```

Open file at line and column:
```bash
cursor /path/to/file.ts:42:10
```

Open folder:
```bash
cursor /path/to/project
```

Open multiple files:
```bash
cursor file1.ts file2.ts file3.ts
```

## Window Options

Open in new window:
```bash
cursor -n /path/to/project
```

Open in new window (alias):
```bash
cursor --new-window /path/to/project
```

Reuse existing window:
```bash
cursor -r /path/to/file
```

Reuse existing window (alias):
```bash
cursor --reuse-window /path/to/file
```

## Diff Mode

Compare two files:
```bash
cursor -d file1.ts file2.ts
```

Diff (alias):
```bash
cursor --diff file1.ts file2.ts
```

## Wait Mode

Wait for file to close (useful in scripts):
```bash
cursor --wait /path/to/file
```

Short form:
```bash
cursor -w /path/to/file
```

Use as git editor:
```bash
git config --global core.editor "cursor --wait"
```

## Adding to Workspace

Add folder to current workspace:
```bash
cursor --add /path/to/folder
```

## Extensions

List installed extensions:
```bash
cursor --list-extensions
```

Install extension:
```bash
cursor --install-extension <extension-id>
```

Uninstall extension:
```bash
cursor --uninstall-extension <extension-id>
```

Disable all extensions:
```bash
cursor --disable-extensions
```

## Verbose and Debugging

Show version:
```bash
cursor --version
```

Show help:
```bash
cursor --help
```

Verbose output:
```bash
cursor --verbose /path/to/file
```

Open developer tools:
```bash
cursor --inspect-extensions
```

## Settings

User settings location:
```
~/Library/Application Support/Cursor/User/settings.json
```

Keybindings location:
```
~/Library/Application Support/Cursor/User/keybindings.json
```

## Portable Mode / Profiles

Specify user data directory:
```bash
cursor --user-data-dir /path/to/data
```

Specify extensions directory:
```bash
cursor --extensions-dir /path/to/extensions
```

## Piping Input

Read from stdin:
```bash
echo "console.log('hello')" | cursor -
```

## Remote Development

Cursor supports remote development similar to VS Code. SSH remotes are configured in:
```
~/.ssh/config
```

Then use command palette or remote explorer in the GUI.
