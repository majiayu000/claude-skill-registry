---
name: docs-out
description: Activates the Technical Writer to generate, update, or refactor internal project documentation. Use when creating READMEs, ADRs, or technical guides.
argument-hint: "[file, directory, or topic to document]"
---

# Generate Documentation

Create or update internal technical documentation.

1. **Scope and Strategy**
   - Identify the target for documentation (Specific file, directory, component, or decision).
   - Determine the appropriate artifact type:
     - **README.md**: For directories, components, or project root.
     - **ADR**: For architectural decisions (Architecture Decision Record).
     - **Guide**: For "How-to" or conceptual explanations.
   - Confirm the placement of the documentation (e.g., co-located with code or in a `docs/` folder).

2. **Analysis and Context**
   - Read the relevant source code to ensure technical accuracy.
   - Identify key concepts, architectural patterns, and "gotchas".
   - Review existing related documentation to ensure consistency and avoid duplication.

3. **Draft Documentation**
   - Generate the documentation content using the **Technical Writer** persona.
   - **Focus**:
     - Explain the *Why* and *Structure*, not just the *How*.
     - Use active voice and clear, concise English.
     - Include accurate code snippets with language tags.
     - Use diagrams (Mermaid) if complex relationships exist.

4. **Verification**
   - Validation:
     - Are all commands copy-pasteable and working?
     - Do relative links point to valid files?
     - Is the tone consistent with internal developer documentation?
