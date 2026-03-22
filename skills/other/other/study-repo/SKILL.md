---
name: study-repo
description: Deep analysis of an external repository's architecture, patterns, and design decisions. Generates comprehensive influence document and updates improvements.md with prioritized recommendations.
agent: general-purpose
allowed-tools: Read, Grep, Glob, Bash
disable-model-invocation: false
argument-hint: [repo-path] [--focus=aspect]
---

# Repository Study Skill

Deep analysis of external repositories to identify patterns, architecture decisions, and opportunities for adoption in ClaudeMemory.

## Prerequisites

Before running this skill, clone the repository you want to study:

```bash
# For public repos
git clone https://github.com/user/project /tmp/study-repos/project-name

# For private repos (requires gh CLI)
gh repo clone user/project /tmp/study-repos/project-name

# Use --depth 1 for speed (recommended)
git clone --depth 1 https://github.com/user/project /tmp/study-repos/project-name
```

Then invoke: `/study-repo /tmp/study-repos/project-name`

**Optional Focus Mode**: Narrow analysis to specific aspect
```bash
/study-repo /tmp/study-repos/project-name --focus="MCP implementation"
/study-repo /tmp/study-repos/project-name --focus="testing strategy"
```

See `.claude/skills/study-repo/focus-examples.md` for more examples.

## Analysis Phases

Follow these phases systematically to ensure comprehensive coverage:

### Phase 1: Repository Context (10 minutes)

**Goal**: Understand project purpose, maturity, and ecosystem

**Tasks**:
1. Read README.md, CHANGELOG.md, LICENSE
2. Examine gemspec/package.json for dependencies and metadata
3. Check GitHub metadata (stars, issues, PRs, contributors)
4. Review CI configuration (.github/workflows/, .gitlab-ci.yml)
5. Check documentation structure (docs/, wiki)

**Output**: Executive Summary section with:
- Project purpose (1-2 sentences)
- Key innovation (what makes it unique)
- Technology stack table
- Production readiness assessment

### Phase 2: Architecture Mapping (15 minutes)

**Goal**: Map high-level structure and module organization

**Tasks**:
1. Run `tree -L 3 -d` to understand directory structure
2. Identify entry points (bin/, exe/, main files)
3. Map core modules and their responsibilities
4. Identify data model (database schema, structs, classes)
5. Document dependencies between modules

**Output**: Architecture Overview section with:
- Data model description
- Design patterns identified
- Module organization diagram (text-based)
- Comparison table vs ClaudeMemory

### Phase 3: Pattern Recognition (20 minutes)

**Goal**: Identify key design patterns and conventions

**Tasks**:
1. Search for common patterns:
   - Dependency injection
   - Command pattern
   - Repository pattern
   - Factory pattern
   - Observer pattern
2. Review naming conventions
3. Check error handling approaches
4. Examine configuration management
5. Identify testing patterns

**Output**: Key Components Deep-Dive with:
- Component purpose
- Code examples with file:line references
- Design decision rationale

### Phase 4: Code Quality Assessment (15 minutes)

**Goal**: Evaluate testing, documentation, and performance

**Tasks**:
1. Analyze test coverage and structure
2. Review documentation quality
3. Check for performance optimizations
4. Examine logging and observability
5. Look for code quality tools (linters, formatters)

**Output**: Comparative Analysis section with:
- What they do well (with evidence)
- What we do well (our advantages)
- Trade-offs table

### Phase 5: Comparative Analysis (15 minutes)

**Goal**: Compare their approach with ClaudeMemory's

**Tasks**:
1. For each major component, compare:
   - Their implementation
   - Our implementation
   - Pros/cons of each approach
2. Identify areas where they excel
3. Identify areas where we excel
4. Document fundamental architectural differences

**Output**: Enhanced Comparative Analysis with:
- Side-by-side comparison
- Trade-off analysis
- Context for adoption decisions

### Phase 6: Adoption Opportunities (20 minutes)

**Goal**: Extract actionable recommendations with priorities

**Tasks**:
1. List all potential adoptions
2. For each, assess:
   - Value (quantified benefit)
   - Effort (implementation complexity)
   - Risk (compatibility, maintenance)
   - Fit (alignment with our architecture)
3. Prioritize as High ⭐ / Medium / Low
4. Identify features to avoid
5. Propose implementation phases

**Output**: Adoption Opportunities section with:
- High Priority ⭐ items (adopt soon)
- Medium Priority items (consider)
- Low Priority items (defer)
- Features to Avoid (with reasoning)
- Implementation Recommendations (phased plan)

## Output Format

