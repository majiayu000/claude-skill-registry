---
name: app-template
description: |
  Deploy applications using bjw-s/app-template Helm chart - a flexible chart for helmifying container images without dedicated charts.

  Use when: (1) Deploying container images that lack official Helm charts, (2) Creating HelmRelease manifests for Flux GitOps,
  (3) Configuring multi-container pods with sidecars, (4) Setting up persistent storage, ingress, services for custom applications,
  (5) Questions about app-template values structure or patterns, (6) Deploying any custom container to Kubernetes.

  Triggers: "deploy with app-template", "helmify this image", "create helm release for", "app-template values",
  "sidecar container", "multi-container pod helm", "deploy container image", "no helm chart available",
  "custom container deployment", "bjw-s", "app-template chart", "deploy docker image to kubernetes",
  "container without helm chart", "generic helm chart"
user-invocable: false
---

# app-template Helm Chart

The bjw-s/app-template chart deploys containerized applications without requiring a dedicated Helm chart. It provides a declarative interface for common Kubernetes resources.

**Chart source**: `oci://ghcr.io/bjw-s-labs/helm/app-template`
**Schema**: `https://raw.githubusercontent.com/bjw-s-labs/helm-charts/app-template-4.6.0/charts/other/app-template/values.schema.json`

## Quick Start

Minimal values.yaml for a single-container deployment:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/bjw-s-labs/helm-charts/app-template-4.6.0/charts/other/app-template/values.schema.json
controllers:
  main:
    containers:
      main:
        image:
          repository: nginx
          tag: latest

service:
  main:
    controller: main
    ports:
      http:
        port: 80
```

## Core Structure

### Controllers

Controllers define workload types. Each controller creates one Pod spec.

```yaml
controllers:
  main:                              # Controller identifier (arbitrary name)
    type: deployment                 # deployment|statefulset|daemonset|cronjob|job
    replicas: 1
    strategy: Recreate               # Recreate|RollingUpdate (deployment)

    # Pod-level settings
    pod:
      securityContext:
        fsGroup: 568
        fsGroupChangePolicy: OnRootMismatch

    containers:
      main:                          # Container identifier
        image:
          repository: ghcr.io/org/app
          tag: v1.0.0
        env:
          TZ: UTC
          CONFIG_PATH: /config
```

### Multiple Controllers

Create separate deployments in one release:

```yaml
controllers:
  web:
    containers:
      main:
        image:
          repository: nginx
          tag: latest

  worker:
    type: deployment
    replicas: 3
    containers:
      main:
        image:
          repository: myapp/worker
          tag: v1.0.0
```

### Sidecar Containers

Add sidecars with `dependsOn` for ordering:

```yaml
controllers:
  main:
    containers:
      main:
        image:
          repository: myapp
          tag: v1.0.0

      sidecar:
        dependsOn: main              # Start after main container
        image:
          repository: sidecar-image
          tag: latest
        args: ["--config", "/config/sidecar.yaml"]
```

## Services

Services expose controller pods. Link via `controller` field.

```yaml
service:
  main:
    controller: main                 # Links to controllers.main
    type: ClusterIP                  # ClusterIP|LoadBalancer|NodePort
    ports:
      http:
        port: 8080
      metrics:
        port: 9090

  websocket:
    controller: main
    ports:
      ws:
        port: 3012
```

## Ingress

```yaml
ingress:
  main:
    className: nginx
    hosts:
      - host: app.example.com
        paths:
          - path: /
            pathType: Prefix
            service:
              identifier: main       # References service.main
              port: http             # References port name
    tls:
      - hosts:
          - app.example.com
        secretName: app-tls
```

Multiple paths to different services:

```yaml
ingress:
  main:
    hosts:
      - host: app.example.com
        paths:
          - path: /
            service:
              identifier: main
              port: http
          - path: /ws
            service:
              identifier: websocket
              port: ws
```

## Persistence

### PersistentVolumeClaim

```yaml
persistence:
  config:
    type: persistentVolumeClaim
    accessMode: ReadWriteOnce
    size: 1Gi
    globalMounts:
      - path: /config
```

### Existing PVC

```yaml
persistence:
  config:
    existingClaim: my-existing-pvc
    globalMounts:
      - path: /config
```

### NFS Mount

```yaml
persistence:
  backup:
    type: nfs
    server: nas.local
    path: /volume/backups
    globalMounts:
      - path: /backup
```

### EmptyDir (Shared Between Containers)

```yaml
persistence:
  shared-data:
    type: emptyDir
    globalMounts:
      - path: /shared
```

### Advanced Mounts (Per-Controller/Container)

```yaml
persistence:
  config:
    existingClaim: app-config
    advancedMounts:
      main:                          # Controller identifier
        main:                        # Container identifier
          - path: /config
        sidecar:
          - path: /config
            readOnly: true
```

## Environment Variables

### Direct Values

```yaml
controllers:
  main:
    containers:
      main:
        env:
          TZ: UTC
          LOG_LEVEL: info
          TEMPLATE_VAR: "{{ .Release.Name }}"
