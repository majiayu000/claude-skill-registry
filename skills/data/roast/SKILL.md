---
name: roast
description: Multi-perspective UI/UX roasting workflow with iterative improvement cycles
---

# 🔥 UI/UX Roast Skill

Brutally honest UI/UX critique with multi-perspective analysis and iterative improvement.

## Command Syntax

```bash
/roast [mode] [target] [options]

# Modes
screen <target>     # Single screen analysis (default)
flow <target>       # Multi-screen user journey
audit               # Full application review

# Options
--iterations=<1-10> # Roast cycles (default: 3)
--focus=<area>      # Priority: a11y|conversion|usability|visual|implementation
--output=<path>     # Output directory (default: reports/roast/)
--fix=<mode>        # Fix handling: auto|report|ask (default: ask)
```

## Examples

```bash
/roast screen login                     # Roast login screen
/roast screen settings --focus=a11y     # Focus on accessibility
/roast flow checkout --iterations=5     # 5-iteration checkout flow
/roast flow onboarding --fix=auto       # Auto-fix issues found
/roast audit                            # Full app audit
```

## Execution Workflow

### 1. Immediate Start

**Do NOT ask questions upfront.** Apply smart defaults and begin immediately.

```
🔥 ROAST SESSION STARTED
├─ Mode: screen
├─ Target: login
├─ Iterations: 3
├─ Focus: balanced
└─ Output: reports/roast/
```

### 2. Screenshot Capture

Auto-detect screenshot method:

```
📸 Capturing screenshot...
├─ Xcode MCP: [✓ found | ✗ not found]
├─ Playwright MCP: [✓ found | ✗ not found]
└─ Using: [xcode | playwright | manual upload]
```

**Detection priority:**
1. `mcp__xcodebuildmcp__screenshot` → iOS/macOS
2. `mcp__playwright__browser_take_screenshot` → Web
3. Request user upload → Fallback

**CRITICAL: Always specify the output path explicitly!**

```typescript
// First, ensure directory exists
Bash: mkdir -p reports/roast/screenshots

// Playwright MCP - specify filename parameter
mcp__playwright__browser_take_screenshot({
  type: "png",
  filename: "reports/roast/screenshots/[target]_[iteration].png"
})

// Xcode MCP - specify path parameter
mcp__xcodebuildmcp__screenshot({
  path: "reports/roast/screenshots/[target]_[iteration].png"
})
```

Without explicit path, screenshots go to wrong location (e.g., `.playwright-mcp/`).

### 3. Parallel Analysis with Progress

Show real-time progress:

```
🔥 Roasting: login (1/3)
├─ 📸 Screenshot ✓
├─ 🎨 Designer: analyzing...
├─ 💻 Developer: analyzing...
├─ 👤 User: analyzing...
├─ ♿ A11y: analyzing...
└─ 📈 Marketing: analyzing...
```

Launch agents in parallel:

```typescript
// All 5 agents run simultaneously
Task(subagent_type="claude-roaster:roaster-designer", prompt="...")
Task(subagent_type="claude-roaster:roaster-developer", prompt="...")
Task(subagent_type="claude-roaster:roaster-user", prompt="...")
Task(subagent_type="claude-roaster:roaster-a11y", prompt="...")
Task(subagent_type="claude-roaster:roaster-marketing", prompt="...")
```

Update as each completes:

```
├─ 🎨 Designer: ✓ 3 issues
├─ 💻 Developer: ✓ 2 issues
├─ 👤 User: ✓ 4 issues
├─ ♿ A11y: ✓ 5 issues (2 critical!)
└─ 📈 Marketing: ✓ 2 issues
```

### 4. Results Summary

Display in terminal before asking about fixes:

```
🔥 ROAST RESULTS (Iteration 1/3)

Found 16 issues:
├─ 🔴 Critical: 2
├─ 🟠 Major: 6
└─ 🟡 Minor: 8

Top Critical Issues:
1. Missing form labels - add aria-label to inputs
2. Contrast ratio 2.1:1 - increase to 4.5:1 minimum

📄 Full report: reports/roast/roast_login_1.md
```

### 5. Fix Decision (After Results)

Ask ONLY after showing results:

```
How should we handle these 16 issues?

[1] Auto-fix critical & major (8 fixes)
[2] Fix all issues (16 fixes)
[3] Cherry-pick fixes
[4] Report only (no changes)
```

### 6. Fix Implementation

