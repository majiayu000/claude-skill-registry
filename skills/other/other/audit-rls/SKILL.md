---
name: audit-rls
description: |
  Auditer les policies RLS d'une table ou du projet.
  TRIGGERS : audit-rls, vérifier RLS, sécurité DB, check policies, audit sécurité
disable-model-invocation: false
allowed-tools: Read, Bash, Grep
---

# Audit RLS Policies

## Procédure

### 1. Lister les tables SANS RLS

```sql
SELECT schemaname, tablename
FROM pg_tables
WHERE schemaname = 'public'
AND tablename NOT IN (
  SELECT DISTINCT tablename FROM pg_policies
)
ORDER BY tablename;
```

### 2. Vérifier les policies existantes

```sql
SELECT
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual as using_clause,
  with_check
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, cmd;
```

### 3. Valider les règles

| Opération | USING | WITH CHECK | Correct ? |
|-----------|-------|------------|-----------|
| SELECT | ✅ | ❌ | USING seul |
| INSERT | ❌ | ✅ | WITH CHECK seul |
| UPDATE | ✅ | ✅ | Les deux |
| DELETE | ✅ | ❌ | USING seul |

### 4. Vérifier les indexes

```sql
SELECT
  indexname,
  tablename,
  indexdef
FROM pg_indexes
WHERE schemaname = 'public'
AND (
  indexdef LIKE '%user_id%'
  OR indexdef LIKE '%auth.uid%'
)
ORDER BY tablename;
```

### 5. Vérifier les performances

```sql
-- Tables avec RLS mais sans index sur user_id
SELECT t.tablename
FROM pg_tables t
JOIN pg_policies p ON t.tablename = p.tablename
WHERE t.schemaname = 'public'
AND t.tablename NOT IN (
  SELECT tablename FROM pg_indexes
  WHERE indexdef LIKE '%user_id%'
)
GROUP BY t.tablename;
```

## Rapport

Générer un rapport avec :

- ❌ **Critique** : Tables sans RLS
- ⚠️ **Warning** : Policies mal configurées
- ⚠️ **Warning** : Indexes manquants sur colonnes RLS
- ✅ **OK** : Tables conformes
