---
name: doc-fetcher
description: Fetch library and framework documentation via context7-mcp and fetch-mcp
  for comprehensive documentation research with version-specific content.
allowed-tools: Read
---

## Purpose

The doc-fetcher skill provides comprehensive capabilities for fetching library and framework documentation from multiple sources using MCP integrations. This skill helps the Documentation Researcher agent retrieve up-to-date, version-specific documentation that enables informed implementation decisions and adherence to library best practices.

This skill emphasizes:
- **Latest Documentation:** Always fetch current, version-specific documentation
- **Multiple Sources:** Leverage both context7-mcp (deep context) and fetch-mcp (web content)
- **Comprehensive Coverage:** Retrieve API references, examples, guides, and best practices
- **Version Awareness:** Track version compatibility and breaking changes
- **Efficient Retrieval:** Optimize MCP usage for token efficiency and accuracy

The doc-fetcher skill ensures that implementation guidance is based on authoritative, current documentation from official sources.

## When to Use

This skill auto-activates when the agent describes:
- "Fetch documentation for..."
- "Retrieve API reference for..."
- "Get library documentation..."
- "Access documentation for..."
- "Find documentation about..."
- "Retrieve latest docs for..."
- "Look up documentation..."
- "Fetch API docs from..."

## Provided Capabilities

### 1. Context7-MCP Documentation Retrieval

**What it provides:**
- Deep documentation retrieval with semantic search
- Version-specific API references
- Code examples from documentation
- Library-specific patterns and conventions
- Integration guidance

**Context7 Workflow:**
```python
# Step 1: Resolve library name to context7 ID
library_id = invoke_mcp(
    "context7-mcp",
    tool="resolve-library-id",
    params={
        "libraryName": "fastapi"  # or "react", "django", etc.
    }
)

# Step 2: Fetch comprehensive documentation
docs = invoke_mcp(
    "context7-mcp",
    tool="get-library-docs",
    params={
        "context7CompatibleLibraryID": library_id["library_id"],  # e.g., "/tiangolo/fastapi"
        "topic": "API routing and dependency injection",  # Focus area
        "tokens": 3000  # Amount of documentation to retrieve
    }
)

# Result contains:
# - documentation: Markdown-formatted docs
# - version: Library version
# - examples: Code examples
# - metadata: Additional context
```

**Context7 Best Practices:**
- Use specific topics to focus documentation retrieval
- Start with 2000-3000 tokens for comprehensive coverage
- Adjust token count based on complexity
- Combine multiple focused queries for complex features

### 2. Fetch-MCP Web Content Retrieval

**What it provides:**
- Official documentation page fetching
- GitHub README and Wiki retrieval
- Community resource access
- Tutorial and guide retrieval
- Changelog and migration guide access

**Fetch-MCP Workflow:**
```python
# Fetch official documentation page
official_docs = invoke_mcp(
    "fetch-mcp",
    tool="fetch",
    params={
        "url": "https://fastapi.tiangolo.com/tutorial/first-steps/",
        "prompt": "Extract quick start guide, installation steps, and first API example"
    }
)

# Fetch GitHub README
github_readme = invoke_mcp(
    "fetch-mcp",
    tool="fetch",
    params={
        "url": "https://github.com/tiangolo/fastapi/blob/master/README.md",
        "prompt": "Extract key features, installation, and basic usage examples"
    }
)

# Result contains:
# - Extracted content focused on the prompt
# - Markdown-formatted for easy parsing
# - Cleaned and processed for relevance
```

**Fetch-MCP Best Practices:**
- Use specific prompts to extract relevant content
- Prefer official documentation URLs over third-party
- Fetch READMEs for overview and quick start
- Retrieve changelogs for version migration info

### 3. Multi-Source Documentation Strategy

**What it provides:**
- Combined documentation from multiple sources
- Cross-reference validation
- Comprehensive coverage
- Authoritative source prioritization

