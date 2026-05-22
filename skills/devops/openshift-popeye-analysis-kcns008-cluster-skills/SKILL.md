---
name: openshift-popeye-analysis
description: |
  OpenShift-specific cluster health analysis and troubleshooting based on Popeye's issue detection patterns. Use this skill when:
  (1) Analyzing OpenShift cluster operators and platform health
  (2) Troubleshooting Security Context Constraints (SCC) violations
  (3) Diagnosing BuildConfig, ImageStream, and Route issues
  (4) Analyzing Projects, Quotas, and resource management
  (5) Validating OpenShift-specific security configurations
  (6) Monitoring OpenShift networking (Routes, Routers, OVNKubernetes)
  (7) OpenShift performance and reliability analysis
  (8) ARO/ROSA managed service troubleshooting
  (9) OpenShift CI/CD pipeline issues (Builds, Deployments)
  (10) Operator Lifecycle Manager and Operator issues
---

# OpenShift Cluster Health Analysis (Popeye-Style)

## OpenShift Platform Versions & Documentation (January 2026)

| Platform | Current Version | Support Status | Documentation |
|----------|-----------------|----------------|---------------|
| **OpenShift Container Platform** | 4.17.x | Current | https://docs.openshift.com/container-platform/4.17/ |
| **OCP EUS (Extended Update Support)** | 4.16.x | EUS | https://access.redhat.com/support/policy/updates/openshift |
| **ARO (Azure Red Hat OpenShift)** | 4.15-4.17 | GA | https://learn.microsoft.com/azure/openshift/ |
| **ROSA (Red Hat OpenShift on AWS)** | 4.14-4.17 | GA | https://docs.openshift.com/rosa/ |
| **ROSA HCP (Hosted Control Planes)** | 4.16-4.17 | GA | https://docs.openshift.com/rosa/rosa_hcp/ |
| **OKD** | 4.16.x | Community | https://www.okd.io/ |

### OpenShift 4.17 Key Features
- **OVN-Kubernetes**: Default CNI with eBPF datapath acceleration
- **MachineConfig Drift Detection**: Automatic detection of node configuration changes
- **Enhanced Web Terminal**: Built-in terminal with pre-installed tools
- **Pod Security Admission**: Full PSA enforcement with SCC integration
- **OpenShift AI**: ML/AI platform integration (optional operator)
- **GitOps 1.12+**: ArgoCD-based, ApplicationSet controller enhancements
- **Pipelines 1.15+**: Tekton-based, Chains for supply chain security

### CLI Installation

```bash
# OpenShift CLI (oc)
brew install openshift-cli
# OR download from mirror.openshift.com

# ROSA CLI
curl -LO https://mirror.openshift.com/pub/openshift-v4/clients/rosa/latest/rosa-linux.tar.gz
tar -xf rosa-linux.tar.gz && sudo mv rosa /usr/local/bin/
rosa login --token="${ROSA_TOKEN}"

# ARO (uses Azure CLI)
az extension add --name aro
az aro list -o table

# Verify CLI versions
oc version
rosa version
az aro --help
```

## OpenShift Detection and Command Convention

**IMPORTANT**: This skill automatically detects OpenShift environments and uses `oc` commands.
- **OpenShift clusters (OCP, ARO, ROSA)**: Use `oc` commands
- **Detection**: Check for OpenShift API groups and cluster operators
- **Fallback**: If `oc` not available, use `kubectl` with OpenShift-specific resources

## OpenShift Cluster Health Score Framework

Based on Popeye's scoring system adapted for OpenShift:

- **CRITICAL (BOOM)**: -50 points - Cluster operators degraded, SCC violations, router failures
- **WARNING (WARN)**: -20 points - Build failures, Route issues, Project quota exceeded
- **INFO (Informational)**: -5 points - Optimization opportunities, best practice suggestions

## OpenShift Comprehensive Health Assessment

### Cluster Operator Health Check

```bash
#!/bin/bash
# OpenShift Cluster Operator Health Assessment
echo "=== OPENSHIFT CLUSTER OPERATOR HEALTH ANALYSIS ==="

# 1. Check overall cluster operator status
echo "### Cluster Operator Overview ###"
oc get clusteroperators
echo ""

# Calculate operator health score
TOTAL_OPERATORS=$(oc get clusteroperators --no-headers | wc -l)
DEGRADED_OPERATORS=$(oc get clusteroperators --no-headers | grep -c "False.*True")
PROGRESSING_OPERATORS=$(oc get clusteroperators --no-headers | grep -c "True.*True")
AVAILABLE_OPERATORS=$(oc get clusteroperators --no-headers | grep -c "True.*False")

# 2. Detailed operator analysis
echo "### Critical Operator Analysis ###"
for operator in authentication console ingress network operator-lifecycle-manager storage; do
    echo "--- $operator ---"
    oc get clusteroperator $operator -o jsonpath='{.status.conditions[?(@.type=="Degraded")].status} {.status.conditions[?(@.type=="Progressing")].status} {.status.conditions[?(@.type=="Available")].status}'
    echo ""

    # Check for specific issues
    if oc get clusteroperator $operator -o jsonpath='{.status.conditions[?(@.type=="Degraded")].status}' | grep -q "True"; then
        echo "BOOM: $operator operator is DEGRADED!"
        echo "Reason: $(oc get clusteroperator $operator -o jsonpath='{.status.conditions[?(@.type=="Degraded")].reason}')"
        echo "Message: $(oc get clusteroperator $operator -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}')"
    fi
done

# 3. Check operator-specific issues
echo -e "\n### Operator-Specific Issue Detection ###"

# Authentication/OAuth issues
echo "--- Authentication/OAuth ---"
if oc get clusteroperator authentication -o jsonpath='{.status.conditions[?(@.type=="Degraded")].status}' | grep -q "True"; then
    echo "WARN: Authentication operator issues detected"
    echo "Check: OAuth server certificates, identity provider config"
fi

# Ingress/Router issues
echo "--- Ingress Controller ---"
if oc get clusteroperator ingress -o jsonpath='{.status.conditions[?(@.type=="Degraded")].status}' | grep -q "True"; then
    echo "BOOM: Ingress operator degraded - router issues!"
    echo "Check: Router pods, certificates, load balancer"
    oc get pods -n openshift-ingress -l ingresscontroller.operator.openshift.io/deployment-ingresscontroller=default
fi

# Network issues
echo "--- Network Operator ---"
if oc get clusteroperator network -o jsonpath='{.status.conditions[?(@.type=="Degraded")].status}' | grep -q "True"; then
    echo "BOOM: Network operator degraded - connectivity issues!"
    echo "Check: OVNKubernetes, SDN configuration"
    oc get pods -n openshift-ovn-kubernetes
fi

# 4. Console accessibility
echo -e "\n### Console Health ###"
if oc get clusteroperator console -o jsonpath='{.status.conditions[?(@.type=="Available")].status}' | grep -q "True"; then
    echo "✓ Console operator is available"
    CONSOLE_URL=$(oc get consoles.config.openshift.io cluster -o jsonpath='{.status.consoleURL}')
    echo "Console URL: $CONSOLE_URL"
else
    echo "WARN: Console operator not available"
fi

# 5. Calculate and display cluster health score
HEALTH_SCORE=$(( (AVAILABLE_OPERATORS * 100 / TOTAL_OPERATORS) - (DEGRADED_OPERATORS * 50) - (PROGRESSING_OPERATORS * 20) ))
echo -e "\n=== CLUSTER HEALTH SCORE: $HEALTH_SCORE/100 ==="
if [ $HEALTH_SCORE -lt 60 ]; then
    echo "BOOM: Cluster health is CRITICAL - immediate attention required!"
elif [ $HEALTH_SCORE -lt 80 ]; then
    echo "WARN: Cluster health needs attention - investigate issues"
else
    echo "INFO: Cluster health is acceptable"
fi
```

