---
name: eks-networking
description: EKS networking configuration including VPC CNI, load balancers, and network policies. Use when setting up cluster networking, configuring ingress/load balancing, implementing network security, troubleshooting connectivity, or optimizing network costs.
---

# EKS Networking

Comprehensive guide for configuring Amazon EKS networking including VPC CNI plugin, load balancers, network policies, and security.

## Overview

EKS networking involves several key components working together:

1. **VPC CNI Plugin** - Assigns real VPC IP addresses to pods
2. **Load Balancers** - ALB for Layer 7, NLB for Layer 4 traffic
3. **Network Policies** - Control pod-to-pod and pod-to-external traffic
4. **Security Groups for Pods** - AWS-level network security
5. **DNS** - CoreDNS for in-cluster, ExternalDNS for external records
6. **Service Discovery** - AWS Cloud Map for multi-cluster

## Quick Start

### 1. Enable VPC CNI with Prefix Mode

```bash
# Update VPC CNI addon with prefix delegation
aws eks update-addon \
  --cluster-name my-cluster \
  --addon-name vpc-cni \
  --addon-version v1.19.2-eksbuild.1 \
  --configuration-values '{
    "env": {
      "ENABLE_PREFIX_DELEGATION": "true",
      "WARM_PREFIX_TARGET": "1"
    }
  }'

# Verify configuration
kubectl get daemonset -n kube-system aws-node -o yaml | grep ENABLE_PREFIX_DELEGATION
```

### 2. Install AWS Load Balancer Controller

```bash
# Create IAM policy
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.11.0/docs/install/iam_policy.json

aws iam create-policy \
  --policy-name AWSLoadBalancerControllerIAMPolicy \
  --policy-document file://iam_policy.json

# Create IRSA
eksctl create iamserviceaccount \
  --cluster=my-cluster \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --attach-policy-arn=arn:aws:iam::ACCOUNT_ID:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve

# Install via Helm
helm repo add eks https://aws.github.io/eks-charts
helm repo update

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=my-cluster \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller
```

### 3. Create ALB Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/group.name: shared-alb
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}, {"HTTPS": 443}]'
    alb.ingress.kubernetes.io/ssl-redirect: '443'
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:region:account:certificate/xxx
spec:
  ingressClassName: alb
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

### 4. Enable Network Policies

```bash
# VPC CNI v1.14+ supports network policies natively
kubectl set env daemonset -n kube-system aws-node ENABLE_NETWORK_POLICY=true

# Apply a network policy
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
EOF
```

## Workflow: Complete Networking Setup

### Phase 1: VPC and Subnet Planning

**1.1 Calculate IP Requirements**

```bash
# Formula: IPs per node = (max-pods × 2) + ENIs + buffer
# Example for m5.large:
# - Max pods: 29
# - ENIs: 3
# - IPs needed: (29 × 2) + 3 + 5 = 66 IPs per node

# For a 10-node cluster: 660 IPs minimum
# Recommended subnet: /24 (254 IPs) or /23 (510 IPs)
```

**1.2 Tag Subnets for EKS**

```bash
# Public subnets (for internet-facing ALB/NLB)
aws ec2 create-tags \
  --resources subnet-xxx \
  --tags Key=kubernetes.io/role/elb,Value=1

# Private subnets (for internal ALB/NLB and worker nodes)
aws ec2 create-tags \
  --resources subnet-yyy \
  --tags Key=kubernetes.io/role/internal-elb,Value=1

# Cluster-specific tags (required)
aws ec2 create-tags \
  --resources subnet-xxx subnet-yyy \
  --tags Key=kubernetes.io/cluster/my-cluster,Value=shared
```

### Phase 2: Configure VPC CNI

**2.1 Choose Configuration Mode**

```bash
# Option 1: Standard Mode (default)
# - One IP per pod
# - Limited by ENI capacity

# Option 2: Prefix Delegation Mode (recommended for high pod density)
kubectl set env daemonset -n kube-system aws-node ENABLE_PREFIX_DELEGATION=true
kubectl set env daemonset -n kube-system aws-node WARM_PREFIX_TARGET=1

# Option 3: IPv6 (recommended for IP exhaustion issues)
# - Virtually unlimited IPs
# - Must create IPv6-enabled cluster

# Option 4: Custom Networking (for secondary CIDR)
kubectl set env daemonset -n kube-system aws-node AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true
kubectl set env daemonset -n kube-system aws-node ENI_CONFIG_LABEL_DEF=topology.kubernetes.io/zone
```

**2.2 Configure IP Management**

```bash
# Warm pool settings (reduce pod startup time)
kubectl set env daemonset -n kube-system aws-node WARM_IP_TARGET=5
kubectl set env daemonset -n kube-system aws-node MINIMUM_IP_TARGET=10

# Maximum IPs per node
kubectl set env daemonset -n kube-system aws-node MAX_ENI=3

# Monitor IP usage
kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/master/config/master/cni-metrics-helper.yaml
```

### Phase 3: Load Balancer Setup

**3.1 Configure IngressClass**

