---
name: ops__doctor_check
description: Checks specific tools and SDKs required for the BookStore project. Use this to diagnose environment issues before deployment or development.
---

Perform a health check on the development environment to ensure all prerequisites are met:

1. **.NET SDK**
   - Run `dotnet --version`
   - **Requirement**: Version 10.0.x or later.
   - *Action*: If too old, advise upgrading .NET.

2. **Docker**
   - Run `docker --version`
   - **Requirement**: Version 20.x or later.
   - *Action*: If missing, Docker Desktop or Podman is required for running the Aspire containers.

4. **Aspire CLI** (for orchestration)
   - Run: `aspire --version`
   - **Requirement**: Aspire CLI must be installed.
   - *Action*: If missing, see [Install instructions](https://aspire.dev/get-started/install-cli/)

5. **Playwright Browsers** (for `BookStore.AppHost.Tests`)
   - Check if the chromium binary exists inside the build output: `ls tests/BookStore.AppHost.Tests/bin/Debug/net10.0/.playwright/package/` (requires the project to have been built)
   - **Requirement**: Chromium must be installed for browser-based integration tests.
   - *Action*: If missing or the project hasn't been built yet, run:
     ```bash
     dotnet build tests/BookStore.AppHost.Tests/BookStore.AppHost.Tests.csproj
     node tests/BookStore.AppHost.Tests/bin/Debug/net10.0/.playwright/package/index.js install chromium
     ```

6. **Report Summary**
   - If all checks pass: "✅ Environment is healthy"
   - If issues found: List specific missing tools with installation instructions

## Related Skills

**Next Steps**:
- If issues found, resolve them and re-run `/ops__doctor_check`
- `/ops__rebuild_clean` - Clean rebuild after environment changes

**See Also**:
- [getting-started](../../../docs/getting-started.md) - Installation instructions
- [aspire-guide](../../../docs/guides/aspire-guide.md) - Aspire orchestration