### Security Context Constraints (SCC) Analysis

```bash
#!/bin/bash
# OpenShift SCC Violation Analysis
echo "=== OPENSHIFT SCC ANALYSIS ==="

# 1. Check for SCC violations in recent events
echo "### SCC Violations Detection ###"
SCC_VIOLATIONS=$(oc get events -A --field-selector reason=FailedScheduling --no-headers | grep -c "unable to validate against any security context constraint")

if [ $SCC_VIOLATIONS -gt 0 ]; then
    echo "BOOM: $SCC_VIOLATIONS SCC violations detected!"
    echo "Recent SCC violations:"
    oc get events -A --field-selector reason=FailedScheduling --no-headers | grep "unable to validate against any security context constraint" | tail -5
else
    echo "✓ No recent SCC violations"
fi

# 2. Analyze pod security contexts
echo -e "\n### Pod Security Context Analysis ###"

# Check pods without proper security context
INSECURE_PODS=$(oc get pods -A -o json | jq -r '.items[] | select(.spec.securityContext.runAsNonRoot != true) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
echo "INFO: $INSECURE_PODS pods without runAsNonRoot=true"

# Check for privileged pods
PRIVILEGED_PODS=$(oc get pods -A -o json | jq -r '.items[] | select(.spec.containers[].securityContext.privileged == true) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $PRIVILEGED_PODS -gt 0 ]; then
    echo "BOOM: $PRIVILEGED_PODS privileged containers detected!"
    oc get pods -A -o json | jq -r '.items[] | select(.spec.containers[].securityContext.privileged == true) | "\(.metadata.namespace)/\(.metadata.name):\(.spec.containers[].name)"'
else
    echo "✓ No privileged containers found"
fi

# 3. SCC usage analysis
echo -e "\n### SCC Usage Patterns ###"
echo "Available SCCs:"
oc get scc

# Check which pods are using which SCCs
echo -e "\n### Pod to SCC Mapping ###"
for scc in restricted-v2 anyuid privileged; do
    echo "--- SCC: $scc ---"
    oc get pods -A -o custom-columns=POD:.metadata.name,NAMESPACE:.metadata.namespace,SCC:.metadata.annotations."openshift\.io/scc" --no-headers | grep "$scc" | head -3
done

# 4. Service account SCC analysis
echo -e "\n### Service Account SCC Access ###"
# Find service accounts with broad SCC access
for sa in $(oc get serviceaccounts -A --no-headers | awk '{print $1"/"$2}'); do
    namespace=$(echo $sa | cut -d/ -f1)
    sa_name=$(echo $sa | cut -d/ -f2)

    # Check for SCC access
    if oc adm policy who-can use scc anyuid | grep -q "$sa_name.*system:serviceaccount:$namespace"; then
        echo "WARN: Service account $sa has anyuid SCC access"
    fi
done

# 5. SCC recommendations
echo -e "\n### SCC Security Recommendations ###"
echo "Best Practices:"
echo "1. Use restricted-v2 SCC for most workloads"
echo "2. Create custom SCCs for specific requirements"
echo "3. Grant SCC access to specific service accounts, not groups"
echo "4. Regularly audit SCC assignments"
echo "5. Use securityContext in pod specs for explicit configuration"
```

### BuildConfig and ImageStream Analysis

