---
name: meta-agent-skills
description: Proactively analyzes the codebase and generates specialized subagents and skills to standardize agentic workflows.
---

# Meta-Agent Skills

## Purpose

This skill serves as a "Meta-Skill" that bootstraps the Agentic Makefile environment. It empowers the Agent to analyze the repository's technology stack (e.g., Python/Poetry, Node/Next.js, Go), detect the AI environment (Claude Code, Cursor, Gemini), and generate specialized, ready-to-use Agent Skills and Subagents.

## When to Use

- When initializing a new repository for AI agent use.
- When the technology stack changes (e.g., switching from Pip to Poetry).
- When you want to reset or update the standard agent capabilities.
- When asked to "setup skills", "maintain agent rules", or "install standard agents".

## Instructions

1.  **Detect AI Environment**:
    - Check for `.claude/`, `.cursor/`, or `.gemini/` directories to determine the target AI platform.
    - **Claude Code Detection**: If `.claude/` exists, Claude Code is a primary target.
      - **Prefix Selection**: Claude Code does not support recursive search for skills/agents. You MUST use a flat structure with a prefix to identify generated components (e.g., `ma-`, `meta-`, `m-`).
      - **User Consultation**: Present 3-5 candidate prefixes (e.g., `ma-`, `meta-agent-`, `m-`, `agent-`, `gen-`) and ask the user to choose one or provide their own.
    - **Cursor Detection**: If `.cursor/` exists, Cursor is a primary target. Cursor supports recursive search.
    - **Default**: If ambiguous, prioritize `.claude/` as the standard, following the flat structure protocol.

2.  **Analyze Codebase**:
    - **Review Documentation**: Read `README.md`, `CONTRIBUTING.md`, `DEVELOPMENT.md`, or other relevant documentation to understand the project structure, development workflows, and any specific commands recommended for the codebase.
    - **Detect Sub-Projects**: Recursively search for "logical project boundaries" in sub-directories. Look for files like `package.json` (Node.js), `go.mod` (Go), `pyproject.toml` or `requirements.txt` (Python), `main.tf` or `*.tf` (Terraform), etc.
    - **Detect Multi-Layered Builds**: Search for files that indicate a layered build or deployment process, such as `Dockerfile`, `docker-compose.yml`, `Earthfile`, `Tiltfile`, `Skaffold.yaml`, or `kustomization.yaml`.
    - **Map Tech Stack per Project**: For each detected sub-project, determine its specific tech stack and how to run builds, linters, and tests within its directory.
    - **Analyze Layered Commands**: Categorize commands into logical layers (e.g., `App` for compilation, `Docker` for image building, `Infra` for deployment or local orchestration).
    - **Identify Test Types**: Look for `tests/unit`, `tests/integration`, `cypress`, `playwright`, etc., to distinguish between Unit, Integration, and E2E tests for each project.
    - **Identify Security Tools**: Check if `trivy`, `osv-scanner`, or other security tools are configured or available.
    - **Identify Setup Scripts**: Look for `pre-commit` config, `Makefile`, or setup scripts to include in `setup-dev-env`.

3.  **Verify Commands**:
    - Before generating skills, proactively verify that the detected commands work in their respective project environments.
    - Run `command --help`, `command --version`, or similar check for each primary command in the correct working directory.
    - If a command fails or is missing, investigate alternatives or suggest installation in the final report.