```yaml
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: alb
spec:
  controller: ingress.k8s.aws/alb
---
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: nginx
spec:
  controller: k8s.io/ingress-nginx
```

**3.2 Create Shared ALB with IngressGroups**

```yaml
# App 1
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app1-ingress
  annotations:
    alb.ingress.kubernetes.io/group.name: shared-alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/healthcheck-path: /health
spec:
  ingressClassName: alb
  rules:
  - host: app1.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app1-service
            port:
              number: 80
---
# App 2 (shares same ALB)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app2-ingress
  annotations:
    alb.ingress.kubernetes.io/group.name: shared-alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
spec:
  ingressClassName: alb
  rules:
  - host: app2.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app2-service
            port:
              number: 80
```

**3.3 Create NLB for TCP Services**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: tcp-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: external
    service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: ip
    service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-protocol: TCP
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  selector:
    app: tcp-app
  ports:
  - port: 3306
    targetPort: 3306
    protocol: TCP
```

### Phase 4: Network Security

**4.1 Enable Network Policies**

```bash
# For VPC CNI v1.14+
kubectl set env daemonset -n kube-system aws-node ENABLE_NETWORK_POLICY=true

# OR install Calico for enhanced policies
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/calico-policy-only.yaml
```

**4.2 Implement Security Groups for Pods**

```bash
# Enable SGP in VPC CNI
kubectl set env daemonset -n kube-system aws-node ENABLE_POD_ENI=true

# Create security group
aws ec2 create-security-group \
  --group-name pod-security-group \
  --description "Security group for pods" \
  --vpc-id vpc-xxx

# Create SecurityGroupPolicy
kubectl apply -f - <<EOF
apiVersion: vpcresources.k8s.aws/v1beta1
kind: SecurityGroupPolicy
metadata:
  name: database-pods-sg
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: database
  securityGroups:
    groupIds:
    - sg-xxx
EOF
```

**4.3 Default Deny Network Policy**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Phase 5: DNS and Service Discovery

**5.1 Configure CoreDNS**

```bash
# Scale CoreDNS for large clusters
kubectl scale deployment coredns -n kube-system --replicas=3

# Custom DNS forwarding
kubectl edit configmap coredns -n kube-system
# Add custom forwarding rules in Corefile
```

**5.2 Install ExternalDNS**

```bash
# Create IAM policy for Route 53
cat > external-dns-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "route53:ChangeResourceRecordSets"
      ],
      "Resource": "arn:aws:route53:::hostedzone/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "route53:ListHostedZones",
        "route53:ListResourceRecordSets"
      ],
      "Resource": "*"
    }
  ]
}
EOF

# Create IRSA
eksctl create iamserviceaccount \
  --cluster=my-cluster \
  --namespace=kube-system \
  --name=external-dns \
  --attach-policy-arn=arn:aws:iam::ACCOUNT_ID:policy/ExternalDNSPolicy \
  --approve

# Deploy ExternalDNS
helm repo add external-dns https://kubernetes-sigs.github.io/external-dns/
helm install external-dns external-dns/external-dns \
  -n kube-system \
  --set serviceAccount.create=false \
  --set serviceAccount.name=external-dns \
  --set provider=aws \
  --set policy=sync \
  --set txtOwnerId=my-cluster
```

### Phase 6: Optimization and Monitoring

**6.1 Reduce Cross-AZ Traffic**

```yaml
# Use topology-aware routing
apiVersion: v1
kind: Service
metadata:
  name: app-service
  annotations:
    service.kubernetes.io/topology-mode: Auto
spec:
  internalTrafficPolicy: Local
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
```

**6.2 Deploy VPC Endpoints**

```bash
# Create VPC endpoints for AWS services
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-xxx \
  --service-name com.amazonaws.us-west-2.ecr.api \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-xxx subnet-yyy \
  --security-group-ids sg-zzz

# Common endpoints to create:
# - com.amazonaws.region.ecr.api
# - com.amazonaws.region.ecr.dkr
# - com.amazonaws.region.s3
# - com.amazonaws.region.logs
# - com.amazonaws.region.sts
```

**6.3 Monitor Network Metrics**

```bash
# Deploy CNI metrics helper
kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/master/config/master/cni-metrics-helper.yaml

# View metrics
kubectl top nodes
kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes
```

## Common Tasks

### Check Available IPs

```bash
# View CNI metrics
kubectl get daemonset aws-node -n kube-system -o yaml | grep -A 10 WARM

# Check CloudWatch metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EKS \
  --metric-name cluster_ip_allocation \
  --dimensions Name=ClusterName,Value=my-cluster \
  --statistics Average \
  --start-time 2025-01-01T00:00:00Z \
  --end-time 2025-01-27T00:00:00Z \
  --period 3600
```

### Troubleshoot Pod Networking

```bash
# Check pod IP assignment
kubectl get pods -o wide

# Describe pod networking
kubectl describe pod <pod-name> | grep IP

# Check CNI logs
kubectl logs -n kube-system -l k8s-app=aws-node --tail=50

# Verify ENI attachments
aws ec2 describe-network-interfaces \
  --filters "Name=attachment.instance-id,Values=i-xxx"
