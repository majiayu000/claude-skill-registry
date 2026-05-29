---
name: tech-detection
description: Detects project tech stack including languages, frameworks, package managers, and cloud platforms. Use when analyzing a project, detecting technologies, bootstrapping infrastructure, or setting up permissions. Generates project-context.json with detected stack.
allowed-tools: Bash(*), Read, Glob, Grep, Write, Edit, WebSearch, WebFetch
---

# Tech Detection Skill

You are a tech stack detection specialist. Your role is to analyze projects and determine their technology stack with high accuracy.

## When to Activate

- Project analysis requested
- Stack detection needed
- Permissions need updating based on tech
- New project bootstrap (`/claudenv`)
- Cloud platform configuration

## Detection Process

### Step 1: Run Detection Script

```bash
bash .claude/scripts/detect-stack.sh
```

### Step 2: Analyze Results

Parse the JSON output and assess:

- **Languages**: What programming languages are used?
- **Frameworks**: What frameworks are detected?
- **Package Manager**: npm, yarn, pnpm, pip, cargo, etc.?
- **Test Runner**: jest, vitest, pytest, rspec, etc.?
- **Database/ORM**: prisma, drizzle, mongoose, etc.?
- **Cloud Platforms**: AWS, GCP, Azure, Heroku, Vercel, etc.?
- **Infrastructure**: Docker, Kubernetes, CI/CD?

### Step 3: Determine Confidence

- **HIGH**: Clear package manager + framework + established patterns
- **MEDIUM**: Some indicators but incomplete picture
- **LOW**: Minimal or no indicators (new/empty project)

### Step 4: Generate Permissions

Based on detected tech, look up commands in:
`assets/command-mappings.json`

Merge the appropriate command sets into the project's settings.json.

### Step 5: Create project-context.json

Write the detection results to `.claude/project-context.json` for reference by other skills.

## Cloud Platform Detection

The script detects these cloud platforms:

| Platform | Detection Files |
|----------|-----------------|
| AWS | `samconfig.toml`, `template.yaml`, `cdk.json`, `amplify.yml`, `aws-exports.js`, `.aws/`, `buildspec.yml` |
| GCP | `app.yaml`, `cloudbuild.yaml`, `.gcloudignore`, `.gcloud/` |
| Azure | `azure-pipelines.yml`, `.azure/`, `azuredeploy.json` |
| Heroku | `Procfile`, `app.json`, `heroku.yml` |
| Vercel | `vercel.json` |
| Netlify | `netlify.toml` |
| Fly.io | `fly.toml` |
| Railway | `railway.json` |
| DigitalOcean | `.do/app.yaml`, `do.yaml` |
| Cloudflare | `wrangler.toml`, `wrangler.json` |
| Supabase | `supabase/`, `supabase/config.toml` |
| Firebase | `firebase.json`, `.firebaserc` |

## Command Mapping Reference

See `command-mappings.json` for the full mapping of technologies to allowed commands.

Example mappings:
- `npm` detected → add `npm *`, `npx *`, `node *`
- `aws` detected → add `aws *`, `sam *`, `cdk *`, `amplify *`
- `gcp` detected → add `gcloud *`, `gsutil *`, `bq *`
- `heroku` detected → add `heroku *`
- `prisma` detected → add `prisma *`
- `docker` detected → add `docker *`, `docker-compose *`

## Low Confidence Handling

If confidence is LOW:

1. Inform the user of limited detection
2. Recommend running `/interview` to clarify tech stack
3. Ask if they want to proceed with interview or use defaults

## Files Used

- `.claude/scripts/detect-stack.sh` - Detection script
- `assets/command-mappings.json` - Tech→commands map
- `.claude/project-context.json` - Output location
- `.claude/settings.json` - Permissions to update

---

## Agent Creation

**IMPORTANT**: After tech detection completes, create specialist agents for detected technologies.

### Step 6: Create Specialist Agents

For each detected technology that benefits from specialized expertise:

1. Check if agent already exists in `.claude/agents/`
2. If not exists, invoke `agent-creator` to create it
3. Log created agents to `pending-agents.md` for tracking

### Tech-to-Agent Mapping

| Detected Tech | Agent to Create |
|--------------|-----------------|
| React | `react-specialist` |
| Vue | `vue-specialist` |
| Angular | `angular-specialist` |
| Next.js | `nextjs-specialist` |
| Nuxt | `nuxt-specialist` |
| Django | `django-specialist` |
| FastAPI | `fastapi-specialist` |
| AWS | `aws-architect` |
| GCP | `gcp-architect` |
| Azure | `azure-architect` |
| Prisma | `prisma-specialist` |
| Drizzle | `drizzle-specialist` |
| Stripe | `stripe-specialist` |
| GraphQL | `graphql-architect` |

### Agent Creation Process

```markdown
For each detected technology:
1. Look up in tech-agent-mappings
2. Check if .claude/agents/{name}.md exists
3. If not exists:
   - Invoke agent-creator skill
   - Pass technology name and detected context
   - agent-creator researches and generates agent file
4. Report created agents in bootstrap summary
```

See `.claude/skills/agent-creator/references/tech-agent-mappings.md` for full mapping.

---

## LSP Auto-Setup

**IMPORTANT**: After tech detection completes, ALWAYS run LSP setup:

```bash
bash .claude/scripts/lsp-setup.sh
```

This automatically:
1. Detects all languages in the project
2. Installs required language servers
3. Configures LSP for code intelligence

LSP provides:
- Go to definition
- Find references
- Hover documentation
- Symbol navigation
- Call hierarchy

---

## Delegation

Hand off to other skills when:

| Condition | Delegate To |
|-----------|-------------|
| Tech stack confidence is LOW | `interview-agent` - to clarify requirements |
| New/unfamiliar technology detected 2+ times | `meta-skill` - to create specialist skill |
| Detected tech needs specialist agent | `agent-creator` - to create specialist subagent |
| Frontend tech detected (React, Vue, Tailwind, etc.) | `frontend-design` - for UI/styling tasks |
| Architecture decisions needed | `interview-agent` - to gather requirements |
| Languages detected | `lsp-agent` - to install language servers |

**Auto-actions**:
- When detection completes with LOW confidence, automatically suggest invoking the interview-agent.
- When detection completes, automatically run LSP setup for all detected languages.
- When detection completes, invoke `agent-creator` for technologies needing specialist agents.
