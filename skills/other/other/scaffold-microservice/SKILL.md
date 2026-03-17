---
name: scaffold-microservice
description: Scaffold a complete microservice with Controller-Service-Repository pattern for RH-OptimERP
argument-hint: "<service-name> [--entities=Entity1,Entity2] [--port=5000]"
tags: [scaffold, microservice, dotnet, architecture, codegen]
user-invocable: true
---

# Scaffold Microservice

Generate a complete .NET 8 microservice following the RH-OptimERP Controller-Service-Repository pattern.

## What To Do

1. **Parse arguments**: Extract service name, entity list, and port.

2. **Create directory structure**:
   ```
   src/backend/{ServiceName}/
     Controllers/         -- One per entity
     Services/
       Interfaces/        -- I{Entity}Service.cs
       {Entity}Service.cs
     Repositories/
       Interfaces/        -- I{Entity}Repository.cs
       {Entity}Repository.cs
     Models/
       {Entity}.cs        -- Domain models
       DTOs/
         {Entity}Dto.cs   -- With ToDomain() and FromDomain()
     Program.cs           -- DI, CORS, Swagger, health checks
     {ServiceName}.csproj -- .NET 8, CosmosDB SDK 3.54
     appsettings.json
     appsettings.Development.json
     Dockerfile
   src/backend/Tests/{ServiceName}Tests/
     {Entity}ServiceTests.cs
     {ServiceName}Tests.csproj
   ```

3. **Generate each file** following these patterns:

   **Controller** (HTTP concerns only):
   ```csharp
   [ApiController]
   [Route("api/[controller]")]
   public class {Entity}Controller : ControllerBase
   {
       private readonly I{Entity}Service _service;
       public {Entity}Controller(I{Entity}Service service) => _service = service;

       [HttpGet("{id}")]
       public async Task<ActionResult<{Entity}Dto>> GetById(string id) { ... }

       [HttpGet]
       public async Task<ActionResult<PagedResult<{Entity}Dto>>> GetAll([FromQuery] int page = 1, [FromQuery] int size = 20) { ... }

       [HttpPost]
       public async Task<ActionResult<{Entity}Dto>> Create([FromBody] Create{Entity}Dto dto) { ... }
   }
   ```

   **Service** (business logic + validation):
   ```csharp
   public class {Entity}Service : I{Entity}Service
   {
       private readonly I{Entity}Repository _repository;
       public {Entity}Service(I{Entity}Repository repository) => _repository = repository;
   }
   ```

   **Repository** (CosmosDB SDK 3.54 direct):
   ```csharp
   public class {Entity}Repository : I{Entity}Repository
   {
       private readonly Container _container;
       public {Entity}Repository(CosmosClient client, IOptions<CosmosDbSettings> settings)
       {
           var db = client.GetDatabase(settings.Value.DatabaseName);
           _container = db.GetContainer("{entities}");
       }
   }
   ```

   **DTO** (static mapping methods):
   ```csharp
   public class {Entity}Dto
   {
       public static {Entity}Dto FromDomain({Entity} entity) => new() { ... };
       public {Entity} ToDomain() => new() { ... };
   }
   ```

4. **Program.cs** must include:
   - CosmosClient singleton with direct mode
   - All services and repositories registered via DI
   - CORS for React frontend (localhost:3000)
   - Swagger/OpenAPI
   - Health checks endpoint
   - Security headers middleware

5. **Dockerfile** (multi-stage):
   ```dockerfile
   FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
   WORKDIR /src
   COPY . .
   RUN dotnet publish -c Release -o /app
   FROM mcr.microsoft.com/dotnet/aspnet:8.0
   WORKDIR /app
   COPY --from=build /app .
   EXPOSE {port}
   ENTRYPOINT ["dotnet", "{ServiceName}.dll"]
   ```

6. **Verify**: `dotnet build` succeeds with zero warnings.

## GDPR Compliance
For entities containing personal data, add:
- `AnonymizeXxx()` method
- `IsAnonymized` flag
- Exclude PII from ToString() and logging

## Arguments
- `<service-name>`: Name of the microservice (PascalCase)
- `--entities=<list>`: Comma-separated entity names
- `--port=<n>`: HTTP port (default: 5000)
- `--with-gdpr`: Add GDPR compliance to all entities
- `--with-tests`: Generate test project (default: true)