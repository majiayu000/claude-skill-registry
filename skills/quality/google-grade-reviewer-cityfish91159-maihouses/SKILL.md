---
name: google_grade_reviewer
description: Applies Google's engineering practices for strict, health-focused code reviews.
allowed-tools: Read, Edit
---

# Google-Grade Review Protocol

## 1. Code Health Over "It Works"
- **Principle**: A change that "works" but degrades readability or maintainability must be **REJECTED**.
- **Check**:
    - Is the code consistent with the project's style?
    - Is it "Atomic"? (Focuses on one thing). If not, suggest splitting the PR.
    - Are variable names descriptive enough to not need comments?

## 2. Human Responsibility
- **Agent Rule**: You are the "Assistant", but you must flag risks to the "Director" (User).
- **Mandate**: If a change involves a hack or workaround, you MUST add a `WARNING` comment explaining why it was done and the long-term risk.

## 3. The "Why" Rule
- Code comments should explain **WHY**, not **WHAT**.
- *Bad*: `// increment i`
- *Good*: `// increment retry count to handle flakey network`

## 4. Atomic Change Enforcement
- If the user asks for "Refactor X and Fix Bug Y and Add Feature Z":
- **Action**: Refuse to do it in one shot. Propose 3 separate steps:
    1.  Refactor X (Pure refactor, no logic change).
    2.  Fix Bug Y (Minimal fix).
    3.  Add Feature Z (New functionality).
