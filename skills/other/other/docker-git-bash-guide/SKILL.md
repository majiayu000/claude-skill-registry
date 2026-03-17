---
name: docker-git-bash-guide
description: Comprehensive Windows Git Bash and MINGW path conversion guide for Docker volume mounts and commands
---

# Docker on Windows Git Bash / MINGW - Path Conversion Guide

This skill provides comprehensive guidance on handling Docker commands in Git Bash (MINGW) on Windows, with specific focus on volume mount path conversion issues and solutions.

## The Path Conversion Problem

When running Docker commands in Git Bash (MINGW) or MSYS2 on Windows, automatic path conversion can cause serious issues with volume mounts and other Docker commands.

### What Triggers Automatic Conversion

MSYS/MINGW shells automatically convert arguments that look like Unix paths when calling Windows executables (like `docker.exe`):

**Examples of problematic conversions:**
```bash
# What you type:
docker run -v /c/Users/project:/app myimage

# What Docker receives (BROKEN):
docker run -v C:\Program Files\Git\c\Users\project:/app myimage
```

**Triggers for path conversion:**
- Leading forward slash (`/`) in arguments
- Colon-separated path lists (`/foo:/bar`)
- Arguments with path components after `-` or `,`

**What's exempt from conversion:**
- Arguments containing `=` (variable assignments)
- Drive letters (`C:`)
- Arguments with `;` (already Windows format)
- Arguments starting with `//` (network paths/Windows switches)

## Shell Detection for Docker Commands

### Detecting Git Bash / MINGW Environment

Use these environment variables to detect when path conversion issues may occur:

```bash
# Most reliable: Check for MSYSTEM
if [ -n "$MSYSTEM" ]; then
  echo "Running in Git Bash/MINGW - path conversion needed"
fi

# Alternative: Check uname
if [[ "$(uname -s)" == MINGW* ]]; then
  echo "Running in MINGW environment"
fi

# Environment variable to check:
# MSYSTEM values: MINGW64, MINGW32, MSYS
```

## Solution 1: MSYS_NO_PATHCONV (Recommended for Git Bash)

The most reliable solution for Git Bash on Windows.

### Per-Command Usage

Prefix each Docker command with `MSYS_NO_PATHCONV=1`:

```bash
# Volume mount with $(pwd)
MSYS_NO_PATHCONV=1 docker run -v $(pwd):/app myimage

# Volume mount with absolute path
MSYS_NO_PATHCONV=1 docker run -v /c/Users/project:/app myimage

# Multiple volume mounts
MSYS_NO_PATHCONV=1 docker run \
  -v $(pwd)/data:/data \
  -v $(pwd)/config:/etc/config \
  myimage
```

### Shell-Level Configuration

Disable path conversion for all Docker commands in your session:

```bash
# Add to ~/.bashrc or run in current shell
export MSYS_NO_PATHCONV=1

# Now all Docker commands work normally
docker run -v $(pwd):/app myimage
```

### Function Wrapper (Automatic per Docker Command)

Create a function wrapper that automatically disables path conversion:

```bash
# Add to ~/.bashrc
docker() {
  (export MSYS_NO_PATHCONV=1; command docker.exe "$@")
}

# Or using MSYS2_ARG_CONV_EXCL for MSYS2
docker() {
  (export MSYS2_ARG_CONV_EXCL='*'; command docker.exe "$@")
}

# Make function available in subshells
export -f docker
```

## Solution 2: MSYS2_ARG_CONV_EXCL (MSYS2 Specific)

For MSYS2 environments (not standard Git Bash):

```bash
# Disable all argument conversion
export MSYS2_ARG_CONV_EXCL='*'

# Selective exclusion (specific patterns)
export MSYS2_ARG_CONV_EXCL='--dir=;/test'

# Environment variable conversion exclusion
export MSYS2_ENV_CONV_EXCL='*'
```

## Solution 3: Double Leading Slash

Prefix paths with an extra `/` to prevent conversion:

```bash
# Single slash (converted - BROKEN)
docker run -v /c/Users/project:/app myimage

# Double slash (not converted - WORKS)
docker run -v //c/Users/project:/app myimage

# Works in Git Bash on Windows
# Treated as single slash on Linux (portable)
```

**Advantages:**
- No environment variables needed
- Works without wrapper functions
- Portable (extra slash ignored on Linux)

**Disadvantages:**
- Less readable
- Easy to forget
- Doesn't look like standard Docker syntax

## Solution 4: Use $(pwd) with Proper Escaping

Always use lowercase `$(pwd)` (not `$PWD`) with proper syntax:

```bash
# CORRECT: Round brackets, lowercase pwd, no quotes
MSYS_NO_PATHCONV=1 docker run -v $(pwd):/app myimage

# CORRECT: With subdirectories
MSYS_NO_PATHCONV=1 docker run -v $(pwd)/src:/app/src myimage

# WRONG: Uppercase PWD variable (may not convert correctly)
docker run -v $PWD:/app myimage

# WRONG: Without MSYS_NO_PATHCONV (path gets mangled)
docker run -v $(pwd):/app myimage
```

