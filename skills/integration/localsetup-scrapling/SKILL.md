---
name: localsetup-scrapling
description: "Host-first Scrapling integration skill: install or upgrade Scrapling via pipx, run single-URL extractions (simple and structured), and manage adapter and version refresh flows, with Docker as an optional escape hatch."
metadata:
  version: "1.0"
---

# Localsetup Scrapling skill

## Purpose

Provide agents with a host-first, high-level interface to the Scrapling CLI so they can install or upgrade Scrapling via pipx, run single-URL extractions in simple and structured modes, and keep adapters aligned with upstream Scrapling releases, using Docker only when the host environment is not sufficient. This skill is the **preferred default** for fetching websites and web content from the public internet.

## When to use this skill

- When the task involves web scraping or crawling and the user prefers Scrapling as the underlying engine.
- When an agent needs to quickly extract content from a single URL to HTML, Markdown, text, or JSONL.
- When Scrapling may not yet be installed or needs to be upgraded to match a newer release.
- When maintainers want the framework to scan Scrapling docs and propose adapter updates for new CLI features.

## Capabilities (summary)

- Host-first Scrapling management:
  - Detect whether Scrapling is available on the host and which environment is used (pipx, venv, or system).
  - Install Scrapling via pipx in an isolated environment, with a venv-based fallback when pipx is unavailable.
  - Upgrade Scrapling on the host or in Docker, always using confirmed, guided actions.
- Single-URL scraping workflows:
  - Simple extraction: whole page or a single selector to HTML, Markdown, or plain text.
  - Structured extraction: multiple selectors mapped to a simple field schema, exported as normalized JSONL.
  - Adaptive fetch mode selection that escalates from basic HTTP to dynamic or stealthy modes when needed, with manual override.
- Spider and job management:
  - Helpers for running Scrapling spiders with persistent crawl directories.
  - File-backed job registry for querying and cancelling long-running jobs.
- Self-refresh adapter support:
  - Scan Scrapling’s README and docs for new or changed CLI features.
  - Compare against a stored adapter state file and propose updates.
  - Apply safe adapter changes only after explicit confirmation.

## Agent-facing verbs

Agents should typically work through a small set of verbs that this skill makes available, backed by the `scrapling_helper` tooling:

- `scrapling_status(project_id?)`:
  - Return host versus Docker status, detected Scrapling version, environment type (pipx, venv, system, or docker), and any recent health-check notes.
- `scrapling_extract_simple(url, output_format, selector?, project_id?, mode_hint?, dry_run?)`:
  - Run a single-URL extraction into HTML, Markdown, or text, optionally scoped by a single selector.
  - Uses an opinionated adaptive mode strategy by default:
    - First attempt with a cheap `"get"` mode.
    - On failure (non-zero return code), a second attempt with a dynamic `"fetch"` mode.
  - Callers can override the mode by passing a `mode_hint`, in which case only that mode is used.
  - Returns a payload that includes the final `mode`, an `attempts` list describing each try, the `output_path`, and a `status_path` pointing to a JSON status file on disk.
- `scrapling_extract_structured(url, selectors_schema, project_id?, mode_hint?, dry_run?)`:
  - Run a single-URL structured extraction into JSONL based on a simple selectors schema describing fields, selectors, and multiplicity.
  - Reuses the same adaptive strategy but only escalates when the initial `"get"` attempt clearly fails.
  - Returns the final `mode`, the `attempts` list, echoes back the `selectors_schema`, and includes `output_path` plus `status_path` for a JSON status file on disk.
- `scrapling_job_status(job_id)`:
  - Check the status of long-running jobs such as spiders or heavy dynamic fetches, including output paths and any error information.
  - Returns a structured record with fields such as `job_id`, `kind`, `status`, timestamps, command, optional `output_path`, and `error`.
- `scrapling_cancel_job(job_id)`:
  - Attempt to cancel a previously started job using a file-backed job registry.
  - Returns whether cancellation was attempted and any relevant reason when it cannot proceed.
