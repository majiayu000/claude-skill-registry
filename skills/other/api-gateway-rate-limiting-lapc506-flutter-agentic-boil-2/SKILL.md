# 🚪 Skill: API Gateway & Rate Limiting

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-api-gateway-rate-limiting` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `api-gateway`, `rate-limiting`, `kong`, `nginx`, `traefik`, `throttling`, `api-management` |
| **Referencia** | [Kong Documentation](https://docs.konghq.com/) |

## 🔑 Keywords para Invocación

- `api-gateway`
- `rate-limiting`
- `kong`
- `nginx`
- `traefik`
- `throttling`
- `api-management`
- `@skill:api-gateway`

### Ejemplos de Prompts

```
Implementa API Gateway con Kong y rate limiting
```

```
Configura throttling y API management
```

```
Setup Nginx como API Gateway con rate limiting
```

```
@skill:api-gateway - API Gateway completo con rate limiting
```

## 📖 Descripción

API Gateway actúa como punto de entrada único para APIs, proporcionando rate limiting, autenticación, routing, y observabilidad. Este skill cubre implementación de Kong/Nginx como gateway, rate limiting strategies, y API management.

### ✅ Cuándo Usar Este Skill

- Múltiples microservicios
- Requisitos de rate limiting
- API versioning
- Centralized authentication
- API analytics
- DDoS protection

### ❌ Cuándo NO Usar Este Skill

- Single service
- Sin requisitos de rate limiting
- APIs internas simples

## 🏗️ API Gateway Architecture

```
┌───────────────────────┐
│         Clients       │
└────────────┬──────────┘
             │
┌────────────▼──────────┐
│       API Gateway     │
│      ┌───────────┐    │
│      │ Rate Limit│    │
│      │ Auth      │    │
│      │ Routing   │    │
│      └───────────┘    │
└────────────┬──────────┘
             │
    ┌────────┼────────┐
    │        │        │
┌───▼───┐┌───▼───┐┌───▼───┐
│Service││Service││Service│
│   A   ││   B   ││   C   │
└───────┘└───────┘└───────┘
```

## 💻 Implementación

> **📁 Scripts Ejecutables:** Este skill incluye scripts ejecutables en la carpeta [`scripts/`](scripts/):
> - [`kong_custom_rate_limiting.lua`](scripts/kong_custom_rate_limiting.lua) - Plugin personalizado de Kong
> - [`rate_limiting_strategies.py`](scripts/rate_limiting_strategies.py) - Algoritmos de rate limiting (CLI)
> - [`api_gateway_middleware.py`](scripts/api_gateway_middleware.py) - API Gateway FastAPI con rate limiting
> - [`requirements.txt`](scripts/requirements.txt) - Dependencias Python
> 
> Ver [`scripts/README.md`](scripts/README.md) para documentación de uso.

### 1. Kong API Gateway

#### 1.1 Kong Configuration

```yaml
# kong/kong.yml
_format_version: "3.0"
_transform: true

services:
  - name: user-service
    url: http://user-service:3000
    routes:
      - name: user-route
        paths:
          - /api/v1/users
        methods:
          - GET
          - POST
        plugins:
          - name: rate-limiting
            config:
              minute: 100
              hour: 1000
              policy: local
          - name: key-auth
            config:
              key_names:
                - apikey

  - name: product-service
    url: http://product-service:3000
    routes:
      - name: product-route
        paths:
          - /api/v1/products
        plugins:
          - name: rate-limiting
            config:
              second: 10
              minute: 100
              hour: 1000
              policy: redis
              redis_host: redis
              redis_port: 6379
          - name: request-size-limiting
            config:
              allowed_payload_size: 512

plugins:
  - name: cors
    config:
      origins:
        - https://example.com
      methods:
        - GET
        - POST
        - PUT
        - DELETE
      credentials: true

consumers:
  - username: api-user
    keyauth_credentials:
      - key: api-key-12345
