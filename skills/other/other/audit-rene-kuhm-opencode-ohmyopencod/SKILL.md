---
description: "Auditoría completa del proyecto: dependencias, seguridad, performance, código. Genera reporte actionable."
user-invocable: true
argument-hint: "[full|security|deps|performance|code] [--fix]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - WebSearch
---

# Audit Skill

Realiza una auditoría completa del proyecto y genera un reporte con acciones recomendadas.

## Tipos de Auditoría

### 1. FULL - Auditoría Completa

Ejecuta todas las auditorías y genera un reporte consolidado.

```bash
/audit full
/audit  # Default es full
```

### 2. SECURITY - Seguridad

```bash
/audit security
```

**Verifica:**
- Vulnerabilidades en dependencias (`npm audit`)
- Secrets en código (patterns de API keys)
- Headers de seguridad
- OWASP Top 10 issues
- Archivos sensibles expuestos

**Comandos:**
```bash
# NPM audit
pnpm audit --json

# Buscar secrets hardcodeados
grep -rE "(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}" src/

# Buscar TODO/FIXME de seguridad
grep -rE "(TODO|FIXME).*(security|auth|password)" src/
```

### 3. DEPS - Dependencias

```bash
/audit deps
```

**Verifica:**
- Dependencias desactualizadas
- Dependencias no utilizadas
- Dependencias duplicadas
- Licencias incompatibles
- Bundle size impact

**Comandos:**
```bash
# Outdated
pnpm outdated

# Unused dependencies
npx depcheck

# Bundle analysis
npx @next/bundle-analyzer
```

### 4. PERFORMANCE - Rendimiento

```bash
/audit performance
```

**Verifica:**
- Bundle size
- Lighthouse metrics
- N+1 queries
- Memory leaks potenciales
- Imágenes sin optimizar

**Patterns a buscar:**
```typescript
// N+1 queries
/for.*await.*find/

// Re-renders innecesarios
/style=\{\{/
/onClick=\{\(\) =>/

// Imports pesados
/import \* as/
/from 'lodash'/
```

### 5. CODE - Calidad de Código

```bash
/audit code
```

**Verifica:**
- TypeScript strict compliance
- ESLint/Biome violations
- Code coverage
- Complejidad ciclomática
- Code smells

**Comandos:**
```bash
# TypeScript
pnpm tsc --noEmit

# Lint
pnpm biome check .

# Coverage
pnpm vitest run --coverage
```

## Reporte de Auditoría

### Formato de Salida

```markdown
# 🔍 Project Audit Report

**Project:** my-project
**Date:** 2024-12-25
**Version:** 1.0.0

## Executive Summary

| Category | Status | Issues | Critical |
|----------|--------|--------|----------|
| Security | 🟡 | 3 | 1 |
| Dependencies | 🟢 | 2 | 0 |
| Performance | 🟡 | 5 | 0 |
| Code Quality | 🟢 | 1 | 0 |

**Overall Score: 78/100**

---

## 🔴 Critical Issues

### 1. SQL Injection Vulnerability
**File:** `src/services/user.service.ts:42`
**Severity:** Critical
**Description:** Direct string interpolation in SQL query
**Fix:**
```typescript
// Before
const query = `SELECT * FROM users WHERE id = ${id}`;

// After
const query = `SELECT * FROM users WHERE id = $1`;
await db.query(query, [id]);
```

---

## 🟠 High Priority

### 2. Outdated Dependency with Known Vulnerability
**Package:** `axios@0.21.1`
**Vulnerability:** CVE-2023-XXXXX
**Fix:** `pnpm update axios`

---

## 🟡 Medium Priority

### 3. Missing Rate Limiting
**File:** `src/app/api/login/route.ts`
**Recommendation:** Add rate limiting to prevent brute force

---

## 🟢 Low Priority / Suggestions

### 4. Bundle Size Optimization
**Current:** 450KB
**Suggestion:** Use dynamic imports for Chart component

---

## Action Items

| Priority | Action | Owner | Effort |
|----------|--------|-------|--------|
| 🔴 P0 | Fix SQL injection | - | 1h |
| 🟠 P1 | Update axios | - | 15m |
| 🟡 P2 | Add rate limiting | - | 2h |
| 🟢 P3 | Optimize bundle | - | 4h |

---

## Commands to Run

```bash
# Fix vulnerabilities
pnpm audit fix

# Update dependencies
pnpm update

# Run full lint
pnpm biome check --write .
```
```

## Opción --fix

Cuando se usa `--fix`, intenta corregir automáticamente:
- Actualizar dependencias menores
- Correr `pnpm audit fix`
- Aplicar fixes de Biome
- Formatear código

```bash
/audit full --fix
```

## Proceso

1. Detectar tipo de proyecto (Next.js, Node, etc.)
2. Ejecutar checks correspondientes
3. Analizar resultados
4. Clasificar issues por severidad
5. Generar reporte
6. Sugerir comandos de fix
