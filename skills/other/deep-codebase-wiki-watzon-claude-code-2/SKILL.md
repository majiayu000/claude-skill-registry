---
name: deep-codebase-wiki
description: |
  MUST CHECK FIRST before DeepWiki or any external research. Local-first codebase documentation wikis.
  
  **Priority order for library/framework research**:
  1. deep-codebase-wiki (THIS) - check local wikis FIRST
  2. DeepWiki - only if no local wiki exists
  3. librarian/explore agents - only as fallback
  
  **Auto-trigger when**:
  - Any GitHub repository mentioned (org/repo format)
  - "How does X work?" about libraries/frameworks
  - Architecture, implementation, or codebase questions
  - Before cloning or analyzing any repository
  - Debugging external dependencies
  
  **Workflow**: Run `search_wikis.sh --repo "owner/repo"` first. If wiki exists, read it. If not, offer to analyze and create wiki (saves hours vs repeated agent searches).
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, LSP, ASTGrep
---

# Deep Codebase Wiki

## ⚡ PROACTIVE CHECK PROTOCOL (CRITICAL)

**BEFORE** any repository research, exploration, or analysis:

```bash
# ALWAYS run this first when a repository is mentioned
bash scripts/search_wikis.sh --repo "owner/repo"
```

**If wiki exists** → Read it immediately, save hours of exploration  
**If wiki doesn't exist** → Offer to analyze and create comprehensive wiki

**Common triggers requiring this check**:
- User mentions any GitHub repo (e.g., "facebook/react", "vercel/next.js")
- Questions like "How does X work?" about known libraries/frameworks
- "Understand the architecture of..."
- "Explain how [library] implements..."
- Before launching multiple explore/librarian agents
- When debugging external dependencies
- Architecture or implementation questions

**Why this matters**: A 2-hour comprehensive wiki beats 10 parallel agent searches that rediscover the same information every time.

---

## Overview

This skill enables creation, reading, and updating of comprehensive codebase documentation wikis. It analyzes GitHub repositories to generate structured, searchable documentation similar to DeepWiki and Zread services, but running entirely locally with full customization.

## Quick Start

This skill operates in three modes with a **mandatory check-first workflow**:

### Decision Flowchart

```
Repository mentioned
        ↓
Run: search_wikis.sh --repo "owner/repo"
        ↓
    ┌───┴───┐
    ↓       ↓
 Found    Not Found
    ↓       ↓
  READ     OFFER TO ANALYZE
  MODE     → User confirms
    ↓           ↓
 Present    ANALYZE MODE
  docs     (2-8 hours)
             ↓
          Save wiki
             ↓
          READ MODE
```

### Mode 1: Read Mode (Search Existing Wikis)

**Trigger**: Wiki found in index  
**Duration**: Seconds to minutes  
**Action**: Load and present relevant documentation

**Usage pattern**:
```bash
# Check for wiki
WIKI_PATH=$(bash scripts/search_wikis.sh --repo "facebook/react")

# If found, read relevant sections
if [[ -n "$WIKI_PATH" ]]; then
  # Read overview
  cat "$WIKI_PATH/overview.md"
  
  # Read specific system if user asked about it
  cat "$WIKI_PATH/systems/reconciliation.md"
fi
```

### Mode 2: Analyze Mode (Create New Wiki)

**Trigger**: Wiki not found, user needs understanding  
**Duration**: 2-8 hours depending on depth  
**Action**: Clone, analyze, document, save

**ALWAYS ask user first**:
> "I don't have a wiki for {repo} yet. Would you like me to analyze it? This will take approximately {estimated_time} and create comprehensive local documentation. Depth options: quick (1-2hr), standard (3-5hr), comprehensive (5-8hr)."

### Mode 3: Update Mode (Refresh Documentation)

**Trigger**: Wiki exists but may be outdated  
**Duration**: 1-4 hours  
**Action**: Check staleness, re-analyze if needed

**Check staleness**:
```bash
bash scripts/update_check.sh "$WIKI_PATH"
# Returns: up_to_date | partial_update | full_reanalysis
```

## Analyze Mode (Create New Wiki)

### Step 1: Determine Repository and Scope

Extract from user's request:
- **Repository**: Owner and repo name (e.g., "facebook/react")
- **Focus areas**: Specific systems or features of interest
- **Depth**: Quick overview vs comprehensive analysis

Examples:
- "Analyze the React repository" → Full analysis
- "How does Next.js routing work?" → Focus on routing system
- "Understand Supabase auth implementation" → Focus on auth module

