---
name: api-design
description: API Design - Princípios RESTful e boas práticas
version: 1.0.0
category: process
triggers:
  - api
  - rest
  - endpoint
  - rota
  - route
  - http
  - request
  - response
  - crud
tools: []
author: liquid-ai
---

# API Design - Princípios RESTful

Esta skill implementa boas práticas para design de APIs RESTful consistentes e intuitivas.

## Princípios Fundamentais

```
┌─────────────────────────────────────────────────────────────┐
│  1. CONSISTÊNCIA - Padrões previsíveis em toda API         │
│  2. SIMPLICIDADE - Fácil de entender e usar                │
│  3. DOCUMENTAÇÃO - Auto-explicativa quando possível        │
│  4. VERSIONAMENTO - Evoluir sem quebrar clientes           │
└─────────────────────────────────────────────────────────────┘
```

## URL Structure

### Naming Convention

```
# ✅ BOM - Substantivos no plural, kebab-case
GET /api/v1/users
GET /api/v1/user-profiles
GET /api/v1/order-items

# ❌ RUIM - Verbos, singular, camelCase
GET /api/v1/getUser
GET /api/v1/user
GET /api/v1/orderItems
```

### Hierarquia de Recursos

```
# Recurso principal
GET /api/v1/users

# Sub-recurso (pertence a user)
GET /api/v1/users/{userId}/orders

# Máximo 2-3 níveis de aninhamento
GET /api/v1/users/{userId}/orders/{orderId}/items

# Se muito profundo, promova a recurso próprio
GET /api/v1/order-items?orderId={orderId}
```

## HTTP Methods

| Method | Uso | Idempotente | Body |
|--------|-----|-------------|------|
| `GET` | Ler recurso(s) | Sim | Não |
| `POST` | Criar recurso | Não | Sim |
| `PUT` | Substituir recurso completo | Sim | Sim |
| `PATCH` | Atualizar parcialmente | Sim* | Sim |
| `DELETE` | Remover recurso | Sim | Não |

### Exemplos CRUD

```bash
# Listar todos os usuários
GET /api/v1/users

# Obter usuário específico
GET /api/v1/users/123

# Criar usuário
POST /api/v1/users
Body: { "name": "João", "email": "joao@email.com" }

# Atualizar usuário (completo)
PUT /api/v1/users/123
Body: { "name": "João Silva", "email": "joao@email.com", "phone": "..." }

# Atualizar usuário (parcial)
PATCH /api/v1/users/123
Body: { "name": "João Silva" }

# Remover usuário
DELETE /api/v1/users/123
```

## Status Codes

### Sucesso (2xx)

| Code | Quando Usar |
|------|-------------|
| `200 OK` | GET/PUT/PATCH bem-sucedido |
| `201 Created` | POST criou recurso |
| `204 No Content` | DELETE bem-sucedido |

### Erro do Cliente (4xx)

| Code | Quando Usar |
|------|-------------|
| `400 Bad Request` | Dados inválidos |
| `401 Unauthorized` | Não autenticado |
| `403 Forbidden` | Autenticado mas sem permissão |
| `404 Not Found` | Recurso não existe |
| `409 Conflict` | Conflito (ex: email duplicado) |
| `422 Unprocessable Entity` | Validação falhou |
| `429 Too Many Requests` | Rate limit excedido |

### Erro do Servidor (5xx)

| Code | Quando Usar |
|------|-------------|
| `500 Internal Server Error` | Erro inesperado |
| `502 Bad Gateway` | Serviço upstream falhou |
| `503 Service Unavailable` | Serviço temporariamente indisponível |

## Request/Response Format

### Request Headers

```http
Content-Type: application/json
Authorization: Bearer <token>
Accept: application/json
Accept-Language: pt-BR
X-Request-ID: uuid-for-tracing
```

### Response Structure (Sucesso)

```json
{
  "data": {
    "id": "123",
    "name": "João",
    "email": "joao@email.com",
    "createdAt": "2025-01-13T10:30:00Z"
  }
}
```

### Response Structure (Lista)

```json
{
  "data": [
    { "id": "1", "name": "João" },
    { "id": "2", "name": "Maria" }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "perPage": 20,
    "totalPages": 5
  }
}
```

