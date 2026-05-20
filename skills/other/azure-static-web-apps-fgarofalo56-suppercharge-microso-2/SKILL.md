---
name: azure-static-web-apps
description: Deploy static sites with Azure Static Web Apps. Configure API routes, authentication, custom domains, and staging environments. Use for JAMstack, SPAs, static sites, and serverless backends on Azure.
---

# Azure Static Web Apps

Expert guidance for deploying static sites and serverless APIs.

## Create App

```bash
# Create from GitHub
az staticwebapp create \
  --name mystaticwebapp \
  --resource-group myResourceGroup \
  --source https://github.com/myorg/myapp \
  --branch main \
  --app-location "/" \
  --api-location "api" \
  --output-location "dist" \
  --login-with-github

# Create standalone
az staticwebapp create \
  --name mystaticwebapp \
  --resource-group myResourceGroup \
  --location eastus2 \
  --sku Standard
```

## Configuration (staticwebapp.config.json)

### Basic Configuration

```json
{
  "navigationFallback": {
    "rewrite": "/index.html",
    "exclude": ["/images/*", "/api/*"]
  },
  "routes": [
    {
      "route": "/api/*",
      "allowedRoles": ["authenticated"]
    },
    {
      "route": "/admin/*",
      "allowedRoles": ["admin"]
    }
  ],
  "responseOverrides": {
    "401": {
      "statusCode": 302,
      "redirect": "/.auth/login/aad"
    },
    "404": {
      "rewrite": "/404.html"
    }
  }
}
```

### Headers and MIME Types

```json
{
  "globalHeaders": {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Content-Security-Policy": "default-src 'self'"
  },
  "mimeTypes": {
    ".wasm": "application/wasm",
    ".json": "application/json"
  },
  "routes": [
    {
      "route": "/api/*",
      "headers": {
        "Cache-Control": "no-cache"
      }
    },
    {
      "route": "/static/*",
      "headers": {
        "Cache-Control": "max-age=31536000"
      }
    }
  ]
}
```

## Authentication

### Built-in Providers

```json
{
  "routes": [
    {
      "route": "/.auth/login/github",
      "statusCode": 404
    },
    {
      "route": "/.auth/login/twitter",
      "statusCode": 404
    }
  ],
  "auth": {
    "identityProviders": {
      "azureActiveDirectory": {
        "registration": {
          "openIdIssuer": "https://login.microsoftonline.com/{tenant}/v2.0",
          "clientIdSettingName": "AAD_CLIENT_ID",
          "clientSecretSettingName": "AAD_CLIENT_SECRET"
        }
      }
    }
  }
}
```

### Custom Roles

```json
{
  "auth": {
    "rolesSource": "/api/GetRoles",
    "identityProviders": {
      "azureActiveDirectory": {
        "userDetailsClaim": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"
      }
    }
  }
}
```

## API Functions

### Python API

```python
# api/products/__init__.py
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    products = [
        {"id": 1, "name": "Product A"},
        {"id": 2, "name": "Product B"}
    ]

    return func.HttpResponse(
        json.dumps(products),
        mimetype="application/json"
    )
```

### Node.js API

```javascript
// api/products/index.js
module.exports = async function (context, req) {
    const products = [
        { id: 1, name: "Product A" },
        { id: 2, name: "Product B" }
    ];

    context.res = {
        body: products,
        headers: {
            'Content-Type': 'application/json'
        }
    };
};
```

### API with Database

```python
# api/products/__init__.py
import azure.functions as func
import os
from azure.cosmos import CosmosClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    client = CosmosClient.from_connection_string(os.environ["COSMOS_CONNECTION"])
    container = client.get_database_client("mydb").get_container_client("products")

    products = list(container.read_all_items())

    return func.HttpResponse(
        json.dumps(products),
        mimetype="application/json"
    )
```

## GitHub Actions Workflow

```yaml
# .github/workflows/azure-static-web-apps.yml
name: Deploy Static Web App

on:
  push:
    branches: [main]
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches: [main]

jobs:
  build_and_deploy:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build And Deploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "/"
          api_location: "api"
          output_location: "dist"

  close_pull_request:
    if: github.event_name == 'pull_request' && github.event.action == 'closed'
    runs-on: ubuntu-latest
    steps:
      - name: Close Pull Request
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          action: "close"
```

## Custom Domains

```bash
# Add custom domain
az staticwebapp hostname set \
  --name mystaticwebapp \
  --resource-group myResourceGroup \
  --hostname www.example.com

# Verify
az staticwebapp hostname list \
  --name mystaticwebapp \
  --resource-group myResourceGroup
```

## Environment Variables

```bash
# Set app settings
az staticwebapp appsettings set \
  --name mystaticwebapp \
  --resource-group myResourceGroup \
  --setting-names \
    "API_KEY=secret123" \
    "DATABASE_URL=connection-string"
```

## Linked Backend

```bash
# Link to Azure Functions
az staticwebapp backends link \
  --name mystaticwebapp \
  --resource-group myResourceGroup \
  --backend-resource-id /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Web/sites/{functionapp} \
  --backend-region eastus
```

## Bicep Deployment

```bicep
resource staticWebApp 'Microsoft.Web/staticSites@2023-01-01' = {
  name: appName
  location: location
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
  properties: {
    repositoryUrl: repoUrl
    branch: 'main'
    buildProperties: {
      appLocation: '/'
      apiLocation: 'api'
      outputLocation: 'dist'
    }
  }
}

resource customDomain 'Microsoft.Web/staticSites/customDomains@2023-01-01' = {
  parent: staticWebApp
  name: 'www.example.com'
  properties: {}
}
```

## Resources

- [Static Web Apps Documentation](https://learn.microsoft.com/azure/static-web-apps/)
- [Configuration Reference](https://learn.microsoft.com/azure/static-web-apps/configuration)
- [API Support](https://learn.microsoft.com/azure/static-web-apps/apis)
