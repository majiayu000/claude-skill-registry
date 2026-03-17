---
name: deepwiki-mcp
description: DeepWiki MCP server for AI-powered GitHub repository documentation and
  Q&A
metadata:
  trit: 0
  bundle: research
---

# DeepWiki MCP Skill

> AI-powered documentation and Q&A for any public GitHub repository

**Version**: 1.0.0
**Trit**: 0 (Ergodic - coordinates knowledge retrieval)
**Bundle**: research
**Provider**: Cognition (Devin AI) - Official, Free, No Auth Required

## Overview

DeepWiki MCP provides programmatic access to AI-generated documentation for any public GitHub repository indexed on [DeepWiki.com](https://deepwiki.com/). It enables:

1. **Wiki Structure**: Get table of contents for any repo's documentation
2. **Wiki Contents**: Read AI-generated documentation for specific topics
3. **Ask Questions**: Get AI-powered answers grounded in repository context

## Server Configuration

### Base URL

```
https://mcp.deepwiki.com/
```

### Wire Protocols

| Protocol | URL | Best For |
|----------|-----|----------|
| **SSE** | `https://mcp.deepwiki.com/sse` | Claude, most clients |
| **Streamable HTTP** | `https://mcp.deepwiki.com/mcp` | OpenAI, Cloudflare, Amp |

## Tools

### 1. `read_wiki_structure`

Get the documentation topic tree for a GitHub repository.

```json
{
  "tool": "read_wiki_structure",
  "params": {
    "repo_owner": "AlgebraicJulia",
    "repo_name": "ACSets.jl"
  }
}
```

Returns: List of documentation topics/sections

### 2. `read_wiki_contents`

Read documentation for a specific topic.

```json
{
  "tool": "read_wiki_contents",
  "params": {
    "repo_owner": "AlgebraicJulia",
    "repo_name": "ACSets.jl",
    "topic": "Overview"
  }
}
```

Returns: AI-generated documentation content

### 3. `ask_question`

Ask any question about a repository with AI-powered, context-grounded response.

```json
{
  "tool": "ask_question",
  "params": {
    "repo_owner": "AlgebraicJulia",
    "repo_name": "Catlab.jl",
    "question": "How do wiring diagrams compose?"
  }
}
```

Returns: AI-powered answer with repository context

## Client Configuration

### Amp / Codex (.mcp.json)

```json
{
  "mcpServers": {
    "deepwiki": {
      "serverUrl": "https://mcp.deepwiki.com/mcp"
    }
  }
}
```

### Claude Desktop

```json
{
  "mcpServers": {
    "deepwiki": {
      "serverUrl": "https://mcp.deepwiki.com/sse"
    }
  }
}
```

### Claude Code (CLI)

```bash
claude mcp add -s user -t http deepwiki https://mcp.deepwiki.com/mcp
```

### Cursor / Windsurf

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "deepwiki": {
      "serverUrl": "https://mcp.deepwiki.com/sse"
    }
  }
}
```

## GF(3) Triad Integration

| Trit | Skill | Role |
|------|-------|------|
| -1 | hatchery-papers | Validates academic sources |
| 0 | **deepwiki-mcp** | Coordinates repo knowledge |
| +1 | bmorphism-stars | Generates from starred repos |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

### Additional Triads

```
hatchery-papers (-1) ⊗ deepwiki-mcp (0) ⊗ bmorphism-stars (+1) = 0 ✓  [Research]
persistent-homology (-1) ⊗ deepwiki-mcp (0) ⊗ gay-mcp (+1) = 0 ✓  [Documentation]
sheaf-cohomology (-1) ⊗ deepwiki-mcp (0) ⊗ topos-generate (+1) = 0 ✓  [Knowledge]
three-match (-1) ⊗ deepwiki-mcp (0) ⊗ cider-clojure (+1) = 0 ✓  [Clojure Repos]
polyglot-spi (-1) ⊗ deepwiki-mcp (0) ⊗ gay-mcp (+1) = 0 ✓  [Cross-Lang Docs]
```

## Use Cases

### 1. Understand New Libraries

```
"Read the documentation structure for react/react and explain the hooks system"
```

### 2. Answer Technical Questions

```
"How does Catlab.jl implement natural transformations?"
```

### 3. Compare Implementations

```
"Compare how ACSets.jl and Catlab.jl handle graph homomorphisms"
```

### 4. Explore Category Theory Libraries

```
"What topics are covered in AlgebraicJulia/AlgebraicDynamics.jl documentation?"
```

## Indexing Your Repository

To make your public GitHub repo available via DeepWiki MCP:

1. Visit [DeepWiki.com](https://deepwiki.com/)
2. Enter your repository URL
3. Wait for indexing to complete
4. Add the DeepWiki badge to your README:

```markdown
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/owner/repo)
```

## Related Resources

- [DeepWiki.com](https://deepwiki.com/) - Web interface
- [Devin Docs](https://docs.devin.ai/work-with-devin/deepwiki-mcp) - Official documentation
- [MCP Specification](https://modelcontextprotocol.io/) - Protocol details

## ACSet Skill Integration

Both `deepwiki-mcp` and `acsets-algebraic-databases` are **ERGODIC (trit 0)** — they substitute for each other in triads and coordinate knowledge transport.

### Qualified Workflow

| Phase | deepwiki-mcp | acsets skill | Verification |
|-------|--------------|--------------|--------------|
| **Discovery** | `read_wiki_structure` | Schema patterns | ✓ Catlab.jl has 16 topic pages |
| **Q&A** | `ask_question` | Formal definitions | ✓ ACSet = Functor C → Set confirmed |
| **Apply** | Code examples | Specter navigation | ✓ `oapply` documented in Catlab |
| **Debug** | "Why does X fail?" | Check naturality | ✓ HomSearch uses BacktrackingSearch |

### Verified DeepWiki ↔ ACSets Correspondence

From DeepWiki `ask_question("AlgebraicJulia/Catlab.jl", "How do ACSets work...")`:

| DeepWiki Response | ACSets Skill | Match |
|-------------------|--------------|-------|
| "ACSet represents a functor from schema to Set" | `C-set = Functor X: C → Set` | ✓ |
| "ACSetFunctor wraps ACSet for functorial view" | ∫G category of elements | ✓ |
| "BacktrackingSearch (CSP-based, MRV heuristic)" | `homomorphisms(G, complete_graph(k))` | ✓ |
| "VMSearch (compiled virtual machine)" | Specter zero-overhead navigation | ✓ |

### Repository Indexing Status (Verified 2025-12-22)

| Repository | DeepWiki Status | Topics |
|------------|-----------------|--------|
| `AlgebraicJulia/Catlab.jl` | ✅ Indexed | 16 pages (GATs, CSets, HomSearch, WiringDiagrams...) |
| `AlgebraicJulia/ACSets.jl` | ❌ Needs indexing | Visit https://deepwiki.com/AlgebraicJulia/ACSets.jl |
| `AlgebraicJulia/AlgebraicDynamics.jl` | ❌ Needs indexing | Visit https://deepwiki.com/AlgebraicJulia/AlgebraicDynamics.jl |
| `AlgebraicJulia/StructuredDecompositions.jl` | ❌ Needs indexing | Visit https://deepwiki.com/AlgebraicJulia/StructuredDecompositions.jl |
| `redplanetlabs/agent-o-rama` | ✅ Indexed | 28 pages (Rama PStates, Agent Topologies, Tool Calling...) |
| `discopy/discopy` | ✅ Indexed | 23 pages (Monoidal Categories, Quantum Circuits, QNLP...) |

### Cross-Skill Examples

**Example 1: ACSets + Catlab.jl**
```julia
# 1. Query DeepWiki for oapply semantics
mcp__deepwiki__ask_question("AlgebraicJulia/Catlab.jl", 
  "How does oapply compose undirected wiring diagrams?")

