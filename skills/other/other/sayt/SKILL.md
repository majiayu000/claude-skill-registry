---
name: sayt-lifecycle
description: >
  Unified development lifecycle tool. Use when the user asks about building,
  testing, setting up, deploying, or configuring a development environment.
  Teaches how to write and fix the configuration files behind each verb
  and how to configure sayt itself.
allowed-tools: Bash(sayt:*)
---

# sayt-lifecycle — Unified Development Lifecycle

sayt is a small CLI that provides consistent verbs for the entire software development lifecycle. It reuses configuration you already have (.vscode/tasks.json, .mise.toml, compose.yaml, skaffold.yaml) so there is zero drift between your IDE, CI, and terminal.

## The 5 Verb Pairs

| Verb pair | What it does | Underlying tool | Config file |
|-----------|-------------|----------------|-------------|
| `sayt setup` / `sayt doctor` | Install and verify toolchains | [mise](https://mise.jdx.dev/) | `.mise.toml` |
| `sayt build` / `sayt test` | Compile and run unit tests | [vscode-task-runner](https://pypi.org/project/vscode-task-runner/) | `.vscode/tasks.json` |
| `sayt generate` / `sayt lint` | Generate code, lint config | [CUE](https://cuelang.org/) + [gomplate](https://gomplate.ca/) | `.say.cue` / `.say.yaml` |
| `sayt launch` / `sayt integrate` | Containerize and integration-test | [docker compose](https://docs.docker.com/compose/) | `Dockerfile` + `compose.yaml` |
| `sayt release` / `sayt verify` | Deploy and validate in production | [skaffold](https://skaffold.dev/) | `skaffold.yaml` |

## Seven-Environment Model

sayt organizes the development lifecycle into seven environments, each adding a layer of confidence:

1. **pkg** — Package manager (mise). Tools are installed and available.
2. **cli** — CLI tools (cue, gomplate). Code generation and validation work.
3. **ide** — IDE integration (vscode-task-runner). Build and test tasks run from your editor.
4. **cnt** — Container (docker). Code runs identically across machines.
5. **k8s** — Kubernetes (kind, skaffold). Full-stack preview deployments work.
6. **cld** — Cloud (gcloud). Staging deployment is live.
7. **xpl** — Crossplane. Production infrastructure is managed as code.

Run `sayt doctor` to check which environments are ready.

## How sayt Reuses Existing Config

sayt does **not** invent new configuration formats. It delegates to tools you already configure:

- **`.mise.toml`** — You probably already specify tool versions. `sayt setup` runs `mise install`.
- **`.vscode/tasks.json`** — Your IDE already knows how to build/test. `sayt build` and `sayt test` run those same tasks via vscode-task-runner.
- **`compose.yaml`** — Your containers already define services. `sayt launch` runs `docker compose run --build develop`. `sayt integrate` runs `docker compose up integrate`.
- **`skaffold.yaml`** — Your deploy pipeline already has profiles. `sayt release` runs `skaffold run`.

## The TDD Loop

The core inner loop when developing with sayt:

```
edit code → sayt build → sayt test → fix → repeat
```

Once green, widen the loop:

```
sayt integrate → fix → (back to inner loop if needed)
```

When ready to ship:

```
sayt release → sayt verify
```

## When to Use Which Verb

| I want to... | Run |
|-------------|-----|
| Install project dependencies | `sayt setup` |
| Check if my environment is ready | `sayt doctor` |
| Generate code from templates/schemas | `sayt generate` |
| Validate generated code | `sayt lint` |
| Compile the project | `sayt build` |
| Run unit tests | `sayt test` |
| Start the app in a container | `sayt launch` |
| Run integration tests in containers | `sayt integrate` |
| Deploy to staging/production | `sayt release` |
| Run E2E tests against a deployment | `sayt verify` |

## Per-Verb Skill Reference

For detailed guidance on writing the configuration file for each verb, see [reference.md](./reference.md) or ask about a specific verb pair.

## Current sayt help

!`sayt help 2>&1 || echo "sayt not installed — see https://github.com/bonisoft3/sayt"`