```bash
#!/bin/bash
# OpenShift Build and Image Analysis
echo "=== OPENSHIFT BUILDCONFIG AND IMAGESTREAM ANALYSIS ==="

# 1. BuildConfig health check
echo "### BuildConfig Health Analysis ###"
TOTAL_BUILDCONFIGS=$(oc get buildconfigs -A --no-headers | wc -l)
echo "INFO: $TOTAL_BUILDCONFIGS BuildConfigs found"

# Check recent build failures
FAILED_BUILDS=$(oc get builds -A --field-selector status.phase=Failed --no-headers | wc -l)
if [ $FAILED_BUILDS -gt 0 ]; then
    echo "WARN: $FAILED_BUILDS failed builds detected"
    echo "Recent failed builds:"
    oc get builds -A --field-selector status.phase=Failed --sort-by='.metadata.creationTimestamp' | tail -3
else
    echo "✓ No recent build failures"
fi

# Analyze build strategies
echo -e "\n### Build Strategy Analysis ###"
echo "--- Build Strategies Distribution ---"
oc get buildconfigs -A -o custom-columns=STRATEGY:.spec.strategy.type,NAMESPACE:.metadata.namespace,NAME:.metadata.name | sort | uniq -c

# 2. ImageStream health
echo -e "\n### ImageStream Health Analysis ###"
TOTAL_IMAGESTREAMS=$(oc get imagestreams -A --no-headers | wc -l)
echo "INFO: $TOTAL_IMAGESTREAMS ImageStreams found"

# Check for ImageStreams without images
EMPTY_IMAGESTREAMS=$(oc get imagestreams -A -o json | jq -r '.items[] | select(.status.tags[]?.items? | length == 0) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $EMPTY_IMAGESTREAMS -gt 0 ]; then
    echo "WARN: $EMPTY_IMAGESTREAMS ImageStreams without images"
    echo "Empty ImageStreams:"
    oc get imagestreams -A -o json | jq -r '.items[] | select(.status.tags[]?.items? | length == 0) | "\(.metadata.namespace)/\(.metadata.name)"' | head -5
else
    echo "✓ All ImageStreams have images"
fi

# 3. Image import issues
echo -e "\n### Image Import Status ###"
# Check for recent image import failures
IMPORT_FAILURES=$(oc get events -A --field-selector reason=FailedImageImport --no-headers | wc -l)
if [ $IMPORT_FAILURES -gt 0 ]; then
    echo "WARN: $IMPORT_FAILURES image import failures"
    echo "Recent import failures:"
    oc get events -A --field-selector reason=FailedImageImport | tail -3
else
    echo "✓ No recent image import failures"
fi

# 4. Build performance analysis
echo -e "\n### Build Performance Analysis ###"
# Find long-running builds
LONG_BUILDS=$(oc get builds -A --no-headers | awk '$5 ~ /h/ && $5 > "1h" {print}' | wc -l)
if [ $LONG_BUILDS -gt 0 ]; then
    echo "WARN: $LONG_BUILDS builds running longer than 1 hour"
    echo "Long-running builds:"
    oc get builds -A --no-headers | awk '$5 ~ /h/ && $5 > "1h" {print}'
fi

# 5. Build resource usage
echo -e "\n### Build Resource Configuration ###"
# Check builds without resource limits
NO_RESOURCES=$(oc get buildconfigs -A -o json | jq -r '.items[] | select(.spec.resources.limits == null and .spec.resources.requests == null) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $NO_RESOURCES -gt 0 ]; then
    echo "WARN: $NO_RESOURCES BuildConfigs without resource limits"
else
    echo "✓ All BuildConfigs have resource configuration"
fi

# 6. Security analysis
echo -e "\n### Build Security Analysis ###"
# Check builds running as root
ROOT_BUILDS=$(oc get buildconfigs -A -o json | jq -r '.items[] | select(.spec.strategy.customStrategy?.securityContext?.runAsUser == 0) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $ROOT_BUILDS -gt 0 ]; then
    echo "WARN: $ROOT_BUILDS BuildConfigs configured to run as root"
fi

# Check for insecure build strategies
INSECURE_DOCKER_BUILDS=$(oc get buildconfigs -A -o json | jq -r '.items[] | select(.spec.strategy.dockerStrategy?.noCache == false) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
echo "INFO: $INSECURE_DOCKER_BUILDS Docker builds without noCache optimization"
```

### Route and Networking Analysis