### Step 2: Check for Existing Wiki

Search for existing wiki before creating new one:

```bash
bash scripts/search_wikis.sh --repo "owner/repo"
```

If found with recent timestamp (< 30 days old), suggest using Read Mode instead.

### Step 3: Clone Repository

Clone the repository locally for analysis:

```bash
bash scripts/clone_repo.sh "owner/repo" [--depth 1] [--branch main]
```

Options:
- `--depth 1`: Shallow clone for faster analysis (default)
- `--branch <name>`: Specific branch to analyze

Repository cloned to: `/tmp/wiki-analysis/owner-repo/`

### Step 4: Perform Multi-Level Analysis

Analyze the codebase systematically:

**Level 1: Repository Overview**
1. Identify primary language(s) using Glob
2. Locate entry points (main.py, index.js, package.json, etc.)
3. Map directory structure
4. Read README, CONTRIBUTING, and core docs
5. Identify frameworks and major dependencies

**Level 2: System Architecture**
1. Identify major systems/modules (auth, database, API, UI, etc.)
2. Map system boundaries and responsibilities
3. Document key design patterns
4. Identify external dependencies and integrations

**Level 3: Component Analysis**
1. Map important classes, functions, and modules
2. Document component responsibilities
3. Identify relationships and dependencies
4. Note configuration and environment setup

**Level 4: Trace Flows**
1. Trace common user journeys (e.g., login flow, API request)
2. Document data transformation pipelines
3. Map error handling paths
4. Identify security-critical code paths

Use LSP tools for accurate type information, AST-grep for pattern discovery, and Grep for searching relevant code.

### Step 5: Generate Wiki Structure

Create wiki following the schema in `references/wiki-schema.md`:

**Directory Structure:**
```
.claude/wikis/<org>-<repo>/
├── metadata.yaml          # Repo info, analysis metadata
├── overview.md            # High-level summary
├── systems/               # Major system docs
│   ├── authentication.md
│   ├── data-layer.md
│   ├── api-routing.md
│   └── ...
├── components/            # Component-level docs
│   └── ...
└── traces/                # User journey traces
    └── ...
```

Use templates from `assets/wiki-template/` as starting point.

**Content Guidelines:**
- **Accuracy**: Verify all file paths and line numbers
- **Completeness**: Cover all systems in scope
- **Clarity**: Use descriptive headings and examples
- **Cross-references**: Link related systems and components
- **Code snippets**: Include relevant code examples with file paths

### Step 6: Validate and Save

Validate wiki structure:

```bash
bash scripts/validate_wiki.sh /path/to/wiki
```

Register wiki in index and save to `.claude/wikis/<org>-<repo>/`:

```bash
bash scripts/search_wikis.sh --add "<org>-<repo>" "owner/repo" "/path/to/wiki" "<commit-sha>"
```

Save to `.claude/wikis/<org>-<repo>/` with proper metadata.

### Step 7: Present Summary

Provide user with:
1. Wiki location
2. Analysis scope and coverage
3. Key systems identified
4. Notable findings or concerns
5. Recommendations for deep dives

## Read Mode (Search Existing Wikis)

### Step 1: Locate Relevant Wiki

Find appropriate wiki using search:

**By Repository:**
```bash
bash scripts/search_wikis.sh --repo "owner/repo"
```

**By Query (Keyword Search):**
```bash
bash scripts/search_wikis.sh --query "authentication"
```

**List All Wikis:**
```bash
bash scripts/search_wikis.sh --list
```

### Step 2: Load and Analyze Wiki

Read relevant wiki sections:

1. **Check metadata** for freshness and scope
2. **Read overview** for high-level context
3. **Navigate to relevant systems** based on query
4. **Follow cross-references** for related information
5. **Review traces** for flow understanding

### Step 3: Present Findings

Structure response based on wiki content:

1. **Overview**: High-level summary of system/feature
2. **Architecture**: Key components and their roles
3. **Code Locations**: Files and line numbers for navigation
4. **Flows**: Data/process flows relevant to query
5. **Considerations**: Security, performance, or edge cases
6. **Next Steps**: Recommendations for further investigation

## Update Mode (Refresh Documentation)

### Step 1: Check if Update Needed

```bash
bash scripts/update_check.sh ".claude/wikis/org-repo" [branch]
```

Returns:
- Last analysis timestamp
- Current commit SHA vs analyzed commit
- Number of changed files since analysis
- Recommendation: full re-analysis vs partial update

