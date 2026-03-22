---
name: create-workflow-python
description: This skill creates a Dapr workflow application in Python. Use this skill when the user asks to "create a workflow in Python", "write a Python workflow application" or "build a workflow app in Python".
model: opus
---

# Create Dapr Workflow Python Application

## Overview

This skill describes how to create a Dapr Workflow application using Python.

## Execution Order

You MUST follow these phases in strict order:
1. **Prerequisite Checks** — Run ALL checks. Stop if any fail.
2. **Project Setup** — Create all files and folders.
3. **Verify** — Verify that the project builds.
4. **Create README.md** — Create a readme that summarizes what is built and how to run & test the application. Do not provide instructions at the end of this phase.
5. **Show final message** - Your LAST output MUST be EXACTLY the message defined in the `## Show final message` section. Do NOT add any other text, summary, or commentary after it.

## Prerequisites

The following must be installed by the user before this skill can run:

- [Python 3.12+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (Astral)
- [Docker](https://www.docker.com/products/docker-desktop/) or [Podman](https://podman.io/docs/installation)
- [Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/)

Additional runtime dependencies (handled during project setup):

- Python package: `dapr-ext-workflow` version `1.17.0`
- Start the [Diagrid Dev Dashboard](https://www.diagrid.io/blog/improving-the-local-dapr-workflow-experience-diagrid-dashboard): `docker run -p 8080:8080 ghcr.io/diagridio/diagrid-dashboard:latest`

## Prerequisite Checks

**IMPORTANT: Run ALL of these checks BEFORE creating any files or folders. If any check fails, stop and inform the user with the relevant install link from the Prerequisites section. Do NOT proceed to Project Setup until all checks pass.**

### Step 1: Check the Python LSP plugin

Read the file at [`../shared/prereq-check-python-lsp.md`](../shared/prereq-check-python-lsp.md) and follow those instructions.

### Step 2: Detect Operating System

Read the file at [`../shared/prereq-detect-os.md`](../shared/prereq-detect-os.md) and follow those instructions.

### Step 3: Check uv

Read the file at [`../shared/prereq-check-uv.md`](../shared/prereq-check-uv.md) and follow those instructions.

### Step 4: Check Python SDK version

Read the file at [`../shared/prereq-check-python-sdk.md`](../shared/prereq-check-python-sdk.md) and follow those instructions.

### Step 5: Check Docker or Podman

Read the file at [`../shared/prereq-check-docker-podman.md`](../shared/prereq-check-docker-podman.md) and follow those instructions.

### Step 6: Check Dapr CLI

Read the file at [`../shared/prereq-check-dapr-cli.md`](../shared/prereq-check-dapr-cli.md) and follow those instructions.

## Project Setup

Create the project root folder inside the current location where the terminal is open:

```shell
mkdir <ProjectRoot>
cd <ProjectRoot>
```

The <ProjectName> should start with the <ProjectRoot> and end with `-app`: <ProjectRoot>-app.

### Folder structure

```
<ProjectRoot>/
├── .gitignore
├── dapr.yaml
├── local.http
├── resources/
│   └── statestore.yaml
└── <ProjectName>/
    ├── pyproject.toml
    ├── main.py
    ├── models.py
    ├── workflow.py
    └── activities.py
```

### .gitignore

Python style `.gitignore` file in the project root. See `REFERENCE.md` for full example.

### dapr.yaml

Multi-app run file in the project root. Configures the Dapr sidecar and points to the resources folder. See `REFERENCE.md` for full example and key points.

### resources/statestore.yaml

Dapr Workflow requires a state store component (with `actorStateStore` set to `"true"`). See `REFERENCE.md` for full example and key points.

### pyproject.toml

Python configuration file used by packaging tools. See `REFERENCE.md` for full example.

### main.py

Main entry for the Python workflow application. See `REFERENCE.md` for full example.

### Models

Pydantic types for workflow and activity input/output, placed in a `models.py` file. Models must be serializable since Dapr persists workflow state. See `REFERENCE.md` for full example and key points.

### Workflow file

A workflow is defined using the @wfr.workflow(name="<NAME>") attribute. The workflow code is placed in a workflow.py file. See `REFERENCE.md` for full example, key points, determinism rules, and workflow patterns (chaining, fan-out/fan-in, sub-workflows).

### Activities file

A workflow activity is defined using the @wfr.activity(name="<NAME>") attribute. The activity code is placed in an `activities.py` file. See `REFERENCE.md` for full example and key points.

### local.http

HTTP request file for testing the workflow endpoints. Contains a `start` request (POST) to schedule a new workflow instance and a `status` request (GET) to query the workflow state. Uses the `<app-port>` from `dapr.yaml`. See `REFERENCE.md` for full example.

## Verify

**IMPORTANT: After Project Setup you MUST show these exact verification instructions:**

1. Run `uv venv` in the `<ProjectName>` folder to create a virtual environment.
2. Run `uv sync` in the `<ProjectName>` folder to install dependencies.
3. Instruct the user to start the application with `dapr run -f .` in the project root to start the workflow app.

## Create README.md

**IMPORTANT: After Verify you MUST run these instructions:**

Create a README.md file inside the <ProjectRoot> folder.

The README contains the following sections:
1. Summary of what this folder contains.
2. Architecture description that explains the technology stack and prerequisites to run it locally. **DO NOT suggest to run Redis separately since it's part of the Dapr installation and is running in a container already.**
3. A mermaid diagram that explains the workflow.
4. How to start the application using the Dapr CLI.
5. List the available endpoints in the main.py file and provide examples how to call these using curl. Also include a link to the `local.http` file.
6. How to inspect the workflow execution using the Diagrid Dev Dashboard.
7. How to run the application with Diagrid Catalyst to visually inspect the workflow.

See `REFERENCE.md` for additional instructions on running locally and running with Catalyst.

## Show final message

**IMPORTANT: This is the LAST step. After Create README.md, your final output MUST be ONLY the message below — no preamble, no summary, no additional commentary, only replace the <ProjectRoot> with the actual value:**

The <ProjectRoot> workflow application is created. Open the README.md file in the <ProjectRoot> folder for a summary and instructions for running locally.
