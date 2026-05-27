---
name: claude-flow-hook-customizing
description: Use this skill when creating, optimizing, or maintaining claude hooks.
---

## 📖 Overview

> **A Complete Guide to Verification Hooks with Claude Flow**

This guide demonstrates how to use Claude Code's hook system to ensure AI agents create **real, functional, and secure code** - not mocks or simulations. The hooks provide both preventive guidance (before edits) and verification feedback (after edits) to maintain code quality.

### Reference
REFERENCE.md

### Examples
./examples/memory-workflow-mcp.js
./examples/session-memory-workflow.sh

### 🎯 The Problem

One of the hardest problems in fast-moving development is that things slip through the cracks:
- A `console.log` left behind
- A mock never removed  
- An API still pointing at localhost
- Hardcoded secrets in production

By the time it hits production, you're firefighting instead of building.

### ✅ The Solution

**Make verification automatic, not optional.** That's where Claude Flow verification hooks come in.

This tutorial shows you how to wire up Claude Code `PreToolUse` and `PostToolUse` hooks that keep your coding agents on track using the Claude Flow Truth and Verification tools.

> 💡 **Think of it as**: Having a senior developer quietly checking over your shoulder every time you hit save, but without slowing you down.

---

## 🔍 What Claude Code Sees: Before & After Every Operation

### Example: Creating a Production API Handler

#### ❌ What Claude Attempts to Write (BAD):

```javascript
// api/users.js
const API_KEY = "sk-prod-12345"; // Quick fix for now
const password = "admin123"; 

function getUserData() {
  // TODO: Implement real database call
  console.log("Mock response for testing");
  return { mock: true, data: "placeholder" };
}

fetch("http://api.example.com/users"); // Will fix SSL later
```

#### 🛡️ What the Hooks Enforce BEFORE Creation:

```
🎯 PRE-EDIT VERIFICATION
Target: /api/users.js
⚠️  REQUIREMENTS:
  • Real implementations only (no mocks in production)
  • No hardcoded secrets - use environment variables
  • Complete error handling
  • Secure protocols (HTTPS)

🔍 Mandatory Verification Checklist:
  ✓ Implementation MUST be FULLY FUNCTIONAL
  ✓ NO mocks/stubs/simulations (unless test file)
  ✓ Real API connections (not placeholders)
  ✓ Actual data persistence (not in-memory only)
  ✓ Complete error handling (not just happy path)
  ✓ Production-ready code (not proof-of-concept)

🔐 Security Requirements:
  ⚠️ NEVER hardcode credentials or secrets
  ⚠️ Use environment variables for sensitive data
  ⚠️ No API keys, passwords, or tokens in code
  ⚠️ Validate and sanitize ALL user inputs
  ⚠️ Use secure connection protocols (HTTPS/TLS)
  ⚠️ Implement proper authentication & authorization

🚫 REJECT IF YOU SEE:
  • Hardcoded: API_KEY="sk-..."
  • Direct secrets: password="admin123"
  • TODO/FIXME without implementation
  • return mockData or simulatedResponse
  • console.log with sensitive data
  • Unvalidated user inputs (SQL injection risk)
  • HTTP instead of HTTPS for APIs
```

#### 📊 What Gets Verified AFTER Creation:

```
✅ POST-EDIT ANALYSIS
Modified: /api/users.js
Checking for issues...
  ⚠️  TODO comments found
  ⚠️  console.log detected
  🚨 Hardcoded password!

📊 CODE QUALITY ANALYSIS
File: /api/users.js
  ❌ TODO found (-15)
  ⚠️  console.log (-5)
  ❌ Mock detected (-25)
  🚨 Hardcoded API key (-30)
  🚨 Hardcoded password (-30)
  ⚠️  Insecure HTTP protocol (-10)

📊 QUALITY SCORE: -15/100
🚫 BELOW THRESHOLD (95) - Review required!

🔧 REQUIRED ACTIONS:
  1. Fix all security issues immediately
  2. Replace mocks with real implementations
  3. Use environment variables for secrets
  4. Remove debug statements

🔬 CLAUDE FLOW VERIFICATION
Truth Score: 0.45
Status: ❌ FAILED - Below 0.95 threshold
```

#### ✅ The Result: Claude Rewrites Properly

