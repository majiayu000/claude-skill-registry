---
name: vercel-deploy
description: 'Purpose: One-click deployment to Vercel with transferable ownership.'
---

# Vercel Deploy

**Purpose:** One-click deployment to Vercel with transferable ownership.

**Source:** Adapted from [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/claude.ai/vercel-deploy-claimable)

---

## When to Activate

This skill activates when:

- User explicitly requests deployment
- Build has passed Ralph QA (PASS verdict)

Trigger phrases:

- "Deploy my app"
- "Deploy to Vercel"
- "Push this live"
- "Deploy to production"

---

## How to Use This Skill

1. **Verify Ralph PASS:** Ensure build has passed Ralph Polish Loop
2. **Run Deploy Script:** Execute `scripts/deploy.sh` from build directory
3. **Return URLs:** Provide preview URL and claim URL to user

---

## Prerequisites

Before deploying:

- [ ] Ralph final verdict is PASS
- [ ] `npm run build` completes without errors
- [ ] No `.env` file with secrets (use `.env.example`)
- [ ] `vercel.json` exists with deployment config

---

## Deployment Process

### Step 1: Verify Build

```bash
cd web3-builds/<app-slug>
npm run build
```

### Step 2: Run Deploy Script

```bash
bash ../../skills/vercel-deploy/scripts/deploy.sh
```

### Step 3: Parse Output

The script outputs JSON:

```json
{
  "deploymentId": "dpl_...",
  "projectId": "prj_...",
  "previewUrl": "https://app-name-abc123.vercel.app",
  "claimUrl": "https://vercel.com/claim-deployment?code=..."
}
```

### Step 4: Return to User

Provide both URLs:

```
Deployment successful!

Preview URL: https://app-name-abc123.vercel.app
Claim URL: https://vercel.com/claim-deployment?code=...

The preview URL is live now. Use the claim URL to transfer
this deployment to your own Vercel account.
```

---

## Framework Detection

The deploy script auto-detects framework from `package.json`:

| Detected Dependency | Framework   |
| ------------------- | ----------- |
| `next`              | Next.js     |
| `nuxt`              | Nuxt        |
| `@sveltejs/kit`     | SvelteKit   |
| `astro`             | Astro       |
| `remix`             | Remix       |
| `vite`              | Vite        |
| (none)              | Static HTML |

---

## Error Handling

### Build Failures

If deployment fails due to build errors:

```
Deployment failed. Please verify:
1. npm run build completes locally
2. All environment variables are documented in .env.example
3. No hardcoded localhost URLs in code
```

### Network Errors

If deployment fails due to network:

```
Deployment failed due to network error.
Please try again or deploy manually via Vercel CLI.
```

---

## Files

- `SKILL.md` - This file (usage instructions)
- `scripts/deploy.sh` - Deployment script

---

## Security Notes

- Never include `.env` files in deployments
- All secrets should be documented in `.env.example`
- User must configure production secrets in Vercel dashboard after claiming

---

## Version

- **1.0** (2026-01-15): Initial release
