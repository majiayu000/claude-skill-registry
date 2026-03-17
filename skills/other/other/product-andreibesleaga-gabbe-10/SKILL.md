---
name: business-case
description: Generate comprehensive business cases, ROI analysis, and strategic justification for new initiatives.
triggers: [business case, ROI, cost-benefit, justify project, strategic value, investment memo, pitch]
context_cost: medium
---

# Business Case Skill

## Goal
To articulate the *Why* behind a project. This skill generates a structured business case that justifies investment through clear problem definition, solution analysis, and financial projection. It bridges the gap between a raw idea and a formal project requirement.

## Steps

1.  **Problem Definition (The "Pain")**
    *   Identify the core business problem or opportunity.
    *   Quantify the impact of doing nothing (Status Quo analysis).
    *   *Prompt:* "What is broken? How much is it costing us in time, money, or opportunity?"

2.  **Strategic Alignment**
    *   Map the initiative to company goals (OKRs, KPIs).
    *   Identify stakeholders and distinct user groups.

3.  **Solution Options (The "how")**
    *   **Option 1: Do Nothing** (Baseline)
    *   **Option 2: Minimum Viable Solution** (Low cost, low risk)
    *   **Option 3: Strategic Solution** (High value, higher cost)
    *   *For each:* Analyze Pros, Cons, Risks, and Estimations.

4.  **Financial Analysis (ROI)**
    *   **Cost:** Dev hours + Infrastructure + ongoing maintenance.
    *   **Benefit:** Revenue increase + Cost savings + Risk avoidance.
    *   *Formula:* `(Net Benefit / Cost) * 100` = ROI %.
    *   *Payback Period:* Time to recoup investment.

5.  **Risk Assessment**
    *   Technical risks (complexity, legacy integration).
    *   Market risks (adoption, competition).
    *   Organizational risks (change management).

6.  **Recommendation**
    *   Select the preferred option.
    *   Define the "Definition of Success".

## Output Format
A markdown document at `docs/strategic/BUSINESS_CASE.md` following the template.

## Integration with SDLC
*   The output of this skill (`BUSINESS_CASE.md`) acts as **Step 0 — Strategy**.
*   It feeds directly into `spec-writer.skill` or `req-elicitation.skill` (S01 Requirements).
*   Validate the "Why" and "Who" here, before moving to Step 1 to define the "What".

## Constraints
*   Always quantify "pain" where possible ($, hours, %).
*   Always consider "Do Nothing" as a valid option.
*   Be realistic about costs (include maintenance, not just build).
