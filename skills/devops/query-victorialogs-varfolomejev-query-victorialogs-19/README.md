# query-victorialogs

A skill for querying and analyzing logs from [VictoriaLogs](https://docs.victoriametrics.com/victorialogs/) using LogsQL via HTTP API.

**Compatible with:** Claude Code, Codex, and other AI coding tools that support the universal SKILL.md format.

## What It Does

Gives Claude Code the ability to:

- Query logs from VictoriaLogs instances using LogsQL
- Search for errors, trace requests, and investigate issues across services
- Get hit counts and histograms for log patterns
- Discover available fields, streams, and field values
- Safely handle time ranges to avoid server overload

## Installation

```bash
# Via ccpm
ccpm install <your-username>/query-victorialogs

# Or manually
git clone https://github.com/<your-username>/query-victorialogs.git ~/.claude/skills/query-victorialogs
```

## Setup

Add your VictoriaLogs endpoints to your project's `CLAUDE.md`:

```markdown
## VictoriaLogs

- **DEV**: `http://<your-dev-host>:9428`
- **PROD**: `http://<your-prod-host>:9428`

Default to DEV unless user explicitly says "prod" or "production".
```

## Usage Examples

Once installed, just ask Claude Code in natural language:

- "search logs for errors in last 5 minutes"
- "find logs matching user ID u-12345 on prod"
- "check what happened on March 20 around the deployment"
- "get error rate per service in the last hour"
- "tail dev logs for connection refused"

## Skill Structure

```
query-victorialogs/
├── SKILL.md                      # Main skill instructions
├── skill.json                    # CCPM/Claude Code metadata
├── .skillfish.json               # Codex compatibility metadata
├── references/
│   ├── logsql-reference.md       # Full LogsQL syntax (filters, pipes, stats)
│   └── http-api.md               # HTTP API endpoints reference
└── scripts/
    ├── vl-query.sh               # Helper: query logs
    └── vl-hits.sh                # Helper: hit counts
```

## Key Features

**Safe time range handling** — enforces max 3-hour query windows to prevent server overload. When searching by date without a known time, automatically uses a two-step approach: hits first to locate, then query to fetch.

**Full LogsQL support** — filters (word, phrase, regex, field, stream, time), pipes (fields, unpack_json, stats, sort, limit, extract), and all stats functions (count, avg, quantile, rate, etc.).

**Multi-environment** — supports DEV/PROD switching via project CLAUDE.md configuration.

## References

- [VictoriaLogs Documentation](https://docs.victoriametrics.com/victorialogs/)
- [LogsQL Reference](https://docs.victoriametrics.com/victorialogs/logsql/)
- [VictoriaLogs Querying API](https://docs.victoriametrics.com/victorialogs/querying/)

## License

MIT
