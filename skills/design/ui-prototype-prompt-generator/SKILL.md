---
name: ui-prototype-prompt-generator
description: This skill should be used when users need to generate detailed, structured prompts for creating UI/UX prototypes. Trigger when users request help with "create a prototype prompt", "design a mobile app", "generate UI specifications", or need comprehensive design documentation for web/mobile applications. Works with multiple design systems including WeChat Work, iOS Native, Material Design, and Ant Design Mobile.
version: 1.0.0
---

# UI/UX Prototype Prompt Generator

Generate comprehensive, structured prompts for creating production-ready UI/UX prototypes with detailed specifications and design system adherence.

---

## When to Use This Skill

Use this skill when:
- Creating detailed design briefs for web or mobile applications
- Generating structured prompts for AI-assisted UI design
- Documenting UI specifications across multiple design systems
- Building design handoff documentation for development teams
- Prototyping mobile apps with specific design system constraints
- Generating comprehensive design documentation from high-level concepts

**Trigger phrases:**
- "Create a prototype prompt for [app description]"
- "Design a mobile app for [use case]"
- "Generate UI specifications for [feature]"
- "Build a design brief for [application type]"
- "Create design documentation for [platform]"

---

## Supported Design Systems

This skill generates prompts compatible with:

| Design System | Platform | Best For |
|---------------|----------|----------|
| **WeChat Work** | Enterprise messaging | Internal enterprise apps, workflow tools |
| **iOS Native (HIG)** | Apple platforms | Consumer iOS apps, native experiences |
| **Material Design 3** | Android, Web | Cross-platform apps, Google ecosystem |
| **Ant Design Mobile** | Mobile web, Hybrid | Admin panels, data-heavy mobile apps |

**Automatic adaptation**: Prompts adjust component names, interaction patterns, and visual styles based on selected design system.

➜ **Design system details:** [references/design-systems.md](references/design-systems.md)

---

## Prompt Generation Process

### Step 1: Gather Requirements

Extract from user input:
- **Application type** (e.g., task manager, e-commerce, social app)
- **Target platform** (iOS, Android, Web, Hybrid)
- **Design system preference** (if specified)
- **Key features** (user flows, core functionality)
- **Target audience** (demographic, use case context)

### Step 2: Structure the Prompt

Generate a comprehensive prompt with these sections:

1. **Project Overview** - App purpose, target users, core value proposition
2. **Design System Specification** - Selected system and adherence requirements
3. **Page/Screen List** - Complete navigation structure
4. **Detailed Specifications** - Per-screen component breakdown:
   - Layout structure
   - Component hierarchy
   - Interaction states
   - Visual styling (colors, typography, spacing)
   - Accessibility requirements
5. **User Flows** - Critical paths and interactions
6. **Edge Cases** - Empty states, error handling, loading states
7. **Responsive Behavior** - Breakpoints and adaptive layouts (for web)
8. **Design Tokens** - Colors, typography scales, spacing system

### Step 3: Output Structured Documentation

Deliver in Markdown format with:
- Clear section hierarchy (H2, H3 headings)
- Tables for component specifications
- Code blocks for design tokens
- ASCII diagrams for layouts (when helpful)

---

## Quick Start

### Example 1: Mobile Task Manager

**User request:**
> "Create a prototype prompt for a mobile task management app using iOS Native design"

**Generated prompt structure:**

```markdown
# Task Manager App - iOS Native Prototype

## Project Overview
- **Purpose**: Simple task management for personal productivity
- **Platform**: iOS (iPhone, iPad)
- **Design System**: iOS Human Interface Guidelines
- **Target Users**: 25-45 professionals managing daily tasks

## Core Features
1. Task list with priorities
2. Calendar view
3. Categories and tags
4. Quick add with Siri shortcuts

## Screen Specifications

### 1. Home Screen (Task List)
**Layout:**
- Navigation Bar: Title "Tasks", Add button (SF Symbol: plus)
- Search Bar (UISearchBar with cancel button)
- Segmented Control: "Today" | "Upcoming" | "All"
- Table View: Tasks with swipe actions

**Components:**
- UINavigationBar (large title)
- UISegmentedControl
- UITableViewCell (custom):
  - Checkbox (SF Symbol: circle / checkmark.circle.fill)
  - Task title (SF Pro Text, 17pt)
  - Due date (SF Pro Text, 15pt, secondary label color)
  - Priority indicator (colored dot)

**Interactions:**
- Swipe right: Mark complete (green checkmark)
- Swipe left: Delete (red trash icon)
- Tap: Navigate to detail view
- Pull-to-refresh: Sync tasks

...
```