```bash
#!/bin/bash
# OpenShift Route and Networking Analysis
echo "=== OPENSHIFT ROUTE AND NETWORKING ANALYSIS ==="

# 1. Route health check
echo "### Route Health Analysis ###"
TOTAL_ROUTES=$(oc get routes -A --no-headers | wc -l)
echo "INFO: $TOTAL_ROUTES routes found"

# Check routes without endpoints
UNHEALTHY_ROUTES=$(oc get routes -A -o json | jq -r '.items[] | select(.status.ingress == null or .status.ingress[].conditions[]?.status == "False") | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $UNHEALTHY_ROUTES -gt 0 ]; then
    echo "WARN: $UNHEALTHY_ROUTES routes without healthy endpoints"
    echo "Unhealthy routes:"
    oc get routes -A -o json | jq -r '.items[] | select(.status.ingress == null or .status.ingress[].conditions[]?.status == "False") | "\(.metadata.namespace)/\(.metadata.name): \(.status.ingress[].conditions[]?.message // "No endpoints")"'
else
    echo "✓ All routes have healthy endpoints"
fi

# 2. TLS certificate analysis
echo -e "\n### TLS Certificate Analysis ###"
# Check routes with TLS configuration
TLS_ROUTES=$(oc get routes -A -o json | jq -r '.items[] | select(.spec.tls != null) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
echo "INFO: $TLS_ROUTES routes with TLS configuration"

# Check for expired certificates (requires cert-utils)
echo "WARN: Certificate expiration analysis requires external cert checking tools"
echo "Recommended: Implement automated certificate monitoring"

# 3. Router health
echo -e "\n### Router Health Analysis ###"
# Check router pods
ROUTER_PODS=$(oc get pods -n openshift-ingress -l ingresscontroller.operator.openshift.io/deployment-ingresscontroller=default --no-headers | wc -l)
echo "INFO: $ROUTER_PODS router pods running"

READY_ROUTERS=$(oc get pods -n openshift-ingress -l ingresscontroller.operator.openshift.io/deployment-ingresscontroller=default --field-selector=status.phase=Running --no-headers | wc -l)
if [ $READY_ROUTERS -lt $ROUTER_PODS ]; then
    echo "WARN: Not all router pods are ready"
    oc get pods -n openshift-ingress -l ingresscontroller.operator.openshift.io/deployment-ingresscontroller=default
else
    echo "✓ All router pods are healthy"
fi

# 4. NetworkPolicy analysis
echo -e "\n### NetworkPolicy Analysis ###"
TOTAL_NETWORKPOLICIES=$(oc get networkpolicy -A --no-headers | wc -l)
echo "INFO: $TOTAL_NETWORKPOLICIES NetworkPolicies found"

# Find namespaces without NetworkPolicies
NAMESPACES_WITHOUT_NP=$(oc get namespaces -A --no-headers | awk '{print $1}' | while read ns; do
    if [ $(oc get networkpolicy -n $ns --no-headers 2>/dev/null | wc -l) -eq 0 ]; then
        echo $ns
    fi
done | wc -l)

if [ $NAMESPACES_WITHOUT_NP -gt 0 ]; then
    echo "WARN: $NAMESPACES_WITHOUT_NP namespaces without NetworkPolicies"
    echo "Namespaces without NetworkPolicies:"
    oc get namespaces -A --no-headers | awk '{print $1}' | while read ns; do
        if [ $(oc get networkpolicy -n $ns --no-headers 2>/dev/null | wc -l) -eq 0 ]; then
            echo $ns
        fi
    done | head -5
else
    echo "✓ All namespaces have NetworkPolicies"
fi

# 5. OVNKubernetes network analysis (default in OCP 4.12+, eBPF in 4.17+)
echo -e "\n### OVNKubernetes Network Analysis (OCP 4.17+ eBPF) ###"
NETWORK_TYPE=$(oc get network.config.openshift.io cluster -o jsonpath='{.status.networkType}' 2>/dev/null)
echo "INFO: Network type: $NETWORK_TYPE"

if [ "$NETWORK_TYPE" == "OVNKubernetes" ]; then
    echo "INFO: OVNKubernetes CNI detected (default for OCP 4.12+)"
    
    # Check OVNKubernetes pods
    OVN_PODS=$(oc get pods -n openshift-ovn-kubernetes --no-headers 2>/dev/null | wc -l)
    echo "INFO: $OVN_PODS OVNKubernetes pods running"

    OVN_READY=$(oc get pods -n openshift-ovn-kubernetes --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l)
    if [ $OVN_READY -lt $OVN_PODS ]; then
        echo "WARN: Some OVNKubernetes pods not ready"
        oc get pods -n openshift-ovn-kubernetes | grep -v Running
    else
        echo "✓ OVNKubernetes pods healthy"
    fi
    
    # Check for eBPF acceleration (4.17+)
    if oc get network.operator.openshift.io cluster -o jsonpath='{.spec.defaultNetwork.ovnKubernetesConfig.egressIPConfig}' 2>/dev/null; then
        echo "INFO: OVN-Kubernetes with eBPF datapath support available"
    fi
    
    # Check EgressIP configuration
    EGRESS_IPS=$(oc get egressip --no-headers 2>/dev/null | wc -l)
    if [ $EGRESS_IPS -gt 0 ]; then
        echo "INFO: $EGRESS_IPS EgressIP resources configured"
    fi
    
    # Check for NetworkPolicy enforcement
    echo "--- NetworkPolicy Status ---"
    NETWORK_POLICIES=$(oc get networkpolicy -A --no-headers 2>/dev/null | wc -l)
    echo "INFO: $NETWORK_POLICIES NetworkPolicies configured cluster-wide"
elif [ "$NETWORK_TYPE" == "OpenShiftSDN" ]; then
    echo "WARN: OpenShiftSDN detected - consider migrating to OVNKubernetes for OCP 4.17+ features"
    echo "Migration guide: https://docs.openshift.com/container-platform/4.17/networking/ovn_kubernetes_network_provider/migrate-from-openshift-sdn.html"
fi

# 6. Egress networking analysis
echo -e "\n### Egress Networking Analysis ###"
# Check for EgressNetworkPolicies
EGRESS_POLICIES=$(oc get egressnetworkpolicy -A --no-headers 2>/dev/null | wc -l)
echo "INFO: $EGRESS_POLICIES EgressNetworkPolicies found"

# Check for EgressFirewalls (if available)
if oc get crd egressfirewalls.k8s.ovn.org &>/dev/null; then
    EGRESS_FIREWALLS=$(oc get egressfirewall -A --no-headers 2>/dev/null | wc -l)
    echo "INFO: $EGRESS_FIREWALLS EgressFirewalls found"
fi
```

### Project and Resource Quota Analysis

```bash
#!/bin/bash
# OpenShift Project and Resource Analysis
echo "=== OPENSHIFT PROJECT AND RESOURCE QUOTA ANALYSIS ==="

# 1. Project health
echo "### Project Health Analysis ###"
TOTAL_PROJECTS=$(oc get projects -A --no-headers | wc -l)
ACTIVE_PROJECTS=$(oc get projects -A --field-selector=status.phase=Active --no-headers | wc -l)
TERMINATING_PROJECTS=$(oc get projects -A --field-selector=status.phase=Terminating --no-headers | wc -l)

echo "INFO: $TOTAL_PROJECTS total projects"
echo "INFO: $ACTIVE_PROJECTS active projects"

if [ $TERMINATING_PROJECTS -gt 0 ]; then
    echo "WARN: $TERMINATING_PROJECTS projects stuck in terminating"
    echo "Terminating projects:"
    oc get projects -A --field-selector=status.phase=Terminating
else
    echo "✓ No projects stuck in terminating"
fi

# 2. Resource quota analysis
echo -e "\n### Resource Quota Analysis ###"
PROJECTS_WITH_QUOTA=$(oc get resourcequota -A --no-headers | awk '{print $1}' | sort -u | wc -l)
echo "INFO: $PROJECTS_WITH_QUOTA projects with resource quotas"

# Check quota violations
QUOTA_VIOLATIONS=$(oc get events -A --field-selector reason=ExceededQuota --no-headers | wc -l)
if [ $QUOTA_VIOLATIONS -gt 0 ]; then
    echo "WARN: $QUOTA_VIOLATIONS quota violations detected"
    echo "Recent quota violations:"
    oc get events -A --field-selector reason=ExceededQuota | tail -3
else
    echo "✓ No recent quota violations"
fi

# Analyze quota utilization
echo -e "\n### Quota Utilization Analysis ###"
for project in $(oc get projects -A --field-selector=status.phase=Active --no-headers | awk '{print $1}'); do
    quota_count=$(oc get resourcequota -n $project --no-headers 2>/dev/null | wc -l)
    if [ $quota_count -gt 0 ]; then
        echo "--- Project: $project ---"
        oc get resourcequota -n $project -o custom-columns=NAME:.metadata.name,HARD:.status.hard,USED:.status.used
    fi
done | head -20

# 3. LimitRange analysis
echo -e "\n### LimitRange Analysis ###"
PROJECTS_WITH_LIMITRANGE=$(oc get limitrange -A --no-headers | awk '{print $1}' | sort -u | wc -l)
echo "INFO: $PROJECTS_WITH_LIMITRANGE projects with LimitRanges"

# Projects without resource governance
UNGOVERNED_PROJECTS=$((ACTIVE_PROJECTS - PROJECTS_WITH_QUOTA))
if [ $UNGOVERNED_PROJECTS -gt 0 ]; then
    echo "WARN: $UNGOVERNED_PROJECTS projects without resource quotas"
    echo "Consider implementing resource governance for all projects"
fi

# 4. Resource requests/limits analysis
echo -e "\n### Resource Configuration Analysis ###"
# Pods without resource limits
PODS_WITHOUT_LIMITS=$(oc get pods -A -o json | jq -r '.items[] | select(.spec.containers[].resources.limits == null) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $PODS_WITHOUT_LIMITS -gt 0 ]; then
    echo "WARN: $PODS_WITHOUT_LIMITS pods without resource limits"
else
    echo "✓ All pods have resource limits"
fi

# Pods without resource requests
PODS_WITHOUT_REQUESTS=$(oc get pods -A -o json | jq -r '.items[] | select(.spec.containers[].resources.requests == null) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $PODS_WITHOUT_REQUESTS -gt 0 ]; then
    echo "WARN: $PODS_WITHOUT_REQUESTS pods without resource requests"
else
    echo "✓ All pods have resource requests"
fi

# 5. Resource utilization analysis
echo -e "\n### Resource Utilization Analysis ###"
# Node utilization
echo "--- Node Resource Utilization ---"
if command -v oc adm top &>/dev/null; then
    oc adm top nodes
else
    echo "WARN: Metrics server not available for utilization analysis"
fi

# Project-level utilization (if metrics available)
echo -e "\n--- Project Resource Usage ---"
if oc adm top pods -A &>/dev/null; then
    for project in $(oc get projects -A --field-selector=status.phase=Active --no-headers | awk '{print $1}' | head -5); do
        echo "Project: $project"
        oc adm top pods -n $project 2>/dev/null | awk 'NR>1 {cpu+=$2; mem+=$3} END {print "  CPU: " cpu "m, Memory: " mem}'
    done
fi
```

