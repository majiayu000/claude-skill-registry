---
name: stack
description: Load technology stack configurations with project templates, dependencies, and best practices. Supports dotnet, node, python, java, go.
argument-hint: "<tech> - Choose: dotnet, node, python, java, go"
---

# Technology Stack Loader

When invoked with `/stack <tech>`, load the corresponding technology stack configuration.

**Configuration File**: `C:\.claude\stacks\tech-stacks.yaml`

## Supported Stacks

### @dotnet (or /stack dotnet)
- **Runtime**: .NET 8
- **Framework**: ASP.NET Core, Minimal APIs
- **ORM**: Entity Framework Core 8
- **Testing**: xUnit, Moq, FluentAssertions
- **Build**: dotnet CLI, NuGet

**Commands**:
```bash
dotnet build --configuration Release
dotnet test --collect:"XPlat Code Coverage"
dotnet run
```

### @node (or /stack node)
- **Runtime**: Node.js 20.x LTS
- **Language**: TypeScript 5.3+
- **Frontend**: React 18, Vite
- **Backend**: Express, Fastify
- **Testing**: Jest, Vitest, Playwright

**Commands**:
```bash
npm install
npm run dev
npm run build
npm test
```

### @python (or /stack python)
- **Runtime**: Python 3.11+
- **Framework**: FastAPI, Django
- **ORM**: SQLAlchemy 2.0
- **Testing**: pytest, pytest-cov
- **Build**: Poetry, pip

**Commands**:
```bash
poetry install
poetry run uvicorn main:app --reload
poetry run pytest
```

### @java (or /stack java)
- **Runtime**: Java 21 (Temurin)
- **Framework**: Spring Boot 3.2
- **ORM**: Spring Data JPA, Hibernate 6
- **Testing**: JUnit 5, Mockito
- **Build**: Maven 3.9, Gradle 8.5

**Commands**:
```bash
mvn clean package
mvn test
mvn spring-boot:run
```

### @go (or /stack go)
- **Runtime**: Go 1.22+
- **Framework**: Gin, Echo, stdlib
- **ORM**: GORM, sqlx
- **Testing**: go test, testify
- **Build**: go build

**Commands**:
```bash
go mod init
go build -o bin/app ./cmd/app
go test ./...
```

## Usage
1. Load stack: `/stack dotnet`
2. Get project structure, dependencies, and patterns
3. Combine: `@dotnet @arch:ms @deploy:k8s`
