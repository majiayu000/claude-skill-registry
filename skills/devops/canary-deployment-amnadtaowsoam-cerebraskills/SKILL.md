---
name: Canary Deployment
description: Gradually rolling out new versions to a subset of users, monitoring for issues, and expanding the rollout if everything looks healthy to minimize risk and enable fast rollback.
---

# Canary Deployment

> **Current Level:** Intermediate  
> **Domain:** DevOps / Deployment

---

## Overview

Canary deployment is a deployment strategy where you gradually roll out a new version to a subset of users, monitor for issues, and expand the rollout if everything looks healthy. This minimizes risk by catching issues early and enabling fast rollback.

## What is Canary Deployment

### Core Concept

```
┌─────────────────────────────────────────────────────────────────┐
│  Canary Deployment Process                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Stage 1: 5% Canary                                    │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  Old Version (95%) │ New Version (5%) │         │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Stage 2: 25% Canary                                   │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  Old Version (75%) │ New Version (25%) │        │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Stage 3: 50% Canary                                   │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  Old Version (50%) │ New Version (50%) │        │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Stage 4: 100% Rollout                                │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  New Version (100%) │                         │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why Canary Deployment

| Benefit | Impact |
|---------|---------|
| **Reduce Blast Radius** | Only affects small % of users |
| **Real-World Testing** | Test with actual users |
| **Early Issue Detection** | Catch problems early |
| **Confidence Building** | Gradual expansion |
| **Rollback Safety** | Quick rollback if issues |

## Canary Process

### Step-by-Step Process

```
┌─────────────────────────────────────────────────────────────────┐
│  Canary Deployment Steps                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Deploy to Canary Servers ──▶ 2. Route 5% Traffic ──▶ 3. Monitor Metrics ──▶ 4. Increase to 25% ──▶ 5. Monitor ──▶ 6. Increase to 50% ──▶ 7. Monitor ──▶ 8. 100% Rollout │
│                                                                  │
│  └───────────────────────────────────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

### Step 1: Deploy to Canary

```bash
# Deploy new version to canary servers
kubectl apply -f canary-deployment.yaml

# Wait for canary to be ready
kubectl rollout status deployment/web-app-canary
```

```yaml
# Canary deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app-canary
  labels:
    app: web-app
    version: v2.0
spec:
  replicas: 1
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
        version: v2.0
    spec:
      containers:
      - name: web-app
        image: web-app:v2.0
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            successThreshold: 3
            failureThreshold: 3
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            successThreshold: 3
            failureThreshold: 3
```

### Step 2: Route 5% Traffic

```yaml
# Service with traffic splitting
apiVersion: v1
kind: Service
metadata:
  name: web-app
spec:
  selector:
    app: web-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

```yaml
# Istio VirtualService for canary
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: web-app
spec:
  hosts:
    - web-app.example.com
  http:
    - route:
      - destination:
          host: web-app
          subset: v1
        weight: 95
      - destination:
          host: web-app
          subset: v2
        weight: 5
```

### Step 3: Monitor Metrics

```python
# Monitoring script
import requests
import time

def monitor_canary():
    """Monitor canary metrics."""
    while True:
        try:
            # Check error rate
            error_rate = get_error_rate()
            print(f"Error rate: {error_rate}%")
            
            # Check latency
            latency = get_latency()
            print(f"Latency: {latency}ms")
            
            # Check business metrics
            conversion_rate = get_conversion_rate()
            print(f"Conversion rate: {conversion_rate}%")
            
            # Check if metrics are healthy
            if error_rate > 5:
                print("⚠️  Error rate too high")
                trigger_rollback()
                break
                
            if latency > 1000:
                print("⚠️  Latency too high")
                trigger_rollback()
                break
                
            if conversion_rate < 10:
                print("⚠️  Conversion rate too low")
                trigger_rollback()
                break
                
            print("✓ Metrics healthy")
            
        except Exception as e:
            print(f"✗ Error monitoring: {e}")
            
        time.sleep(60)  # Check every minute

monitor_canary()
```

### Step 4: Increase to 25%

```yaml
# Update VirtualService for 25% canary
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: web-app
spec:
  hosts:
    - web-app.example.com
  http:
    - route:
      - destination:
          host: web-app
          subset: v1
        weight: 75
      - destination:
          host: web-app
          subset: v2
        weight: 25