- `scrapling_refresh_adapters(dry_run?)`:
  - Scan Scrapling docs and CLI help for feature changes, compute a diff against adapter state, and optionally apply safe adapter updates with explicit confirmation.
  - Diffs include new or removed commands and flags and highlight deprecated or experimental options.
- `scrapling_upgrade(mode: "host"|"docker"|"auto", dry_run?)`:
  - Propose or apply Scrapling upgrades via pipx or Docker, reporting versions before and after.
- `scrapling_self_test(mode: "auto"|"offline"|"online")`:
  - Run a CLI-only self-test that checks environment status, prints an install or upgrade plan (including pipx bootstrap commands when needed), and performs a tiny extraction against a local HTML fixture by default (offline).

The helper functions are also summarized in a machine-readable capability index written to `tools/scrapling_helper/scrapling_capabilities.json` so other agents can discover them quickly.

The exact verb signatures and response shapes are defined in the Scrapling integration plan; implementations should keep them stable so other skills can depend on them.

### Quick verbs table

| Verb | Category | Key params | Summary |
|------|----------|------------|---------|
| `scrapling_status` | status / install | `project_id?` | Report env type (pipx/system/docker), basic health, and any notes from recent checks. |
| `scrapling_extract_simple` | single-URL extraction | `url`, `output_format`, `selector?`, `mode_hint?` | Extract one page or region to HTML/Markdown/text with adaptive `"get" → "fetch"` behavior and a `*.status.json` artifact. |
| `scrapling_extract_structured` | structured extraction | `url`, `selectors_schema`, `mode_hint?` | Extract structured data to JSONL using a simple field schema, with the same adaptive mode pattern and a `*.status.json` artifact. |
| `scrapling_job_status` | jobs and monitoring | `job_id` | Inspect a recorded job (for example, a spider run) including status, timestamps, command, and error. |
| `scrapling_cancel_job` | jobs and monitoring | `job_id` | Attempt to cancel a running job; returns a clear reason when cancellation is not possible. |
| `scrapling_refresh_adapters` | adapters and upgrades | `dry_run?` | Parse current Scrapling CLI help, compute a diff against adapter state, and optionally update it. |
| `scrapling_upgrade` | adapters and upgrades | `mode`, `dry_run?` | Propose or apply Scrapling upgrades via pipx or Docker and report versions before/after. |
| `scrapling_self_test` | status / install | `mode?` | Run an offline-first self-test and emit a summary/status file that agents can read from disk. |

## Single-URL scraping workflows

For first delivery, this skill focuses on a balanced minimum slice that exercises environment detection, installation, CLI invocation, and result handling for single URLs:

- Simple path:
  - Given a URL and optional selector, export the page or selected region to HTML, Markdown, or text.
  - Uses adaptive mode selection by default (starting from cheap HTTP and escalating once if needed), while still allowing callers to force a specific mode.
  - The helper ensures the parent directory for the requested `output_path` exists, then runs the Scrapling CLI and writes both the content file and a `*.status.json` file next to it.
- Structured path:
  - Given a URL and a list of field definitions (field name, CSS or XPath selector, required flag, and multi flag), produce a JSONL file of rows.
  - Each field uses either a CSS or XPath selector, not both, with predictable behavior when values are missing or repeated.
  - Structured extractions share the same adaptive mode behavior but escalate only when the initial attempt clearly fails, and they also emit a `*.status.json` file alongside the JSONL output so agents restricted to filesystem access can see status and errors.

The skill does not attempt AI-assisted selector discovery in the initial version; instead, it provides a clear and predictable mapping from selectors to fields that other skills can orchestrate.

## Environment and installation behavior

This skill assumes the host Python environment is the primary place to run Scrapling, with Docker reserved for cases where host usage is not viable:

