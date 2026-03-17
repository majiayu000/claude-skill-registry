---
name: umbraco-openapi-client
description: Set up OpenAPI client for authenticated API calls in Umbraco backoffice (REQUIRED for custom APIs)
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, Bash
---

# Umbraco OpenAPI Client Setup

## CRITICAL: Why This Matters

**NEVER use raw `fetch()` calls for Umbraco backoffice API communication.** Raw fetch calls will result in 401 Unauthorized errors because they don't include the bearer token authentication that Umbraco requires.

**ALWAYS use a generated OpenAPI client** configured with Umbraco's auth context. This ensures:
- Proper bearer token authentication
- Type-safe API calls
- Automatic token refresh handling

## When to Use This

Use this pattern whenever you:
- Create custom C# API controllers with `[BackOfficeRoute]`
- Need to call your custom APIs from the backoffice frontend
- Build trees, workspaces, or any UI that loads data from custom endpoints

## Setup Overview

The setup has 4 parts:
1. **C# Backend**: Controller with Swagger/OpenAPI documentation
2. **Client Dependencies**: `@hey-api/openapi-ts` and `@hey-api/client-fetch`
3. **Generation Script**: Fetches swagger.json and generates TypeScript client
4. **Entry Point Configuration**: Configures client with Umbraco auth

## Step-by-Step Implementation

### 1. C# Backend Setup (Swagger/OpenAPI)

Your API must be exposed via Swagger. Create a composer:

```csharp
// Composers/MyApiComposer.cs
using Asp.Versioning;
using Microsoft.Extensions.Options;
using Microsoft.OpenApi.Models;
using Swashbuckle.AspNetCore.SwaggerGen;
using Umbraco.Cms.Api.Common.OpenApi;
using Umbraco.Cms.Core.Composing;
using Umbraco.Cms.Web.Common.ApplicationBuilder;

namespace MyExtension.Composers;

public class MyApiComposer : IComposer
{
    public void Compose(IUmbracoBuilder builder)
    {
        // Register the API and Swagger
        builder.Services.AddSingleton<ISchemaIdHandler, MySchemaIdHandler>();
        builder.Services.AddTransient<IConfigureOptions<SwaggerGenOptions>, MySwaggerGenOptions>();
        builder.Services.Configure<UmbracoPipelineOptions>(options =>
        {
            options.AddFilter(new UmbracoPipelineFilter(Constants.ApiName)
            {
                SwaggerPath = $"/umbraco/swagger/{Constants.ApiName.ToLower()}/swagger.json",
                SwaggerRoutePrefix = $"{Constants.ApiName.ToLower()}",
            });
        });
    }
}

// Swagger schema ID handler
public class MySchemaIdHandler : SchemaIdHandler
{
    public override bool CanHandle(Type type)
        => type.Namespace?.StartsWith("MyExtension") ?? false;
}

// Swagger generation options
public class MySwaggerGenOptions : IConfigureOptions<SwaggerGenOptions>
{
    public void Configure(SwaggerGenOptions options)
    {
        options.SwaggerDoc(
            Constants.ApiName,
            new OpenApiInfo
            {
                Title = "My Extension API",
                Version = "1.0",
            });
    }
}

// Constants
public static class Constants
{
    public const string ApiName = "myextension";
}
```

### 2. Client package.json Dependencies

Add to your `Client/package.json`:

```json
{
  "scripts": {
    "generate-client": "node scripts/generate-openapi.js https://localhost:44325/umbraco/swagger/myextension/swagger.json"
  },
  "devDependencies": {
    "@hey-api/client-fetch": "^0.10.0",
    "@hey-api/openapi-ts": "^0.66.7",
    "chalk": "^5.4.1",
    "node-fetch": "^3.3.2"
  }
}
```

### 3. Generation Script

Create `Client/scripts/generate-openapi.js`:

