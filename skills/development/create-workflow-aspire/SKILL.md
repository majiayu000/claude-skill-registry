---
name: create-workflow-aspire
description: This skill creates a Dapr workflow application with .NET Aspire. Use this skill when the user asks to "create a workflow with Aspire", "write an Aspire workflow application" or "build a workflow app with .NET Aspire".
model: opus
---

# Create Dapr Workflow .NET Aspire Application

## Overview

This skill describes how to create a Dapr Workflow application using Aspire. The generated solution uses Aspire to orchestrate the Dapr sidecar, a Valkey state store, and the Diagrid Dev Dashboard as container resources.

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
- [Aspire CLI](https://aspire.dev/get-started/install-cli/) — install via `curl -sSL https://aspire.dev/install.sh | bash` or `irm https://aspire.dev/install.ps1 | iex`
- [Docker](https://www.docker.com/products/docker-desktop/) or [Podman](https://podman.io/docs/installation)
- [Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/)

Additional runtime dependencies (handled during project setup):

- NuGet package: `Dapr.Workflow` version `1.17.4` (ApiService)
- NuGet package: `Dapr.Workflow.Versioning` version `1.17.4` (ApiService)
- NuGet package: `CommunityToolkit.Aspire.Hosting.Dapr` version `13.0.0` (AppHost)
- NuGet package: `Aspire.Hosting.Valkey` version `13.1.2` (AppHost)

## Prerequisite Checks

**IMPORTANT: Run ALL of these checks BEFORE creating any files or folders. If any check fails, stop and inform the user with the relevant install link from the Prerequisites section. Do NOT proceed to Project Setup until all checks pass.**

### Step 1: Check the C# LSP plugin

Read the file at [`../shared/prereq-check-csharp-lsp.md`](../shared/prereq-check-csharp-lsp.md) and follow those instructions.

### Step 2: Detect Operating System

Read the file at [`../shared/prereq-detect-os.md`](../shared/prereq-detect-os.md) and follow those instructions.

### Step 3: Check .NET SDK

Read the file at [`../shared/prereq-check-dotnet-sdk.md`](../shared/prereq-check-dotnet-sdk.md) and follow those instructions.

### Step 4: Check Docker or Podman

Read the file at [`../shared/prereq-check-docker-podman.md`](../shared/prereq-check-docker-podman.md) and follow those instructions.

### Step 5: Check Dapr CLI

Read the file at [`../shared/prereq-check-dapr-cli.md`](../shared/prereq-check-dapr-cli.md) and follow those instructions.

### Step 6: Check Aspire CLI

Run `aspire --version` (on Windows, retry with `powershell -Command "aspire --version"` if needed). If not installed, inform the user they need to install the [Aspire CLI](https://learn.microsoft.com/en-us/dotnet/aspire/fundamentals/dotnet-aspire-cli) via `dotnet tool install -g dotnet-aspire`.

## Project Setup

Scaffold the solution using the Aspire CLI inside the current location where the terminal is open, then customize it for Dapr Workflow:

```shell
aspire new aspire-starter -n <SolutionRoot> -o <SolutionRoot>
```

After scaffolding:

1. **Remove the Web project** — The generated `<SolutionRoot>.Web` project is not needed. Delete the `<SolutionRoot>.Web` folder and remove its project reference from `<SolutionRoot>.AppHost.csproj` and the `.sln` file.
2. **Add NuGet packages**:
   ```shell
   dotnet add <SolutionRoot>.ApiService package Dapr.Workflow --version 1.17.4
   dotnet add <SolutionRoot>.ApiService package Dapr.Workflow.Versioning --version 1.17.4
   dotnet add <SolutionRoot>.AppHost package CommunityToolkit.Aspire.Hosting.Dapr --version 13.0.0
   dotnet add <SolutionRoot>.AppHost package Aspire.Hosting.Valkey --version 13.1.2
   ```
3. **Create/update source files** — Create all files described below, using `REFERENCE.md` for complete code.

### Folder structure

```
<SolutionRoot>/
├── .aspire/
│   └── settings.json
├── .gitignore
├── <SolutionRoot>.sln
├── local.http
├── <SolutionRoot>.ApiService/
│   ├── <SolutionRoot>.ApiService.csproj
│   ├── Program.cs
│   ├── appsettings.json
│   ├── appsettings.Development.json
│   ├── Properties/
│   │   └── launchSettings.json
│   ├── Models/
│   │   └── <ModelName>.cs
│   ├── Workflows/
│   │   └── <WorkflowName>.cs
│   └── Activities/
│       └── <ActivityName>.cs
├── <SolutionRoot>.AppHost/
│   ├── <SolutionRoot>.AppHost.csproj
│   ├── AppHost.cs
│   ├── appsettings.json
│   ├── appsettings.Development.json
│   ├── Properties/
│   │   └── launchSettings.json
│   └── Resources/
│       ├── statestore.yaml
│       └── statestore-dashboard.yaml
└── <SolutionRoot>.ServiceDefaults/
    ├── <SolutionRoot>.ServiceDefaults.csproj
    └── Extensions.cs
```

### .gitignore

Visual Studio style `.gitignore` file in the solution root. Ignores build output (`bin`, `obj`), debug/release folders, and other common .NET artifacts. See `REFERENCE.md` for full example.

### AppHost.cs

Configures Dapr via `AddDapr()`, adds a Valkey cache container on port 16379, registers the ApiService project with `WithDaprSidecar()`, and adds the Diagrid Dashboard as a container resource. See `REFERENCE.md` for full example and key points.

### AppHost .csproj

Uses `Aspire.AppHost.Sdk`, references `CommunityToolkit.Aspire.Hosting.Dapr` and `Aspire.Hosting.Valkey` packages, includes a project reference to ApiService, and copies Resources to output. See `REFERENCE.md` for full example.

### Resources/statestore.yaml

State store component for the apiservice Dapr sidecar. Uses `localhost:16379` to connect to the Valkey container managed by Aspire. See `REFERENCE.md` for full example and key points.

### Resources/statestore-dashboard.yaml

State store component for the Diagrid Dashboard container. Uses `host.docker.internal:16379` because the dashboard runs in a Docker container and needs to reach Valkey on the host. Scoped to `diagrid-dashboard`. See `REFERENCE.md` for full example and key points.

### ApiService Program.cs

Same pattern as the dotnet skill but adds `builder.AddServiceDefaults()` at the start and `app.MapDefaultEndpoints()` before `app.Run()`. Uses `AddDaprWorkflow` to register workflow and activity types. Uses `DaprWorkflowClient` to schedule workflow instances and query status via HTTP endpoints. Includes start, status, pause, resume, and terminate endpoints. See `REFERENCE.md` for full example and key points.

### ApiService .csproj

Standard ASP.NET Core web project targeting `net10.0` with `Dapr.Workflow` and `Dapr.Workflow.Versioning` packages and a project reference to ServiceDefaults. See `REFERENCE.md` for full example.

### Models

Record types for workflow and activity input/output, placed in a `Models` folder. Must be serializable since Dapr persists workflow state. See `REFERENCE.md` for full example and key points.

### Workflow Class

Inherits from `Workflow<TInput, TOutput>`, overrides `RunAsync`, and orchestrates activities via `context.CallActivityAsync`. Must be `internal sealed`. Place in a `Workflows` folder/namespace. See `REFERENCE.md` for full example, key points, determinism rules, and workflow patterns (chaining, fan-out/fan-in, sub-workflows).

### Activity Class

Inherits from `WorkflowActivity<TInput, TOutput>`, overrides `RunAsync`, and contains the actual business logic. Must be `internal sealed`. Place in an `Activities` folder/namespace. See `REFERENCE.md` for full example and key points.

### ServiceDefaults Extensions.cs

Template-generated file that adds OpenTelemetry, health checks, service discovery, and resilience. No modifications needed — keep as scaffolded by `aspire new`. See `REFERENCE.md` for reference.

### <SolutionRoot>.ApiService.http

HTTP request file for testing the workflow endpoints. Contains a `start` request (POST) to schedule a new workflow instance and a `status` request (GET) to query the workflow state. See `REFERENCE.md` for full example.

## Verify

**IMPORTANT: After Project Setup you MUST show these exact verification instructions:**

1. Run `dotnet build` on the `.sln` file to check for build errors.
2. Instruct the user to start the application with `aspire run` in the solution root to start the Aspire-orchestrated workflow app.

## Create README.md

**IMPORTANT: After Verify you MUST run these instructions:**

Create a README.md file inside the `<SolutionRoot>` folder.

The README contains the following sections:
1. Summary of what this folder contains.
2. Architecture description that explains the technology stack (Aspire, Dapr Workflow, Valkey, ServiceDefaults) and prerequisites to run it locally. **DO NOT suggest to run Redis or Valkey separately since Aspire manages it as a container resource.**
3. A mermaid diagram that explains the workflow.
4. How to start the application using `aspire run`.
5. List the available endpoints in the ApiService `Program.cs` file and provide examples how to call these using curl. Also include a link to the `<SolutionRoot>.ApiService.http` file.
6. How to inspect the workflow execution using the Diagrid Dev Dashboard (managed by Aspire, accessible via the Aspire dashboard resource links).

## Show final message

**IMPORTANT: This is the LAST step. After Create README.md, your final output MUST be ONLY the message below — no preamble, no summary, no additional commentary, only replace the <SolutionRoot> with the actual value:**

The <SolutionRoot> workflow application is created. Open the README.md file in the <SolutionRoot> folder for a summary and instructions for running locally.
