---
name: Plugin Guide & Help
description: Use this skill when users ask specifically about the Storybook Assistant plugin - "what can the storybook assistant do", "storybook plugin features", "storybook assistant commands", "help with storybook assistant", "storybook plugin capabilities". ONLY triggers when user explicitly mentions "storybook assistant", "storybook plugin", or asks about Storybook-specific features. Does NOT trigger on generic help questions.
version: 1.0.1
---

# Plugin Guide & Help

## Overview

This skill helps users discover and understand all Storybook Assistant Plugin capabilities through natural language queries **that specifically mention the Storybook Assistant or Storybook plugin**.

## When to Use This Skill

**IMPORTANT:** This skill should ONLY trigger when the user explicitly mentions the plugin or Storybook-specific features.

**✅ DO Trigger on:**
- "What can the **Storybook Assistant** do?"
- "Show me **Storybook plugin** features"
- "Help with **Storybook Assistant**"
- "List **Storybook** commands"
- "**Storybook Assistant** capabilities"
- "What **Storybook** features are available?"
- "How do I use the **Storybook plugin**?"
- "Tell me about **Storybook Assistant**"

**❌ DO NOT Trigger on:**
- "help" (generic - goes to Claude Code help)
- "what can you do" (generic - not plugin-specific)
- "show features" (generic - could be anything)
- "list commands" (generic - could be any commands)
- General questions that don't mention Storybook or the plugin

## Response Strategy

### For Storybook-Specific Feature Questions

When user asks about the Storybook Assistant plugin specifically, provide a well-organized, scannable overview:

```markdown
# 🎨 Storybook Assistant - What I Can Do

I'm your complete AI-powered Storybook development assistant with 17 specialized features and 11 commands.

## 🚀 Most Popular Features

### Vision AI: Design-to-Code 🎨
Upload a screenshot and I'll generate pixel-perfect React components with:
- Exact spacing, colors, and typography
- Design tokens automatically extracted
- Multiple variants detected
- Full TypeScript support

**Try:** `/design-to-code` or "Generate a component from this design"

### Natural Language Components 💬
Describe a component in plain English and I'll build it:
- Complete TypeScript component
- Props with types
- Storybook stories
- Interaction tests

**Try:** `/generate-from-description` or "Create a user profile card with..."

### AI-Powered Accessibility ♿
Automatically find and fix WCAG 2.2 violations:
- Context-aware fix suggestions
- One-click application
- Ranked recommendations
- Real-time detection

**Try:** `/fix-accessibility Button.tsx` or "Check accessibility of my Card component"

### Visual Regression Testing 🔍
Intelligent screenshot comparison with 90% fewer false positives:
- AI understands intentional vs accidental changes
- Auto-approves theme updates
- Detects real layout bugs
- CI/CD integration

**Try:** `/setup-visual-testing`

### Design Token Sync 🔄
Keep Figma and code perfectly synchronized:
- Bidirectional sync (Figma ↔ Code)
- Automatic drift detection
- Conflict resolution
- Multi-format output

**Try:** `/sync-design-tokens --setup`

---

## 📋 All Available Commands

### Setup & Configuration
- `/setup-storybook` - Initialize Storybook 9
- `/setup-ci-cd` - Generate CI/CD pipeline
- `/setup-visual-testing` - Configure visual regression

### Component Development
- `/create-component` - Scaffold new component
- `/generate-stories` - Generate stories for existing components
- `/design-to-code` - Screenshot → Component
- `/generate-from-description` - Natural language → Component

### Quality & Maintenance
- `/fix-accessibility` - AI a11y remediation
- `/generate-dark-mode` - Auto-generate dark mode
- `/sync-design-tokens` - Figma sync
- `/analyze-usage` - Component analytics

---

## 💡 Common Workflows

**New Project:**
1. `/setup-storybook`
2. `/setup-ci-cd`
3. `/setup-visual-testing`

**Design-to-Code:**
1. `/design-to-code [screenshot]`
2. `/fix-accessibility ComponentName`
3. `/generate-dark-mode`

**Improve Existing:**
1. `/generate-stories ComponentName`
2. `/fix-accessibility ComponentName`
3. `/analyze-usage ComponentName`

---

## 🎯 Just Ask Me Naturally!

You don't need to memorize commands. Just ask:
- "Generate a button component from this description..."
- "Fix accessibility issues in my Card component"
- "Set up visual regression testing"
- "Sync my design tokens from Figma"
- "Show me how to create a dark mode"

I understand natural language and will use the right tools automatically.

---

**Getting started?** Try `/setup-storybook` first
**Have a screenshot?** Try `/design-to-code`
**Want more details?** Just ask about any specific feature!
```

