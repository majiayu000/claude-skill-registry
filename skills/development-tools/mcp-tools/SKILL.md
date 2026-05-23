---
name: mcp-tools
description: MCP tools for Xcode automation and Apple documentation access. XcodeBuildMCP for builds, apple-docs for WWDC and API docs.
user-invocable: false
---

# MCP Tools for Swift Development

**Model Context Protocol servers for enhanced Swift/Xcode workflows.**

## Available MCP Servers

### 1. XcodeBuildMCP
**Purpose**: Xcode project automation and build validation

**Documentation**: `xcode-build-mcp.md`

**Key features**:
- Discover Xcode projects and workspaces
- Build for macOS, iOS Simulator, iOS Device
- List schemes and show build settings
- Clean builds and derived data
- Create new projects from templates
- **Autonomous build validation** (AI can build, read errors, fix, rebuild)

**Installation**:
```json
{
  "mcpServers": {
    "XcodeBuildMCP": {
      "command": "npx",
      "args": ["-y", "xcodebuildmcp@latest"]
    }
  }
}
```

**Use when**:
- After making code changes (MANDATORY validation)
- Debugging build issues
- Creating new Xcode projects
- Cleaning stale builds

---

### 2. Apple Docs MCP
**Purpose**: Official Apple documentation with offline WWDC access

**Documentation**: `apple-docs-mcp.md`

**Key features**:
- Search all Apple frameworks (SwiftUI, UIKit, Foundation, etc.)
- Get detailed symbol information (classes, methods, properties)
- **WWDC sessions 2014-2025** with full transcripts (offline)
- Access Apple sample code
- Framework exploration and discovery
- API availability and deprecation checking

**Installation**:
```json
{
  "mcpServers": {
    "apple-docs": {
      "command": "npx",
      "args": ["-y", "@kimsungwhee/apple-docs-mcp"]
    }
  }
}
```

**Use when**:
- Researching Apple APIs (PRIORITY over Context7)
- Finding WWDC best practices
- Checking API availability
- Getting official code examples

---

## Workflow Integration

### Research-First (MANDATORY)

```text
Priority order:
1. ⭐ Apple Docs MCP (official Apple docs + WWDC)
2. Context7 (third-party libraries)
3. Exa web search (community tutorials)
```

### Build Validation (MANDATORY)

```text
After EVERY code change:
1. XcodeBuildMCP: Build project
2. If errors → Read error messages
3. Fix issues
4. Rebuild to validate
5. Only commit if zero errors
```

---

## Complete Development Workflow (2026)

```text
1. Feature request received
   ↓
2. Apple Docs MCP: Search API/WWDC
   ↓
3. Read existing codebase (DRY principle)
   ↓
4. Implement following Apple patterns
   ↓
5. XcodeBuildMCP: Build to validate ⭐
   ↓
6. If build errors:
   - Read error messages
   - Fix issues
   - Rebuild
   ↓
7. Run tests (if available)
   ↓
8. Commit changes
```

---

## Benefits

### XcodeBuildMCP
✅ Autonomous error detection and fixing
✅ Zero tolerance for compilation errors
✅ Lightning-fast incremental builds
✅ Project scaffolding automation
✅ Build validation before commits

### Apple Docs MCP
✅ Official Apple documentation (most accurate)
✅ WWDC sessions offline (2014-2025)
✅ Zero network latency
✅ Complete API coverage
✅ Deprecation and availability info

---

## Resources

**XcodeBuildMCP**:
- [GitHub](https://github.com/cameroncooke/XcodeBuildMCP)
- [npm](https://www.npmjs.com/package/xcodebuildmcp)
- Version: 1.12.3

**Apple Docs MCP**:
- [GitHub](https://github.com/kimsungwhee/apple-docs-mcp)
- [npm](https://www.npmjs.com/@kimsungwhee/apple-docs-mcp)

---

## Quick Reference

| Task | MCP Tool | Documentation |
|------|----------|---------------|
| Search Apple API | `apple-docs` | `apple-docs-mcp.md` |
| Find WWDC session | `apple-docs` | `apple-docs-mcp.md` |
| Get code example | `apple-docs` | `apple-docs-mcp.md` |
| Build project | `XcodeBuildMCP` | `xcode-build-mcp.md` |
| Validate changes | `XcodeBuildMCP` | `xcode-build-mcp.md` |
| Clean build | `XcodeBuildMCP` | `xcode-build-mcp.md` |
| Create project | `XcodeBuildMCP` | `xcode-build-mcp.md` |
