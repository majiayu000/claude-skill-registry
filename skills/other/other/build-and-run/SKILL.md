---
description: Build, run, and test the NovaTune .NET Aspire application
---
# Build and Run Skill

Build, run, and manage the NovaTune .NET Aspire application.

## Common Commands

All commands run from repository root: `/home/tassadar/Documents/GitHub/NovaTune`

### Build

```bash
# Restore packages
dotnet restore

# Build solution (warnings-as-errors enabled)
dotnet build

# Build specific project
dotnet build src/NovaTuneApp/NovaTuneApp.ApiService
```

### Run

```bash
# Run Aspire orchestration (starts all services)
dotnet run --project src/NovaTuneApp/NovaTuneApp.AppHost

# Run API service standalone
dotnet run --project src/NovaTuneApp/NovaTuneApp.ApiService

# Run web frontend standalone
dotnet run --project src/NovaTuneApp/NovaTuneApp.Web
```

### Code Quality

```bash
# Format code
dotnet format

# Verify formatting (CI check)
dotnet format --verify-no-changes
```

### Testing

```bash
# Run all tests
dotnet test

# Run tests with coverage
dotnet test /p:CollectCoverage=true

# Run specific test project
dotnet test src/NovaTuneApp/NovaTuneApp.Tests
dotnet test src/unit_tests
```

## Project Structure

| Project | Purpose |
|---------|---------|
| `NovaTuneApp.AppHost` | Aspire orchestration host |
| `NovaTuneApp.ApiService` | REST API endpoints |
| `NovaTuneApp.Web` | Blazor web frontend |
| `NovaTuneApp.ServiceDefaults` | Shared config (telemetry, resilience) |
| `NovaTuneApp.Tests` | Integration tests |
| `NovaTune.UnitTests` | Unit tests |

## Aspire Dashboard

When running with AppHost, access the Aspire dashboard at the URL shown in console output (typically `https://localhost:PORT`).

## Environment

- .NET 9.0 SDK required
- Docker for infrastructure dependencies
- Start infra first: `docker compose up -d`
