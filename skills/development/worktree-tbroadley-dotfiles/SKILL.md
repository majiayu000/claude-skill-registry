---
name: worktree
description: This skill should be used when the user asks to "create a worktree", "add a worktree", "set up a worktree", mentions "git worktree", or wants to work on multiple branches simultaneously.
user-invocable: true
---

# Create Git Worktree

This skill creates git worktrees in a standardized location with proper DVC configuration.

## When to Use

Use this skill when the user:
- Asks to create a new git worktree
- Wants to work on multiple branches simultaneously
- Mentions "git worktree add" or similar

## Worktree Location

All worktrees are created under `.worktrees/` in the repository root:
```
repo/
├── .worktrees/
│   ├── feature-branch-1/
│   └── feature-branch-2/
├── src/
└── ...
```

## Instructions

### 1. Determine the Repository Root

Find the git repository root:
```bash
git rev-parse --show-toplevel
```

### 2. Create the Worktrees Directory

Ensure the `.worktrees` directory exists:
```bash
mkdir -p "$(git rev-parse --show-toplevel)/.worktrees"
```

### 3. Create the Worktree

Create the worktree with the specified branch:
```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
git worktree add "$REPO_ROOT/.worktrees/<branch-name>" <branch-name>
```

If creating a new branch:
```bash
git worktree add -b <new-branch-name> "$REPO_ROOT/.worktrees/<new-branch-name>"
```

### 4. Copy .env File

Copy `.env` from the project root to the worktree so environment variables are available:

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
WORKTREE_PATH="$REPO_ROOT/.worktrees/<branch-name>"

# Copy .env if it exists
[ -f "$REPO_ROOT/.env" ] && cp "$REPO_ROOT/.env" "$WORKTREE_PATH/"
```

### 5. Handle DVC Configuration (if applicable)

Check if the repository uses DVC by looking for `.dvc/` directory:
```bash
if [ -d "$(git rev-parse --show-toplevel)/.dvc" ]; then
    echo "DVC detected"
fi
```

If DVC is present and `.dvc/config.local` exists, copy and update it:

1. Copy the local config:
```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
WORKTREE_PATH="$REPO_ROOT/.worktrees/<branch-name>"
cp "$REPO_ROOT/.dvc/config.local" "$WORKTREE_PATH/.dvc/config.local"
```

2. Update the cache directory to point to the main repo's cache:
```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
WORKTREE_PATH="$REPO_ROOT/.worktrees/<branch-name>"
cat > "$WORKTREE_PATH/.dvc/config.local" << EOF
[cache]
    dir = $REPO_ROOT/.dvc/cache
EOF
```

Note: If the original `.dvc/config.local` contains other settings beyond cache configuration, preserve those settings and only update/add the cache dir setting.

## Complete Example

Creating a worktree for branch `feature/new-api`:

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
BRANCH_NAME="feature/new-api"
WORKTREE_DIR="$REPO_ROOT/.worktrees/$BRANCH_NAME"

mkdir -p "$REPO_ROOT/.worktrees"
git worktree add "$WORKTREE_DIR" "$BRANCH_NAME"

# Copy .env if it exists
[ -f "$REPO_ROOT/.env" ] && cp "$REPO_ROOT/.env" "$WORKTREE_DIR/"

if [ -f "$REPO_ROOT/.dvc/config.local" ]; then
    mkdir -p "$WORKTREE_DIR/.dvc"
    cat > "$WORKTREE_DIR/.dvc/config.local" << EOF
[cache]
    dir = $REPO_ROOT/.dvc/cache
EOF
fi

echo "Worktree created at: $WORKTREE_DIR"
```

## Notes

- Worktree names typically match branch names, with slashes replaced by the filesystem
- The `.worktrees/` directory should be added to `.gitignore` if not already
- Use `git worktree list` to see all worktrees
- Use `git worktree remove <path>` to remove a worktree