➜ **Complete example:** [examples/prompt-templates.md#task-manager](examples/prompt-templates.md)

---

### Example 2: Enterprise Dashboard (WeChat Work)

**User request:**
> "Generate UI specs for a sales dashboard using WeChat Work design system"

**Generated prompt includes:**
- WeChat Work navigation components (TabBar, NavigationBar)
- Enterprise color scheme (primary: #07C160)
- Cell components (weui-cell, weui-media-box)
- Charts and data visualization specs
- Role-based access control UI elements

➜ **Complete example:** [examples/prompt-templates.md#enterprise-dashboard](examples/prompt-templates.md)

---

### Example 3: Material Design 3 E-commerce

**User request:**
> "Design a mobile e-commerce app with Material Design 3"

**Generated prompt includes:**
- Material You dynamic color system
- FAB (Floating Action Button) placement
- Material card layouts for products
- Bottom sheet for filters
- Navigation rail (tablet), bottom bar (phone)
- Motion specifications (ease-in-out curves)

➜ **Complete example:** [examples/prompt-templates.md#ecommerce-app](examples/prompt-templates.md)

---

## Design System Adaptation Rules

### Component Mapping

When switching design systems, automatically map equivalent components:

| Generic Component | WeChat Work | iOS Native | Material Design | Ant Design Mobile |
|-------------------|-------------|------------|-----------------|-------------------|
| **Primary Button** | weui-btn_primary | UIButton (filled) | Filled Button | Button (type="primary") |
| **List Item** | weui-cell | UITableViewCell | List item | List.Item |
| **Input Field** | weui-input | UITextField | Text field | InputItem |
| **Navigation** | TabBar | UITabBar | Navigation bar | TabBar |
| **Modal** | weui-dialog | UIAlertController | Dialog | Modal |

### Visual Style Adaptation

**iOS Native:**
- Blur effects (translucent navigation bars)
- SF Symbols for icons
- SF Pro font family
- Large titles (44pt)

**Material Design 3:**
- Elevation shadows (0-5)
- Material icons
- Roboto font family
- FAB with elevation

**WeChat Work:**
- Flat design (no shadows)
- WeUI icons
- System font stack
- Green primary color (#07C160)

**Ant Design Mobile:**
- Hairline borders (0.5px)
- Ant Design icons
- PingFang SC / Roboto
- Blue primary color (#1677FF)

➜ **Full specification:** [references/design-systems.md#component-mapping](references/design-systems.md)

---

## Prompt Templates

### Template Structure

All generated prompts follow this structure:

```markdown
# [App Name] - [Design System] Prototype

## 1. Project Overview
- Purpose: [Brief description]
- Platform: [iOS/Android/Web/Hybrid]
- Design System: [Selected system]
- Target Users: [Demographics and use cases]

## 2. Information Architecture
- [Navigation structure]
- [Screen hierarchy]

## 3. Design Tokens
```css
/* Colors */
--primary: #[HEX];
--secondary: #[HEX];
...

/* Typography */
--heading-1: [size] / [line-height] [font-family];
...

/* Spacing */
--space-unit: [base unit]px;
```

## 4. Screen Specifications

### [Screen Name]
**Layout:** [Description]
**Components:**
- [Component 1]: [Spec]
- [Component 2]: [Spec]
**States:**
- Default: [Description]
- Loading: [Description]
- Error: [Description]
...

## 5. User Flows
[Critical paths with step-by-step interactions]

## 6. Accessibility
- [WCAG compliance requirements]
- [Screen reader considerations]
- [Keyboard navigation]

## 7. Edge Cases
- Empty states
- Network errors
- Permission requests
```

➜ **Customizable templates:** [examples/prompt-templates.md](examples/prompt-templates.md)

---

## Integration with Other Skills

### Workflow Combinations

**UX Design → Prompt Generation:**
```bash
# Step 1: Use ux-design-gemini for user research
memex-cli run --stdin <<'EOF'
---TASK---
backend: gemini
---CONTENT---
创建用户画像：任务管理App的目标用户
---END---
EOF

# Step 2: Use this skill to generate prototype prompt
# (Based on research insights)
```

**Prompt Generation → Code Implementation:**
```bash
# Step 1: Generate prototype prompt (this skill)
# Step 2: Use code-with-codex to implement UI
memex-cli run --stdin <<'EOF'
---TASK---
backend: codex
model: gpt-5.2-codex
---CONTENT---
实现以下UI规格：[paste generated prompt]
---END---
EOF
```

**Multi-Platform Design:**
Generate prompts for all platforms simultaneously:
```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: ios-version
backend: gemini
---CONTENT---
生成iOS原生版本的UI规格：[app description]
---END---

---TASK---
id: android-version
backend: gemini
dependencies: ios-version
---CONTENT---
基于iOS版本，生成Material Design 3规格
---END---
EOF
```

---

## Output Customization

### Verbosity Levels

**Level 1: Brief** (Quick reference)
- Component list only
- Basic interaction notes
- No design tokens

**Level 2: Standard** (Default)
- Full component specifications
- Interaction states
- Design tokens included
- One user flow example

**Level 3: Comprehensive**
- All Level 2 content
- Multiple user flows
- Accessibility annotations
- Edge case documentation
- Responsive behavior details

**Request specific level:**
> "Generate a **brief** prototype prompt for [app]"
> "Create a **comprehensive** design spec for [app]"

---

## Best Practices

### For High-Quality Prompts

1. **Be specific about target users**
   - Good: "25-35 year old professionals managing personal tasks"
   - Bad: "Anyone who needs a task manager"

2. **Specify design constraints**
   - Good: "iOS app following HIG, accessibility priority"
   - Bad: "Mobile app"

3. **Clarify feature priorities**
   - Good: "Core: task list, categories, quick add. Future: collaboration, attachments"
   - Bad: "Task manager with all features"

4. **Indicate technical constraints**
   - Mention if it's a web app (responsive required)
   - Note if it's a native app (platform-specific components)
   - Specify if hybrid (framework limitations)

### Common Pitfalls to Avoid

❌ **Mixing design systems**
- Don't combine iOS navigation with Material Design buttons

❌ **Ignoring platform conventions**
- Don't use Android back button on iOS
- Don't use iOS swipe gestures as primary on Android

❌ **Overcomplicating initial screens**
- Start with core flows, add secondary features later

✅ **Follow system defaults**
- Use native components when possible
- Respect platform interaction patterns
- Adhere to accessibility guidelines

---

## Additional Resources

### Reference Files

Detailed documentation for design system specifications:
- **[references/design-systems.md](references/design-systems.md)** - Complete design system guide
  - Component libraries
  - Visual styles
  - Interaction patterns
  - Platform-specific guidelines

### Example Templates

Working prompt examples for common app types:
- **[examples/prompt-templates.md](examples/prompt-templates.md)** - Template library
  - Task manager (iOS Native)
  - Enterprise dashboard (WeChat Work)
  - E-commerce app (Material Design 3)
  - Admin panel (Ant Design Mobile)
  - Social app (Cross-platform)

### Related Skills

- **[ux-design-gemini](../ux-design-gemini/SKILL.md)** - User research and design workflow
- **[code-with-codex](../code-with-codex/SKILL.md)** - UI implementation from specs

---

## Quick Reference

### Common Commands

**Generate prompt for iOS app:**
> "Create a prototype prompt for a [description] using iOS Native design"

**Generate prompt for Android app:**
> "Generate UI specifications for a [description] with Material Design 3"

**Generate prompt for enterprise app:**
> "Build a design brief for a [description] using WeChat Work components"

**Generate cross-platform specs:**
> "Design a [description] with responsive web layout using Material Design"

### Output Format

All prompts are delivered in Markdown format with:
- H2 headings for major sections
- Tables for component specifications
- Code blocks for design tokens (CSS custom properties)
- ASCII diagrams for complex layouts (when needed)
- Links to reference images (when helpful)

---

## Limitations

- **Not a code generator**: Produces specifications, not implementation code
- **Requires AI execution**: Prompts are designed for AI code generation tools (Codex, Claude)
- **Platform expertise needed**: Generated specs assume familiarity with target platform
- **Static specifications**: Does not include animation timings or micro-interactions (add manually)
- **No visual mockups**: Generates text descriptions, not visual designs (use Figma/Sketch separately)

---

For detailed examples and design system specifications, refer to `references/` and `examples/` directories.
