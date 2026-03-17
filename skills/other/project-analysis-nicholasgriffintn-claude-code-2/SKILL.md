---
name: project-analysis
description: A specialist skill that analyses a codebase to understand its structure, dependencies, and architecture. This skill should be used at the start of a new project or when onboarding to an existing codebase.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Project Analysis Skill

## Tooling Notes

This skill should only use read-only commands and avoid modifying files.

## Analysis Process

Copy this checklist and use it to track your progress through the analysis process:

```markdown
Project Analysis Checklist

- [ ] Gather a quick overview of the project by reading the README.md or equivalent documentation.
- [ ] Identify the main programming languages and frameworks used in the codebase.
- [ ] Map out the project structure, including key directories and files.
- [ ] Analyze dependencies by reviewing package management files (e.g., package.json, requirements.txt).
- [ ] Identify core modules and components of the application.
- [ ] Understand the data flow and architecture patterns used in the project.
- [ ] Review any existing tests to understand the testing strategy and coverage.
- [ ] Document any areas of the codebase that may require further investigation or clarification.
```

## Analysis Commands

Here are some useful commands to help you analyze the codebase:

```bash
# List the main files and directories in the project
ls -R

# Check for package management files to identify dependencies
ls | grep -E 'package\.json|requirements\.txt|Pipfile|Gemfile'

# Display the contents of a package management file
cat package.json
cat requirements.txt

# Search for key architecture patterns or components
grep -r 'MVC\|Microservices\|Singleton\|Factory' .

# Identify test files and directories
find . -type f -name '*test*' -o -name '*spec*'
```

## Documentation of Findings

After completing the analysis, document your findings in a structured format. Include sections such as:

- **Project Overview**: A brief summary of the project, its purpose, and main features.
- **Technologies Used**: A list of programming languages, frameworks, and libraries used in the project.
- **Project Structure**: An outline of the key directories and files in the codebase.
- **Dependencies**: A summary of the main dependencies and their roles in the project.
- **Core Components**: A description of the main modules and components of the application.
- **Architecture Patterns**: An overview of the architecture patterns and data flow used in the project.
- **Testing Strategy**: A summary of the existing tests and their coverage.