```

### Step 5: Monitor

```python
# Continue monitoring for 25% canary
def monitor_25_percent():
    """Monitor 25% canary metrics."""
    while True:
        try:
            # Check error rate
            error_rate = get_error_rate()
            print(f"Error rate: {error_rate}%")
            
            # Check latency
            latency = get_latency()
            print(f"Latency: {latency}ms")
            
            # Check business metrics
            conversion_rate = get_conversion_rate()
            print(f"Conversion rate: {conversion_rate}%")
            
            # Check if metrics are healthy
            if error_rate > 5:
                print("⚠️  Error rate too high")
                trigger_rollback()
                break
                
            if latency > 1000:
                print("⚠️  Latency too high")
                trigger_rollback()
                break
                
            if conversion_rate < 10:
                print("⚠️  Conversion rate too low")
                trigger_rollback()
                break
                
            print("✓ Metrics healthy")
            
        except Exception as e:
            print(f"✗ Error monitoring: {e}")
            
        time.sleep(60)  # Check every minute

monitor_25_percent()
```

### Step 6: Increase to 50%

```yaml
# Update VirtualService for 50% canary
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: web-app
spec:
  hosts:
    - web-app.example.com
  http:
    - route:
      - destination:
          host: web-app
          subset: v1
        weight: 50
      - destination:
          host: web-app
          subset: v2
        weight: 50
```

### Step 7: Monitor

```python
# Continue monitoring for 50% canary
def monitor_50_percent():
    """Monitor 50% canary metrics."""
    while True:
        try:
            # Check error rate
            error_rate = get_error_rate()
            print(f"Error rate: {error_rate}%")
            
            # Check latency
            latency = get_latency()
            print(f"Latency: {latency}ms")
            
            # Check business metrics
            conversion_rate = get_conversion_rate()
            print(f"Conversion rate: {conversion_rate}%")
            
            # Check if metrics are healthy
            if error_rate > 5:
                print("⚠️  Error rate too high")
                trigger_rollback()
                break
                
            if latency > 1000:
                print("⚠️  Latency too high")
                trigger_rollback()
                break
                
            if conversion_rate < 10:
                print("⚠️  Conversion rate too low")
                trigger_rollback()
                break
                
            print("✓ Metrics healthy")
            
        except Exception as e:
            print(f"✗ Error monitoring: {e}")
            
        time.sleep(60)  # Check every minute

monitor_50_percent()
```

### Step 8: 100% Rollout

```yaml
# Update VirtualService for 100% canary
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: web-app
spec:
  hosts:
    - web-app.example.com
  http:
    - route:
      - destination:
          host: web-app
          subset: v2
        weight: 100
```

## Traffic Routing

### Load Balancer with Weights

```yaml
# Kubernetes Service with traffic splitting
apiVersion: v1
kind: Service
metadata:
  name: web-app
spec:
  selector:
    app: web-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

```yaml
# Istio DestinationRule
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: web-app
spec:
  host: web-app
  subsets:
    - name: v1
      labels:
        version: v1.0
    - name: v2
      labels:
        version: v2.0
```

### Service Mesh

```yaml
# Istio VirtualService
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: web-app
spec:
  hosts:
    - web-app.example.com
  http:
    - route:
      - destination:
          host: web-app
          subset: v1
        weight: 95
      - destination:
          host: web-app
          subset: v2
        weight: 5
```

### Feature Flags

```javascript
// Using LaunchDarkly for canary
const LaunchDarkly = require('ldclient-node');

const client = LaunchDarkly.init('sdk-key');

client.on('ready', () => {
    const flagValue = client.variation('new-checkout', false, {
        key: 'user-123',
        custom: {
            segment: 'beta'
        }
    });
    
    if (flagValue) {
        // Show new checkout
    } else {
        // Show old checkout
    }
});
```

## Canary Metrics

### Error Rate

```python
# Calculate error rate
def get_error_rate():
    """Calculate error rate."""
    total_requests = 1000
    error_requests = 50
    
    error_rate = (error_requests / total_requests) * 100
    return error_rate

# Threshold: < 5%
```

