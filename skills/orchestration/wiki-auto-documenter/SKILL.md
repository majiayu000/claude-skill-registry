---
name: wiki-auto-documenter
description: Multi-agent orchestration system for automatically generating comprehensive Azure DevOps wiki documentation from Python codebase. Creates hierarchical wiki pages matching repository structure with bidirectional linkages between documentation and source files. Use when needing to document entire directories or maintain wiki docs synchronized with code.
---

# Wiki Auto-Documenter

Automated Azure DevOps wiki documentation generation using multi-agent orchestration. This skill coordinates specialized agents to analyze Python code, generate comprehensive documentation, and publish to Azure DevOps wiki with proper hierarchy and cross-references.

## When to Use This Skill

Use this skill when:
- Generating comprehensive wiki documentation for Python files in `python_files/`
- Creating or updating Azure DevOps wiki pages to match repository structure
- Documenting entire directories recursively (gold/, silver/, utilities/, etc.)
- Establishing bidirectional links between wiki docs and source code
- Maintaining documentation that mirrors codebase hierarchy
- Onboarding new team members with comprehensive code documentation
- Synchronizing outdated wiki pages with current codebase state

## Core Concept

This skill implements a three-tier multi-agent orchestration pattern:

1. **Orchestrator Agent** - Analyzes directory structure, decomposes work, coordinates execution
2. **Code-Documenter Agents (2-8)** - Parallel code analysis and markdown generation
3. **Wiki-Publisher Agent** - Creates Azure DevOps wiki pages with hierarchy and linkages

**Context Efficiency**:
- Parallel processing reduces total execution time by 5-7x
- Each agent operates independently on assigned file subset
- JSON-based communication protocol for structured data flow
- Estimated time: 209 files in <30 minutes (~7 files/minute)

## Prerequisites

### Environment Variables
```bash
export AZURE_DEVOPS_PAT="your-personal-access-token"
export AZURE_DEVOPS_ORGANIZATION="emstas"
export AZURE_DEVOPS_PROJECT="Program Unify"
```

### Required Permissions
- Azure DevOps PAT with `vso.wiki_write` scope
- Read access to target repository
- Wiki edit permissions on target wiki

### Repository Configuration
- **Organization**: emstas
- **Project**: Program Unify
- **Repository**: unify_2_1_dm_synapse_env_d10
- **Wiki Base URL**: https://dev.azure.com/emstas/Program%20Unify/_wiki/wikis/Program-Unify.wiki/274/unify_2_1_dm_synapse_env_d10

## Markdown Formatting Standards

All generated documentation MUST follow these markdown formatting conventions for consistency and clarity:

### Headers
- Use `#` for headers following proper hierarchy (H1 → H2 → H3 → H4)
- Add blank line before and after headers
- Use title case for H1 and H2, sentence case for H3+

### Emphasis
- Use `**bold**` for field labels (e.g., **Purpose**, **Parameters**, **Returns**)
- Use `*italic*` for emphasis within text
- Use backticks for inline code: `variable_name`, `function()`, `ClassName`

### Lists
- Use `-` (hyphen) for unordered lists
- Use `1.` for ordered lists with proper numbering
- Add blank line before and after list blocks
- Indent sub-items with 2 spaces

### Code Blocks
- Use triple backticks with language identifier: \`\`\`python
- Include code examples with proper indentation (4 spaces)
- Add blank line before and after code blocks

### Links
- Use `[text](url)` format for inline links
- Use relative paths for wiki cross-references: `[file](./file_name)`
- Use descriptive link text (not "click here")

### Tables
- Use pipes `|` with proper alignment
- Include header separator row: `| --- | --- |`
- Add blank line before and after tables
- Align content for readability in source

### Line Breaks
- Use single blank line between sections
- Use `---` (horizontal rule) only for major section separators
- Never use double blank lines

### Formatting Consistency
- Maintain consistent bullet styles throughout document
- Use consistent indentation (2 spaces for nested items)
- Keep lines under 120 characters where possible for readability
- Use consistent terminology (e.g., "parameter" not "param" in prose)

### Special Formatting for Technical Documentation

**Field Labels** (use bold):
- **Purpose**:
- **Description**:
- **Parameters**:
- **Returns**:
- **Decorators**:
- **Layer**:
- **File Path**:

**Code Elements** (use backticks):
- Function names: `function_name()`
- Class names: `ClassName`
- Variables: `variable_name`
- Modules: `module.submodule`
- File paths: `path/to/file.py`

**Structure Requirements**:
- Always include blank line after section headers
- Separate list items from preceding text with blank line
- Close each major section with single blank line before next section
- Use consistent indentation in nested structures

## Multi-Agent Workflow Architecture

### Tier 1: Orchestrator Agent

**Agent Type**: `general-purpose`
**Model**: `sonnet` (or `opus` for large codebases >300 files)

**Responsibilities**:
1. Analyze target directory structure and file count
2. Determine optimal agent count (2-8 based on file distribution)
3. Decompose work by directory or file count chunks
4. Launch code-documenter agents in parallel
5. Collect and aggregate documentation JSON from all agents
6. Identify cross-references and dependencies across files
7. Launch wiki-publisher agent with complete documentation set
8. Produce final consolidated report with all wiki URLs

**Decomposition Strategy**:
- **By Directory**: When directories have balanced file counts (e.g., gold/, silver/cms/, silver/fvms/)
- **By File Chunks**: When one directory dominates (e.g., 150 gold files → 3 agents with 50 files each)
- **Optimal Agent Count**: 2-8 agents (sweet spot: 4-6 for typical 150-250 file codebases)

**Example Orchestrator Prompt**:
```
You are an ORCHESTRATOR AGENT for automated wiki documentation generation.

