---
name: slim-executive-summary
description: Generate comprehensive executive summaries from workspace communication files using AI analysis with automatic context discovery
dependencies:
  skills:
    - slim-project-aware-workspace
---

# Executive Summary Writer

Generate comprehensive executive summaries from communication and project files using AI analysis with automatic workspace integration.

## Prerequisites

This skill requires the **[SLIM Project-Aware Workspace](../slim-project-aware-workspace/SKILL.md)** to be set up first. The workspace provides:
- **static/** folder with project context (PROJECT.md, TEAM.md, PRODUCTS.md, MEETINGS.md, TECH.md)
- **dynamic/** folder with date-organized subfolders (YYYY-MM-DD format) containing communication files

## Usage

This skill automatically discovers project context from your workspace and generates executive summaries from communication files.

Simply invoke this skill and provide:
1. Which date folder (YYYY-MM-DD) within the `dynamic/` directory to analyze
2. Optional project name and custom focus areas

The skill will:
- Automatically locate your workspace by finding the `static/` and `dynamic/` folders
- Read project context from the `static/` folder
- Scan and analyze files in the specified date folder
- Generate a comprehensive executive summary
- Save the output to `executive-summary.md` in the same date folder

## What This Skill Does

1. **Workspace Discovery**: Automatically locates your AI task workspace (by finding `static/` and `dynamic/` folders)
2. **Context Loading**: Reads project context from `static/` folder (PROJECT.md, TEAM.md, PRODUCTS.md, etc.)
3. **Date Folder Selection**: Prompts you to specify which date folder to analyze (e.g., `2024-12-15`)
4. **File Scanning**: Recursively reads all relevant communication files in the specified date folder
5. **Enhanced Analysis**: Uses AI to analyze content with full project context
6. **Pattern Recognition**: Identifies key themes, issues, accomplishments, and action items
7. **Intelligent Synthesis**: Combines information from multiple sources using project context
8. **Executive Summary**: Generates a structured summary and saves it to the date folder

## File Types Supported

### Communication Files (in dynamic/ date folders)
- **Markdown files** (.md): Meeting notes, documentation, reports
- **JSON files** (.json): Slack exports, GitHub API responses, email data
- **Text files** (.txt): Email exports, plain text notes, communication logs
- **CSV files** (.csv): Issue tracking exports, metrics data

### Context Files (in static/ folder)
- **PROJECT.md**: Project overview, components, tech stack, repositories
- **TEAM.md**: Team structure, roles, leadership, contact information
- **PRODUCTS.md**: Product types, specifications, technical details
- **MEETINGS.md**: Meeting schedules, cadence, communication channels
- **TECH.md**: Technology stack, tool integrations (MCP servers, APIs, scripts)

## Output Format

The skill generates a comprehensive executive summary using a standardized template that ensures consistency across all summaries. The template includes:

- **Executive Overview**: 2-3 paragraph summary of key developments
- **Issues**: Critical and other issues with status indicators
- **Key Accomplishments**: Organized by category with decisions made
- **Action Items**: Prioritized by urgency with owners and due dates
- **Themes & Patterns**: Cross-cutting observations across all activity
- **Team Activity**: Contributors, collaborations, and team dynamics
- **Metrics**: Quantified activity levels and completion rates
- **Looking Ahead**: Future priorities based on current patterns

**Template Reference**: [executive-summary-template.md](assets/executive-summary-template.md)

The AI will read this template file and use it as the exact structure for generating your executive summary, ensuring consistent formatting and complete coverage of all sections.

## Example Usage

**Example 1: Generate summary from a specific date**
```
Generate an executive summary from the 2024-12-15 folder
```

**Example 2: With project name**
```
Create an executive summary for the "Alpha Release Project" from the 2025-01-05 folder
```

**Example 3: With specific focus**
```
Generate an executive summary from the 2024-11-20 folder, focusing on security issues and deployment status
```

## Workflow

1. **Invoke the skill** with your date folder reference
2. **Skill locates workspace** automatically (finds `static/` and `dynamic/` folders)
3. **Skill asks for confirmation** of the date folder to analyze
4. **Skill loads project context** from `static/` folder files
5. **Skill reads template** from [executive-summary-template.md](assets/executive-summary-template.md) for consistent formatting
6. **Skill scans communication files** in the specified `dynamic/YYYY-MM-DD/` folder
7. **Skill generates summary** with enriched context and insights following the template structure
8. **Output saved** as `executive-summary.md` in the same date folder

## Benefits of Workspace Integration

- **No manual path specification**: Automatically finds your workspace structure
- **Rich context**: Uses project knowledge from `static/` folder for better analysis
- **Name mapping**: Translates GitHub usernames to real names using TEAM.md
- **Technical understanding**: Recognizes product names and tech stack from PROJECT.md/PRODUCTS.md
- **Team dynamics**: Understands roles and collaborations from TEAM.md
- **Organized output**: Saves summary in the same date folder as input files
- **Consistent structure**: Follows workspace date organization (YYYY-MM-DD)

## AI Instructions

When this skill is invoked, follow these steps:

1. **Locate Workspace**: Search for directories containing both `static/` and `dynamic/` folders
2. **List Date Folders**: Show available date folders in `dynamic/` and ask user which to analyze
3. **Load Context**: Read all files from `static/` folder (PROJECT.md, TEAM.md, PRODUCTS.md, MEETINGS.md, TECH.md)
4. **Read Template**: Load the template structure from [executive-summary-template.md](assets/executive-summary-template.md)
5. **Scan Input Files**: Find and read all communication files in the specified `dynamic/YYYY-MM-DD/` folder
6. **Analyze Content**: Extract issues, accomplishments, action items, themes, team activity, and metrics
7. **Generate Summary**: Fill in the template with analyzed content, using project context for enrichment
8. **Save Output**: Write to `dynamic/YYYY-MM-DD/executive-summary.md`

**Key Guidelines:**
- Use the template structure exactly as provided in executive-summary-template.md
- Leverage static context to map usernames to real names (TEAM.md)
- Understand technical terms using project knowledge (PROJECT.md, PRODUCTS.md)
- Consolidate duplicate items mentioned across multiple sources
- Prioritize by business impact: Critical → High → Medium → Low
- Use emojis consistently: 🚨 (critical), 🔄 (in progress), ⚠️ (warning), 🔍 (investigating), ✅ (complete)
- Write at executive level - entire summary should be scannable in 2-3 minutes

## Integration

Works seamlessly with:
- Slack history exports saved to date folders
- GitHub activity reports and issue exports
- Meeting notes from specific dates
- Email thread summaries and communication logs
- Project tracking data and metrics files
- Any communication files organized by date in your workspace

## Resources

- **[executive-summary-template.md](assets/executive-summary-template.md)**: Standard template structure that must be read and followed for every summary generation
