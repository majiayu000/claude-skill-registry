---
name: import-github-dirs
description: Import specific directories from external GitHub repos without cloning. Uses tarball extraction to pull only what you need. TRIGGER when user wants to copy files/folders from another repo.
---

# Import GitHub Directories

## TRIGGER CONDITIONS

USE when:
- "bring in files from [repo]"
- "import directories from GitHub"
- Copying code from external repos

SKIP when:
- User wants to clone entire repo
- Just need single file (use raw URL instead)

## One-Command Import

```bash
curl -L https://github.com/{owner}/{repo}/tarball/{branch} | \
  tar -xz --strip-components=1 --wildcards '*/{dir1}/*' '*/{dir2}/*'
```

## Examples

Single directory:
```bash
curl -L https://github.com/rjs/shaping-skills/tarball/main | \
  tar -xz --strip-components=1 --wildcards '*/shaping/*'
```

Multiple directories:
```bash
curl -L https://github.com/rjs/shaping-skills/tarball/main | \
  tar -xz --strip-components=1 --wildcards '*/breadboarding/*' '*/shaping/*'
```

## How It Works

- HTTP download of tarball (no git operations)
- `--strip-components=1` removes root folder
- `--wildcards` extracts only matching paths
- Files land in current directory, ready to move/stage/commit