4.  **Generate Skills & Agents**:
    - Read the templates located in `assets/templates/skills/` and `assets/templates/agents/`.
    - **Strict Policy**: You MUST NOT generate any subagent or Agent Skill if its corresponding template does not exist in `assets/templates/agents/` or `assets/templates/skills/`.
    - **Instantiate Templates**:
      - For each skill template, populate the **Commands** table with the verified commands for all detected sub-projects.
      - **Build Separation**: Distinguish between project compilation (App layer) and container image building (Docker layer).
        - Use `build-project` template for compilation/build commands (e.g., `npm run build`, `go build`).
        - Use `build-container-image` template for containerization commands (e.g., `docker build`, `earthly --push +docker`).
      - Each row in the table MUST include the `Order`, `Component`, `Path` (relative to root), `Layer` (e.g., App, Docker), `Command`, and `Description`.
      - Ensure the **order of commands** is logical (e.g., compile app before building docker image).
    - **Write** the generated files to the target directory based on the platform:
      - **Claude Code (Flat Structure)**:
        - **Skills**: `.claude/skills/<prefix><skill-name>/SKILL.md` (e.g., `.claude/skills/ma-lint-fix/SKILL.md`).
        - **Agents**: `.claude/agents/<prefix><agent-name>.md` (e.g., `.claude/agents/ma-maintainer-agent.md`).
      - **Cursor (Nested Structure)**:
        - **Skills**: `.cursor/skills/meta-agent-skills/<skill-name>/SKILL.md` (e.g., `.cursor/skills/meta-agent-skills/lint-fix/SKILL.md`).
        - **Agents**: `.cursor/agents/meta-agent-skills/<agent-name>.md` (e.g., `.cursor/agents/meta-agent-skills/maintainer-agent.md`).
    - **Bind Skills to Agents**:
      - For each generated agent, identify the `skills` required from its template frontmatter.
      - Synchronize the `Capabilities` section between `<!-- SKILLS_START -->` and `<!-- SKILLS_END -->` markers.
      - **Link Resolution**:
        - **Claude Code**: Use links like `[lint-fix](../skills/<prefix>lint-fix/SKILL.md)`.
        - **Cursor**: Use links like `[lint-fix](../../skills/meta-agent-skills/lint-fix/SKILL.md)`.
      - Ensure each mentioned skill is linked to its respective `SKILL.md` file.
    - _Note_: For `test-*` skills, only generate the ones that match the detected test types.

5.  **Verify & Fix Generated Output**:
    - **Audit**: Read a sample of the generated `SKILL.md` files (prioritize `lint-fix` and `build-project`).
    - **Verify Templates**: Verify that every generated subagent and Agent Skill has a corresponding template in the assets directory. If you find any generated file that does not have a corresponding template, you MUST delete it.
    - **Check for Placeholders**: Ensure no unpopulated templates like `{{ command }}` remain in the generated files.
    - **Path Validation**: Verify that the `Working Directory` paths specified in the tables actually exist relative to the workspace root.
    - **Immediate Remediation**: If errors, broken links, or missing information are found, use editing tools to fix the generated files immediately.

6.  **Execute Generated Skills & Agents**:
    - **Smoke Test**: Execute a subset of the generated skills to verify their real-world functionality.
    - **Priority Skills**: Run `setup-dev-env` (if applicable), followed by `lint-fix`, `build-project`, and `build-container-image`.
    - **Verify Subagents**: If a subagent was generated, consider invoking it for a simple query (e.g., "Analyze the current state of the codebase").
    - **Error Handling**: If execution fails, analyze the output, fix the generated skill/agent, and re-run until successful.

7.  **Report**:
    - List the skills and agents created.
    - Mention which stack and test types were detected.
    - Report the results of command verification (which commands are confirmed and which might need setup).
    - Report on the **Verification & Fix** results (e.g., "Verified all generated skills; fixed 1 path error in lint-fix").
    - Report on the **Execution** results (e.g., "Successfully ran lint-fix, build-project, and build-container-image skills").

## Capabilities Generated

- **Core Skills**: `lint-fix` (includes type checking), `build-project`, `build-container-image`, `update-deps`, `docs-gen-readme`, `security-scan`, `setup-dev-env`, `add-skill-templates`, `add-agent-templates`, `mend-agent-templates`.
- **Test Skills**: `test-unit`, `test-integration`, `test-e2e`.
- **Subagents**: `codebase-maintainer-agent`, `security-auditor-agent`, `qa-engineer-agent`, `template-factory-agent`.

## References

- [Agent Skills Standard](references/agent-skills.md)
- [Claude Code](references/claude-code.md)
- [Cursor](references/cursor.md)
- [Gemini CLI](references/gemini-cli.md)
- [Codex](references/codex.md)
