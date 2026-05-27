---
name: docs_api
router_kit: ManagementKit
description: OpenAPI/Swagger API documentation ve endpoint belgeleme şablonları.
metadata:
  skillport:
    category: operations
    tags: [accessibility, api integration, backend, browser apis, client-side, components, css3, debugging, deployment, docs api, frameworks, frontend, fullstack, html5, javascript, libraries, node.js, npm, performance optimization, responsive design, seo, state management, testing, typescript, ui/ux, web development]      - docs-code
---

# 🌐 Docs API

> API documentation ve OpenAPI best practices.

---

## 📋 OpenAPI Template

```yaml
openapi: 3.0.3
info:
  title: User API
  version: 1.0.0

paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      properties:
        id: { type: string }
        email: { type: string, format: email }
```

---

## 📝 Endpoint Doc Template

```markdown
## Create User

`POST /api/v1/users`

### Request
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | Valid email |
| password | string | Yes | Min 8 chars |

### Response (201)
{ "success": true, "data": { "id": "...", "email": "..." } }

### Error (400)
{ "success": false, "error": { "code": "VALIDATION_ERROR" } }
```

---

*Docs API v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Redocly OpenAPI Workflow](https://redocly.com/docs/cli/) & [API Handyman](https://apihandyman.io/)

### Aşama 1: Design (Spec First)
- [ ] **Mock**: `prism` veya `stoplight` ile API'yi kodlamadan önce mockla.
- [ ] **Lint**: OpenAPI dosyasını `spectral` ile standartlara (CamelCase, Descriptions vb.) göre denetle.
- [ ] **Structure**: Tek devasa dosya yerine `$ref` kullanarak bileşenlere böl (`components/schemas/User.yaml`).

### Aşama 2: Documentation
- [ ] **Descriptions**: Her endpoint ve parametre için anlamlı açıklama yaz.
- [ ] **Examples**: Başarılı ve hatalı (4xx, 5xx) response örneklerini mutlaka ekle.
- [ ] **Auth**: Security şemalarını (Bearer, OAuth2) net şekilde tanımla.

### Aşama 3: Publication
- [ ] **Generate**: `redoc-cli bundle` veya `swagger-cli` ile statik HTML oluştur.
- [ ] **Version**: API versiyonunu ve değişiklik günlüğünü (Changelog) güncelle.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | `spectral lint openapi.yaml` hatasız geçiyor mu? |
| 2 | Oluşturulan dokümantasyonda "Try it out" çalışıyor mu? |
| 3 | Tüm zorunlu alanlar (`required`) şemada işaretli mi? |