### OpenShift Platform-Specific Issues

```bash
#!/bin/bash
# OpenShift Platform-Specific Analysis
echo "=== OPENSHIFT PLATFORM-SPECIFIC ANALYSIS ==="

### OpenShift Platform Detection

```bash
#!/bin/bash
# OpenShift Platform-Specific Analysis
echo "=== OPENSHIFT PLATFORM-SPECIFIC ANALYSIS ==="

# 1. Detect OpenShift variant and version
echo "### OpenShift Platform Detection ###"
if oc get clusterversion version -o jsonpath='{.status.desired.version}' 2>/dev/null; then
    OCP_VERSION=$(oc get clusterversion version -o jsonpath='{.status.desired.version}')
    echo "INFO: OpenShift Container Platform version: $OCP_VERSION"
    
    # Parse major.minor version
    OCP_MAJOR=$(echo $OCP_VERSION | cut -d. -f1)
    OCP_MINOR=$(echo $OCP_VERSION | cut -d. -f2)
    echo "INFO: Major: $OCP_MAJOR, Minor: $OCP_MINOR"
    
    # Check for 4.17+ features
    if [ "$OCP_MINOR" -ge 17 ]; then
        echo "INFO: OCP 4.17+ detected - OVN-Kubernetes eBPF, Pod Security Admission GA"
    fi
else
    echo "WARN: Unable to determine OpenShift version"
fi

# Check for managed service platforms
if oc get infrastructure cluster -o jsonpath='{.status.platformStatus.type}' 2>/dev/null | grep -qi "azure"; then
    echo "INFO: Azure Red Hat OpenShift (ARO) detected"
    PLATFORM="ARO"
    
    # ARO-specific checks
    echo "--- ARO Resource Group and Location ---"
    oc get infrastructure cluster -o jsonpath='{.status.platformStatus.azure.resourceGroupName}'
    
elif oc get infrastructure cluster -o jsonpath='{.status.platformStatus.type}' 2>/dev/null | grep -qi "aws"; then
    # Check for ROSA markers
    if oc get configmap -n kube-system aws-auth &>/dev/null && rosa describe cluster 2>/dev/null; then
        echo "INFO: Red Hat OpenShift Service on AWS (ROSA) detected"
        PLATFORM="ROSA"
        
        # Check for HCP (Hosted Control Planes)
        if rosa describe cluster 2>/dev/null | grep -q "Hosted Control Plane"; then
            echo "INFO: ROSA with Hosted Control Planes (HCP) - faster provisioning, reduced cost"
            PLATFORM="ROSA-HCP"
        fi
    else
        echo "INFO: Self-managed OpenShift on AWS detected"
        PLATFORM="OCP-AWS"
    fi
    
elif oc get infrastructure cluster -o jsonpath='{.status.platformStatus.type}' 2>/dev/null | grep -qi "gcp"; then
    echo "INFO: OpenShift on Google Cloud Platform detected"
    PLATFORM="OCP-GCP"
    
elif oc get infrastructure cluster -o jsonpath='{.status.platformStatus.type}' 2>/dev/null | grep -qi "vsphere"; then
    echo "INFO: OpenShift on VMware vSphere detected"
    PLATFORM="OCP-vSphere"
    
elif oc get infrastructure cluster -o jsonpath='{.status.platformStatus.type}' 2>/dev/null | grep -qi "baremetal"; then
    echo "INFO: OpenShift on Bare Metal detected"
    PLATFORM="OCP-BareMetal"
    
else
    echo "INFO: Self-managed OpenShift Container Platform detected"
    PLATFORM="OCP"
fi

