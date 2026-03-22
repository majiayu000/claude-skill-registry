---
name: template-skill
description: Template for creating new skills in gptme-contrib. Use this as a starting point when creating your own skills.
---

# Template Skill

This is a minimal skill template demonstrating the basic structure of a gptme skill.

## Overview

Skills are enhanced lessons that bundle:
- Instructional content (like lessons)
- Executable scripts and utilities (optional)
- Dependencies and setup requirements (optional)
- Hook points for automation (optional)

## Basic Structure

Every skill needs:
1. **SKILL.md** - This file with YAML frontmatter + Markdown content
2. **Supporting files** (optional) - Scripts, templates, or resources

## YAML Frontmatter

Required fields:
- `type: skill` - Distinguishes from lessons
- `name: skill-name` - Skill identifier (must match directory name)
- `description: ...` - What the skill does and when to use it
- `status: active` - active, automated, deprecated, or archived
- `match: {keywords: [...]}` - Trigger keywords

Optional fields:
- `scripts: []` - List of bundled Python scripts
- `dependencies: []` - Required Python packages
- `hooks: []` - Execution hooks (future feature)

## Markdown Content

The markdown body can include:
- Detailed instructions for the LLM
- Step-by-step workflows
- Code examples and templates
- Best practices and principles
- References to supporting files

## Creating Your Own Skill

1. Copy this template-skill directory
2. Rename to your-skill-name
3. Update SKILL.md frontmatter (especially name and description)
4. Write your skill instructions in markdown
5. Add any supporting scripts or resources
6. Test with gptme

## Example: Minimal Skill

```yaml
---
type: skill
name: my-skill
description: Brief description of what the skill does
status: active
match:
  keywords: [keyword1, keyword2]
scripts: []
dependencies: []
---

# My Skill

Instructions for using this skill...
```

## Example: Skill with Scripts

```yaml
---
type: skill
name: data-analysis
description: Data analysis workflows with pandas and visualization
status: active
match:
  keywords: [data analysis, pandas, visualization]
scripts:
  - helpers.py
  - plot_utils.py
dependencies:
  - pandas
  - matplotlib
---

# Data Analysis Skill

Use this skill for data analysis tasks...

## Bundled Scripts

- `helpers.py`: Common data manipulation functions
- `plot_utils.py`: Visualization utilities

## Usage

```python
# Import bundled helpers
from helpers import load_data, clean_data
from plot_utils import plot_distribution

# Analyze data
df = load_data("data.csv")
df = clean_data(df)
plot_distribution(df["column"])
```
```

## Integration with Lessons

Skills complement lessons:
- **Lessons**: Behavioral patterns and best practices (auto-included)
- **Skills**: Executable workflows with bundled tools (explicitly loaded)

Example:
- Lesson teaches: "Use type hints in Python"
- Skill provides: Type checking utilities and templates

## Related

- [Skills README](../README.md) - Skills system overview