### Step 2: Determine Update Scope

**Full Re-analysis** (if):
- Major refactoring detected
- > 30% of files changed
- Core systems modified
- > 90 days since last analysis

**Partial Update** (if):
- Minor changes to specific systems
- New features added to existing modules
- Documentation updates

### Step 3: Perform Update

**Full Re-analysis:**
- Follow Analyze Mode steps
- Preserve user annotations from old wiki
- Highlight what changed since last analysis

**Partial Update:**
- Re-analyze only changed systems
- Update affected traces
- Preserve unchanged sections
- Update metadata with partial update timestamp

### Step 4: Validate and Save

Run validation and save updated wiki with change summary in metadata.

## Implementation Guidelines

### Analysis Depth Control

Adjust analysis depth based on repository size:

- **Small (<100 files)**: Full comprehensive analysis
- **Medium (100-1000 files)**: Focus on core systems
- **Large (>1000 files)**: Scope to specific modules or user-requested areas

### Quality Standards

- **Accuracy**: All paths, line numbers, and code references must be current
- **Completeness**: Cover all major systems in scope
- **Navigability**: Clear cross-references and table of contents
- **Maintainability**: Document assumptions and limitations in metadata
- **Searchability**: Use consistent terminology and tags

### Performance Optimization

- Use shallow clones (`--depth 1`) for faster analysis
- Leverage LSP for type information (faster than AST parsing)
- Parallelize independent system analysis when possible
- Cache dependency graphs and import maps

## Resources

### scripts/
- `clone_repo.sh` - Clone GitHub repository for analysis
- `search_wikis.sh` - Search existing wikis by repo or query (uses jq + JSON index)
- `validate_wiki.sh` - Validate wiki structure against schema
- `update_check.sh` - Check if wiki needs refresh

**Dependencies**: `jq` for JSON processing (install: `brew install jq` on macOS)

### references/
- `wiki-schema.md` - Complete wiki schema with examples
- `analysis-guide.md` - Detailed analysis methodology

### assets/
- `wiki-template/` - Directory structure template
- `system-template.md` - Template for system documentation
- `component-template.md` - Template for component docs
- `trace-template.md` - Template for flow traces

## Usage Examples

**Example 1 - Analyze New Repository:**
```
User: "Analyze the Supabase repository, focusing on authentication"
→ Clone supabase/supabase
→ Perform focused analysis on auth system
→ Generate wiki with comprehensive auth documentation
→ Present summary with key findings
```

**Example 2 - Read Existing Wiki:**
```
User: "How does Next.js handle API routes?"
→ Search for Next.js wiki
→ Navigate to API routing system docs
→ Extract routing flow and code locations
→ Present structured explanation
```

**Example 3 - Update Outdated Wiki:**
```
User: "Update my React wiki, it's 6 months old"
→ Check what changed in React repo
→ Determine full re-analysis needed
→ Perform fresh analysis preserving annotations
→ Highlight changes since last analysis
```

## Integration with Agent Workflow

### Priority Order for Repository Understanding

When user asks about external repositories or libraries:

**1. Check deep-codebase-wiki FIRST** (this skill)
```bash
bash scripts/search_wikis.sh --repo "owner/repo"
```
If wiki exists → Use it, skip steps 2-4

**2. Check use-codemap** (for lightweight maps)
Only if wiki doesn't exist and user needs quick overview

**3. Launch background agents** (if no local docs exist)
- explore agents for codebase patterns
- librarian agents for official docs

**4. Manual exploration** (last resort)
- Clone and analyze from scratch
- Offer to create wiki for future use

### Integration with Other Skills

This skill complements:
- **use-codemap**: For focused, lightweight architecture maps (codemaps are quick, wikis are comprehensive)
- **crystal-lang**: When analyzing Crystal projects, combine with language-specific knowledge
- When both exist for same codebase, prefer wikis for comprehensive reference, codemaps for specific investigations

### Example: User Asks "How does Next.js routing work?"

**WRONG workflow** (wasteful):
```
1. Launch 3 explore agents to search Next.js codebase
2. Launch 2 librarian agents for docs
3. Manually grep through cloned repo
4. Spend 30 minutes rediscovering information
```

**CORRECT workflow** (efficient):
```
1. Check wiki: search_wikis.sh --repo "vercel/next.js"
2. If found → Read systems/routing.md (30 seconds)
3. If not found → Ask user: "Analyze Next.js? (~4hrs for comprehensive wiki)"
4. Only if user declines → Fall back to agent exploration
```