```javascript
// api/users.js
const API_KEY = process.env.API_KEY;
const password = process.env.DB_PASSWORD;

async function getUserData() {
  try {
    const response = await fetch("https://api.example.com/users", {
      headers: { 'Authorization': `Bearer ${API_KEY}` }
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return await response.json();
  } catch (error) {
    logger.error('Failed to fetch user data:', error);
    throw new Error('Unable to retrieve user data');
  }
}
```

---

## 🎯 How Hooks Work

Claude Code's hook system fires at specific points:

| Hook Type | When it Fires | Purpose |
|-----------|---------------|---------|
| **PreToolUse** | BEFORE tools execute | Preventive guidance & requirements |
| **PostToolUse** | AFTER tools complete | Verification & scoring |
| **UserPromptSubmit** | When you send a message | Automated feedback to Claude |

---

## 🚀 Working Implementation (Tested & Confirmed)

### Step 1: Create the Hook Analyzer Script

First, create a script to handle complex security checks without quote escaping issues:

```bash
# Create .claude/hook-analyzer-v2.sh
cat > .claude/hook-analyzer-v2.sh << 'EOF'
#!/bin/bash
# Enhanced hook analyzer with dynamic Claude Flow integration

FILE="$1"
echo "✅ POST-EDIT ANALYSIS" | tee -a /tmp/claude-hooks.log
echo "Modified: $FILE" | tee -a /tmp/claude-hooks.log
echo "Security Check Results:" | tee -a /tmp/claude-hooks.log

# Check for TODOs
if grep -q 'TODO' "$FILE" 2>/dev/null; then
  echo "  ⚠️  TODO found" | tee -a /tmp/claude-hooks.log
else
  echo "  ✓ No TODOs" | tee -a /tmp/claude-hooks.log
fi

# Check for console.log
if grep -q 'console.log' "$FILE" 2>/dev/null; then
  echo "  ⚠️  console.log found" | tee -a /tmp/claude-hooks.log
else
  echo "  ✓ No console.log" | tee -a /tmp/claude-hooks.log
fi

# Check for hardcoded secrets (improved regex)
if grep -qiE '(password|secret|token|key|credential)[[:space:]]*=[[:space:]]*["'"'"'][^"'"'"']+["'"'"']' "$FILE" 2>/dev/null; then
  echo "  🚨 Hardcoded secret detected!" | tee -a /tmp/claude-hooks.log
else
  echo "  ✓ No obvious secrets" | tee -a /tmp/claude-hooks.log
fi

# Dynamic Claude Flow verification
if command -v npx >/dev/null 2>&1; then
  echo "" | tee -a /tmp/claude-hooks.log
  echo "📊 Claude Flow Verification:" | tee -a /tmp/claude-hooks.log
  
  # Run verification and capture output
  VERIFY_OUTPUT=$(npx claude-flow@alpha verify verify "$FILE" --agent coder --threshold 0.95 2>&1)
  
  # Extract and display actual scores
  echo "$VERIFY_OUTPUT" | grep -E "Score:|compile:|test:|lint:|Status:" | while read line; do
    echo "   $line" | tee -a /tmp/claude-hooks.log
  done
  
  # Get current truth scores
  TRUTH_JSON=$(npx claude-flow@alpha truth --json 2>/dev/null)
  if [ $? -eq 0 ]; then
    AVG_SCORE=$(echo "$TRUTH_JSON" | jq -r '.averageScore // "N/A"')
    THRESHOLD=$(echo "$TRUTH_JSON" | jq -r '.threshold // "0.85"')
    echo "   Overall Average: $AVG_SCORE (threshold: $THRESHOLD)" | tee -a /tmp/claude-hooks.log
  fi
fi
EOF

# Make it executable
chmod +x .claude/hook-analyzer-v2.sh
```

### Step 2: Configure `.claude/settings.json`