### Latency

```python
# Calculate latency
def get_latency():
    """Calculate latency."""
    response_times = [100, 150, 200, 250, 300]
    
    average_latency = sum(response_times) / len(response_times)
    return average_latency

# Threshold: < 1000ms
```

### Business Metrics

```python
# Calculate conversion rate
def get_conversion_rate():
    """Calculate conversion rate."""
    visitors = 1000
    conversions = 100
    
    conversion_rate = (conversions / visitors) * 100
    return conversion_rate

# Threshold: > 10%
```

### Resource Usage

```python
# Calculate resource usage
def get_resource_usage():
    """Calculate resource usage."""
    cpu_usage = 50  # Percentage
    memory_usage = 60  # Percentage
    
    return {
        'cpu': cpu_usage,
        'memory': memory_usage
    }

# Threshold: CPU < 80%, Memory < 80%
```

## Canary Decision

### Automated Decision

```python
# Automated canary decision
def automated_canary_decision():
    """Automatically decide whether to proceed."""
    error_rate = get_error_rate()
    latency = get_latency()
    conversion_rate = get_conversion_rate()
    
    # Check if metrics are healthy
    if error_rate < 5 and latency < 1000 and conversion_rate > 10:
        print("✓ Metrics healthy, proceeding to next stage")
        return True
    else:
        print("✗ Metrics unhealthy, rolling back")
        return False

# Usage
if automated_canary_decision():
    increase_canary_percentage()
else:
    rollback_canary()
```

### Manual Decision

```python
# Manual canary decision
def manual_canary_decision():
    """Manually decide whether to proceed."""
    error_rate = get_error_rate()
    latency = get_latency()
    conversion_rate = get_conversion_rate()
    
    print(f"Error rate: {error_rate}%")
    print(f"Latency: {latency}ms")
    print(f"Conversion rate: {conversion_rate}%")
    
    # Ask user for decision
    decision = input("Proceed to next stage? (yes/no): ")
    
    if decision.lower() == 'yes':
        print("✓ Proceeding to next stage")
        return True
    else:
        print("✗ Rolling back")
        return False

# Usage
if manual_canary_decision():
    increase_canary_percentage()
else:
    rollback_canary()
```

### Hybrid Decision

```python
# Hybrid canary decision
def hybrid_canary_decision():
    """Hybrid decision: auto proceed unless anomaly."""
    error_rate = get_error_rate()
    latency = get_latency()
    conversion_rate = get_conversion_rate()
    
    print(f"Error rate: {error_rate}%")
    print(f"Latency: {latency}ms")
    print(f"Conversion rate: {conversion_rate}%")
    
    # Check for anomalies
    if error_rate > 5 or latency > 1000 or conversion_rate < 10:
        print("⚠️  Anomaly detected, manual review required")
        decision = input("Proceed to next stage? (yes/no): ")
        return decision.lower() == 'yes'
    else:
        print("✓ Metrics healthy, automatically proceeding")
        return True

# Usage
if hybrid_canary_decision():
    increase_canary_percentage()
else:
    rollback_canary()
```

## Canary Duration

### Fast Canary

```python
# Fast canary: 10 minutes per stage
def fast_canary():
    """Fast canary deployment."""
    stages = [5, 25, 50, 100]
    duration = 10  # minutes
    
    for stage in stages:
        print(f"Rolling out to {stage}%")
        set_canary_percentage(stage)
        time.sleep(duration * 60)  # Wait for duration
        
        if not check_metrics():
            rollback_canary()
            return
    
    print("✓ Canary deployment successful")
```

### Slow Canary

```python
# Slow canary: Hours per stage
def slow_canary():
    """Slow canary deployment."""
    stages = [5, 25, 50, 100]
    duration = 60  # minutes
    
    for stage in stages:
        print(f"Rolling out to {stage}%")
        set_canary_percentage(stage)
        time.sleep(duration * 60)  # Wait for duration
        
        if not check_metrics():
            rollback_canary()
            return
    
    print("✓ Canary deployment successful")
```

### Soak Time