**Multi-Source Workflow:**
```python
documentation_sources = {
    "primary": {
        # Context7: Deep, comprehensive docs
        "context7": fetch_via_context7(library_name, topic),

        # Official docs: Quick start and guides
        "official": fetch_via_fetch_mcp(official_docs_url),
    },
    "supplementary": {
        # GitHub: Latest examples and README
        "github": fetch_via_fetch_mcp(github_url),

        # Migration guides (if version upgrade)
        "migration": fetch_via_fetch_mcp(migration_guide_url) if needs_migration else None,
    }
}

# Synthesize documentation from multiple sources
synthesized_docs = synthesize_documentation(documentation_sources)
```

**Source Prioritization:**
1. **Official Documentation** (highest priority)
2. **Context7 Documentation** (comprehensive reference)
3. **GitHub Repository** (latest examples)
4. **Community Resources** (supplementary)

### 4. Version-Specific Retrieval

**What it provides:**
- Version compatibility checking
- Breaking change identification
- Migration guidance
- Deprecated feature detection

**Version Handling:**
```python
# Specify version in context7 (if supported)
docs_v2 = invoke_mcp(
    "context7-mcp",
    tool="get-library-docs",
    params={
        "context7CompatibleLibraryID": "/tiangolo/fastapi/v0.100.0",  # Version-specific
        "topic": "API routing",
        "tokens": 2000
    }
)

# Fetch version-specific changelog
changelog = invoke_mcp(
    "fetch-mcp",
    tool="fetch",
    params={
        "url": "https://github.com/tiangolo/fastapi/blob/master/CHANGELOG.md",
        "prompt": "Extract changes between version 0.95.0 and 0.100.0, focusing on breaking changes"
    }
)

# Compare versions and identify migration needs
migration_notes = analyze_version_changes(changelog)
```

### 5. Code Example Extraction

**What it provides:**
- Working code examples
- Integration patterns
- Configuration examples
- Test examples

**Example Extraction:**
```python
# Extract examples from context7 docs
examples = []
for code_block in docs["examples"]:
    examples.append({
        "code": code_block["code"],
        "language": code_block["language"],
        "description": code_block["description"],
        "category": categorize_example(code_block)
    })

# Extract examples from official docs
official_examples = extract_code_blocks(official_docs["content"], language="python")

# Combine and deduplicate
all_examples = deduplicate_examples(examples + official_examples)
```

### 6. Documentation Caching

**What it provides:**
- Reduced MCP calls
- Faster subsequent retrievals
- Token usage optimization
- Consistent documentation state

**Caching Strategy:**
```python
# Check cache before fetching
cache_key = f"{library_name}:{version}:{topic_hash}"

if cache_key in documentation_cache:
    return documentation_cache[cache_key]

# Fetch and cache
docs = fetch_documentation(library_name, version, topic)
documentation_cache[cache_key] = docs
documentation_cache[cache_key]["cached_at"] = datetime.utcnow()

return docs
```

**Cache Invalidation:**
- Expire after 24 hours
- Clear on version change
- Manual refresh option

## Usage Guide

### Step 1: Identify Documentation Needs
```
Analysis doc → Extract libraries → Identify topics → Prioritize sources
```

### Step 2: Resolve Library IDs (context7)
```
Library name → context7 resolve-library-id → Library ID
```

### Step 3: Fetch Context7 Documentation
```
Library ID + Topic → get-library-docs → Comprehensive docs
```

### Step 4: Fetch Web Resources (fetch-mcp)
```
URLs + Prompts → fetch → Supplementary docs
```

### Step 5: Extract Examples
```
Documentation → Code blocks → Categorized examples
```

### Step 6: Synthesize Documentation
```
Multiple sources → Prioritize → Combine → Structured output
```

## Best Practices

1. **Use Context7 for Depth**
   - Primary source for API references
   - Comprehensive coverage of library features
   - Semantic search capabilities
   - Version-specific support

2. **Use Fetch-MCP for Breadth**
   - Official quick start guides
   - GitHub examples and READMEs
   - Migration guides and changelogs
   - Community tutorials (verified sources)

3. **Focus Documentation Retrieval**
   - Use specific topics in context7
   - Use targeted prompts in fetch-mcp
   - Avoid generic "get all documentation"
   - Retrieve only what's needed for feature

4. **Version Awareness**
   - Always specify version requirements
   - Check for breaking changes
   - Document version compatibility
   - Provide migration notes if needed

5. **Token Optimization**
   - Start with 2000-3000 tokens
   - Adjust based on complexity
   - Multiple focused queries > one large query
   - Cache frequently accessed docs