```

### From Secrets/ConfigMaps

```yaml
controllers:
  main:
    containers:
      main:
        env:
          DATABASE_URL:
            valueFrom:
              secretKeyRef:
                name: db-secret
                key: url
        envFrom:
          - secretRef:
              name: app-secrets
          - configMapRef:
              name: app-config
```

## Security Context

### Restricted Profile (Required for restricted namespaces)

Namespaces with `security: restricted` (cert-manager, external-secrets, system, database, kromgo) enforce the PodSecurity `restricted` profile. All containers MUST have the following security context or pods will be rejected at admission time.

```yaml
defaultPodOptions:
  securityContext:
    runAsNonRoot: true
    runAsUser: 65534             # Use if image runs as root; omit if image already runs non-root
    runAsGroup: 65534
    fsGroup: 65534
    fsGroupChangePolicy: OnRootMismatch
    seccompProfile:
      type: RuntimeDefault

controllers:
  main:
    containers:
      main:
        image:
          repository: myapp
          tag: v1.0.0
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop: ["ALL"]
```

If the application writes to the filesystem, mount writable `emptyDir` volumes at the required paths rather than disabling `readOnlyRootFilesystem`.

### Pod-Level (Baseline namespaces)

For namespaces with `security: baseline`, a lighter security context is sufficient:

```yaml
defaultPodOptions:
  securityContext:
    runAsUser: 568
    runAsGroup: 568
    fsGroup: 568
    fsGroupChangePolicy: OnRootMismatch

controllers:
  main:
    containers:
      main:
        image:
          repository: myapp
          tag: v1.0.0
```

### Container-Level (Privileged Sidecar)

Only applicable in namespaces with `security: privileged`:

```yaml
controllers:
  main:
    containers:
      main:
        securityContext:
          runAsUser: 568
          runAsGroup: 568

      vpn:
        image:
          repository: vpn-client
          tag: latest
        securityContext:
          capabilities:
            add:
              - NET_ADMIN
```

## Probes

Default probes use TCP on the primary service port. Customize:

```yaml
controllers:
  main:
    containers:
      main:
        probes:
          liveness:
            enabled: true
            custom: true
            spec:
              httpGet:
                path: /health
                port: 8080
              initialDelaySeconds: 10
              periodSeconds: 30
          readiness:
            enabled: true
            type: HTTP
            spec:
              path: /ready
              port: 8080
          startup:
            enabled: false
```

## Resource Limits

Resource limits exist to prevent runaway processes, not to optimize bin-packing. The homelab hardware is heavily over-provisioned — **be generous with limits** rather than running tight to avoid OOMKills and CrashLoopBackOff.

**Guidelines:**
- **Limits should be 2-4x the expected working set** — leave room for spikes, GC pressure, and startup allocations
- **Requests should reflect steady-state usage** — this is what the scheduler uses for placement
- **Never set CPU limits** unless the workload is genuinely CPU-abusive — CPU throttling causes latency spikes and is harder to debug than memory OOMKills
- **When in doubt, go higher** — an OOMKill costs more in debugging time than 128Mi of unused RAM

**Typical ranges for common workloads:**

| Workload Type | Memory Request | Memory Limit |
|--------------|----------------|--------------|
| Lightweight sidecar (gluetun, oauth2-proxy) | 64Mi | 256Mi |
| Web application | 128-256Mi | 512Mi-1Gi |
| Media application (qbittorrent, jellyfin) | 512Mi | 2-4Gi |
| Database (CNPG) | 256Mi | 1-2Gi |

## StatefulSet with VolumeClaimTemplates

```yaml
controllers:
  main:
    type: statefulset
    statefulset:
      volumeClaimTemplates:
        - name: data
          accessMode: ReadWriteOnce
          size: 10Gi
          globalMounts:
            - path: /data
```

## CronJob

```yaml
controllers:
  backup:
    type: cronjob
    cronjob:
      schedule: "0 2 * * *"
      concurrencyPolicy: Forbid
      successfulJobsHistory: 3
      failedJobsHistory: 1
    containers:
      main:
        image:
          repository: backup-tool
          tag: v1.0.0
        args: ["--backup", "/data"]
```

## ServiceMonitor (Prometheus)

```yaml
serviceMonitor:
  main:
    enabled: true
    serviceName: main
    endpoints:
      - port: metrics
        scheme: http
        path: /metrics
        interval: 30s
```

## Flux HelmRelease Integration

For this homelab, app-template deploys via Flux ResourceSet. Add to `kubernetes/platform/helm-charts.yaml`:

```yaml
# In resourcesTemplate, the pattern generates HelmRelease automatically
# For app-template specifically, add to inputs:
- name: "my-app"
  namespace: "default"
  chart:
    name: "app-template"
    version: "4.6.0"
    url: "oci://ghcr.io/bjw-s-labs/helm"  # Note: OCI registry
  dependsOn: [cilium]
```

Values go in `kubernetes/platform/charts/my-app.yaml`.

## Common Patterns

See [references/patterns.md](references/patterns.md) for:
- VPN sidecar with gluetun
- Code-server sidecar for config editing
- Multi-service applications (websocket + http)
- Init containers for setup tasks

See [references/values-reference.md](references/values-reference.md) for complete values.yaml documentation.
