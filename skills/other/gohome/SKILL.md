---
name: gohome
description: Use when Moltbot needs to test or operate GoHome via gRPC discovery, metrics, and Grafana.
metadata: {"moltbot":{"nix":{"plugin":"github:joshp123/gohome","systems":["x86_64-linux","aarch64-linux"]},"config":{"requiredEnv":["GOHOME_GRPC_ADDR","GOHOME_HTTP_BASE"],"example":"config = { env = { GOHOME_GRPC_ADDR = \"gohome:9000\"; GOHOME_HTTP_BASE = \"http://gohome:8080\"; }; };"},"cliHelp":"GoHome CLI\n\nUsage:\n  gohome-cli [command]\n\nAvailable Commands:\n  services   List registered services\n  plugins    Inspect loaded plugins\n  methods    List RPC methods\n  call       Call an RPC method\n  roborock   Manage roborock devices\n  tado       Manage tado zones\n\nFlags:\n  --grpc-addr string   gRPC endpoint (host:port)\n  -h, --help           help for gohome-cli\n"}}
---

# GoHome Skill

## Quick start

```bash
export GOHOME_HTTP_BASE="http://gohome:8080"
export GOHOME_GRPC_ADDR="gohome:9000"
```

## CLI

```bash
gohome-cli services
```

## Discovery flow (read-only)

1) List plugins.
2) Describe a plugin.
3) List RPC methods.
4) Call a read-only RPC.

## Metrics validation

```bash
curl -s "${GOHOME_HTTP_BASE}/gohome/metrics" | rg -n "gohome_"
```

## Stateful actions

Only call write RPCs after explicit user approval.
