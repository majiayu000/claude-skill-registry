---
name: .net-new-project
description: Create a new .NET 8 Web API solution following Clean Architecture principles.
---

# .NET 8 Clean Architecture Project Generator

This skill guides the creation of a new .NET 8 Web API solution using Clean Architecture.
**IMPORTANT:** Do NOT generate code files manually. Use the CLI commands provided below to scaffold the solution and projects.

## Prerequisite

- .NET 8 SDK installed (`dotnet --version`)

## Directory Structure

The final structure will look like this:

```
SolutionName/
├── src/
│   ├── SolutionName.Domain/        # Core business logic, entities, interfaces (No dependencies)
│   ├── SolutionName.Application/   # Use cases, DTOs, interfaces (Depends on Domain)
│   ├── SolutionName.Infrastructure/ # External concerns, DB, file system (Depends on Application)
│   └── SolutionName.Api/           # Presentation layer (Depends on Application, Infrastructure)
├── tests/                          # Unit and Integration tests
└── SolutionName.sln
```

## Step-by-Step Instructions

### 1. Create Solution

Run these commands in the terminal:

```bash
# Create solution file
dotnet new sln -n __SOLUTION_NAME__
```

### 2. Create Projects (Clean Architecture Layers)

```bash
# Create src directory
mkdir src

# DOMAIN Layer (Class Library)
dotnet new classlib -n __SOLUTION_NAME__.Domain -o src/__SOLUTION_NAME__.Domain

# APPLICATION Layer (Class Library)
dotnet new classlib -n __SOLUTION_NAME__.Application -o src/__SOLUTION_NAME__.Application

# INFRASTRUCTURE Layer (Class Library)
dotnet new classlib -n __SOLUTION_NAME__.Infrastructure -o src/__SOLUTION_NAME__.Infrastructure

# API Layer (Web API)
dotnet new webapi -n __SOLUTION_NAME__.Api -o src/__SOLUTION_NAME__.Api --use-controllers
```

### 3. Establish Dependencies

```bash
# Application -> Domain
dotnet add src/__SOLUTION_NAME__.Application reference src/__SOLUTION_NAME__.Domain

# Infrastructure -> Application
dotnet add src/__SOLUTION_NAME__.Infrastructure reference src/__SOLUTION_NAME__.Application

# Api -> Application
dotnet add src/__SOLUTION_NAME__.Api reference src/__SOLUTION_NAME__.Application

# Api -> Infrastructure
dotnet add src/__SOLUTION_NAME__.Api reference src/__SOLUTION_NAME__.Infrastructure
```

### 4. Add Projects to Solution

```bash
dotnet sln add src/__SOLUTION_NAME__.Domain
dotnet sln add src/__SOLUTION_NAME__.Application
dotnet sln add src/__SOLUTION_NAME__.Infrastructure
dotnet sln add src/__SOLUTION_NAME__.Api
```

### 5. Cleanup

- Remove default `Class1.cs` and `WeatherForecast.cs` files from all projects.

## Verification

Run `dotnet build` to ensure the solution builds correctly.


## Parent Hub
- [_backend-mastery](../_backend-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-feature-lifecycle](../_workflow-feature-lifecycle/SKILL.md)
