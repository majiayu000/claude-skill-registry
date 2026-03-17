---
name: system-diagram-generator
description: Creates visual representations of system structure including architecture diagrams, data flow diagrams, deployment diagrams, and sequence diagrams. Use when Claude needs to visualize system components, infrastructure, data flows, or interactions. Supports Mermaid (recommended for Markdown/GitHub), PlantUML (for detailed UML), and Graphviz/DOT (for complex networks). Trigger when users request diagrams, visualizations, or ask to "show", "diagram", "visualize", or "map out" system architecture, infrastructure, data flows, or component interactions.
---

# System Diagram Generator

Generate clear, accurate visual representations of system structure using text-based diagram formats.

## Quick Start

When a user requests a system diagram:

1. **Understand the system**: Ask clarifying questions about components, relationships, and scope
2. **Choose the format**: Select based on user preference or context (default to Mermaid for versatility)
3. **Select diagram type**: Match the visualization to the information being conveyed
4. **Generate the diagram**: Create the diagram code with clear labels and structure
5. **Provide context**: Include a brief explanation of what the diagram shows

## Format Selection

### Mermaid (Default)
Use for most cases - renders in Markdown, GitHub, GitLab, and many documentation tools.

**Best for:**
- Quick visualizations
- Documentation in Markdown files
- GitHub/GitLab README files
- General-purpose diagrams

**See:** [mermaid-patterns.md](references/mermaid-patterns.md) for examples

### PlantUML
Use when detailed UML diagrams are needed or when working with Java/enterprise systems.

**Best for:**
- Detailed UML diagrams
- C4 architecture models
- Complex component relationships
- Enterprise documentation

**See:** [plantuml-patterns.md](references/plantuml-patterns.md) for examples

### Graphviz/DOT
Use for complex network topologies or when fine-grained layout control is needed.

**Best for:**
- Network diagrams
- Complex hierarchies
- Graph structures
- Custom layout requirements

**See:** [graphviz-patterns.md](references/graphviz-patterns.md) for examples

## Diagram Types

### Architecture Diagrams
Show system components, services, databases, and their relationships.

**Use when:**
- Explaining system structure
- Documenting microservices
- Showing component dependencies
- Illustrating system boundaries

**Key elements:**
- Services/components (boxes)
- Databases (cylinders)
- External systems
- Communication protocols
- Data stores

### Data Flow Diagrams
Illustrate how data moves through the system.

**Use when:**
- Explaining data processing pipelines
- Documenting ETL processes
- Showing transformation steps
- Illustrating validation flows

**Key elements:**
- Data sources
- Processing steps
- Transformations
- Data stores
- Outputs

### Deployment Diagrams
Show infrastructure, servers, containers, and deployment topology.

**Use when:**
- Documenting cloud infrastructure
- Explaining deployment architecture
- Showing network topology
- Illustrating container orchestration

**Key elements:**
- Cloud providers/regions
- Networks/subnets
- Servers/containers
- Load balancers
- Databases and caches

### Sequence Diagrams
Visualize API calls, user interactions, and process flows over time.

**Use when:**
- Documenting API interactions
- Explaining authentication flows
- Showing request/response cycles
- Illustrating multi-step processes

**Key elements:**
- Actors/participants
- Messages/calls
- Time sequence (top to bottom)
- Return values
- Conditional logic

## Best Practices

### Clarity
- Use descriptive, meaningful names for all components
- Keep diagrams focused on one aspect of the system
- Avoid overcrowding - split complex systems into multiple diagrams
- Use consistent naming conventions

### Structure
- Group related components using subgraphs/clusters
- Show clear directional flow (left-to-right or top-to-bottom)
- Use appropriate shapes for different component types
- Include relevant protocols and technologies

### Context
- Add a title or caption explaining what the diagram shows
- Include legends for non-obvious symbols or colors
- Provide brief explanations of key components
- Note any assumptions or simplifications

### Format-Specific
- **Mermaid**: Use standard graph types (flowchart, sequence, C4)
- **PlantUML**: Leverage UML stereotypes and C4 includes
- **Graphviz**: Use clusters for grouping and rankdir for layout

## Workflow

1. **Gather requirements**
   - What system or process needs visualization?
   - What level of detail is needed?
   - Who is the audience?
   - Any format preferences?

2. **Choose format and type**
   - Select diagram format (Mermaid/PlantUML/Graphviz)
   - Select diagram type (architecture/data flow/deployment/sequence)
   - Load relevant reference file if needed

3. **Create diagram**
   - Define all components/nodes
   - Establish relationships/edges
   - Add grouping/structure
   - Include labels and protocols

4. **Validate and refine**
   - Ensure all components are labeled
   - Verify relationships are clear
   - Check for visual balance
   - Add explanatory text

5. **Deliver**
   - Provide the diagram code in a code block
   - Include brief explanation
   - Suggest improvements or variations if relevant

## Example Usage Patterns

**User:** "Show me the architecture of our authentication system"
→ Create Mermaid architecture diagram showing auth components

**User:** "Diagram the data flow for user registration"
→ Create Mermaid flowchart showing registration data flow

**User:** "Visualize our AWS deployment"
→ Create Mermaid or Graphviz deployment diagram with AWS infrastructure

**User:** "Show the sequence of API calls for checkout"
→ Create Mermaid sequence diagram showing checkout flow

**User:** "I need a detailed UML component diagram"
→ Create PlantUML component diagram with stereotypes

**User:** "Map out our network topology"
→ Create Graphviz network diagram with clusters