echo "Platform: $PLATFORM"
```

# 2. Platform-specific checks
case $PLATFORM in
    "ARO")
        echo -e "\n### ARO-Specific Checks (Azure Red Hat OpenShift) ###"
        echo "Checking Azure-specific configurations..."
        
        # Check Azure resource limits
        echo "INFO: Monitor Azure subscription quotas and limits"
        echo "INFO: Check Azure resource group permissions"
        
        # ARO networking
        echo "--- ARO Networking ---"
        oc get network.config.openshift.io cluster -o jsonpath='{.status.networkType}'
        
        # ARO upgrade
        echo "--- ARO Upgrade Status ---"
        echo "Use: az aro update --resource-group \${RG} --name \${CLUSTER}"
        echo "Check available versions: az aro get-versions --location \${LOCATION}"
        ;;
        
    "ROSA"|"ROSA-HCP")
        echo -e "\n### ROSA-Specific Checks (Red Hat OpenShift on AWS) ###"
        echo "Checking AWS-specific configurations..."
        
        # Check AWS STS configuration
        echo "INFO: Verify AWS IAM roles and STS configuration"
        rosa describe cluster 2>/dev/null | grep -E "AWS Account|Region|STS"
        
        # ROSA upgrade
        echo "--- ROSA Upgrade Status ---"
        rosa list upgrades --cluster \${CLUSTER} 2>/dev/null || echo "Run: rosa list upgrades --cluster \${CLUSTER}"
        
        # Check machine pools
        echo "--- ROSA Machine Pools ---"
        rosa list machinepools --cluster \${CLUSTER} 2>/dev/null || echo "Run: rosa list machinepools --cluster \${CLUSTER}"
        
        if [ "$PLATFORM" == "ROSA-HCP" ]; then
            echo "--- ROSA HCP Specific ---"
            echo "INFO: Hosted Control Planes managed by AWS"
            echo "INFO: Control plane nodes not visible, managed service"
        fi
        ;;
        
    "OCP"*)
        echo -e "\n### Self-Managed OCP Checks ###"
        echo "Checking infrastructure components..."
        # Check infrastructure nodes
        INFRA_NODES=$(oc get nodes --no-headers -l node-role.kubernetes.io/infra | wc -l)
        echo "INFO: $INFRA_NODES infrastructure nodes found"

        # Check bootstrap node removal
        if oc get nodes --no-headers | grep -q bootstrap; then
            echo "WARN: Bootstrap node still present - should be removed post-install"
        else
            echo "✓ Bootstrap node properly removed"
        fi
        ;;
esac

# 3. Cluster upgrade status
echo -e "\n### Cluster Upgrade Analysis ###"
if [ "$PLATFORM" != "OCP" ]; then
    echo "INFO: Managed service - check with cloud provider for upgrade status"
else
    # Check for update availability
    oc adm upgrade
fi

# 4. Certificate rotation status
echo -e "\n### Certificate Analysis ###"
# Check certificate signing requests
PENDING_CSRS=$(oc get csr --no-headers | grep -c "Pending")
if [ $PENDING_CSRS -gt 0 ]; then
    echo "WARN: $PENDING_CSRS pending certificate signing requests"
    oc get csr --no-headers | grep "Pending"
else
    echo "✓ No pending certificate requests"
fi

# Check kubelet serving certificates
echo "INFO: Checking node certificate rotation..."
oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.conditions[?(@.type=="KubeletReady")].lastTransitionTime}{"\n"}{end}'

# 5. Monitoring and observability
echo -e "\n### Monitoring Stack Analysis ###"
# Check Prometheus
PROMETHEUS_PODS=$(oc get pods -n openshift-monitoring -l app.kubernetes.io/name=prometheus --no-headers | wc -l)
echo "INFO: $PROMETHEUS_PODS Prometheus pods running"

# Check AlertManager
ALERTMANAGER_PODS=$(oc get pods -n openshift-monitoring -l app.kubernetes.io/name=alertmanager --no-headers | wc -l)
echo "INFO: $ALERTMANAGER_PODS AlertManager pods running"

# Check Thanos Ruler (if available)
if oc get pods -n openshift-monitoring -l app.kubernetes.io/name=thanos-ruler &>/dev/null; then
    THANOS_PODS=$(oc get pods -n openshift-monitoring -l app.kubernetes.io/name=thanos-ruler --no-headers | wc -l)
    echo "INFO: $THANOS_PODS Thanos Ruler pods running"
fi

# Check for critical alerts
echo -e "\n### Critical Alerts Analysis ###"
if oc -n openshift-monitoring get prometheusrules --no-headers &>/dev/null; then
    echo "INFO: Alerting rules configured"
    echo "Check critical alerts via Console or Prometheus API"
else
    echo "WARN: Unable to access alerting rules"
fi

# 6. Storage operator health
echo -e "\n### Storage Operator Analysis ###"
# Check storage operator status
if oc get clusteroperator storage &>/dev/null; then
    STORAGE_STATUS=$(oc get clusteroperator storage -o jsonpath='{.status.conditions[?(@.type=="Degraded")].status}')
    if [ "$STORAGE_STATUS" == "True" ]; then
        echo "BOOM: Storage operator is degraded!"
        echo "Check storage classes and CSI drivers"
    else
        echo "✓ Storage operator is healthy"
    fi

    # Check storage classes
    STORAGE_CLASSES=$(oc get storageclass --no-headers | wc -l)
    echo "INFO: $STORAGE_CLASSES storage classes available"
else
    echo "WARN: Storage operator status not available"
fi
```

### OpenShift Operator Lifecycle Manager (OLM) Analysis

