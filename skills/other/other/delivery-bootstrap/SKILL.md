---
name: delivery-bootstrap
description: "Use when starting implementation on a new or unfamiliar codebase. Auto-detects tech stack and sets up development context."
---

# Delivery Bootstrap Skill

Just-in-Time tech stack detection and setup.

## Workflow

1. **Check product_type** from `diamonds/active.yml`:
   - If `product_type` is set (from `/interview`), use it to determine the delivery profile.
   - If not set, scan for indicators per `detector.md` Step 1b:
     - Curriculum/lesson plans, LMS config -> `content_course`
     - Manuscript/chapters, editorial calendar -> `content_publication`
     - Video scripts, subtitle files, podcast RSS -> `content_media`
     - Prompt templates, model configs, agent definitions -> `ai_tool`
     - Service blueprints, pricing docs -> `service_offering`
   - If non-software product_type detected: skip software tooling detection (Steps 2-3 below), configure product-type-appropriate validation instead, and proceed to Step 4.

1b. **Scan project root** for technology indicators (software and ai_tool with code):
   - Package files: package.json, Cargo.toml, go.mod, requirements.txt, pyproject.toml, Gemfile, pom.xml, build.gradle
   - Config files: tsconfig.json, .eslintrc, .prettierrc, rustfmt.toml, .editorconfig
   - CI/CD: .github/workflows, .gitlab-ci.yml, Jenkinsfile, Dockerfile
   - Framework indicators: next.config.js, nuxt.config.ts, angular.json, etc.

2. **Identify stack components** (software/ai_tool with code):
   - Language(s) and version(s)
   - Framework(s)
   - Package manager
   - Test runner and framework
   - Linter and formatter
   - Build tool
   - CI/CD platform
   - Database (if detectable)
   - Deployment target

3. **Verify tooling works**:
   - Run build command
   - Run test command
   - Run lint command
   - Note any failures or warnings

4. **Document existing patterns**:
   - Code organization (monorepo, src layout, etc.)
   - Naming conventions
   - Test patterns
   - Error handling patterns
   - API patterns

5. **Output**:
   ```
   ## Stack Profile
   - Language: [x] v[y]
   - Framework: [x]
   - Package manager: [x]
   - Test: [command] ([framework])
   - Lint: [command]
   - Build: [command]
   - CI/CD: [platform]

   ## Commands
   - Install: [command]
   - Dev server: [command]
   - Test: [command]
   - Build: [command]
   - Lint: [command]

   ## Observed Patterns
   - [list of patterns detected]

   ## Issues Found
   - [any broken tooling or warnings]
   ```

## Rules
- Use the project's established patterns. Don't impose external preferences.
- Be language-agnostic in principles, language-specific in implementation.
- If tooling is broken, flag it rather than silently working around it.

## Canvas Output
Create/update `.claude/jit-tooling/active-stack.yml` with detected stack configuration.
See `.claude/jit-tooling/active-stack.example.yml` for the expected format.

## Theory Citations
- Forsgren: Accelerate (tooling and automation)
- Smart: Sooner Safer Happier (remove friction)
