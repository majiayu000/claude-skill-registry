---
name: umbraco-health-check
description: Implement health checks in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Health Check

## What is it?
Health Checks in Umbraco allow you to create custom system diagnostics that appear in the Health Check dashboard. They verify that your Umbraco installation and related services are functioning correctly. Health checks can report status, display warnings, and provide actionable recommendations for resolving issues.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/extending/health-check
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Related Foundation Skills

- **Context API**: When accessing application state
  - Reference skill: `umbraco-context-api`

- **Controllers**: When creating API endpoints for checks
  - Reference skill: `umbraco-controllers`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What should be checked? What actions to provide?
3. **Generate files** - Create manifest + context based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestHealthCheck } from '@umbraco-cms/backoffice/health-check';

export const manifests: Array<ManifestHealthCheck> = [
  {
    type: 'healthCheck',
    alias: 'My.HealthCheck.Custom',
    name: 'Custom Health Check',
    api: () => import('./my-health-check.context.js'),
    meta: {
      label: 'Custom Check',
    },
  },
];
```

### Context Implementation (my-health-check.context.ts)
```typescript
import { UmbHealthCheckContext } from '@umbraco-cms/backoffice/health-check';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';
import type { HealthCheckResultResponseModel } from '@umbraco-cms/backoffice/external/backend-api';

export class MyHealthCheckContext extends UmbHealthCheckContext {
  constructor(host: UmbControllerHost) {
    super(host);
  }

  override async check(): Promise<HealthCheckResultResponseModel> {
    // Perform your health check logic
    const isHealthy = await this.#performCheck();

    return {
      message: isHealthy ? 'All systems operational' : 'Issue detected',
      resultType: isHealthy ? 'Success' : 'Warning',
      actions: isHealthy ? [] : [
        {
          alias: 'fix-issue',
          name: 'Fix Issue',
          description: 'Attempt to automatically fix this issue',
        },
      ],
    };
  }

  async #performCheck(): Promise<boolean> {
    // Your custom check logic here
    return true;
  }

  override async executeAction(actionAlias: string): Promise<HealthCheckResultResponseModel> {
    if (actionAlias === 'fix-issue') {
      // Execute the fix action
      return {
        message: 'Issue has been resolved',
        resultType: 'Success',
        actions: [],
      };
    }

    return {
      message: 'Unknown action',
      resultType: 'Error',
      actions: [],
    };
  }
}

export { MyHealthCheckContext as api };
```

## Interface Reference

```typescript
interface ManifestHealthCheck extends ManifestBase {
  type: 'healthCheck';
  api: ApiLoaderProperty; // Should implement UmbHealthCheckContext
  meta: MetaHealthCheck;
}

interface MetaHealthCheck {
  label: string;
}

// Result types: 'Success' | 'Warning' | 'Error' | 'Info'
interface HealthCheckResultResponseModel {
  message: string;
  resultType: string;
  actions?: Array<{
    alias: string;
    name: string;
    description?: string;
  }>;
}
```

## Backend C# Health Check

Health checks can also be implemented as C# classes that are auto-discovered by Umbraco.

```csharp
using Umbraco.Cms.Core.HealthChecks;

namespace MyPackage.HealthChecks;

[HealthCheck(
    "12345678-1234-1234-1234-123456789012",
    "My Custom Check",
    Description = "Verifies custom services are running",
    Group = "Custom")]
public class MyHealthCheck : HealthCheck
{
    public MyHealthCheck(HealthCheckContext context) : base(context) { }

    public override Task<IEnumerable<HealthCheckStatus>> GetStatus()
    {
        var isHealthy = CheckMyService();
        var status = new HealthCheckStatus(isHealthy ? "Service running" : "Service down")
        {
            ResultType = isHealthy ? StatusResultType.Success : StatusResultType.Error,
            Actions = isHealthy ? null : new List<HealthCheckAction>
            {
                new("restart", Id) { Name = "Restart Service" }
            }
        };
        return Task.FromResult<IEnumerable<HealthCheckStatus>>(new[] { status });
    }

    public override HealthCheckStatus ExecuteAction(HealthCheckAction action)
    {
        if (action.Alias == "restart")
        {
            RestartMyService();
            return new HealthCheckStatus("Restarted") { ResultType = StatusResultType.Success };
        }
        throw new InvalidOperationException("Unknown action");
    }

    private bool CheckMyService() => true;
    private void RestartMyService() { }
}
```

## Best Practices

- Return clear, actionable messages
- Provide fix actions when possible
- Use appropriate result types (Success, Warning, Error, Info)
- Consider performance - health checks run periodically

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
