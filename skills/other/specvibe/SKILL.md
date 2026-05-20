---
name: SpecVibe
description: An executable, spec-driven framework for building production-ready AI-native applications. Based on 2026 best practices.
version: 1.0.0
tags: ["spec-driven-development", "ai-native", "vibe-coding", "development-framework", "best-practices", "security", "testing", "devops"]
---

# SpecVibe: The AI-Native Development Framework

This skill provides a universal, seven-stage framework for developing production-ready, AI-native applications. It enforces a **"Specification-as-Source-of-Truth"** mindset, ensuring that every aspect of the project is defined, testable, secure, and documented before and during implementation, following the most advanced 2026 community best practices from Google, GitHub, and Thoughtworks.

## Core Philosophy

- **Intent is the Source of Truth**: The specification (`spec.md`) is the primary artifact. Code is the last-mile implementation of that intent.
- **Human-AI Collaboration**: Follow the **Delegate/Review/Own** model at every stage to maximize efficiency and maintain quality.
- **Iterate in Small, Validated Chunks**: Break down work into the smallest possible units, test them, and commit frequently. Never let the AI generate large, monolithic blocks of code.
- **Automate Everything**: Use tests, linters, CI/CD, and automated documentation to build a robust quality assurance system.

## The Seven Stages of AI-Native Development

Follow these stages sequentially. Each stage has a **Quality Gate**—a set of questions you must answer before proceeding—and a clear **Delegate/Review/Own** model for human-AI collaboration.

| Stage | Focus | Key Activities | Reference Guides |
| :--- | :--- | :--- | :--- |
| **1. Specify** | User Journey & Requirements | Create `spec.md` defining user stories, goals, and non-functional requirements. | `references/00-specvibe.md` |
| **2. Plan** | Technical Architecture | Create `PLAN.md`, select tech stack, define architecture, and break down the spec into tasks. | `references/02-backend.md`, `references/03-frontend.md` |
| **3. Test** | Behavior-Driven Definition | Write failing unit, integration, and E2E tests based on the spec and plan. | `references/05-testing.md` |
| **4. Implement** | Code Generation & Refinement | Write (or generate) code to make the tests pass, following a chunked iteration strategy. | `references/08-ai-collaboration.md` |
| **5. Review** | Quality & Security Assurance | Conduct automated and human code reviews, focusing on security, logic, and maintainability. | `references/04-security.md` |
| **6. Document** | Knowledge Capture | Automatically generate and manually refine user and developer documentation. | `references/09-documentation.md` |
| **7. Deploy** | CI/CD & Observability | Containerize, set up CI/CD pipelines, and implement full observability. | `references/06-devops.md`, `references/07-error-handling.md` |

---

## Stage 1: Specify - The Intent

**Goal**: Define *what* to build and *why* in a structured `spec.md`.

- **Delegate**: Ask the AI to interview you about the project goals and generate a draft `spec.md` using the `templates/spec-template.md`.
- **Review**: Check if the spec accurately captures all user stories, edge cases, and success metrics.
- **Own**: The final approval of the user requirements and business goals.

### Quality Gate 1: Specification Review

- *Does the `spec.md` clearly define the user, their problem, and the proposed solution?*
- *Are non-functional requirements (performance, security, accessibility) listed?*
- *Is the scope well-defined and unambiguous for an AI to understand?*

---

## Stage 2: Plan - The Blueprint

**Goal**: Translate the `spec.md` into a concrete technical plan.

- **Delegate**: Feed `spec.md` to the AI and ask it to generate a `PLAN.md` detailing the architecture, data models (using `references/01-schema-and-types.md`), API contracts (using `templates/openapi-template.yaml`), and a task breakdown.
- **Review**: Assess the proposed tech stack, architecture, and task list for feasibility and alignment with best practices.
- **Own**: The final architectural decisions and technology choices.

### Quality Gate 2: Plan Review

- *Is the chosen architecture appropriate for the project's scale and requirements?*
- *Is the API contract complete and consistent with the data models?*
- *Are the tasks small, independent, and logically sequenced?*

---

## Stage 3: Test - The Safety Net

**Goal**: Define the application's behavior through a comprehensive, failing test suite.

- **Delegate**: Ask the AI to generate a full suite of tests (unit, integration, E2E) based on `spec.md` and `PLAN.md`. Refer to `references/05-testing.md`.
- **Review**: Ensure tests cover all user stories, API endpoints, and critical business logic. Check for meaningful assertions.
- **Own**: The definition of "done" for each feature, as represented by the tests.

### Quality Gate 3: Test Suite Review

- *Does every feature in the spec have corresponding tests?*
- *Do all tests currently fail for the correct reasons?*

---

## Stage 4: Implement - The Engine Room

**Goal**: Write clean, efficient code that makes all tests pass.

- **Delegate**: Instruct the AI to implement one task at a time, feeding it the relevant spec, plan, and failing test. Use the "chunked iteration" strategy from `references/08-ai-collaboration.md`.
- **Review**: After each small chunk, review the generated code for correctness and style. Do not wait for the entire feature to be complete.
- **Own**: The responsibility for committing each validated chunk of code to version control.

### Quality Gate 4: Implementation Review

- *Do all tests for the implemented task now pass?*
- *Is the code clean, readable, and consistent with the project's style guide?*
- *Has the change been committed to Git with a clear message?*

---

## Stage 5: Review - The Quality Shield

**Goal**: Ensure the implemented code is secure, robust, and maintainable.

- **Delegate**: Automate security scans (SAST, DAST, dependency checking) in CI. Use an AI agent to perform a preliminary code review based on `references/04-security.md` (OWASP 2025).
- **Review**: A human developer must perform a final review, focusing on logic, architecture, and subtle bugs that AI might miss.
- **Own**: The final approval (LGTM) to merge the code into the main branch.

### Quality Gate 5: Code Review

- *Does the code pass all automated security and quality checks?*
- *Has a human engineer reviewed and approved the changes?*

---

## Stage 6: Document - The Knowledge Base

**Goal**: Create clear, comprehensive documentation for both users and developers.

- **Delegate**: Use AI to generate initial drafts of API documentation from the OpenAPI spec, and user guides from the `spec.md`. Refer to `references/09-documentation.md`.
- **Review**: Edit the AI-generated content for clarity, accuracy, and tone. Add diagrams and examples.
- **Own**: The final, published documentation that serves as the official source of information.

### Quality Gate 6: Documentation Review

- *Is the API documentation accurate and complete?*
- *Is the user guide easy for a non-technical person to understand?*

---

## Stage 7: Deploy - The Launchpad

**Goal**: Automate deployment and ensure the application is observable and reliable in production.

- **Delegate**: Ask the AI to generate Dockerfiles, CI/CD pipeline configurations (e.g., GitHub Actions), and infrastructure-as-code scripts. Refer to `references/06-devops.md`.
- **Review**: Verify the deployment scripts, container configurations, and monitoring setup (`references/07-error-handling.md`).
- **Own**: The production environment and the ultimate responsibility for uptime and reliability.

### Quality Gate 7: Production Readiness Review

- *Can the application be deployed and rolled back with a single command?*
- *Is comprehensive, structured logging (OpenTelemetry) in place?*
- *Are alerting and monitoring configured for key performance indicators?*