### For Specific Feature Questions

When user asks about a specific capability:

**User:** "Can you help with accessibility?"
**Response:**
```markdown
# ♿ Accessibility Features

Yes! I have comprehensive AI-powered accessibility features:

## What I Can Do

1. **Automatic Detection**
   - Scans components for WCAG 2.2 violations
   - Real-time analysis via hooks
   - Covers 90% of common issues

2. **AI-Powered Fixes**
   - Context-aware suggestions (knows button purpose)
   - Ranked recommendations (Best → Good → Acceptable)
   - One-click application
   - Color contrast calculation

3. **Education**
   - Explains WHY each fix is needed
   - Teaches WCAG best practices
   - Links to relevant WCAG guidelines

## How to Use

**Quick fix for a component:**
```bash
/fix-accessibility Button.tsx
```

**Natural language:**
"Check my Card component for accessibility issues"
"Fix accessibility violations in the LoginForm"

## What Gets Checked

- Missing accessible names (buttons, links, images)
- Color contrast (WCAG AA/AAA)
- Keyboard navigation
- ARIA usage (semantic HTML first)
- Form labels
- Heading hierarchy

## Example Output

```
❌ Accessibility issue detected in Button.tsx:12

Issue: Button has no accessible name
WCAG: 4.1.2 Name, Role, Value (Level A)
Impact: Screen reader users won't know button purpose

Recommended fixes:
1. Add visible text + icon (BEST) ⭐
2. Use aria-label (GOOD)
3. Use title attribute (ACCEPTABLE)

Apply fix? [1] [2] [3]
```

**Related Features:**
- `testing-suite` - Accessibility tests in Storybook
- `component-scaffold` - New components with a11y built-in

Try `/fix-accessibility [file]` or just ask me to check accessibility!
```

### For "How Do I..." Questions

Extract the task and provide step-by-step guidance:

**User:** "How do I set up visual regression testing?"
**Response:**
```markdown
# Setting Up Visual Regression Testing

Here's how to set up AI-powered visual regression testing:

## Quick Start (Automated)

Just run:
```bash
/setup-visual-testing
```

I'll automatically:
1. Detect your framework and build tool
2. Install dependencies (Playwright, test-runner)
3. Create configuration files
4. Capture baseline screenshots
5. Set up NPM scripts
6. Configure CI/CD integration (optional)

## Step-by-Step Process

**1. Run Setup Command**
```bash
/setup-visual-testing
```

**2. Choose Your Preferences**
I'll ask about:
- Integration with Chromatic/Percy (optional)
- Auto-approval rules (conservative/balanced/aggressive)
- CI/CD integration (GitHub Actions, GitLab, etc.)

**3. Capture Baselines**
Initial screenshots will be captured automatically:
```
Capturing baseline screenshots...
  ✓ Button/Primary
  ✓ Card/Default
  ...
  ✓ Captured 47 stories
```

**4. Test Your Setup**
Make a small change and run:
```bash
npm run test:visual
```

**5. Review AI Analysis**
The AI will categorize changes:
- ✅ Expected (theme updates)
- ⚠️ Warning (review needed)
- ❌ Error (likely bugs)

## What Makes It "AI-Powered"?

Traditional visual regression:
- Flags thousands of anti-aliasing changes ❌
- Can't distinguish intentional from accidental ❌
- Requires manual review of everything ❌

AI-powered approach:
- Understands git history and design tokens ✅
- Auto-approves expected changes ✅
- Only flags real issues ✅
- 90% fewer false positives ✅

## Next Steps

After setup:
- Run `npm run test:visual` to test
- Use `npm run test:visual:interactive` for manual review
- Integrate with CI/CD to block regressions

Need more details? Type `/help visual-regression`
```

