---
name: powerpoint-generator
description: Generate professional PowerPoint presentations with slides, charts, and transitions. Use for executive presentations, reports, and visual communication.
allowed-tools: read, write, memory
version: 1.0
best_practices:
  - Use clear slide structure
  - Include visualizations from data
  - Apply consistent formatting
  - Keep slides focused and concise
error_handling: graceful
streaming: supported
---

# PowerPoint Generator Skill

## Identity

PowerPoint Generator - Creates professional PowerPoint presentations with slides, charts, and transitions using Claude's built-in `pptx` skill.

## Capabilities

- **Presentation Creation**: Generate multi-slide presentations
- **Charts and Visualizations**: Include charts and graphs
- **Formatting**: Apply professional formatting and styling
- **Transitions**: Add slide transitions and animations
- **Content Organization**: Structure content logically

## Usage

### Basic PowerPoint Generation

**When to Use**:

- Executive presentations
- Quarterly reports
- Project updates
- Training materials
- Visual communication

**How to Invoke**:

```
"Generate a PowerPoint presentation for Q4 results"
"Create an executive presentation from the financial data"
"Generate a project update presentation"
```

**What It Does**:

- Uses Claude's built-in `pptx` skill (skill_id: `pptx`)
- Creates PowerPoint presentations with multiple slides
- Includes charts, formatting, and transitions
- Returns file_id for download

### Advanced Features

**Multi-Slide Presentations**:

- Title slide
- Content slides
- Summary slides
- Appendix slides

**Charts and Visualizations**:

- Data visualizations from Excel
- Trend charts
- Comparison charts
- Process diagrams

**Formatting**:

- Professional templates
- Consistent styling
- Brand guidelines
- Visual hierarchy

## Best Practices

### Presentation Structure

**Recommended Approach**:

- **Clear slide structure**: Title, content, summary
- **Visual focus**: Use charts and diagrams
- **Consistent formatting**: Apply templates
- **Concise content**: Keep slides focused

**For Complex Presentations**:

1. **Create from data**: Use Excel data as source
2. **Visualize key insights**: Focus on important metrics
3. **Tell a story**: Logical flow and narrative
4. **Professional polish**: Consistent formatting

### Performance Tips

- **PowerPoint generation**: Very reliable for complex content
- **Chart integration**: Works well with Excel data
- **Batch operations**: Process multiple presentations
- **Template reuse**: Use consistent templates

## Integration

### With Excel Generator

PowerPoint can use Excel data:

- Import charts from Excel
- Reference data from spreadsheets
- Create visualizations from analysis

### With Artifact Publisher

PowerPoint files can be published as artifacts:

- Save to `.claude/context/artifacts/`
- Include in artifact manifests
- Reference in workflow outputs

### With Workflows

PowerPoint generation integrates with workflows:

- Reporting workflows
- Presentation workflows
- Communication workflows

## Examples

### Example 1: Executive Presentation

```
User: "Generate a PowerPoint presentation for Q4 results"

PowerPoint Generator:
1. Creates presentation with slides:
   - Title slide
   - Executive summary
   - Financial highlights
   - Key metrics
   - Trends and analysis
   - Next steps
2. Includes charts from Excel data
3. Applies professional formatting
4. Returns file_id for download
```

### Example 2: Project Update

```
User: "Create a project update presentation"

PowerPoint Generator:
1. Creates presentation with:
   - Project overview
   - Progress update
   - Milestones achieved
   - Challenges and solutions
   - Next steps
2. Includes visualizations
3. Applies project branding
```

### Example 3: Training Materials

```
User: "Generate training presentation"

PowerPoint Generator:
1. Creates educational presentation
2. Includes diagrams and examples
3. Structures content logically
4. Adds interactive elements
```

## Technical Details

### API Usage

Uses Claude's beta Skills API:

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    container={"type": "skills", "skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]},
    messages=[{"role": "user", "content": "Create PowerPoint presentation..."}]
)
```

### File Download

Files are returned as `file_id`:

```python
file_id = response.content[0].file_id
file_content = client.beta.files.content(file_id)
```

## Related Skills

- **excel-generator**: Create data for presentations
- **pdf-generator**: Convert PowerPoint to PDF
- **artifact-publisher**: Publish presentations as artifacts

## Related Documentation

- [Document Generation Guide](../docs/DOCUMENT_GENERATION.md) - Comprehensive guide
- [Skills Cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/skills) - Reference implementation
