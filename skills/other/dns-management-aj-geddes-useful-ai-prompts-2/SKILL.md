---
name: dns-management
description: Manage DNS records, routing policies, and failover configurations for high availability and disaster recovery.
---

# DNS Management

## Overview

Implement DNS management strategies for traffic routing, failover, geo-routing, and high availability using Route53, Azure DNS, or CloudFlare.

## When to Use

- Domain management and routing
- Failover and disaster recovery
- Geographic load balancing
- Multi-region deployments
- DNS-based traffic management
- CDN integration
- Health check routing
- Zero-downtime migrations

## Implementation Examples

### 1. **AWS Route53 Configuration**

```yaml
# route53-setup.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: route53-config
  namespace: operations
data:
  setup-dns.sh: |
    #!/bin/bash
    set -euo pipefail

    DOMAIN="myapp.com"
    HOSTED_ZONE_ID="Z1234567890ABC"
    PRIMARY_ENDPOINT="myapp-primary.example.com"
    SECONDARY_ENDPOINT="myapp-secondary.example.com"

    echo "Setting up Route53 DNS for $DOMAIN"

    # Create health check for primary
    PRIMARY_HEALTH=$(aws route53 create-health-check \
      --health-check-config '{
        "Type": "HTTPS",
        "ResourcePath": "/health",
        "FullyQualifiedDomainName": "'${PRIMARY_ENDPOINT}'",
        "Port": 443,
        "RequestInterval": 30,
        "FailureThreshold": 3
      }' --query 'HealthCheck.Id' --output text)

    echo "Created health check: $PRIMARY_HEALTH"

    # Create failover record for primary
    aws route53 change-resource-record-sets \
      --hosted-zone-id "$HOSTED_ZONE_ID" \
      --change-batch '{
        "Changes": [{
          "Action": "UPSERT",
          "ResourceRecordSet": {
            "Name": "'$DOMAIN'",
            "Type": "A",
            "TTL": 60,
            "SetIdentifier": "Primary",
            "Failover": "PRIMARY",
            "AliasTarget": {
              "HostedZoneId": "Z35SXDOTRQ7X7K",
              "DNSName": "'${PRIMARY_ENDPOINT}'",
              "EvaluateTargetHealth": true
            },
            "HealthCheckId": "'${PRIMARY_HEALTH}'"
          }
        }]
      }'

    # Create failover record for secondary
    aws route53 change-resource-record-sets \
      --hosted-zone-id "$HOSTED_ZONE_ID" \
      --change-batch '{
        "Changes": [{
          "Action": "UPSERT",
          "ResourceRecordSet": {
            "Name": "'$DOMAIN'",
            "Type": "A",
            "TTL": 60,
            "SetIdentifier": "Secondary",
            "Failover": "SECONDARY",
            "AliasTarget": {
              "HostedZoneId": "Z35SXDOTRQ7X7K",
              "DNSName": "'${SECONDARY_ENDPOINT}'",
              "EvaluateTargetHealth": false
            }
          }
        }]
      }'

    echo "DNS failover configured"

---
# Terraform Route53 configuration
resource "aws_route53_zone" "myapp" {
  name = "myapp.com"

  tags = {
    Name = "myapp-zone"
  }
}

# Health check for primary region
resource "aws_route53_health_check" "primary" {
  ip_address = aws_lb.primary.ip_address
  port       = 443
  type       = "HTTPS"
  resource_path = "/health"

  failure_threshold = 3
  request_interval  = 30

  tags = {
    Name = "primary-health-check"
  }
}

# Primary failover record
resource "aws_route53_record" "primary" {
  zone_id       = aws_route53_zone.myapp.zone_id
  name          = "myapp.com"
  type          = "A"
  ttl           = 60
  set_identifier = "Primary"

  failover_routing_policy {
    type = "PRIMARY"
  }

  alias {
    name                   = aws_lb.primary.dns_name
    zone_id                = aws_lb.primary.zone_id
    evaluate_target_health = true
  }

  health_check_id = aws_route53_health_check.primary.id
}

# Secondary failover record
resource "aws_route53_record" "secondary" {
  zone_id       = aws_route53_zone.myapp.zone_id
  name          = "myapp.com"
  type          = "A"
  ttl           = 60
  set_identifier = "Secondary"

  failover_routing_policy {
    type = "SECONDARY"
  }

  alias {
    name                   = aws_lb.secondary.dns_name
    zone_id                = aws_lb.secondary.zone_id
    evaluate_target_health = false
  }
}

# Weighted routing for canary deployments
resource "aws_route53_record" "canary" {
  zone_id       = aws_route53_zone.myapp.zone_id
  name          = "api.myapp.com"
  type          = "A"
  ttl           = 60
  set_identifier = "Canary"

  weighted_routing_policy {
    weight = 10
  }

  alias {
    name                   = aws_lb.canary.dns_name
    zone_id                = aws_lb.canary.zone_id
    evaluate_target_health = true
  }
}

# Geolocation routing
resource "aws_route53_record" "geo_us" {
  zone_id       = aws_route53_zone.myapp.zone_id
  name          = "myapp.com"
  type          = "A"
  ttl           = 60
  set_identifier = "US"

  geolocation_routing_policy {
    country = "US"
  }

  alias {
    name                   = aws_lb.us_east.dns_name
    zone_id                = aws_lb.us_east.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "geo_eu" {
  zone_id       = aws_route53_zone.myapp.zone_id
  name          = "myapp.com"
  type          = "A"
  ttl           = 60
  set_identifier = "EU"

  geolocation_routing_policy {
    continent = "EU"
  }

  alias {
    name                   = aws_lb.eu_west.dns_name
    zone_id                = aws_lb.eu_west.zone_id
    evaluate_target_health = true
  }
}
```

