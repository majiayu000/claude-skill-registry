---
name: gcp-setup
description: "Interactive GCP Cloud Build + Cloud Run setup. Provisions APIs, AR, SAs, IAM, secrets, and triggers."
triggers: "gcp setup, cloud run setup, deploy setup, infrastructure setup, gcp provision"
project-agnostic: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__voicemode__converse
---

# GCP Setup — Cloud Build + Cloud Run

Interactive skill for bootstrapping GCP infrastructure for Cloud Build + Cloud Run projects. Handles everything from `gcloud auth login` to verified production deploy.

## Security First

Every phase validates security posture. The skill enforces:
- Dedicated runtime service account (never default compute SA)
- Per-secret IAM bindings (never project-level secretAccessor)
- Approval-gated Cloud Build triggers
- Non-root container execution
- Optional app-level OAuth with configurable domain restriction
- Same-origin CORS in production
- Secrets in Secret Manager only (never env vars, never in images)

## Tool Paths

All tools are relative to this skill directory:
```
SKILL_DIR="${CLAUDE_PLUGIN_ROOT}/skills/gcp-setup"
```

## Workflow

### Phase 0: Config Detection

Detect and load configuration before any infrastructure operations.

#### 0a: User-Level Customization (BLOCKING)

Check `~/.agents/customization/gcp-setup/index.md` for saved preferences.

If missing, use AskUserQuestion to collect:
- **Company domain** (e.g., `example.com`)
- **Company name** (e.g., `Example Corp`)
- **GitHub organization** (e.g., `ExampleOrg`)
- **Preferred GCP region** (e.g., `us-central1`)

Save to `~/.agents/customization/gcp-setup/index.md`:
```markdown
# GCP Setup Preferences

- domain: example.com
- company: Example Corp
- github_org: ExampleOrg
- region: us-central1
```

If values already exist, present them as defaults. If user provides different values, update `index.md`.

#### 0b: Project-Level Config (BLOCKING)

Detect `.gcp-setup.yml` in the project root.

**If exists:** Load and present current config to user. AskUserQuestion: "Config found. Proceed with these settings, or modify?"

**If missing:** Auto-detect everything possible, then confirm. Typeform-style: one question at a time, smart defaults, minimal friction.

**Step 1: Silent auto-detection** (no user interaction — run all probes first)

```bash
# GitHub repo from git remote
GITHUB_SLUG=$(git remote get-url origin 2>/dev/null | sed -E 's#.*[:/]([^/]+/[^/.]+)(\.git)?$#\1#')
DIR_NAME=$(basename "$(pwd)")

# Runtime + framework
RUNTIME=""
[[ -f package.json ]] && RUNTIME="nodejs"
[[ -f requirements.txt || -f pyproject.toml ]] && RUNTIME="python"
[[ -f go.mod ]] && RUNTIME="go"
FRAMEWORK=""
grep -q '"express"' package.json 2>/dev/null && FRAMEWORK="express"
grep -q 'fastapi' requirements.txt pyproject.toml 2>/dev/null && FRAMEWORK="fastapi"

# Feature detection from code/dependencies
HAS_OAUTH=$(grep -rl -m 1 "passport\|GoogleStrategy\|google-auth-library\|authlib" \
  --include="*.ts" --include="*.js" --include="*.py" \
  --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=vendor . 2>/dev/null | head -1)
HAS_FIRESTORE=$(grep -rl -m 1 "@google-cloud/firestore\|google.cloud.firestore" \
  --include="*.ts" --include="*.js" --include="*.py" --include="*.go" \
  --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=vendor . 2>/dev/null | head -1)

# Build configs, Dockerfile, health endpoint
CLOUDBUILD_FILES=$(ls cloudbuild*.yaml cloudbuild*.yml 2>/dev/null || true)
DOCKERFILE=$(ls Dockerfile */Dockerfile 2>/dev/null | head -1)
HEALTH_EP=$(grep -roh '"/health[z]*"\|"/api/health"' \
  --include="*.ts" --include="*.js" --include="*.py" . 2>/dev/null | head -1 | tr -d '"')

# Secret manifest from .env.example
ENV_EXAMPLE=$(ls .env.example .env.sample env.example 2>/dev/null | head -1)

# GCP projects (for matching)
GCP_PROJECTS=$(gcloud projects list --format="value(projectId)" 2>/dev/null)
```

