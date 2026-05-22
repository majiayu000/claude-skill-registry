---
name: agentic-engineering-workflow
description: Transition from a hands-on "bricklayer" to a high-level "architect" by managing a fleet of autonomous AI agents. Use this when you need to scale engineering output with a small team, handle repetitive migrations/bug fixes, or onboard engineers to complex legacy codebases.
---

# Agentic Engineering Workflow

This workflow enables you to transition from manual implementation to high-level system architecture by managing autonomous AI agents (like Devin) as "junior buddies." By shifting implementation to agents, you can scale a small team (e.g., 15 engineers) to handle the output of a much larger organization, aiming for 25% to 50% of pull requests to be AI-generated.

## Core Principle: Bricklayer to Architect
Most engineering time is spent on "bricklaying": debugging Kubernetes errors, fixing port issues, or writing boilerplate code. Your goal is to move to "architecting": defining the problem precisely, mapping out the solution, and specifying trade-offs, while the agent handles the execution.

## 1. Task Delegation Framework
Do not hand agents "problems" (ambiguous high-level goals); hand them "tasks" (well-defined, verifiable units of work).

*   **Verifiability:** Choose tasks that have an automated feedback loop (e.g., code that can be run, tests that can pass, or UI that can be previewed).
*   **The "Junior Buddy" Lens:** Treat the agent like a talented but new junior engineer. 
    *   **Bad Prompt:** "Fix our scaling issues."
    *   **Good Prompt:** "I'm seeing a 404 error on the signup page. Research the logs in Datadog, reproduce the bug in a local environment, and suggest a fix."

## 2. Managing the Asynchronous "Fleet"
Do not watch the AI work action-by-action. To achieve massive productivity gains, you must manage multiple agents in parallel.

*   **The 5-Devin Rule:** Aim to have up to 5 agents running at once.
*   **Morning Kickoff:** Identify the 5 most discrete tickets in your sprint (e.g., Linear or Jira). Assign each to a separate agent session.
*   **Context Sharing:** Use an integrated "Wiki" or index tool so the agent can learn the idiosyncrasies of your specific codebase (e.g., "how we handle multi-token prediction" or "our specific deployment operations").

## 3. The Integration Loop
Integrate the agent into your existing human workflows to maintain quality and oversight.

*   **Communication Channels:** Interact via Slack for quick steering and GitHub for code review.
*   **The "Jagged Intelligence" Review:** Be aware that AI has "jagged intelligence"—it may solve a complex algorithm but fail at a basic architectural convention. 
    *   Review the **Plan** before execution.
    *   Review the **PR** before merging.
*   **Interactive Planning:** If an agent asks a question (e.g., "Should the button open in a new tab?"), answer immediately to keep the asynchronous momentum.

## 4. Onboarding and Documentation
Use agents to bridge the knowledge gap for human engineers.

*   **The Devin Wiki:** Have the agent index the codebase and generate diagrams/explanations of complex modules (e.g., FP8 operations or networking abstractions).
*   **AI Mentorship:** Use agents to answer "dumb questions" for new hires, such as "Where is the feature flag for the billing module located?"

## Examples

**Example 1: Bug Reproduction and Fix**
*   **Context:** A user reports that the sidebar links are broken on mobile.
*   **Input:** Tag the agent on the Linear ticket with the specific error report.
*   **Application:** The agent spins up a virtual machine, reproduces the mobile view, identifies the CSS conflict, and runs the linter.
*   **Output:** A GitHub Pull Request with a screenshot of the fix in the mobile preview.

**Example 2: Feature Implementation**
*   **Context:** You need to add a "Newsletter Feature" component to the web app.
*   **Input:** "Modify the web app to feature this URL. Use the existing sidebar component. Make sure the link opens in a new tab."
*   **Application:** The agent researches the sidebar code, creates a new component, and asks for clarification on styling. You provide 1-2 lines of feedback on the roundness of the button.
*   **Output:** A ready-to-merge PR that matches the existing site architecture.

## Common Pitfalls
*   **Watching the Pot Boil:** Staying "synchronous" and watching the agent's terminal. This wastes your time. Kick off the task and come back when notified in Slack.
*   **Ambiguous Scoping:** Giving a task that requires 50 architectural decisions without providing a starting point. Start with a "one-pointer" task to help the agent get familiar with the repo first.
*   **Ignoring the Trace:** Not looking at the research steps the agent took. If an agent fails, check its "Playback" to see where its logic diverged from a human's.
*   **Over-Reliance on Base IQ:** Assuming the AI knows your company's specific "messiness" (e.g., old COBOL or legacy wrappers). You must explicitly point it to the documentation for your "jagged" areas.