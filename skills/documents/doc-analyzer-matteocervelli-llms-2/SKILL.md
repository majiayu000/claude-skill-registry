---
name: doc-analyzer
description: Analyze and extract relevant patterns, best practices, and usage examples
  from fetched documentation for implementation guidance.
allowed-tools: Read, Grep
---

## Purpose

The doc-analyzer skill provides comprehensive capabilities for analyzing fetched library and framework documentation to extract actionable implementation guidance. This skill helps the Documentation Researcher agent identify relevant code patterns, best practices, common pitfalls, and integration strategies that enable high-quality feature implementations.

This skill emphasizes:
- **Pattern Recognition:** Identify reusable code patterns and architectural approaches
- **Best Practice Extraction:** Discover recommended practices from authoritative sources
- **Example Compilation:** Collect and categorize working code examples
- **Pitfall Identification:** Recognize common mistakes and antipatterns
- **Integration Guidance:** Extract patterns for combining libraries and frameworks

The doc-analyzer skill ensures that documentation research provides practical, actionable guidance rather than raw documentation dumps.

## When to Use

This skill auto-activates when the agent describes:
- "Analyze documentation for..."
- "Extract patterns from..."
- "Identify best practices..."
- "Find examples of..."
- "Discover common pitfalls..."
- "Extract API usage patterns..."
- "Analyze integration approaches..."
- "Identify security considerations..."

## Provided Capabilities

### 1. Code Pattern Extraction

**What it provides:**
- Initialization and setup patterns
- Common usage patterns
- Integration patterns between libraries
- Configuration patterns
- Testing patterns

**Pattern Categories:**

**Initialization Patterns:**
```python
def extract_initialization_patterns(docs: dict) -> list:
    """
    Extract initialization and setup patterns from documentation.
    """
    keywords = [
        "setup", "initialize", "config", "configuration",
        "getting started", "first steps", "__init__", "setup.py"
    ]

    patterns = []
    for section in docs["sections"]:
        if contains_keywords(section, keywords):
            patterns.append({
                "type": "initialization",
                "title": section["title"],
                "code": extract_code_blocks(section),
                "description": section["description"],
                "prerequisites": extract_prerequisites(section)
            })

    return patterns

# Example extracted pattern
{
    "type": "initialization",
    "title": "FastAPI Application Setup",
    "code": """
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API description",
    version="1.0.0"
)
    """,
    "description": "Basic FastAPI application initialization with metadata",
    "prerequisites": ["fastapi installed", "Python 3.7+"]
}
```

**Usage Patterns:**
```python
def extract_usage_patterns(docs: dict) -> list:
    """
    Extract common usage patterns from documentation.
    """
    keywords = [
        "example", "usage", "how to", "tutorial",
        "guide", "quickstart", "getting started"
    ]

    patterns = []
    for section in docs["sections"]:
        if contains_keywords(section, keywords):
            patterns.append({
                "type": "usage",
                "title": section["title"],
                "code": extract_code_blocks(section),
                "use_case": identify_use_case(section),
                "complexity": assess_complexity(section)
            })

    return patterns
```

**Integration Patterns:**
```python
def extract_integration_patterns(docs: dict) -> list:
    """
    Extract patterns for integrating with other libraries.
    """
    keywords = [
        "integrate", "combination", "together", "with",
        "plugin", "middleware", "extension"
    ]

    patterns = []
    for section in docs["sections"]:
        if contains_keywords(section, keywords):
            patterns.append({
                "type": "integration",
                "libraries": identify_libraries(section),
                "pattern": section["title"],
                "code": extract_code_blocks(section),
                "compatibility": extract_compatibility(section)
            })

    return patterns
```

### 2. Best Practice Identification

**What it provides:**
- Recommended practices from official documentation
- Performance optimization techniques
- Security best practices
- Code organization recommendations
- Testing strategies

**Best Practice Categories:**

