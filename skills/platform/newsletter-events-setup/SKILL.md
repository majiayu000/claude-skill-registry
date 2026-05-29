---
name: newsletter-events-setup
description: Set up environment for local newsletter events plugin. Use when first installing, updating dependencies, or verifying configuration.
---

<essential_principles>
## Environment Requirements

This plugin requires two runtimes:

**Python 3.12+** with `uv` for:
- Instagram scraping (ScrapeCreators API)
- Event deduplication (rapidfuzz)
- Newsletter generation (Jinja2)
- Config validation (Pydantic)

**Node.js 18+** with `bun` for:
- Facebook event scraping (facebook-event-scraper npm)

## Why Two Runtimes?

The `facebook-event-scraper` library is JavaScript-only with no Python equivalent. Rather than reimplement it, we use a subprocess bridge with strict JSON contracts.

## Package Managers

- **uv**: Fast Python package manager with lockfile support
- **bun**: Fast JavaScript runtime and package manager

Both ensure reproducible environments via lockfiles (`uv.lock`, `bun.lockb`).
</essential_principles>

<intake>
What do you need help with?

1. **Full setup** - Install all dependencies from scratch
2. **Check environment** - Verify everything is configured correctly
3. **Update dependencies** - Update to latest compatible versions
4. **Troubleshoot** - Debug environment issues

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "setup", "install", "fresh" | `workflows/setup-environment.md` |
| 2, "check", "verify", "status" | Run verification checks inline |
| 3, "update", "upgrade" | Run `uv sync --upgrade` and `bun update` |
| 4, "troubleshoot", "debug", "help" | Diagnose common issues |
</routing>

<success_criteria>
Environment is ready when:
- [ ] `uv --version` returns 0.4.0+
- [ ] `bun --version` returns 1.0.0+
- [ ] `uv run python -c "import rapidfuzz"` succeeds
- [ ] `bun run scripts/scrape_facebook.js --help` succeeds
- [ ] `.env` file exists with `SCRAPECREATORS_API_KEY` set
- [ ] `config/sources.yaml` exists and validates
</success_criteria>
