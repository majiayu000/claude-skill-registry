---
name: arch-diagrams
cluster: se-architecture
description: "Diagrams: C4 model, PlantUML, Mermaid, sequence diagrams, ERDs, infrastructure diagrams"
tags: ["diagrams","c4","mermaid","plantuml","architecture"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "architecture diagram c4 mermaid sequence erd plantuml infrastructure"
---

# arch-diagrams

## Purpose
This skill allows OpenClaw to generate, edit, and render architecture diagrams using tools like C4 model, PlantUML, Mermaid, sequence diagrams, ERDs, and infrastructure diagrams. It integrates diagram creation into coding workflows for visualizing system designs.

## When to Use
Use this skill when documenting software architecture, planning system interactions, or creating visual aids for ERDs and sequence flows. Apply it during design phases, code reviews, or when collaborating on infrastructure setups to quickly prototype diagrams from text descriptions.

## Key Capabilities
- Generate C4 diagrams from high-level descriptions.
- Render PlantUML code into SVG or PNG outputs.
- Create Mermaid diagrams for flowcharts, sequences, and ERDs.
- Support infrastructure diagrams with tools like AWS or generic cloud icons.
- Edit existing diagrams by parsing and modifying source code (e.g., PlantUML syntax).
- Export diagrams as code snippets or image files for inclusion in docs.

## Usage Patterns
To accomplish tasks, provide a clear text description or partial diagram code to OpenClaw, then specify the diagram type. For example, invoke the skill via CLI or API with inputs like JSON configs. Always include context, such as "Generate a C4 container diagram for a web app with a database." Handle iterations by chaining commands, e.g., generate, review, and refine. Use environment variables for authentication, like setting `$OPENCLAW_API_KEY` before operations.

## Common Commands/API
Use the OpenClaw CLI for direct execution or API for programmatic access. Authenticate with `$OPENCLAW_API_KEY` in your environment.

- CLI Command: `openclaw arch-diagrams generate --type mermaid --input "sequenceDiagram: A->B: Request" --output diagram.md`
  This generates a Mermaid sequence diagram from the input string and saves it to a file.

- API Endpoint: POST to `/api/v1/arch-diagrams/generate` with JSON body: `{"type": "plantuml", "description": "@startuml\nAlice -> Bob: Hello\n@enduml", "format": "svg"}`
  Response includes the rendered SVG; handle with HTTP headers for authentication.

- Config Format: Use YAML for inputs, e.g.,
  ```
  type: c4
  elements:
    - name: System
      type: container
  ```
  Pass this via CLI flag: `--config path/to/config.yaml`.

- Code Snippet (Python):
  ```
  import requests
  response = requests.post('https://api.openclaw.ai/api/v1/arch-diagrams/generate', json={"type": "erd", "input": "User has many Posts"}, headers={'Authorization': f'Bearer {os.environ["OPENCLAW_API_KEY"]}'})
  print(response.json()['output'])
  ```

## Integration Notes
Integrate this skill into your workflow by adding it to IDE extensions (e.g., VS Code plugin for OpenClaw) or CI/CD pipelines. For example, in a GitHub Action, use: `run: openclaw arch-diagrams generate --type sequence --input ./specs.md && echo '::set-output name=diagram::$(cat diagram.md)'`. Set `$OPENCLAW_API_KEY` as a secret in your environment. When combining with other skills, pipe outputs; e.g., generate a diagram from code analysis results. Ensure compatibility by specifying versions, like OpenClaw CLI v2.5+.

## Error Handling
Always check for errors by parsing response codes or CLI exit statuses. For invalid inputs, OpenClaw returns HTTP 400 with details like "Invalid PlantUML syntax: missing @enduml". Handle network issues by retrying with exponential backoff, e.g., in code: `if response.status_code == 503: time.sleep(5); retry()`. Validate inputs before sending, such as ensuring diagram types are from ["c4", "mermaid", "plantuml", "sequence", "erd"]. Use try-except blocks for API calls, e.g.,
```
try:
    result = requests.post(url, json=data)
    result.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"Error: {e.response.text} - Fix input and retry")
```

## Concrete Usage Examples
1. **Generate a C4 System Diagram:** To visualize a simple web application, run: `openclaw arch-diagrams generate --type c4 --input "System: WebApp with Database and API" --output c4_diagram.puml`. This produces a PlantUML file for a C4 system context diagram. Review and refine by adding: `openclaw arch-diagrams edit --file c4_diagram.puml --add "Container: Frontend"`.

2. **Create an ERD for a Database Schema:** For modeling relationships, use: `openclaw arch-diagrams generate --type erd --input '{"entities": [{"name": "User", "attributes": ["id", "name"]}, {"name": "Post", "attributes": ["id", "content"]}]}' --output erd.mmd`. This outputs a Mermaid ERD code, which you can render in Markdown files.

## Graph Relationships
- In C4 diagrams: "System depends on External System", "Container uses Component".
- In Sequence diagrams: "Actor sends message to Object", "Object returns response to Actor".
- In ERDs: "Entity has one-to-many relationship with another Entity", "Attribute belongs to Entity".
- In Infrastructure diagrams: "Server connects to Database", "Load Balancer routes to Service".
