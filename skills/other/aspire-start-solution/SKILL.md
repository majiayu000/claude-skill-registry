---
name: aspire__start_solution
description: Start the BookStore solution using Aspire CLI or debug mode. Use this to run the full application stack (API, Web, PostgreSQL, Redis, Azurite) with optional GitHub Copilot integration.
---

Start the BookStore solution infrastructure. Choose between CLI or debug mode based on your needs.

## Prerequisites Check

1. **Verify Environment** (optional)
   - Run `/ops__doctor_check` skill to ensure all tools are installed

## Start Method Selection

**Two options available:**

### Option A: Aspire CLI (Quick Start)
- Faster startup
- Background execution
- MCP server included

### Option B: Debug AppHost (Full Features)
- GitHub Copilot integration in dashboard
- Full debugging capabilities
- MCP server included
- Breakpoint support in AppHost

## Option A: Start with Aspire CLI

// turbo
2. **Start Aspire in Background**
   ```bash
   cd /Users/antaoalmada/Projects/BookStore && aspire run &
   ```
   - Starts: API, Web, PostgreSQL, Redis, Azurite, PgAdmin
   - Dashboard URL: `http://localhost:15888` (check terminal output for actual port)
   - API URL: `http://localhost:5000` (or assigned port)
   - Web URL: `http://localhost:5001` (or assigned port)
   - **MCP Server**: Automatically available for `/aspire__setup_mcp`

## Option B: Start with Debug Mode

// turbo
2. **Start AppHost in Debug**
   ```bash
   cd /Users/antaoalmada/Projects/BookStore && dotnet run --project src/BookStore.AppHost
   ```
   - Or use IDE: Debug → Start Debugging (F5) on `BookStore.AppHost` project
   - Starts same services as CLI mode
   - Dashboard URL: `http://localhost:15888` (check terminal output for actual port)
   - **GitHub Copilot Integration**: Available in dashboard UI
   - **MCP Server**: Automatically available for `/aspire__setup_mcp`
   - Can set breakpoints in `Program.cs` for orchestration debugging

3. **Verify Services Are Running**
   - Check Aspire dashboard for green status on all resources
   - Console logs appear in terminal
   - Structured logs available via dashboard → Logs
   - Metrics available via dashboard → Metrics
   - **Debug mode only**: GitHub Copilot chat available in dashboard

## Accessing Logs & Metrics

Aspire dashboard provides:
- **Console**: Real-time stdout/stderr from all services
- **Structured Logs**: Filterable logs with correlation IDs
- **Traces**: Distributed tracing across services
- **Metrics**: CPU, memory, HTTP request metrics
- **MCP Server**: Programmatic access to logs, traces, and metrics (both modes)
- **GitHub Copilot** (debug mode): AI assistance for troubleshooting in dashboard

## Stopping the Solution

// turbo
4. **Stop Services**

   **CLI Mode:**
   ```bash
   # Find and kill the Aspire process
   pkill -f "aspire run" || true
   ```

   **Debug Mode:**
   - Press `Ctrl+C` in terminal
   - Or use IDE: Stop Debugging (Shift+F5)

## Related Skills

**Prerequisites**:
- `/ops__doctor_check` - Verify environment (Docker, .NET, Aspire CLI)

**Next Steps**:
- `/aspire__setup_mcp` - Connect to MCP server (available in both modes)
- `/test__integration_suite` - Run tests against running instance

**Debugging**:
- `/frontend__debug_sse` - If real-time updates not working
- `/cache__debug_cache` - If caching issues

**See Also**:
- `docs/guides/aspire-guide.md`
- `src/BookStore.AppHost/AGENTS.md`

## Choosing the Right Mode

**Use CLI mode when:**
- Quick testing or development
- Running in CI/CD
- No need for AppHost debugging

**Use Debug mode when:**
- Troubleshooting with GitHub Copilot in dashboard
- Need to debug AppHost orchestration
- Want full IDE integration
- Investigating service startup issues
