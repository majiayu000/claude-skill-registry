---
name: openshift:debug
description: Debug OpenShift-specific resources, operators, and platform issues
---

# OpenShift Debug Skill

Debug OpenShift-specific resources and platform issues.

## When to Use

- OpenShift operators not working
- Cluster operator issues
- Authentication/OAuth problems
- Route or ingress issues
- Build failures

## Quick Diagnostics

### Cluster Health

```bash
# Cluster version and status
oc get clusterversion
oc describe clusterversion version

# Cluster operators status
oc get clusteroperators
oc get clusteroperators -o json | jq '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'

# Check for degraded operators
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | "\(.metadata.name): \(.status.conditions[] | select(.type=="Degraded") | .message)"'
```

### Operator Debugging

```bash
# List installed operators
oc get csv -A

# Check operator logs
oc logs -n openshift-operators deployment/<operator-name>

# Check install plans
oc get installplans -A

# Check subscriptions
oc get subscriptions -A
```

### Authentication Issues

```bash
# Check OAuth status
oc get clusteroperator authentication
oc describe clusteroperator authentication

# Check OAuth pods
oc get pods -n openshift-authentication

# Check OAuth logs
oc logs -n openshift-authentication deployment/oauth-openshift
```

### Route Issues

```bash
# List all routes
oc get routes -A

# Check route status
oc describe route <route-name> -n <namespace>

# Check ingress controller
oc get ingresscontroller -n openshift-ingress-operator
oc logs -n openshift-ingress-operator deployment/ingress-operator
```

### Build Issues

```bash
# Check builds
oc get builds -A

# Check build logs
oc logs -n <namespace> build/<build-name>

# Check build config
oc describe buildconfig <bc-name> -n <namespace>
```

## OpenShift-Specific Resources

### Routes

```bash
# Get route URL
oc get route <route-name> -n <namespace> -o jsonpath='{.spec.host}'

# Check route TLS
oc get route <route-name> -n <namespace> -o jsonpath='{.spec.tls.termination}'
```

### Security Context Constraints

```bash
# List SCCs
oc get scc

# Check which SCC a pod uses
oc get pod <pod-name> -n <namespace> -o jsonpath='{.metadata.annotations.openshift\.io/scc}'

# Check SCC details
oc describe scc <scc-name>
```

### Service Accounts

```bash
# List service accounts
oc get sa -n <namespace>

# Check SA tokens
oc get secrets -n <namespace> | grep <sa-name>

# Add SCC to service account
oc adm policy add-scc-to-user <scc-name> -z <sa-name> -n <namespace>
```

## Common Issues

### Issue: Route not accessible

```bash
# Check route exists
oc get route <route-name> -n <namespace>

# Check service has endpoints
oc get endpoints <service-name> -n <namespace>

# Check ingress controller logs
oc logs -n openshift-ingress deployment/router-default
```

### Issue: Operator stuck

```bash
# Check CSV status
oc get csv -n <namespace>

# Check operator pod
oc get pods -n <namespace> -l name=<operator-name>

# Delete and reinstall
oc delete subscription <sub-name> -n <namespace>
oc delete csv <csv-name> -n <namespace>
```

### Issue: Authentication failed

```bash
# Check OAuth pods
oc get pods -n openshift-authentication

# Check OAuth config
oc get oauth cluster -o yaml

# Check identity providers
oc get oauth cluster -o jsonpath='{.spec.identityProviders}'
```

## Related Skills

- **k8s:pods**: Generic pod debugging
- **k8s:logs**: Log analysis
- **k8s:health**: Platform health checks
