---
name: generate-typed-client
description: Generate typed HTTP client with Microsoft Kiota
argument-hint: "<openapi-spec> [--namespace=MyApp.Client]"
tags: [codegen, kiota, api, microsoft]
user-invocable: true
---

# Generate Typed HTTP Client with Microsoft Kiota

Generate a strongly-typed HTTP API client using Microsoft Kiota.

## Steps
1. Install: `dotnet tool install -g Microsoft.OpenApi.Kiota`
2. Search: `kiota search <api-name>`
3. Generate:
   ```bash
   kiota generate -l CSharp -d https://api.example.com/openapi.json -c ExampleApiClient -n MyApp.ApiClients -o ./src/Generated
   ```
4. Add packages:
   ```bash
   dotnet add package Microsoft.Kiota.Abstractions
   dotnet add package Microsoft.Kiota.Http.HttpClientLibrary
   dotnet add package Microsoft.Kiota.Serialization.Json
   ```
5. Use:
   ```csharp
   var authProvider = new AnonymousAuthenticationProvider();
   var adapter = new HttpClientRequestAdapter(authProvider);
   var client = new ExampleApiClient(adapter);
   var candidates = await client.Api.Candidates.GetAsync();
   ```

Supported languages: CSharp, TypeScript, Java, Go, Python, PHP, Ruby, Swift

## Arguments
- `<openapi-spec>`: URL or path to OpenAPI specification
- `--namespace=<ns>`: Root namespace for generated code
- `--lang=<CSharp|TypeScript|Go|Python>`: Target language