6. **Source Validation**
   - Prefer official documentation
   - Verify URL authenticity
   - Check documentation date
   - Cross-reference when uncertain

## Resources

### doc-sources.md
Curated list of documentation sources:
- Official documentation URLs by framework
- GitHub repository locations
- Community resource repositories
- API reference locations
- Tutorial and guide sources
- Changelog and release note locations

### fetching-strategies.md
Documentation fetching strategies:
- When to use context7 vs fetch-mcp
- Token optimization techniques
- Version-specific retrieval
- Caching strategies
- Error handling patterns
- Multi-source synthesis
- Example extraction methods

## Example Usage

### Input (from Documentation Researcher agent):
```
"Fetch documentation for FastAPI framework focusing on API routing, dependency injection, and Pydantic integration."
```

### Output (doc-fetcher skill provides):
```python
# Comprehensive documentation retrieval

# 1. Context7 Documentation
fastapi_docs = {
    "library_id": "/tiangolo/fastapi",
    "version": "0.100.0",
    "documentation": """
    # FastAPI API Routing

    FastAPI provides a powerful routing system based on Python type hints...

    ## Dependency Injection

    FastAPI's dependency injection system allows you to declare dependencies...

    ## Pydantic Integration

    FastAPI uses Pydantic models for request validation...
    """,
    "examples": [
        {
            "title": "Basic API with dependency injection",
            "code": """
from fastapi import FastAPI, Depends

app = FastAPI()

def get_query_param(q: str = None):
    return {"q": q}

@app.get("/items/")
async def read_items(commons: dict = Depends(get_query_param)):
    return commons
            """,
            "language": "python"
        }
    ]
}

# 2. Official Documentation (fetch-mcp)
official_docs = {
    "url": "https://fastapi.tiangolo.com/tutorial/",
    "content": """
    # First Steps

    Create a file `main.py` with:

    ```python
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "Hello World"}
    ```

    Run the server with: `uvicorn main:app --reload`
    """
}

# 3. GitHub README (fetch-mcp)
github_readme = {
    "url": "https://github.com/tiangolo/fastapi",
    "content": """
    # FastAPI

    FastAPI framework, high performance, easy to learn, fast to code, ready for production

    ## Key features:
    - Fast: Very high performance, on par with NodeJS and Go
    - Fast to code: Increase the speed to develop features by about 200% to 300%
    - Fewer bugs: Reduce about 40% of human errors
    - Intuitive: Great editor support
    - Easy: Designed to be easy to use and learn
    - Short: Minimize code duplication
    - Robust: Get production-ready code
    - Standards-based: Based on OpenAPI and JSON Schema
    """
}

# 4. Synthesized Output
{
    "library": "fastapi",
    "version": "0.100.0",
    "sources": {
        "context7": "Primary documentation source",
        "official": "Quick start and tutorials",
        "github": "Overview and features"
    },
    "api_routing": {
        "overview": "FastAPI provides decorator-based routing...",
        "examples": [...],
        "best_practices": [...]
    },
    "dependency_injection": {
        "overview": "Dependency injection via Depends()...",
        "examples": [...],
        "best_practices": [...]
    },
    "pydantic_integration": {
        "overview": "Pydantic models for validation...",
        "examples": [...],
        "best_practices": [...]
    },
    "version_notes": "Compatible with Pydantic v2.x"
}
```

## Integration

### Used By:
- **@documentation-researcher** (Primary) - Phase 2 sub-agent for documentation research

### Integrates With:
- **doc-analyzer** skill - Fetched documentation is analyzed for patterns and best practices
- **context7-mcp** - Primary documentation retrieval mechanism
- **fetch-mcp** - Supplementary web content retrieval

### Workflow Position:
1. Analysis Specialist identifies technical stack requirements
2. Documentation Researcher receives analysis
3. **doc-fetcher skill** retrieves documentation (Step 3-4)
4. doc-analyzer skill analyzes documentation (Step 5-6)
5. Results synthesized into documentation summary
6. Design Orchestrator includes in PRP

---

**Version:** 2.0.0
**Auto-Activation:** Yes
**Phase:** 2 - Design & Planning
**Created:** 2025-10-29