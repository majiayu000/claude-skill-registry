---
name: vibe-coding
description: Methodology for effective AI-assisted software development. Use when helping users build software with AI coding assistants, debugging AI-generated code, planning features for AI implementation, managing version control in AI workflows, or when users mention "vibe coding," Cursor, Windsurf, or similar AI coding tools. Provides strategies for planning, testing, debugging, and iterating on code written with LLM assistance.
---

# Vibe coding methodology

Practical strategies for building software effectively with AI coding assistants.

## Planning process

Start by working with the AI to write a detailed implementation plan in a markdown file.

**Scope management**: Review and refine the plan—delete unnecessary items, mark complex features as "won't do," and keep a separate section for ideas to implement later. This prevents scope creep and maintains focus.

**Incremental implementation**: Work section by section rather than building everything at once. Have the AI mark sections complete after successful implementation, and commit each working section to git before moving to the next.

**Track progress visibly**: Use todo lists, markdown checklists, or inline status markers so both you and the AI can see what's done and what remains. This prevents re-implementing completed work and keeps sessions focused.

## Version control strategies

Git is your safety net—don't rely solely on the AI tool's revert functionality.

**Clean slate principle**: Begin each new feature with a clean git state. When stuck, use `git reset --hard HEAD` if the AI goes down an unproductive path. Multiple failed attempts create layers of bad code that compound problems.

**Clean implementation**: When you finally find a working solution after several attempts, reset to a clean state and implement it fresh. Multiple failed attempts create layers and layers of bad code—don't keep the accumulated mess. A clean re-implementation of a known-good solution is faster and more maintainable than untangling spaghetti.

## Testing framework

Prioritize end-to-end integration tests over unit tests. Focus on simulating user behavior—testing features by simulating someone clicking through the site or app.

**Regression prevention**: LLMs often make unnecessary changes to unrelated logic. Tests catch these regressions before they compound.

**Tests as guardrails**: Consider starting with test cases to provide clear boundaries for what the AI should and shouldn't change. Ensure tests pass before moving to the next feature.

## Effective bug fixing

**Error messages**: Simply copy-pasting error messages is often enough context for the AI to identify and fix issues.

**Analyze before coding**: Ask the AI to consider multiple possible causes before jumping to implementation. This prevents chasing the wrong problem.

**Reset after failures**: Start with a clean slate after each unsuccessful fix attempt rather than layering fixes on top of broken code.

**Strategic logging**: Add logging statements to better understand what's happening when bugs are opaque.

**Switch models**: Try different AI models when one gets stuck on a problem.

## AI tool optimization

**Instruction files**: Write detailed instructions for your AI in appropriate files (cursor.rules, windsurf.rules, claude.md). These provide project-specific context that improves output quality.

**Local documentation**: Download API documentation to your project folder. AI tools work more accurately with local docs than trying to recall API details from training.

**Multiple tools**: Some developers run both Cursor and Windsurf simultaneously on the same project. Cursor tends to be faster for frontend work while Windsurf thinks longer on complex problems.

**Compare outputs**: Generate multiple solutions and pick the best one rather than accepting the first output.

## Complex feature development

**Standalone prototypes**: Build complex features in a clean codebase first, then integrate once working. This isolates problems and makes debugging easier.

**Reference implementations**: Point the AI to working examples to follow. Existing code patterns provide concrete guidance.

**Clear boundaries**: Maintain consistent external APIs while allowing internal changes. Service-based architectures with clear boundaries work better than monorepos for AI-assisted development.

## Tech stack considerations

**Established frameworks**: Ruby on Rails and similar mature frameworks work well due to 20+ years of consistent conventions in training data.

**Training data matters**: Newer languages like Rust or Elixir may have less training data, leading to more errors or outdated patterns.

**Modularity**: Small, modular files are easier for both humans and AIs to work with. Avoid files with thousands of lines—they exceed context windows and create confusion.

## Beyond coding

AI assistants help with more than writing code:

- **DevOps**: Configuring servers, DNS, and hosting
- **Design**: Generating favicons and other design elements
- **Documentation**: Drafting docs and marketing materials
- **Education**: Explaining implementations line by line
- **Visual input**: Share screenshots for UI bugs or design inspiration
- **Voice input**: Tools like Aqua enable 140 words per minute input

## Continuous improvement

**Regular refactoring**: Once tests are in place, refactor frequently. Ask the AI to identify refactoring candidates.

**Stay current**: Try every new model release. Different models excel at different tasks—experiment to find which works best for your use case.
