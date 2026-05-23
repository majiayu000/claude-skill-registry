---
name: llm-docs-optimizer
description: Optimize documentation for AI coding assistants and LLMs. Improves docs for Claude, Copilot, and other AI tools through c7score optimization, llms.txt generation, question-driven restructuring, and automated quality scoring. Use when asked to improve, optimize, or enhance documentation for AI assistants, LLMs, c7score, Context7, or when creating llms.txt files. Also use for documentation quality analysis, README optimization, or ensuring docs follow best practices for LLM retrieval systems.
---

# LLM Docs Optimizer

This skill optimizes project documentation and README files for AI coding assistants and LLMs like Claude, GitHub Copilot, and others. It improves documentation quality through multiple approaches: c7score optimization (Context7's quality benchmark), llms.txt file generation for LLM navigation, question-driven content restructuring, and automated quality scoring across 5 key metrics.

**Version:** 1.3.0

## Understanding C7Score

C7score evaluates documentation using 5 metrics across two categories:

**LLM Analysis (85% of score):**
1. **Question-Snippet Comparison (80%)**: How well snippets answer common developer questions
2. **LLM Evaluation (5%)**: Relevancy, clarity, correctness, and uniqueness

**Text Analysis (15% of score):**
3. **Formatting (5%)**: Proper structure and language tags
4. **Project Metadata (5%)**: Absence of irrelevant content
5. **Initialization (5%)**: Not just imports/installations

For detailed information on each metric, read `references/c7score_metrics.md`.

## Core Workflow

### Step 0: Ask About llms.txt Generation (C7Score Optimization Only)

**IMPORTANT**: When the user requests c7score documentation optimization, ALWAYS ask if they also want an llms.txt file:

Use the `AskUserQuestion` tool with this question:

```
Question: "Would you also like me to generate an llms.txt file for your project?"
Header: "llms.txt"
Options:
  - "Yes, create both optimized docs and llms.txt"
    Description: "Optimize documentation for c7score AND generate an llms.txt navigation file"
  - "No, just optimize the documentation"
    Description: "Only perform c7score optimization without llms.txt generation"
```

**If user chooses "Yes"**:
- Proceed with c7score optimization workflow (Steps 1-5)
- Then follow the llms.txt generation workflow
- Provide both optimized documentation AND llms.txt file

**If user chooses "No"**:
- Proceed with c7score optimization workflow only (Steps 1-5)

**Note**: If the user explicitly requests ONLY llms.txt generation (no c7score mention), skip this step and go directly to the llms.txt generation workflow.

### Step 1: Analyze Current Documentation

When given a project or documentation to optimize:

1. **Read the documentation files** (README.md, docs/*.md, etc.)
2. **Run the analysis script** (optional but recommended) to identify issues:
   ```bash
   python scripts/analyze_docs.py <path-to-readme.md>
   ```
   Note: The script requires Python 3.7+ and is optional. You can skip it if Python is unavailable.
3. **Review the analysis report** (if script was run) to understand current state:
   - Count of code snippets with issues
   - Breakdown by metric type
   - Duplicate snippets
   - Language distribution

### Step 2: Generate Developer Questions

Create a list of 15-20 questions that developers commonly ask about the project:

- Focus on "How do I..." questions
- Cover setup, configuration, basic usage, common operations
- Include authentication, error handling, advanced features
- Think about real-world use cases

**Example questions:**
- How do I install and set up [project]?
- How do I authenticate/configure [project]?
- How do I [main feature/operation]?
- How do I handle errors?
- How do I integrate with [common tools]?

### Step 3: Map Questions to Snippets

Evaluate which questions are well-answered by existing documentation:
- ✅ Questions with complete, working code examples
- ⚠️ Questions with partial or theoretical answers
- ❌ Questions with no answers

Prioritize filling gaps for unanswered questions.

### Step 4: Optimize Documentation

Apply optimizations based on priority:

**Priority 1: Question Coverage (80% of score)**
- Add complete code examples for unanswered questions
- Transform API references into usage examples
- Ensure each major snippet answers at least one common question
- Make examples self-contained and runnable

**Priority 2: Remove Duplicates**
- Identify similar or identical snippets
- Consolidate into comprehensive examples
- Ensure each snippet provides unique value

**Priority 3: Fix Formatting**
- Use proper language tags (python, javascript, typescript, bash, etc.)
- Follow TITLE / DESCRIPTION / CODE structure
- Avoid very short (<3 lines) or very long (>100 lines) snippets
- Don't use descriptive strings as language tags

**Priority 4: Remove Metadata**
- Remove or minimize licensing snippets
- Remove directory structure listings
- Remove citations and BibTeX entries
- Keep only usage-relevant content

**Priority 5: Enhance Initialization Snippets**
- Combine import-only snippets with usage examples
- Add context to installation commands
- Always show what comes after setup

For detailed transformation patterns, read `references/optimization_patterns.md`.

### Step 5: Validate Optimizations

Before finalizing, verify each optimized snippet:

✅ Can run standalone (copy-paste works)
✅ Answers a specific developer question
✅ Provides unique information
✅ Uses proper format and language tag
✅ Focuses on practical usage
✅ Includes necessary imports/setup
✅ No licensing, citations, or directory trees
✅ Syntactically correct code

### Step 6: Evaluate C7Score Impact

After optimization, provide a c7score evaluation comparing the original and optimized documentation:

**Evaluation Process:**

1. **Analyze Original Documentation** against c7score metrics:
   - Question-Snippet Matching (80%): How well do code examples answer developer questions?
   - LLM Evaluation (10%): Clarity, correctness, unique information
   - Formatting (5%): Proper markdown structure and language tags
   - Metadata Removal (2.5%): Absence of licenses, citations, directory trees
   - Initialization (2.5%): More than just imports/installation

2. **Analyze Optimized Documentation** using the same metrics

3. **Calculate Scores** (0-100 for each metric):
   - For Question-Snippet Matching:
     - 90-100: Excellent - Complete, practical answers with context
     - 70-89: Good - Most questions answered with working examples
     - 50-69: Fair - Partial answers, missing context
     - 30-49: Poor - Vague or incomplete answers
     - 0-29: Very Poor - Questions not addressed

   - For LLM Evaluation:
     - 90-100: Unique, clear, syntactically perfect
     - 70-89: Mostly unique and clear, minor issues
     - 50-69: Some duplicates or clarity issues
     - 30-49: Significant duplicates or syntax errors
     - 0-29: Major quality problems

   - For Formatting:
     - 100: All snippets properly formatted with language tags
     - 80-99: Minor formatting issues
     - 50-79: Multiple formatting problems
     - 0-49: Significant formatting issues

   - For Metadata Removal:
     - 100: No project metadata
     - 50-99: Some metadata present
     - 0-49: Significant metadata content

   - For Initialization:
     - 100: All examples show usage beyond setup
     - 50-99: Some initialization-only snippets
     - 0-49: Many initialization-only snippets

4. **Present Results** in this format:

```markdown
## C7Score Evaluation

### Original Documentation Score: XX/100

**Metric Breakdown:**
- Question-Snippet Matching: XX/100 (weight: 80%)
  - Analysis: [Brief explanation of score]
- LLM Evaluation: XX/100 (weight: 10%)
  - Analysis: [Brief explanation]
- Formatting: XX/100 (weight: 5%)
  - Analysis: [Brief explanation]
- Metadata Removal: XX/100 (weight: 2.5%)
  - Analysis: [Brief explanation]
- Initialization: XX/100 (weight: 2.5%)
  - Analysis: [Brief explanation]

**Weighted Average:** XX/100

---

### Optimized Documentation Score: XX/100

**Metric Breakdown:**
[Same format as above]

**Weighted Average:** XX/100

---

### Improvement Summary

**Overall Improvement:** +XX points (XX → XX)

**Key Improvements:**
- [Metric]: +XX points - [What specifically improved]
- [Metric]: +XX points - [What specifically improved]

**Impact Assessment:**
[Brief explanation of how optimizations improved the documentation quality]
```

5. **Scoring Guidelines:**
   - Be objective and consistent
   - Base scores on concrete evidence from the documentation
   - Explain reasoning for each score
   - Highlight specific improvements made
   - Final score is weighted average: (Q×0.8) + (L×0.1) + (F×0.05) + (M×0.025) + (I×0.025)

**Note:** These are estimated scores based on c7score methodology. For official scores, users can submit to Context7's benchmark.

## Common Transformation Patterns

### Transform API Reference → Complete Example

**Before:**
```
## authenticate(api_key)
Authenticates the client.
```

**After:**
```
## Authentication

```python
from library import Client

client = Client(api_key="your_key")
client.authenticate()

# Now ready to make requests
result = client.get_data()
```
```

### Transform Import-Only → Quick Start

**Before:**
```python
from library import Client, Config
```

**After:**
```python
# Install: pip install library
from library import Client, Config

# Initialize and use
config = Config(api_key="key")
client = Client(config)
result = client.query("SELECT * FROM data")
```

### Transform Multiple Small → One Comprehensive

Combine related small snippets into one complete workflow example.

## README Structure for High Scores

Organize documentation to prioritize question-answering:

1. **Quick Start** (High Priority)
   - Installation + immediate usage
   - Complete, working first example
   
2. **Common Use Cases** (High Priority)
   - Each major feature with full examples
   - Real-world scenarios
   
3. **Configuration** (Medium Priority)
   - Common configuration patterns with context
   
4. **Error Handling** (Medium Priority)
   - Practical error handling examples
   
5. **API Reference** (Lower Priority)
   - Include usage examples for each method
   
6. **Advanced Topics** (Lower Priority)
   - Complex scenarios with complete code

## Tips for High Scores

1. **Think "How would a developer use this?"** - Lead with usage, not theory
2. **Make examples copy-paste ready** - Include all imports and setup
3. **Answer questions, don't just document APIs** - Show solutions, not just signatures
4. **One snippet, one lesson** - Avoid duplicate information
5. **Format consistently** - Use proper language tags and structure
6. **Remove noise** - No licensing, directory trees, or pure imports in main docs
7. **Test your examples** - Ensure code is syntactically correct and runnable
8. **Focus on the 80%** - Question-answering dominates the score

## Skill Capabilities

This skill provides two main capabilities:

1. **C7Score Documentation Optimization** - Improve documentation quality for AI-assisted coding
2. **llms.txt File Generation** - Create LLM-friendly navigation files for projects

## When to Use This Skill

### For C7Score Optimization:
- User asks to optimize documentation for c7score
- User wants to improve README or docs for Context7
- User requests documentation analysis or quality assessment
- User is creating new documentation for a library/framework
- User mentions improving documentation for AI coding assistants
- User wants to follow best practices for developer documentation

### For llms.txt Generation:
- User asks to create an llms.txt file
- User mentions llmstxt.org or llms.txt format
- User wants to make their project more accessible to LLMs
- User is setting up documentation navigation for AI tools
- User asks how to help LLMs understand their project structure

## Output Format

When optimizing documentation, provide:

1. **Analysis summary** - Key findings and issues
2. **Optimized documentation** - Complete, improved files
3. **Change summary** - What was improved and why
4. **Score impact estimate** - Expected improvement by metric
5. **Recommendations** - Further improvement suggestions

Save the optimized documentation files in the user's working directory or a designated output location. You can ask the user where they'd like the files saved if unclear.

## Examples

- For c7score optimization: See `examples/sample_readme.md` for before/after transformations
- For llms.txt generation: See `examples/sample_llmstxt.md` for different project types

---

# Creating llms.txt Files

## What is llms.txt?

**llms.txt** is a standardized markdown file format designed to provide LLM-friendly content summaries and documentation navigation. It helps language models and AI agents quickly understand project structure and find relevant documentation.

Key purposes:
- Provides brief background information and guidance
- Links to detailed markdown documentation
- Optimized for consumption by language models
- Helps LLMs navigate documentation efficiently
- Used at inference time when users request information

Official specification: https://llmstxt.org/

For complete format details, read `references/llmstxt_format.md`.

## llms.txt Generation Workflow

### Step 1: Analyze Project Structure

When asked to create an llms.txt file:

1. **Explore the project directory** to understand structure:
   - Identify documentation files (README.md, docs/, CONTRIBUTING.md, etc.)
   - Find example files or tutorials
   - Locate API reference or configuration docs
   - Check for guides, blog posts, or additional resources

2. **Identify project type**:
   - Python library, CLI tool, web framework, Claude skill, etc.
   - This determines the appropriate section structure

3. **Assess documentation organization**:
   - Is documentation in a single README?
   - Multiple files in a docs/ directory?
   - Wiki, website, or external documentation?

### Step 2: Determine Project Category

Choose the appropriate template based on project type:

**Python Library / Package:**
- Documentation, API Reference, Examples, Development, Optional

**CLI Tool:**
- Getting Started, Commands, Configuration, Examples, Optional

**Web Framework:**
- Documentation, Guides, API Reference, Examples, Integrations, Optional

**Claude Skill:**
- Documentation, Reference Materials, Examples, Development, Optional

**General Project:**
- Documentation, Guides, Examples, Contributing, Optional

See `examples/sample_llmstxt.md` for complete examples of each type.

### Step 3: Create the Structure

Build the llms.txt file following this structure:

#### 1. H1 Title (Required)
```markdown
# Project Name
```

#### 2. Blockquote Summary (Highly Recommended)
```markdown
> Brief description of what the project does, its main purpose, and key value proposition.
> Should be 1-3 sentences that give LLMs essential context.
```

#### 3. Key Features/Principles (Optional but Helpful)
```markdown
Key features:
- Main feature or capability
- Another important aspect
- Third key point

Project follows these principles:
- Design principle 1
- Design principle 2
```

#### 4. Documentation Sections (Core Content)

Organize links into H2-headed sections:

```markdown
## Documentation

- [Link Title](https://full-url): Brief description of what this contains
- [Another Doc](https://full-url): What developers will find here

## API Reference

- [Core API](https://full-url): Main API documentation
- [Configuration](https://full-url): Configuration options

## Examples

- [Basic Usage](https://full-url): Simple getting-started examples
- [Advanced Patterns](https://full-url): Complex use cases

## Optional

- [Blog](https://full-url): Latest updates and tutorials
- [Community](https://full-url): Where to get help
```

### Step 4: Format Links Properly

Each link must follow this exact format:

```markdown
- [Descriptive Title](https://full-url): Optional helpful notes about the resource
```

**Requirements:**
- Use markdown bullet lists (`-`)
- Use markdown hyperlinks `[text](url)`
- Use **full URLs** with protocol (https://), not relative paths
- Add `:` followed by helpful description (optional but recommended)
- Prefer linking to `.md` files when possible

**Examples:**

✅ Good:
```markdown
- [Quick Start](https://github.com/user/repo/blob/main/docs/quickstart.md): Get running in 5 minutes
- [API Reference](https://github.com/user/repo/blob/main/docs/api.md): Complete function documentation
```

❌ Bad:
```markdown
- [Guide](../docs/guide.md): A guide
- Guide: docs/guide.md
- [Click here](guide)
```

### Step 5: Organize Sections by Priority

Order sections from most to least important:

**High Priority (First):**
- Documentation / Getting Started
- Core API / Commands
- Examples

**Medium Priority (Middle):**
- Guides / Tutorials
- Configuration
- Development / Contributing

**Low Priority (Last - Optional Section):**
- Blog posts
- Community links
- Changelog
- Extended tutorials
- Background reading

The **"Optional" section** has special meaning: LLMs can skip this when shorter context is needed.

### Step 6: Handle Different Repository Structures

#### GitHub Repository

For GitHub repos, construct URLs like:
```markdown
https://github.com/username/repo/blob/main/path/to/file.md
```

#### Local Files Only

If no remote repository exists yet, use placeholder URLs:
```markdown
https://github.com/username/repo/blob/main/README.md
```

And note in your response that URLs need to be updated when the repo is published.

#### Documentation Website

If project has a docs website, prefer linking to markdown versions:
```markdown
- [Guide](https://docs.example.com/guide.md): Getting started guide
```

Or link to HTML with `.md` suffix if markdown versions exist:
```markdown
- [Guide](https://docs.example.com/guide.html.md): Getting started guide
```

### Step 7: Validate the File

Before finalizing, check:

- ✅ File named exactly `llms.txt` (lowercase)
- ✅ Has H1 title as first element
- ✅ Has blockquote summary (highly recommended)
- ✅ Uses only H1 and H2 headings (no H3, H4, etc. in descriptive content)
- ✅ All links use full URLs with protocol
- ✅ Links use proper markdown format `[text](url)`
- ✅ Sections logically organized (essential → optional)
- ✅ Descriptive notes added after colons where helpful
- ✅ Content is concise and clear
- ✅ No complex markdown (tables, images, code blocks in the llms.txt itself)

## Common Section Templates

### For Python Libraries

```markdown
# LibraryName

> Brief description of what the library does and its main use case.

## Documentation
- Getting started, installation, core concepts

## API Reference
- Module/class/function documentation

## Examples
- Usage examples, patterns, recipes

## Development
- Contributing, testing, development setup

## Optional
- Changelog, blog, community
```

### For CLI Tools

```markdown
# ToolName

> Brief description of what the tool does.

## Getting Started
- Installation, quickstart

## Commands
- Command reference and examples

## Configuration
- Config files, environment variables

## Examples
- Common workflows and patterns

## Optional
- Advanced usage, plugins, troubleshooting
```

### For Web Frameworks

```markdown
# FrameworkName

> Brief description and key features.

## Documentation
- Core concepts, routing, data fetching

## Guides
- Authentication, deployment, testing

## API Reference
- Configuration, CLI, components

## Examples
- Sample applications

## Integrations
- Third-party tools and services

## Optional
- Blog, showcase, community
```

### For Claude Skills

```markdown
# skill-name

> Brief description of what the skill does.

## Documentation
- README, SKILL.md, usage guide

## Reference Materials
- Specifications, patterns, formats

## Examples
- Usage examples, before/after

## Development
- Scripts, contributing guide

## Optional
- External resources, related tools
```

## Tips for High-Quality llms.txt Files

1. **Be Concise**: Use clear, brief language in descriptions
2. **Think Like a New User**: What would they want to find first?
3. **Descriptive Links**: Use meaningful link text, not "click here"
4. **Add Context**: Notes after colons help LLMs understand what each link contains
5. **Stable URLs**: Link to versioned or permanent documentation
6. **Progressive Detail**: Start with essentials, end with optional resources
7. **Test Comprehension**: Read it yourself - does it make sense quickly?
8. **Keep Updated**: Update as documentation structure evolves

## Output Format for llms.txt Generation

When generating an llms.txt file, provide:

1. **Analysis summary** - Project type, documentation structure, identified resources
2. **Generated llms.txt file** - Complete, properly formatted file
3. **File placement instructions** - Where to save it (repository root)
4. **URL update notes** - If using placeholder URLs that need updating
5. **Suggestions** - Additional documentation that could improve the file

Save the file as `llms.txt` in the project root directory.

## Integration with C7Score Optimization

llms.txt generation can be combined with c7score optimization:

1. **Optimize documentation first** - Improve README and docs for c7score
2. **Then generate llms.txt** - Create navigation file pointing to optimized docs
3. **Result**: High-quality documentation with LLM-friendly navigation

Or generate them independently based on user needs.

## Additional Resources

- Format specification: `references/llmstxt_format.md`
- Examples by project type: `examples/sample_llmstxt.md`
- Official specification: https://llmstxt.org/
- Real examples: https://llmstxt.site/