# 2. Apply via ACSets skill patterns
@present SchUWD(FreeSchema) begin
  Box::Ob; Port::Ob; Junction::Ob; OuterPort::Ob
  box::Hom(Port, Box)
  junction::Hom(Port, Junction)
  outer_junction::Hom(OuterPort, Junction)
end

# 3. oapply = colimit of component diagram (verified by DeepWiki)
composite = oapply(wiring_diagram, components)
```

**Example 2: DisCoPy for Quantum/Categorical Diagrams**
```python
# Query DisCoPy documentation
mcp__deepwiki__ask_question("discopy/discopy",
  "How do monoidal categories compose with tensor products?")

# DisCoPy has 23 pages covering:
# - Monoidal, Rigid, Symmetric, Frobenius categories
# - Quantum circuits and gates
# - QNLP (Quantum Natural Language Processing)
# - Tensor network backends
```

**Example 3: Agent-o-rama for Rama Integration**
```clojure
;; Query agent-o-rama patterns
mcp__deepwiki__ask_question("redplanetlabs/agent-o-rama",
  "How do PStates store agent invocation state?")

;; 28 pages covering:
;; - Agent Modules and Topology
;; - PStates and Depots storage
;; - Tool Calling Integration
;; - Human-in-the-Loop Workflows
```

## See Also

- `hatchery-papers` - Academic paper research
- `bmorphism-stars` - GitHub stars index
- `librarian` - Codebase understanding agent
- `exa` - Web search MCP
- `acsets-algebraic-databases` - ACSet computational patterns (trit 0, substitutes in triads)

---

**Skill Name**: deepwiki-mcp
**Type**: Repository Documentation / Q&A
**Trit**: 0 (ERGODIC)
**GF(3)**: Coordinates knowledge flow
**Auth**: None required (free)
**Scope**: All public GitHub repos indexed on DeepWiki.com
**Qualified**: 2025-12-22 (verified against acsets skill)
