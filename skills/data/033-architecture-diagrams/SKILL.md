---
name: 033-architecture-diagrams
description: Use when you need to generate Java project diagrams — including UML sequence diagrams, UML class diagrams, C4 model diagrams, UML state machine diagrams, UML Deployment Diagrams, ER (Entity Relationship) diagrams, and bounded-context diagrams — through a modular, step-based interactive process that adapts to your specific visualization needs. This should trigger for requests such as Generate UML diagram; Create sequence diagram; Create class diagram; Create state machine diagram; Create deployment diagram; Create C4 diagram; Create bounded-context diagram; Create context-map diagram. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Java Diagrams Generator with modular step-based configuration

Generate comprehensive Java project diagrams through a modular, step-based interactive process that covers UML sequence diagrams, UML class diagrams, C4 model diagrams, UML state machine diagrams, UML Deployment Diagrams, ER (Entity Relationship) diagrams, and bounded-context diagrams using PlantUML syntax. **This is an interactive SKILL**.

**What is covered in this Skill?**

- UML sequence diagram generation for application workflows and API interactions
- UML class diagram generation for package structure and class relationships
- C4 model diagram generation for Context, Container, and Component diagrams
- UML state machine diagram generation for entity lifecycles and business workflows
- UML Deployment Diagram generation for runtime topology, nodes, execution environments, deployed components, data stores, queues, external systems, and communication paths
- ER diagram generation from SQL schema (DDL, migrations) using PlantUML Chen notation
- Bounded-context diagram generation for DDD context maps across one or more repositories
- PlantUML syntax for all diagram types
- File organization strategies: single-file, separate-files, or integrated with existing documentation
- Final diagram validation with PlantUML syntax checking
- Docker-based PlantUML validation and PNG/SVG rendering with the official `plantuml/plantuml` image

## Constraints

Before applying any diagram generation, ensure the project validates. If validation fails, stop immediately — do not proceed until all validation errors are resolved.

- **MANDATORY**: Run `./mvnw validate` or `mvn validate` before applying any diagram generation
- **SAFETY**: If validation fails, stop immediately — do not proceed until all validation errors are resolved
- **BEFORE READING DIAGRAM REFERENCES**: Run the question flow embedded in this SKILL.md first. Ask the diagram preference questions one by one, collect selected diagram families and output preferences, then read only the implementation references selected by the user's answers
- **C4 SCOPE**: C4 diagrams are restricted to Context, Container, and Component diagrams
- **SUPPLY CHAIN**: Generated PlantUML diagrams must use trusted local includes only; do not use remote `!include` URLs for C4 or icon libraries

## When to use this skill

- Generate UML diagram
- Create sequence diagram
- Create class diagram
- Create state machine diagram
- Create deployment diagram
- Create C4 diagram
- Generate ER diagram
- Create bounded-context diagram
- Create context-map diagram

## Workflow

1. **Validate project state**

Run `./mvnw validate` or `mvn validate` before applying any diagram generation.

Step constraints:
- If validation fails, stop and ask to resolve errors first

2. **Ask diagram assessment questions before reading references**


Run this XML-included question flow before reading any diagram-family implementation reference. Ask questions one-by-one in strict order, wait for the user's answer to each question, and record selected diagram families, C4 scope, bounded-context repository scope, output organization, file format, and documentation preference before continuing.


IMPORTANT: You MUST ask these questions in the exact order and wording shown here. The very first question to the user MUST be "Question 1: What diagrams do you want to generate?". Do not ask any other questions prior to it.

Diagrams Selection

Conditional Flow Rules:
- Based on your selection here, only the relevant diagram generation steps will be executed.
- If you choose "Skip", no diagrams will be generated.
- Each diagram type has its own conditional follow-up questions.

---

**Question 1**: What diagrams do you want to generate?

Options:
- UML sequence diagrams
- UML class diagrams
- UML state-machine diagrams
- C4 model diagrams (Context, Container, Component)
- UML Deployment Diagrams
- ER diagrams (Entity Relationship)
- Bounded-context diagrams
- All diagrams
- Skip

---

**Question 2**: For UML sequence diagrams, which types would you like to generate?
Ask this question only if you selected "UML sequence diagrams" or "All diagrams" in Question 1.

Options:
- Main application flows (user journeys, authentication, core features)
- API interactions (REST endpoints, request/response patterns)
- Complex business logic flows (multi-step processes, transactions)
- All sequence diagram types
- Skip

---

**Question 3**: For UML class diagrams, which scope would you like to cover?
Ask this question only if you selected "UML class diagrams" or "All diagrams" in Question 1.

