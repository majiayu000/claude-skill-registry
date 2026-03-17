---
name: research-documentation
description: Research topics and document findings in Notion with organized structure and sources
---

## Overview

The Research Documentation skill automates the process of researching topics and capturing findings in a well-organized Notion database. It streamlines research by structuring information, tracking sources, and connecting related findings.

## When to Use

Use this skill when you need to:
- Research complex topics and document findings
- Compile competitive analysis or market research
- Create literature reviews or research summaries
- Build knowledge bases around specific topics
- Track sources and citations
- Organize research across multiple domains
- Create research reports with sourced information

## Features

- **Structured Research Capture**: Automatically organizes research findings with proper hierarchy
- **Source Tracking**: Maintains complete source attribution and citations
- **Topic Organization**: Categorizes findings by theme and relevance
- **Cross-referencing**: Connects related research across topics
- **Evidence Collection**: Captures quotes, data, and supporting evidence
- **Research Timeline**: Tracks how understanding evolved during research

## Requirements

- **Notion API Access**: For creating and updating research documentation
- **Research Database**: Notion database structure for organizing findings
- **Web Access**: For gathering information from online sources
- **Citation Format Preference**: Configured citation style (APA, MLA, Chicago, etc.)

## Implementation Details

This skill orchestrates research workflows by:

1. Breaking down research topics into focused areas
2. Gathering information from multiple sources
3. Analyzing and synthesizing findings
4. Organizing findings with proper attribution
5. Creating relationships between related research
6. Generating summary documents and reports

### Research Documentation Workflow

```
Research Topic/Question
  ↓
Break into Research Areas
  ↓
Gather Information
  ↓
Analyze & Synthesize
  ↓
Extract Key Findings
  ↓
Organize with Sources
  ↓
Create Notion Documentation
  ↓
Output: Research Summary
```

## Example Use Cases

1. **Competitive Analysis**
   - Research competitors and market landscape
   - Document features, pricing, and positioning
   - Create competitive comparison matrix

2. **Technology Evaluation**
   - Research framework/tool options
   - Document pros, cons, and use cases
   - Create evaluation report with recommendations

3. **Domain Knowledge Building**
   - Research industry best practices
   - Document standards and approaches
   - Create reference guide for team

4. **Literature Review**
   - Research academic papers on topic
   - Summarize findings and arguments
   - Create annotated bibliography

5. **Market Research**
   - Gather market size and trends
   - Document customer needs
   - Create market analysis report

## Configuration

```env
NOTION_API_TOKEN=your_token_here
RESEARCH_DATABASE_ID=your_database_id
SOURCES_DATABASE_ID=your_sources_database_id
CITATION_FORMAT=APA
```

## Citation Formats Supported

- APA
- MLA
- Chicago Style
- Harvard
- IEEE

## See Also

- [Knowledge Capture](/skills/knowledge-capture) - For documenting discussions and insights
- [Meeting Intelligence](/skills/meeting-intelligence) - For research-informed meeting prep
- [Spec to Implementation](/skills/spec-to-implementation) - For research-based implementation planning
- [Notion API Documentation](https://developers.notion.com)