```python
# Canary with soak time
def canary_with_soak_time():
    """Canary deployment with soak time."""
    stages = [5, 25, 50, 100]
    soak_time = 30  # minutes
    
    for stage in stages:
        print(f"Rolling out to {stage}%")
        set_canary_percentage(stage)
        time.sleep(soak_time * 60)  # Soak time
        
        if not check_metrics():
            rollback_canary()
            return
    
    print("✓ Canary deployment successful")
```

## User Selection

### Random Users

```python
# Random user selection
import random

def random_user_selection():
    """Select random users for canary."""
    canary_percentage = 5
    user_id = get_user_id()
    
    # Randomly select users
    if random.random() < canary_percentage / 100:
        return True
    else:
        return False

# Usage
if random_user_selection():
    show_new_version()
else:
    show_old_version()
```

### Internal Users

```python
# Internal user selection
def internal_user_selection():
    """Select internal users for canary."""
    user_email = get_user_email()
    
    # Check if user is internal
    if user_email.endswith('@company.com'):
        return True
    else:
        return False

# Usage
if internal_user_selection():
    show_new_version()
else:
    show_old_version()
```

### Beta Testers

```python
# Beta tester selection
def beta_tester_selection():
    """Select beta testers for canary."""
    user_id = get_user_id()
    
    # Check if user is beta tester
    beta_testers = ['user-1', 'user-2', 'user-3']
    
    if user_id in beta_testers:
        return True
    else:
        return False

# Usage
if beta_tester_selection():
    show_new_version()
else:
    show_old_version()
```

### Segment-Based

```python
# Segment-based selection
def segment_based_selection():
    """Select users based on segment."""
    user_segment = get_user_segment()
    
    # Select specific segments
    canary_segments = ['free-tier', 'new-users']
    
    if user_segment in canary_segments:
        return True
    else:
        return False

# Usage
if segment_based_selection():
    show_new_version()
else:
    show_old_version()
```

## Automated Canary with Flagger

### Flagger Installation

```bash
# Install Flagger
kubectl apply -k github.com/fluxcd/flagger//kustomize/istio
```

### Flagger Configuration

```yaml
# Flagger Canary resource
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: web-app
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  service:
    port: 80
    targetPort: 8080
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 5
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
      - name: request-duration
        thresholdRange:
          max: 500
    webhooks:
      - name: load-test
        url: http://flagger-loadtester/
        timeout: 5s
        metadata:
          cmd: "hey -z 1m -q 10 -c 2 http://web-app-canary/"
```

### Flagger Monitoring

```bash
# Monitor canary status
kubectl get canary web-app -w

# Check canary events
kubectl describe canary web-app
```

## Monitoring and Alerting

### Dashboards

```python
# Create monitoring dashboard
def create_canary_dashboard():
    """Create canary monitoring dashboard."""
    dashboard = {
        'title': 'Canary Deployment Monitoring',
        'panels': [
            {
                'title': 'Error Rate',
                'type': 'graph',
                'targets': [
                    {
                        'expr': 'rate(http_requests_total{status=~"5.."}[5m])'
                    }
                ]
            },
            {
                'title': 'Latency',
                'type': 'graph',
                'targets': [
                    {
                        'expr': 'histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))'
                    }
                ]
            },
            {
                'title': 'Conversion Rate',
                'type': 'graph',
                'targets': [
                    {
                        'expr': 'rate(conversions_total[5m]) / rate(visitors_total[5m])'
                    }
                ]
            }
        ]
    }
    
    return dashboard
```

### Alerting

```python
# Set up alerts
def setup_canary_alerts():
    """Set up canary alerts."""
    alerts = [
        {
            'name': 'High Error Rate',
            'condition': 'error_rate > 5',
            'action': 'send_alert',
            'message': 'Error rate too high, rolling back'
        },
        {
            'name': 'High Latency',
            'condition': 'latency > 1000',
            'action': 'send_alert',
            'message': 'Latency too high, rolling back'
        },
        {
            'name': 'Low Conversion Rate',
            'condition': 'conversion_rate < 10',
            'action': 'send_alert',
            'message': 'Conversion rate too low, rolling back'
        }
    ]
    
    return alerts
```

## Rollback

### Automatic Rollback

