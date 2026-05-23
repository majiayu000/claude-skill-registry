---
name: helm-chart-generator
description: "Generate complete Helm charts using the bjw-s-labs common library (app-template). Use when: (1) Creating a new Helm chart for Kubernetes applications, (2) Converting Docker Compose to Helm charts, (3) Setting up controllers with sidecars/init containers, (4) Configuring services, ingress, persistence, or networking, (5) Creating charts with multiple controllers or complex setups. Generates Chart.yaml, values.yaml, templates/common.yaml, and templates/NOTES.txt following bjw-s patterns."
metadata:
  version: "1.0.1"
---

# Helm Chart Generator (bjw-s Common Library)

Generate production-ready Helm charts using the bjw-s-labs common library (app-template v4+).

## Quick Start Workflow

1. **Understand the application**
   - Ask about the container image, ports, environment variables
   - Identify if sidecars/init containers are needed
   - Determine storage requirements (config, data, logs)
   - Check if ingress/networking is required

2. **Generate base structure**
   - Use templates from `assets/templates/`
   - Start with Chart.yaml and basic values.yaml
   - Add templates/common.yaml (minimal, just includes library)
   - Create templates/NOTES.txt for post-install instructions

3. **Build values.yaml progressively**
   - Controllers and containers (main app + sidecars if needed)
   - Services (one per controller or port)
   - Ingress if web-accessible
   - Persistence for stateful data
   - Secrets/ConfigMaps if needed

4. **Validate and refine**
   - Use `scripts/validate_chart.py` to check structure
   - Review against `references/best-practices.md`
   - Test with `helm template` and `helm lint`

## Core Structure

Every chart consists of:

```text
my-app/
├── Chart.yaml           # Chart metadata and dependencies
├── values.yaml          # Configuration values
└── templates/
    ├── common.yaml      # Includes the bjw-s library
    └── NOTES.txt        # Post-install instructions
```

### Chart.yaml Template

```yaml
apiVersion: v2
name: <app-name>
description: <brief description>
type: application
version: 1.0.0
appVersion: "<app version>"
dependencies:
  - name: common
    repository: https://bjw-s-labs.github.io/helm-charts
    version: 4.6.0  # Latest stable version
```

### templates/common.yaml (Always the same)

```yaml
{{- include "bjw-s.common.loader.all" . }}
```

### templates/NOTES.txt

Provide useful post-install information:

- How to access the application
- Default credentials if any
- Next steps for configuration

## values.yaml Structure

Follow this order for clarity:

```yaml
# 1. Default Pod options (optional)
defaultPodOptions:
  securityContext: {}
  annotations: {}

# 2. Controllers (required)
controllers:
  main:  # or custom name
    containers:
      main:  # or custom name
        image: {}
        env: {}
        probes: {}

# 3. Service (required if exposing)
service:
  main:
    controller: main
    ports: {}

# 4. Ingress (optional)
ingress:
  main:
    className: ""
    hosts: []

# 5. Persistence (optional)
persistence:
  config:
    type: persistentVolumeClaim
    # or: emptyDir, configMap, secret, nfs, hostPath

# 6. ConfigMaps/Secrets (optional)
configMaps: {}
secrets: {}
```

## Common Patterns

### Single Container Application

```yaml
controllers:
  main:
    containers:
      main:
        image:
          repository: nginx
          tag: alpine
          pullPolicy: IfNotPresent

service:
  main:
    controller: main
    ports:
      http:
        port: 80

persistence:
  config:
    type: persistentVolumeClaim
    accessMode: ReadWriteOnce
    size: 1Gi
    globalMounts:
      - path: /config
```

### Application with Sidecar

```yaml
controllers:
  main:
    containers:
      main:
        image:
          repository: myapp
          tag: latest
      
      sidecar:
        dependsOn: main
        image:
          repository: sidecar-image
          tag: latest
```

See `references/patterns.md` for more examples:

- Multi-controller setups
- Init containers
- VPN sidecars (gluetun)
- Code-server sidecars
- Shared volumes between containers

## Best Practices

**Always:**

- Use specific image tags, never `:latest`
- Set resource limits and requests
- Configure health checks (liveness, readiness, startup)
- Use non-root security contexts when possible
- Reference services by identifier, not name

**Naming:**

- Controllers: Use descriptive names (not just "main")
- Containers: Use descriptive names (not just "main")
- Services: Match controller name or purpose

**Security:**

- Set `automountServiceAccountToken: false` unless needed
- Configure proper `securityContext`
- Use secrets for sensitive data

**Persistence:**

- Use `globalMounts` for simple cases
- Use `advancedMounts` for complex multi-container scenarios
- Specify `existingClaim` for pre-created PVCs

See `references/best-practices.md` for comprehensive guidelines.

## Key Differences from v3.x

If migrating from app-template v3:

1. **No default objects**: Must explicitly name all controllers, services, etc.
2. **Service references**: Use `identifier` instead of `name`
3. **Resource naming**: New consistent naming scheme
4. **ServiceAccount syntax**: Changed from single `default` to multiple named accounts

See chart upgrade documentation for full migration guide.

## Validation

After generating a chart:

```bash
# Validate structure
python scripts/validate_chart.py /path/to/chart

# Helm validation
cd /path/to/chart
helm lint .
helm template . --debug

# Dry-run installation
helm install --dry-run --debug my-release .
```

## Common Issues

**Services not found**: Use `identifier` not `name` in ingress paths
**Mounts not working**: Check `globalMounts` vs `advancedMounts` usage
**Names too long**: Use `nameOverride` or `fullnameOverride` in global settings
**Controller not starting**: Check `dependsOn` order for init/sidecar containers

## References

- `references/patterns.md` - Common deployment patterns
- `references/best-practices.md` - Kubernetes/Helm best practices
- `references/values-schema.md` - Complete values.yaml reference
- `assets/templates/` - Base templates for quick start