### 2. **DNS Failover Script**

```bash
#!/bin/bash
# dns-failover.sh - Manage DNS failover

set -euo pipefail

DOMAIN="${1:-myapp.com}"
HOSTED_ZONE_ID="${2:-Z1234567890ABC}"
NEW_PRIMARY="${3:-}"

if [ -z "$NEW_PRIMARY" ]; then
    echo "Usage: $0 <domain> <hosted-zone-id> <new-primary-endpoint>"
    exit 1
fi

echo "Initiating DNS failover for $DOMAIN"

# Get current primary
CURRENT_PRIMARY=$(aws route53 list-resource-record-sets \
    --hosted-zone-id "$HOSTED_ZONE_ID" \
    --query "ResourceRecordSets[?Name=='$DOMAIN.' && SetIdentifier=='Primary'].AliasTarget.DNSName" \
    --output text)

echo "Current primary: $CURRENT_PRIMARY"
echo "New primary: $NEW_PRIMARY"

# Verify new endpoint is healthy
echo "Verifying new endpoint health..."
if ! curl -sf --max-time 5 "https://${NEW_PRIMARY}/health" > /dev/null; then
    echo "ERROR: New endpoint is not healthy"
    exit 1
fi

# Update primary record
aws route53 change-resource-record-sets \
    --hosted-zone-id "$HOSTED_ZONE_ID" \
    --change-batch '{
        "Changes": [{
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": "'$DOMAIN'",
                "Type": "A",
                "TTL": 60,
                "SetIdentifier": "Primary",
                "Failover": "PRIMARY",
                "AliasTarget": {
                    "HostedZoneId": "Z35SXDOTRQ7X7K",
                    "DNSName": "'$NEW_PRIMARY'",
                    "EvaluateTargetHealth": true
                }
            }
        }]
    }'

echo "DNS failover completed: $NEW_PRIMARY is now primary"
```

### 3. **CloudFlare DNS Configuration**

```bash
#!/bin/bash
# cloudflare-dns.sh - CloudFlare DNS management

set -euo pipefail

CF_EMAIL="${CF_EMAIL}"
CF_API_KEY="${CF_API_KEY}"
DOMAIN="${1:-myapp.com}"
ZONE_ID="${2:-}"

# Get zone ID
if [ -z "$ZONE_ID" ]; then
    ZONE_ID=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=$DOMAIN" \
        -H "X-Auth-Email: $CF_EMAIL" \
        -H "X-Auth-Key: $CF_API_KEY" \
        -H "Content-Type: application/json" \
        | jq -r '.result[0].id')
fi

echo "Zone ID: $ZONE_ID"

# Create DNS record
create_record() {
    local type="$1"
    local name="$2"
    local content="$3"
    local ttl="${4:-3600}"

    curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
        -H "X-Auth-Email: $CF_EMAIL" \
        -H "X-Auth-Key: $CF_API_KEY" \
        -H "Content-Type: application/json" \
        --data '{
            "type":"'$type'",
            "name":"'$name'",
            "content":"'$content'",
            "ttl":'$ttl',
            "proxied":true
        }' | jq '.'
}

# List records
list_records() {
    curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
        -H "X-Auth-Email: $CF_EMAIL" \
        -H "X-Auth-Key: $CF_API_KEY" \
        -H "Content-Type: application/json" | jq '.result[] | {id, type, name, content}'
}

list_records
```

### 4. **DNS Monitoring and Validation**

```yaml
# dns-monitoring.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: dns-health-check
  namespace: operations
spec:
  schedule: "*/5 * * * *"  # Every 5 minutes
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: health-check
              image: curlimages/curl:latest
              command:
                - sh
                - -c
                - |
                  DOMAIN="myapp.com"
                  PRIMARY_IP=$(nslookup $DOMAIN | grep "Address:" | tail -1 | awk '{print $2}')

                  echo "Checking DNS resolution for $DOMAIN"
                  echo "Resolved to: $PRIMARY_IP"

                  # Verify connectivity
                  if curl -sf --max-time 10 "https://$PRIMARY_IP/health" > /dev/null 2>&1; then
                    echo "PASS: Primary endpoint is healthy"
                    exit 0
                  else
                    echo "FAIL: Primary endpoint is unreachable"
                    exit 1
                  fi
          restartPolicy: OnFailure
```

## Best Practices

### ✅ DO
- Use health checks with failover
- Set appropriate TTL values
- Implement geolocation routing
- Use weighted routing for canary
- Monitor DNS resolution
- Document DNS changes
- Test failover procedures
- Use DNS DNSSEC

### ❌ DON'T
- Use TTL of 0
- Point to single endpoint
- Forget health checks
- Mix DNS and application failover
- Change DNS during incidents
- Ignore DNS propagation time
- Use generic names
- Skip DNS monitoring

## DNS Routing Policies

- **Simple**: Single resource
- **Weighted**: Distribute by percentage
- **Latency-based**: Route to lowest latency
- **Failover**: Active/passive failover
- **Geolocation**: Route by geography
- **Multi-value**: Multiple resources with health checks

## Resources

- [AWS Route53 Documentation](https://docs.aws.amazon.com/route53/)
- [CloudFlare DNS API](https://api.cloudflare.com/)
- [Azure DNS Documentation](https://docs.microsoft.com/en-us/azure/dns/)
- [DNS Best Practices](https://www.zytrax.com/books/dns/)
