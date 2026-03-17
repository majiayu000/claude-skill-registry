---
name: skill-document-converter
description: Document conversion routing with dual invocation support
allowed-tools: Task
---

# Document Converter Skill

Thin wrapper that delegates document conversion to `document-converter-agent` subagent.

## Context Pointers

Reference (do not load eagerly):
- Path: `.claude/context/core/formats/subagent-return.md`
- Purpose: Return validation
- Load at: Subagent execution only

Note: This skill is a thin wrapper. Context is loaded by the delegated agent, not this skill.

## Trigger Conditions

This skill activates when:

### Direct Invocation
- User explicitly runs `/convert` command
- User requests file format conversion in conversation

### Implicit Invocation (during task implementation)

When an implementing agent encounters any of these patterns:

**Plan step language patterns**:
- "Extract text from [file].pdf"
- "Extract content from [file]"
- "Convert [file] to markdown"
- "Convert [file] to PDF"
- "Generate PDF from [documentation/file]"
- "Read content from [file].docx"
- "Create PDF version of [file]"
- "Parse [file].pdf for content"
- "Import [file] content"

**File extension detection**:
- Source file has extension: `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.html`
- Target mentions: "markdown", ".md", "PDF", ".pdf"

**Task description keywords**:
- "document conversion"
- "format transformation"
- "extract from PDF"
- "generate PDF"

### When NOT to trigger

Do not invoke for:
- Reading source code files (.py, .js, .lean, etc.)
- Viewing images without extraction
- Operations that don't involve format conversion
- Files already in the target format

---

## Execution

### 1. Input Validation

Validate required inputs:
- `source_path` - Must be provided and file must exist
- `output_path` - Optional, defaults to source dir with appropriate extension

```bash
# Validate source exists
if [ ! -f "$source_path" ]; then
  return error "Source file not found: $source_path"
fi

# Determine output path if not provided
if [ -z "$output_path" ]; then
  source_dir=$(dirname "$source_path")
  source_base=$(basename "$source_path" | sed 's/\.[^.]*$//')
  source_ext="${source_path##*.}"

  # Infer target extension
  case "$source_ext" in
    pdf|docx|xlsx|pptx|html) output_path="${source_dir}/${source_base}.md" ;;
    md) output_path="${source_dir}/${source_base}.pdf" ;;
    *) return error "Cannot infer output format for .$source_ext" ;;
  esac
fi
```

### 2. Context Preparation

Prepare delegation context:

```json
{
  "source_path": "/absolute/path/to/source.pdf",
  "output_path": "/absolute/path/to/output.md",
  "metadata": {
    "session_id": "sess_{timestamp}_{random}",
    "delegation_depth": 1,
    "delegation_path": ["orchestrator", "convert", "skill-document-converter"]
  }
}
```

### 3. Invoke Subagent

**CRITICAL**: You MUST use the **Task** tool to spawn the subagent.

The `agent` field in this skill's frontmatter specifies the target: `document-converter-agent`

**Required Tool Invocation**:
```
Tool: Task (NOT Skill)
Parameters:
  - subagent_type: "document-converter-agent"
  - prompt: [Include source_path, output_path, metadata]
  - description: "Convert {source_path} to {output_path}"
```

**DO NOT** use `Skill(document-converter-agent)` - this will FAIL.
Agents live in `.claude/agents/`, not `.claude/skills/`.
The Skill tool can only invoke skills from `.claude/skills/`.

The subagent will:
- Detect available conversion tools
- Determine conversion direction from file extensions
- Execute conversion with appropriate tool
- Validate output exists and is non-empty
- Return standardized JSON result

### 4. Return Validation

Validate return matches `subagent-return.md` schema:
- Status is one of: converted, extracted, partial, failed
- Summary is non-empty and <100 tokens
- Artifacts array present with output file path
- Metadata contains session_id, agent_type, delegation info

### 5. Return Propagation

Return validated result to caller without modification.

---

## Return Format

See `.claude/context/core/formats/subagent-return.md` for full specification.

Expected successful return:
```json
{
  "status": "converted",
  "summary": "Successfully converted document.pdf to document.md using markitdown",
  "artifacts": [
    {
      "type": "implementation",
      "path": "/absolute/path/to/document.md",
      "summary": "Converted markdown document"
    }
  ],
  "metadata": {
    "session_id": "sess_...",
    "agent_type": "document-converter-agent",
    "delegation_depth": 1,
    "delegation_path": ["orchestrator", "convert", "skill-document-converter", "document-converter-agent"],
    "tool_used": "markitdown"
  },
  "next_steps": "Review converted document"
}
```

---

## Error Handling

### Input Validation Errors
Return immediately with failed status if source file not found.

### Unsupported Format
Return failed status with clear message about supported formats.

### Subagent Errors
Pass through the subagent's error return verbatim.

### Tool Not Available
Return failed status with installation instructions.
