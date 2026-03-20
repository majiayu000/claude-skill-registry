---
name: aelf-skills-hub
description: >
  Discovery, download, and configuration hub for the entire aelf agent skill ecosystem.
  Use when the user wants to: (1) explore or list available aelf skills,
  (2) install/bootstrap aelf skills into Cursor, Claude Desktop, OpenClaw, Codex, or Claude Code,
  (3) route an aelf-related intent to the correct skill,
  (4) check health or audit installed skills,
  (5) onboard a new skill into the aelf ecosystem.
  Covers domains: Portkey CA wallet, Portkey EOA wallet, Awaken DEX, eForest NFT marketplace,
  AelfScan explorer, TomorrowDAO governance, aelf node interaction.
---

# aelf Skills Hub

One-stop meta-skill for discovering, downloading, configuring, and routing all aelf ecosystem skills.

## Available Skills

Read `skills-catalog.json` for the full machine-readable registry. Current skills:

| ID | Domain |
|---|---|
| `portkey-ca-agent-skills` | CA wallet: registration, auth, guardian, transfer |
| `portkey-eoa-agent-skills` | EOA wallet: create, import, assets, transfer |
| `aelf-node-skill` | Node: chain status, block, tx, contract view/send |
| `aelfscan-skill` | Explorer: address, token, NFT, statistics analytics |
| `awaken-agent-skills` | DEX: quote, swap, liquidity, K-line |
| `eforest-agent-skills` | NFT marketplace: symbol, collection, listing, trade |
| `tomorrowdao-agent-skills` | Governance: DAO, proposals, BP election, resources |

## Workflow

### 1. Route user intent

Read [docs/SKILL_ROUTING_MATRIX.md](docs/SKILL_ROUTING_MATRIX.md) to map intent → skill.

Key rules:
- Wallet: default EOA; switch to CA on guardian/register/recover/CA-hash signals.
- Chain data: `aelf-node-skill` for raw node interaction; `aelfscan-skill` for aggregated analytics.
- DEX/NFT: domain skill handles logic; wallet skill provides signing identity.
- Ambiguous: return Recommended / Alternative / Reason.

### 2. Bootstrap the skill

```bash
./bootstrap.sh --only <skill-id>
```

Options: `--source auto|npm|github|local`, `--skip-install`, `--skip-health`, `--dest <dir>`.

### 3. Configure for client

After bootstrap, run setup inside the downloaded skill directory:

```bash
cd downloaded-skills/<skill-id>
bun run setup openclaw   # for OpenClaw
bun run setup cursor     # for Cursor
bun run setup claude     # for Claude Desktop
```

### 4. Health check

```bash
bun run health:check -- --skills-root ./downloaded-skills
```

## Recovery

| Problem | Action |
|---|---|
| Dependency download failed | `./bootstrap.sh --source github --only <skill-id>` |
| skill-id not found | `bun run catalog:generate`, then retry |
| Health check failed | Follow `health:check` output, add missing artifacts |

## References

- Catalog field semantics: [docs/CATALOG_SCHEMA.md](docs/CATALOG_SCHEMA.md)
- Intent routing matrix: [docs/SKILL_ROUTING_MATRIX.md](docs/SKILL_ROUTING_MATRIX.md)
- E2E scenarios with recovery: [docs/AI_E2E_SCENARIOS.md](docs/AI_E2E_SCENARIOS.md)
- Security audit: `bun run security:audit`
