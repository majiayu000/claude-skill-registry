---
name: create-workflow-dotnet
description: This skill creates a Dapr workflow application in .NET. Use this skill when the user asks to "create a workflow in .NET", "write a .NET workflow application" or "build a workflow app in C#".
model: opus
---

# Create Dapr Workflow .NET Application

## Overview

This skill describes how to create a Dapr Workflow application using .NET.

## Execution Order

You MUST follow these phases in strict order:
1. **Prerequisite Checks** — Run ALL checks. Stop if any fail.
2. **Project Setup** — Create all files and folders.
3. **Verify** — Verify that the project builds.
4. **Create README.md** — Create a readme that summarizes what is built and how to run & test the application. Do not provide instructions at the end of this phase.
5. **Show final message** - Your LAST output MUST be EXACTLY the message defined in the `## Show final message` section. Do NOT add any other text, summary, or commentary after it.

## Prerequisites

The following must be installed by the user before this skill can run:

- [.NET 10 SDK](https://dotnet.microsoft.com/en-us/download)
- [Docker](https://www.docker.com/products/docker-desktop/) or [Podman](https://podman.io/docs/installation)
- [Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/)

Additional runtime dependencies (handled during project setup):

- NuGet package: `Dapr.Workflow` version `1.16.1`
- Start the [Diagrid Dev Dashboard](https://www.diagrid.io/blog/improving-the-local-dapr-workflow-experience-diagrid-dashboard): `docker run -p 8080:8080 ghcr.io/diagridio/diagrid-dashboard:latest`

## Prerequisite Checks

**IMPORTANT: Run ALL of these checks BEFORE creating any files or folders. If any check fails, stop and inform the user with the relevant install link from the Prerequisites section. Do NOT proceed to Project Setup until all checks pass.**

### Step 1: Check the C# LSP plugin

Check if the `csharp-lsp@claude-plugins-official` plugin is installed. Do not run `claude plugin` from the session since that is not allowed. Check by inspecting the claude settings. If the plugin is not installed, instruct the user to exit claude code, run `claude plugin install csharp-lsp@claude-plugins-official` to install the C# language server plugin, restart claude code and enter the prompt again.

### Step 2: Detect Operating System

Run `uname -s 2>/dev/null || echo "Windows"` to determine the OS:
- **macOS**: `uname -s` returns `Darwin`. All tools are expected to be available in bash.
- **Linux**: `uname -s` returns `Linux`. All tools are expected to be available in bash.
- **Windows**: returns `Windows`. Tools may only be on the Windows PATH and not available in the bash shell. For each subsequent check, if the direct bash command fails, retry via `powershell -Command "<cmd>"` (Windows PowerShell) or `pwsh -Command "<cmd>"` (PowerShell 7+).

### Step 3: Check .NET SDK

Run `dotnet --version` (on Windows, retry with `powershell -Command "dotnet --version"` if needed). Verify the output starts with `10.`. If not installed or the version is below 10, inform the user they need to install the [.NET 10 SDK](https://dotnet.microsoft.com/en-us/download).

### Step 4: Check Docker or Podman

Run `docker info` (on Windows, retry with `powershell -Command "docker info"` if needed). If Docker is unavailable, try `podman info` (on Windows, retry with `powershell -Command "podman info"` if needed). At least one container runtime must be available and running. If neither is available, inform the user they need to install [Docker](https://www.docker.com/products/docker-desktop/) or [Podman](https://podman.io/docs/installation).

### Step 5: Check Dapr CLI

Run `dapr --version` (on Windows, retry with `powershell -Command "dapr --version"` if needed). Verify the output contains `1.16`. If not installed, inform the user they need to install the [Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/).

## Project Setup

Create the project root folder, then create a new ASP.NET Core web application inside it:

```shell
mkdir <ProjectRoot>
cd <ProjectRoot>
dotnet new web -n <ProjectName>
dotnet add <ProjectName> package Dapr.Workflow --version 1.16.1
```

The <ProjectName> should start with the <ProjectRoot> and end with `App`: <ProjectRoot>App.

### Folder structure

```
<ProjectRoot>/
├── .gitignore
├── dapr.yaml
├── local.http
├── resources/
│   └── statestore.yaml
└── <ProjectName>/
    ├── <ProjectName>.csproj
    ├── Program.cs
    ├── Properties/
    │   └── launchSettings.json
    ├── Models/
    │   └── <ModelName>.cs
    ├── Workflows/
    │   └── <WorkflowName>.cs
    └── Activities/
        └── <ActivityName>.cs
```

### .gitignore

Visual Studio style `.gitignore` file in the project root. Ignores build output (`bin`, `obj`), debug/release folders, and other common .NET artifacts. See `REFERENCE.md` for full example.

### dapr.yaml

Multi-app run file in the project root. Configures the Dapr sidecar and points to the resources folder. See `REFERENCE.md` for full example and key points.

### resources/statestore.yaml

Dapr Workflow requires a state store component (with `actorStateStore` set to `"true"`). See `REFERENCE.md` for full example and key points.

### Properties/launchSettings.json

Configures the application port, which must match `appPort` in `dapr.yaml`. See `REFERENCE.md` for full example.

### .csproj

Standard ASP.NET Core web project targeting `net10.0` with the `Dapr.Workflow` package. See `REFERENCE.md` for full example.

### Models

Record types for workflow and activity input/output, placed in a `Models` folder. Must be serializable since Dapr persists workflow state. See `REFERENCE.md` for full example and key points.

### Program.cs

Uses `AddDaprWorkflow` to register workflow and activity types. Uses `DaprWorkflowClient` to schedule workflow instances and query status via HTTP endpoints. See `REFERENCE.md` for full example and key points.

### Workflow Class

Inherits from `Workflow<TInput, TOutput>`, overrides `RunAsync`, and orchestrates activities via `context.CallActivityAsync`. Must be `internal sealed`. Place in a `Workflows` folder/namespace. See `REFERENCE.md` for full example, key points, determinism rules, and workflow patterns (chaining, fan-out/fan-in, sub-workflows).

### Activity Class

Inherits from `WorkflowActivity<TInput, TOutput>`, overrides `RunAsync`, and contains the actual business logic. Must be `internal sealed`. Place in an `Activities` folder/namespace. See `REFERENCE.md` for full example and key points.

### local.http

HTTP request file for testing the workflow endpoints. Contains a `start` request (POST) to schedule a new workflow instance and a `status` request (GET) to query the workflow state. Uses the `<app-port>` from `launchSettings.json`. See `REFERENCE.md` for full example.

## Verify

**IMPORTANT: After Project Setup you MUST show these exact verification instructions:**

1. Run `dotnet build` on the csproj file to check for build errors.
2. Instruct the user to start the application with `dapr run -f .` in the project root to start the workflow app.

## Create README.md

**IMPORTANT: After Verify you MUST run these instructions:**

Create a README.md file inside the <ProjectRoot> folder.

The README contains the following sections:
1. Summary of what this folder contains.
2. Architecture description that explains the technology stack and prerequisites to run it locally. **DO NOT suggest to run Redis separately since it's part of the Dapr installation and is running in a container already.**
3. A mermaid diagram that explains the workflow.
4. How to start the application using the Dapr CLI.
5. List the available endpoints in the Program.cs file and provide examples how to call these using curl. Also include a link to the `local.http` file. 
6. How to inspect the workflow execution using the Diagrid Dev Dashboard.
7. How to run the application with Diagrid Catalyst to visually inspect the workflow.

See `REFERENCE.md` for additional instructions on running locally and running with Catalyst.

## Show final message

**IMPORTANT: This is the LAST step. After Create README.md, your final output MUST be ONLY the message below — no preamble, no summary, no additional commentary, only replace the <ProjectRoot> with the actual value:**

The <ProjectRoot> workflow application is created. Open the README.md file in the <ProjectRoot> folder for a summary and instructions for running locally.