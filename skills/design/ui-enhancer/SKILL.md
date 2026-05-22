---
name: ui-enhancer
description: Systematic protocol for upgrading a 'functional' UI into a 'premium' UI.
---

# ✨ UI Enhancer Protocol

**Goal**: Transform "It works" into "It feels amazing."

## 📝 The Instruction
**When to run**:
*   After implementing a feature.
*   When a UI looks "bland" or "basic".
*   User says "Polish this".

**Protocol Steps**:

1.  **Normalization (The Skeleton)**:
    *   Sanitize Spacing: Replace all arbitrary margins (e.g., `15px`) with the Grid (`8px`, `16px`).
    *   Sanitize Colors: Replace hardcoded hex values with Semantic Tokens (`text-primary`, `bg-subtle`).
    *   Align-Items: Ensure vertical centers are perfect.

2.  **Typography Refinement (The Voice)**:
    *   Check Line-Length: Ensure text columns aren't too wide (max ~60-80 chars).
    *   Check Hierarchy: Is the Title clearly distinguishable from the Body? Increase weight/size gap if not.
    *   Soften: Change strictly black text (`#000`) to off-black (`#111` or `#1A1A1A`) for better readability.

3.  **Interaction Polish (The Soul)**:
    *   **Add Hovers**: Does the mouse cursor change? Does the background shift slightly?
    *   **Add Focus**: Can I tab through it? Is the ring visible?
    *   **Add Empty States**: If a list is empty, show a helpful illustration/message, not just blank space.

4.  **Aesthetic Lift (The Gloss)**:
    *   **Borders**: Make them standard (1px solid border-subtle).
    *   **Shadows**: Use them for depth (modals, dropdowns), not decoration. Use soft, diffused shadows.
    *   **Radius**: Consistent border-radius (e.g., `sm: 4px`, `md: 8px`).

5.  **Final Comparison**:
    *   Compare against `rules/design-system.md`.
    *   Does it look like Linear/Stripe? If 'No', iterate on spacing and contrast.

"Good design is obvious. Great design is transparent."
