# HubSpot developer platform skill

Agent skill for building and reviewing **HubSpot developer platform** projects: CLI apps, `app-hsmeta.json`, UI extensions (cards, app pages, settings), `@hubspot/ui-extensions`, `hubspot.fetch()`, serverless, scopes, and Marketplace-related constraints. Entry point is [`SKILL.md`](SKILL.md); deeper notes live under [`references/`](references/).

## Install with the Skills CLI (recommended)

Use the open [Skills CLI](https://github.com/vercel-labs/skills) (`npx skills`). It wires this package into each agent’s expected layout (for example **Cursor** under the project’s `.agents/skills/`, and **Claude Code** via symlink when installing globally).

### From GitHub

```bash
npx skills add 0xry4n/hubspot-developer-skill -y
```

### Useful CLI flags

| Flag | Purpose |
| --- | --- |
| `-y`, `--yes` | Skip confirmation prompts |
| `-g`, `--global` | Install under **`~/.agents/skills/`** for all projects on this machine (symlinks into Claude Code; universal bundle for Cursor, Codex, and others per CLI output) |
| `-a`, `--agent` | Limit targets, e.g. `--agent cursor` or `--agent claude-code cursor` |
| `--copy` | Copy files instead of symlinking into agent directories |

Discover and update skills: [skills.sh](https://skills.sh/) · `npx skills find`, `npx skills update`.

### Telemetry

To opt out of anonymous install telemetry: `export DISABLE_TELEMETRY=1` (see [Skills documentation](https://skills.sh/docs/cli)).

### Where files land

The installed directory name comes from the skill **`name`** in `SKILL.md` frontmatter (currently **`hubspot-developer-skill`**), not the GitHub repo name:

- **Project install:** `<your-project>/.agents/skills/hubspot-developer-skill/`
- **Global install:** `~/.agents/skills/hubspot-developer-skill/`

The CLI also writes **`skills-lock.json`** in the project you ran `add` from; commit it if your team should share the same skill versions.

### Do not run `add` from inside this skill repo

Run `npx skills add` from a **consumer** project (or point at this folder with an **absolute path** from elsewhere). Running `npx skills add .` **inside** this repository nests `.agents/` under the skill copy and breaks the install. This repo’s [`.gitignore`](.gitignore) ignores `.agents/` so stray installs are not committed by mistake.

## Alternative: Claude `~/.claude/skills` copy

If you only use Claude’s legacy skills folder and do not use the Skills CLI:

```bash
chmod +x scripts/install-claude-skill.sh
./scripts/install-claude-skill.sh
```

That copies the repo to **`~/.claude/skills/hubspot-developer-skill/`**. Override the root with `CLAUDE_SKILLS_DIR`.

## Manual install

Copy or symlink this repository so **`SKILL.md`** sits at the root of the installed folder; keep the bundled **`references/`** directory alongside it so links in `SKILL.md` resolve.
