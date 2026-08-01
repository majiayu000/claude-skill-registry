---
name: rcc
description: 'Expert help with RCC (Repeatable, Contained Code): creating/running
  robots, robot.yaml + conda.yaml, holotree environment caching, rcc task testrun
  vs rcc run, dependency management (conda-forge + pip'
---

---
name: rcc
description: Expert help with RCC (Repeatable, Contained Code): creating/running robots, robot.yaml + conda.yaml, holotree environment caching, rcc task testrun vs rcc run, dependency management (conda-forge + pip), Playwright/robotframework-browser install (rccPostInstall: rfbrowser init), Control Room (rcc cloud), troubleshooting enterprise networks/proxies, and performance profiling with --pprof/--timeline/--trace.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# RCC Skill

RCC (Repeatable, Contained Code) is a Go CLI tool for creating, managing, and distributing Python-based self-contained automation packages.

**Repository:** https://github.com/joshyorko/rcc
**Maintainer:** JoshYorko

## Instructions

### Creating a new robot (project scaffolding)

Prefer RCC’s built-in templates.

There are two creation paths:

1) **Non-interactive (script/CI friendly):** `rcc robot initialize`

```bash
# List templates
rcc robot initialize --list
rcc robot initialize --json

# Create a robot directory from a template
rcc robot initialize -t <template-name> -d <directory>
```

2) **Interactive (human-driven):** `rcc create`

`rcc create` is interactive-only and should not be used in CI/scripting.

After creation, verify:

```bash
ls -la <directory>
cat <directory>/robot.yaml
cat <directory>/conda.yaml
```

### Running Robots

```bash
# Run in-place (good for iterative debugging)
rcc run
rcc run --task "Task Name"
rcc run --dev --task "Dev Task"

# Run in a clean, temporary directory (closest to Control Room deploy behavior)
rcc task testrun
```

When diagnosing “works locally but fails in CI/Control Room”, reach for `rcc task testrun` early.

### Dependency management (conda-forge first; pip when needed)

RCC environments are typically described in `conda.yaml`. Default posture:

- Prefer **conda-forge** packages when available.
- Use **pip** only for packages not available on conda-forge.
- Keep pins minimal while iterating; freeze/pin for production or when debugging solver drift.

RCC can also help edit the environment file for you:

```bash
# Example from the upstream workflow docs (adds numpy as pip, updates conda.yaml)
rcc robot libs -a numpy -p --conda conda.yaml
```

#### Optional speed-up: uv

`uv` can be a good speed-up in some environments, but it is not universal (enterprise constraints, restricted indexes, policy, etc.). Treat it as an optional optimization.

```yaml
dependencies:
  - python=3.10
  - uv
  - pip:
      - your-package==1.0.0
```

### Environment Management

```bash
rcc ht vars -r robot.yaml                   # Pre-build / print activation vars (advanced)
rcc ht vars -r robot.yaml --json            # Activation vars as JSON
rcc task shell                              # Interactive shell
rcc task script --silent -- python --version
rcc holotree list                           # List environments
rcc configure diagnostics                   # System check
```

Notes:

- Most workflows don’t require `rcc ht vars` explicitly; `rcc run` / `rcc task testrun` will build on-demand.
- Use `rcc ht vars` when you need activation variables (e.g., integrating with another tool) or you want to pre-warm builds.

Local dev tip:

- If your robot expects environment variables (common with Vault / Work Items integrations), a common convention is `devdata/env.json` in the robot root. RCC can load an env.json via `rcc holotree variables --environment devdata/env.json ...` (see `reference.md`).

### Debugging Environment Issues

```bash
rcc configure diagnostics --robot robot.yaml
rcc task script --silent -- pip list
rcc task shell --robot robot.yaml
```

### Dependency Management

```bash
rcc robot dependencies --space user           # View dependencies
rcc robot dependencies --space user --export  # Export frozen deps
```

### Configuration Reference

