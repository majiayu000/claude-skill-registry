---
name: codebase-audit
description: Performs comprehensive codebase audit checking architecture, tech debt, security vulnerabilities, test coverage, documentation, dependencies, and maintainability. Use when auditing a project, assessing codebase health, running security scans, checking for vulnerabilities, reviewing code quality, analyzing tech debt, or asked to audit/analyze the entire codebase.
compatibility: Requires trufflehog for secret scanning, npm/pnpm/yarn/pip/cargo for dependency audits. Optional Chrome DevTools MCP for performance testing.
allowed-tools: Read Grep Glob Bash WebSearch WebFetch
metadata:
  author: Saturate
  version: "1.0"
---

# Codebase Audit

Audit the codebase like you're inheriting someone else's mess - be thorough and honest. No diplomacy, no softening. Focus on what actually matters: security holes, bugs, maintainability problems, and tech debt. If something is broken or badly done, say it.

## Audit Process

Copy this checklist to track your progress:

```
Codebase Audit Progress:
- [ ] Step 1: Check available tools
- [ ] Step 2: Detect project type and run audits
- [ ] Step 3: Detect tech stack and framework patterns
- [ ] Step 4: Identify and document critical issues
- [ ] Step 5: Generate high-level findings summary
```

### 1. Check Available Tools

Start by checking what tools you have available:
```bash
command -v trufflehog
command -v npm # or pnpm, yarn, pip, cargo, etc.
```

If any expected tools are missing, list them in your output and ask the user if they want to continue without them. Don't let missing tools block the entire audit.

### 2. Detect Project Type and Run Audits

**Figure out the package manager and run the right audit:**
- `package-lock.json` → `npm audit --json`
- `pnpm-lock.yaml` → `pnpm audit --json`
- `yarn.lock` → `yarn audit --json`
- `requirements.txt` / `poetry.lock` → `pip-audit --format json` or `safety check --json`
- `Cargo.toml` → `cargo audit --json`
- `go.mod` → `go list -json -m all | nancy sleuth`
- `*.csproj` → `dotnet list package --vulnerable --include-transitive`

**Secret scanning:** Need help with TruffleHog? Check [references/secret-scanning.md](references/secret-scanning.md) for scanning both current files and git history.

Parse the JSON output from these tools and integrate what you find into the audit report.

