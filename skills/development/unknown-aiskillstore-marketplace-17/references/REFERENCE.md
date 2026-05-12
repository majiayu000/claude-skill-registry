# Xget Reference

Use this file only when the user needs shell setup, deployment, or
troubleshooting details. Reuse the base URL already resolved from
[`SKILL.md`](../SKILL.md), and keep `https://xget.example.com` as a placeholder
only for docs or templates.

## Configuring `XGET_BASE_URL`

Ask which shell the user is using before giving commands when it is unclear.
Offer one of these two setup modes:

### Temporary (current shell or session)

- PowerShell:

```powershell
$env:XGET_BASE_URL = "https://xget.example.com"
```

- bash / zsh:

```bash
export XGET_BASE_URL="https://xget.example.com"
```

- fish:

```fish
set -x XGET_BASE_URL https://xget.example.com
```

### Persistent (future shells)

- PowerShell profile:

```powershell
if (!(Test-Path $PROFILE)) { New-Item -ItemType File -Path $PROFILE -Force | Out-Null }
Add-Content $PROFILE '$env:XGET_BASE_URL = "https://xget.example.com"'
```

- bash:

```bash
echo 'export XGET_BASE_URL="https://xget.example.com"' >> ~/.bashrc
```

- zsh:

```bash
echo 'export XGET_BASE_URL="https://xget.example.com"' >> ~/.zshrc
```

- fish:

```fish
set -Ux XGET_BASE_URL https://xget.example.com
```

After a persistent change, remind the user to open a new shell or reload their
profile before retrying commands.

## Live platform source

The authoritative platform list for this skill comes from:

`https://raw.gitcode.com/xixu-me/xget/raw/main/src/config/platform-catalog.js`

Fetch it from the repository root with:

```bash
node scripts/xget.mjs platforms --format json
```

## README `Use Cases` section

List the latest README `Use Cases` headings first:

```bash
node scripts/xget.mjs topics --format text
```

Narrow the list when the user's task is obvious:

```bash
node scripts/xget.mjs topics --match docker --format text
```

Fetch only the smallest relevant live subsection and rewrite the public demo
domain to your resolved base URL:

```bash
node scripts/xget.mjs snippet --base-url https://xget.example.com --heading "Docker Compose Configuration" --format text
```

If `XGET_BASE_URL` is already configured, the skill can omit `--base-url` and
read from the environment instead.

If a heading is repeated, such as `Use in Project`, fetch its parent section
instead of relying on the ambiguous child title alone.

When the right section is not obvious, prefer `topics --match <tool-or-task>`
over maintaining a second static map in the skill docs. Typical matches are
package managers (`npm`, `pip`, `cargo`), runtime tools (`docker`, `kubernetes`,
`github actions`), AI providers (`openai`, `anthropic`, `gemini`), or hosting
targets (`cloudflare`, `vercel`, `netlify`, `docker compose`).

## Execute instead of paraphrase

When the user wants a change in a real project, adapt the live README snippet to
the target file and run the necessary commands instead of pasting generic
examples back:

- `.npmrc`, `pip.conf`, `NuGet.Config`, `.cargo/config.toml`, `.condarc`
- `Dockerfile`, `docker-compose.yml`, Kubernetes manifests, GitHub Actions
  workflows
- `.env`, SDK initialization code, shell profile files

Treat phrasing like "configure this", "change it", "wire it in", "switch to
Xget", "run this", "fix it", or "deploy it" as a cue to execute. Only fall back
to example commands when the user explicitly asks for examples or a missing fact
prevents safe execution.

## Deployment

For deployment guidance, use the README section on deployment in the:

[Xget deployment guide](https://github.com/xixu-me/xget?tab=readme-ov-file#-deployment)

## Troubleshooting heuristics

- `404` on converted URLs often means the wrong prefix or an unmatched upstream
  platform.
- crates.io conversions should strip the upstream `/api/v1/crates` prefix before
  adding `/crates/...`.
- pip issues often come from adding `trusted-host` unnecessarily or pointing it
  at the wrong host.
- Docker examples must use `/cr/{registry}` prefixes, not plain `/{prefix}`.
- AI SDK examples usually need the Xget base URL changed but keep the original
  API key behavior.
- If the user asks for the “latest” supported platform, refresh the live
  platform map before answering.