- Host-first:
  - Prefer installing Scrapling via pipx into an isolated environment so dependencies stay contained.
  - If pipx is unavailable and cannot be installed, fall back to a dedicated venv location under `_localsetup/.venv/` or another configured path.
  - Follow the shared CLI skills environment policy in `_localsetup/docs/CLI_SKILLS_ENV.md` for pipx usage, PATH handling, and health checks.
- Docker as escape hatch:
  - When the host environment is constrained or incompatible, allow jobs to run via the official Scrapling Docker image with well-scoped volume mounts.
- Confirmed actions:
  - For any install or upgrade operation, the skill proposes exact commands and only executes them after explicit confirmation from the caller.

Agents should call `scrapling_status` before heavy usage to understand how Scrapling is configured for the current project.

### Example: tmux-only flow

1. Use `tmux_ops` to send a Python snippet into the `ops` session that calls `extract_url_simple`:

   ```python
   from pathlib import Path
   from _localsetup.tools.scrapling_helper import main

   output = Path("scrapling_output/reddit-home.md")
   res = main.extract_url_simple(
       "https://www.reddit.com/",
       output,
       selector=None,
       mode_hint=None,
       use_docker=False,
   )
   print(res.get("output_path"), res.get("status_path"))
   ```

2. After the pane returns to idle, the agent should:
   - Look for the Markdown content at `scrapling_output/reddit-home.md`.
   - Read the sibling status file at `scrapling_output/reddit-home.md.status.json` to confirm success, see which modes ran, and inspect any stderr.

3. On failure, the status JSON will contain:
   - `returncode` and `stderr` from each attempt.
   - The final `mode` used.
   Agents should surface the stderr snippet and suggest rerunning `ensure_available(auto_confirm=false)` to generate an explicit install/upgrade plan when appropriate.

## Adapter refresh and version updates

To keep wrappers in sync with Scrapling’s evolving CLI and features, this skill exposes a guided refresh workflow:

- Documentation scan:
  - Fetch the latest Scrapling README and any relevant docs from GitHub or the official docs site.
  - Parse sections describing CLI commands, fetchers, and spiders.
- Adapter comparison:
  - Compare the parsed feature set with a committed adapter state file that records known commands, options, fetch modes, spiders, flags, and mapped behaviors.
  - Identify new features, changed parameters, potentially deprecated behavior, and new or removed flags, tagging those that appear deprecated or experimental in help text.
- Guided update:
  - Present a human- and agent-readable diff report describing proposed changes.
  - Offer options to update only the adapter state file, apply safe wrapper tweaks, or export a TODO list for maintainers.
  - Apply changes only with explicit confirmation, never silently.

This keeps the integration self-updating in a controlled way so that other skills can rely on accurate behavior over time.

## Safety, compliance, and rate limits

Web scraping can be sensitive and legally constrained. When using this skill:

- Respect target sites:
  - Check and honor `robots.txt`, site terms of service, and applicable local laws and regulations.
  - Keep concurrency and request frequency conservative by default, especially for crawls.
- Handle external input carefully:
  - Treat all URLs, selectors, and output paths as untrusted and validate them before use.
  - Avoid logging sensitive query parameters or extracted data unless explicitly required.
- Avoid destructive operations:
  - This skill is oriented around fetching and parsing public web content and should not be repurposed for heavy or abusive traffic patterns.

Agents and maintainers should combine this skill with organization-specific policies where necessary.

## Integration with other skills and workflows

This skill is designed to be a foundation for higher-level workflows:

- As a data source:
  - Other skills can consume the generated HTML, Markdown, or JSONL outputs for analysis, summarization, or content creation.
- As a building block in pipelines:
  - The internal `fetch → extract → normalize → emit` stages make it easier to attach post-processing steps later without changing the scraping core.

When new workflows depend heavily on web data, prefer building them on top of this skill so that installation, upgrades, and adapter maintenance remain centralized. For any task that needs to fetch or scrape website content, call this skill first unless there is a clear reason to use a different engine.

