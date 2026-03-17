---
name: Project Detection
description: Framework and stack identification with detection scripts and patterns. Use when detecting project type, analyzing framework, identifying stack, initializing projects, or when user mentions project detection, framework analysis, stack identification, or codebase analysis.
allowed-tools: Read, Bash, Glob, Grep
---

# Project Detection

**CRITICAL: The description field above controls when Claude auto-loads this skill.**

This skill provides mechanical detection scripts and patterns for identifying project frameworks, languages, and structures across any technology stack.

## What This Skill Provides

### 1. Detection Scripts (Mechanical - No AI Needed)
- `detect-framework.sh` - Identifies framework from config files
- `detect-language.sh` - Detects primary programming language
- `detect-structure.sh` - Maps project directory structure
- `detect-tools.sh` - Finds build tools, linters, formatters
- `analyze-dependencies.sh` - Analyzes package dependencies

### 2. Templates
- `project-json.template` - Standard project.json structure
- Framework detection patterns for 20+ frameworks
- Language detection rules

### 3. Reference Documentation
- Framework identification rules
- Directory structure patterns
- Tooling detection logic

## Instructions

When user asks to detect or analyze a project:

### Step 1: Run Framework Detection

Execute the framework detection script:

!{bash plugins/01-core/skills/project-detection/scripts/detect-framework.sh .}

This mechanically checks for:
- package.json (Node.js/JavaScript)
- pyproject.toml, requirements.txt (Python)
- Cargo.toml (Rust)
- go.mod (Go)
- pom.xml, build.gradle (Java)
- composer.json (PHP)
- Gemfile (Ruby)

### Step 2: Detect Language and Version

Execute language detection:

!{bash plugins/01-core/skills/project-detection/scripts/detect-language.sh .}

### Step 3: Map Directory Structure

Execute structure detection:

!{bash plugins/01-core/skills/project-detection/scripts/detect-structure.sh .}

### Step 4: Analyze Dependencies and Tools

Execute dependency analysis:

!{bash plugins/01-core/skills/project-detection/scripts/analyze-dependencies.sh .}

### Step 5: Generate Project Configuration

Use the detected information to create .claude/project.json with:
- type (web-app, api, cli, library, etc.)
- framework (Next.js, Django, FastAPI, etc.)
- language and version
- structure mappings
- tools (build, test, lint, format)
- dependencies

## Detection Patterns

### Framework Detection Rules

**Node.js Frameworks:**
- Next.js: package.json contains "next" dependency + pages/ or app/ directory
- React: package.json contains "react" + src/components/
- Vue: package.json contains "vue" + src/
- Express: package.json contains "express"
- NestJS: package.json contains "@nestjs/core"

**Python Frameworks:**
- Django: requirements.txt contains "Django" or pyproject.toml lists django
- FastAPI: fastapi dependency + app/main.py pattern
- Flask: flask dependency
- Streamlit: streamlit dependency

**Rust:**
- Cargo.toml [package] section
- Check for web frameworks: axum, actix-web, rocket

**Go:**
- go.mod file
- Check for frameworks: gin, echo, fiber

### Structure Detection Patterns

**Common Patterns:**
- src/, app/, lib/ → Source code
- components/, pages/ → Frontend
- api/, routes/, handlers/ → Backend
- tests/, test/, spec/ → Tests
- docs/, documentation/ → Documentation
- config/, .config/ → Configuration

## Examples

**Example 1: Detect Next.js Project**

User: "What framework is this project using?"

Claude (auto-loads this skill, runs detection):
!{bash plugins/01-core/skills/project-detection/scripts/detect-framework.sh .}

Result: "Next.js 14.0.0 with TypeScript, App Router architecture"

**Example 2: Initialize New Project**

User: "Initialize this project"

Claude (auto-loads this skill, analyzes structure):
!{bash plugins/01-core/skills/project-detection/scripts/detect-structure.sh .}

Creates .claude/project.json with detected mappings

## Requirements

**Scripts must be:**
- ✅ Mechanical (pattern recognition, no AI decisions)
- ✅ Fast (complete in < 1 second)
- ✅ Project-agnostic (work with ANY framework)
- ✅ Exit codes: 0 = success, 1 = error

**Output format:**
- JSON for machine parsing
- Clear status messages for humans
- Error messages explain what's missing

## Success Criteria

- ✅ Detects 20+ frameworks accurately
- ✅ Works in any project directory
- ✅ Generates valid project.json
- ✅ Scripts are executable and documented
- ✅ No hardcoded assumptions about structure

---

**Plugin**: 01-core
**Skill Type**: Analyzer + Generator
**Auto-invocation**: Yes (via description matching)
