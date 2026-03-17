---
name: lang__docfx_guide
description: Creates comprehensive documentation guides following BookStore conventions with proper structure, cross-references, and DocFX integration. Use when adding new technical documentation or updating existing guides.
---

Creates a new documentation guide in `docs/guides/` with proper structure, cross-references, and adherence to BookStore documentation standards.

1. **Gather Context**
   - Identify the topic and target audience (developers, operators, contributors)
   - Review related guides in `docs/guides/` to avoid duplication
   - Check existing documentation in source code (XML comments, README files)
   - Determine if the guide should include:
     - **Tutorial**: Step-by-step instructions for completing a task
     - **Reference**: Detailed technical specifications or API documentation
     - **Conceptual**: Architectural explanations and design decisions
     - **How-To**: Solutions to specific problems or scenarios

2. **Create Guide File**
   - Create file in `docs/guides/{topic-name}-guide.md` (use kebab-case)
   - Use template: `templates/guide-template.md`
   - Replace all placeholders:
     - `{Title}`: Descriptive title in Title Case
     - `{Brief}`: One-sentence description of the guide's purpose
     - `{Content}`: Main body organized with clear headings
   - Follow structure:
     ```markdown
     # {Title}

     {Brief introduction - 1-2 paragraphs explaining what, why, and when}

     ## Table of Contents (if guide > 100 lines)

     ## Prerequisites (if applicable)

     ## Core Concepts / Getting Started

     ## Detailed Sections

     ## Examples

     ## Troubleshooting (if applicable)

     ## Related Documentation
     ```

3. **Add Cross-References**
   - Link to related guides using relative paths: `[Event Sourcing Guide](event-sourcing-guide.md)`
   - Link to source files using project-relative paths: `[BookStore.ApiService](../../src/BookStore.ApiService/)`
   - Reference specific types/methods: `` `IDocumentSession` ``, `` `MartenRegistry` ``
   - Add links to external documentation for third-party libraries

4. **Include Code Examples**
   - Use fenced code blocks with language identifiers: `` ```csharp ``
   - Keep examples focused and minimal (5-20 lines)
   - Show complete, runnable examples when possible
   - Use real types from the BookStore project
   - Add comments to explain non-obvious logic
   - Follow BookStore coding standards:
     - Use `Guid.CreateVersion7()`, not `Guid.NewGuid()`
     - Use `DateTimeOffset.UtcNow`, not `DateTime.Now`
     - Use `record` types for DTOs/commands/events
     - File-scoped namespaces: `namespace BookStore.X;`

5. **Add Visual Aids**
   - For architecture/flow diagrams, add images to `docs/images/`
   - Use Mermaid diagrams for simple flows:
     ````markdown
     ```mermaid
     graph TD
         A[Start] --> B[Process]
         B --> C[End]
     ```
     ````
   - Add screenshots for UI-related documentation (save as PNG)
   - Keep images optimized (< 500KB)

6. **Update Navigation**
   - Add the new guide to `docs/toc.yml` under the appropriate section
   - Format:
     ```yaml
     - name: Guides
       items:
       - name: {Your Guide Title}
         href: guides/{topic-name}-guide.md
     ```
   - Place in logical order (alphabetical within categories or by workflow)

// turbo
7. **Verify Locally**
   - Run: `docfx docs/docfx.json --serve`
   - Open `http://localhost:8080` in browser
   - Check:
     - Guide appears in navigation
     - All links work correctly
     - Code examples render properly
     - Formatting is consistent

8. **Follow Documentation Standards**
   - **Headings**: Use sentence case for headings
   - **Code**: Inline code for types/methods, blocks for examples
   - **Admonitions**: Use DocFX alerts for important information:
     ```markdown
     > [!NOTE]
     > Additional context or tip

     > [!WARNING]
     > Important warning about potential issues

     > [!TIP]
     > Best practice or optimization suggestion
     ```
   - **Lists**: Use `-` for unordered, `1.` for ordered
   - **Tables**: Use markdown tables for structured data
   - **Line Length**: Wrap prose at 120 characters for readability

9. **Update Related Documentation**
   - If this guide supersedes old documentation, update or remove it
   - Add links from `docs/getting-started.md` if relevant for new users
   - Update `docs/architecture.md` if guide explains architectural decisions
   - Add link from `AGENTS.md` if the guide supports agent workflows

10. **Add to Agent Context (Optional)**
    - If the guide describes patterns agents should follow, reference it in:
      - `AGENTS.md` (root or domain-specific)
      - `.github/copilot-instructions.md`
    - For critical patterns, consider creating a related skill in `.claude/skills/`

## Related Skills

**Prerequisites**:
- Review existing guides in `docs/guides/` to understand conventions
- Ensure DocFX is installed: `dotnet tool update -g docfx`

**Next Steps**:
- `/meta__cheat_sheet` - Add quick reference if guide introduces new patterns
- `/meta__create_skill` - Create skill if guide describes a repeatable workflow

**Related**:
- `docs/guides/documentation-guide.md` - Overall documentation process
- `docs/guides/agent-guide.md` - How to write agent-friendly documentation

**See Also**:
- [DocFX Documentation](https://dotnet.github.io/docfx/)
- [Markdown Guide](https://www.markdownguide.org/)
- `docs/docfx.json` - Site configuration
- `.github/workflows/docs.yml` - Deployment workflow
