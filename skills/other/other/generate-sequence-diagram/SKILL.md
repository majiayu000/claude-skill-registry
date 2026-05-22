---
name: generate-sequence-diagram
description: Generate sequence diagram for a feature
argument-hint: [feature-name]
disable-model-invocation: true
allowed-tools: Bash(npx *)
---

# Generate Sequence Diagram

Generate a simple Mermaid sequence diagram showing the flow of a feature: $ARGUMENTS

## Instructions

### 1. Identify the Feature Flow
Search the codebase to understand how the feature works:
- Find the entry point (API view, signal, management command, etc.)
- Identify the key functions/methods called
- Understand the order of operations
- Note important interactions between components

#### Guidelines
- Focus on the main happy path flow
- Keep it simple - only show essential steps
- Include key function calls and their purpose
- Skip trivial operations (logging, validation unless critical)

### 2. Generate Mermaid Sequence Diagram
Follow these rules:
- Use Mermaid sequence diagram syntax
- Keep it SIMPLE - max 10-15 key steps
- Show participants (actors, models, functions, external services)
- Use clear, descriptive step descriptions
- Group related operations in loops or alt blocks when helpful
- Add notes to separate major phases

#### Example Output
```
sequenceDiagram
    autonumber

    Note over User,Storage: CREATING RESOURCE

    participant User
    participant API
    participant create_resource
    participant Storage

    User->>API: POST /resources/ with data
    API->>create_resource: create_resource(data)
    create_resource->>Storage: Save to database
    create_resource-->>API: Return resource
    API-->>User: Return 201 Created

    Note over User,Storage: PROCESSING RESOURCE

    participant process_task

    API->>process_task: process_resource.delay(resource_id)

    loop Each item
        process_task->>process_task: Process item
    end

    process_task->>Storage: Update status
```

### 3. Generate the Diagram Image
- Create an SVG image: `.claude/outputs/sequence-diagram-<feature-name>.svg` (use kebab-case)
- Create the `.claude/outputs/` directory with a `.gitkeep` if it doesn't exist
- Use SVG format for better scalability and readability

#### Steps
1. Pipe the Mermaid sequence diagram code directly to `npx @mermaid-js/mermaid-cli` using stdin:
   ```bash
   mkdir -p .claude/outputs && touch .claude/outputs/.gitkeep && cat << 'EOF' | npx -y @mermaid-js/mermaid-cli -i - -o .claude/outputs/sequence-diagram-<feature-name>.svg
   sequenceDiagram
       autonumber

       participant User
       participant API
       participant create_resource

       User->>API: POST /resources/
       API->>create_resource: create_resource(data)
       create_resource-->>API: resource
       API-->>User: 201 Created
   EOF
   ```
2. Inform the user that the diagram has been created at `.claude/outputs/sequence-diagram-<feature-name>.svg`

## Tips for Simple Diagrams
- Combine multiple small steps into one meaningful step
- Use descriptive names instead of technical details
- Focus on WHAT happens, not HOW it happens internally
- Use notes to separate major phases
- Limit to 10-15 steps maximum
- Group repetitive operations in loops
