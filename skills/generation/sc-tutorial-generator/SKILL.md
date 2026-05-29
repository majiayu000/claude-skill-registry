```skill
---
name: sc-tutorial-generator
description: "Generate VHS tape files for terminal tutorials from project context. Infers CLI entrypoints, creates consistent tutorials following developer-terminal conventions."
category: utility
invokes: [agent-ops-interview, agent-ops-planning]
invoked_by: []
state_files:
  read: [constitution.md, focus.md]
  write: [focus.md]
---

# ScriptCast Tutorial Generator Skill

## Purpose

Enable AI agents to autonomously generate VHS tape files that:
1. Record terminal command sequences as professional videos
2. Infer project context (CLI entrypoints, shell, tools)
3. Use shared profiles for consistent styling
4. Follow developer-terminal best practices
5. Never hard-code secrets or private URLs

## When to Use

- User requests a tutorial/demo video for a CLI tool
- User wants to showcase terminal commands
- User asks to "create a VHS tape" or "record a demo"
- User wants to document a workflow with terminal recordings

## Prerequisites

Before generating a tutorial, ensure:
- VHS is installed (`vhs --version`)
- ScriptCast CLI is available (`scriptcast --version`)
- Project has identifiable CLI entrypoints

## Procedure: Generate Tutorial

### Phase 1: Context Discovery

1. **Identify Project Type**
   ```
   Look for:
   - pyproject.toml → Python project
   - package.json → Node.js project
   - Cargo.toml → Rust project
   - go.mod → Go project
   ```

2. **Extract CLI Entrypoints**
   ```python
   # Python: Check [project.scripts] in pyproject.toml
   # Node.js: Check "bin" in package.json
   # Go: Check main.go location
   ```

3. **Detect Shell Preference**
   ```
   Default: /bin/bash
   Override if:
   - .zshrc present → /bin/zsh
   - constitution.md specifies shell
   ```

4. **Gather Project Metadata**
   ```
   - Project name (from package config)
   - Version (from package config)
   - Description (from README or config)
   ```

### Phase 2: Profile Resolution

Check for existing profile or create one:

1. **Look for shared profile**:
   ```
   .vhs/profile-default.tape
   .vhs/profiles/default.tape
   scriptcast profiles list
   ```

2. **If no profile exists**:
   ```bash
   scriptcast profiles init default
   ```

3. **Use profile in tape**:
   ```tape
   Source "profile-default.tape"
   ```

### Phase 3: Tutorial Structure

Every tutorial should follow this structure:

```tape
# Tutorial: {title}
# Project: {project_name}
# Generated: {date}

Output "{slug}.mp4"

# Require tools used in demo
Require {shell}
Require {cli_tool}

# Source shared profile
Source "profile-default.tape"

# === INTRO ===
# Brief pause for title card (optional)
Sleep 2s

# === DEMO STEPS ===
# Step 1: {step_title}
Type@0.05s "{command}"
Enter
Sleep 2s  # Wait for output

# Step 2: {step_title}
Type@0.05s "{command}"
Enter
Sleep 2s

# ... more steps ...

# === OUTRO ===
Sleep 3s  # Final pause
```

### Phase 4: Command Selection

When choosing commands to demonstrate:

1. **Prioritize**:
   - Help/version commands (show CLI exists)
   - Core functionality (main use case)
   - Common workflows (typical user path)

2. **Avoid**:
   - Commands that require auth/secrets
   - Commands that modify system state destructively
   - Commands with long output (truncate or redirect)
   - Commands that prompt for input (unless handled)

3. **Use safe placeholders**:
   ```tape
   # ❌ BAD: Real credentials
   Type "api-key-abc123xyz"
   
   # ✅ GOOD: Placeholder
   Type "your-api-key-here"
   ```

### Phase 5: Timing Calibration

Set appropriate wait times:

| Command Type | Recommended Sleep |
|--------------|-------------------|
| Quick command (ls, pwd) | 1s |
| Medium command (build) | 2-3s |
| Long command (install) | 5s+ or use WaitPattern |
| After typing | 0.5s before Enter |
| Output review | 2-3s |
| Section transition | 1-2s |

For commands with unpredictable duration:
```tape
Set WaitPattern "\\$ $"  # Wait for prompt
Set WaitTimeout 30s      # Max wait time
```

### Phase 6: Narration Timing (Optional)

If tutorial will have voiceover, add duration comments:

```tape
# [Narration: "First, let's check the version"]
Type@0.05s "myctl --version"
Enter
Sleep 3s  # Narration duration: ~2s + buffer
```

## Output Structure

Generated files:

```
.vhs/
├── profile-default.tape     # Shared profile (if created)
└── {slug}.tape              # Generated tutorial tape

tutorials/
└── {slug}.md                # Optional manuscript (if requested)
```

## Interview Questions (if context unclear)

| # | Question | Purpose |
|---|----------|---------|
| 1 | "What CLI tool/command should the tutorial demonstrate?" | Target command |
| 2 | "What's the main use case or workflow to show?" | Demo scope |
| 3 | "Any specific commands you want included?" | Content |
| 4 | "Will this have narration/voiceover?" | Timing mode |
| 5 | "Output filename/slug?" | File naming |

## Generated Tape Validation

After generating, validate:

1. **Syntax check**: `vhs validate {tape}.tape` (if available)
2. **Preview**: `vhs {tape}.tape` to record
3. **Review**: Watch generated video for timing issues

## Anti-patterns (avoid)

- ❌ Hard-coding API keys, tokens, or passwords
- ❌ Using `rm -rf` or other destructive commands without confirmation
- ❌ Commands that access private URLs or internal systems
- ❌ Assuming specific user environment (use generic paths)
- ❌ Overly long recordings (>3 min without purpose)
- ❌ Missing `Require` directives for used tools
- ❌ Skipping profile for consistent styling

## Example: Generate Tutorial for Python CLI

**Context**: User has a Python project with CLI entrypoint `myctl`

**Discovery**:
```yaml
project_name: my-cli-tool
cli_entrypoint: myctl
shell: /bin/bash
version: 1.2.0
```

**Generated tape**:
```tape
# Tutorial: my-cli-tool Demo
# Generated by ScriptCast Tutorial Generator

Output "myctl-demo.mp4"

Require bash
Require myctl

Source "profile-default.tape"

# === INTRO ===
Sleep 1s

# === Step 1: Show version ===
Type@0.05s "myctl --version"
Enter
Sleep 2s

# === Step 2: Show help ===
Type@0.05s "myctl --help"
Enter
Sleep 3s

# === Step 3: Run main command ===
Type@0.05s "myctl process input.txt"
Enter
Sleep 3s

# === OUTRO ===
Sleep 2s
```

## ScriptCast Integration

For full video production (not just VHS tape):

```bash
# Parse tutorial manuscript
scriptcast parse tutorial.md

# Generate VHS tape from manuscript
scriptcast vhs tutorial.md --profile default

# Render complete video with TTS
scriptcast render tutorial.md --output output/
```

## Completion Criteria

Tutorial generation is complete when:

- [ ] VHS tape file created in `.vhs/` directory
- [ ] Tape uses shared profile for styling
- [ ] All required tools declared with `Require`
- [ ] No secrets or private URLs in commands
- [ ] Timing appropriate for command types
- [ ] Tape can be executed without errors
- [ ] User has previewed or approved structure

```