PROJECT CONTEXT:
- Repository: unify_2_1_dm_synapse_env_d10 (Azure Synapse PySpark ETL pipelines)
- Medallion architecture: Bronze → Silver → Gold layers
- Python files use: SparkOptimiser, TableUtilities, NotebookLogger
- Follow: .claude/CLAUDE.md and .claude/rules/python_rules.md

YOUR TASK:
Generate comprehensive Azure DevOps wiki documentation for: {target_path}

STEPS:
1. Analyze directory structure and count Python files
2. Decompose into 2-8 optimal subtasks (balance workload)
3. Launch code-documenter agents IN PARALLEL (single message, multiple Task calls)
4. Collect JSON responses from all agents
5. Aggregate documentation and build cross-reference map
6. Launch wiki-publisher agent with complete dataset
7. Produce final report with all created wiki URLs

AGENT LAUNCH:
Use Task tool with subagent_type="general-purpose" for all agents.
Launch all code-documenter agents in a SINGLE MESSAGE for parallelization.

EXPECTED OUTPUT:
Comprehensive JSON report with:
- Total files documented
- All wiki page URLs
- Cross-reference map
- Execution metrics
- Any errors or warnings
```

### Tier 2: Code-Documenter Agents (Workers)

**Agent Type**: `general-purpose` with code analysis specialization
**Count**: 2-8 (determined by orchestrator based on file distribution)
**Model**: `haiku` (faster for code analysis tasks)

**Responsibilities**:
1. Read assigned Python files from file system
2. Perform AST (Abstract Syntax Tree) analysis:
   - Extract imports and dependencies
   - Identify classes and methods with docstrings
   - Extract functions with signatures and docstrings
   - Parse class/method/function descriptions from docstrings
   - Infer purpose from code structure when docstrings are missing
   - Find decorators (especially `@synapse_error_print_handler`)
   - Detect ETL patterns (Extract/Transform/Load methods)
   - Extract parameter descriptions from docstrings
   - Identify return value descriptions
3. Generate comprehensive markdown documentation per file
4. Create repository file links (Azure DevOps blob URLs)
5. Identify related files (e.g., gold → silver mappings)
6. Return structured JSON with all documentation

**Documentation Template Per File**:

CRITICAL: Follow markdown formatting standards strictly:
- Blank line after every header
- Blank line before and after lists
- Blank line before and after code blocks
- Blank line before and after tables
- Use `**bold**` for field labels
- Use backticks for code elements
- Use `-` for unordered lists
- Proper indentation (2 spaces for nested items)

```markdown
# {FileName}

**File Path**: `{relative_path}`
**Repository Link**: [View Source]({azure_devops_blob_url})
**Layer**: {Bronze|Silver|Gold|Utility|Testing|Pipeline}

## Overview

{Brief 2-3 sentence description of file purpose}

## Key Components

### Classes

{For each class found:}

#### `{ClassName}`

**Purpose**: {Extract from class docstring or infer from code - 1-2 sentence description of what this class does}
**Pattern**: {ETL|Utility|Test|Other}

**Description**:

{Extract full class docstring if available, or generate detailed description from code analysis:}

- What problem does this class solve?
- What are its main responsibilities?
- How does it fit into the overall system?
- Any important design patterns or architectural considerations

**Attributes**:

- `{attr_name}`: {type} - {description from docstring or inferred from usage}

**Methods**:

##### `{method_name}({params}) -> {return_type}`

{Extract from method docstring or describe what the method does}

**Parameters**:

- `{param_name}`: {type} - {description from docstring}

**Returns**: {description of return value from docstring}

**Decorators**: {decorator_list}

**Behavior**: {Key behavior or side effects if relevant}

---

### Functions

{For each standalone function:}

#### `{function_name}({params}) -> {return_type}`

**Purpose**: {Extract from function docstring or infer - 1-2 sentence description}

**Description**:

{Extract full function docstring if available, or generate description:}

- What does this function do?
- What are the key inputs and outputs?
- Any important side effects or state changes?
- When should this function be used?

**Parameters**:

- `{param_name}`: {type} - {description from docstring or inferred}

**Returns**: {description of return value from docstring or inferred}

**Decorators**: {decorator_list}

**Behavior**: {Detailed behavior description from docstring or code analysis}

---

## Dependencies

### External Imports

- `{package}`: {purpose}

### Internal Imports

- [`{module}`]({wiki_link_to_module}): {purpose}

### Related Files

- [{related_file_name}]({wiki_link}): {relationship_description}

## Usage Examples

{If ETL class pattern:}

```python
# Bronze to Silver transformation
from {module_path} import {ClassName}

table = {ClassName}(bronze_table_name="bronze_db.b_table_name")
# Extract, Transform, Load executed in __init__
```

{If utility/function:}

```python
from {module_path} import {function_name}

result = {function_name}(param1, param2)
```

## ETL Pattern Details

{If applicable - only for silver/gold layer files:}

**Input Layer**: {Bronze|Silver}
**Output Layer**: {Silver|Gold}
**Source Table**: `{source_db}.{source_table}`
**Target Table**: `{target_db}.{target_table}`

**Transformation Logic**:

- {Key transformation step 1}
- {Key transformation step 2}

## Notes

- {Any special considerations}
- {Performance notes}
- {Known issues or limitations}

---

