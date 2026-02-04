---
name: git-performance-issue-investigator
description: When the user needs to investigate performance issues in a Git repository by finding specific code changes, identifying responsible commits, and contacting authors. This skill is triggered by requests involving finding commits containing specific variables or code patterns, identifying earliest/introducing commits, extracting author information (name, email), and communicating about performance issues. It provides capabilities for searching Git history for specific code patterns using git log -S, retrieving full commit details with git show, extracting author metadata, and generating formatted communications using templates.
---
# Instructions

## Overview
This skill investigates performance issues in Git repositories by tracing code changes to specific commits, identifying responsible authors, and generating communications.

## Core Workflow

### 1. Initialize Investigation
- Identify the target Git repository path in the workspace
- Confirm the specific code pattern or variable name to search for (e.g., `remove_caching_layer`)
- Locate any communication templates in the workspace (e.g., `template.txt`)

### 2. Find Introducing Commit
Use `git log` with the `-S` flag to search for the earliest commit containing the specified code pattern:
