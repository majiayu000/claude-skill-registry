---
name: load-balancer-setup
description: Configure and deploy load balancers (HAProxy, AWS ELB/ALB/NLB) for distributing traffic, session management, and high availability.
---

# Load Balancer Setup

## Overview

Deploy and configure load balancers to distribute traffic across multiple backend servers, ensuring high availability, fault tolerance, and optimal resource utilization across your infrastructure.

## When to Use

- Multi-server traffic distribution
- High availability and failover
- Session persistence and sticky sessions
- Health checking and auto-recovery
- SSL/TLS termination
- Cross-region load balancing
- API rate limiting at load balancer
- DDoS mitigation

## Implementation Examples

### 1. **HAProxy Configuration**

```conf
# /etc/haproxy/haproxy.cfg
global
    log stdout local0
    log stdout local1 notice
    maxconn 4096
    daemon

    # Security
    tune.ssl.default-dh-param 2048
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256
    ssl-default-bind-options ssl-min-ver TLSv1.2

defaults
    log global
    mode http
    option httplog
    option denylogin
    option forwardfor
    option http-server-close

    # Timeouts
    timeout connect 5000
    timeout client 50000
    timeout server 50000

    # Stats
    stats enable
    stats uri /stats
    stats refresh 30s
    stats admin if TRUE

# Frontend - Public facing
frontend web_frontend
    bind *:80
    bind *:443 ssl crt /etc/ssl/certs/myapp.pem
    mode http
    option httplog

    # Redirect HTTP to HTTPS
    http-request redirect scheme https if !{ ssl_fc }

    # Logging
    log /dev/log local0 debug

    # Rate limiting
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny if { sc_http_req_rate(0) gt 100 }

    # ACLs
    acl is_websocket hdr(Upgrade) -i websocket
    acl is_api path_beg /api/
    acl is_health path /health
    acl is_static path_beg /static/

    # Route to appropriate backend
    use_backend health_backend if is_health
    use_backend api_backend if is_api
    use_backend static_backend if is_static
    use_backend web_backend if is_websocket
    default_backend web_backend

# Frontend for internal API
frontend internal_api_frontend
    bind 127.0.0.1:8080
    mode http
    default_backend stats_backend

# Health check backend
backend health_backend
    mode http
    balance roundrobin
    server local 127.0.0.1:8080 check

# Main web backend
backend web_backend
    mode http
    balance roundrobin

    # Session persistence
    cookie SERVERID insert indirect nocache

    # Compression
    compression algo gzip
    compression type text/html text/plain text/css application/json

    # Servers with health checks
    server web1 10.0.1.10:8080 check cookie web1 weight 5
    server web2 10.0.1.11:8080 check cookie web2 weight 5
    server web3 10.0.1.12:8080 check cookie web3 weight 3

    # Health check configuration
    option httpchk GET /health HTTP/1.1\r\nHost:\ localhost
    timeout check 5s

# API backend with connection limits
backend api_backend
    mode http
    balance least_conn
    maxconn 1000

    option httpchk GET /api/health
    timeout check 5s

    server api1 10.0.2.10:3000 check weight 5
    server api2 10.0.2.11:3000 check weight 5
    server api3 10.0.2.12:3000 check weight 3

# Static file backend
backend static_backend
    mode http
    balance roundrobin

    # Cache control for static files
    http-response set-header Cache-Control "public, max-age=31536000, immutable"

    server static1 10.0.3.10:80 check
    server static2 10.0.3.11:80 check

# Stats backend
backend stats_backend
    stats enable
    stats uri /stats
    stats refresh 30s
```

### 2. **AWS Application Load Balancer (CloudFormation)**

