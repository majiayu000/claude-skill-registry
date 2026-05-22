---
name: vercel-api
description: Patterns for programmatic deployment via Vercel API. Use this skill when implementing deployment workflows, managing projects, configuring environment variables, or setting up domains.
---

# Vercel API Patterns

## API Client Setup

```typescript
const VERCEL_API = 'https://api.vercel.com'

interface VercelClientConfig {
  token: string
  teamId?: string
}

class VercelClient {
  constructor(private config: VercelClientConfig) {}

  private async request<T>(
    path: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = new URL(path, VERCEL_API)

    if (this.config.teamId) {
      url.searchParams.set('teamId', this.config.teamId)
    }

    const response = await fetch(url, {
      ...options,
      headers: {
        Authorization: `Bearer ${this.config.token}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })

    if (!response.ok) {
      const error = await response.json()
      throw new VercelAPIError(error.error.message, response.status)
    }

    return response.json()
  }
}
```

## Project Creation

```typescript
interface CreateProjectRequest {
  name: string
  framework?: 'nextjs' | 'vite' | 'remix' | null
  gitRepository?: {
    type: 'github' | 'gitlab' | 'bitbucket'
    repo: string
  }
  buildCommand?: string
  outputDirectory?: string
  rootDirectory?: string
}

async createProject(data: CreateProjectRequest) {
  return this.request<Project>('/v10/projects', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}
```

## Environment Variables

### Set Environment Variables

```typescript
interface EnvVariable {
  key: string
  value: string
  target: ('production' | 'preview' | 'development')[]
  type: 'plain' | 'secret' | 'encrypted'
}

async setEnvVariables(projectId: string, variables: EnvVariable[]) {
  return this.request(`/v10/projects/${projectId}/env`, {
    method: 'POST',
    body: JSON.stringify(variables),
  })
}
```

### Get Environment Variables

```typescript
async getEnvVariables(projectId: string) {
  return this.request<{ envs: EnvVariable[] }>(
    `/v9/projects/${projectId}/env`
  )
}
```

## Deployment

### Create Deployment from Files

```typescript
interface DeploymentFile {
  file: string
  data: string // base64 encoded
}

async createDeployment(projectId: string, files: DeploymentFile[]) {
  return this.request<Deployment>('/v13/deployments', {
    method: 'POST',
    body: JSON.stringify({
      name: projectId,
      files,
      projectSettings: {
        framework: 'nextjs',
      },
    }),
  })
}
```

### Check Deployment Status

```typescript
type DeploymentState =
  | 'QUEUED'
  | 'BUILDING'
  | 'READY'
  | 'ERROR'
  | 'CANCELED'

async getDeployment(deploymentId: string) {
  return this.request<Deployment>(`/v13/deployments/${deploymentId}`)
}

async waitForDeployment(
  deploymentId: string,
  timeout = 300000
): Promise<Deployment> {
  const start = Date.now()

  while (Date.now() - start < timeout) {
    const deployment = await this.getDeployment(deploymentId)

    if (deployment.readyState === 'READY') {
      return deployment
    }

    if (deployment.readyState === 'ERROR') {
      throw new Error(`Deployment failed: ${deployment.errorMessage}`)
    }

    await new Promise((r) => setTimeout(r, 2000))
  }

  throw new Error('Deployment timeout')
}
```

## Domain Configuration

### Add Domain

```typescript
async addDomain(projectId: string, domain: string) {
  return this.request(`/v10/projects/${projectId}/domains`, {
    method: 'POST',
    body: JSON.stringify({ name: domain }),
  })
}
```

### Configure Subdomain

Battery uses subdomains for deployed apps: `{app-name}.{org}.battery.app`

```typescript
async configureBatteryDomain(
  projectId: string,
  appName: string,
  orgSlug: string
) {
  const domain = `${appName}.${orgSlug}.battery.app`
  return this.addDomain(projectId, domain)
}
```

## Error Handling

```typescript
class VercelAPIError extends Error {
  constructor(
    message: string,
    public statusCode: number
  ) {
    super(message)
    this.name = 'VercelAPIError'
  }
}

// Handle common errors
try {
  await client.createProject({ name: 'my-app' })
} catch (error) {
  if (error instanceof VercelAPIError) {
    switch (error.statusCode) {
      case 400:
        // Invalid request
        break
      case 401:
        // Invalid token
        break
      case 403:
        // Insufficient permissions
        break
      case 409:
        // Project already exists
        break
    }
  }
}
```

## Rate Limiting

Vercel API has rate limits. Implement backoff:

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      if (
        error instanceof VercelAPIError &&
        error.statusCode === 429 &&
        i < maxRetries - 1
      ) {
        await new Promise((r) => setTimeout(r, 2 ** i * 1000))
        continue
      }
      throw error
    }
  }
  throw new Error('Max retries exceeded')
}
```

## Key Endpoints Reference

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List projects | GET | `/v9/projects` |
| Create project | POST | `/v10/projects` |
| Get project | GET | `/v9/projects/{idOrName}` |
| Delete project | DELETE | `/v9/projects/{idOrName}` |
| Create deployment | POST | `/v13/deployments` |
| Get deployment | GET | `/v13/deployments/{id}` |
| List deployments | GET | `/v6/deployments` |
| Set env vars | POST | `/v10/projects/{id}/env` |
| Add domain | POST | `/v10/projects/{id}/domains` |