If fixes chosen:

```
🔧 Implementing fixes...
├─ [1/8] Adding aria-labels... ✓
├─ [2/8] Fixing contrast... ✓
├─ [3/8] Increasing touch targets... ✓
...
└─ ✓ Complete

📸 Capturing updated screenshot...
```

### 7. Next Iteration

```
Iteration 2/3 starting...
[Repeat steps 2-6]
```

### 8. Final Summary

```
🔥 FINAL ROAST SUMMARY

Session Complete!
├─ Iterations: 3
├─ Issues found: 24
├─ Issues fixed: 18
└─ Resolution: 75%

Score Improvement:
| Category      | Before | After | Δ    |
|---------------|--------|-------|------|
| Visual        | 4/10   | 8/10  | +4   |
| Usability     | 5/10   | 9/10  | +4   |
| Accessibility | 3/10   | 8/10  | +5   |
| Overall       | 4/10   | 8/10  | +4   |

📄 reports/roast/roast_login_final.md
```

---

## Mode-Specific Behavior

### Screen Mode

Single screen, multiple iterations:

```
/roast screen login --iterations=3

Iteration 1: Capture → Analyze → Report → Fix?
Iteration 2: Capture → Analyze → Report → Fix?
Iteration 3: Capture → Analyze → Final Report
```

### Flow Mode

Multiple screens, analyze journey:

```
/roast flow checkout

🗺️ Flow: checkout (5 steps)
├─ [1/5] Cart → 📸 analyzing...
├─ [2/5] Shipping → 📸 analyzing...
├─ [3/5] Payment → 📸 analyzing...
├─ [4/5] Review → 📸 analyzing...
└─ [5/5] Confirmation → 📸 analyzing...

Cross-screen checks:
├─ Visual consistency
├─ Navigation clarity
├─ Progress indication
└─ Drop-off risk points
```

### Audit Mode

Auto-detect and roast all critical screens:

```
/roast audit

🔍 Scanning for critical screens...
├─ Login ✓
├─ Dashboard ✓
├─ Settings ✓
├─ Checkout ✓
└─ Profile ✓

Roasting 5 screens (3 iterations each)...
```

---

## Agent Configuration

| Agent | Model | Focus | Weight |
|-------|-------|-------|--------|
| roaster (orchestrator) | Opus | Synthesis | - |
| roaster-designer | Sonnet | Visual, typography, color | 1.0x |
| roaster-developer | Sonnet | Implementation, structure | 1.0x |
| roaster-user | Sonnet | Usability, friction | 1.0x |
| roaster-a11y | Sonnet | Accessibility, WCAG | 1.0x |
| roaster-marketing | Sonnet | Conversion, trust | 1.0x |

**With `--focus` option:**
- Focused agent: 1.5x weight
- Other agents: 0.5x weight

---

## Output Structure

```
reports/roast/
├─ roast_[target]_1.md
├─ roast_[target]_2.md
├─ roast_[target]_final.md
└─ screenshots/
   ├─ [target]_1.png
   ├─ [target]_2.png
   └─ [target]_final.png
```

---

## Report Format

```markdown
# 🔥 Roast Report: [Target] - Iteration [N]

**Mode:** screen | **Focus:** balanced | **Date:** 2024-01-15

![Screenshot](screenshots/login_1.png)

## The Verdict

[Brutal 2-3 sentence summary]

## Issues by Severity

### 🔴 Critical (2)
| Issue | Agent | Fix |
|-------|-------|-----|
| Missing labels | A11y | Add aria-label="Email" |
| Low contrast | Designer | Change #999 to #595959 |

### 🟠 Major (6)
...

### 🟡 Minor (8)
...

## Agent Deep Dives

### 🎨 Designer
[Full analysis]

### ♿ A11y Expert
[Full analysis]

...

## Quick Wins
- [ ] Fix 1 (< 2 min)
- [ ] Fix 2 (< 2 min)

## Scores
| Category | Score |
|----------|-------|
| Visual | 4/10 |
| Usability | 5/10 |
| Accessibility | 3/10 |
| Overall | 4/10 |
```

---

## Voice Guidelines

1. **Brutal but fair** - Harsh critique, always with solutions
2. **Specific values** - "#2563eb", "48px", "font-weight: 600"
3. **Actionable fixes** - Every issue has a concrete fix
4. **Fast start** - Begin immediately, ask questions later
5. **Progress visibility** - Always show what's happening
