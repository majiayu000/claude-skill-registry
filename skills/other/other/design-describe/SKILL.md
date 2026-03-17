---
name: design-describe
version: 1.0.0
description: '[Design] Describe a design based on screenshot/video'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

> **Skill Variant:** Variant of design skills — describe UI from screenshot or video.

## Quick Summary

**Goal:** Analyze a screenshot or video and produce a detailed written description of the UI design.

**Workflow:**
1. **Analyze** — Process the visual input (screenshot/video) using vision capabilities
2. **Describe** — Write detailed description of layout, colors, typography, interactions

**Key Rules:**
- Use `ai-multimodal` skill for image/video analysis
- Focus on design elements: layout, spacing, colors, typography, interactions

Think hard to describe the design based on this screenshot/video:
<screenshot>$ARGUMENTS</screenshot>

## Required Skills (Priority Order)

1. **`ui-ux-pro-max`** - Design intelligence database (ALWAYS ACTIVATE FIRST)
2. **`frontend-design`** - Visual analysis

**Ensure token efficiency while maintaining high quality.**

## Workflow:

1. Use `ai-multimodal` skills to describe super details of the screenshot/video so the developer can implement it easily.
    - Be specific about design style, every element, elements' positions, every interaction, every animation, every transition, every color, every border, every icon, every font style, font size, font weight, every spacing, every padding, every margin, every size, every shape, every texture, every material, every light, every shadow, every reflection, every refraction, every blur, every glow, every image, background transparency, etc.
    - **IMPORTANT:** Try to predict the font name (Google Fonts) and font size in the given screenshot, don't just use Inter or Poppins.
2. Use `ui-ux-designer` subagent to create a design implementation plan following the progressive disclosure structure so the result matches the screenshot/video:
    - Create a directory using naming pattern from `## Naming` section.
    - Save the overview access point at `plan.md`, keep it generic, under 80 lines, and list each phase with status/progress and links.
    - For each phase, add `phase-XX-phase-name.md` files containing sections (Context links, Overview with date/priority/statuses, Key Insights, Requirements, Architecture, Related code files, Implementation Steps, Todo list, Success Criteria, Risk Assessment, Security Considerations, Next steps).
3. Report back to user with a summary of the plan.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
