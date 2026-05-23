---
name: nielsen-usability-heuristics
description: UI design and review should apply Nielsen's 10 Usability Heuristics — the foundational principles for evaluating and improving usability. Use when auditing an interface, designing interaction flows, writing error messages, or reviewing any UI for usability issues.
metadata:
  priority: 8
  docs:
    - "https://www.nngroup.com/articles/ten-usability-heuristics/"
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "**/*.vue"
    - "**/*.svelte"
    - "design-system/**"
    - "ui/**"
  promptSignals:
    phrases:
      - "usability"
      - "nielsen"
      - "heuristic"
      - "ux review"
      - "ui audit"
      - "error message"
      - "user feedback"
      - "ui clarity"
retrieval:
  aliases:
    - nielsen heuristics
    - usability principles
    - ux heuristics
    - usability audit
    - heuristic evaluation
  intents:
    - audit ui for usability
    - improve error messages
    - review interaction flow
    - check ui against best practices
    - reduce user errors
  examples:
    - review this component for usability issues
    - is this error message good
    - how do I make this flow less confusing
---

# Nielsen's 10 Usability Heuristics

Foundational principles for evaluating and designing usable interfaces. Apply these as a review checklist and as design constraints from the start — not only as a post-hoc audit tool.

---

## 1. Visibility of System Status

The design should always keep users informed about what is going on, through appropriate feedback within a reasonable amount of time.

Users cannot make good decisions without knowing the current state of the system. Trust is built through clear, timely feedback.

**In practice:**
- Show loading states, progress indicators, and completion confirmations
- Indicate where the user is in a multi-step process
- Reflect state changes immediately (optimistic UI or loading spinners)
- Never leave a user wondering whether an action was registered

**Review question:** After any user action, is the outcome visible within 1 second?

---

## 2. Match Between System and Real World

The design should speak the users' language — words, phrases, and concepts familiar to the user, not internal jargon or system terminology.

Follow real-world conventions and natural mapping so the interface feels intuitive rather than requiring translation.

**In practice:**
- Use terminology the target audience uses, not what the engineering team uses
- Icons should match real-world objects or widely established web conventions
- Spatial metaphors should match real-world expectations (e.g. "trash" for deletion)
- Avoid exposing internal system concepts (IDs, error codes, process names) to end users

**Review question:** Would a user unfamiliar with this product understand every label and term?

---

## 3. User Control and Freedom

Users often perform actions by mistake. They need a clearly marked emergency exit to leave an unwanted state without going through an extended process.

Easy undo and escape paths foster confidence and prevent users from feeling trapped.

**In practice:**
- Always provide Undo for destructive or irreversible actions
- Modals and dialogs need an obvious close/cancel action
- Multi-step flows need a way to go back
- Destructive actions (delete, publish, send) should be reversible where possible — or require explicit confirmation

**Review question:** Can the user get out of any state without losing their work or needing to contact support?

---

## 4. Consistency and Standards

Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions.

Consistency reduces cognitive load by meeting expectations users have built from other products.

**In practice:**
- Use the same label for the same action across the entire product
- Follow platform conventions (e.g. left-swipe to delete on mobile, Cmd+Z for undo)
- Design system components should look and behave identically everywhere they appear
- Do not rename standard web patterns (e.g. calling a "breadcrumb" a "path trail")

**Review question:** Does the same action always look and behave the same way throughout the product?

---

## 5. Error Prevention

Good error messages matter, but the best designs prevent errors from occurring in the first place.

Prevention addresses both slips (unintentional actions) and mistakes (misunderstanding of design intent).

**In practice:**
- Use constraints to make wrong inputs impossible (e.g. disable a Submit button until required fields are complete)
- Confirm before destructive or irreversible actions
- Use input masks, validation, and sensible defaults to guide correct input
- Design forms so the happy path is the obvious path

**Review question:** For every destructive or irreversible action, is there a confirmation step or an undo path?

---

## 6. Recognition Rather Than Recall

Minimise the user's memory load by making elements, actions, and options visible. The user should not have to remember information from one part of the interface to another.

Recognition requires less cognitive effort than recall. Visible affordances reduce the work of using the product.

**In practice:**
- Show relevant options in context rather than requiring users to remember commands
- Display previously entered data when relevant (e.g. pre-fill known fields)
- Use icons with labels — icons alone are ambiguous to many users
- Navigation should be visible at all times, not hidden behind a gesture or hover

**Review question:** Does a returning user need to remember anything to pick up where they left off?

---

## 7. Flexibility and Efficiency of Use

Shortcuts — hidden from novice users — may speed up interaction for expert users. The design should serve both.

Accelerators, customisation, and personalisation let experienced users work faster without adding complexity for beginners.

**In practice:**
- Provide keyboard shortcuts for frequent actions
- Support both guided flows (for new users) and direct paths (for experts)
- Allow users to customise views, filters, or layouts they use repeatedly
- Surface frequently used actions prominently based on usage patterns

**Review question:** Can a power user complete their most frequent task significantly faster than a first-time user?

---

## 8. Aesthetic and Minimalist Design

Interfaces should not contain information that is irrelevant or rarely needed. Every extra unit of information competes with relevant information and reduces its relative visibility.

Focus content and visual design on the essentials that support primary user goals. Less is more, only when the less is the right less.

**In practice:**
- Remove decorative elements that carry no meaning
- Secondary and tertiary actions should be visually subordinate to primary ones
- Avoid showing all features simultaneously — progressive disclosure reveals complexity only when needed
- Empty states, error states, and loading states deserve the same design attention as content states

**Review question:** Does every element on screen earn its place, or is something there "just in case"?

---

## 9. Help Users Recognize, Diagnose, and Recover from Errors

Error messages should be expressed in plain language, precisely indicate the problem, and constructively suggest a solution.

Error messages are a UX surface — they deserve the same care as any other UI copy.

**In practice:**
- Never show raw error codes or stack traces to end users
- State clearly what went wrong in plain language
- Tell the user what to do next, not just what failed
- Use appropriate visual treatment: red for errors, but not red for warnings or info
- Inline validation errors should appear adjacent to the problematic field

**Review question:** Does every error message tell the user what happened, why, and what to do next?

---

## 10. Help and Documentation

It is best if the system does not need any additional explanation. However, it may be necessary to provide documentation to help users complete tasks.

Help should be contextual, searchable, and actionable — not a last resort buried in a footer.

**In practice:**
- Prefer self-explanatory UI over tooltips; prefer tooltips over documentation
- Inline help (placeholder text, helper text, tooltips) should appear at the point of need
- Documentation should be task-oriented ("How do I…") not feature-oriented ("About the settings panel")
- Empty states are an opportunity for contextual help, not just a blank screen

**Review question:** Can a confused user find help without leaving the current screen?

---

## Heuristic Review Checklist

| # | Heuristic | Check |
|---|---|---|
| 1 | System status | Every action gives visible feedback within 1s |
| 2 | Real-world language | No jargon, terminology matches user vocabulary |
| 3 | User control | Undo available, exit paths always visible |
| 4 | Consistency | Same action = same label and behaviour everywhere |
| 5 | Error prevention | Irreversible actions have confirmation or undo |
| 6 | Recognition over recall | Options visible in context, no hidden commands |
| 7 | Flexibility | Power users have faster paths to frequent tasks |
| 8 | Minimalist design | Every element earns its place |
| 9 | Error recovery | Error messages are plain, specific, and actionable |
| 10 | Help and docs | Help is contextual and available at point of need |
