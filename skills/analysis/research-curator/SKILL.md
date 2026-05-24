---
name: research-curator
description: 'Add new resources to the research directory with comprehensive documentation. Use when user provides a URL, repository, or tool to research and document for future reference. Triggers on phrases like "add to research", "document this tool", "research this", or when given URLs to novel agentic development resources.'
argument-hint: '[url-or-resource]'
context: fork
---

# Research Curator - Add Resources to Research Directory

Add novel tools, repositories, and resources to `./research/` for future reference in Claude Code development.

---

## Definition of Success

1. A comprehensive research entry exists at `./research/{category}/{resource-name}.md`
2. The entry follows the standard format (see existing entries for reference)
3. `./research/README.md` is updated with the new entry in the appropriate table
4. All information is verified from primary sources with access dates
5. Freshness tracking section is complete

---

## Research Directory Structure

```text
./research/
├── README.md                    # Index - UPDATE THIS
├── research-agent-patterns/     # Multi-agent architectures
├── skill-generation-tools/      # Tools that create AI skills
└── [other categories as needed]
```

---

## Category Selection

| Category             | Directory                  | Resource Type                                 |
| -------------------- | -------------------------- | --------------------------------------------- |
| Multi-agent patterns | `research-agent-patterns/` | Agent architectures, orchestration, workflows |
| Skill generation     | `skill-generation-tools/`  | Tools that create AI skills/prompts           |
| Prompt engineering   | `prompt-engineering/`      | Prompt optimization, testing                  |
| Context management   | `context-management/`      | Memory, RAG, context window tools             |
| MCP ecosystem        | `mcp-ecosystem/`           | MCP servers, integrations                     |
| Agent frameworks     | `agent-frameworks/`        | Agent SDKs, orchestration frameworks          |
| Evaluation/testing   | `evaluation-testing/`      | Agent testing, benchmarking                   |

Create the directory if it doesn't exist.

---

## Required Information to Gather

<information_requirements>

**Identity**:

- Official name and current version
- Primary URL, GitHub repository, package registry
- License type

**Substance**:

- Core purpose and value proposition
- Problem it solves
- Key features (detailed)
- Technical architecture or workflow
- Installation/usage patterns
- Statistics (stars, downloads, contributors)

**Relevance**:

- How it applies to Claude Code development
- Patterns worth adopting
- Integration opportunities

</information_requirements>

---

## Available Resources

The following tools are available for gathering information:

- **MCP Ref tools**: `mcp__Ref__ref_search_documentation`, `mcp__Ref__ref_read_url` for documentation
- **MCP Exa tools**: `mcp__exa__web_search_exa`, `mcp__exa__get_code_context_exa` for code/API research
- **GitHub CLI**: `gh repo view`, `gh api` for repository metadata, issues, releases
- **Read tool**: For examining files after cloning or for local resources
- **Grep/Glob**: For searching within fetched content

Check the `<functions>` list for current MCP tool availability.

---

## Entry Template

See existing entries for format reference:

- `./research/skill-generation-tools/skill-seekers.md`
- `./research/research-agent-patterns/github-patterns.md`

Required sections:

1. **Header**: Name, research date, URLs, version, license
2. **Overview**: 2-3 sentence description
3. **Problem Addressed**: Table of problems and solutions
4. **Key Statistics**: With date gathered
5. **Key Features**: Categorized feature list
6. **Technical Architecture**: How it works
7. **Installation & Usage**: Examples
8. **Relevance to Claude Code Development**: Applications, patterns, integrations
9. **References**: All sources with access dates
10. **Freshness Tracking**: Version, metrics, next review date (3 months)

---

## Completion Checklist

Before reporting done:

- [ ] Entry file created at `./research/{category}/{name}.md`
- [ ] All template sections filled (no placeholders remaining)
- [ ] Information verified from primary sources
- [ ] All references include access dates
- [ ] Statistics are current (gathered during this session)
- [ ] `./research/README.md` updated with new entry
- [ ] Next review date set (3 months from today)

---

## Output

Report completion with:

```text
## Research Entry Created

**Resource**: [Name]
**Category**: [category-name]
**File**: ./research/{category}/{filename}.md
**README Updated**: Yes/No

### Key Findings
- [Finding 1]
- [Finding 2]
- [Finding 3]

### Relevance to Claude Code
[Brief assessment]

### Next Review
YYYY-MM-DD
```
