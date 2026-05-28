---
name: mcp-catalog
description: "Catalog of Top Open Source MCP Servers (2025 Edition). Includes Android, Browser, Docker, Google Cloud, etc."
trigger: mcp OR server OR tools OR integration OR browser control OR android control OR deep research OR docker OR google cloud
scope: global
---

# MCP Server Catalog - The Arsenal

> [!TIP]
> This catalog lists specialized MCP Servers that can be deployed to extend Agent capabilities.
> Source: "Top Open-Source MCP Servers" (Transcript).

## 1. HuggingFace MCP

**Role**: The Gateway to Models & Data.

- **Capabilities**: Access datasets, run models, and interact with Spaces dynamically.
- **Why**: Use for specialized inference or fetching data without leaving the agent context.
- **Mode**: Dynamic discovery of tools.

## 2. Octagon Deep Research

**Role**: Unlimited Parallel Researcher.

- **Capabilities**: 8-10x faster than traditional search. Runs parallel deep dives across broad domains.
- **Why**: For complex market research or academic queries requiring synthesis of 100+ sources.

## 3. AllVoice Lab (Damn Many Mercy)

**Role**: High-Fidelity Voice & Video.

- **Capabilities**: Text-to-Speech, Voice Cloning (seconds), Multilingual Dubbing, Subtitle Removal.
- **Why**: Generate multimedia assets or localize content programmatically.

## 4. Android MCP

**Role**: Mobile Device Control.

- **Capabilities**: Uses ADB to control Android phones/emulators. Launch apps, tap, screenshot, inspect UI tree.
- **Why**: E2E Mobile Testing or automating mobile-only workflows.

## 5. Deep View MCP

**Role**: Large-Scale Codebase Understanding.

- **Capabilities**: Feeds entire repositories (via `repomix`) to Gemini Flash/Pro for "Global Context" answers.
- **Why**: "Refactor class X" knowing how it affects the entire system, not just the open file.

## 6. Combine MCP

**Role**: The Server Aggregator.

- **Capabilities**: Merges multiple MCP servers into one endpoint. Handles namespace conflicts (e.g., `serverA_search` vs `serverB_search`).
- **Why**: Bypass client limits on connection count.

## 7. Google Admin MCP

**Role**: Workspace Automator.

- **Capabilities**: Manage Users, Groups, Suspensions, Password Resets via Google Admin Directory API.
- **Why**: Automate HR Onboarding/Offboarding flows.

## 8. JSON MCP

**Role**: Structured Data Handler.

- **Capabilities**: Split, Merge, Filter, and Validate massive JSON files without loading them entirely into context.
- **Why**: Manipulating large data exports efficiently.

## 9. Browser MCP

**Role**: Stealthy Local Automation.

- **Capabilities**: Uses _existing_ Chrome profile. No login needed. Detects accessibility tree for precise clicking.
- **Why**: Automating web tasks that require auth (Logged-in sessions) without triggering bot detection.

## 10. Bright Data MCP

**Role**: Unblocked Web Access.

- **Capabilities**: Enterprise-grade proxying to bypass Captchas, Geo-blocks, and IP bans.
- **Why**: When "Fetch URL" fails due to 403 Forbidden or Cloudflare checks.

## 11. Notion MCP

**Role**: Knowledge Management & Task Sync.

- **Capabilities**: Read pages, manage databases (tasks), generate task lists from code analysis.
- **Why**: Keep project management (Notion) in sync with code status automatically.

## 12. GitHub MCP

**Role**: DevOps & Code Collaboration.

- **Capabilities**: Manage Repos, Pull Requests, Issues, Actions.
- **Why**: Create PRs directly from the Agent (e.g., "Refactor this and open a PR").

## 13. TestSprite MCP

**Role**: Autonomous Testing Agent.

- **Capabilities**: Scans code, generates test plans, executes tests (Playwright/Python), and reports issues.
- **Why**: "Unit Testing on Autopilot" - detects regressions without human intervention.

## 14. Linear MCP

**Role**: Agile Project Management.

- **Capabilities**: Manage tickets/issues for teams (similar to Notion but for Agile/Scrum).
- **Why**: Team-based task tracking integration.

## 15. Context7 MCP

**Role**: Live Documentation Context.

- **Capabilities**: Fetches _latest_ documentation (e.g., Next.js 15 breaking changes) to prevent hallucinations.
- **Why**: Ensures code generation uses up-to-date syntax (avoiding deprecated APIs).

## 16. Ref MCP

**Role**: Context-Efficient Documentation.

- **Capabilities**: Alternative to Context7. combination of web search, scraping, and code search. Uses semantic search to expose _only_ relevant snippets, saving tokens.
- **Why**: When Context7 is too heavy on context/tokens.

## 17. Docker MCP

**Role**: The Sandbox & Context Optimizer.

- **Capabilities**: Runs verified MCPs in a sandbox. Reduces context bloat by loading only required tools for a specific query ("Code Mode").
- **Why**: Security (sandbox) and Efficiency (prevent context limit errors with many tools).

## 18. Shadcn Registry MCP

**Role**: UI Component Installer.

- **Capabilities**: Install shadcn/ui components directly. Supports custom registries (Aceternity, Magic UI).
- **Why**: "Add a pricing table" -> Installs the actual component code + dependencies automatically.

## 19. Google Cloud MCP Suite

**Role**: Cloud Infrastructure Control.

- **Capabilities**:
  - **Maps**: Location-based grounding.
  - **BigQuery**: Query enterprise data without exposing sensitive rows to context.
  - **Compute/Kubernetes**: Manage VMs and containers.
- **Why**: Full stack cloud management from the agent.

## 20. Obsidian MCP

**Role**: Local Knowledge Base.

- **Capabilities**: Manage Obsidian pages/tasks (Search, Read, Write).
- **Why**: For users who prefer local-first notes over Notion.

## 🌍 Discovery & Markets

- [MCP Market](https://mcpmarket.com/es/categories/learning-documentation)
- [Awesome Claude Skills](https://github.com/VoltAgent/awesome-claude-skills)
- [LobeHub Local Skills](https://lobehub.com/es/mcp/moscaverd-local-skills)