```python
# Automatic rollback
def automatic_rollback():
    """Automatically rollback if metrics are unhealthy."""
    error_rate = get_error_rate()
    latency = get_latency()
    conversion_rate = get_conversion_rate()
    
    # Check if metrics are unhealthy
    if error_rate > 5 or latency > 1000 or conversion_rate < 10:
        print("✗ Metrics unhealthy, rolling back")
        rollback_canary()
    else:
        print("✓ Metrics healthy")
```

### Manual Rollback

```python
# Manual rollback
def manual_rollback():
    """Manually rollback canary."""
    decision = input("Rollback canary? (yes/no): ")
    
    if decision.lower() == 'yes':
        print("Rolling back canary...")
        rollback_canary()
    else:
        print("Continuing canary...")
```

### Rollback Script

```python
# Rollback script
def rollback_canary():
    """Rollback canary to old version."""
    print("Rolling back canary...")
    
    # Update VirtualService to route 100% to old version
    update_virtual_service(100, 0)
    
    # Delete canary deployment
    delete_canary_deployment()
    
    print("✓ Canary rolled back")
```

## Database Challenges

### Backward-Compatible Schema Changes

```sql
-- Version N: Add new column (nullable)
ALTER TABLE users ADD COLUMN new_feature_enabled BOOLEAN;

-- Version N+1: Populate new column
UPDATE users SET new_feature_enabled = FALSE;

-- Version N+2: Enable feature for canary
UPDATE users SET new_feature_enabled = TRUE;

-- Version N+3: Make column non-nullable
ALTER TABLE users ALTER COLUMN new_feature_enabled SET NOT NULL;
```

### Both Versions Work with Same Schema

```sql
-- Both versions must work with same schema
-- Old version: Ignores new column
-- New version: Uses new column

-- Example:
-- Old version
SELECT * FROM users;

-- New version
SELECT *, new_feature_enabled FROM users;
```

## Session Handling

### Sticky Sessions

```yaml
# Istio DestinationRule with sticky sessions
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: web-app
spec:
  host: web-app
  trafficPolicy:
    loadBalancer:
      consistentHash:
        httpCookie:
          name: canary
          ttl: 60s
```

### Stateless Apps

```python
# Stateless app: No session handling needed
def handle_request(request):
    """Handle request without session."""
    # Process request
    response = process_request(request)
    
    # Return response
    return response
```

## Progressive Delivery

### Canary + Feature Flags

```python
# Canary deployment with feature flags
def canary_with_feature_flags():
    """Canary deployment with feature flags."""
    # Deploy new version
    deploy_new_version()
    
    # Enable feature flag for 5% of users
    set_feature_flag_percentage('new-checkout', 5)
    
    # Monitor metrics
    if check_metrics():
        # Increase to 25%
        set_feature_flag_percentage('new-checkout', 25)
        
        if check_metrics():
            # Increase to 50%
            set_feature_flag_percentage('new-checkout', 50)
            
            if check_metrics():
                # Increase to 100%
                set_feature_flag_percentage('new-checkout', 100)
            else:
                rollback_feature_flag()
        else:
            rollback_feature_flag()
    else:
        rollback_feature_flag()
```

### A/B Testing + Canary

```python
# A/B testing with canary
def ab_testing_with_canary():
    """A/B testing with canary deployment."""
    # Deploy new version
    deploy_new_version()
    
    # Split traffic 50/50
    set_canary_percentage(50)
    
    # Monitor metrics
    if check_metrics():
        # Determine winner
        winner = determine_winner()
        
        if winner == 'new':
            # Rollout new version
            set_canary_percentage(100)
        else:
            # Rollback to old version
            rollback_canary()
    else:
        rollback_canary()
```

## Tools

### Flagger

```bash
# Install Flagger
kubectl apply -k github.com/fluxcd/flagger//kustomize/istio

# Create canary
kubectl apply -f canary.yaml

# Monitor canary
kubectl get canary web-app -w
```

### Argo Rollouts

```bash
# Install Argo Rollouts
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml

# Create rollout
kubectl apply -f rollout.yaml

# Monitor rollout
kubectl argo rollouts get rollout web-app -w
```

### AWS CodeDeploy

