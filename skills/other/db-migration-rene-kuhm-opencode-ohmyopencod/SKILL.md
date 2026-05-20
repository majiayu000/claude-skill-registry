---
description: "Generar y validar migraciones de base de datos. Soporta Prisma, Drizzle, TypeORM y migraciones SQL raw."
user-invocable: true
argument-hint: "[create|validate|rollback] [nombre-migracion]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Database Migration Skill

Eres un experto en migraciones de bases de datos. Tu rol es generar, validar y gestionar migraciones de forma segura.

## Flujo de Trabajo

### 1. Detectar ORM/Herramienta

Primero detecta qué herramienta de base de datos usa el proyecto:

```bash
# Verificar package.json para dependencias
cat package.json | jq '.dependencies, .devDependencies'
```

Soportamos:
- **Prisma**: `prisma/schema.prisma`
- **Drizzle**: `drizzle.config.ts`
- **TypeORM**: `ormconfig.json` o `data-source.ts`
- **Raw SQL**: carpeta `migrations/` o `db/migrations/`

### 2. Comandos por Acción

#### CREATE - Crear nueva migración

**Prisma:**
```bash
npx prisma migrate dev --name <nombre>
```

**Drizzle:**
```bash
npx drizzle-kit generate:pg --name <nombre>
```

**TypeORM:**
```bash
npx typeorm migration:generate src/migrations/<Nombre>
```

**Raw SQL:**
Crear archivo: `migrations/YYYYMMDDHHMMSS_<nombre>.sql`

#### VALIDATE - Validar migraciones pendientes

1. Verificar sintaxis SQL
2. Detectar operaciones destructivas:
   - `DROP TABLE`
   - `DROP COLUMN`
   - `TRUNCATE`
   - `ALTER TABLE ... DROP`
3. Verificar backups antes de destructivas
4. Estimar tiempo de ejecución

#### ROLLBACK - Revertir última migración

**Prisma:**
```bash
npx prisma migrate reset --skip-seed
```

**Drizzle:**
```bash
npx drizzle-kit drop
```

### 3. Mejores Prácticas

#### Siempre:
- Crear backup antes de migraciones destructivas
- Usar transacciones cuando sea posible
- Agregar índices AFTER insertar datos masivos
- Documentar cambios en el schema

#### Nunca:
- Ejecutar migraciones en producción sin validar
- Modificar migraciones ya aplicadas
- Usar `CASCADE` sin entender las implicaciones

### 4. Template de Migración SQL

```sql
-- Migration: <nombre>
-- Created: <fecha>
-- Author: Claude Code Enterprise

-- UP Migration
BEGIN;

-- Cambios aquí
ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT false;
CREATE INDEX idx_users_email_verified ON users(email_verified);

COMMIT;

-- DOWN Migration (para rollback)
-- BEGIN;
-- ALTER TABLE users DROP COLUMN email_verified;
-- COMMIT;
```

### 5. Validaciones de Seguridad

Antes de ejecutar, verificar:

1. **Backup existe**:
```bash
# PostgreSQL
pg_dump -Fc database > backup_$(date +%Y%m%d_%H%M%S).dump
```

2. **No hay conexiones activas** (para DDL pesado):
```sql
SELECT count(*) FROM pg_stat_activity WHERE datname = 'database';
```

3. **Espacio en disco suficiente**:
```bash
df -h
```

## Output Esperado

Después de cada operación, mostrar:

```
✅ Migration Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Migration: add_user_preferences
ORM: Prisma
Action: CREATE
Status: Generated

Files Modified:
- prisma/migrations/20241225_add_user_preferences/migration.sql
- prisma/schema.prisma

⚠️ Review Required:
- Contains ALTER TABLE operation
- Estimated execution time: ~2s

Next Steps:
1. Review the generated migration
2. Run: npx prisma migrate dev
3. Update seed data if needed
```
