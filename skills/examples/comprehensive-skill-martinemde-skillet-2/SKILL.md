---
name: comprehensive-skill
description: A comprehensive skill demonstrating all frontmatter fields. Use for testing complete SKILL.md parsing.
license: Apache-2.0
compatibility: Requires git, docker, and access to the internet
metadata:
  author: test-org
  version: "1.0.0"
  category: testing
allowed-tools: Read Write Bash(git:*) Bash(docker:*)
model: claude-sonnet-4-5-20250929
---

# Comprehensive Skill

This skill demonstrates all possible frontmatter fields and features.

## Overview

This skill is designed to test the complete parsing and execution pipeline
of the skillet CLI tool. It includes all optional frontmatter fields and
demonstrates proper formatting.

## Prerequisites

- Git must be installed
- Docker must be installed
- Internet access is required

## Instructions

### Step 1: Initialize

First, check the environment:

```bash
git --version
docker --version
```

### Step 2: Execute

Perform the main task according to user requirements.

### Step 3: Report

Provide a detailed summary of actions taken.

## Output Format

Results should be formatted as:

```
Task: [task name]
Status: [success/failure]
Details: [description]
```

## Error Handling

If prerequisites are not met, report clearly which requirement failed.

## Resources

Additional documentation can be found in the references/ directory.
