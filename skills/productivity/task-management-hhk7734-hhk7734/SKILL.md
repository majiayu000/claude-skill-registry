---
name: task-management
description: A comprehensive framework for high-performance engineering management and task execution. It guides users through reducing ambiguity, defining "Done," choosing the optimal leadership positioning, and managing risks via implication-based communication.
---

# Task Management

This skill operationalizes "Seniority" and "Engineering Management" into a repeatable process. It enforces standards for reducing ambiguity, defining completion based on business value, and positioning oneself effectively between technical details and strategic direction.

## 1. Phase: Ambiguity Reduction (The Seniority Test)

True seniority is defined by the ability to take abstract/fuzzy requirements and turn them into concrete plans. Before execution, you must define the problem, not just the solution.

**Diagnostic Questions:**

1. **What is the underlying problem?** (Separate the requested solution from the actual pain point).
2. **Who is the specific user?** (Be specific; "the team" or "users" is insufficient).
3. **The "Why" Test:** Can the engineer explain *why* this feature exists in the product vision? If the answer is "because PM asked," the context is broken.
4. **Risk Assessment:** What happens if we are wrong?

**Output Required:**

- A **Problem Statement** that replaces the original vague request.
- **Clarification Action Items** (e.g., "Sync with stakeholders regarding naming conventions") [Conversation History].

## 2. Phase: Strategic Positioning (Command & Control)

Do not blindly "work hard." Determine your optimal positioning based on **Situational Awareness** (knowing what/why is happening) and **Operational Clarity** (team knows what to do).

**Select Your Mode:**

- **Crisis Mode** (Low Awareness, Low Clarity): **Learn & Stabilise.** Prioritize coding/investigation to regain control immediately.
- **Ambiguity** (High Awareness, Low Clarity): **Lead by Example.** Code alongside the team to set standards and build shared understanding.
- **Flying Blind** (Low Awareness, High Clarity): **Passive Coding.** Trust the team's direction but do targeted contributions (e.g., bug fixes) to ramp up context.
- **Clarity** (High Awareness, High Clarity): **Strategic Direction.** Step back from coding. Focus on long-term planning, risk mitigation, and "Wolf Time" (71/29 rule) allocation.

## 3. Phase: Definition of "Done" (Artifacts over Efforts)

"Done" is not a feeling or an effort; it is a social construct defined by the satisfaction of the stakeholder/company. Work is only complete when it produces readable results.

**Standard for Engineering Completion:**

Development is effectively "Done" only when the following artifacts exist:

1. **PR Merged**: Code review passed and merged.
2. **CD Image**: A deployable image generated via CI/CD.
3. **Versioned Helm Chart**: A chart capable of running the image.
4. **End-to-End Validation**: Proof that it works in the target environment (e.g., specific GPU targeting confirmed).

**The "Done" Manifesto:**

- Do not report "Investigation" as a result. Report the **Document** produced.
- Do not report "Refactoring" as a result. Report the **Performance Metric** improved or **Tech Debt** removed.
- **Declare Victory and Leave:** When the criteria are met, explicitly state "This task is complete" and move to the next challenge. Do not get trapped in infinite gardening.

## 4. Phase: Execution & Communication

Communication must bridge the gap between technical facts and business decisions.

**Implication-Based Communication:**

- **BAD (Fact-only):** "OOM occurred." / "Cache hit rate changed."
- **GOOD (Implication):** "OOM occurred, which implies we cannot support the target batch size. Recommendation: Decrease batch size or increase GPU memory request."

**Risk Management:**

If the "Expected Result" and the "Schedule" are misaligned:

1. **Acknowledge** the gap immediately.
2. **Identify** the cause.
3. **Propose** a mitigation plan (e.g., "Draft by Jan 7, Final by Jan 14").

## Example Usage

**Input Task:** "Action item: Please actually write the templates and validate that they work end-to-end."

**Applied Framework:**

1. **Ambiguity:** Clarified "Write templates" -> "Create Odin presets for specific GPU models." Synced on naming conventions.
2. **Positioning:** **Ambiguity Mode**. The manager/senior engineer will write the initial templates (Lead by Example) to set the standard for the Hanoi team.
3. **Definition of Done:** Artifacts = Preset File + Doc + Validation Log + Versioned Chart.
4. **Closing:** "Task Complete. Hanoi team can now target GPUs using label `x`. Documentation is at `link`."