```yaml
# aws-alb-cloudformation.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Application Load Balancer with Target Groups'

Parameters:
  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: VPC ID
  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>
    Description: Public subnet IDs for ALB
  Environment:
    Type: String
    Default: production
    AllowedValues: [dev, staging, production]

Resources:
  # Security Group for ALB
  LoadBalancerSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for ALB
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
      SecurityGroupEgress:
        - IpProtocol: -1
          CidrIp: 0.0.0.0/0
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-alb-sg'

  # Application Load Balancer
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub '${Environment}-alb'
      Type: application
      Scheme: internet-facing
      SecurityGroups:
        - !Ref LoadBalancerSecurityGroup
      Subnets: !Ref SubnetIds
      Tags:
        - Key: Environment
          Value: !Ref Environment

  # HTTP Listener (redirect to HTTPS)
  HttpListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - Type: redirect
          RedirectConfig:
            Protocol: HTTPS
            Port: '443'
            StatusCode: HTTP_301
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 80
      Protocol: HTTP

  # HTTPS Listener
  HttpsListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref WebTargetGroup
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 443
      Protocol: HTTPS
      Certificates:
        - CertificateArn: !Sub 'arn:aws:acm:${AWS::Region}:${AWS::AccountId}:certificate/xxxxxxxx'

  # Target Group for Web Servers
  WebTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub '${Environment}-web-tg'
      Port: 8080
      Protocol: HTTP
      VpcId: !Ref VpcId
      TargetType: instance

      # Health Check
      HealthCheckEnabled: true
      HealthCheckPath: /health
      HealthCheckProtocol: HTTP
      HealthCheckIntervalSeconds: 30
      HealthCheckTimeoutSeconds: 5
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 3

      # Stickiness
      TargetGroupAttributes:
        - Key: deregistration_delay.timeout_seconds
          Value: '30'
        - Key: stickiness.enabled
          Value: 'true'
        - Key: stickiness.type
          Value: 'lb_cookie'
        - Key: stickiness.lb_cookie.duration_seconds
          Value: '86400'

  # Target Group for API
  ApiTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub '${Environment}-api-tg'
      Port: 3000
      Protocol: HTTP
      VpcId: !Ref VpcId
      TargetType: instance

      HealthCheckPath: /api/health
      HealthCheckIntervalSeconds: 15
      HealthCheckTimeoutSeconds: 5
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 2

  # Listener Rule for API routing
  ApiListenerRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      Actions:
        - Type: forward
          TargetGroupArn: !Ref ApiTargetGroup
      Conditions:
        - Field: path-pattern
          Values: ['/api/*']
      ListenerArn: !Ref HttpsListener
      Priority: 1

Outputs:
  LoadBalancerDNS:
    Description: DNS name of the ALB
    Value: !GetAtt ApplicationLoadBalancer.DNSName
  LoadBalancerArn:
    Description: ARN of the ALB
    Value: !Ref ApplicationLoadBalancer
  WebTargetGroupArn:
    Description: ARN of Web Target Group
    Value: !Ref WebTargetGroup
  ApiTargetGroupArn:
    Description: ARN of API Target Group
    Value: !Ref ApiTargetGroup
```

### 3. **Load Balancer Health Check Script**

```bash
#!/bin/bash
# health-check.sh - Monitor backend health

set -euo pipefail

BACKENDS=("10.0.1.10:8080" "10.0.1.11:8080" "10.0.1.12:8080")
HEALTH_ENDPOINT="/health"
TIMEOUT=5
ALERT_EMAIL="ops@myapp.com"

check_backend_health() {
    local backend=$1
    local host=${backend%:*}
    local port=${backend#*:}

    if timeout "$TIMEOUT" bash -c "echo >/dev/tcp/$host/$port" 2>/dev/null; then
        if curl -sf --max-time "$TIMEOUT" "http://$backend$HEALTH_ENDPOINT" > /dev/null; then
            return 0
        fi
    fi
    return 1
}

main() {
    local unhealthy_backends=()

    for backend in "${BACKENDS[@]}"; do
        if ! check_backend_health "$backend"; then
            unhealthy_backends+=("$backend")
            echo "WARNING: Backend $backend is unhealthy"
        else
            echo "OK: Backend $backend is healthy"
        fi
    done

    if [ ${#unhealthy_backends[@]} -gt 0 ]; then
        local message="Unhealthy backends detected: ${unhealthy_backends[*]}"
        echo "$message"
        echo "$message" | mail -s "Load Balancer Alert" "$ALERT_EMAIL"
        exit 1
    fi
}

main "$@"
```

### 4. **Load Balancer Monitoring**

```yaml
# prometheus-scrape-config.yaml
scrape_configs:
  - job_name: 'haproxy'
    static_configs:
      - targets: ['localhost:8404']
    metrics_path: '/stats;csv'
    scrape_interval: 15s

  - job_name: 'alb'
    cloudwatch_sd_configs:
      - region: us-east-1
        port: 443
    relabel_configs:
      - source_labels: [__meta_aws_cloudwatch_namespace]
        action: keep
        regex: 'AWS/ApplicationELB'
```

## Load Balancing Algorithms

- **Round Robin**: Sequential distribution
- **Least Connections**: Fewest active connections
- **IP Hash**: Based on client IP
- **Weighted**: Proportional to server capacity
- **Random**: Random distribution

## Best Practices

### ✅ DO
- Implement health checks
- Use connection pooling
- Enable session persistence when needed
- Monitor load balancer metrics
- Implement rate limiting
- Use multiple availability zones
- Enable SSL/TLS termination
- Implement graceful connection draining

### ❌ DON'T
- Allow single point of failure
- Skip health check configuration
- Mix HTTP and HTTPS without redirect
- Ignore backend server limits
- Over-provision without monitoring
- Cache sensitive responses
- Use default security groups
- Neglect backup load balancers

## Resources

- [HAProxy Documentation](http://www.haproxy.org/)
- [AWS ELB/ALB/NLB Documentation](https://docs.aws.amazon.com/elasticloadbalancing/)
- [Load Balancing Strategies](https://en.wikipedia.org/wiki/Load_balancing_(computing))