**Recommended Practices:**
```python
def extract_best_practices(docs: dict, category: str = "recommended") -> list:
    """
    Extract best practices from documentation.
    """
    # Keywords for different categories
    keywords = {
        "recommended": ["best practice", "recommended", "should", "prefer", "tip"],
        "avoid": ["avoid", "don't", "antipattern", "pitfall", "common mistake"],
        "performance": ["performance", "optimize", "efficient", "fast", "slow", "bottleneck"],
        "security": ["security", "secure", "vulnerability", "safety", "protect", "authentication"]
    }

    practices = []
    for section in docs["sections"]:
        if contains_keywords(section, keywords[category]):
            practices.append({
                "category": category,
                "practice": extract_practice_statement(section),
                "rationale": extract_rationale(section),
                "example": extract_code_example(section),
                "source": section["source_url"]
            })

    return practices

# Example extracted best practice
{
    "category": "recommended",
    "practice": "Use dependency injection for database connections",
    "rationale": "Enables testability and reduces coupling",
    "example": """
from fastapi import Depends

async def get_db():
    db = Database()
    try:
        yield db
    finally:
        await db.close()

@app.get("/items/")
async def read_items(db = Depends(get_db)):
    return db.query("SELECT * FROM items")
    """,
    "source": "https://fastapi.tiangolo.com/tutorial/dependencies/"
}
```

**Performance Best Practices:**
```python
def extract_performance_practices(docs: dict) -> list:
    """
    Extract performance optimization practices.
    """
    keywords = ["performance", "optimize", "cache", "async", "efficient", "scalability"]

    practices = []
    for section in docs["sections"]:
        if contains_keywords(section, keywords):
            practices.append({
                "category": "performance",
                "optimization": section["title"],
                "technique": extract_technique(section),
                "impact": assess_performance_impact(section),
                "implementation": extract_code_blocks(section)
            })

    return practices
```

**Security Best Practices:**
```python
def extract_security_practices(docs: dict) -> list:
    """
    Extract security best practices.
    """
    keywords = ["security", "secure", "authentication", "authorization", "vulnerability", "OWASP"]

    practices = []
    for section in docs["sections"]:
        if contains_keywords(section, keywords):
            practices.append({
                "category": "security",
                "security_concern": identify_concern(section),
                "mitigation": extract_mitigation(section),
                "implementation": extract_code_blocks(section),
                "owasp_category": map_to_owasp(section) if applicable else None
            })

    return practices
```

### 3. API Usage Example Compilation

**What it provides:**
- Categorized code examples
- Working, runnable code
- Example annotations and explanations
- Complexity ratings
- Use case mapping

**Example Extraction:**
```python
def extract_api_examples(docs: dict) -> list:
    """
    Extract and categorize API usage examples.
    """
    examples = []

    for section in docs["sections"]:
        code_blocks = extract_code_blocks(section)

        for code_block in code_blocks:
            examples.append({
                "api_element": identify_api_element(code_block),
                "use_case": infer_use_case(section["title"], code_block),
                "code": code_block["code"],
                "language": code_block["language"],
                "complexity": assess_complexity(code_block),
                "runnable": validate_runnability(code_block),
                "dependencies": extract_dependencies(code_block),
                "explanation": section["description"]
            })

    return examples

# Example output
{
    "api_element": "FastAPI.get decorator",
    "use_case": "Simple GET endpoint with path parameter",
    "code": """
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
    """,
    "language": "python",
    "complexity": "simple",
    "runnable": True,
    "dependencies": ["fastapi"],
    "explanation": "Defines a GET endpoint with a path parameter and optional query parameter"
}
```

**Example Categorization:**
```python
def categorize_examples(examples: list) -> dict:
    """
    Categorize examples by complexity and use case.
    """
    categorized = {
        "basic": [],      # Simple, introductory examples
        "intermediate": [],  # Common patterns
        "advanced": [],   # Complex integrations
        "by_feature": {}  # Organized by feature
    }

    for example in examples:
        # By complexity
        categorized[example["complexity"]].append(example)

        # By feature
        feature = example["api_element"]
        if feature not in categorized["by_feature"]:
            categorized["by_feature"][feature] = []
        categorized["by_feature"][feature].append(example)

    return categorized
```

### 4. Common Pitfall Identification

**What it provides:**
- Common mistakes and antipatterns
- Error-prone patterns
- Deprecated features
- Version-specific gotchas
- Migration pitfalls

