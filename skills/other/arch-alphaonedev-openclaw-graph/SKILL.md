---
name: arch
cluster: se-architecture
description: "Root SE architecture: system design, ADRs, trade-off analysis, tech stack selection"
tags: ["architecture","design","system"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "system design architecture trade-off decision adr"
---

# arch

## Purpose
This skill handles root SE architecture tasks, including system design, creating Architecture Decision Records (ADRs), performing trade-off analyses, and selecting tech stacks. It integrates with OpenClaw's core engine to output structured artifacts like diagrams, documents, or JSON reports.

## When to Use
Use this skill when starting a new system design, evaluating architectural decisions, or resolving trade-offs in tech choices. Apply it during project kickoffs, refactoring, or when scaling systems, especially for complex applications involving microservices, cloud infrastructure, or distributed systems.

## Key Capabilities
- Generate ADRs in Markdown format with sections for context, decision, and consequences.
- Analyze trade-offs using predefined models (e.g., CAP theorem for distributed systems).
- Recommend tech stacks based on inputs like requirements, constraints, and performance metrics.
- Produce system design diagrams via integration with tools like PlantUML.
- Support iterative refinement of designs through feedback loops.

## Usage Patterns
Invoke the skill via OpenClaw CLI or API for interactive or scripted workflows. Start with a command to initialize a design session, then chain subcommands for analysis. For example, pipe outputs to other tools for visualization. Always provide inputs as JSON files for consistency. Use environment variables for authentication, like `$OPENCLAW_API_KEY`, to secure requests.

## Common Commands/API
Use the OpenClaw CLI with the `arch` subcommand. Prefix all commands with `openclaw arch`.

- **Design a system**: `openclaw arch design --input design.json --output system.md`  
  This generates a system design document. The `--input` flag requires a JSON file with fields like {"requirements": ["scalable"], "components": ["database", "API"]}.

- **Create an ADR**: `openclaw arch adr --title "Use Microservices" --context "Monolith limitations" --decision "Adopt microservices"`  
  Example snippet:  
  ```bash
  openclaw arch adr --title "Microservices ADR" > adr.md
  cat adr.md  # Outputs: # Architecture Decision Record\n## Title: Microservices ADR\n## Context: ...
  ```

- **Analyze trade-offs**: `openclaw arch tradeoff --options "monolith,microservices" --criteria "scalability,cost"`  
  API endpoint: POST /api/skills/arch/tradeoff with body: {"options": ["monolith"], "criteria": ["cost"]}  
  Response: JSON like {"winner": "microservices", "reasons": ["better scalability"]}.

- **Select tech stack**: `openclaw arch techstack --requirements "high-availability,nodejs" --constraints "budget:low"`  
  Config format: JSON input e.g., {"requirements": ["REST API"], "constraints": {"budget": 1000}}  
  API: POST /api/skills/arch/techstack returns {"recommendations": ["Express.js", "MongoDB"]}.

Always set `$OPENCLAW_API_KEY` for API calls, e.g., in curl: `curl -H "Authorization: Bearer $OPENCLAW_API_KEY" -X POST https://api.openclaw.ai/api/skills/arch/design`.

## Integration Notes
Integrate with OpenClaw by including the skill in workflows via CLI piping or API chaining. Dependencies: Node.js runtime for local execution. For auth, set `$OPENCLAW_API_KEY` as an environment variable before running commands. Example integration with Git: Hook into pre-commit to validate designs, e.g., `openclaw arch validate --file architecture.md && git commit`. Use JSON for inputs/outputs to enable parsing in scripts. Avoid direct file modifications; use `--output` flags. If using in a CI/CD pipeline, wrap commands in a script like:  
```bash
export OPENCLAW_API_KEY=your_key
openclaw arch design --input ci-input.json > output.md
```

## Error Handling
Common errors include invalid inputs (e.g., missing JSON fields) or auth failures. Check for HTTP 401 on API calls if `$OPENCLAW_API_KEY` is unset or invalid—fix by exporting the variable. For CLI, errors like "Invalid flag" return exit code 1; parse with `if [ $? -ne 0 ]; then echo "Fix input and retry"; fi`. Handle trade-off analysis errors (e.g., unsupported criteria) by catching JSON responses like {"error": "Criterion not found"} and retry with corrected inputs. Always validate JSON schemas before commands using tools like jq:  
```bash
jq . design.json  # Ensure it's valid JSON
openclaw arch design --input design.json
```

## Concrete Usage Examples
1. **Generate an ADR for a microservices migration**: First, prepare a JSON file: {"title": "Microservices Migration", "context": "Current monolith is unscalable"}. Run: `openclaw arch adr --input adr-input.json --output migration-adr.md`. This produces a Markdown ADR file for version control, e.g., commit it to track decisions.

2. **Analyze trade-offs for database selection**: Input options via CLI: `openclaw arch tradeoff --options "MongoDB,PostgreSQL" --criteria "flexibility,query-speed"`. Review the output JSON to decide, then integrate into design: `openclaw arch design --input previous-output.json`. This workflow helps in selecting PostgreSQL for complex queries based on analysis results.

## Graph Relationships
- Relates to: se-design (for detailed implementation), se-implementation (for code-level integration)
- Depends on: core-engine (for processing), se-tools (for visualization utilities)
- Conflicts with: none directly, but avoid overlapping with se-security for access controls
