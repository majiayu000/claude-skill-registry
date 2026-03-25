---
name: project-detect
description: Projeye girdiginde tech stack'i tespit et, uygun skill ve agent'lari aktive et. Kullanim: /project-detect
---

# /project-detect - Otomatik Proje Tespiti

Mevcut dizindeki dosyalari tarayarak projenin tech stack'ini tespit et.

## Adim 1: Dosya Tarama

Su dosyalari kontrol et (paralel):
- package.json (name, dependencies, scripts)
- tsconfig.json
- pyproject.toml / requirements.txt / setup.py
- go.mod
- Cargo.toml
- pom.xml / build.gradle
- manage.py
- docker-compose.yml / Dockerfile
- .github/workflows/
- CLAUDE.md (mevcut proje hafizasi)
- .env.example

## Adim 2: Stack Raporu

```
PROJE TESPITI
=============
Proje: <dizin adi>
Dil: TypeScript / Python / Go / Java / Rust
Framework: Next.js / Django / Spring Boot / Gin / ...
Database: PostgreSQL / MongoDB / SQLite / ...
ORM: Prisma / SQLAlchemy / GORM / JPA / ...
Test: Jest / pytest / go test / JUnit / ...
CI/CD: GitHub Actions / GitLab CI / ...
Container: Docker / Docker Compose / K8s / ...
Monorepo: Evet/Hayir (turborepo, nx, lerna)

Aktif Skill'ler:
  - <skill-1>
  - <skill-2>
  - ...

Aktif Workflow:
  feature: @architect -> @kraken -> @tdd-guide -> @code-reviewer -> @verifier
  bugfix: @sleuth -> @spark -> @verifier
  refactor: @phoenix -> @kraken -> @verifier
```

## Adim 3: CLAUDE.md Kontrol

- Dizinde CLAUDE.md var mi?
- Yoksa: "CLAUDE.md olusturayim mi? (template: ~/.claude/templates/CLAUDE-TEMPLATE.md)"
- Varsa: Oku, proje bilgilerini kontrol et, eksikleri tamamla

## Adim 4: Oneriler

Projeye ozel oneriler sun:
- Eksik test varsa belirt
- Security riski varsa uyar
- Performans iyilestirme firsati varsa soyple
- Kullanilmayan dependency varsa belirt