**Pitfall Detection:**
```python
def identify_pitfalls(docs: dict) -> list:
    """
    Identify common pitfalls from documentation.
    """
    keywords = [
        "avoid", "don't", "pitfall", "common mistake", "gotcha",
        "warning", "caution", "deprecated", "not recommended"
    ]

    pitfalls = []
    for section in docs["sections"]:
        if contains_keywords(section, keywords):
            pitfalls.append({
                "pitfall": extract_pitfall_description(section),
                "why_problematic": extract_reasoning(section),
                "incorrect_example": extract_incorrect_example(section),
                "correct_alternative": extract_correct_example(section),
                "severity": assess_severity(section)
            })

    return pitfalls

# Example identified pitfall
{
    "pitfall": "Blocking I/O in async functions",
    "why_problematic": "Blocks the event loop, preventing concurrent request handling",
    "incorrect_example": """
@app.get("/items/")
async def read_items():
    # ❌ Blocking database call in async function
    items = blocking_db_query("SELECT * FROM items")
    return items
    """,
    "correct_alternative": """
@app.get("/items/")
async def read_items():
    # ✅ Non-blocking async database call
    items = await async_db_query("SELECT * FROM items")
    return items
    """,
    "severity": "high"
}
```

### 5. Integration Strategy Extraction

**What it provides:**
- Multi-library integration patterns
- Middleware and plugin patterns
- Configuration strategies
- Dependency management

**Integration Analysis:**
```python
def extract_integration_strategies(docs: dict, libraries: list) -> dict:
    """
    Extract strategies for integrating multiple libraries.
    """
    strategies = {}

    for lib in libraries:
        # Find integration mentions
        integration_sections = find_integration_sections(docs, lib)

        strategies[lib] = {
            "compatibility": extract_compatibility_info(integration_sections),
            "integration_pattern": extract_integration_pattern(integration_sections),
            "configuration": extract_configuration(integration_sections),
            "examples": extract_integration_examples(integration_sections),
            "known_issues": extract_known_issues(integration_sections)
        }

    return strategies

# Example integration strategy
{
    "library": "sqlalchemy",
    "compatibility": "Compatible with FastAPI via async support",
    "integration_pattern": "Dependency injection for database sessions",
    "configuration": {
        "database_url": "Configuration via environment variables",
        "engine_options": "async_engine with asyncpg driver"
    },
    "examples": [...],
    "known_issues": ["Connection pool management in async context"]
}
```

### 6. Version Compatibility Analysis

**What it provides:**
- Breaking changes between versions
- Deprecated features
- Migration requirements
- Version-specific considerations

**Compatibility Detection:**
```python
def analyze_version_compatibility(docs: dict, current_version: str, target_version: str) -> dict:
    """
    Analyze compatibility between versions.
    """
    changelog = extract_changelog(docs)

    return {
        "current_version": current_version,
        "target_version": target_version,
        "breaking_changes": extract_breaking_changes(changelog, current_version, target_version),
        "deprecations": extract_deprecations(changelog, current_version, target_version),
        "new_features": extract_new_features(changelog, target_version),
        "migration_required": requires_migration(changelog, current_version, target_version),
        "migration_guide": extract_migration_guide(docs, current_version, target_version),
        "compatibility_notes": extract_compatibility_notes(docs)
    }
```

## Usage Guide

### Step 1: Receive Fetched Documentation
```
doc-fetcher completes → Fetched documentation → doc-analyzer input
```

### Step 2: Extract Code Patterns
```
Documentation → Pattern recognition → Categorized patterns
```

### Step 3: Identify Best Practices
```
Documentation → Best practice detection → Recommended/avoid lists
```

### Step 4: Compile Examples
```
Code blocks → Extraction → Categorization → Example library
```

### Step 5: Identify Pitfalls
```
Documentation → Pitfall detection → Antipattern catalog
```

### Step 6: Analyze Integration
```
Multiple libraries → Integration patterns → Compatibility matrix
```

### Step 7: Generate Analysis Summary
```
All analyses → Synthesis → Structured output
```

## Best Practices

1. **Focus on Relevance**
   - Extract only patterns relevant to feature requirements
   - Prioritize commonly used patterns over edge cases
   - Filter examples by complexity appropriate to feature