*Auto-generated documentation*
*Last updated: {timestamp}*
*Generated by: wiki-auto-documenter skill*
```

**JSON Response Format**:
```json
{
  "agent_id": "code-documenter-{n}",
  "status": "completed",
  "files_documented": [
    {
      "file_path": "python_files/gold/g_cms_address.py",
      "wiki_path": "/gold/g_cms_address",
      "markdown_content": "# g_cms_address\n\n...",
      "repo_link": "https://dev.azure.com/emstas/Program%20Unify/_git/unify_2_1_dm_synapse_env_d10?path=/python_files/gold/g_cms_address.py&version=GB{branch}",
      "metadata": {
        "layer": "gold",
        "has_etl_pattern": true,
        "class_count": 1,
        "function_count": 3,
        "decorator_count": 3,
        "import_count": 7
      },
      "dependencies": [
        "utilities/session_optimiser",
        "utilities/table_utilities"
      ],
      "related_files": [
        {
          "file_path": "python_files/silver/silver_cms/s_cms_address.py",
          "relationship": "silver_input",
          "wiki_path": "/silver/silver_cms/s_cms_address"
        }
      ]
    }
  ],
  "summary": {
    "files_processed": 52,
    "files_successful": 52,
    "files_failed": 0,
    "total_classes": 48,
    "total_functions": 156
  },
  "errors": [],
  "warnings": ["File X has no docstrings"],
  "execution_time_seconds": 45
}
```

**Code Analyzer Helper Script**:
The `scripts/code_analyzer.py` provides reusable functions for Python AST analysis:
- `analyze_python_file(file_path)` - Complete AST analysis with docstring extraction
- `extract_classes(ast_tree)` - Parse class definitions with docstrings
- `extract_functions(ast_tree)` - Parse function signatures with docstrings
- `extract_docstring(node)` - Extract docstring from AST node
- `parse_docstring_sections(docstring)` - Parse Google/NumPy/reStructuredText docstring format
- `infer_purpose_from_code(node)` - Generate description when docstring is missing
- `extract_imports(ast_tree)` - Parse import statements
- `detect_etl_pattern(ast_tree)` - Identify Extract/Transform/Load methods
- `extract_parameter_descriptions(docstring)` - Parse parameter docs from docstring
- `extract_return_description(docstring)` - Parse return value docs from docstring
- `generate_markdown(analysis_result)` - Convert analysis to markdown with descriptions

### Tier 3: Wiki-Publisher Agent

**Agent Type**: `general-purpose`
**Model**: `sonnet` (needs robust error handling and API management)

**Responsibilities**:
1. Use `mcp-code-execution` pattern for context-efficient wiki updates
2. Receive complete aggregated documentation from orchestrator
3. Create wiki page hierarchy (parent directories before children)
4. Generate index pages for each directory level
5. Publish/update individual file documentation pages via Azure DevOps Wiki API
6. Add navigation breadcrumbs and cross-reference links
7. Handle API rate limiting (200 requests/minute)
8. Implement retry logic for failed page creations (3 attempts)
9. Verify all pages published successfully
10. Return comprehensive publication report (summary only, not full content)

**Wiki Hierarchy Creation Strategy**:
```
1. Analyze aggregated docs to build directory tree
2. Create pages depth-first (root → leaf):
   a. Create parent directory index page
   b. Create child directory index pages
   c. Create file documentation pages
3. Add navigation links:
   a. Breadcrumbs: /unify_2_1_dm_synapse_env_d10 > /gold > g_cms_address
   b. Directory index: "Files in this directory: [file1], [file2]..."
   c. Related files: Links to upstream/downstream files
```

**Directory Index Page Template**:

CRITICAL: Follow markdown formatting standards strictly:
- Blank line after every header
- Blank line before and after tables
- Blank line before and after lists
- Proper table alignment

```markdown
# {Directory Name}

**Path**: `{directory_path}`
**Total Files**: {file_count}
**Subdirectories**: {subdir_count}
**Repository Folder**: [View in Repository]({repo_folder_link})

## Overview

{Description of what this directory contains}

## Files in This Directory

| File | Description | Key Components |
| ---- | ----------- | -------------- |
| [{file1_name}]({file1_wiki_link}) | {brief_description} | {class_count} classes, {func_count} functions |
| [{file2_name}]({file2_wiki_link}) | {brief_description} | {class_count} classes, {func_count} functions |

## Subdirectories

- [{subdir1}]({subdir1_wiki_link}) - {subdir1_description}
- [{subdir2}]({subdir2_wiki_link}) - {subdir2_description}

## Quick Links

- [Parent Directory]({parent_wiki_link})
- [Repository Folder]({repo_folder_link})

---

*Auto-generated directory index*
*Last updated: {timestamp}*
```

**MCP Code Execution Pattern for Wiki Updates**:
```bash
# Context-efficient wiki updates using mcp-code-execution pattern
python3 /home/vscode/.claude/skills/mcp-code-execution/scripts/ado_wiki_updater.py
```

**Key Benefits of MCP Pattern**:
- Analysis and markdown generation happen in subprocess (not in Claude context)
- Only summary statistics returned to context (not full content)
- Automatic retries and error handling
- ETag management from response headers
- PUT method for updates (not PATCH)

**Script Features**:
```python
# Context-efficient operations:
# 1. Lightweight AST analysis (summary only)
# 2. Markdown generation in subprocess
# 3. GET with ETag from headers: response.headers.get('ETag')
# 4. PUT for updates with If-Match header
# 5. PUT for creates (same endpoint)
# 6. Return minimal summary (not full responses)

# Example usage in agent:
updater = WikiUpdater()
summary = updater.update_utilities_wiki()
# Returns: {pages_updated: 20, pages_created: 0, pages_failed: 0, ...}
# NOT the full markdown content or API responses
```

**JSON Response Format**:
```json
{
  "agent_id": "wiki-publisher",
  "status": "completed",
  "pages_created": 52,
  "pages_updated": 7,
  "index_pages_created": 8,
  "wiki_urls": [
    "https://dev.azure.com/emstas/Program%20Unify/_wiki/wikis/Program-Unify.wiki/274/unify_2_1_dm_synapse_env_d10",
    "https://dev.azure.com/emstas/Program%20Unify/_wiki/wikis/Program-Unify.wiki/275/unify_2_1_dm_synapse_env_d10/gold",
    "https://dev.azure.com/emstas/Program%20Unify/_wiki/wikis/Program-Unify.wiki/276/unify_2_1_dm_synapse_env_d10/gold/g_cms_address"
  ],
  "hierarchy_map": {
    "/unify_2_1_dm_synapse_env_d10": {
      "type": "index",
      "children": ["gold", "silver", "utilities", "testing", "pipeline_operations"]
    },
    "/unify_2_1_dm_synapse_env_d10/gold": {
      "type": "index",
      "files": ["g_cms_address", "g_cms_business", ...]
    }
  },
  "api_metrics": {
    "total_requests": 67,
    "successful_requests": 67,
    "failed_requests": 0,
    "retries": 2,
    "rate_limit_hits": 0,
    "avg_response_time_ms": 340
  },
  "errors": [],
  "warnings": ["Page X already exists, updated instead of created"],
  "execution_time_seconds": 120
}
```

## Workflow Execution Sequence

```
USER REQUEST: "Document python_files/gold/"
    ↓
