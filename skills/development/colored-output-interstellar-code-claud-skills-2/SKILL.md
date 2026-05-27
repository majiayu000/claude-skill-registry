---
name: colored-output
description: Centralized colored output formatter for all skills, agents, and commands with ANSI escape codes
version: 1.1.0
author: Claude Code
tags: [output, formatting, colors, ansi, terminal, utility, ux]
---

# Colored Output Formatter Skill

**Centralized, reusable colored output formatting for ALL skills, agents, and commands!**

## 🎯 Purpose

This skill provides a **single source of truth** for colored terminal output. Instead of duplicating ANSI codes across every skill/agent, they all call this formatter.

**Benefits:**
- ✅ **DRY Principle** - Define colors once, use everywhere
- ✅ **Consistent UX** - All skills/agents look the same
- ✅ **Easy Updates** - Change colors in one place
- ✅ **Zero Duplication** - No repeated ANSI codes

## 🔧 **BASH COMMAND ATTRIBUTION PATTERN**

**CRITICAL: Before executing EACH bash command, MUST output:**
```
🔧 [colored-output] Running: <command>
```

**Examples:**
```
🔧 [colored-output] Running: bash .claude/skills/colored-output/color.sh skill-header "skill-name" "Starting..."
🔧 [colored-output] Running: bash .claude/skills/colored-output/color.sh success "" "Complete!"
🔧 [colored-output] Running: bash .claude/skills/colored-output/color.sh error "" "Failed!"
```

**Why:** This pattern helps users identify which skill is executing which command, improving transparency and debugging.

---

## 🎯 **USAGE GUIDELINES** (CRITICAL)

**⚠️ IMPORTANT: Use colored output SPARINGLY to prevent screen flickering and visual clutter!**

### ✅ DO Use Colored Output For:

1. **Initial Header** (once at start of operation)
   ```bash
   bash .claude/skills/colored-output/color.sh skill-header "skill-name" "Starting operation..."
   ```

2. **Final Results** (success, error, or completion)
   ```bash
   bash .claude/skills/colored-output/color.sh success "" "Operation complete!"
   ```

3. **Critical Alerts** (warnings, errors)
   ```bash
   bash .claude/skills/colored-output/color.sh warning "" "Configuration issue detected"
   bash .claude/skills/colored-output/color.sh error "" "Operation failed"
   ```

4. **Summary Sections** (key metrics, final status)
   ```bash
   bash .claude/skills/colored-output/color.sh info "" "Processed 10 files"
   ```

### ❌ DON'T Use Colored Output For:

1. **Progress Updates** - Use regular text instead
   - ❌ Bad: `bash .claude/skills/colored-output/color.sh progress "" "Step 1 of 5..."`
   - ✅ Good: Regular Claude text: "Step 1 of 5: Analyzing files..."

2. **Intermediate Info Messages** - Use regular text
   - ❌ Bad: `bash .claude/skills/colored-output/color.sh info "" "Found 3 files"`
   - ✅ Good: Regular Claude text: "Found 3 files to process..."

3. **Verbose Logging** - Use regular text
   - ❌ Bad: Multiple colored calls for each step
   - ✅ Good: Regular text for all intermediate steps

### 📏 Recommended Pattern

**Minimal Colored Output (2-3 calls per operation):**

```
# START: Colored header (1 call)
🔧 [skill-name] Starting operation...

# MIDDLE: Regular Claude text (0 colored calls)
Analyzing 10 files...
Processing configurations...
Updating database...
Generating reports...

# END: Colored result (1-2 calls)
✅ Operation complete!
📋 Summary: 10 files processed, 0 errors
```

### 🚫 Anti-Pattern (Causes Flickering)

**Excessive Colored Output (10+ calls per operation):**

```
🔧 [skill-name] Starting operation...          ← Colored
▶ Step 1: Analyzing files...                   ← Colored (unnecessary)
ℹ️ Found 10 files                              ← Colored (unnecessary)
▶ Step 2: Processing...                        ← Colored (unnecessary)
ℹ️ Processing file 1...                        ← Colored (unnecessary)
ℹ️ Processing file 2...                        ← Colored (unnecessary)
... (8 more colored calls) ...
✅ Operation complete!                          ← Colored
```

**Problem:** Each bash call creates a new task in Claude CLI, causing screen flickering and visual noise.