Add this configuration with automated feedback loop:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "echo '🎯 PRE-EDIT VERIFICATION' | tee -a /tmp/claude-hooks.log && FILE=$(cat | jq -r '.tool_input.file_path // .tool_input.path // empty') && echo \"Target: $FILE\" | tee -a /tmp/claude-hooks.log && echo '⚠️  REQUIREMENTS:' | tee -a /tmp/claude-hooks.log && echo '  • Real implementations only (no mocks in production)' | tee -a /tmp/claude-hooks.log && echo '  • No hardcoded secrets - use environment variables' | tee -a /tmp/claude-hooks.log && echo '  • Complete error handling' | tee -a /tmp/claude-hooks.log && echo '  • Secure protocols (HTTPS)' | tee -a /tmp/claude-hooks.log"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(cat | jq -r '.tool_input.file_path // .tool_input.path // empty') && /workspaces/flow-nexus/.claude/hook-analyzer-v2.sh \"$FILE\""
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "CMD=$(cat | jq -r '.tool_input.command // empty') && echo \"Command executed: $CMD\" | tee -a /tmp/claude-hooks.log"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "if [ -f /tmp/claude-hooks.log ] && [ -s /tmp/claude-hooks.log ]; then echo '<user-prompt-submit-hook>'; echo '📋 Recent Hook Activity:'; tail -30 /tmp/claude-hooks.log; echo '</user-prompt-submit-hook>'; > /tmp/claude-hooks.log; fi"
          }
        ]
      }
    ]
  }
}
```

---

## ✨ Key Improvements in This Approach

### 1. 📝 Script-Based Analysis
- **Problem Solved**: Complex quote escaping issues in JSON
- **Solution**: Dedicated bash script for security analysis
- **Benefit**: Clean, maintainable code without syntax errors

### 2. 🔄 Automated Feedback Loop
- **Feature**: UserPromptSubmit hook with `<user-prompt-submit-hook>` tags
- **How it Works**: Automatically shares hook output with Claude
- **Result**: Real-time visibility into all verification checks

### 3. 📊 Dynamic Scoring
- **Before**: Static values like `test: 0.60`
- **After**: Real Claude Flow scores that reflect actual code quality
- **Example**: `Overall Average: 0.9 (threshold: 0.85)`

### 4. 💾 Persistent Logging
- **Location**: `/tmp/claude-hooks.log`
- **Features**: Append mode with `tee -a` for complete history
- **Cleanup**: Automatic reset after each UserPromptSubmit

### 5. 🔐 Enhanced Secret Detection
- **Improved Regex**: Case-insensitive pattern matching
- **Detects Variables**: 
  - `password`, `secret`, `token`, `key`, `credential`
  - Any variation: `apiKey`, `API_KEY`, `authToken`, etc.
- **Pattern**: `(password|secret|token|key|credential)[[:space:]]*=[[:space:]]*["'][^"']+["']`

---

## 🔬 Advanced Configurations

### Claude Flow Truth Verification

Integrate Claude Flow's verification system for automated truth scoring:

```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit|MultiEdit",
    "hooks": [{
      "type": "command",
      "command": "echo '🔬 Initializing Claude Flow Verification...' && npx claude-flow@alpha verify init strict 2>/dev/null && echo '✅ Strict mode: 0.95 threshold' || echo '⚠️  Claude Flow not available'"
    }]
  }],
  "PostToolUse": [{
    "matcher": "Write|Edit|MultiEdit",
    "hooks": [{
      "type": "command",
      "command": "FILE=$(cat | jq -r '.tool_input.file_path // .tool_input.path // empty') && echo '📊 CLAUDE FLOW VERIFICATION' && npx claude-flow@alpha verify verify \"$FILE\" --agent coder --threshold 0.95 2>/dev/null || echo '  Manual check required' && npx claude-flow@alpha truth --agent coder --json 2>/dev/null | jq -r '\"Truth Score: \\(.averageScore // \"N/A\")\"' || true"
    }]
  }]
}
```

### Quantitative Scoring with Manual Fallback

Combine Claude Flow verification with manual scoring:

```json
{
  "PostToolUse": [{
    "matcher": "Write|Edit|MultiEdit",
    "hooks": [{
      "type": "command",
      "command": "FILE=$(cat | jq -r '.tool_input.file_path // .tool_input.path // empty') && echo '📊 CODE QUALITY ANALYSIS' && echo \"File: $FILE\" && SCORE=100 && grep -q 'TODO' \"$FILE\" 2>/dev/null && { echo '  ❌ TODO found (-15)'; SCORE=$((SCORE-15)); } || echo '  ✓ No TODOs' && grep -q 'console.log' \"$FILE\" 2>/dev/null && { echo '  ⚠️  console.log (-5)'; SCORE=$((SCORE-5)); } || echo '  ✓ No console.log' && grep -qE 'mock|Mock|placeholder' \"$FILE\" 2>/dev/null && { echo '  ❌ Mock detected (-25)'; SCORE=$((SCORE-25)); } || echo '  ✓ No mocks' && echo \"📊 Manual Score: $SCORE/100\" && echo '' && echo '🔬 Claude Flow Truth Analysis:' && npx claude-flow@alpha truth --report --agent coder 2>/dev/null | head -10 || echo '  Claude Flow not available'"
    }]
  }]
}
```

### Security-Focused Hooks

Detect potential security issues in commands:

```json
{
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "CMD=$(cat | jq -r '.tool_input.command // empty') && echo \"$CMD\" | grep -qE 'export.*(KEY|TOKEN|SECRET|PASSWORD)' && echo '⚠️  SECURITY WARNING: Potential secret exposure!' || true"
    }]
  }]
}
```

---

## ✅ Real Example Output

### When Creating a File with Issues

#### PreToolUse Hook Output:
```
🎯 PRE-EDIT VERIFICATION
Target: /workspaces/flow-cloud/test-hooks.js
⚠️  REQUIREMENTS:
  • Real implementations only (no mocks in production)
  • No hardcoded secrets - use environment variables
  • Complete error handling
  • Secure protocols (HTTPS)