Load user preferences from Phase 0a (`~/.agents/customization/gcp-setup/index.md`): domain, company, org, region.

**Step 2: Typeform questionnaire** — one AskUserQuestion per step

Rules:
- First option = recommended default (auto-detected or convention-based)
- Skip question entirely if auto-detection is unambiguous (e.g., GitHub repo from remote)
- NEVER ask about convention-derived values — fill them automatically
- Options must be concrete and actionable — no "Chat about this" or "Need to setup later"
- Target: 2-4 questions max for a typical project

**Q1: GCP Projects** (required — cannot auto-detect)

Filter `$GCP_PROJECTS` for pairs matching `*-stage/*-dev` + `*-prod` patterns, or containing `$DIR_NAME`. Present best-match pair first:
1. `detected-app-dev` + `detected-app-prod` (if pair found)
2. Pick from my GCP projects (show filtered short-list)
3. Enter project IDs manually

> **Multi-app pattern:** Multiple apps can share the same GCP projects. Each app gets its own `.gcp-setup.yml` with unique `sa_prefix`, `service_name`, and secret names. Shared resources (AR repo, KMS keyring, GitHub connection) are created idempotently — the second app's provisioning simply finds them already in place. See `cookbook/environments.md` for naming conventions and examples.

**Q2: Service Names** (skip if `$DIR_NAME` is clean)

1. `${DIR_NAME}-stage`, `${DIR_NAME}` — convention: stage suffixed, prod is base name
2. Enter custom names

If `$DIR_NAME` produces clean service names (lowercase, no special chars, <30 chars), skip this question and use option 1 automatically — show in review.

**Q3: Detected Features** (confirmation only)

Present auto-detected features as a summary:
- Runtime: `$RUNTIME` / `$FRAMEWORK` (or "not detected")
- OAuth: Yes/No (based on `$HAS_OAUTH`)
- Firestore: Yes/No (based on `$HAS_FIRESTORE`)
- Health endpoint: `$HEALTH_EP` or `/api/health` (default)

1. Confirm
2. Change (let user toggle specific features)

If nothing ambiguous was detected, skip this question too.

**Q3b: OAuth Mode** (conditional — only when OAuth = Yes from Q3)