Generate a comprehensive influence document following this structure (see `.claude/skills/study-repo/analysis-template.md` for full template):

```markdown
# [Project Name] Analysis

*Analysis Date: YYYY-MM-DD*
*Repository: GitHub URL*
*Version/Commit: tag or SHA*

---

## Executive Summary
[Project purpose, key innovation, tech stack, maturity]

## Architecture Overview
[Data model, design patterns, module organization, comparison table]

## Key Components Deep-Dive
[Component 1, Component 2, etc. with code examples and file:line references]

## Comparative Analysis
[What they do well, what we do well, trade-offs]

## Adoption Opportunities

### High Priority ⭐
#### 1. [Feature]
- **Value**: [Benefit]
- **Evidence**: [file:line proof]
- **Implementation**: [Approach]
- **Effort**: [Estimate]
- **Trade-off**: [Costs]
- **Recommendation**: ADOPT / CONSIDER / DEFER

[Medium and Low sections follow]

### Features to Avoid
[With reasoning]

## Implementation Recommendations
[Phase 1, Phase 2, etc.]

## Architecture Decisions
[What to preserve, adopt, reject]

## Key Takeaways
[Main learnings and next steps]
```

**Critical Requirements**:
- All claims must include file:line references
- Code examples for key patterns
- Priority markers (⭐) on High Priority items
- Comparison table vs ClaudeMemory
- Quantified benefits where possible
- Clear ADOPT/CONSIDER/DEFER recommendations

## Integration with improvements.md

After creating the influence document, update `docs/improvements.md`:

1. **Extract High Priority items** (⭐ marked) from influence doc
2. **Format as new section**:
   ```markdown
   ## [Project Name] Study (YYYY-MM-DD)

   Source: docs/influence/[project-name].md

   ### High Priority Recommendations

   - [ ] **[Feature 1]**: [Brief description]
     - Value: [Quantified benefit]
     - Evidence: [file:line from their repo]
     - Effort: [Estimate]

   - [ ] **[Feature 2]**: [...]
   ```
3. **Append to improvements.md** preserving existing structure
4. **Update "Last updated" timestamp** at top of file

## Success Criteria

The analysis is complete when all of these are verified:

- ✅ `docs/influence/<project_name>.md` created with all sections
- ✅ Executive Summary includes project metadata and tech stack
- ✅ Architecture Overview has comparison table vs ClaudeMemory
- ✅ Key Components include code examples with file:line references
- ✅ All major claims have evidence citations
- ✅ Adoption Opportunities use ⭐ for High Priority items
- ✅ Each opportunity has Value/Evidence/Implementation/Effort/Trade-off
- ✅ Clear ADOPT/CONSIDER/DEFER recommendations given
- ✅ Implementation Recommendations organized in phases
- ✅ Trade-offs section discusses costs and risks
- ✅ `docs/improvements.md` updated with new dated section
- ✅ High priority items extracted and formatted as tasks
- ✅ Existing improvements.md structure preserved
- ✅ Console summary shows key findings

## Focus Mode

When `--focus` flag is provided, narrow the analysis:

1. **Parse focus topic** from arguments
2. **Filter files** to only relevant ones:
   - For "testing": test/, spec/, .github/workflows/
   - For "MCP": mcp/, server/, tools/
   - For "database": schema, migrations, queries
   - For "CLI": bin/, exe/, commands/
3. **Narrow exploration** to focused aspect
4. **Target recommendations** to focused area
5. **Faster execution** with reduced scope

See `.claude/skills/study-repo/focus-examples.md` for detailed examples.

## Error Handling

Handle common error cases gracefully:

- **Invalid path**: Display clear error with example usage
- **Empty directory**: Warn about missing files
- **No README**: Note absence but continue analysis
- **Large repo**: Suggest using `--focus` flag
- **Permission issues**: Check file permissions and suggest fixes

## Execution Steps

1. **Parse arguments**: Extract repo path and optional focus
2. **Validate path**: Check directory exists and is readable
3. **Detect project name**: Extract from path or .git/config
4. **Run analysis phases**: Follow Phase 1-6 systematically
5. **Generate influence doc**: Use template with collected data
6. **Update improvements.md**: Extract and append High Priority items
7. **Display summary**: Show key findings and output locations
8. **Exit with success**: Return 0 if complete

## Integration with /improve

The recommendations added to `docs/improvements.md` can be implemented using `/improve`:

```bash
# Study external project
/study-repo /tmp/study-repos/some-project

# Review recommendations
cat docs/influence/some-project.md

# Implement selected improvements
/improve
```

This creates a complete workflow: `/study-repo` → recommendations → `/improve` → implementation
