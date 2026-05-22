---
name: openshift:routes
description: Manage OpenShift routes for external access to services
---

# OpenShift Routes Skill

Manage OpenShift routes for exposing services externally.

## When to Use

- Exposing services externally
- Configuring TLS/SSL
- Troubleshooting route access
- Setting up custom domains

## Quick Commands

### View Routes

```bash
# All routes
oc get routes -A

# Routes in namespace
oc get routes -n <namespace>

# Route details
oc describe route <route-name> -n <namespace>
```

### Create Routes

```bash
# Simple route (edge TLS)
oc expose svc/<service-name> -n <namespace>

# With custom hostname
oc expose svc/<service-name> -n <namespace> --hostname=myapp.example.com

# Edge TLS (terminate at router)
oc create route edge <route-name> --service=<service-name> -n <namespace>

# Passthrough TLS (end-to-end)
oc create route passthrough <route-name> --service=<service-name> -n <namespace>

# Reencrypt TLS
oc create route reencrypt <route-name> --service=<service-name> \
  --dest-ca-cert=ca.crt -n <namespace>
```

### Get Route URL

```bash
# Get host
oc get route <route-name> -n <namespace> -o jsonpath='{.spec.host}'

# Full URL
echo "https://$(oc get route <route-name> -n <namespace> -o jsonpath='{.spec.host}')"

# Test access
curl -k "https://$(oc get route <route-name> -n <namespace> -o jsonpath='{.spec.host}')"
```

### Modify Routes

```bash
# Add TLS
oc patch route <route-name> -n <namespace> -p '{"spec":{"tls":{"termination":"edge"}}}'

# Change target port
oc patch route <route-name> -n <namespace> -p '{"spec":{"port":{"targetPort":"8080-tcp"}}}'

# Set path
oc patch route <route-name> -n <namespace> -p '{"spec":{"path":"/api"}}'
```

## TLS Termination Types

| Type | Description | Use Case |
|------|-------------|----------|
| `edge` | TLS terminates at router | Most common, router handles certs |
| `passthrough` | TLS passes to pod | Pod handles TLS, end-to-end encryption |
| `reencrypt` | TLS at router, re-encrypts to pod | High security, pod has different cert |

## Troubleshooting

### Route Not Accessible

```bash
# Check route status
oc describe route <route-name> -n <namespace>

# Check service exists
oc get svc <service-name> -n <namespace>

# Check service has endpoints
oc get endpoints <service-name> -n <namespace>

# Check pod is running
oc get pods -n <namespace> -l <selector>

# Check router logs
oc logs -n openshift-ingress deployment/router-default | grep <route-host>
```

### Certificate Issues

```bash
# Check route TLS config
oc get route <route-name> -n <namespace> -o jsonpath='{.spec.tls}'

# Check certificate expiry
echo | openssl s_client -connect <route-host>:443 2>/dev/null | openssl x509 -noout -dates

# View certificate
echo | openssl s_client -connect <route-host>:443 2>/dev/null | openssl x509 -noout -text
```

### DNS Issues

```bash
# Check DNS resolution
nslookup <route-host>
dig <route-host>

# Check wildcard DNS
oc get ingresscontroller default -n openshift-ingress-operator -o jsonpath='{.status.domain}'
```

## Common Patterns

### Expose Kagenti UI

```bash
# Create route for UI
oc expose svc/kagenti-ui -n kagenti-system

# Get URL
echo "https://$(oc get route kagenti-ui -n kagenti-system -o jsonpath='{.spec.host}')"
```

### Expose Agent Service

```bash
# Create edge route with TLS
oc create route edge weather-service \
  --service=weather-service \
  -n team1

# Get agent URL
export AGENT_URL="https://$(oc get route weather-service -n team1 -o jsonpath='{.spec.host}')"
```

## Related Skills

- **openshift:debug**: Debug OpenShift issues
- **k8s:health**: Check platform health