```bash
#!/bin/bash
# OpenShift Operator Lifecycle Manager Analysis
echo "=== OPENSHIFT OPERATOR LIFECYCLE MANAGER ANALYSIS ==="

# 1. OLM health check
echo "### OLM Component Health ###"
OLM_NAMESPACES="openshift-operator-lifecycle-manager openshift-operators openshift-marketplace"

for ns in $OLM_NAMESPACES; do
    echo "--- Namespace: $ns ---"
    TOTAL_PODS=$(oc get pods -n $ns --no-headers 2>/dev/null | wc -l)
    READY_PODS=$(oc get pods -n $ns --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l)

    if [ $TOTAL_PODS -gt 0 ]; then
        echo "Pods: $READY_PODS/$TOTAL_PODS ready"
        if [ $READY_PODS -lt $TOTAL_PODS ]; then
            echo "WARN: Some OLM pods not ready in $ns"
            oc get pods -n $s | grep -v "Running\|Completed"
        else
            echo "✓ All pods healthy in $ns"
        fi
    else
        echo "INFO: No pods in $ns"
    fi
done

# 2. Operator installation analysis
echo -e "\n### Installed Operators Analysis ###"
if oc get operators.coreos.com &>/dev/null; then
    TOTAL_OPERATORS=$(oc get operators.coreos.com --all-namespaces --no-headers | wc -l)
    echo "INFO: $TOTAL_OPERATORS operators installed via OLM"

    # Check for failed operators
    FAILED_OPERATORS=$(oc get operators.coreos.com --all-namespaces -o json | jq -r '.items[] | select(.status.phase == "Failed") | "\(.metadata.namespace)/\(.metadata.name): \(.status.message)"' | wc -l)
    if [ $FAILED_OPERATORS -gt 0 ]; then
        echo "WARN: $FAILED_OPERATORS operators in failed state"
        oc get operators.coreos.com --all-namespaces -o json | jq -r '.items[] | select(.status.phase == "Failed") | "\(.metadata.namespace)/\(.metadata.name): \(.status.message)"'
    else
        echo "✓ All operators healthy"
    fi

    # Check for operators not ready
    NOT_READY=$(oc get operators.coreos.com --all-namespaces -o json | jq -r '.items[] | select(.status.phase != "Succeeded") | "\(.metadata.namespace)/\(.metadata.name): \(.status.phase)"' | wc -l)
    if [ $NOT_READY -gt $FAILED_OPERATORS ]; then
        echo "INFO: $((NOT_READY - FAILED_OPERATORS)) operators still installing/upgrading"
    fi
else
    echo "WARN: OLM API not available"
fi

# 3. Operator catalog analysis
echo -e "\n### Operator Catalog Analysis ###"
# Check catalog sources
CATALOG_SOURCES=$(oc get catalogsource -n openshift-marketplace --no-headers 2>/dev/null | wc -l)
if [ $CATALOG_SOURCES -gt 0 ]; then
    echo "INFO: $CATALOG_SOURCES catalog sources configured"

    # Check catalog source health
    UNHEALTHY_CATALOGS=$(oc get catalogsource -n openshift-marketplace -o json | jq -r '.items[] | select(.status.connectionState.lastObservedState != "READY") | "\(.metadata.name): \(.status.connectionState.lastObservedState)"' | wc -l)
    if [ $UNHEALTHY_CATALOGS -gt 0 ]; then
        echo "WARN: $UNHEALTHY_CATALOGS catalog sources not ready"
        oc get catalogsource -n openshift-marketplace -o json | jq -r '.items[] | select(.status.connectionState.lastObservedState != "READY") | "\(.metadata.name): \(.status.connectionState.lastObservedState)"'
    else
        echo "✓ All catalog sources healthy"
    fi
else
    echo "INFO: No catalog sources found"
fi

# 4. Subscription analysis
echo -e "\n### Operator Subscriptions Analysis ###"
if oc get subscription -A &>/dev/null; then
    TOTAL_SUBSCRIPTIONS=$(oc get subscription -A --no-headers | wc -l)
    echo "INFO: $TOTAL_SUBSCRIPTIONS operator subscriptions"

    # Check subscriptions with upgrade issues
    FAILED_UPGRADES=$(oc get subscription -A -o json | jq -r '.items[] | select(.status.state == "UpgradeFailed") | "\(.metadata.namespace)/\(.metadata.name): \(.status.reason)"' | wc -l)
    if [ $FAILED_UPGRADES -gt 0 ]; then
        echo "WARN: $FAILED_UPGRADES subscriptions with failed upgrades"
        oc get subscription -A -o json | jq -r '.items[] | select(.status.state == "UpgradeFailed") | "\(.metadata.namespace)/\(.metadata.name): \(.status.reason)"'
    fi

    # Check manual upgrade required
    MANUAL_UPGRADE=$(oc get subscription -A -o json | jq -r '.items[] | select(.status.state == "UpgradePending") | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
    if [ $MANUAL_UPGRADE -gt 0 ]; then
        echo "INFO: $MANUAL_UPGRADE subscriptions pending manual approval"
    fi
else
    echo "INFO: No operator subscriptions found"
fi

# 5. Operator resource analysis
echo -e "\n### Operator Resource Usage Analysis ###"
# Calculate resources used by operators
OPERATOR_CPU_REQUESTS=$(oc get pods -A -l app.kubernetes.io/part-of=operator-lifecycle-manager -o jsonpath='{range .items[*]}{.spec.containers[*].resources.requests.cpu}{"\n"}{end}' | grep -v "null" | sed 's/m//' | awk '{sum+=$1} END {print sum}')
OPERATOR_MEMORY_REQUESTS=$(oc get pods -A -l app.kubernetes.io/part-of=operator-lifecycle-manager -o jsonpath='{range .items[*]}{.spec.containers[*].resources.requests.memory}{"\n"}{end}' | grep -v "null" | sed 's/Mi//' | awk '{sum+=$1} END {print sum}')

echo "INFO: OLM components request ${OPERATOR_CPU_REQUESTS}m CPU and ${OPERATOR_MEMORY_REQUESTS}Mi memory"

# Check operator-specific resource usage
echo -e "\n--- Operator-Specific Resource Usage ---"
if oc get pods -A --no-headers | grep -q "operator"; then
    echo "Top 5 operators by CPU usage (if metrics available):"
    if oc adm top pods -A 2>/dev/null | grep operator &>/dev/null; then
        oc adm top pods -A | grep operator | sort -k3 -nr | head -5
    else
        echo "Metrics not available for detailed analysis"
    fi
fi

# 6. Operator best practices analysis
echo -e "\n### Operator Best Practices Analysis ###"
# Check for operators without resource limits
OPERATORS_WITHOUT_LIMITS=$(oc get pods -A -l app.kubernetes.io/part-of=operator -o json | jq -r '.items[] | select(.spec.containers[].resources.limits == null) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $OPERATORS_WITHOUT_LIMITS -gt 0 ]; then
    echo "WARN: $OPERATORS_WITHOUT_LIMITS operator pods without resource limits"
else
    echo "✓ All operator pods have resource limits"
fi

# Check for operators using default service accounts
DEFAULT_SA_OPERATORS=$(oc get pods -A -l app.kubernetes.io/part-of=operator -o json | jq -r '.items[] | select(.spec.serviceAccountName == "default") | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $DEFAULT_SA_OPERATORS -gt 0 ]; then
    echo "WARN: $DEFAULT_SA_OPERATORS operators using default service accounts"
else
    echo "✓ Operators using dedicated service accounts"
fi
```

