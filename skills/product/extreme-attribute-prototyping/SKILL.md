---
name: extreme-attribute-prototyping
description: A framework for discovering non-obvious product solutions by rapidly building and testing radical, opposing versions of a feature's core attributes. Use this when stuck between mediocre design options, when a feature involves a fundamental trade-off (like speed vs. safety), or when designing a V1 from scratch.
---

# Extreme Attribute Prototyping

This framework avoids the "trap of the middle ground" by forcing teams to explore the radical ends of a design spectrum. By building "extreme" versions of a feature, you reveal hidden requirements and emotional hooks that lead to an "obvious in hindsight" solution.

## The 10% Velocity Rule
Before applying the framework, set the pace. Speed is a proxy for competence, not sloppiness.
*   **Set a Time Budget:** Determine how long the total feature should take to build (e.g., 4 weeks).
*   **The 10% Milestone:** By the time 10% of the budget has passed (e.g., 2-3 days), you must have a workable, internal version that tests a key hypothesis.
*   **Avoid Perfection:** Do not wait for pixel-perfect designs. Use the first 10% to "feel" the software and validate or invalidate major assumptions.

## The Prototyping Process

### 1. Identify the Core Tension
Define the two competing values or attributes for the feature.
*   *Example:* Speed vs. Safety, Customization vs. Simplicity, Predictability vs. Availability.

### 2. Design the "Extreme Archetypes"
Instead of looking for a compromise, design two radical versions that ignore the other side of the tension entirely.
*   **Version A (The Radical Max):** If "Speed" is the goal, build the version that requires zero clicks, even if it feels "unsafe" or risks data loss.
*   **Version B (The Radical Safe):** If "Safety" is the goal, build the version that auto-saves every character and interrupts the user constantly to prevent mistakes.

### 3. Build and "Feel" the Extremes
Roll out these versions to an internal group or a very small circle of "alpha" users.
*   **Identify the "Bad Feeling":** Note exactly where the extreme version makes the user feel anxious, annoyed, or frustrated. 
*   **Extract the Insight:** "Version A felt too dangerous because I didn't know if my work was saved," or "Version B felt bloated because it left a trail of 500 untitled documents."

### 4. Synthesize the "Obvious" Solution
The final product is rarely one of the extremes, but the extremes tell you exactly where the "dial" needs to be set. Use the feedback to create a version that captures the benefits of both without the "bad feelings" identified in step 3.

---

## Examples

### Example 1: Issue Drafts in Linear
**Context:** Designing a way to save work when a user is interrupted while writing a bug report.
*   **The Tension:** Speed (getting out of the way) vs. Safety (not losing data).
*   **Extreme A (The "Fastest"):** No popups. If you close the window, it's gone.
    *   *Result:* Felt "super unsafe." Users were anxious.
*   **Extreme B (The "Safest"):** Auto-save every character as a new object.
    *   *Result:* Created "paper trail bloat" (hundreds of accidental "Untitled" issues).
*   **Synthesis (The Solution):** If it's a **new** issue, interrupt the user with a "Save Draft" prompt. If it's an **existing** draft, auto-save silently in the background.

### Example 2: The Box-Cut Tee (Fashion)
**Context:** A batch of men’s shirts arrived from the factory 1.5 inches too short to sell.
*   **The Extreme:** Instead of trying to "fix" the length to a standard size, the team cut another 2 inches off to create a "Radical Crop."
*   **Application:** They marketed it specifically to women as a "Box-Cut Crop Tee."
*   **Output:** It sold out in a week and became a multi-year bestseller. By leaning into the "defect" as an extreme attribute, they found a new product-market fit.

---

## Common Pitfalls

*   **Solving for the "Middle Manager" first:** Do not add customization or reporting fields that make the Individual Contributor (IC) experience worse. If a feature makes an IC's daily workflow "feel bad," they will provide poor data, making the manager's reports useless anyway.
*   **Schlep Blindness:** Becoming so used to a manual, annoying process that you forget it’s a problem. Look for "Mondays" (tasks you dread) to find the best opportunities for extreme prototyping.
*   **Polishing the Extremes:** Spending time on UI/UX polish for an extreme prototype. The goal of an extreme version is to "feel the logic," not to look pretty.
*   **Estimation Paralysis:** Spending weeks estimating a deadline instead of building. Use the 10% rule to create a workable version immediately; the building process provides more "estimation data" than a spreadsheet ever will.