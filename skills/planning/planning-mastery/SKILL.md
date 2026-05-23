---
name: planning-mastery
description: Create concise, architectural implementation plans using the RFC-Lite format. STRICTLY LIMITED VERBOSITY.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---
<domain_overview>
# 📋 RFC-Lite Planning Protocol
> **The 300-Line Limit:** If your plan exceeds 300 lines, **YOU HAVE FAILED**.
> **Rule:** Code belongs in files, not plans. Do not write pseudo-code. Do not paste entire file contents.
> **Focus:** Define *What* (Files), *How* (Logic Strategy), and *Success* (Verification).

**DEPENDENCY FORECASTING MANDATE (CRITICAL):** Never propose a change without mapping its "Blast Radius". AI-generated plans frequently fail by ignoring downstream effects on coupled modules. Before defining file changes, you MUST explicitly identify which existing features or tests might break. If a change requires "Shotgun Surgery" (modifying more than 5 files for one feature), you MUST pause and propose an architectural abstraction instead.
</domain_overview>
<philosophy>
## 🎯 CORE PHILOSOPHY
Understanding comes before implementation. A well-designed solution is half-implemented. Never code without a clear design.
</philosophy>
<template_enforcement>
## 📝 MANDATORY TEMPLATE (Copy & Fill)
```markdown
# [Task/Feature Name] - Implementation Plan
## 1. 🎯 Objective
[1-2 sentences strictly defining the goal.]
## 2. 🏗️ Tech Strategy
- **Pattern:** [e.g. Composition vs Inheritance]
- **State:** [e.g. Global Store vs Local Hook]
- **Constraints:** [e.g. "Must use LCH colors", "No external libs"]
## 3. 📂 File Changes
| Action | File Path | Brief Purpose |
|:-------|:----------|:--------------|
| [NEW]  | `src/components/MyComp.tsx` | Visual shell |
| [MOD]  | `src/App.tsx` | Routing integration |
## 4. 👣 Execution Sequence
1.  **Scaffold:** Create component files with types (No logic yet).
2.  **Logic:** Implement `useLogic.ts` hook with TDD.
3.  **Visuals:** Apply LCH gradients & Glassmorphism.
4.  **Connect:** Wire up to parent component.
## 5. ✅ Verification Standards
- [ ] **Visual:** Check against `frontend_reference.md` (no flat colors).
- [ ] **Interaction:** Verify `scale(0.97)` tap effect.
- [ ] **Console:** Zero errors during flow.
```
</template_enforcement>
<strict_rules>
## ⛔ ZERO TOLERANCE RULES
1.  **NO CODE BLOCKS:** Do not write function bodies in the plan.
2.  **NO EXPLANATIONS:** Do not teach the user *why* React is good.
3.  **NO CONVERSATION:** Do not talk to the user in the plan.
4.  **STAY HIGH LEVEL:** "Implement Auth" is better than "Write function login() { ... }".
</strict_rules>
<audit_and_reference>
## 📂 COGNITIVE AUDIT CYCLE
1. Does the plan exceed 300 lines?
2. Are all breaking changes identified?
3. Is it RFC-Lite compliant?
4. Are verification steps actionable commands?
</audit_and_reference>
