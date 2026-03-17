---
name: generate-api-client
description: Generate typed API client from OpenAPI/Swagger specification
argument-hint: "<openapi-url-or-path> [--lang=typescript|csharp]"
tags: [codegen, openapi, api, client]
user-invocable: true
---

# Generate Typed API Client from OpenAPI

Generate a fully typed HTTP client from an OpenAPI/Swagger specification.

## For .NET (NSwag)
```bash
dotnet tool install -g NSwag.ConsoleCore
nswag openapi2csclient /input:swagger.json /output:ApiClient.cs /namespace:MyApp.ApiClients /className:SourcingApiClient /generateClientInterfaces:true /injectHttpClient:true
```

Register in DI:
```csharp
builder.Services.AddHttpClient<ISourcingApiClient, SourcingApiClient>(client =>
    client.BaseAddress = new Uri(config["ApiBaseUrl"]));
```

## For TypeScript (openapi-typescript + openapi-fetch)
```bash
npm install openapi-typescript openapi-fetch
npx openapi-typescript ./openapi.yaml -o ./src/api/schema.d.ts
```

Usage:
```typescript
import createClient from "openapi-fetch";
import type { paths } from "./api/schema";
const client = createClient<paths>({ baseUrl: "http://localhost:5000" });
const { data } = await client.GET("/api/candidates/{id}", { params: { path: { id: "c-001" } } });
```

## For .NET (Microsoft Kiota)
```bash
dotnet tool install -g Microsoft.OpenApi.Kiota
kiota generate -l CSharp -d openapi.yaml -c SourcingClient -n MyApp.ApiClients -o ./Generated
```

## Arguments
- `<openapi-url-or-path>`: URL or path to OpenAPI spec
- `--lang=<typescript|csharp>`: Target language (default: csharp)