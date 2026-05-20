---
name: deploy
description: Enforces local testing before any deployment. MUST be used before running vercel, git push, or any deployment command. Prevents deploying untested code.
---

# Deploy Skill

**NEVER deploy without completing ALL steps below.**

## Required Workflow

Before ANY deployment (vercel, git push to main, etc.):

### 1. Build Locally
```bash
pnpm build
```
- Must complete with zero errors
- Check output for warnings

### 2. Start Local Dev Server
```bash
pnpm dev
```
- Server must start successfully

### 3. Test in Browser
- Open the local URL in Chrome DevTools MCP
- Test ALL changed functionality manually:
  - Click buttons, verify they work
  - Test keyboard input if applicable
  - Submit forms, verify responses
  - Check for console errors

### 4. Verify Tests Pass (if tests exist)
```bash
pnpm test
```

### 5. Only Then Deploy
After ALL above steps pass:
```bash
vercel --prod
```

## Rules

1. **NO SHORTCUTS** - Every step must be completed
2. **NO ASSUMPTIONS** - "It worked before" is not verification
3. **TEST AFTER CHANGES** - Any code change requires re-testing
4. **LOCAL FIRST** - Never deploy to see if something works

## Common Mistakes to Avoid

- Deploying immediately after build without browser testing
- Assuming dependency changes don't break anything
- Skipping keyboard/interaction testing
- Deploying to "check if it works on Vercel"

## When User Says "Deploy"

1. Ask: "Have you verified locally? Let me run through the checklist."
2. Run build
3. Start dev server
4. Test in browser via Chrome DevTools MCP
5. Only after confirming everything works, deploy