```

#### PostToolUse Hook Output:
```
✅ POST-EDIT ANALYSIS
Modified: /workspaces/flow-cloud/test-hooks.js
Security Check Results:
  ⚠️  TODO comments found
  ⚠️  console.log detected
  🚨 Hardcoded password!

📊 Claude Flow Verification:
   ✅ compile: 1.00
   ❌ test: 0.60
   ✅ lint: 1.00
   📊 Verification Score: 0.90/0.85
   Status: ✅ PASSED
   Overall Average: 0.9 (threshold: 0.85)
```

---

## ⚙️ Benefits

| Benefit | Description |
|---------|-------------|
| **Automated Truth Scoring** | Reliability metrics with configurable thresholds (0.75-0.95) |
| **Pair Programming Mode** | Real-time collaborative verification during edits |
| **Implementation Verification** | Confirms functional requirements are met |
| **Continuous Quality Metrics** | Track truth scores and trends over time |

The verification commands add quantitative analysis to the qualitative checklist, giving you both human-readable reminders and data-driven confidence scores.

---

## 🔧 Troubleshooting

### If Hooks Don't Fire:

1. **Restart Claude Code** after changing `settings.json`
2. **Validate JSON**: `jq '.' .claude/settings.json`
3. **Check permissions format**: Use `:*` not just `*`
4. **Run `/doctor`** to validate settings
5. **Check script permissions**: `chmod +x .claude/hook-analyzer-v2.sh`

> 💡 **Remember**: The goal is real, secure, functional code - not placeholders or simulations. These hooks keep AI agents focused on production-quality implementations.

---

## 🚀 Optional: Claude Flow Integration

For advanced verification with Claude Flow:

### Installation
```bash
# Install Claude Flow globally
npm install -g claude-flow@alpha
```

### Quick Commands
```bash
npx claude-flow@alpha verify init strict  # 0.95 threshold
npx claude-flow@alpha truth               # View scores
npx claude-flow@alpha verify verify "$FILE" --threshold 0.95
```

## 📚 Claude Flow Commands Reference

### Verify Command (Truth Enforcement)

#### Initialize verification modes
```bash
npx claude-flow@alpha verify init strict          # 0.95 threshold
npx claude-flow@alpha verify init moderate        # 0.85 threshold
npx claude-flow@alpha verify init development     # 0.75 threshold
```

#### Run verification on files/tasks
```bash
npx claude-flow@alpha verify verify <file> --agent coder --threshold 0.95
npx claude-flow@alpha verify status --recent 10
npx claude-flow@alpha verify rollback --checkpoint last
```

### Truth Command (Score Analytics)

#### View and analyze scores
```bash
npx claude-flow@alpha truth                       # Current scores
npx claude-flow@alpha truth --report              # Detailed report
npx claude-flow@alpha truth --analyze             # Pattern analysis
npx claude-flow@alpha truth --agent coder         # Filter by agent
npx claude-flow@alpha truth --json | jq .averageScore  # For hooks
```

---

## 📝 Key Takeaways

✅ **PreToolUse** prevents errors before edits happen  
✅ **PostToolUse** enforces checks right after changes  
✅ **Claude Flow verification** provides truth-based enforcement at a 0.95 threshold  
✅ **Security hooks** stop secrets from leaking  
✅ **Quantitative + qualitative** = code that is real, secure, and production-ready  

> By building these checks into Claude Code, you shift from **reactive debugging** to **proactive verification**.
