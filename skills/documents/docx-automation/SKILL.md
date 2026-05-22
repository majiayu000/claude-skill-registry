---
name: docx-automation
description: |
  Generate DOCX documents from pipeline results or structured data.
  Uses python-docx library for Word document generation.
  Independent utility skill (can be called standalone or post-pipeline).
user-invocable: true
context: fork
model: opus
version: "3.1.0"
argument-hint: "generate <source> | from-json <data.json> | report <image_id> | --workload <slug>"
allowed-tools:
  - Read
  - Bash
  - Write
  - Task
  - mcp__sequential-thinking__sequentialthinking
hooks:
  Setup:
    - type: command
      command: "source /home/palantir/.claude/skills/shared/workload-files.sh"
      timeout: 5000

# EFL Pattern Configuration (Utility Skill - Minimal)
agent_delegation:
  enabled: false
  reason: "Utility skill - direct execution for document generation"

parallel_agent_config:
  enabled: false
  reason: "Sequential document generation preferred for consistency"

internal_validation:
  enabled: true
  checks:
    - "Source data is readable and valid"
    - "python-docx library is installed"
    - "Output directory is writable"
  max_retries: 2

output_paths:
  l1: ".agent/prompts/{slug}/docx-automation/l1_summary.yaml"
  l2: ".agent/prompts/{slug}/docx-automation/l2_index.md"
---

# /docx-automation - DOCX Document Generation

> **Version:** 3.1.0 | **Type:** Independent Utility Skill
> **Role:** Generate Word documents from pipeline results or data
> **Pipeline:** Standalone or post-pipeline utility

## 1. Purpose

Generate Microsoft Word documents from:
- Pipeline export results (mathpix_pipeline)
- Structured data (JSON/YAML/Dict)
- Template-based reports

## 2. Prerequisites

```bash
pip install python-docx>=0.8.11
```

## 3. Invocation

```bash
# Generate from pipeline results
/docx-automation generate <source_file> [--output <output.docx>]

# Convert JSON to DOCX
/docx-automation from-json <data.json> --output report.docx

# Generate report from pipeline data
/docx-automation report <image_id> --format detailed

# With workload context
/docx-automation generate synthesis-report --workload <slug>
```

## 4. L1/L2/L3 Output Format

### L1 Summary (returned to main context)

```yaml
taskId: docx-{timestamp}
agentType: docx-automation
status: success
summary: "Generated report.docx (125KB)"

filePath: ".agent/prompts/{slug}/docx/report.docx"
fileSize: 128000
pageCount: 5

l2Path: .agent/prompts/{slug}/docx-automation/l2_index.md
requiresL2Read: false
nextActionHint: "Document at {filePath}"
```

### L2 Report Structure

```markdown
# DOCX Generation Summary

## Document Info
- **Output:** report.docx
- **Size:** 125 KB
- **Pages:** 5

## Content Structure
1. Title Section
2. Content (equations, graphs)
3. Metadata
4. Provenance

## Generation Details
- Font: Times New Roman, 11pt
- Margins: 1 inch
- Header/Footer: Enabled
```

## 5. Actions

### generate
Generate DOCX from pipeline results.

```bash
/docx-automation generate <source_file> [--output <output.docx>] [--config <config.yaml>]
```

### from-json
Convert structured JSON to formatted DOCX.

```bash
/docx-automation from-json <data.json> --output <output.docx> [--template <template>]
```

### report
Generate detailed report from pipeline results.

```bash
/docx-automation report <image_id> --format <summary|detailed|full> [--include-images]
```

## 6. Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| output_dir | Path | ./exports | Output directory |
| page_width_inches | float | 8.5 | Page width |
| page_height_inches | float | 11.0 | Page height |
| margin_inches | float | 1.0 | Page margins |
| font_name | str | Times New Roman | Body font |
| font_size_pt | int | 11 | Body font size |
| heading_font_name | str | Arial | Heading font |
| include_toc | bool | false | Table of contents |
| include_header | bool | true | Document header |
| include_footer | bool | true | Page numbers |

## 7. Programmatic Usage

```python
from mathpix_pipeline.export.exporters.docx_exporter import (
    DOCXExporter,
    DOCXExporterConfig,
)
from mathpix_pipeline.schemas.export import ExportOptions

# Initialize with custom config
config = DOCXExporterConfig(
    output_dir=Path("./exports"),
    font_name="Arial",
    font_size_pt=12,
)
exporter = DOCXExporter(config)

# Export
options = ExportOptions(include_metadata=True)
spec = exporter.export(data, options, image_id="img_001")
print(f"Exported to: {spec.file_path}")
```

## 8. Output Structure

Generated DOCX documents include:

1. **Title Section** - Document title, center-aligned
2. **Content Section** - Outputs, graphs, equations
3. **Metadata Section** (optional) - Generation timestamp, attributes
4. **Provenance Section** (optional) - Pipeline version, stages

## 9. Error Handling

```python
try:
    spec = exporter.export(data, options, image_id)
except ImportError:
    print("Install python-docx: pip install python-docx")
except ExporterError as e:
    print(f"Export error: {e.message}")
```

## 10. Pipeline Integration

```
[Independent Utility]
    |
/docx-automation ---- Can be called standalone
    |
    +-- Output: .agent/prompts/{slug}/docx/{filename}.docx
```

### Workload Context Resolution

```bash
# Priority:
# 1. --workload argument
# 2. Active workload (_active_workload.yaml)
# 3. New workload (document type based)
```

## 11. Handoff Contract

```yaml
handoff:
  skill: "docx-automation"
  workload_slug: "{slug}"
  status: "completed"
  next_action:
    skill: null
    arguments: null
    required: false
    reason: "Document generated successfully"
  output:
    path: ".agent/prompts/{slug}/docx/{filename}.docx"
    format: "docx"
```

## 12. Post-Compact Recovery

```javascript
if (isPostCompactSession()) {
  const slug = await getActiveWorkload();
  if (slug) {
    const exportDir = `.agent/prompts/${slug}/docx/`;
    const partialFiles = await Glob(`${exportDir}/*.partial`);
    if (partialFiles.length > 0) {
      console.log("Resuming partial document generation...");
    }
  }
}
```

---

### Version History

| Version | Change |
|---------|--------|
| 3.1.0 | Cleaned duplicate blocks, normalized frontmatter |
| 3.0.0 | EFL Pattern integration, context: fork |
| 2.2.0 | Standalone execution, handoff contract |
| 2.1.0 | V2.1.19 spec compatibility |
| 1.1.1 | Initial DOCX generation |
