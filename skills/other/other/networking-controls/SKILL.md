---
name: networking-controls
description: Network security and connectivity standards. Use when networking controls guidance is required.
---
## Purpose

Help agents apply networking control requirements (default deny, segmentation, controlled outbound access) in concrete recommendations and plans, without re-encoding the full guideline text.

### Timeout and Backoff Configuration

Apply appropriate timeout and retry policies:
- Set realistic connection timeouts
- Implement exponential backoff for retries
- Configure circuit breaker patterns
- Apply jitter to prevent thundering herd

Timeout and retry configuration:
```python
import time
from typing import Callable, Any

# Exponential backoff implementation
def exponential_backoff_retry(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0
) -> Any:
    retry_count = 0
    current_delay = base_delay

    while retry_count < max_retries:
        try:
            return func()
        except Exception as e:
            retry_count += 1
            if retry_count >= max_retries:
                raise e

            # Add jitter to prevent thundering herd
            jitter = current_delay * 0.1 * (time.time() % 1)
            sleep_time = min(current_delay + jitter, max_delay)

            time.sleep(sleep_time)
            current_delay *= backoff_factor

# Circuit breaker implementation
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func: Callable, *args, kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"

            raise e
```

## Network Performance Optimization

### Load Balancing Configuration

Implement optimal load balancing strategies:
- Use health checks for backend service monitoring
- Apply appropriate load balancing algorithms
- Implement session affinity when required
- Configure geographic load balancing for global services

Load balancer configuration:
```yaml
# Kubernetes service with load balancing
apiVersion: v1
kind: Service
metadata:
  name: web-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
spec:
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer

# Health check configuration
apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  containers:
  - name: web-app
    image: nginx:latest
    ports:
    - containerPort: 8080
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
      initialDelaySeconds: 30
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 5
```

### Caching and CDN Integration

Implement comprehensive caching strategy:
- Configure reverse proxy caching for static content
- Deploy CDN for global content delivery
- Apply application-level caching for dynamic content
- Implement cache invalidation policies

Caching configuration:
```nginx
# Nginx reverse proxy caching
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=10g
                 inactive=60m use_temp_path=off;

server {
    listen 443 ssl;
    server_name api.example.com;

    # Enable caching
    proxy_cache my_cache;
    proxy_cache_valid 200 302 10m;
    proxy_cache_valid 404 1m;

    # Cache key configuration
    proxy_cache_key "$scheme$request_method$host$request_uri";

    # Bypass cache for specific requests
    proxy_cache_bypass $http_authorization;
    proxy_no_cache $http_authorization;

    location /api/ {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Network Monitoring and Observability

### Network Metrics Collection

Implement comprehensive network monitoring:
- Monitor bandwidth utilization and throughput
- Track connection counts and response times
- Collect error rates and timeout statistics
- Monitor security events and anomalous traffic

Monitoring configuration:
```yaml
# Prometheus network monitoring rules
groups:
- name: network.rules
  rules:
  - alert: HighBandwidthUsage
    expr: rate(container_network_transmit_bytes_total[5m]) / 1024 / 1024 > 100
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "High bandwidth usage detected"
      description: "Network transmit rate is {{ $value }} MB/s"

  - alert: ConnectionPoolExhaustion
    expr: db_connections_active / db_connections_max > 0.9
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Database connection pool nearly exhausted"
      description: "Connection pool usage is {{ $value | humanizePercentage }}"
```

### Network Security Monitoring

Implement security event monitoring:
- Monitor firewall rule hits and denials
- Track unusual traffic patterns and anomalies
- Collect DDoS attack indicators
- Monitor authentication failures and access violations

Security monitoring setup:
```bash
#!/bin/bash
# Network security monitoring script

# Monitor failed SSH connections
monitor_ssh_failures() {
    journalctl -u sshd --since "1 hour ago" | grep "Failed password" | \
        awk '{print $1, $2, $3, $11, $13}' | \
        sort | uniq -c | sort -nr
}

# Monitor unusual traffic patterns
monitor_traffic_anomalies() {
    # Check for port scanning
    nmap -sS -p 1-65535 192.168.1.0/24 --open

    # Monitor connection spikes
    netstat -an | grep :80 | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr
}

# Generate security report
generate_security_report() {
    echo "=== Network Security Report ==="
    echo "Timestamp: $(date)"
    echo ""

    echo "Failed SSH attempts:"
    monitor_ssh_failures
    echo ""

    echo "Top traffic sources:"
    monitor_traffic_anomalies | head -10
    echo ""

    echo "Firewall log summary:"
    tail -n 1000 /var/log/iptables.log | grep DROP | wc -l
}
```