```bash
# Create deployment group
aws deploy create-deployment-group \
  --application-name web-app \
  --deployment-group-name canary \
  --deployment-config-name CodeDeployDefault.Canary10Percent30Minutes

# Create deployment
aws deploy create-deployment \
  --application-name web-app \
  --deployment-group-name canary \
  --deployment-config-name CodeDeployDefault.Canary10Percent30Minutes \
  --s3-location bucket=web-app,bundleType=zip,key=web-app-v2.zip
```

### Service Mesh

```yaml
# Istio VirtualService
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: web-app
spec:
  hosts:
    - web-app.example.com
  http:
    - route:
      - destination:
          host: web-app
          subset: v1
        weight: 95
      - destination:
          host: web-app
          subset: v2
        weight: 5
```

### Feature Flags

```javascript
// LaunchDarkly
const LaunchDarkly = require('ldclient-node');

const client = LaunchDarkly.init('sdk-key');

client.on('ready', () => {
    const flagValue = client.variation('new-checkout', false, {
        key: 'user-123'
    });
    
    if (flagValue) {
        show_new_version();
    } else {
        show_old_version();
    }
});
```

## Canary vs Blue-Green

| Aspect | Canary | Blue-Green |
|--------|--------|------------|
| **Rollout** | Gradual | All-at-once |
| **Risk** | Lower | Higher |
| **Speed** | Slower | Faster |
| **Rollback** | Fast | Instant |
| **Cost** | Lower | Higher |
| **Complexity** | Higher | Lower |

## Real Examples

### Example 1: API Service Canary

**Scenario**: Deploy new API version

**Timeline**:
- 09:00: Deploy to canary
- 09:05: Route 5% traffic
- 09:15: Monitor metrics (healthy)
- 09:20: Increase to 25%
- 09:35: Monitor metrics (healthy)
- 09:40: Increase to 50%
- 09:55: Monitor metrics (healthy)
- 10:00: Rollout to 100%

**Outcome**: Successful deployment

### Example 2: Frontend Canary

**Scenario**: Deploy new checkout flow

**Timeline**:
- 14:00: Deploy to canary
- 14:05: Route 5% traffic
- 14:15: Monitor metrics (conversion rate low)
- 14:20: Rollback to old version

**Outcome**: Rollback due to low conversion rate

### Example 3: Kubernetes Canary with Flagger

**Scenario**: Deploy microservice with Flagger

**Timeline**:
- 10:00: Deploy new version
- 10:05: Flagger automatically routes 5% traffic
- 10:15: Flagger increases to 10%
- 10:25: Flagger increases to 15%
- 10:35: Flagger increases to 20%
- 10:45: Flagger increases to 25%
- 10:55: Flagger increases to 50%
- 11:05: Flagger increases to 100%

**Outcome**: Successful automated deployment

## Canary Anti-Patterns

### Not Monitoring Metrics

```python
# Bad: Blind canary (no monitoring)
def blind_canary():
    """Blind canary deployment."""
    # Deploy new version
    deploy_new_version()
    
    # Route 5% traffic
    set_canary_percentage(5)
    
    # Wait 10 minutes
    time.sleep(600)
    
    # Increase to 25%
    set_canary_percentage(25)
    
    # Wait 10 minutes
    time.sleep(600)
    
    # Increase to 50%
    set_canary_percentage(50)
    
    # Wait 10 minutes
    time.sleep(600)
    
    # Rollout to 100%
    set_canary_percentage(100)
```

### Increasing Too Fast

```python
# Bad: Fast canary (increases too fast)
def fast_canary():
    """Fast canary deployment."""
    stages = [5, 25, 50, 100]
    duration = 1  # minute
    
    for stage in stages:
        set_canary_percentage(stage)
        time.sleep(duration * 60)
```

### No Rollback Plan

```python
# Bad: No rollback plan
def canary_without_rollback():
    """Canary deployment without rollback plan."""
    # Deploy new version
    deploy_new_version()
    
    # Route 5% traffic
    set_canary_percentage(5)
    
    # Monitor metrics
    if not check_metrics():
        # No rollback plan
        print("Metrics unhealthy, but no rollback plan")
        return
    
    # Continue rollout
    set_canary_percentage(25)
```

## Summary Checklist

### Planning

