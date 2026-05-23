---
name: create-prd-feature
description: Create a feature-specific PRD (FRD) for individual features
argument-hint: <feature-name>
---

# create-prd-feature

**Category**: Product & Strategy

## Usage

```bash
create-prd-feature <feature-name>
```

## Arguments

- `<feature-name>`: Required - The name of the feature (will be used for filename and document title)

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

1. Read the FRD template from `plugins/product-design/templates/frd-template.md`
2. Start an interactive session optimized for feature-level requirements
3. Focus on gathering technical details needed for implementation
4. Generate actionable tasks and clear specifications
5. Create deliverables for business conversations
6. Save the document as `<feature-name>-frd.md`

## Interactive Session Flow

The session is designed to extract maximum technical detail for implementation:

### 1. **Initial Context** [Section 1 of 12]
- "Feature name confirmation:"
- "Which product/system does this feature belong to?"
- "Feature ID or ticket number (if exists):"
- "Epic or parent initiative link:"
- "Your name (author):"
- "Priority level (P0-Critical, P1-High, P2-Medium, P3-Low):"

### 2. **Executive Summary** [Section 2 of 12]
- "Describe this feature in one sentence:"
- "What business value does it provide? (2-3 bullet points):"
- "Estimated effort (XS/S/M/L/XL or story points):"
- "Risk level (Low/Medium/High) and why:"

### 3. **Problem & Context** [Section 3 of 12]
- "Describe the current state/problem (what's happening now):"
- "What specific problem does this feature solve?"
- "What happens if we don't implement this feature?"
- "Are there any workarounds users currently employ?"

### 4. **Objectives & Success** [Section 4 of 12]
- "List 3-5 specific, measurable objectives:"
- "How will we measure success? (provide specific metrics):"
- "Write detailed acceptance criteria (use Given/When/Then format):"

  Example:
  ```
  Given: User is on the dashboard
  When: They click the export button
  Then: A CSV file with all visible data is downloaded
  ```

### 5. **User Stories & Scenarios** [Section 5 of 12]
- "Primary user story (As a... I want to... So that...):"
- "List 3-5 key usage scenarios (step by step):"
- "Identify edge cases and error scenarios:"
- "Any special permissions or roles involved?"

### 6. **Functional Requirements** [Section 6 of 12]
This section is critical for code generation:
- "List all core functionality (be specific):"
- "Define inputs (data types, validation rules, sources):"
- "Define outputs (format, structure, destinations):"
- "List all business rules and logic:"
- "Data requirements (what data is needed, where from):"

### 7. **Technical Specifications** [Section 7 of 12]
Detailed technical requirements for implementation:
- "API endpoints needed (method, path, request/response):"

  Example:
  ```
  POST /api/v1/users/{id}/preferences
  Request: { theme: 'dark', notifications: true }
  Response: { success: true, preferences: {...} }
  ```

- "Database changes (new tables, columns, indexes):"
- "How does this impact system architecture?"
- "External systems to integrate with:"
- "Performance requirements (response time, throughput):"

### 8. **UI/UX Requirements** [Section 8 of 12]
- "List all UI components needed:"
- "Describe the user flow (with screen transitions):"
- "Link to mockups/wireframes (or describe layout):"
- "Interaction patterns (clicks, hovers, drag-drop, etc.):"
- "Responsive behavior (mobile, tablet, desktop):"

### 9. **Implementation Details** [Section 9 of 12]
Critical for task breakdown:
- "Preferred technical approach/pattern:"
- "Code structure (files, modules, classes):"
- "Specific libraries or frameworks to use:"
- "Configuration/environment variables needed:"
- "Feature flags or toggles required:"

### 10. **Task Breakdown** [Section 10 of 12]
Generate actionable tasks:
- "Break down backend tasks (API, database, business logic):"
- "Break down frontend tasks (UI components, state management):"
- "List infrastructure/DevOps tasks:"
- "Testing tasks (unit, integration, e2e):"
- "Documentation tasks:"
- "Deployment and rollout tasks:"

Provide in this format:
```
- [ ] Task description (estimate) [assignee]
  - Subtask 1
  - Subtask 2
```

### 11. **Testing & Quality** [Section 11 of 12]
- "Unit test scenarios (list key functions to test):"
- "Integration test scenarios:"
- "User acceptance test cases:"
- "Performance test requirements:"
- "Security testing needs:"

### 12. **Business Deliverables** [Section 12 of 12]
For stakeholder communication:
- "Demo scenarios (step-by-step for showcasing):"
- "Key talking points for business review:"
- "Success metrics dashboard/report format:"
- "Training needs for users:"
- "Communication plan for rollout:"

### 13. **Final Review**
- "Any open questions or blockers?"
- "Decisions needed from stakeholders?"
- "Key assumptions we're making?"
- "Related features or dependencies?"

## Output Format

Generate a comprehensive FRD document that:
- Provides clear implementation guidance
- Includes all technical specifications
- Breaks down into actionable tasks
- Serves as reference for developers
- Includes business communication materials
- Can be used directly for sprint planning

## Task Generation Guidelines

When creating the task breakdown section:
1. Each task should be 1-3 days of work
2. Include clear acceptance criteria
3. Specify dependencies between tasks
4. Add technical notes for complex tasks
5. Include testing in each task
6. Consider parallel work streams

## Example Usage

```bash
create-prd-feature user-notifications
```

This creates `user-notifications-frd.md` with detailed specs ready for implementation.

## Tips for Claude Code

1. For technical sections, ask for specific examples
2. Encourage detailed API specifications
3. Push for measurable acceptance criteria
4. Extract enough detail for accurate estimation
5. Generate tasks that can go directly to sprint planning
6. Create clear deliverables for business communication
7. Validate technical feasibility during the session
8. Suggest common patterns based on feature type