### For Version/Changelog Questions

**User:** "What's new?" or "What changed?"
**Response:**
```markdown
# 🆕 What's New in v2.1.0

## Major Additions (3 New Features)

### 1. AI Visual Regression Testing 🔍
- Intelligent screenshot comparison
- Context-aware diff analysis
- 90% reduction in false positives
- Auto-approval for theme updates
- CI/CD integration

**Try:** `/setup-visual-testing`

### 2. Design Token Sync 🔄
- Bidirectional Figma ↔ Code synchronization
- Automatic drift detection
- Conflict resolution
- Multi-format output (CSS, SCSS, TS, JSON)

**Try:** `/sync-design-tokens --setup`

### 3. Component Usage Analytics 📊
- Track component usage across codebase
- Deprecation impact analysis
- Unused component detection
- Migration effort estimation

**Try:** `/analyze-usage Button`

## Complete Feature Set

**Now includes ALL 10 SOTA 2026 features:**
- ✅ Vision AI Design-to-Code (P0)
- ✅ Natural Language Generation (P0)
- ✅ Accessibility Remediation (P1)
- ✅ Server Components (P1)
- ✅ **Visual Regression Testing (P1)** ⭐ NEW
- ✅ Performance Analysis (P2)
- ✅ Dark Mode Generation (P2)
- ✅ **Design Token Sync (P2)** ⭐ NEW
- ✅ CI/CD Generator (P3)
- ✅ **Component Usage Analytics (P3)** ⭐ NEW

## Version History

**v2.1.0** (Current)
- 100% SOTA roadmap complete
- 17 skills, 3 agents, 11 commands
- All P0, P1, P2, P3 features implemented

**v2.0.6** (Previous)
- 70% roadmap complete
- 14 skills, 2 agents, 8 commands

## What's Next?

All planned features are now complete! Future development will focus on:
- Performance optimizations
- Additional integrations
- Community-requested features

Try the new features with:
- `/setup-visual-testing`
- `/sync-design-tokens`
- `/analyze-usage [component]`
```

## Response Guidelines

### Keep It Scannable
- Use headers, bullets, and emoji
- Highlight key commands with code blocks
- Show examples, not just descriptions

### Be Conversational
- "I can help you..." not "This plugin can..."
- "Try `/command`" not "Use the command tool"
- Encourage questions: "Just ask me!"

### Provide Next Steps
- Always end with actionable next steps
- Suggest related features
- Point to detailed docs when appropriate

### Progressive Disclosure
- Start with high-level overview
- Provide details on request
- Link to full documentation

### Handle Edge Cases

**User:** "I'm completely lost"
**Response:** Start with `/setup-storybook` and offer to walk through step-by-step

**User:** "Too many features, overwhelming"
**Response:** Focus on the "Big 3" - design-to-code, accessibility, visual regression

**User:** "Which command should I use for X?"
**Response:** Suggest the most appropriate command with brief explanation

**User:** "Does this work with [framework]?"
**Response:** List supported frameworks and platform compatibility

## Integration Points

This skill should seamlessly hand off to:
- Specific skills when user wants to use a feature
- The `/help` command for detailed documentation
- Other skills for specialized tasks

## Files Structure

While this skill doesn't need supporting scripts, it should reference:
- `README.md` - Main project documentation
- `SOTA_IMPLEMENTATION_COMPLETE.md` - Feature details
- `CLAUDE.md` - Development guidelines
- Individual `skills/*/SKILL.md` files - Feature documentation

## Summary

The plugin-guide skill makes the Storybook Assistant approachable and discoverable. It translates natural language queries into actionable guidance, helping users find the right features without needing to know exact command names or technical details.

**Key Benefit:** Users can explore capabilities conversationally - "What can you do?" - rather than reading documentation first.