## Docker Volume Mount Best Practices (Git Bash on Windows)

### For docker run Commands

```bash
# Named volumes (no path conversion issue)
docker run -v my-named-volume:/data myimage

# Bind mount with MSYS_NO_PATHCONV (RECOMMENDED)
MSYS_NO_PATHCONV=1 docker run -v $(pwd):/app myimage

# Bind mount with double slash (ALTERNATIVE)
docker run -v //c/Users/project:/app myimage

# Read-only bind mount
MSYS_NO_PATHCONV=1 docker run -v $(pwd)/config:/etc/config:ro myimage

# Multiple volumes
MSYS_NO_PATHCONV=1 docker run \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/data:/app/data \
  -v my-named-volume:/var/lib/data \
  myimage
```

### For docker-compose.yml Files

Docker Compose files use forward slashes and relative paths - **these work correctly** in Git Bash:

```yaml
# WORKS WITHOUT MODIFICATION in Git Bash
services:
  app:
    image: myimage
    volumes:
      # Relative paths (RECOMMENDED)
      - ./src:/app/src
      - ./data:/app/data

      # Named volumes (RECOMMENDED)
      - my-data:/var/lib/data

      # Windows absolute paths with forward slashes (WORKS)
      - C:/Users/project:/app

      # Unix-style paths (WORKS if referring to WSL/MINGW paths)
      - /c/Users/project:/app

volumes:
  my-data:
```

**Important:** When running `docker compose` commands:

```bash
# No special handling needed for compose files
docker compose up -d

# But if you use command-line volume overrides:
MSYS_NO_PATHCONV=1 docker compose run -v $(pwd)/extra:/extra app
```

## Complete Examples

### Example 1: Simple Application Development

```bash
# Set up environment once per session
export MSYS_NO_PATHCONV=1

# Run with live code reload
docker run -d \
  --name dev-app \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/public:/app/public \
  -p 3000:3000 \
  node:20-alpine \
  npm run dev

# View logs
docker logs -f dev-app
```

### Example 2: Database with Data Persistence

```bash
# Use named volume for database data (no path issues)
docker run -d \
  --name postgres-db \
  -e POSTGRES_PASSWORD=mypassword \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16-alpine

# Mount init scripts with MSYS_NO_PATHCONV
MSYS_NO_PATHCONV=1 docker run -d \
  --name postgres-db \
  -e POSTGRES_PASSWORD=mypassword \
  -v pgdata:/var/lib/postgresql/data \
  -v $(pwd)/init.sql:/docker-entrypoint-initdb.d/init.sql:ro \
  -p 5432:5432 \
  postgres:16-alpine
```

### Example 3: Full Stack with Docker Compose

```bash
# Project structure:
# /c/Users/project/
#   ├── docker-compose.yml
#   ├── backend/
#   ├── frontend/
#   └── data/

# docker-compose.yml (no special path handling needed)
cat > docker-compose.yml <<'EOF'
services:
  backend:
    build: ./backend
    volumes:
      - ./backend/src:/app/src
      - ./data:/app/data
    ports:
      - "4000:4000"

  frontend:
    build: ./frontend
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/public:/app/public
    ports:
      - "3000:3000"
    depends_on:
      - backend

  database:
    image: postgres:16-alpine
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: changeme

volumes:
  db-data:
EOF

# Start everything (works normally)
docker compose up -d

# Override with additional volume (needs MSYS_NO_PATHCONV)
MSYS_NO_PATHCONV=1 docker compose run -v $(pwd)/scripts:/scripts backend bash
```

## Troubleshooting Path Issues

### Problem: "No such file or directory" errors

**Symptoms:**
```
Error response from daemon: invalid mount config for type "bind":
bind source path does not exist: C:\Program Files\Git\c\Users\project
```

**Diagnosis:**
- Path has been incorrectly converted by MINGW
- Notice `C:\Program Files\Git\` prefix added

**Solution:**
```bash
# Add MSYS_NO_PATHCONV before command
MSYS_NO_PATHCONV=1 docker run -v $(pwd):/app myimage
```

### Problem: Volume appears empty in container

**Symptoms:**
- Container starts successfully
- But mounted directory is empty
- Files exist on host

**Diagnosis:**
- Path conversion mangled the source path
- Docker created empty directory instead

**Solution:**
```bash
# Use MSYS_NO_PATHCONV with $(pwd)
MSYS_NO_PATHCONV=1 docker run -v $(pwd)/data:/data myimage

# Or use double slash
docker run -v //c/Users/project/data:/data myimage

# Or use named volumes for persistent data
docker run -v my-named-volume:/data myimage
```

### Problem: Path with spaces fails

**Symptoms:**
```
Error: invalid reference format
```

**Diagnosis:**
- Spaces in Windows paths not properly quoted
- Path conversion + spaces = disaster

**Solution:**
```bash
# Use MSYS_NO_PATHCONV and quote $(pwd)
MSYS_NO_PATHCONV=1 docker run -v "$(pwd)":/app myimage