- [ ] Canary strategy defined
- [ ] Metrics thresholds set
- [ ] Rollback plan documented
- [ ] Monitoring configured
- [ ] Alerting set up

### Deployment

- [ ] Deploy to canary
- [ ] Route initial traffic (5%)
- [ ] Monitor metrics
- [ ] Increase to 25%
- [ ] Monitor metrics
- [ ] Increase to 50%
- [ ] Monitor metrics
- [ ] Rollout to 100%

### Monitoring

- [ ] Error rate monitored
- [ ] Latency monitored
- [ ] Business metrics monitored
- [ ] Resource usage monitored
- [ ] Alerts configured

### Rollback

- [ ] Rollback triggers defined
- [ ] Rollback procedure documented
- [ ] Rollback tested
- [ ] Rollback automated
```

---

## Quick Start

### Kubernetes Canary Deployment

```yaml
# canary-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-canary
spec:
  replicas: 1  # 5% of traffic
  selector:
    matchLabels:
      app: myapp
      version: canary
  template:
    metadata:
      labels:
        app: myapp
        version: canary
    spec:
      containers:
      - name: app
        image: myapp:v2
---
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
```

### Traffic Splitting

```yaml
# Istio VirtualService for canary
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: app
spec:
  hosts:
  - app.example.com
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: app
        subset: canary
      weight: 100
  - route:
    - destination:
        host: app
        subset: stable
      weight: 95
    - destination:
        host: app
        subset: canary
      weight: 5
```

---

## Production Checklist

- [ ] **Traffic Splitting**: Configure traffic splitting (5% initial)
- [ ] **Monitoring**: Set up comprehensive monitoring
- [ ] **Metrics**: Define success/failure metrics
- [ ] **Alerts**: Configure alerts for canary issues
- [ ] **Rollback Plan**: Automated rollback triggers
- [ ] **Testing**: Test canary deployment process
- [ ] **Documentation**: Document canary procedure
- [ ] **Approval**: Approval process for promotion
- [ ] **Timeline**: Define canary duration (e.g., 1 hour)
- [ ] **Gradual Rollout**: Plan for gradual traffic increase
- [ ] **Communication**: Notify team of canary deployment
- [ ] **Validation**: Validate canary health before promotion

---

## Anti-patterns

### ❌ Don't: No Monitoring

```yaml
# ❌ Bad - Deploy without monitoring
apiVersion: apps/v1
kind: Deployment
# No health checks or metrics!
```

```yaml
# ✅ Good - With monitoring
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: app
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
```

### ❌ Don't: Too Fast Rollout

```yaml
# ❌ Bad - Jump to 100% immediately
weight: 5  # 5%
# ... 1 minute later
weight: 100  # 100% - Too fast!
```

```yaml
# ✅ Good - Gradual increase
# Stage 1: 5% for 1 hour
weight: 5
# Stage 2: 25% for 1 hour
weight: 25
# Stage 3: 50% for 1 hour
weight: 50
# Stage 4: 100%
weight: 100
```

### ❌ Don't: No Rollback Triggers

```yaml
# ❌ Bad - Manual rollback only
# No automatic triggers
```

```yaml
# ✅ Good - Automatic rollback
apiVersion: argoproj.io/v1alpha1
kind: Rollout
spec:
  strategy:
    canary:
      steps:
      - setWeight: 5
      - pause: { duration: 1h }
      - analysis:
          templates:
          - templateName: error-rate
          args:
          - name: error-rate
            value: "0.01"  # Rollback if > 1%
```

---

## Integration Points

- **Blue-Green Deployment** (`26-deployment-strategies/blue-green-deployment/`) - Alternative strategy
- **Rollback Strategies** (`26-deployment-strategies/rollback-strategies/`) - Rollback procedures
- **Monitoring** (`14-monitoring-observability/`) - Deployment monitoring

---

## Further Reading

- [Kubernetes Canary Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#canary-deployment)
- [Istio Traffic Management](https://istio.io/latest/docs/tasks/traffic-management/)
- [Argo Rollouts](https://argoproj.github.io/argo-rollouts/)
- [ ] Rollback monitored

### Post-Deployment

- [ ] Metrics reviewed
- [ ] Documentation updated
- [ ] Lessons learned
- [ ] Process improved
