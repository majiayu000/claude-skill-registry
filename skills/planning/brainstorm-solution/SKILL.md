---
name: brainstorm-solution
description: Structured brainstorming for technical solutions
argument-hint: <problem-statement>
---

# brainstorm-solution

**Category**: Documentation

## Usage

```bash
proc brainstorm-solution [brief] [--constraints "constraints"] [--docs "doc1,doc2"] [--template template-name] [--help]
```

## Arguments

- `[brief]`: Brief description of the feature/problem to brainstorm (if not provided, will be prompted)
- `--constraints`: Any existing constraints or requirements
- `--docs`: Comma-separated list of related documentation links
- `--template`: Use a predefined template (api-integration, data-migration, performance-optimization)
- `--help`: Show this help message

## Examples

```bash
# Full command with all options
proc brainstorm-solution --brief "Add capacity planning to training scheduler" --constraints "Must integrate with existing booking system" --docs "docs/api.md,specs/booking.md"

# Simplified - will prompt for missing info
proc brainstorm-solution "Add capacity planning to training scheduler"

# Using a template
proc brainstorm-solution --template api-integration --brief "Integrate with payment provider"

# Show help
proc brainstorm-solution --help
```

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

### 1. Parse Arguments and Show Help if Requested

If `--help` is provided, display this documentation and exit.

### 2. Initialize Brainstorming Session

a. If brief not provided as argument, prompt for it:
   ```
   🧠 Technical Brainstorming Session

   What feature or problem would you like to brainstorm?
   >
   ```

b. If constraints not provided, ask:
   ```
   Any constraints or requirements? (Press Enter to skip)
   >
   ```

c. If docs not provided, ask:
   ```
   Related documentation? (comma-separated paths, Press Enter to skip)
   >
   ```

### 3. Create Session Directory

Create directory structure:
```
docs/tech-brainstorm/YYYY-MM-DD-{feature-slug}/
```

Where feature-slug is derived from the brief (e.g., "capacity-planning")

### 4. Interactive Brainstorming Flow

Present the interactive menu:
```
📋 Brainstorming: {brief}

Available sections:
[1] Data Models & Relationships (primary)
[2] System Components & Interactions (primary)
[3] API Design & Endpoints (secondary)
[4] Technology Choices & Trade-offs (secondary)
[5] Security Considerations
[6] Scalability & Performance
[7] Integration Points
[8] Other Considerations

Commands:
- Enter number to work on section
- 'jump N' to switch sections
- 'preview' to see current progress
- 'suggest' for AI suggestions
- 'diagram' to create visualizations
- 'done' to finish session

Current section: [None]
>
```

### 5. Section-Specific Prompts

For each section, provide intelligent prompts based on the feature type and template:

#### Data Models (data-models.md):
- "What are the main entities involved?"
- "How do these entities relate to each other?"
- "What are the key attributes for each entity?"
- "Any existing models to extend or integrate with?"

#### System Components (system-components.md):
- "What are the major components/services needed?"
- "How do components communicate?"
- "What are the responsibilities of each component?"
- "Any shared services or utilities?"

#### API Design (api-design.md):
- "What endpoints are needed?"
- "What's the request/response format?"
- "Authentication/authorization approach?"
- "Rate limiting or quota considerations?"

#### Technology Choices (tech-choices.md):
- "What technologies/frameworks to use?"
- "Trade-offs between options?"
- "Build vs buy decisions?"
- "Migration or compatibility concerns?"

### 6. AI Assistance Features

When user types 'suggest', provide contextual suggestions:
- Common patterns for the problem type
- Potential pitfalls to consider
- Best practices relevant to the feature
- Questions to deepen thinking

### 7. Diagram Creation

When user types 'diagram', offer options:
```
What type of diagram?
[1] Entity Relationship (Mermaid ERD)
[2] Component/Architecture (Mermaid flowchart)
[3] Sequence Diagram (Mermaid sequence)
[4] State Machine (Mermaid stateDiagram)
>
```

Generate and save to `diagrams.md` in the session folder.

### 8. Auto-Save Progress

After each section update, save the content to the appropriate file with proper markdown formatting.

### 9. Session Completion

When user types 'done':

a. Generate `session-summary.md` with:
   ```markdown
   # Brainstorming Summary: {brief}

   Date: {date}
   Duration: {elapsed_time}

   ## Key Decisions
   - Decision 1
   - Decision 2

   ## Open Questions
   - [ ] Question 1
   - [ ] Question 2

   ## Key Models

   ### Entity: User
   - id: uuid
   - name: string
   - ...

   ## Architecture Overview
   {Include main diagram if created}

   ## Next Steps
   1. Research {specific_tech}
   2. Prototype {component}
   3. Create tech-spec document

   ## Section Completion
   - [x] Data Models & Relationships
   - [x] System Components & Interactions
   - [ ] API Design & Endpoints
   - [ ] Technology Choices & Trade-offs
   ```

b. Display summary and location:
   ```
   ✅ Brainstorming session complete!

   📁 Files created in: docs/tech-brainstorm/YYYY-MM-DD-{feature-slug}/
   - data-models.md
   - system-components.md
   - session-summary.md
   - diagrams.md

   🎯 Next: Use 'proc create-tech-spec' to formalize this into a technical specification
   ```

### 10. Template Support

If `--template` is provided, pre-populate sections with relevant prompts and common patterns:

- **api-integration**: Focus on authentication, rate limits, error handling, webhook patterns
- **data-migration**: Focus on data mapping, transformation rules, rollback strategies
- **performance-optimization**: Focus on bottlenecks, caching strategies, query optimization

## Error Handling

- If docs/tech-brainstorm/ doesn't exist, create it
- If session directory already exists, append timestamp
- Handle invalid template names gracefully
- Save progress even if session is interrupted
