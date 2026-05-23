---
name: create-plugin
description: "Add a new datasource plugin to ethpandaops/mcp. Triggers on: add plugin, new plugin, create plugin, add datasource."
---

# Create New Plugin

Add a datasource plugin following the existing patterns.

## Files to Create

```
plugins/{name}/
├── config.go        # Config struct + Validate() + ApplyDefaults()
├── plugin.go        # Implements plugin.Plugin interface
├── examples.go      # Embeds examples.yaml
├── examples.yaml    # Query examples
└── python/{name}.py # Sandbox module (connects via proxy)
```

Plus:
- `pkg/proxy/handlers/{name}.go` - Reverse proxy handler

## Templates

Copy from `plugins/prometheus/` for a simple plugin, or `plugins/clickhouse/` for one with schema discovery.

## Registration Steps

1. **builder.go** - Import and add `reg.Add({name}plugin.New())`
2. **builder.go** - Add case to `buildProxy()` type switch
3. **pkg/proxy/proxy.go** - Add field to `Options` struct
4. **pkg/proxy/proxy.go** - Register handler in `Start()`
5. **sandbox/ethpandaops/ethpandaops/__init__.py** - Add to lazy imports
6. Copy Python module to `sandbox/ethpandaops/ethpandaops/`

## Key Rules

- **Credentials NEVER go to sandbox** - use `SandboxEnv()` for metadata only
- **ProxyConfig()** returns credentials for the proxy handler
- Python module reads `ETHPANDAOPS_{NAME}_DATASOURCES` env var (JSON, no creds)
- Python module calls proxy at `/{name}/{instance}/...`

## Checklist

- [ ] Implements all `plugin.Plugin` methods (see `pkg/plugin/plugin.go`)
- [ ] Proxy handler follows pattern in `pkg/proxy/handlers/prometheus.go`
- [ ] `make lint && make test` pass
- [ ] `make docker-sandbox` builds
