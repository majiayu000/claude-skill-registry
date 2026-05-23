---
name: generate-db-diagram
description: Generate database diagram for a feature
argument-hint: [feature-name]
disable-model-invocation: true
allowed-tools: Bash(npx *)
---

# Generate Database Diagram

Generate a Mermaid class diagram representing the database schema related to: $ARGUMENTS

## Instructions

### 1. Identify Relevant Models/Tables

Search the codebase for models, entities, or schema definitions related to the specified feature.

#### Guidelines
- Focus on the core tables/models needed to understand the feature's data structure
- If a feature has many related models, prioritize the most important ones
- If uncertain about which models to include, err on the side of including related models
- Search thoroughly through the codebase to find all relevant schema definitions

### 2. Generate Mermaid Diagram

Follow these rules:
- Use Mermaid class diagram syntax
- Include only models directly related to the feature
- Show only important fields (exclude: id, created_at, updated_at, timestamps unless critical)
- Do NOT include field types UNLESS it's a relationship field
- For relationship fields, show them as:
  - `FK to ModelName` (foreign key / belongs to)
  - `O2O to ModelName` (one-to-one)
  - `M2M to ModelName` (many-to-many)
- Show relationships between models using Mermaid relationship syntax:
  - `Model1 "1" --> "many" Model2 : relationship_name`
  - `Model1 "1" --> "1" Model2 : relationship_name`
  - `Model1 "many" --> "many" Model2 : relationship_name`
- Keep it clean and focused on the feature's data structure

#### Example Output
```
classDiagram
    class Project {
        name
        description
        status
        owner FK to User
    }

    class Task {
        title
        completed
        project FK to Project
        assignee FK to User
    }

    class User {
        email
        name
    }

    Task "many" --> "1" Project : project
    Task "many" --> "1" User : assignee
    Project "many" --> "1" User : owner
```

### 3. Generate the Diagram Image
- Create a PNG image: `.claude/outputs/db-diagram-<feature-name>.png` (use kebab-case)
- Create the `.claude/outputs/` directory with a `.gitkeep` if it doesn't exist
- No temporary files needed - pipe directly to mermaid-cli

#### Steps
1. Pipe the Mermaid class diagram code directly to `npx @mermaid-js/mermaid-cli` using stdin:
   ```bash
   mkdir -p .claude/outputs && touch .claude/outputs/.gitkeep && cat << 'EOF' | npx -y @mermaid-js/mermaid-cli -i - -o .claude/outputs/db-diagram-<feature-name>.png
   classDiagram
       class Project {
           name
           description
           status
           owner FK to User
       }

       class Task {
           title
           completed
           project FK to Project
           assignee FK to User
       }

       class User {
           email
           name
       }

       Task "many" --> "1" Project : project
       Task "many" --> "1" User : assignee
       Project "many" --> "1" User : owner
   EOF
   ```
2. Inform the user that the diagram has been created at `.claude/outputs/db-diagram-<feature-name>.png`
