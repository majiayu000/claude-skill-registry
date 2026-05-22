---
name: api-gateway-configuration
description: Configures API gateways for routing, authentication, rate limiting, and request transformation in microservice architectures. Use when setting up Kong, Nginx, AWS API Gateway, or Traefik for centralized API management.
---

# API Gateway Configuration

Design and configure API gateways for microservice architectures.

## Gateway Responsibilities

- Request routing and load balancing
- Authentication and authorization
- Rate limiting and throttling
- Request/response transformation
- Logging and monitoring
- SSL termination

## Kong Configuration (YAML)

```yaml
_format_version: "3.0"

services:
  - name: user-service
    url: http://user-service:3000
    routes:
      - name: user-routes
        paths: ["/api/users"]
    plugins:
      - name: rate-limiting
        config:
          minute: 100
          policy: local
      - name: jwt

  - name: order-service
    url: http://order-service:3000
    routes:
      - name: order-routes
        paths: ["/api/orders"]
```

## Nginx Configuration

```nginx
upstream backend {
    server backend1:3000 weight=5;
    server backend2:3000 weight=5;
    keepalive 32;
}

server {
    listen 443 ssl;

    location /api/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_cache_valid 200 1m;
    }

    location /health {
        return 200 'OK';
    }
}
```

## AWS API Gateway (SAM)

```yaml
Resources:
  ApiGateway:
    Type: AWS::Serverless::Api
    Properties:
      StageName: prod
      Auth:
        DefaultAuthorizer: JWTAuthorizer
        Authorizers:
          JWTAuthorizer:
            JwtConfiguration:
              issuer: !Sub "https://cognito-idp.${AWS::Region}.amazonaws.com/${UserPoolId}"
```

## Best Practices

- Authenticate at gateway level
- Implement global rate limiting
- Enable request logging
- Use health checks for backends
- Apply response caching strategically
- Never expose backend details in errors
- Enforce HTTPS in production
