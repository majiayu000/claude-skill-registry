---
name: code-refactor-analyzer
description: Analyzes codebase for refactoring needs, generates todo reports, and validates completion
---

# Code Refactor Analyzer

This skill helps developers identify code that needs refactoring based on new requirements, generates actionable todo lists, and tracks completion progress.

## Capabilities

- **Requirement Analysis**: Understand user requirements and identify potential code impacts
- **Code Impact Analysis**: Analyze repository to find code lines that may be affected by the requirement
- **Todo Report Generation**: Create structured todo lists with specific code locations and tasks
- **Completion Validation**: Check if previously generated todo items have been completed
- **State Management**: Automatically detects if this is the first use (generate report) or subsequent use (check completion)

## Input Requirements

- **User Requirement**: Description of the new feature, change, or refactoring need
- **Repository Context**: Claude Code should have access to the codebase (via open repository)
- **Optional Parameters**:
  - Specific file paths to focus on
  - Priority levels for tasks
  - Deadline constraints

## Output Formats

- **First Use**: Generates a todo report file at `.claude/code_refactor_report/[requirement]-[date].md`
- **Subsequent Use**: Provides completion validation report showing:
  - Completed items (checked off)
  - Pending items
  - New items that may have been added
- **Interactive Guidance**: Step-by-step suggestions for refactoring

## How to Use

"Analyze the codebase for implementing user authentication and identify what needs to be refactored"
"Check if the todo items from yesterday's refactoring plan have been completed"
"Generate a refactoring plan for migrating from class-based components to functional components"

## Scripts

- `code_analyzer.py`: Main analysis engine that identifies impacted code
- `report_manager.py`: Handles todo report generation and completion validation
- `state_manager.py`: Manages skill state (first use vs subsequent use)

## Best Practices

1. **Clear Requirements**: Provide specific, detailed requirements for better analysis
2. **Repository Access**: Ensure Claude has access to the codebase before using this skill
3. **Incremental Refactoring**: Focus on small, manageable sections rather than entire codebase
4. **Regular Validation**: Use the completion check feature regularly to track progress
5. **Documentation**: Add comments to refactored code explaining the changes

## Limitations

- Requires Claude to have access to the repository files
- Analysis is based on code patterns and may not catch all edge cases
- Cannot automatically fix code - provides guidance only
- Works best with well-structured codebases
- May produce false positives for complex refactoring scenarios