> **How should this app handle authentication?**
>
> 1. **Standalone** — This app authenticates users directly via Google OAuth.
>    Each app needs its own redirect URIs registered in the GCP Console.
>    Standard setup for single apps or small teams.
>
> 2. **Auth-proxy** — This app IS a centralized authentication service.
>    Register its OAuth redirect URIs once. Future apps delegate auth to
>    this proxy — no additional Console configuration needed per app.
>    See `cookbook/auth-proxy.md` for full architecture.
>
> 3. **IAP** (recommended for internal tools) — Google Cloud Identity-Aware Proxy.
>    Google manages the entire auth flow. Enable per service with one CLI flag
>    (`--iap`). No redirect URIs, no OAuth clients to manage per app, no extra
>    infrastructure. Access controlled via IAM policies.
>    Trade-off: no custom login UI (Google's IAP login page).
>    See `cookbook/iap-setup.md` for setup guide.

Cannot be auto-detected — always ask when OAuth is enabled.

Set `oauth.mode` to `standalone` (option 1), `auth-proxy` (option 2), or `iap` (option 3).

**Q4: Review & Generate**

Build the COMPLETE config YAML from auto-detected values + user answers + conventions. Present it formatted.

Convention-derived values (NEVER ask the user for these):
- `artifact_registry.repo_name`: `docker-images`
- `sa_prefix.runtime`: `app-runtime`
- `sa_prefix.cloudbuild`: `app-cloudbuild`
- `kms.keyring`: `cloudbuild-keys`
- `kms.key`: `connection-key`
- `github.connection_name`: repo name from slug
- `github.linked_repo`: slug with `/` replaced by `-`
- `oauth.callback_path`: `/auth/google/cb` (Express + Passport) or `/api/auth/callback/google` (Auth.js / NextAuth) — register BOTH in OAuth client redirect URIs
- `oauth.domain_restriction`: company domain from user preferences
- `oauth.consent_type`: `Internal`
- `oauth.mode`: from Q3b answer (default: `standalone`). When `iap` is selected, `oauth.callback_path` and `oauth.consent_type` are not used (IAP manages these).
- `firestore.collection`: `express-sessions`
- `firestore.ttl_field`: `expiresAt`
- Build configs: detected files or `cloudbuild-stage.yaml` / `cloudbuild-prod.yaml`
- Secrets: OAuth secrets if OAuth detected + `session-secret` with `auto_generate: true`

1. Save as `.gcp-setup.yml`
2. Modify specific values (re-present after changes)

Generate `.gcp-setup.yml` using `assets/gcp-setup-example.yml` as template reference. Write to project root.

> `.gcp-setup.yml` contains no secrets and should be committed to version control.

**After saving config, ensure `.env` files are gitignored:**

```bash
# Ensure .env files are gitignored (secret values must never be committed)
if [[ -f .gitignore ]]; then
  grep -qxF '.env' .gitignore || echo '.env' >> .gitignore
  grep -qxF '.env.*' .gitignore || echo '.env.*' >> .gitignore
else
  printf '.env\n.env.*\n' > .gitignore
fi
```

#### 0c: Build Files Generation

After config is saved, check for missing build files and generate from templates. See `cookbook/build-setup.md` for the full non-tech guide.

**Detection** (uses variables from Phase 0b Step 1):
```bash
HAS_DOCKERFILE=$([[ -n "$DOCKERFILE" ]] && echo true || echo false)
HAS_DOCKERIGNORE=$([[ -f .dockerignore ]] && echo true || echo false)
HAS_CLOUDBUILD=$([[ -n "$CLOUDBUILD_FILES" ]] && echo true || echo false)
```

**1. `.dockerignore`** (always generate if missing):
```bash
cp "$SKILL_DIR/assets/dockerignore-template" .dockerignore
```

**2. `Dockerfile`** (generate if missing, based on detected `$RUNTIME`):

| Runtime | Template | Default CMD |
|---------|----------|-------------|
| `nodejs` | `$SKILL_DIR/assets/dockerfile-node.template` | `CMD ["node", "server.js"]` |
| `python` | `$SKILL_DIR/assets/dockerfile-python.template` | `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]` |
| `go` | `$SKILL_DIR/assets/dockerfile-go.template` | `ENTRYPOINT ["/app/server"]` |

After copying the template, adjust the `CMD`/`ENTRYPOINT` based on detected framework and entry point:
- Express: detect `main` field in `package.json` or `server.js`/`index.js`/`app.js`
- Next.js: `CMD ["npm", "start"]`
- FastAPI: detect `main:app` or `app.main:app` from imports
- Flask/Django: detect `app:app` or `project.wsgi:application`

If runtime is not detected, use AskUserQuestion to ask which runtime to use.

**3. CloudBuild YAMLs** (generate if missing):

Read `$SKILL_DIR/assets/cloudbuild-template.yaml` and substitute tokens from config. Generate TWO files:

**`cloudbuild-stage.yaml`:**
```bash
CONFIG=".gcp-setup.yml"
PROJECT_ID=$(yq -r '.projects.stage.id' "$CONFIG")
SERVICE_NAME=$(yq -r '.projects.stage.service_name' "$CONFIG")
REGION=$(yq -r '.region' "$CONFIG")
REPO_NAME=$(yq -r '.artifact_registry.repo_name' "$CONFIG")
IMAGE_NAME="$SERVICE_NAME"
MAX_INSTANCES=$(yq -r '.app.max_instances_stage // 5' "$CONFIG")
SA_PREFIX=$(yq -r '.sa_prefix.runtime' "$CONFIG")
RUNTIME_SA="${SA_PREFIX}@${PROJECT_ID}.iam.gserviceaccount.com"
APP_DIR=$(dirname "$(yq -r '.app.dockerfile_path // "Dockerfile"' "$CONFIG")")
[[ "$APP_DIR" == "." || -z "$APP_DIR" ]] && APP_DIR="."

# Resolve auth flag and IAP settings based on oauth.mode
OAUTH_MODE=$(yq -r '.oauth.mode // "standalone"' "$CONFIG")
if [[ "$OAUTH_MODE" == "iap" ]]; then
  _AUTH_FLAG="--no-allow-unauthenticated"
  _IAP_FLAG="--iap"
  _ENTRYPOINT="gcloud beta"
else
  _AUTH_FLAG="--allow-unauthenticated"
  _IAP_FLAG=""
  _ENTRYPOINT="gcloud"
fi

# Generate secrets mapping from manifest
SECRETS_MAPPING=""
SECRET_COUNT=$(yq -r '.secrets | length' "$CONFIG")
for ((i=0; i<SECRET_COUNT; i++)); do
  NAME=$(yq -r ".secrets[$i].name" "$CONFIG")
  ENV_VAR=$(yq -r ".secrets[$i].env_var" "$CONFIG")
  [[ -n "$SECRETS_MAPPING" ]] && SECRETS_MAPPING="${SECRETS_MAPPING},"
  SECRETS_MAPPING="${SECRETS_MAPPING}${ENV_VAR}=${NAME}:latest"
done
```

Substitute all `__TOKEN__` placeholders in the template and write to `cloudbuild-stage.yaml`:
- Replace `__ENTRYPOINT__` with `$_ENTRYPOINT` (i.e., `gcloud beta` for IAP, `gcloud` otherwise)
- Replace `__AUTH_FLAG__` with `$_AUTH_FLAG`
- If `$_IAP_FLAG` is non-empty, replace `__IAP_FLAG__` with `--iap`
- If `$_IAP_FLAG` is empty, **remove the entire `- '__IAP_FLAG__'` line** from the generated YAML (do not leave an empty string arg)
- If `$SECRETS_MAPPING` is empty, **remove the entire `--set-secrets=__SECRETS_MAPPING__` line** (an empty `--set-secrets=` causes deploy failure)
- If `$ENV_VARS` is empty, **remove the entire `--set-env-vars=__ENV_VARS__` line** (an empty `--set-env-vars=` causes deploy failure)

**`cloudbuild-prod.yaml`:** Same process with prod values and `max_instances_prod` (default: `100`).

**AskUserQuestion gate:** Present a summary of generated files:
```
Generated build files:
  - .dockerignore (universal exclusions)
  - Dockerfile (Node.js multi-stage, non-root)
  - cloudbuild-stage.yaml (stage project, max 5 instances)
  - cloudbuild-prod.yaml (prod project, max 100 instances)

Review and confirm, or modify specific files.
```

All generated files should be committed to version control.

#### 0d: Project Documentation

After build files are in place, generate project documentation if missing. These docs help onboard new team members and guide AI assistants.

**Detection:**
```bash
HAS_SECRETS_GUIDE=$([[ -f docs/managing-secrets-and-envs.md ]] && echo true || echo false)
HAS_README=$([[ -f README.md ]] && echo true || echo false)
HAS_AGENTS=$([[ -f AGENTS.md || -f CLAUDE.md ]] && echo true || echo false)
```

**Compute deterministic URLs** (needed for templates):
```bash
CONFIG=".gcp-setup.yml"
STAGE_PROJECT=$(yq -r '.projects.stage.id' "$CONFIG")
PROD_PROJECT=$(yq -r '.projects.prod.id' "$CONFIG")
STAGE_SERVICE=$(yq -r '.projects.stage.service_name' "$CONFIG")
PROD_SERVICE=$(yq -r '.projects.prod.service_name' "$CONFIG")
REGION=$(yq -r '.region' "$CONFIG")
STAGE_NUM=$(gcloud projects describe "$STAGE_PROJECT" --format="value(projectNumber)")
PROD_NUM=$(gcloud projects describe "$PROD_PROJECT" --format="value(projectNumber)")
STAGE_URL="https://${STAGE_SERVICE}-${STAGE_NUM}.${REGION}.run.app"
PROD_URL="https://${PROD_SERVICE}-${PROD_NUM}.${REGION}.run.app"
CB_CONSOLE_STAGE="https://console.cloud.google.com/cloud-build/builds;region=${REGION}?project=${STAGE_PROJECT}"
CB_CONSOLE_PROD="https://console.cloud.google.com/cloud-build/builds;region=${REGION}?project=${PROD_PROJECT}"
```

**For each missing doc, generate from template:**

1. **`docs/managing-secrets-and-envs.md`** — Read `$SKILL_DIR/assets/managing-secrets-and-envs.template.md`, substitute tokens from config. Generate `${SECRETS_TABLE}` from secrets manifest:
   ```
   | Secret Name | Env Var | Environments |
   |-------------|---------|--------------|
   | oauth-client-id | GOOGLE_CLIENT_ID | stage, prod |
   ...
   ```
   Generate `${ENV_VARS_TABLE}` for non-secret env vars (`AUTH_URL`, `AUTH_TRUST_HOST`, etc.).
   Create `docs/` directory if needed.

2. **`README.md`** — Read `$SKILL_DIR/assets/readme.template.md`, substitute tokens. Set `${PROJECT_NAME}` from directory name (title-cased). Set `${PROJECT_DESCRIPTION}` from a brief AskUserQuestion or auto-detect from `package.json` description. Compute `${HEALTH_ENDPOINT}` and `${HEALTH_RESPONSE}` from config.

3. **`AGENTS.md`** — Read `$SKILL_DIR/assets/agents.template.md`, substitute tokens. Framework-specific values:

   | Token | Node.js/Express | Node.js/Next.js | Python/FastAPI | Go |
   |-------|----------------|-----------------|----------------|-----|
   | `${RUNTIME_DISPLAY}` | Node.js 22 (Alpine in Docker) | Node.js 22 (Alpine in Docker) | Python 3.12 (slim in Docker) | Go 1.23 (distroless in Docker) |
   | `${LANGUAGE}` | JavaScript/TypeScript | TypeScript (strict mode) | Python | Go |
   | `${PACKAGE_MANAGER}` | npm | npm | pip | go modules |
   | `${BUILD_CMD}` | `npm run build` | `npm run build` | N/A | `go build` |
   | `${DEV_CMD}` | `npm run dev` | `npm run dev` | `uvicorn main:app --reload` | `go run .` |
   | `${LINT_CMD}` | `npm run lint` | `npm run lint` | `ruff check` | `golangci-lint run` |
   | `${TYPECHECK_CMD}` | `npx tsc --noEmit` | `npx tsc --noEmit` | `pyright` | `go vet ./...` |

   `${STYLE_CONVENTIONS}` — framework-specific conventions (App Router for Next.js, route structure for Express, etc.).
   `${AUTH_DESCRIPTION}` — derived from oauth config (e.g., "Google OAuth with `@example.com` domain restriction (Auth.js v5)").

**AskUserQuestion gate:** Present generated docs summary:
```
Generated project documentation:
  - docs/managing-secrets-and-envs.md (secrets guide with current inventory)
  - README.md (environments, local dev, deploy workflow)
  - AGENTS.md (AI assistant project guidelines)

Review and confirm, or modify specific files.
```

All generated docs should be committed to version control.

#### 0e: GCP State Probe

Probe existing infrastructure state (unchanged logic, reads from config):

```bash
CONFIG=".gcp-setup.yml"
STAGE=$(yq -r '.projects.stage.id' "$CONFIG")
PROD=$(yq -r '.projects.prod.id' "$CONFIG")

# Quick check — do APIs exist?
gcloud services list --enabled --filter="name:run.googleapis.com" --project="$STAGE" --format="value(name)" 2>/dev/null
```

Present state table to user and use AskUserQuestion:
- "Here's what already exists. Which phases do you want to run? (0=all from scratch, 1=preflight only, 2=provision, 3=secrets, 4=oauth, 5=verify)"
- If everything exists: suggest Phase 5 (verify) only

### Phase 1: Preflight Validation

```bash
bash "$SKILL_DIR/tools/preflight.sh" --config .gcp-setup.yml
```

**AskUserQuestion gate:** If any required check fails, present install instructions and wait for confirmation before proceeding.

### Phase 2: GCP Resource Provisioning

**MANDATORY — CMEK Encryption Key Setup:**

Before creating the GitHub connection, provision a Cloud KMS encryption key. Connection data (including GitHub OAuth tokens stored in Secret Manager) MUST be encrypted with a customer-managed key.

```bash
bash "$SKILL_DIR/tools/provision.sh" --config .gcp-setup.yml --cmek-only --env all
```

This enables the Cloud KMS API, creates the keyring + key, provisions the Secret Manager service agent, and grants it `cryptoKeyEncrypterDecrypter` on the key.

**MANUAL GATE — 2nd-gen GitHub Connection:**

After CMEK setup, the user must create GitHub connections in both GCP projects. This CANNOT be automated (requires browser OAuth).

Use AskUserQuestion: "CMEK keys are provisioned. Have you created the 2nd-gen GitHub connection in Cloud Build for both projects? You MUST select the encryption key during connection creation."

If NO, read and present the guide:
```bash
cat "$SKILL_DIR/cookbook/oauth-setup.md"
```

Present the Console URLs (read project IDs from config):
```bash
STAGE=$(yq -r '.projects.stage.id' .gcp-setup.yml)
PROD=$(yq -r '.projects.prod.id' .gcp-setup.yml)
echo "Stage: https://console.cloud.google.com/cloud-build/repositories/2nd-gen?project=$STAGE"
echo "Prod: https://console.cloud.google.com/cloud-build/repositories/2nd-gen?project=$PROD"
```

Steps:
1. Open Console URL
2. Click "Create Host Connection" -> GitHub
3. Set **Region** from config
4. Set **Name** from `github.connection_name`
5. **Encryption:** Select the KMS key — do NOT skip this
6. Click **Connect** -> Authorize Cloud Build GitHub App
7. Link the repository

> **SECURITY WARNING:** Do NOT skip the encryption key selection. Google-managed encryption is NOT acceptable. The connection stores GitHub OAuth tokens in Secret Manager — these must be encrypted with the customer-managed key for key rotation control and compliance.

Wait for user confirmation.

**Run provision:**
```bash
bash "$SKILL_DIR/tools/provision.sh" --config .gcp-setup.yml --env all
```

> **Note:** The temporary `secretmanager.admin` grant auto-expires in 20 minutes. No manual revocation needed.

### Phase 3: Secrets Setup

**Create secret shells:**
```bash
bash "$SKILL_DIR/tools/secrets.sh" --config .gcp-setup.yml --action create --env all
```

**AskUserQuestion:** "How do you want to populate secrets?"
- Option A: From an existing .env file -> `--action populate --env-file /path/to/.env`
- Option B: Interactively (guided prompts)

**Populate secrets:**
```bash
bash "$SKILL_DIR/tools/secrets.sh" --config .gcp-setup.yml \
  --action populate --env "$TARGET_ENV" --env-file "$ENV_FILE"
```

**SECURITY WARNING:** If populating both envs from the same .env, warn:
> "OAuth credentials SHOULD differ per environment. Consider running `--env stage` first, then `--env prod --env-file /path/to/prod.env`."

### Phase 4: Authentication Configuration (Conditional)

**Skip entirely when `oauth.enabled` is `false` in config.**

Read `oauth.mode` from config (default: `standalone`).

---

#### Mode: IAP (recommended for internal tools)

When `oauth.mode` is `iap`, authentication is handled entirely by Google Cloud Identity-Aware Proxy. No OAuth clients, no redirect URIs, no custom auth code needed.

**One-time project setup** (first time enabling IAP in this GCP project):

1. **Enable required APIs:**
   ```bash
   for PROJECT in "$STAGE_PROJECT" "$PROD_PROJECT"; do
     gcloud services enable iap.googleapis.com cloudresourcemanager.googleapis.com --project="$PROJECT"
   done
   ```

2. **Configure Google Auth Platform** (Console — one time per project):
   - Go to **Google Auth Platform > Branding** in GCP Console
   - Set app name, support email, authorized domain
   - Go to **Audience** and set to configured consent type (default: **Internal**)
   - Go to **Data Access** and add scopes: `openid`, `email`, `profile`

3. **AskUserQuestion gate:**
   - "Have you configured Google Auth Platform (Branding + Audience) in the GCP Console? This is a one-time step per project."

**Per-service setup** (automated — repeat for each app):

4. **Enable IAP on Cloud Run services:**
   ```bash
   for PROJECT in "$STAGE_PROJECT" "$PROD_PROJECT"; do
     ENV_KEY=$( [ "$PROJECT" = "$STAGE_PROJECT" ] && echo stage || echo prod )
     SERVICE_NAME=$(yq -r ".projects.${ENV_KEY}.service_name" "$CONFIG")
     # For existing services:
     gcloud beta run services update "$SERVICE_NAME" \
       --region="$REGION" \
       --iap \
       --project="$PROJECT"
     # For new deploys, use: gcloud beta run deploy ... --iap --no-allow-unauthenticated
   done
   ```
   > **Note:** `services update --iap` works on already-deployed services. For first deploys, use `gcloud beta run deploy ... --iap --no-allow-unauthenticated` or add these flags to the CloudBuild deploy step.

5. **Grant IAP service agent invoker permission:**
   ```bash
   for PROJECT in "$STAGE_PROJECT" "$PROD_PROJECT"; do
     ENV_KEY=$( [ "$PROJECT" = "$STAGE_PROJECT" ] && echo stage || echo prod )
     SERVICE_NAME=$(yq -r ".projects.${ENV_KEY}.service_name" "$CONFIG")
     PROJECT_NUMBER=$(gcloud projects describe "$PROJECT" --format='value(projectNumber)')
     gcloud run services add-iam-policy-binding "$SERVICE_NAME" \
       --region="$REGION" \
       --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-iap.iam.gserviceaccount.com" \
       --role="roles/run.invoker" \
       --project="$PROJECT"
   done
   ```

6. **Remove public access** (if the service was previously public):
   ```bash
   for PROJECT in "$STAGE_PROJECT" "$PROD_PROJECT"; do
     ENV_KEY=$( [ "$PROJECT" = "$STAGE_PROJECT" ] && echo stage || echo prod )
     SERVICE_NAME=$(yq -r ".projects.${ENV_KEY}.service_name" "$CONFIG")
     gcloud run services remove-iam-policy-binding "$SERVICE_NAME" \
       --region="$REGION" \
       --member="allUsers" \
       --role="roles/run.invoker" \
       --project="$PROJECT" 2>/dev/null || true
   done
   ```
   > **Warning:** If `allUsers` has `roles/run.invoker`, anyone can bypass IAP by calling the Cloud Run URL directly. Always remove public access when enabling IAP.

7. **Grant domain access:**
   ```bash
   DOMAIN=$(yq -r '.oauth.domain_restriction' "$CONFIG")
   for PROJECT in "$STAGE_PROJECT" "$PROD_PROJECT"; do
     ENV_KEY=$( [ "$PROJECT" = "$STAGE_PROJECT" ] && echo stage || echo prod )
     SERVICE_NAME=$(yq -r ".projects.${ENV_KEY}.service_name" "$CONFIG")
     gcloud beta iap web add-iam-policy-binding \
       --resource-type=cloud-run \
       --service="$SERVICE_NAME" \
       --region="$REGION" \
       --member="domain:${DOMAIN}" \
       --role="roles/iap.httpsResourceAccessor" \
       --project="$PROJECT"
   done
   ```

8. **Read the IAP cookbook:**
   ```bash
   cat "$SKILL_DIR/cookbook/iap-setup.md"
   ```

9. **Present IAP guidance** to the user:
   - IAP is now active. Users visiting the app will see Google's IAP login page.
   - The app receives user identity via headers: `X-Goog-Authenticated-User-Email` and `X-Goog-IAP-JWT-Assertion`.
   - Future apps: just add `--iap --no-allow-unauthenticated` to the deploy command and run the IAM bindings above. No Console changes needed.
   - See `cookbook/iap-setup.md` for header verification, service-to-service auth, and local development.

> **Note:** When `oauth.mode` is `iap`, OAuth secrets (`oauth-client-id`, `oauth-client-secret`) are NOT needed in the secrets manifest. Google manages the OAuth client internally. Only `session-secret` is needed if the app manages its own sessions.

---

#### Mode: Standalone (default)

When `oauth.mode` is `standalone` (or not set):

**SECURITY WARNING — Display this to the user before proceeding:**

> **The OAuth consent screen MUST be set to the configured consent type (default: "Internal").** If set to "Internal", this restricts authentication to the configured domain only. Do NOT select "External" unless required — doing so would allow ANY Google account to reach the OAuth flow. If you are unsure, stop and consult the team.

This sub-phase is entirely manual. The skill provides exact step-by-step guidance.

1. **Compute deterministic Cloud Run URLs:**
   ```bash
   CONFIG=".gcp-setup.yml"
   STAGE=$(yq -r '.projects.stage.id' "$CONFIG")
   PROD=$(yq -r '.projects.prod.id' "$CONFIG")
   STAGE_SVC=$(yq -r '.projects.stage.service_name' "$CONFIG")
   PROD_SVC=$(yq -r '.projects.prod.service_name' "$CONFIG")
   REGION=$(yq -r '.region' "$CONFIG")
   STAGE_NUM=$(gcloud projects describe "$STAGE" --format="value(projectNumber)")
   PROD_NUM=$(gcloud projects describe "$PROD" --format="value(projectNumber)")
   echo "Stage URL: https://${STAGE_SVC}-${STAGE_NUM}.${REGION}.run.app"
   echo "Prod URL:  https://${PROD_SVC}-${PROD_NUM}.${REGION}.run.app"
   ```
   > **Warning:** Do NOT use `status.url` to get the service URL for OAuth configuration. It returns a legacy hash-based URL that differs from the deterministic format. Always compute deterministic URLs.

2. **Read the full OAuth guide:**
   ```bash
   cat "$SKILL_DIR/cookbook/oauth-setup.md"
   ```

3. **Present step-by-step** with pre-computed URLs:
   - Configure Google Auth Platform: Branding, Audience, Data Access
   - Create per-environment OAuth 2.0 Client IDs
   - Register callback URLs: `https://<cloud-run-url><callback_path from config>`
   - Add authorized JavaScript origins

4. **AskUserQuestion gates:**
   - "Have you configured Google Auth Platform (Audience set to configured consent type) in the GCP project?"
   - "Have you created OAuth 2.0 Client IDs for each environment?"
   - "Have you populated the oauth secrets via Phase 3?"

---

#### Mode: Auth-Proxy (Additional Steps)

**When `oauth.mode` is `auth-proxy`**, first complete ALL standalone steps above (the proxy itself needs OAuth registration), then:

5. **Read the auth-proxy cookbook:**
   ```bash
   cat "$SKILL_DIR/cookbook/auth-proxy.md"
   ```

6. **Present auth-proxy guidance** to the user:
   - This app is the centralized auth service. The OAuth registration just completed is the ONLY registration needed.
   - Future apps that need authentication will delegate to this proxy instead of registering with Google directly.
   - The proxy must implement: Google OAuth flow, JWT signing with a shared secret, `return_url` allowlist validation, domain restriction.
   - Client apps must implement: redirect to proxy, JWT verification, session creation.
   - Share the proxy URL with the team: `https://<proxy-service>-<project-num>.<region>.run.app`
   - See `cookbook/auth-proxy.md` for the complete architecture, implementation checklist, and client integration guide.

7. **AskUserQuestion gate:**
   - "Have you reviewed the auth-proxy architecture in `cookbook/auth-proxy.md`? This app will serve as the centralized auth service for future apps."

### Phase 5: Verification

**Run full verification:**
```bash
bash "$SKILL_DIR/tools/verify.sh" --config .gcp-setup.yml --env all
```

**Interpret results:**
- All PASS -> Setup complete. Present next steps (first deploy, PR workflow).
- Any FAIL -> Present remediation commands from verify.sh output.
- Re-run verify after remediation.

### Post-Setup: First Deploy

After all phases pass, guide the user through the first deploy:

1. Push a branch and open a PR
2. Comment `/gcbrun` on the PR to trigger stage build
3. Approve the build in Cloud Build console
4. Wait for build + deploy
5. Verify health check using configured endpoint
6. If OAuth enabled: test authentication with configured domain account
7. Merge PR to main for production deploy

### Troubleshooting

If issues arise post-deploy, run diagnostics:
```bash
bash "$SKILL_DIR/tools/diagnose.sh" --config .gcp-setup.yml --env "$TARGET_ENV"
```

For detailed troubleshooting reference:
```bash
cat "$SKILL_DIR/cookbook/troubleshooting.md"
```

## CI Setup: PR Template

To add the deploy checklist to PRs:
```bash
cat "$SKILL_DIR/assets/pr-template.md"
```

Copy this to `.github/PULL_REQUEST_TEMPLATE.md`, replacing `${STAGE_URL}` and `${CB_CONSOLE_URL}` with actual values.

## Reference

| Resource | Location |
|----------|----------|
| Build setup guide | `cookbook/build-setup.md` |
| Prerequisites | `cookbook/prerequisites.md` |
| Security model | `cookbook/security-model.md` |
| OAuth setup guide | `cookbook/oauth-setup.md` |
| Auth.js on Cloud Run | `cookbook/authjs-setup.md` |
| Auth-proxy guide | `cookbook/auth-proxy.md` |
| IAP setup guide | `cookbook/iap-setup.md` |
| Troubleshooting | `cookbook/troubleshooting.md` |
| Environment configs | `cookbook/environments.md` |
| Cloud Build template | `assets/cloudbuild-template.yaml` |
| PR template | `assets/pr-template.md` |
| .env template | `assets/env-example` |
| Secrets guide template | `assets/managing-secrets-and-envs.template.md` |
| README template | `assets/readme.template.md` |
| AGENTS.md template | `assets/agents.template.md` |
| Config example | `assets/gcp-setup-example.yml` |