**robot.yaml:**
```yaml
tasks:
  Main:
    shell: python main.py

devTasks:
  Setup:
    shell: python setup.py

environmentConfigs:
  - environment_linux_amd64_freeze.yaml
  - environment_windows_amd64_freeze.yaml
  - conda.yaml

artifactsDir: output
PATH:
  - .
PYTHONPATH:
  - .
ignoreFiles:
  - .gitignore
```

**conda.yaml (example):**
```yaml
channels:
  - conda-forge

dependencies:
  - python=3.10.14
  # - uv           # Optional speed-up for pip installs
  - pip:
      - requests==2.32.5
      - pandas==2.2.3
```

### Helper Files

See skill directory for:
- `templates/` - Reference conda.yaml configs (basic, browser, data, api)
- `scripts/env_check.py` - Environment health check
- `scripts/validate_robot.py` - Config validation
- `reference.md` - Complete command reference
- `examples.md` - Practical recipes

## Examples

### Create a new Python robot
```
User: Create a new RCC robot for data processing
Assistant: I'll create a new RCC robot using the Python template.
[runs: rcc robot initialize -t <template-name> -d data-processor]
[runs: rcc task testrun (or rcc run) to build the environment]
[reads and shows robot.yaml]
[environment is now ready to use]
```

### Create browser automation robot
```
User: I need to automate web scraping with RCC
Assistant: I'll create a browser automation robot with Playwright.
[runs: rcc robot initialize -t <template-name> -d web-scraper]
[runs: rcc task testrun (or rcc run) to build the environment]
[environment builds with Playwright - ready to use]
```

### Debug environment issues
```
User: My RCC environment build is failing
Assistant: Let me diagnose the environment.
[runs: rcc configure diagnostics --robot robot.yaml]
[runs: rcc task script --silent -- pip list]
[checks conda.yaml for issues]
```

### Check available templates
```
User: What RCC templates are available?
Assistant: Let me list the available templates.
[runs: rcc robot initialize --json]
[displays template options with descriptions]
```

### Update dependencies with UV
```
User: Add pandas to my RCC project
Assistant: I'll update conda.yaml using uv for fast installation.
[reads conda.yaml]
[adds uv if desired/allowed]
[adds pandas to pip section]
[runs: rcc run to rebuild environment]
```

### Freeze dependencies for production
```
User: Prepare my robot for production deployment
Assistant: I'll create a frozen environment file.
[runs: rcc run to generate freeze file]
[copies environment_*_freeze.yaml to project]
[updates robot.yaml to use environmentConfigs]
```

### Run specific task
```
User: Run the Producer task in my robot
Assistant: I'll run the Producer task.
[runs: rcc run --task "Producer"]
```

### Interactive debugging
```
User: I need to debug my robot environment
Assistant: I'll open an interactive shell in the RCC environment.
[runs: rcc task shell]
```

### Pre-build environment after changes
```
User: I updated conda.yaml, rebuild the environment
Assistant: I'll rebuild the holotree environment.
[runs: rcc run or rcc task testrun]
[environment rebuilds with new dependencies]
[ready to use immediately]

---

## “Think like RCC” (holotree + enterprise guardrails)

When asked to “make RCC faster” or to change holotree behavior, keep these constraints in mind (distilled from maintainer discussions and hard-earned production experience):

- **Hololib/holotree can be shared.** Treat it as a security and integrity boundary. Skipping hash verification or trusting “local” files can be dangerous in shared mounts/multi-user/NFS scenarios.
- **Enterprises are weird.** Antivirus, network appliances, proxies, locked-down file permissions, and flaky network shares can surface edge cases that don’t reproduce on dev laptops.
- **Profile before/after.** Use `--pprof` (and optionally `--timeline`/`--trace`) to confirm the bottleneck and validate improvements.
- **Minimize new dependencies.** A smaller dependency tree reduces supply-chain risk and reduces friction with enterprise security tooling.
- **If you break it, you own the pieces.** Avoid platform/filesystem-specific “cleverness” unless you can test and support it across OS + filesystem combinations.

For deeper command syntax and recipes, use:

- `reference.md` (command reference)
- `examples.md` (practical recipes)
- `scripts/env_check.py` and `scripts/validate_robot.py`
```