2. **Validate Code Examples**
   - Verify examples are runnable
   - Check for required dependencies
   - Test examples if possible
   - Document prerequisites

3. **Prioritize Official Sources**
   - Official documentation takes precedence
   - Cross-reference multiple sources
   - Note source URL for all extracted content
   - Verify currency of information

4. **Categorize Systematically**
   - Use consistent categorization scheme
   - Tag with complexity level
   - Associate with use cases
   - Link related patterns

5. **Document Context**
   - Include version information
   - Note applicable scenarios
   - Document limitations
   - Provide rationale for recommendations

6. **Security-First Analysis**
   - Identify security considerations in all patterns
   - Extract security best practices explicitly
   - Flag potential vulnerabilities
   - Cross-reference with OWASP Top 10

## Resources

### pattern-extraction-guide.md
Comprehensive guide for pattern extraction:
- Pattern recognition techniques
- Code block parsing methods
- Pattern categorization schemes
- Example validation approaches
- Integration pattern identification
- Testing pattern extraction

### best-practices-catalog.md
Catalog of best practices by framework:
- Common best practices across frameworks
- Framework-specific recommendations
- Security patterns and practices
- Performance optimization techniques
- Testing best practices
- Error handling patterns

## Example Usage

### Input (from Documentation Researcher agent):
```
"Analyze FastAPI documentation to extract API routing patterns, dependency injection examples, and Pydantic integration best practices."
```

### Output (doc-analyzer skill provides):
```python
# Comprehensive documentation analysis

analysis = {
    "library": "fastapi",
    "version": "0.100.0",

    "patterns": {
        "api_routing": [
            {
                "pattern": "Path parameter with type hint",
                "code": "@app.get('/items/{item_id}')\nasync def read_item(item_id: int): ...",
                "use_case": "REST API with typed path parameters",
                "complexity": "simple"
            },
            {
                "pattern": "Query parameters with defaults",
                "code": "@app.get('/items/')\nasync def read_items(skip: int = 0, limit: int = 10): ...",
                "use_case": "Pagination with query parameters",
                "complexity": "simple"
            }
        ],
        "dependency_injection": [
            {
                "pattern": "Database session dependency",
                "code": "def get_db():\n    db = Database()\n    try:\n        yield db\n    finally:\n        db.close()",
                "use_case": "Resource management with cleanup",
                "complexity": "intermediate"
            }
        ]
    },

    "best_practices": {
        "recommended": [
            {
                "practice": "Use async def for I/O-bound operations",
                "rationale": "Enables concurrent request handling",
                "example": "@app.get('/items/')\nasync def read_items(): ..."
            },
            {
                "practice": "Use Pydantic models for request/response validation",
                "rationale": "Automatic validation and documentation generation",
                "example": "class Item(BaseModel):\n    name: str\n    price: float"
            }
        ],
        "avoid": [
            {
                "antipattern": "Blocking I/O in async functions",
                "why_problematic": "Blocks event loop, kills performance",
                "alternative": "Use async database drivers and await calls"
            }
        ]
    },

    "examples": {
        "basic": [...],
        "intermediate": [...],
        "advanced": [...]
    },

    "integration": {
        "pydantic": {
            "compatibility": "Native integration, Pydantic v2 supported",
            "pattern": "Use BaseModel for all request/response schemas",
            "examples": [...]
        }
    },

    "version_notes": "FastAPI 0.100.0 requires Pydantic v2.x"
}
```

## Integration

### Used By:
- **@documentation-researcher** (Primary) - Phase 2 sub-agent for documentation research

### Integrates With:
- **doc-fetcher** skill - Analyzes documentation fetched by doc-fetcher
- **prp-generator** skill (Design Orchestrator) - Analysis feeds into PRP generation

### Workflow Position:
1. doc-fetcher skill fetches documentation (Step 3-4)
2. **doc-analyzer skill** analyzes documentation (Step 5-6)
3. Documentation summary compiled (Step 7)
4. Design Orchestrator synthesizes into PRP

---

**Version:** 2.0.0
**Auto-Activation:** Yes
**Phase:** 2 - Design & Planning
**Created:** 2025-10-29