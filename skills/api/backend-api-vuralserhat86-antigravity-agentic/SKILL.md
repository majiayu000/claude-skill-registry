---
name: backend-api
description: '> REST API tasarımı ve güvenlik best practices.'
---

---
name: backend_api
router_kit: FullStackKit
description: REST uygulama, validation, security headers, auth patterns. ⚠️ Kod yazarken kullan. API tasarımı/GraphQL için → api-design.
metadata:
  skillport:
    category: development
    tags: [accessibility, api integration, backend, backend api, browser apis, client-side, components, css3, debugging, deployment, frameworks, frontend, fullstack, html5, javascript, libraries, node.js, npm, performance optimization, responsive design, seo, state management, testing, typescript, ui/ux, web development]      - backend-database
---

# 🌐 Backend API

> REST API tasarımı ve güvenlik best practices.

---

## 📋 1. RESTful Endpoints

```
GET    /api/v1/users           # List
GET    /api/v1/users/:id       # Get one
POST   /api/v1/users           # Create
PATCH  /api/v1/users/:id       # Partial update
DELETE /api/v1/users/:id       # Delete
```

### HTTP Status Codes
| Kod | Kullanım |
|-----|----------|
| 200 | GET, PATCH, PUT başarılı |
| 201 | POST Created |
| 204 | DELETE No Content |
| 400 | Validation hatası |
| 401 | Authentication gerekli |
| 403 | Yetki yok |
| 404 | Bulunamadı |
| 429 | Rate limit |

---

## ✅ 2. Input Validation (Zod)

```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(2).max(100),
});

type CreateUserDto = z.infer<typeof CreateUserSchema>;
```

---

## 🔐 3. Güvenlik

### Security Headers
```typescript
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';

app.use(helmet());
app.use(rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
}));
```

### JWT Authentication
```typescript
function authMiddleware(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) return res.status(401).json({ error: 'Token required' });

  const decoded = jwt.verify(token, env.JWT_SECRET);
  req.user = decoded;
  next();
}
```

---

## 📦 4. Response Format

```typescript
interface SuccessResponse<T> {
  success: true;
  data: T;
  meta?: { page, limit, total };
}

interface ErrorResponse {
  success: false;
  error: { code: string; message: string };
}
```

---

## 🔗 İlgili Skill'ler
- `backend-core` - TypeScript, yapı
- `backend-database` - Repository, caching

---

- `backend-database` - Repository, caching

---

*Backend API v1.2 - Verified*

## 🔄 Workflow

> **Kaynak:** [Node.js Best Practices (Goldberg)](https://github.com/goldbergyoni/nodebestpractices#-2-metrics-and-logging)

### Aşama 1: Interface Design (Contract First)
- [ ] **Specs**: OpenAPI (Swagger) veya Zod şeması ile input/output tanımla.
- [ ] **Roadmap**: Endpoint listesini ve HTTP metodlarını belirle.

### Aşama 2: Layered Implementation
- [ ] **Controller**: Sadece HTTP request/response yönet, business logic yazma.
- [ ] **Service**: Tüm iş mantığını buraya koy (Reusable).
- [ ] **DAL**: Veritabanı erişimini soyutla.

### Aşama 3: Security & Hardening
- [ ] **Middleware**: Helmet, Rate Limiter ve CORS ayarlarını yap.
- [ ] **Validation**: Gelen her veriyi (Body, Query, Params) Zod ile doğrula.
- [ ] **Error**: Global Error Handler kur ve user-friendly mesaj dön.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | API dokümantasyonu koddan önce mi hazırlandı? |
| 2 | Controller dosyasında hiç SQL/ORM kodu var mı? (Olmamalı) |
| 3 | 500 hatası dönünce stack trace gizleniyor mu? |