Options:
- All packages (complete project structure)
- Core business logic packages only
- Specific packages (I'll specify which ones)
- Skip

---

**Question 4**: For UML class diagrams, what level of detail do you prefer?
Ask this question only if you selected "UML class diagrams" or "All diagrams" in Question 1 and did not select "Skip" in Question 3.

Options:
- High-level (classes and relationships only)
- Detailed (include key methods and attributes)
- Full detail (all public methods, attributes, and annotations)

---

**Question 5**: For C4 model diagrams, which levels would you like to generate?
Ask this question only if you selected "C4 model diagrams" or "All diagrams" in Question 1.

Options:
- Complete C4 model (Context, Container, Component)
- High-level diagrams only (Context and Container)
- Component diagrams only
- Specific C4 levels (Context, Container, and/or Component)
- Skip

---

**Question 6**: For UML state-machine diagrams, which types would you like to generate?
Ask this question only if you selected "UML state-machine diagrams" or "All diagrams" in Question 1.

Options:
- Entity lifecycles (domain object state transitions like Order, User, Document)
- Business workflows (process state machines like approval, payment, shipping)
- System behaviors (component operational states like connections, jobs, transactions)
- User interactions (UI component state transitions like forms, wizards, dialogs)
- All state machine types
- Skip

---

**Question 7**: For ER diagrams, which schema scope would you like to cover?
Ask this question only if you selected "ER diagrams (Entity Relationship)" or "All diagrams" in Question 1.

Options:
- Complete database schema (all tables)
- Core domain tables only
- Specific tables (I'll specify which ones)
- Skip

---

**Question 8**: For bounded-context diagrams, which repositories should be represented?
Ask this question only if you selected "Bounded-context diagrams" or "All diagrams" in Question 1.

Options:
- Current repository only
- One or more local repository paths (I'll provide paths)
- One or more repository URLs (I'll provide URLs)
- A named repository list (I'll provide names and context)
- Skip

For each repository in scope, collect what is available: repository name or path, bounded context, domain or subdomain, owning team, application type, owned data store, exposed interfaces, consumed interfaces, and known relationships.

---

**Question 9**: For UML Deployment Diagrams, what source material should be used first?
Ask this question only if you selected "UML Deployment Diagrams" or "All diagrams" in Question 1.

Options:
- Existing deployment diagram image or topology sketch (I'll provide the image)
- System description file (I'll provide the file path)
- Repository documentation, configuration, or deployment descriptors
- Ask me for missing deployment topology details
- Skip

When a deployment image or system description file is provided, use it as source material before asking fallback questions. Ask only for missing or ambiguous deployment facts such as actors, services, CI/CD systems, runtime nodes, execution environments, deployed artifacts or components, external systems, data stores, queues, protocols, ports, relationships, and infrastructure or network boundaries.

---

**Question 10**: How would you like to organize the generated diagram files?

Options:
- Single directory (all diagrams in /diagrams folder)
- Organized by type (separate folders for each diagram type)
- Organized by package/domain (group related diagrams together)
- Integrated with existing documentation structure

---

**Question 11**: What file format would you prefer for the diagrams?

Options:
- PlantUML source files (.puml) only
- PlantUML with markdown documentation
- Both PlantUML and generated images (requires PlantUML rendering)
- Integrated into existing documentation files

---

**Question 12**: Would you like to include explanatory documentation with the diagrams?

Options:
- Yes, comprehensive explanations for each diagram
- Yes, brief descriptions and usage notes
- No, just the diagrams
- Integrate explanations into existing documentation

---


After all applicable questions are answered, confirm the selections and map them to references:

- If UML sequence diagrams are selected, read `references/033-architecture-diagrams-uml-sequence.md`.
- If UML class diagrams are selected, read `references/033-architecture-diagrams-uml-class.md`.
- If C4 model diagrams are selected, read `references/033-architecture-diagrams-c4.md`.
- If UML state-machine diagrams are selected, read `references/033-architecture-diagrams-state-machine.md`.
- If UML Deployment Diagrams are selected, read `references/033-architecture-diagrams-deployment.md`.
- If ER diagrams are selected, read `references/033-architecture-diagrams-er.md`.
- If bounded-context diagrams are selected, read `references/033-architecture-diagrams-bounded-context.md`.
- If All diagrams is selected, read all seven focused diagram-family references.
- If Skip is selected for a diagram family, do not read that diagram-family reference.
- Do not read unselected diagram-family references.


3. **Read selected references and generate PlantUML diagrams**

Create requested diagrams in PlantUML syntax using only the selected focused references, project inputs, and repository context.

4. **Validate and finalize outputs**


Check generated diagrams for syntax correctness and consistency with selected scope before final delivery.

When Docker is available, use the official `plantuml/plantuml` image to validate and render generated `.puml` files without requiring a local PlantUML, Java, or Graphviz installation.

Validate PlantUML syntax without generating images:

```bash
docker run --rm -v "$PWD:/data" plantuml/plantuml --check-syntax /data/diagrams
```

Render PNG images:

```bash
docker run --rm -v "$PWD:/data" plantuml/plantuml --png /data/diagrams
```

Render SVG images:

```bash
docker run --rm -v "$PWD:/data" plantuml/plantuml --svg /data/diagrams
```

Use the path mounted under `/data` to point at the directory or `.puml` file containing generated diagrams. This workflow uses the CLI-oriented PlantUML image, not the PlantUML server image.

## Reference

For detailed guidance, examples, and constraints, see:

- [references/033-architecture-diagrams-uml-sequence.md](references/033-architecture-diagrams-uml-sequence.md)
- [references/033-architecture-diagrams-uml-class.md](references/033-architecture-diagrams-uml-class.md)
- [references/033-architecture-diagrams-c4.md](references/033-architecture-diagrams-c4.md)
- [references/033-architecture-diagrams-state-machine.md](references/033-architecture-diagrams-state-machine.md)
- [references/033-architecture-diagrams-deployment.md](references/033-architecture-diagrams-deployment.md)
- [references/033-architecture-diagrams-er.md](references/033-architecture-diagrams-er.md)
- [references/033-architecture-diagrams-bounded-context.md](references/033-architecture-diagrams-bounded-context.md)