## OpenShift Health Score Calculation

```bash
#!/bin/bash
# OpenShift Cluster Health Score Calculation (Popeye-Style)
echo "=== OPENSHIFT CLUSTER HEALTH SCORE ==="

# Initialize score at 100
SCORE=100

# 1. Critical Issues (-50 points each)
echo "### Critical Issues Assessment ###"

# Cluster operators degraded
DEGRADED_OPERATORS=$(oc get clusteroperators --no-headers | grep -c "False.*True")
if [ $DEGRADED_OPERATORS -gt 0 ]; then
    echo "BOOM: $DEGRADED_OPERATORS cluster operators degraded (-$((DEGRADED_OPERATORS * 50)) points)"
    SCORE=$((SCORE - (DEGRADED_OPERATORS * 50)))
fi

# SCC violations
SCC_VIOLATIONS=$(oc get events -A --field-selector reason=FailedScheduling --no-headers | grep -c "unable to validate against any security context constraint")
if [ $SCC_VIOLATIONS -gt 0 ]; then
    echo "BOOM: $SCC_VIOLATIONS SCC violations (-$((SCC_VIOLATIONS * 50)) points)"
    SCORE=$((SCORE - (SCC_VIOLATIONS * 50)))
fi

# Router failures
UNHEALTHY_ROUTERS=$(oc get pods -n openshift-ingress --field-selector=status.phase!=Running --no-headers | wc -l)
if [ $UNHEALTHY_ROUTERS -gt 0 ]; then
    echo "BOOM: $UNHEALTHY_ROUTERS unhealthy router pods (-$((UNHEALTHY_ROUTERS * 50)) points)"
    SCORE=$((SCORE - (UNHEALTHY_ROUTERS * 50)))
fi

# 2. Warning Issues (-20 points each)
echo -e "\n### Warning Issues Assessment ###"

# Build failures
FAILED_BUILDS=$(oc get builds -A --field-selector status.phase=Failed --no-headers | wc -l)
if [ $FAILED_BUILDS -gt 2 ]; then
    echo "WARN: $FAILED_BUILDS failed builds (-20 points)"
    SCORE=$((SCORE - 20))
fi

# Route issues
ROUTE_ISSUES=$(oc get routes -A -o json | jq -r '.items[] | select(.status.ingress == null) | "\(.metadata.name)"' | wc -l)
if [ $ROUTE_ISSUES -gt 0 ]; then
    echo "WARN: $ROUTE_ISSUES routes without endpoints (-20 points)"
    SCORE=$((SCORE - 20))
fi

# Quota violations
QUOTA_VIOLATIONS=$(oc get events -A --field-selector reason=ExceededQuota --no-headers | wc -l)
if [ $QUOTA_VIOLATIONS -gt 0 ]; then
    echo "WARN: Resource quota violations detected (-20 points)"
    SCORE=$((SCORE - 20))
fi

# 3. Info Issues (-5 points each)
echo -e "\n### Information Issues Assessment ###"

# Pods without resource limits
PODS_WITHOUT_LIMITS=$(oc get pods -A -o json | jq -r '.items[] | select(.spec.containers[].resources.limits == null) | "\(.metadata.name)"' | wc -l)
if [ $PODS_WITHOUT_LIMITS -gt 5 ]; then
    echo "INFO: Many pods without resource limits (-5 points)"
    SCORE=$((SCORE - 5))
fi

# Projects without NetworkPolicies
PROJECTS_WITHOUT_NP=$(oc get namespaces -A --field-selector=status.phase=Active --no-headers | awk '{print $1}' | while read ns; do
    if [ $(oc get networkpolicy -n $ns --no-headers 2>/dev/null | wc -l) -eq 0 ]; then
        echo $ns
    fi
done | wc -l)
if [ $PROJECTS_WITHOUT_NP -gt 2 ]; then
    echo "INFO: Multiple namespaces without NetworkPolicies (-5 points)"
    SCORE=$((SCORE - 5))
fi

# 4. Calculate final score
if [ $SCORE -lt 0 ]; then
    SCORE=0
fi

echo -e "\n=== OPENSHIFT CLUSTER HEALTH SCORE: $SCORE/100 ==="

if [ $SCORE -ge 90 ]; then
    echo "🟢 EXCELLENT: Cluster is very healthy"
elif [ $SCORE -ge 80 ]; then
    echo "🟡 GOOD: Cluster is healthy with minor issues"
elif [ $SCORE -ge 60 ]; then
    echo "🟠 FAIR: Cluster has significant issues that need attention"
elif [ $SCORE -ge 40 ]; then
    echo "🔴 POOR: Cluster has critical issues requiring immediate attention"
else
    echo "💀 CRITICAL: Cluster health is critical - emergency response required"
fi

# 5. Recommendations based on score
echo -e "\n### Recommendations ###"

if [ $SCORE -lt 60 ]; then
    echo "URGENT ACTIONS REQUIRED:"
    echo "1. Address all critical cluster operator issues"
    echo "2. Fix SCC violations to restore pod scheduling"
    echo "3. Resolve router/ingress connectivity problems"
    echo "4. Check storage and network operator health"
fi

if [ $SCORE -lt 80 ]; then
    echo "RECOMMENDED ACTIONS:"
    echo "1. Investigate and fix build configuration issues"
    echo "2. Resolve route connectivity problems"
    echo "3. Review and adjust resource quotas"
    echo "4. Implement resource limits for all pods"
fi

if [ $SCORE -ge 80 ]; then
    echo "OPTIMIZATION OPPORTUNITIES:"
    echo "1. Implement NetworkPolicies for all namespaces"
    echo "2. Optimize resource requests and limits"
    echo "3. Enable advanced monitoring and alerting"
    echo "4. Consider cluster upgrade for latest features"
fi
```