# Or avoid spaces in project paths entirely (RECOMMENDED)
# Move project from:
#   C:/Users/My Name/My Projects/app
# To:
#   C:/Users/MyName/projects/app
```

### Problem: $PWD not working correctly

**Symptoms:**
- Using `$PWD` variable instead of `$(pwd)`
- Inconsistent behavior

**Solution:**
```bash
# WRONG: Using $PWD
docker run -v $PWD:/app myimage

# CORRECT: Using $(pwd)
MSYS_NO_PATHCONV=1 docker run -v $(pwd):/app myimage

# Explanation:
# $(pwd) is a command that returns current directory
# $PWD is an environment variable that may not be properly formatted
```

## Testing Your Configuration

Create a test script to verify Docker volume mounts work correctly:

```bash
#!/bin/bash
# test-docker-volume.sh

echo "Testing Docker volume mounts in Git Bash..."

# Create test file
mkdir -p test-mount
echo "Hello from host" > test-mount/test.txt

# Test 1: With MSYS_NO_PATHCONV
echo "Test 1: With MSYS_NO_PATHCONV"
MSYS_NO_PATHCONV=1 docker run --rm -v $(pwd)/test-mount:/data alpine cat /data/test.txt

# Test 2: With double slash
echo "Test 2: With double slash"
docker run --rm -v //$(pwd)/test-mount:/data alpine cat /data/test.txt

# Test 3: Without workaround (should fail)
echo "Test 3: Without workaround (may fail)"
docker run --rm -v $(pwd)/test-mount:/data alpine cat /data/test.txt

# Cleanup
rm -rf test-mount

echo "Testing complete!"
```

Run it:
```bash
chmod +x test-docker-volume.sh
./test-docker-volume.sh
```

## Recommended Configuration

Add to your `~/.bashrc`:

```bash
# Docker path conversion fix for Git Bash on Windows
export MSYS_NO_PATHCONV=1

# Or use a wrapper function if you prefer per-command control
docker() {
  (export MSYS_NO_PATHCONV=1; command docker.exe "$@")
}
export -f docker

# Alias for docker compose (if needed)
alias docker-compose='MSYS_NO_PATHCONV=1 docker compose'
```

## Platform Detection Script

Use this to automatically detect and configure Docker for Git Bash:

```bash
# Add to ~/.bashrc
# Detect if running in Git Bash/MINGW on Windows
if [ -n "$MSYSTEM" ] || [[ "$(uname -s)" == MINGW* ]]; then
  # Running in Git Bash/MINGW
  echo "Git Bash detected - enabling Docker path conversion fix"
  export MSYS_NO_PATHCONV=1

  # Optional: Create wrapper function for explicit control
  docker() {
    (export MSYS_NO_PATHCONV=1; command docker.exe "$@")
  }
  export -f docker
fi
```

## Quick Reference

### Environment Variables

| Variable | Purpose | Values |
|----------|---------|--------|
| `MSYS_NO_PATHCONV` | Disable all path conversion (Git Bash) | `1` to disable |
| `MSYS2_ARG_CONV_EXCL` | Exclude specific arguments (MSYS2) | `'*'` or patterns |
| `MSYS2_ENV_CONV_EXCL` | Exclude environment variables (MSYS2) | `'*'` or patterns |
| `MSYSTEM` | MSYS subsystem indicator | `MINGW64`, `MINGW32`, `MSYS` |

### Command Patterns

```bash
# RECOMMENDED: Export once per session
export MSYS_NO_PATHCONV=1
docker run -v $(pwd):/app myimage

# Per-command prefix
MSYS_NO_PATHCONV=1 docker run -v $(pwd):/app myimage

# Double slash workaround
docker run -v //c/Users/project:/app myimage

# Named volumes (no path issues)
docker run -v my-data:/data myimage

# Docker Compose (relative paths work)
docker compose up -d
```

### What Works Without Modification

These Docker commands work normally in Git Bash without special handling:

- Named volumes: `-v my-volume:/data`
- Network commands: `docker network create`
- Image commands: `docker build`, `docker pull`
- Container commands without volumes: `docker run myimage`
- Docker Compose with relative paths in YAML

### What Needs MSYS_NO_PATHCONV

These commands require path conversion fixes:

- Bind mounts with absolute paths: `-v /c/Users/project:/app`
- Bind mounts with $(pwd): `-v $(pwd):/app`
- Volume mounts on docker run command line
- Any command with Unix-style absolute paths

## Summary

**Best Practice for Git Bash on Windows:**

1. **Add to ~/.bashrc:** `export MSYS_NO_PATHCONV=1`
2. **Use relative paths in docker-compose.yml:** `./src:/app/src`
3. **Use named volumes for data:** `my-data:/var/lib/data`
4. **Use $(pwd) with MSYS_NO_PATHCONV** for bind mounts: `MSYS_NO_PATHCONV=1 docker run -v $(pwd):/app`

This configuration ensures Docker commands work correctly in Git Bash on Windows without path conversion issues.