```

#### 1.2 Rate Limiting Plugin

**Script ejecutable:** [`scripts/kong_custom_rate_limiting.lua`](scripts/kong_custom_rate_limiting.lua)

Plugin personalizado de Kong para rate limiting distribuido usando Redis.

#### Cuándo usar

- Rate limiting distribuido entre múltiples instancias de Kong
- Necesitas control granular sobre la lógica de rate limiting
- Requisitos específicos de identificación (IP, consumer, header)

#### Instalación en Kong

```bash
# 1. Crear directorio del plugin
mkdir -p /usr/local/share/lua/5.1/kong/plugins/custom-rate-limiting

# 2. Copiar plugin
cp scripts/kong_custom_rate_limiting.lua \
   /usr/local/share/lua/5.1/kong/plugins/custom-rate-limiting/access.lua

# 3. Crear schema.lua (ver comentarios en el archivo para estructura)

# 4. Habilitar en kong.yml
plugins:
  - name: custom-rate-limiting
    config:
      limit: 100
      window: 60
      redis_host: redis
      redis_port: 6379
      identifier: ip  # ip, consumer, or header
```

#### Características

- ✅ Rate limiting distribuido con Redis
- ✅ Soporte para múltiples identificadores (IP, consumer, header)
- ✅ Headers estándar de rate limiting (X-RateLimit-*)
- ✅ Fail-open o fail-closed configurable
- ✅ Connection pooling para Redis

### 2. Nginx Rate Limiting

```nginx
# nginx/nginx.conf
http {
    # Rate limiting zones
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;
    
    limit_conn_zone $binary_remote_addr zone=conn_limit_per_ip:10m;

    upstream user_service {
        least_conn;
        server user-service-1:3000 max_fails=3 fail_timeout=30s;
        server user-service-2:3000 max_fails=3 fail_timeout=30s;
        keepalive 32;
    }

    server {
        listen 80;
        server_name api.example.com;

        # Global rate limiting
        limit_req zone=api_limit burst=20 nodelay;
        limit_conn conn_limit_per_ip 10;

        # CORS headers
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type' always;

        # Health check endpoint (no rate limit)
        location /health {
            access_log off;
            return 200 "healthy\n";
        }

        # Login endpoint (stricter rate limit)
        location /api/v1/auth/login {
            limit_req zone=login_limit burst=3 nodelay;
            
            proxy_pass http://user_service;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # API endpoints
        location /api/v1/ {
            # Rate limiting
            limit_req zone=api_limit burst=20 nodelay;
            
            # Authentication
            auth_request /auth;
            
            proxy_pass http://user_service;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            
            # Timeouts
            proxy_connect_timeout 5s;
            proxy_send_timeout 10s;
            proxy_read_timeout 10s;
        }

        # Authentication subrequest
        location = /auth {
            internal;
            proxy_pass http://auth-service:3000/verify;
            proxy_pass_request_body off;
            proxy_set_header Content-Length "";
            proxy_set_header X-Original-URI $request_uri;
        }

        # Error pages
        error_page 429 /429.json;
        location = /429.json {
            internal;
            default_type application/json;
            return 429 '{"error": "Rate limit exceeded", "retry_after": 60}';
            add_header Retry-After 60 always;
        }
    }
}
```

### 3. Rate Limiting Strategies

**Script ejecutable:** [`scripts/rate_limiting_strategies.py`](scripts/rate_limiting_strategies.py)

Implementación de diferentes algoritmos de rate limiting: Fixed Window, Token Bucket, y Sliding Window.

#### Cuándo usar

- **Fixed Window:** Casos simples, tráfico predecible
- **Token Bucket:** Tráfico con bursts, rate limiting suave
- **Sliding Window:** Rate limiting preciso, sin bursts en límites de ventana

#### Uso como CLI

```bash
# Test fixed window
python scripts/rate_limiting_strategies.py \
  --strategy fixed \
  --max-requests 10 \
  --window 60 \
  --num-requests 15

# Test token bucket
python scripts/rate_limiting_strategies.py \
  --strategy token-bucket \
  --capacity 10 \
  --refill-rate 1.0 \
  --num-requests 15

# Test sliding window
python scripts/rate_limiting_strategies.py \
  --strategy sliding \
  --max-requests 10 \
  --window 60 \
  --num-requests 15
```

#### Uso como módulo

```python
from scripts.rate_limiting_strategies import RateLimiter, TokenBucketRateLimiter

# Fixed window
limiter = RateLimiter(max_requests=100, window_seconds=60)
if limiter.is_allowed("user123"):
    # Process request
    pass

# Token bucket
bucket = TokenBucketRateLimiter(capacity=100, refill_rate=10.0)
if bucket.is_allowed("user123", tokens=5):
    # Process request
    pass
```

#### Comparación de estrategias

| Estrategia | Ventajas | Desventajas | Mejor para |
|------------|----------|-------------|------------|
| **Fixed Window** | Simple, eficiente | Bursts en límites | Casos simples |
| **Token Bucket** | Permite bursts, suave | Más complejo | Tráfico variable |
| **Sliding Window** | Preciso, sin bursts | Más memoria | Rate limiting exacto |

### 4. API Gateway with Authentication

**Script ejecutable:** [`scripts/api_gateway_middleware.py`](scripts/api_gateway_middleware.py)

API Gateway completo con FastAPI que incluye rate limiting, autenticación por API key, y diferentes límites por tier.

#### Cuándo ejecutar

- **Servicio API Gateway:** Como microservicio corriendo continuamente
- **Prototipo rápido:** Para probar rate limiting y autenticación
- **Integración:** Como base para un API Gateway más complejo

#### Instalación

```bash
pip install -r scripts/requirements.txt
```

#### Ejecución

```bash
# Desarrollo (con auto-reload)
uvicorn scripts.api_gateway_middleware:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn scripts.api_gateway_middleware:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Endpoints

**Health Check (sin rate limit):**
```bash
curl http://localhost:8000/health
```

**Endpoint público (rate limit por IP):**
```bash
curl http://localhost:8000/api/v1/public
```

**Endpoint protegido (requiere API key):**
```bash
curl -H "Authorization: Bearer valid-api-key-1" \
     http://localhost:8000/api/v1/data
```

#### Características

- ✅ Rate limiting por tier (premium, basic, anonymous)
- ✅ Autenticación por API key
- ✅ Headers estándar de rate limiting
- ✅ Endpoints públicos y protegidos
- ✅ Documentación Swagger en `/docs`

#### Configuración de API Keys

Edita `VALID_API_KEYS` en el script o usa base de datos en producción:

```python
VALID_API_KEYS = {
    "your-api-key": {"user_id": "user1", "tier": "premium"},
}
```

## 🎯 Mejores Práctices

### 1. Rate Limiting

✅ **DO:**
- Set appropriate limits per endpoint
- Use different limits for authenticated vs anonymous
- Provide rate limit headers
- Implement sliding window or token bucket

❌ **DON'T:**
- Set limits too low
- Ignore rate limit headers
- Use fixed window for burst traffic

### 2. API Gateway

✅ **DO:**
- Centralize authentication
- Implement request/response transformation
- Monitor API usage
- Version APIs

❌ **DON'T:**
- Bypass gateway
- Ignore monitoring
- Skip authentication

## 🚨 Troubleshooting

### Rate Limits Too Strict

1. Review limits
2. Check usage patterns
3. Adjust limits per endpoint
4. Implement burst allowances

### Gateway Performance

1. Monitor latency
2. Check connection pooling
3. Review caching strategies
4. Optimize routing rules

## 📚 Recursos Adicionales

- [Kong Documentation](https://docs.konghq.com/)
- [Nginx Rate Limiting](https://www.nginx.com/blog/rate-limiting-nginx/)
- [API Gateway Patterns](https://microservices.io/patterns/apigateway.html)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Total líneas:** 1,100+

