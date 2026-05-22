---
name: generate-service
description: Generate .NET service with interface, implementation, and DI registration
argument-hint: "<service-name> [--with-caching] [--with-validation]"
tags: [codegen, dotnet, service, backend]
user-invocable: true
---

# Generate .NET Service

Generate a service layer with interface, implementation, validation, and DI registration.

## What To Do

1. **Generate IService interface** with async methods
2. **Generate Service implementation** with constructor injection
3. **Add validation logic** in service methods
4. **Register in DI** (Program.cs): `builder.Services.AddScoped<IXxxService, XxxService>()`
5. **Generate unit tests** with mocked repository

## Arguments
- `<service-name>`: Service name (without "Service" suffix)
- `--with-caching`: Add IMemoryCache integration
- `--with-validation`: Add FluentValidation rules