[ORCHESTRATOR AGENT LAUNCH]
    ├─ Read directory tree: python_files/gold/
    ├─ Count Python files: 50 files
    ├─ Decide: 2 agents (25 files each) OR 1 agent (manageable size)
    ├─ Extract current git branch: "staging"
    ↓
[LAUNCH CODE-DOCUMENTER AGENTS IN PARALLEL]
Single message with multiple Task calls:
    ├─ Task(subagent_type="general-purpose", ..., agent_id="code-doc-1")
    │   └─ Assigned: python_files/gold/g_*.py (files 1-25)
    └─ Task(subagent_type="general-purpose", ..., agent_id="code-doc-2")
        └─ Assigned: python_files/gold/g_*.py (files 26-50)
    ↓
[AGENTS WORK IN PARALLEL]
Code-Doc-1:                     Code-Doc-2:
├─ Read file 1                  ├─ Read file 26
├─ AST analysis                 ├─ AST analysis
├─ Generate markdown            ├─ Generate markdown
├─ Identify dependencies        ├─ Identify dependencies
├─ Create repo links            ├─ Create repo links
├─ ...                          ├─ ...
└─ Return JSON (25 docs)        └─ Return JSON (25 docs)
    ↓                               ↓
[ORCHESTRATOR AGGREGATES RESULTS]
    ├─ Collect JSON from agent 1
    ├─ Collect JSON from agent 2
    ├─ Merge documentation arrays
    ├─ Build cross-reference map (gold → silver relationships)
    ├─ Generate directory hierarchy structure
    ↓
[LAUNCH WIKI-PUBLISHER AGENT]
Task(subagent_type="general-purpose", ...)
    ├─ Receives: Complete documentation set (50 files)
    ├─ Loads: azure-devops skill (wiki API operations)
    ↓
[WIKI-PUBLISHER CREATES PAGES]
    ├─ Create /gold/ index page
    ├─ Create /gold/g_cms_address page
    ├─ Create /gold/g_cms_business page
    ├─ ... (50 file pages)
    ├─ Add breadcrumb navigation
    ├─ Add cross-reference links
    ├─ Update parent /unify_2_1_dm_synapse_env_d10 index
    └─ Return JSON with all URLs
    ↓
[ORCHESTRATOR FINAL REPORT]
    └─ Consolidated JSON:
        - 50 files documented
        - 51 wiki pages created (1 index + 50 files)
        - All wiki URLs
        - Total execution time: 8 minutes
        - Quality metrics
```

## Usage Examples

### Example 1: Document Entire python_files Directory

```python
# User command (via custom slash command or direct)
# /wiki-docs python_files/

# Orchestrator analyzes:
# - 209 Python files total
# - Optimal: 7 agents by directory:
#   - Agent 1: gold/ (50 files)
#   - Agent 2: silver/silver_cms/ (48 files)
#   - Agent 3: silver/silver_fvms/ (32 files)
#   - Agent 4: silver/silver_nicheRMS/ (5 files)
#   - Agent 5: utilities/ (35 files)
#   - Agent 6: testing/ (12 files)
#   - Agent 7: pipeline_operations/ (27 files)

# Expected completion: ~25-30 minutes
# Output: 209 file pages + ~10 index pages = 219 total wiki pages
```

### Example 2: Document Single Directory (Gold Layer Only)

```python
# User command
# /wiki-docs python_files/gold/

# Orchestrator analyzes:
# - 50 Python files in gold/
# - Optimal: 2 agents (25 files each)

# Expected completion: ~7-10 minutes
# Output: 50 file pages + 1 index page = 51 total wiki pages
```

### Example 3: Update Existing Documentation

```python
# User command
# /wiki-docs python_files/utilities/ --update

# Orchestrator:
# - Generates new documentation
# - Wiki-Publisher checks existing pages
# - Updates pages (uses PATCH with If-Match header)
# - Preserves page URLs

# Expected completion: ~5-7 minutes
# Output: 35 pages updated + 1 index updated
```

### Example 4: Custom Wiki Path

```python
# User command
# /wiki-docs python_files/gold/ --wiki-base="/documentation/code/"

# Wiki pages created at:
# /documentation/code/gold/ (instead of default /unify_2_1_dm_synapse_env_d10/gold/)

# Useful for organizing multiple projects in same wiki
```

## Dynamic Path Handling

### Supported Parameters

```
/wiki-docs <path> [options]

Parameters:
  path (required)         - Relative path from repo root
                           Examples: "python_files/", "python_files/gold/", "python_files/utilities/session_optimiser.py"

Options:
  --wiki-base=<path>      - Base path in wiki (default: "/unify_2_1_dm_synapse_env_d10/")
  --branch=<name>         - Git branch for repo links (default: current branch)
  --recursive=<bool>      - Process subdirectories (default: true)
  --update                - Update existing pages instead of creating new
  --dry-run               - Generate docs but don't publish to wiki