### 📊 Target Metrics

- **Maximum:** 3-4 colored bash calls per operation
- **Minimum:** 2 colored bash calls (header + result)
- **Ideal:** Use colored output only for boundaries (start/end) and alerts

---

## 🎨 **VISUAL OUTPUT FORMATTING**

**CRITICAL: This skill itself follows the minimal colored output pattern!**

### Self-Reference Pattern

When this skill responds, use the MINIMAL pattern:

```bash
# START: Header only
bash .claude/skills/colored-output/color.sh skill-header "colored-output" "Processing request..."

# MIDDLE: Regular text (no colored calls)
Analyzing color requirements...
Available message types: skill-header, agent-header, success, error, warning, info, progress...

# END: Result only
bash .claude/skills/colored-output/color.sh success "" "Formatting complete!"
```

**DO NOT use excessive colored calls when demonstrating. Follow the 2-3 call guideline!**

---

## 🎨 Color Scheme

### Component Types
- **Skills**: 🔧 Bold Blue `\033[1;34m`
- **Agents**: 🤖 Bold Purple `\033[1;35m`
- **Commands**: ⚡ Bold Green `\033[1;32m`

### Status Types
- **Success**: ✅ Bold Green `\033[1;32m`
- **Error**: ❌ Bold Red `\033[1;31m`
- **Warning**: ⚠️ Bold Yellow `\033[1;33m`
- **Info**: ℹ️ Bold Cyan `\033[1;36m`
- **Progress**: ▶ Blue `\033[0;34m`

---

## 📋 Usage

### Basic Syntax

```bash
bash .claude/skills/colored-output/color.sh [type] [component-name] [message]
```

### Examples

#### Skill Headers
```bash
bash .claude/skills/colored-output/color.sh skill-header "time-helper" "Processing time request..."
# Output: 🔧 [time-helper] Processing time request...  (in blue)
```

#### Agent Headers
```bash
bash .claude/skills/colored-output/color.sh agent-header "eslint-fixer" "Analyzing code..."
# Output: 🤖 [eslint-fixer] Analyzing code...  (in purple)
```

#### Command Headers
```bash
bash .claude/skills/colored-output/color.sh command-header "/commit" "Creating commit..."
# Output: ⚡ [/commit] Creating commit...  (in green)
```

#### Status Messages
```bash
bash .claude/skills/colored-output/color.sh success "" "File updated successfully"
# Output: ✅ File updated successfully  (in green)

bash .claude/skills/colored-output/color.sh error "" "Failed to parse file"
# Output: ❌ Failed to parse file  (in red)

bash .claude/skills/colored-output/color.sh warning "" "This may take a while"
# Output: ⚠️ This may take a while  (in yellow)

bash .claude/skills/colored-output/color.sh info "" "Processing 5 files"
# Output: ℹ️ Processing 5 files  (in cyan)

bash .claude/skills/colored-output/color.sh progress "" "Step 1 of 3"
# Output: ▶ Step 1 of 3  (in blue)
```

---

## 🔧 Integration Guide

### How Skills Should Use This

