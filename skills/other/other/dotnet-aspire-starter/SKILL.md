---
name: dotnet-aspire-starter
description: Creates production-ready .NET 10 Aspire projects with ASP.NET MVC + Razor + TypeScript frontend, REST API backend, Entity Framework, OpenTelemetry observability, and Polly resilience. Use when asked to create a new .NET web application, scaffold a .NET Aspire project, set up a full-stack .NET solution with frontend and API, configure OpenTelemetry for .NET, add Polly resilience patterns, or start a new C# project with modern best practices. Supports OIDC authentication preparation and Grafana-ready telemetry.
---

# .NET Aspire Starter

Create production-ready .NET 10 Aspire projects with minimal friction. This skill transforms a project idea into a fully configured solution with frontend, backend API, database access, observability, and resilience patterns.

## What This Skill Creates

A complete .NET Aspire solution including:

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Orchestrator** | .NET Aspire | Service orchestration, local development, cloud deployment |
| **Frontend** | ASP.NET MVC + Razor + TypeScript + CSS | User-facing web application |
| **Backend API** | ASP.NET MVC REST API | Business logic and data access |
| **Database** | Entity Framework Core | ORM with code-first migrations |
| **Observability** | OpenTelemetry + OTLP | Logs, metrics, traces (Grafana-ready) |
| **Resilience** | Polly.NET | Circuit breakers, retries, timeouts |
| **Authentication** | OIDC (prepared) | Ready-to-enable identity integration |

---

## Quick Start Workflow

**User provides**: A project idea (e.g., "Build me a task management app")

**This skill creates**: A complete .NET solution ready for feature development

### Step 1: Gather Project Details

Ask the user for:
1. **Project name** (e.g., "TaskManager", "InventoryTracker")
2. **Brief description** (1-2 sentences)
3. **Target output path** (where to create the solution)

### Step 2: Run the Scaffold Script

The scaffolder creates a base .NET Aspire project using the official template, then adds skill-specific enhancements (coding standards, AI context, VS Code configuration).

```bash
# Run as a C# script directly (no compilation needed)
dotnet run scripts/ScaffoldAspireProject/Program.cs -- \
  --name "TaskManager" \
  --description "A task management application for teams" \
  --output "./projects"
```

Or build once and reuse the executable:

```bash
# Build the scaffolder (first time only)
dotnet build scripts/ScaffoldAspireProject/ScaffoldAspireProject.csproj -c Release

# Run the compiled executable
./scripts/ScaffoldAspireProject/bin/Release/net10.0/ScaffoldAspireProject \
  --name "TaskManager" \
  --description "A task management application for teams" \
  --output "./projects"
```

### Step 3: Initial Configuration

After scaffolding, guide the user through:

1. **Database connection**: Update `appsettings.json` with connection string
2. **Initial entity model**: Create the first domain entity in the API project
3. **First migration**: Run `dotnet ef migrations add Initial`

See [Initial Setup Guide](./references/initial-setup.md) for detailed steps.

### Step 4: Begin Feature Development

The user can now focus on their idea. The boilerplate is complete:
- Create entities in `{ProjectName}.Api/Models/`
- Add controllers in `{ProjectName}.Api/Controllers/`
- Create views in `{ProjectName}.Web/Views/`
- Write TypeScript in `{ProjectName}.Web/Scripts/`

---

## How It Works

The scaffolder in two steps:

1. **Base Project Creation**: Runs `dotnet new aspire-starter` with your project name
   - Creates official Microsoft Aspire project structure
   - Generates AppHost, ServiceDefaults, Api, and Web projects
   - Includes OpenTelemetry and Polly integration

2. **Skill-Specific Enhancements**: Adds on top:
   - **Coding Standards**: `.editorconfig` and `Directory.Build.props` with Microsoft C# conventions
   - **AI Context**: `.github/copilot-instructions.md` and `docs/ARCHITECTURE.md` for GitHub Copilot/Claude
   - **Developer Experience**: VS Code configuration for debugging and build tasks

This approach keeps you aligned with Microsoft's official template while adding production-ready context and standards.

---

## Project Structure

The scaffold creates this structure (plus everything from `dotnet new aspire-starter`):

```
{ProjectName}/
├── {ProjectName}.sln
├── {ProjectName}.AppHost/              # Aspire orchestrator (from template)
├── {ProjectName}.ServiceDefaults/      # Shared config (from template)
├── {ProjectName}.Api/                  # REST API backend (from template)
├── {ProjectName}.Web/                  # MVC + Razor frontend (from template)
├── Directory.Build.props                # Our: Microsoft coding standards
├── .editorconfig                        # Our: Code style enforcement
├── .github/
│   └── copilot-instructions.md         # Our: AI coding context
├── .vscode/
│   ├── settings.json                   # Our: VS Code config
│   ├── launch.json                     # Our: Debug configuration
│   └── tasks.json                      # Our: Build tasks
└── docs/
    └── ARCHITECTURE.md                 # Our: Architecture reference
```