```javascript
import fetch from "node-fetch";
import chalk from "chalk";
import { createClient, defaultPlugins } from "@hey-api/openapi-ts";

console.log(chalk.green("Generating OpenAPI client..."));

const swaggerUrl = process.argv[2];
if (swaggerUrl === undefined) {
  console.error(chalk.red(`ERROR: Missing URL to OpenAPI spec`));
  process.exit(1);
}

// Ignore self-signed certificates on localhost
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

console.log(`Fetching OpenAPI definition from ${chalk.yellow(swaggerUrl)}`);

fetch(swaggerUrl)
  .then(async (response) => {
    if (!response.ok) {
      console.error(chalk.red(`ERROR: ${response.status} ${response.statusText}`));
      return;
    }

    await createClient({
      input: swaggerUrl,
      output: "src/api",
      plugins: [
        ...defaultPlugins,
        {
          name: "@hey-api/client-fetch",
          bundle: true,
          exportFromIndex: true,
          throwOnError: true,
        },
        {
          name: "@hey-api/typescript",
          enums: "typescript",
        },
        {
          name: "@hey-api/sdk",
          asClass: true,
        },
      ],
    });

    console.log(chalk.green("Client generated successfully!"));
  })
  .catch((error) => {
    console.error(`ERROR: ${chalk.red(error.message)}`);
  });
```

### 4. Entry Point Configuration (CRITICAL)

Configure the generated client with Umbraco's auth context in your entry point:

```typescript
// src/entrypoints/entrypoint.ts
import type { UmbEntryPointOnInit, UmbEntryPointOnUnload } from "@umbraco-cms/backoffice/extension-api";
import { UMB_AUTH_CONTEXT } from "@umbraco-cms/backoffice/auth";
import { client } from "../api/client.gen.js";

export const onInit: UmbEntryPointOnInit = (host, _extensionRegistry) => {
  // CRITICAL: Configure the OpenAPI client with authentication
  host.consumeContext(UMB_AUTH_CONTEXT, (authContext) => {
    if (!authContext) return;

    const config = authContext.getOpenApiConfiguration();

    client.setConfig({
      baseUrl: config.base,
      credentials: config.credentials,
      auth: config.token,  // This provides the bearer token!
    });

    console.log("API client configured with auth");
  });
};

export const onUnload: UmbEntryPointOnUnload = (_host, _extensionRegistry) => {
  // Cleanup if needed
};
```

### 5. Using the Generated Client

After running `npm run generate-client`, use the generated service:

```typescript
// In your workspace context, repository, or data source
import { MyExtensionService } from "../api/index.js";

// The client handles auth automatically!
const response = await MyExtensionService.getItems({
  query: { skip: 0, take: 50 },
});

const item = await MyExtensionService.getItem({
  path: { id: "some-guid" },
});

await MyExtensionService.createItem({
  body: { name: "New Item", value: 123 },
});
```

## Generation Workflow

1. **Start Umbraco** - The swagger.json endpoint must be accessible
2. **Run generation**: `npm run generate-client`
3. **Generated files** appear in `src/api/`:
   - `types.gen.ts` - TypeScript types from your C# models
   - `sdk.gen.ts` - Service class with typed methods
   - `client.gen.ts` - HTTP client configuration
   - `index.ts` - Re-exports everything

## Common Mistakes

### ❌ WRONG: Raw fetch
```typescript
// This will get 401 Unauthorized!
const response = await fetch('/umbraco/myextension/api/v1/items');
```

### ❌ WRONG: fetch with credentials only
```typescript
// Still fails - cookies don't work for Management API
const response = await fetch('/umbraco/myextension/api/v1/items', {
  credentials: 'include'
});
```

### ✅ CORRECT: Generated OpenAPI client
```typescript
// Client is configured with bearer token in entry point
const response = await MyExtensionService.getItems();
```

## Reference Example

See the complete working implementation in:
- `examples/notes-wiki/Client/` - Full OpenAPI client setup
- `examples/tree-example/Client/` - Tree with OpenAPI integration

## Key Files to Create

1. `Composers/MyApiComposer.cs` - Swagger registration
2. `Client/scripts/generate-openapi.js` - Generation script
3. `Client/src/entrypoints/entrypoint.ts` - Auth configuration
4. `Client/src/api/` - Generated (don't edit manually)

That's it! Always generate your API client and configure it with auth. Never use raw fetch for authenticated endpoints.
