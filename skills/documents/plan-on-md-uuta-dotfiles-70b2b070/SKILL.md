---
name: plan-on-md
description: A skill to save plans to local Markdown after creating them in plan mode
---

## TODO

- Store a plan in the Obsidian vault that has been made in advance

## Path

The path is composed of the following parts.

- ~/uuta/Projects/{project_name}/{branch_name}/{file_name}.md

### {project_name}

The project name is the name of directory that an agent work on. For example, if you work on the following path,

- ~/triceps

the project name become the following one.

- triceps

The important point is the suffix numeric number should be removed from the directory name.

- ~/triceps22

The above path becomes the following one.

- triceps

The reason is we occasionally clone GitHub projects with the gitwork tree. Avoiding duplicated directory names, we tend to add suffix number. Precisely, we can say a project name with a suffix number differs from the project without a suffix number, but those projects can be considered the same one.

### {branch_name}

Basically, the branch name should be regexed with the following pattern due to multiple reasons.

- xxx/#123 -> 123
  - xxx and / should be removed from the branch name since xxx is tedious and / means a directory.
  - `#` should be removed since when NeoVim tries to find a file, it doesn't work

The next examples are practical.

- hotfix/#123 -> 123
- feature/#123 -> 123

### {file_name}

The file name should be the summarized name based on a plan an agent created.

- handler-implementation-plan.md
- xx-method-refactor-plan.md

## Use-case

.e.g,

- path: ~/curry2
- branch_name: feature/#468
  - ~/uuta/Projects/curry/468/middleware-refactor-plan.md
