---
name: prisma_specialist
router_kit: FullStackKit
description: Prisma ORM, schema design, migrations ve type-safe database access.
metadata:
  skillport:
    category: database
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, prisma specialist, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - orm
---

# ◭ Prisma Specialist

> Modern ve tip güvenli veritabanı erişimi ve şema yönetimi.

---

*Prisma Specialist v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Prisma Documentation - Schema Reference](https://www.prisma.io/docs/reference/api-reference/prisma-schema-reference)

### Aşama 1: Schema Modeling
- [ ] **Models**: `schema.prisma` dosyasında tabloları ve ilişkileri (1:1, 1:n, m:n) tanımla.
- [ ] **Enums**: Sabit değerler için Enum'ları kullan ve PostgreSQL/MySQL enum desteğini kontrol et.
- [ ] **Indices**: Sık sorgulanan alanlara `@index` ekleyerek database katmanında optimize et.

### Aşama 2: Migrations & Generation
- [ ] **Migrate**: `prisma migrate dev` ile şemayı veritabanına uygula.
- [ ] **Generate**: `prisma generate` ile tip güvenli Prisma Client'ı oluştur.
- [ ] **Studio**: Veriyi görsel olarak incelemek için `npx prisma studio` başllat.

### Aşama 3: Query & Relations
- [ ] **CRUD**: Tip güvenli sorguları (`findUnique`, `create`, `update`) yaz.
- [ ] **Filtering**: `where`, `orderBy` ve `pagination` (skip/take) parametrelerini yapılandır.
- [ ] **Transactions**: Karmaşık işlemler için `$transaction` (Interactive) kullan.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Şema değişikliği sonrası `npx prisma generate` çalıştırıldı mı? |
| 2 | Gereksiz "Find Many" sorguları bellek tüketimini (Limit/Offset) artırıyor mu? |
| 3 | Veritabanı bağlantı havuzu (Pool size) düzgün ayarlandı mı? |
