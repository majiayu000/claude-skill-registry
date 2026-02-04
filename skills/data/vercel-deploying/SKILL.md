---
name: "Vercel Deploying"
description: "Automatically deploys to Vercel production, uses Vercel MCP to fetch build logs, analyzes errors, fixes them, and retries until successful deployment. Use when deploying to production or fixing deployment issues."
---

# Vercel Production Deploy Loop

## Instructions

When requested to deploy to Vercel production with automatic error fixing:

1. **Initial Deployment Attempt**
   - Run `vercel --prod` to start production deployment
   - Wait for deployment to complete

2. **Error Detection & Analysis**
   - **CRITICAL**: Use Vercel MCP tool to fetch detailed logs:
     - The MCP logs provide much more detail than CLI output
   - Analyze the build logs to identify root cause:
     - Build errors (TypeScript, ESLint, compilation)
     - Runtime errors
     - Environment variable issues
     - Dependency problems
     - Configuration issues
   - Extract specific error messages

3. **Error Fixing**
   - Make minimal, targeted fixes to resolve the specific error

4. **Retry Deployment**
   - Run `vercel --prod` again with the fixes applied
   - Repeat steps until deployment succeeds

5. **Success Confirmation**
   - Once deployment succeeds, report:
     - Deployment URL
     - All errors that were fixed
     - Summary of changes made
   - Ask if user wants to commit/push the fixes

## Loop Exit Conditions

- ✅ Deployment succeeds
- ❌ SAME error occurs 5+ times (suggest manual intervention)
- ❌ User requests to stop

## Best Practices
- Make incremental fixes rather than large refactors
- Preserve user's code style and patterns when fixing

## Example Flow

**User:** "Deploy to production and fix any errors"


- Vercel MCP build logs are the PRIMARY source of error information
- CLI output alone is insufficient for proper error diagnosis
- Always wait for deployment to complete before fetching logs
- If errors require user input (like API keys), prompt user immediately