### Response Structure (Erro)

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dados inválidos",
    "details": [
      {
        "field": "email",
        "message": "Email inválido"
      }
    ]
  }
}
```

## Paginação

### Query Parameters

```bash
# Offset-based (simples)
GET /api/v1/users?page=2&perPage=20

# Cursor-based (melhor performance)
GET /api/v1/users?cursor=abc123&limit=20
```

### Response com Paginação

```json
{
  "data": [...],
  "meta": {
    "total": 1000,
    "page": 2,
    "perPage": 20
  },
  "links": {
    "self": "/api/v1/users?page=2",
    "first": "/api/v1/users?page=1",
    "prev": "/api/v1/users?page=1",
    "next": "/api/v1/users?page=3",
    "last": "/api/v1/users?page=50"
  }
}
```

## Filtering, Sorting, Search

### Filtros

```bash
# Filtro simples
GET /api/v1/users?status=active

# Múltiplos valores
GET /api/v1/users?status=active,pending

# Operadores
GET /api/v1/orders?total[gte]=100&total[lte]=500
GET /api/v1/users?createdAt[after]=2025-01-01
```

### Ordenação

```bash
# Ascendente
GET /api/v1/users?sort=name

# Descendente
GET /api/v1/users?sort=-createdAt

# Múltiplos campos
GET /api/v1/users?sort=-createdAt,name
```

### Busca

```bash
# Busca simples
GET /api/v1/users?search=joão

# Busca em campo específico
GET /api/v1/users?name[contains]=silva
```

## Versionamento

### Estratégias

| Estratégia | Exemplo | Pros | Cons |
|------------|---------|------|------|
| URL Path | `/api/v1/users` | Explícito, cacheável | URL muda |
| Header | `Accept-Version: 1` | URL limpa | Menos visível |
| Query | `?version=1` | Fácil testar | Pode ser esquecido |

**Recomendação:** URL Path para APIs públicas

### Evolução

```
# Versão atual
GET /api/v1/users

# Nova versão (breaking changes)
GET /api/v2/users

# Manter v1 funcionando por período de deprecação
```

## Autenticação

### Bearer Token (JWT)

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### API Key

```http
X-API-Key: your-api-key-here
```

### OAuth 2.0 Flows

| Flow | Uso |
|------|-----|
| Authorization Code | Web apps com backend |
| PKCE | Mobile/SPA apps |
| Client Credentials | Server-to-server |

## Rate Limiting

### Headers de Resposta

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1673568000
Retry-After: 60
```

### Resposta 429

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Limite de requisições excedido",
    "retryAfter": 60
  }
}
```

## HATEOAS (Links)

```json
{
  "data": {
    "id": "123",
    "name": "João",
    "status": "active"
  },
  "links": {
    "self": "/api/v1/users/123",
    "orders": "/api/v1/users/123/orders",
    "deactivate": "/api/v1/users/123/deactivate"
  }
}
```

## Ações Não-CRUD

### Opção 1: Verbo como Sub-recurso

```bash
# Ações em recurso
POST /api/v1/users/123/activate
POST /api/v1/orders/456/cancel
POST /api/v1/emails/789/send
```

### Opção 2: Campo de Status

```bash
PATCH /api/v1/users/123
Body: { "status": "active" }
```

## Checklist de Design

### Antes de Implementar
- [ ] Recursos identificados como substantivos?
- [ ] Hierarquia de recursos definida?
- [ ] Versionamento planejado?
- [ ] Autenticação definida?

### Durante Implementação
- [ ] Status codes corretos?
- [ ] Validação de input?
- [ ] Error handling consistente?
- [ ] Rate limiting configurado?

### Antes de Publicar
- [ ] Documentação atualizada?
- [ ] Exemplos funcionando?
- [ ] Testes de integração?
- [ ] Monitoring configurado?

## Anti-Patterns

| Anti-Pattern | Problema | Solução |
|--------------|----------|---------|
| Verbos na URL | `/getUsers`, `/createUser` | Use HTTP methods |
| Inconsistência | `/users` vs `/User` | Padronize plural/kebab |
| Expor IDs internos | IDs sequenciais | Use UUIDs ou slugs |
| Retornar HTML em API | Dificulta consumo | Sempre JSON |
| Ignorar erros | Retornar 200 com erro | Status codes corretos |

---

**Esta skill ativa AUTOMATICAMENTE quando:**
- Design de novos endpoints
- Discussão sobre estrutura de API
- Problemas com REST/HTTP