```

### Verify Load Balancer Configuration

```bash
# Check ingress status
kubectl get ingress -A
kubectl describe ingress <ingress-name>

# Check ALB controller logs
kubectl logs -n kube-system deployment/aws-load-balancer-controller

# Verify target groups
aws elbv2 describe-target-groups
aws elbv2 describe-target-health --target-group-arn <arn>
```

### Test Network Policies

```bash
# Create test pod
kubectl run test-pod --image=nicolaka/netshoot -it --rm -- /bin/bash

# Test connectivity
curl http://service-name:port
nc -zv service-name port

# Verify policy applied
kubectl get networkpolicy
kubectl describe networkpolicy <policy-name>
```

## Reference Documentation

For detailed information, see:

- **VPC CNI**: `references/vpc-cni.md` - CNI plugin configuration, modes, and optimization
- **Load Balancers**: `references/load-balancers.md` - ALB, NLB, and AWS Load Balancer Controller
- **Network Policies**: `references/network-policies.md` - Network policies, security groups, and segmentation

## Best Practices

### IP Address Management
- Use prefix delegation mode for high pod density clusters
- Consider IPv6 for new clusters to avoid IP exhaustion
- Monitor IP usage with CNI metrics helper
- Plan subnets with 2x expected IP requirements

### Load Balancing
- Use IngressGroups to share ALBs and reduce costs
- Set target-type to `ip` for best performance
- Enable cross-zone load balancing for high availability
- Use NLB for static IP requirements

### Network Security
- Enable network policies (VPC CNI v1.14+ or Calico)
- Combine NetworkPolicies with Security Groups for Pods (defense-in-depth)
- Default deny, explicit allow policy approach
- Use private subnets for worker nodes

### Performance and Cost
- Deploy VPC endpoints for AWS services (reduces NAT costs)
- Use topology-aware routing to minimize cross-AZ traffic
- Enable prefix delegation to reduce ENI pressure
- Monitor cross-AZ traffic with Container Network Observability

### High Availability
- Spread subnets across at least 3 availability zones
- Use multiple replicas for critical services
- Configure pod topology spread constraints
- Enable cross-zone load balancing

## Troubleshooting

### Pod Can't Get IP Address

**Symptoms**: Pod stuck in ContainerCreating

**Check**:
```bash
# View CNI logs
kubectl logs -n kube-system -l k8s-app=aws-node

# Check available IPs
kubectl get nodes -o jsonpath='{.items[*].status.allocatable.pods}'

# Verify ENI limits not reached
aws ec2 describe-instances --instance-ids i-xxx
```

**Solutions**:
- Enable prefix delegation mode
- Use larger instance types (more ENIs)
- Add more nodes to cluster

### Ingress Not Creating ALB

**Symptoms**: No load balancer provisioned for Ingress

**Check**:
```bash
# Verify controller running
kubectl get pods -n kube-system | grep aws-load-balancer-controller

# Check controller logs
kubectl logs -n kube-system deployment/aws-load-balancer-controller

# Verify subnet tags
aws ec2 describe-subnets --subnet-ids subnet-xxx
```

**Solutions**:
- Ensure subnets properly tagged
- Verify IAM permissions for controller
- Check IngressClass specified correctly

### Network Policy Not Working

**Symptoms**: Traffic not blocked as expected

**Check**:
```bash
# Verify network policy enabled
kubectl get daemonset -n kube-system aws-node -o yaml | grep ENABLE_NETWORK_POLICY

# Check policy applied
kubectl get networkpolicy -A
kubectl describe networkpolicy <name>
```

**Solutions**:
- Enable network policy support in CNI
- Verify label selectors match pods
- Check policy has both ingress and egress rules

### DNS Resolution Failures

**Symptoms**: Pods can't resolve service names

**Check**:
```bash
# Test DNS from pod
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup kubernetes.default

# Check CoreDNS status
kubectl get pods -n kube-system -l k8s-app=kube-dns

# View CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns
```

**Solutions**:
- Scale CoreDNS replicas
- Check CoreDNS ConfigMap
- Verify network policy allows DNS traffic

## 2025 Recommendations

### CNI Selection
- **Default**: VPC CNI with prefix delegation mode
- **IPv4 exhaustion**: IPv6 clusters (AWS recommended)
- **Advanced policies**: VPC CNI + Calico policy-only agent
- **Maximum features**: Cilium (for EKS Hybrid Nodes or advanced use cases)

### Load Balancing
- **AWS Native**: AWS Load Balancer Controller (recommended)
- **Multi-cloud portability**: NGINX Ingress with NLB
- **Service mesh**: Istio Gateway (App Mesh deprecated Sept 2026)

### Network Security
- VPC CNI native network policies (v1.14+) for most use cases
- Calico for enhanced policy features and observability
- Cilium for eBPF-powered security and deep insights
- Always combine with Security Groups for Pods (defense-in-depth)

### Cost Optimization
- VPC endpoints for all AWS services (ECR, S3, CloudWatch, etc.)
- Topology-aware routing to minimize cross-AZ traffic
- Single NAT Gateway per AZ (not per subnet)
- Monitor network costs with Container Network Observability