---

## Feature Configuration

### OpenTelemetry (Enabled by Default)

Template includes full OpenTelemetry setup. See [Telemetry Setup](./references/telemetry-setup.md) for:

- Enabling Grafana integration
- Custom metrics and traces
- Structured logging patterns
- Production configuration

### Polly Resilience (Enabled by Default)

Template includes `Microsoft.Extensions.Http.Resilience` with sensible defaults. See [Polly Configuration](./references/polly-configuration.md) for:

- Default circuit breaker thresholds
- Retry policies
- Timeout configuration
- Custom resilience strategies

### OIDC Authentication (Prepared, Not Enabled)

Authentication scaffolding is in place but commented out. See [OIDC Preparation](./references/oidc-preparation.md) for:



- Enabling OIDC in frontend and API
- Shared authentication between layers
- Token propagation patterns
- Provider-specific setup (Azure AD, Auth0, Keycloak)

---

## Coding Standards

This skill enforces Microsoft coding standards via:

- **EditorConfig**: Consistent formatting across IDEs
- **.NET Analyzers**: Enabled with `TreatWarningsAsErrors`
- **Nullable Reference Types**: Enabled by default

See [Coding Standards Reference](./references/coding-standards.md) for the complete style guide.

---

## Development Commands

After scaffolding, these commands are available:

```bash
# Run the full solution (frontend + API + database)
dotnet run --project {ProjectName}.AppHost

# Run migrations
dotnet ef migrations add {MigrationName} --project {ProjectName}.Api
dotnet ef database update --project {ProjectName}.Api

# Build TypeScript
npm run build --prefix {ProjectName}.Web

# Watch TypeScript during development
npm run watch --prefix {ProjectName}.Web

# Run tests
dotnet test
```

---

## VS Code & Visual Studio Template Usage

For maximum reuse, this skill can generate templates for direct IDE use.

### VS Code Custom Snippets

The scaffold creates `.vscode/` configurations including:
- Launch configurations for debugging
- Task runners for build/watch
- Recommended extensions

### Visual Studio Template Export

To create a reusable VS template from the scaffolded project:

```bash
dotnet new --install ./{ProjectName}/ --force
```

This registers the project as a `dotnet new` template. See [Template Export Guide](./references/template-export.md) for multi-project template creation.

---

## Maximizing AI Assistant Effectiveness

The scaffold creates documentation that provides context for AI coding assistants:

### GitHub Copilot

The generated `.github/copilot-instructions.md` provides:
- Solution architecture overview
- Coding patterns used in the project
- Entity/controller/view conventions
- Testing patterns

### Claude / Claude Code

The generated `docs/ARCHITECTURE.md` serves as context for:
- Understanding project structure
- Following established patterns
- Maintaining consistency across features

**Recommendation**: When starting new features, reference these files in your prompts to maintain consistency.

---

## References

- [Initial Setup Guide](./references/initial-setup.md) - Post-scaffold configuration steps
- [Coding Standards](./references/coding-standards.md) - C# style guide and analyzer configuration
- [Telemetry Setup](./references/telemetry-setup.md) - OpenTelemetry configuration and Grafana integration
- [Polly Configuration](./references/polly-configuration.md) - Resilience patterns and customization
- [OIDC Preparation](./references/oidc-preparation.md) - Authentication enablement guide
- [Template Export](./references/template-export.md) - Creating reusable VS/VS Code templates

---

## Troubleshooting

### Script Execution Issues

**Missing .NET SDK or old version:**
```bash
# Check version (need .NET 10.0+)
dotnet --version

# Install from https://dotnet.microsoft.com/download
```

**dotnet new aspire-starter template not found:**
```bash
# Update .NET and workload
dotnet workload update
dotnet workload install aspire
dotnet new --list | grep aspire  # Verify installation
```

**Restore dependencies:**
```bash
cd scripts/ScaffoldAspireProject
dotnet restore
```

### Build Errors After Scaffold

**Missing workload error:**
```bash
dotnet workload install aspire
```

**TypeScript compilation errors:**
```bash
cd {ProjectName}.Web && npm install
```

### Database Connection Issues

Ensure the connection string in `appsettings.json` matches your database. For local development, the scaffold defaults to SQLite.