**OLD WAY (Don't do this):**
```markdown
Claude outputs: "Processing..."
(No colors, just plain text)
```

**NEW WAY (Do this):**
```markdown
When skill starts:
1. Output colored header using this formatter
2. Output progress messages using this formatter
3. Output final status using this formatter
```

### Example: time-helper Integration

```bash
# Start of skill
bash .claude/skills/colored-output/color.sh skill-header "time-helper" "Getting current time for Tokyo..."

# Progress
bash .claude/skills/colored-output/color.sh progress "" "Querying timezone database..."

# Result
bash .claude/skills/colored-output/color.sh info "" "Current time: 2025-10-22 14:30:00 JST"

# Success
bash .claude/skills/colored-output/color.sh success "" "Time retrieved successfully"
```

**Output:**
```
🔧 [time-helper] Getting current time for Tokyo...
▶ Querying timezone database...
ℹ️ Current time: 2025-10-22 14:30:00 JST
✅ Time retrieved successfully
```

---

## 🎯 Standard Workflow Pattern

**Every skill/agent should follow this pattern:**

### 1. Header (Start)
```bash
bash .claude/skills/colored-output/color.sh skill-header "SKILL-NAME" "Starting task..."
```

### 2. Progress (During)
```bash
bash .claude/skills/colored-output/color.sh progress "" "Processing step 1..."
bash .claude/skills/colored-output/color.sh progress "" "Processing step 2..."
```

### 3. Info (Results)
```bash
bash .claude/skills/colored-output/color.sh info "" "Found 10 items"
```

### 4. Status (End)
```bash
bash .claude/skills/colored-output/color.sh success "" "Task completed successfully"
# OR
bash .claude/skills/colored-output/color.sh error "" "Task failed: reason"
```

---

## 🧪 Testing

Test all color types:

```bash
cd .claude/skills/colored-output

# Test skill header
bash color.sh skill-header "test-skill" "This is a skill message"

# Test agent header
bash color.sh agent-header "test-agent" "This is an agent message"

# Test command header
bash color.sh command-header "/test" "This is a command message"

# Test statuses
bash color.sh success "" "Success message"
bash color.sh error "" "Error message"
bash color.sh warning "" "Warning message"
bash color.sh info "" "Info message"
bash color.sh progress "" "Progress message"
```

---

## 📚 Available Types

| Type | Usage | Example |
|------|-------|---------|
| `skill-header` | Skill starting | `🔧 [skill-name] Message` |
| `agent-header` | Agent starting | `🤖 [agent-name] Message` |
| `command-header` | Command starting | `⚡ [/command] Message` |
| `success` | Operation succeeded | `✅ Message` |
| `error` | Operation failed | `❌ Message` |
| `warning` | Caution needed | `⚠️ Message` |
| `info` | Informational | `ℹ️ Message` |
| `progress` | Step indicator | `▶ Message` |

---

## 🔄 How Other Skills Call This

### In skill.md Instructions

Add this section to every skill/agent:

```markdown
## 🎨 Colored Output (Required)

**CRITICAL: Use colored-output skill for ALL user-facing messages!**

### Start of Skill
\`\`\`bash
bash .claude/skills/colored-output/color.sh skill-header "SKILL-NAME" "Starting..."
\`\`\`

### Progress Updates
\`\`\`bash
bash .claude/skills/colored-output/color.sh progress "" "Processing..."
\`\`\`

### Final Status
\`\`\`bash
bash .claude/skills/colored-output/color.sh success "" "Complete!"
# OR
bash .claude/skills/colored-output/color.sh error "" "Failed!"
\`\`\`
```

---

## 🎨 Customization

To change colors globally, edit `color.sh`:

```bash
# Change skill color from blue to cyan
SKILL_COLOR='\033[1;36m'    # Was: \033[1;34m

# Change success icon
SUCCESS_ICON='🎉'           # Was: ✅
```

All skills/agents immediately inherit the changes!

---

## 📦 Files

```
.claude/skills/colored-output/
├── skill.md       # This documentation
└── color.sh       # Bash formatter script
```

---

## 🚀 Rollout Strategy

### Phase 1: Create Formatter (Done)
- ✅ Created color.sh script
- ✅ Created skill.md documentation

### Phase 2: Test with One Skill
- 🧪 Test with time-helper skill
- ✅ Verify colors render properly
- ✅ Confirm user experience improvement

### Phase 3: Apply to All Skills
- Update all .claude/skills/* to use formatter
- Update all framework skills to use formatter
- Update all framework agents to use formatter

### Phase 4: Maintain
- All new skills MUST use colored-output
- Updates to colors happen in ONE place

---

## 💡 Best Practices

**DO:**
- ✅ Use `skill-header` at the start of every skill
- ✅ Use `progress` for multi-step operations
- ✅ Use `success`/`error` for final status
- ✅ Use `info` for important details

**DON'T:**
- ❌ Duplicate ANSI codes in individual skills
- ❌ Mix colored and uncolored output
- ❌ Use too many colors (keep it clean)

---

## 🎉 Benefits Summary

**Before colored-output skill:**
- Every skill had duplicate ANSI codes
- Inconsistent colors across skills
- Hard to maintain/update
- Lots of repeated code

**After colored-output skill:**
- ✅ Single source of truth
- ✅ Consistent UX everywhere
- ✅ Easy to update colors globally
- ✅ Clean, DRY code

---

## Version History

### v1.0.0 (2025-10-22)
- Initial release
- Support for skills, agents, commands
- 8 message types (headers + statuses)
- Bash script implementation
- Cross-platform support