**TypeScript projects (if tsconfig.json exists):**
- Check if `strict` mode is enabled (critical issue if it's false or missing)
- Count how many times `any` is used explicitly (this defeats type safety)
- Count type assertions using `as` or `<Type>` (suggest using type narrowing instead)

**OWASP Top 10 checks:** See [references/owasp-top-10.md](references/owasp-top-10.md) for vulnerability patterns and detection commands. Report findings as **critical** with file:line, what the risk is, and how to fix it.

**Accessibility checks:** Check [references/accessibility-checklist.md](references/accessibility-checklist.md) for a11y detection commands and testing procedures. Report these as **important** because they exclude real users from using the app.

**Monitoring/Observability:**
Look for error tracking tools (Sentry, DataDog, NewRelic), structured logging libraries (winston, pino), health check endpoints, and watch out for console.logs making it to production. Report missing observability as **important** for production systems.

### 3. Detect Tech Stack and Understand Project

**Figure out the tech stack:** Need help identifying package managers, frameworks, cloud platforms, or IaC tools? See [references/tech-stack-detection.md](references/tech-stack-detection.md) for the complete detection guide.

Build a summary that covers: language(s), framework, build tools, testing framework, cloud platform, IaC tools, and CI/CD platform.

**Framework best practices:**

Once you know what framework they're using, check the relevant patterns guide:
- **Next.js/React** → [references/framework-patterns-nextjs.md](references/framework-patterns-nextjs.md)
- **Nuxt/Vue** → [references/framework-patterns-nuxt.md](references/framework-patterns-nuxt.md)
- **ASP.NET Core / .NET** → [references/framework-patterns-dotnet.md](references/framework-patterns-dotnet.md)
- **Entity Framework** → [references/entity-framework.md](references/entity-framework.md)
- **Other frameworks** → Use WebSearch to look up current best practices and common mistakes

**Performance testing (if Chrome MCP is available):**

If this is a web app and you have access to chrome-devtools MCP:
- Ask the user: "Want me to run performance tests? Provide a URL or say skip."
- If they give you a URL, use Chrome MCP to run a Lighthouse-style audit
- Report Core Web Vitals (LCP, FID, CLS), bundle size, unoptimized images, and render-blocking resources

Don't forget to also check the project structure, documentation quality, and CI/CD setup.

### 4. Critical Issues (Show Details Immediately)

Surface these issues with full context right away - don't bury them:

**Security (from tools + manual review)**
- Secrets found by trufflehog - show file:line, what type of secret, and severity
- Vulnerable dependencies from npm/pip/cargo/dotnet audit - package name, CVE, severity
- Hardcoded credentials or API keys sitting in the code
- Missing authentication or authorization checks
- Unsafe ways of handling data
- Sensitive endpoints that are exposed
- .NET projects: see [auth](references/dotnet-security-auth.md), [data](references/dotnet-security-data.md), [crypto](references/dotnet-security-crypto.md)

**TypeScript Configuration (if it's a TypeScript project)**
- strict mode is disabled or missing from tsconfig.json
- explicit `any` types being used (this defeats the whole point of TypeScript)
- type casting/assertions (suggest type narrowing instead)

**Breaking Problems**
- Build failures or broken configuration
- Missing dependencies that are critical
- Incompatible version requirements
- Database migrations that can't be rolled back
- Entity Framework projects: see [references/entity-framework.md](references/entity-framework.md)

**Data Loss Risks**
- Operations running without validation
- Missing error handling in paths that matter
- Race conditions in how data is handled

### 5. High-Level Findings (Summary Only)

Organize what you found into categories with counts and brief summaries. Need help with the full category breakdown? Check [references/report-template.md](references/report-template.md).

**Categories to cover:**
- Architecture & Structure
- Tech Debt
- Testing
- Documentation
- Dependencies
- Performance
- Developer Experience
- Best Practices

For each one: give a brief assessment, count the major issues, and summarize the patterns you're seeing. Don't list every single detail here - that's what "Areas to Investigate" is for.

## Output Format

Structure your audit report like this (see [references/report-template.md](references/report-template.md) for examples):

1. **Tool Check** - What tools are available, what's missing
2. **Tech Stack** - Languages, frameworks, cloud platform, CI/CD
3. **Security Scan Results** - What trufflehog, npm audit, and OWASP checks found
4. **TypeScript Check** - Strict mode status, any usage, type casting
5. **Accessibility Check** - Missing alt text, ARIA labels, keyboard support
6. **Monitoring/Observability** - Error tracking, logging, health endpoints
7. **Performance** - If Chrome MCP is available and user provided a URL
8. **Critical Issues 🚨** - Detailed breakdown with file:line, what the risk is, how to fix it
9. **Audit Summary** - Overall health rating plus brief assessment for each category
10. **Areas to Investigate** - Offer to dive deeper into specific areas with file:line details

## Investigation Process

When the user asks you to investigate a specific area:
- Search for relevant patterns in the code
- Give them file:line references so they can jump right to it
- Show specific examples of what you found
- Suggest concrete fixes they can implement
- Prioritize by what will have the most impact

## Tool Output Handling

Parse the JSON output from security tools and work the findings into your report:
- Group them by severity (critical → low)
- Show which package or file, what the vulnerability is, and how to fix it
- Link to the CVE or advisory when you can
- For trufflehog results, make it clear if the secret is in git history vs current files

If a tool fails to run, note it and keep going - don't let one tool failure block the entire audit.

## Guidelines

**Be brutally honest:**
- Call out bad code. Don't soften it.
- If something is a mess, say it's a mess
- No hedging with "might", "could", or "possibly"
- Don't say "consider fixing" - say "fix this" or "this is wrong"
- If strict mode is off in TypeScript, that's a critical issue, not a suggestion
- Explicit `any` defeats the whole point of TypeScript - call it out as breaking type safety
- Tech debt is tech debt, not "areas for improvement"

**Focus and priority:**
- Only report findings they can actually act on, not theoretical problems
- Prioritize by real impact on security, stability, and maintainability
- Skip nitpicks that linters should catch
- Tool findings are facts - just report them straight

**Context matters:**
- Startup MVPs can have some shortcuts, but still call them out
- Enterprise systems need to meet higher standards
- Personal projects can be looser, but point out what's missing
- Don't excuse bad practices just because "it works right now"

**Tone:**
- Be direct and clear, not diplomatic
- If tests are missing, say "no tests" not "test coverage could be improved"
- If docs are bad, say "documentation is inadequate" not "could benefit from more documentation"
- Be specific about what's wrong and why it matters
- Acknowledge what's good, but keep it brief - don't pad with praise

## References

Need more detailed guidance? Check these references:

- **[Tech Stack Detection](references/tech-stack-detection.md)** - How to figure out what package managers, frameworks, cloud platforms, and IaC tools they're using
- **[Secret Scanning Reference](references/secret-scanning.md)** - Complete guide to running TruffleHog on both current files and git history, plus common patterns and how to fix them
- **[OWASP Top 10 Reference](references/owasp-top-10.md)** - Detection patterns and grep commands for finding all OWASP Top 10 vulnerabilities, with severity guidelines
- **[Accessibility Checklist](references/accessibility-checklist.md)** - Practical commands for finding a11y issues and testing for WCAG compliance
- **[Report Template](references/report-template.md)** - What the final report should look like, with example critical issues

**Framework-specific patterns:**
- **[Next.js / React Patterns](references/framework-patterns-nextjs.md)** - Best practices, common anti-patterns, and what to check in Next.js/React projects
- **[Nuxt / Vue Patterns](references/framework-patterns-nuxt.md)** - Best practices, common anti-patterns, and what to check in Nuxt/Vue projects
- **[.NET Framework Patterns](references/framework-patterns-dotnet.md)** - ASP.NET Core, async patterns, DI, testing, and code quality anti-patterns for .NET 6+
- **[Entity Framework Patterns](references/entity-framework.md)** - Performance, security, and correctness issues in Entity Framework Core
- **[.NET Security: Auth](references/dotnet-security-auth.md)** - Authentication, authorization, CSRF, and redirect validation for ASP.NET Core
- **[.NET Security: Data](references/dotnet-security-data.md)** - SQL injection, deserialization, mass assignment, input validation, and XXE
- **[.NET Security: Crypto](references/dotnet-security-crypto.md)** - Secrets management, cryptographic failures, and security headers