```

### Path Resolution Strategy

1. **Absolute vs Relative**: Convert to absolute path from repo root
2. **Directory vs File**:
   - Directory → process all `.py` files recursively (unless --recursive=false)
   - File → process single file
3. **Wiki Path Mapping**: Mirror repo structure in wiki
   - Repo: `python_files/gold/g_cms_address.py`
   - Wiki: `/unify_2_1_dm_synapse_env_d10/gold/g_cms_address`

### Helper Script Usage

```python
from wiki_hierarchy_builder import WikiHierarchyBuilder
import os

builder = WikiHierarchyBuilder(
    repo_root=os.getcwd(),
    wiki_base=f"/{os.path.basename(os.getcwd())}"
)

# Build hierarchy from directory
hierarchy = builder.build_from_path("python_files/gold/")

# Outputs:
# {
#   "wiki_path": "/unify_2_1_dm_synapse_env_d10/gold",
#   "files": [list of .py files],
#   "subdirs": [list of subdirectories],
#   "parent_path": "/unify_2_1_dm_synapse_env_d10"
# }
```

## Repository Linkages

### Link Types

1. **Direct Source Links**: Link to file in Azure DevOps repo
   ```markdown
   [View Source](https://dev.azure.com/emstas/Program%20Unify/_git/unify_2_1_dm_synapse_env_d10?path=/python_files/gold/g_cms_address.py&version=GBstaging)
   ```

2. **Cross-Reference Links**: Links between related wiki pages
   ```markdown
   ## Related Documentation
   - [s_cms_address (Silver Layer)](../silver/silver_cms/s_cms_address) - Upstream source
   - [TableUtilities](../utilities/session_optimiser#tableutilities) - Dependency
   ```

3. **Breadcrumb Navigation**: Hierarchical path links
   ```markdown
   [Home](/) > [unify_2_1_dm_synapse_env_d10](/unify_2_1_dm_synapse_env_d10) > [gold](/unify_2_1_dm_synapse_env_d10/gold) > g_cms_address
   ```

4. **Directory Index Links**: Parent directory link to all files
   ```markdown
   ## Files in gold/
   - [g_cms_address](/unify_2_1_dm_synapse_env_d10/gold/g_cms_address)
   - [g_cms_business](/unify_2_1_dm_synapse_env_d10/gold/g_cms_business)
   ```

### Automatic Relationship Detection

Code analyzer automatically detects:
- **Gold → Silver**: Table name mappings (e.g., `g_cms_address` → `s_cms_address`)
- **Silver → Bronze**: Extract source tables
- **Utility Dependencies**: Import statements referencing other project files
- **Test Coverage**: Test files referencing implementation files

## Docstring Extraction & Description Generation

### Docstring Extraction Strategy

Code-documenter agents should extract and parse docstrings using a multi-tier approach:

#### 1. Extract Docstrings from AST
```python
import ast

def extract_docstring(node):
    """Extract docstring from AST node (class, function, or method)."""
    return ast.get_docstring(node) or ""

def analyze_class(class_node):
    class_info = {
        "name": class_node.name,
        "docstring": extract_docstring(class_node),
        "methods": []
    }

    for item in class_node.body:
        if isinstance(item, ast.FunctionDef):
            method_info = {
                "name": item.name,
                "docstring": extract_docstring(item)
            }
            class_info["methods"].append(method_info)

    return class_info
```

#### 2. Parse Docstring Formats

Support multiple docstring conventions:

**Google Style**:
```python
def function(param1: str, param2: int) -> bool:
    """Brief description.

    Detailed description of what this function does.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When validation fails
    """
```

**NumPy Style**:
```python
def function(param1: str, param2: int) -> bool:
    """
    Brief description.

    Detailed description.

    Parameters
    ----------
    param1 : str
        Description of param1
    param2 : int
        Description of param2

    Returns
    -------
    bool
        Description of return value
    """
```

**reStructuredText Style**:
```python
def function(param1: str, param2: int) -> bool:
    """Brief description.

    Detailed description.

    :param param1: Description of param1
    :type param1: str
    :param param2: Description of param2
    :type param2: int
    :return: Description of return value
    :rtype: bool
    """
```

#### 3. Parse Docstring Sections

```python
import re

def parse_google_docstring(docstring):
    """Parse Google-style docstring into structured sections."""
    sections = {
        "description": "",
        "parameters": [],
        "returns": "",
        "raises": []
    }

    # Extract description (everything before first section)
    desc_match = re.match(r'^(.*?)(?:Args:|Parameters:|Returns:|Raises:|$)',
                          docstring, re.DOTALL)
    if desc_match:
        sections["description"] = desc_match.group(1).strip()

    # Extract Args/Parameters section
    args_match = re.search(r'(?:Args:|Parameters:)\s*(.*?)(?:Returns:|Raises:|$)',
                          docstring, re.DOTALL)
    if args_match:
        for line in args_match.group(1).strip().split('\n'):
            param_match = re.match(r'\s*(\w+):\s*(.*)', line)
            if param_match:
                sections["parameters"].append({
                    "name": param_match.group(1),
                    "description": param_match.group(2)
                })

    # Extract Returns section
    returns_match = re.search(r'Returns:\s*(.*?)(?:Raises:|$)',
                             docstring, re.DOTALL)
    if returns_match:
        sections["returns"] = returns_match.group(1).strip()

    return sections
```

#### 4. Infer Purpose When Docstrings Are Missing

When docstrings are not present, infer purpose from:

- **Class name patterns**: `*Manager`, `*Builder`, `*Factory`, `*Handler`
- **Method name patterns**: `get_*`, `set_*`, `create_*`, `delete_*`, `process_*`
- **Decorators**: `@property`, `@staticmethod`, `@classmethod`, `@synapse_error_print_handler`
- **Method structure**: Analyze first few statements for intent
- **ETL patterns**: Methods named `extract`, `transform`, `load`

```python
def infer_class_purpose(class_node):
    """Infer class purpose from name and structure."""
    name = class_node.name

    # Check naming patterns
    if name.endswith('Manager'):
        return f"Manages {name[:-7].lower()} operations and state"
    elif name.endswith('Builder'):
        return f"Builds and constructs {name[:-7].lower()} instances"
    elif name.endswith('Factory'):
        return f"Creates and configures {name[:-7].lower()} objects"
    elif name.endswith('Handler'):
        return f"Handles {name[:-7].lower()} events and processing"

    # Check for ETL pattern
    method_names = [m.name for m in class_node.body
                   if isinstance(m, ast.FunctionDef)]
    if set(['extract', 'transform', 'load']).issubset(method_names):
        return "ETL class for data transformation between medallion layers"

    # Generic fallback
    return f"Implements {name} functionality"

def infer_method_purpose(method_node):
    """Infer method purpose from name and signature."""
    name = method_node.name

    # Special methods
    if name == '__init__':
        return "Initialize instance with configuration and dependencies"
    elif name.startswith('get_'):
        return f"Retrieve {name[4:].replace('_', ' ')}"
    elif name.startswith('set_'):
        return f"Set {name[4:].replace('_', ' ')}"
    elif name.startswith('create_'):
        return f"Create new {name[7:].replace('_', ' ')}"
    elif name.startswith('delete_'):
        return f"Delete {name[7:].replace('_', ' ')}"
    elif name.startswith('process_'):
        return f"Process {name[8:].replace('_', ' ')}"
    elif name.startswith('validate_'):
        return f"Validate {name[9:].replace('_', ' ')}"
    elif name.startswith('is_') or name.startswith('has_'):
        return f"Check if {name[3:].replace('_', ' ')}"

    return f"Perform {name.replace('_', ' ')} operation"
```

#### 5. Generate Complete Descriptions

Combine extracted docstrings with inferred information:

```python
def generate_description(node, docstring, inferred_purpose):
    """Generate complete description from docstring and inference."""
    if docstring:
        # Use docstring as primary source
        parsed = parse_google_docstring(docstring)
        return {
            "purpose": parsed["description"].split('\n')[0],  # First line
            "description": parsed["description"],
            "parameters": parsed["parameters"],
            "returns": parsed["returns"]
        }
    else:
        # Use inferred purpose
        return {
            "purpose": inferred_purpose,
            "description": f"{inferred_purpose}. (No docstring available - inferred from code structure)",
            "parameters": [],  # Can infer from type hints
            "returns": ""
        }
```

### Integration with Code Analysis

The code-documenter agents should:

1. **Read file** with proper encoding (UTF-8)
2. **Parse AST** using `ast.parse()`
3. **Extract docstrings** for all classes, methods, functions
4. **Parse docstring sections** (description, parameters, returns)
5. **Infer purpose** when docstrings are missing
6. **Generate markdown** with all descriptions included
7. **Include examples** from docstrings if present (Examples section)

## Quality Gates & Error Handling

### Code-Documenter Agent Quality Checks

1. **File Validation**:
   - Verify file exists before reading
   - Check Python syntax validity (`ast.parse()`)
   - Handle unreadable files gracefully (permission errors, encoding issues)

2. **Documentation Quality**:
   - Ensure minimum content length (>100 characters)
   - Verify all sections populated
   - Check repo links are well-formed
   - **Validate markdown formatting**:
     - Blank line after every header (## Header\n\n)
     - Blank line before and after lists
     - Blank line before and after code blocks
     - Blank line before and after tables
     - Proper use of bold for field labels (**Label**:)
     - Proper use of backticks for code elements (`code`)
     - Consistent list markers (use `-` for unordered lists)
     - Proper table alignment with separator row (| --- | --- |)
     - No double blank lines
     - Consistent indentation (2 spaces for nested items)
   - **Verify class/function descriptions are present**:
     - Extract docstrings for all classes, methods, and functions
     - If docstring missing, infer purpose from code analysis
     - Ensure descriptions are meaningful (not just "A class" or "A function")
     - Include parameter descriptions from docstrings
     - Include return value descriptions from docstrings
     - Parse common docstring formats (Google, NumPy, reStructuredText)

3. **Error Handling**:
   ```python
   try:
       analysis = analyze_python_file(file_path)
   except SyntaxError as e:
       warnings.append(f"Syntax error in {file_path}: {e}")
       # Generate partial documentation with error notice
   except Exception as e:
       errors.append(f"Failed to analyze {file_path}: {e}")
       # Skip file, continue with others
   ```

### Wiki-Publisher Agent Quality Checks

1. **API Response Validation**:
   - Check status codes (201 Created, 200 OK expected)
   - Validate response includes eTag (version identifier)
   - Verify page URL in response

2. **Retry Logic**:
   ```python
   max_retries = 3
   for attempt in range(max_retries):
       try:
           response = wiki.create_or_update_page(path, content)
           if response.status_code in [200, 201]:
               break
       except requests.exceptions.RequestException as e:
           if attempt == max_retries - 1:
               errors.append(f"Failed to create page {path} after {max_retries} attempts")
           else:
               time.sleep(2 ** attempt)  # Exponential backoff
   ```

3. **Rate Limiting**:
   - Track request count per minute
   - Pause when approaching 200 requests/minute limit
   - Use batch operations where possible

4. **Cross-Link Verification**:
   - After all pages created, verify links resolve
   - Report broken links as warnings

### Orchestrator Quality Validation

1. **Agent Completion Check**:
   - Verify all launched agents returned results
   - Check agent status: "completed" vs "failed"
   - Ensure file count matches expected

2. **Data Aggregation Validation**:
   - Verify no duplicate file paths in aggregated docs
   - Check all dependencies resolved to valid paths
   - Validate JSON schema from all agents

3. **Final Report Requirements**:
   - List all errors and warnings from all agents
   - Provide success rate (files documented / total files)
   - Include recovery steps for any failures

## Integration with Existing Skills

### Using azure-devops Skill

The wiki-publisher agent loads the `azure-devops` skill for REST API operations:

```markdown
Load the azure-devops skill for wiki API operations.

Use scripts/ado_wiki_client.py to interact with Azure DevOps Wiki REST API.
The skill provides context-efficient REST API helpers without loading 50+ MCP tools.

See .claude/skills/azure-devops/skill.md for complete documentation.
```

### Using multi-agent-orchestration Skill

This skill follows the orchestration patterns from `multi-agent-orchestration`:

- **Orchestrator Pattern**: Single orchestrator coordinating multiple workers
- **JSON Communication**: Structured response format from all agents
- **Parallel Execution**: Launch all workers in single message
- **Quality Gates**: Validation at agent and orchestrator levels
- **Consolidated Reporting**: Aggregate metrics and results

Reference: `.claude/skills/multi-agent-orchestration/skill.md`

## Helper Scripts Reference

### scripts/ado_wiki_client.py

Azure DevOps Wiki REST API client with authentication and error handling.

**Key Methods**:
- `create_or_update_page(path, content, comment)` - Creates new or updates existing page
- `get_page(path)` - Retrieves page content and metadata (including eTag version)
- `delete_page(path)` - Removes wiki page
- `list_pages(path)` - Lists all pages under path
- `get_page_stats(path)` - Returns page views and edit history

**Usage**:
```python
from scripts.ado_wiki_client import WikiClient

client = WikiClient.from_env()  # Reads from environment variables
response = client.create_or_update_page(
    path="/unify_2_1_dm_synapse_env_d10/gold/g_cms_address",
    content=markdown_content,
    comment="Auto-generated documentation"
)
print(response["remoteUrl"])  # Wiki page URL
```

### scripts/code_analyzer.py

Python AST analysis for comprehensive code documentation.

**Key Functions**:
- `analyze_file(file_path) -> dict` - Complete analysis of Python file
- `extract_classes(ast_tree) -> list` - Parse class definitions with methods
- `extract_functions(ast_tree) -> list` - Parse function signatures and decorators
- `extract_imports(ast_tree) -> dict` - Parse import statements (external + internal)
- `detect_etl_pattern(class_node) -> bool` - Check for Extract/Transform/Load methods
- `resolve_internal_imports(import_path, repo_root) -> str` - Convert import to file path
- `generate_markdown(analysis) -> str` - Convert analysis dict to markdown

**Usage**:
```python
from scripts.code_analyzer import analyze_file, generate_markdown, extract_docstring

analysis = analyze_file("python_files/gold/g_cms_address.py")
markdown = generate_markdown(analysis)

# analysis contains:
# {
#   "classes": [
#     {
#       "name": "ClassName",
#       "docstring": "Full class docstring...",
#       "purpose": "Brief extracted purpose",
#       "description": "Detailed description from docstring",
#       "methods": [
#         {
#           "name": "method_name",
#           "signature": "method_name(param1: str, param2: int) -> bool",
#           "docstring": "Full method docstring...",
#           "purpose": "What this method does",
#           "parameters": [
#             {"name": "param1", "type": "str", "description": "..."},
#             {"name": "param2", "type": "int", "description": "..."}
#           ],
#           "returns": {"type": "bool", "description": "..."},
#           "decorators": ["@synapse_error_print_handler"]
#         }
#       ]
#     }
#   ],
#   "functions": [
#     {
#       "name": "function_name",
#       "signature": "function_name(arg1: str) -> dict",
#       "docstring": "Full function docstring...",
#       "purpose": "What this function does",
#       "parameters": [...],
#       "returns": {...},
#       "decorators": [...]
#     }
#   ],
#   "imports": {"external": [...], "internal": [...]},
#   "has_etl_pattern": True,
#   "file_path": "...",
#   "line_count": 145
# }
```

### scripts/wiki_hierarchy_builder.py

Directory tree to wiki hierarchy conversion.

**Key Methods**:
- `build_hierarchy(path) -> dict` - Build complete hierarchy from path
- `get_python_files(directory) -> list` - Find all .py files recursively
- `map_repo_to_wiki(repo_path, wiki_base) -> str` - Convert repo path to wiki path
- `generate_index_content(directory_info) -> str` - Create directory index markdown
- `detect_relationships(file_list) -> dict` - Find related files (gold↔silver)

**Usage**:
```python
from scripts.wiki_hierarchy_builder import WikiHierarchyBuilder
import os

builder = WikiHierarchyBuilder(
    repo_root=os.getcwd(),
    wiki_base=f"/{os.path.basename(os.getcwd())}"
)

hierarchy = builder.build_hierarchy("python_files/gold/")
# Returns complete tree structure with file counts, wiki paths, relationships
```

## Best Practices

### DO
- ✅ Use orchestrator to decompose work before launching agents
- ✅ Launch all code-documenter agents in parallel (single message)
- ✅ Validate JSON responses from all agents before aggregation
- ✅ Create parent directory pages before child pages
- ✅ Include retry logic for wiki API calls
- ✅ Generate comprehensive error reports
- ✅ Add breadcrumb navigation to all pages
- ✅ Link documentation to source code in repo
- ✅ Use descriptive commit messages for wiki edits
- ✅ **Follow markdown formatting standards strictly**:
  - ✅ Blank line after every header
  - ✅ Blank line before and after lists, code blocks, and tables
  - ✅ Use `**bold**` for field labels
  - ✅ Use backticks for code elements
  - ✅ Use `-` for unordered lists
  - ✅ Proper table alignment with separator rows
  - ✅ Consistent indentation (2 spaces for nested items)
  - ✅ No double blank lines
- ✅ **Extract and include docstrings for all classes/functions**
- ✅ **Parse parameter and return value descriptions from docstrings**
- ✅ **Infer purpose when docstrings are missing**
- ✅ **Include behavior descriptions for methods with side effects**
- ✅ **Document class patterns (ETL, Utility, Factory, etc.)**

### DON'T
- ❌ Launch agents sequentially (defeats parallelization benefit)
- ❌ Skip directory index pages (breaks navigation)
- ❌ Create child pages before parent pages (wiki hierarchy violation)
- ❌ Ignore API rate limits (causes request failures)
- ❌ Skip error handling (partial failures cascade)
- ❌ Generate docs without repo links (reduces discoverability)
- ❌ Forget to update existing pages (causes duplicate content)
- ❌ **Violate markdown formatting standards**:
  - ❌ Missing blank lines after headers
  - ❌ Missing blank lines around lists, code blocks, or tables
  - ❌ Using asterisks (*) for unordered lists (use hyphens -)
  - ❌ Inconsistent indentation in nested structures
  - ❌ Double blank lines between sections
  - ❌ Plain text for field labels (must use **bold**)
  - ❌ Plain text for code elements (must use `backticks`)
  - ❌ Tables without proper separator rows
- ❌ **Omit docstrings from documentation** (users need to understand purpose)
- ❌ **Use generic descriptions** (avoid "A class", "A function" - be specific)
- ❌ **Ignore parameter/return descriptions** (critical for API understanding)
- ❌ **Skip behavioral descriptions** (methods with side effects need explanation)

## Troubleshooting

### Issue: Agent Failed to Complete

**Symptoms**: Orchestrator reports agent status "failed" or no response

**Solutions**:
1. Check agent logs for specific errors
2. Verify file paths are accessible
3. Reduce file count per agent (e.g., 25 → 15 files)
4. Switch agent model from haiku → sonnet for complex files

### Issue: Wiki Page Creation Failed

**Symptoms**: Wiki-publisher reports 4xx or 5xx errors

**Solutions**:
1. Verify Azure DevOps PAT has `vso.wiki_write` scope
2. Check wiki path doesn't contain invalid characters
3. Ensure parent pages exist before creating child pages
4. Check rate limiting (wait 60s if hitting 200 req/min limit)
5. Verify wiki ID in URL is correct

### Issue: Broken Cross-Reference Links

**Symptoms**: Wiki page links return 404 errors

**Solutions**:
1. Verify target page was successfully created
2. Check relative path syntax (use forward slashes)
3. Ensure URL encoding for special characters
4. Use absolute wiki paths when unsure of relative path

### Issue: Missing Dependencies in Documentation

**Symptoms**: Import statements not showing related file links

**Solutions**:
1. Verify internal import resolution logic
2. Check file exists in expected location
3. Update `resolve_internal_imports()` for new patterns
4. Add manual cross-references in post-processing

## Performance Metrics

**Expected Execution Times** (209 files, 7 agents):
- Directory analysis: 30-60 seconds
- Code documentation (parallel): 5-8 minutes
- Wiki publishing: 3-5 minutes
- **Total: ~20-30 minutes**

**Optimization Tips**:
- Use `haiku` model for code-documenter agents (faster, cheaper)
- Batch wiki page creation where API supports it
- Cache AST analysis results during iteration
- Use --dry-run to test documentation before publishing

## Success Criteria

- ✅ All Python files in target path documented
- ✅ Wiki hierarchy mirrors repository structure exactly
- ✅ All directory index pages created
- ✅ All source code links functional
- ✅ All cross-references between pages work
- ✅ No API errors or failed page creations
- ✅ Comprehensive execution report provided
- ✅ All wiki page URLs returned in final report

---

**Skill Version**: 2.1
**Created**: 2025-11-12
**Last Updated**: 2025-11-13
**Maintainer**: AI Agent Team
**Status**: Production Ready

## Version History

### Version 2.1 (2025-11-13)
**Major Enhancement: Markdown Formatting Standards & Quality Control**

- ✅ Added comprehensive markdown formatting standards section
- ✅ Implemented strict formatting guidelines for all documentation
- ✅ Added blank line requirements for headers, lists, code blocks, and tables
- ✅ Enforced consistent use of bold for field labels
- ✅ Enforced consistent use of backticks for code elements
- ✅ Standardized list markers (hyphens for unordered lists)
- ✅ Added table alignment standards with proper separator rows
- ✅ Updated documentation template with formatting requirements
- ✅ Updated directory index template with proper formatting
- ✅ Enhanced quality gates with markdown validation checks
- ✅ Added markdown formatting to best practices (DO/DON'T)
- ✅ Included formatting validation in code-documenter agent requirements

**Impact**: All generated documentation now follows consistent markdown standards, improving readability and maintainability across the entire wiki. Ensures professional appearance and compatibility with Azure DevOps wiki rendering.

### Version 2.0 (2025-11-12)
**Major Enhancement: Comprehensive Docstring Extraction & Description Generation**

- ✅ Added docstring extraction from all classes, methods, and functions
- ✅ Implemented parsing for multiple docstring formats (Google, NumPy, reStructuredText)
- ✅ Added intelligent purpose inference when docstrings are missing
- ✅ Enhanced documentation template with detailed description sections
- ✅ Added parameter and return value description extraction
- ✅ Implemented behavior description for methods with side effects
- ✅ Added class pattern detection (ETL, Manager, Builder, Factory, Handler)
- ✅ Enhanced quality gates to validate description presence and quality
- ✅ Added comprehensive docstring parsing examples and helper functions
- ✅ Updated best practices with description-focused guidelines

**Impact**: Documentation now includes meaningful descriptions for every class, method, and function, dramatically improving readability and developer understanding.

### Version 1.0 (2025-11-12)
- Initial release with multi-agent orchestration
- Basic AST analysis and markdown generation
- Azure DevOps wiki publishing
- Cross-reference link generation
