---
name: deploy-metering
description: |
  Déployer le système de métriques et facturation sur une app cliente Supabase.
  TRIGGERS : metering, facturation, métriques, billing, deploy-metering, tracking tokens, usage metrics
  Déploie les tables, le helper trackTokenUsage, les Edge Functions, le cron et valide le pipeline complet.
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
---

# Deploy Metering — Système de métriques et facturation

Déployer automatiquement le pipeline complet de métriques sur une application Supabase existante, pour que ses données de consommation soient collectées par le hub central et facturées.

## Avant de commencer

### OBLIGATOIRE : Lire le blueprint

Avant toute action, lire **intégralement** la documentation de référence dans le somtech-pack :

```
features/metering-billing/overview.md       → Architecture et décisions
features/metering-billing/database.md       → Tables, RPCs, enums, indexes
features/metering-billing/backend.md        → Helper, patterns d'instrumentation, Edge Functions
features/metering-billing/implementation-guide.md → Guide pas-à-pas complet
```

Si le dossier `features/metering-billing/` n'est pas dans le projet courant, le chercher dans le somtech-pack synchronisé ou demander à l'utilisateur de faire un `somtech_pack_pull.sh`.

## Phase 0 — Analyse du projet

### 0.1 Vérifier les prérequis

```bash
# Vérifier que c'est un projet Supabase
ls supabase/config.toml

# Vérifier les migrations existantes
ls supabase/migrations/

# Vérifier les Edge Functions existantes
ls supabase/functions/
```

### 0.2 Détecter les points d'appel AI

Scanner le projet pour trouver TOUS les appels AI :

```bash
grep -rn "completions.create\|messages.create\|embeddings.create\|chat\.create\|anthropic\.\|openai\." src/ supabase/functions/ lib/ app/ --include="*.ts" --include="*.tsx" --include="*.js"
```

Lister les résultats et les présenter à l'utilisateur pour validation avant de continuer.

### 0.3 Détecter la stack

Identifier si l'app utilise :
- **Deno** (Edge Functions Supabase) → variante Deno du helper
- **Node.js** (Express, Workers, Next.js API routes) → variante Node.js du helper
- **Les deux** → créer les deux variantes

### 0.4 Demander confirmation

Présenter à l'utilisateur :
1. Le nombre de points d'appel AI trouvés
2. La stack détectée (Deno/Node.js)
3. La liste des modules qui seront instrumentés
4. Demander le `BILLING_PROJECT_ID` (ou utiliser le UUID temporaire `00000000-0000-0000-0000-000000000000`)

**Attendre la validation avant de continuer.**

## Phase 1 — Migration base de données

### 1.1 Générer le timestamp

```bash
TIMESTAMP=$(date -u +"%Y%m%d%H%M%S")
echo "Migration: ${TIMESTAMP}_create_metering_tables.sql"
```

### 1.2 Créer la migration

Créer `supabase/migrations/${TIMESTAMP}_create_metering_tables.sql` avec le contenu exact de `database.md` (tables, enum, indexes, RPCs).

**Inclure** :
- Table `ai_token_usage` avec RLS
- Table `usage_metrics_daily` avec contrainte UNIQUE et RLS
- Enum `metric_type_local`
- RPC `aggregate_daily_usage`
- RPC `get_monthly_ai_usage`
- RPC `exec_sql`

### 1.3 Appliquer en local

```bash
supabase db reset
```

### 1.4 Valider

Exécuter les requêtes de validation de `implementation-guide.md` étape 1.4.

## Phase 2 — Instrumenter les appels AI

### 2.1 Créer le helper

Créer `lib/track-token-usage.ts` avec la variante appropriée (Deno ou Node.js) depuis `backend.md`.

Si l'app a des Edge Functions ET du code Node.js, créer :
- `lib/track-token-usage.ts` → Node.js
- `supabase/functions/_shared/track-token-usage.ts` → Deno

### 2.2 Instrumenter chaque point d'appel

Pour CHAQUE point détecté en phase 0.2 :

1. Identifier le pattern (A: OpenAI chat, B: Anthropic, C: Embeddings, D: Streaming)
2. Ajouter l'import du helper
3. Ajouter l'appel `trackTokenUsage()` (SANS await) avec le bon module et modèle
4. **Streaming** : S'assurer que `stream_options: { include_usage: true }` est présent

### 2.3 Convention de nommage

Utiliser les noms de modules standardisés (voir `database.md` section "Convention de nommage des modules").

### 2.4 Valider

Demander à l'utilisateur de faire un appel AI de test, puis vérifier :

```sql
SELECT module, model, input_tokens, output_tokens, created_at
FROM ai_token_usage ORDER BY created_at DESC LIMIT 5;
```

## Phase 3 — Edge Functions

### 3.1 Générer la clé API

```bash
METERING_KEY="mtr_$(openssl rand -hex 32)"
echo "🔑 Clé API metering : ${METERING_KEY}"
echo "⚠️  NOTER CETTE CLÉ — nécessaire pour Orbit"
```

### 3.2 Configurer les secrets

```bash
supabase secrets set METERING_API_KEY="${METERING_KEY}"
supabase secrets set BILLING_PROJECT_ID="<valeur-fournie-ou-uuid-temporaire>"
```

### 3.3 Créer les Edge Functions

Créer les deux fichiers depuis `implementation-guide.md` :
- `supabase/functions/collect-usage-metrics/index.ts`
- `supabase/functions/get-metering-data/index.ts`

### 3.4 Déployer

```bash
supabase functions deploy collect-usage-metrics
supabase functions deploy get-metering-data
```

### 3.5 Tester

```bash
# Test collect
curl -X POST \
  -H "Authorization: Bearer $(supabase status --output json | jq -r '.SERVICE_ROLE_KEY // empty')" \
  "$(supabase status --output json | jq -r '.API_URL // empty')/functions/v1/collect-usage-metrics"

# Test get-metering-data
curl -H "X-Metering-API-Key: ${METERING_KEY}" \
  "$(supabase status --output json | jq -r '.API_URL // empty')/functions/v1/get-metering-data?action=summary"
```

## Phase 4 — Cron

### 4.1 Configurer le Vault

Exécuter via MCP Supabase ou SQL Editor :

```sql
SELECT vault.create_secret('<SUPABASE_URL>', 'supabase_url');
SELECT vault.create_secret('<ANON_KEY>', 'anon_key');
```

> On utilise l'`anon_key` (publishable key) — pas le `service_role_key`. L'Edge Function crée son propre client interne avec `SUPABASE_SERVICE_ROLE_KEY` (auto-injecté). Le JWT sert uniquement à passer la validation d'accès.

### 4.2 Créer le cron job

```sql
SELECT cron.schedule(
  'collect-usage-metrics-daily',
  '0 2 * * *',
  $$
  SELECT net.http_post(
    url := (SELECT decrypted_secret FROM vault.decrypted_secrets WHERE name = 'supabase_url')
           || '/functions/v1/collect-usage-metrics',
    headers := jsonb_build_object(
      'Authorization', 'Bearer ' ||
        (SELECT decrypted_secret FROM vault.decrypted_secrets WHERE name = 'anon_key'),
      'Content-Type', 'application/json'
    ),
    body := '{}'::jsonb
  );
  $$
);
```

### 4.3 Valider

```sql
SELECT jobid, jobname, schedule, active FROM cron.job
WHERE jobname = 'collect-usage-metrics-daily';
```

## Phase 5 — Validation finale

Exécuter la checklist complète de `implementation-guide.md` étape 5.

### Résumé à afficher

```
✅ METERING DÉPLOYÉ
──────────────────
Tables       : ai_token_usage, usage_metrics_daily
RPCs         : aggregate_daily_usage, get_monthly_ai_usage, exec_sql
Helper       : lib/track-token-usage.ts
Points AI    : X points instrumentés
Edge Funcs   : collect-usage-metrics, get-metering-data
Cron         : collect-usage-metrics-daily (2h UTC)
Clé API      : mtr_***

📋 À TRANSMETTRE À L'ÉQUIPE ORBIT :
URL metering : https://<projet>.supabase.co/functions/v1/get-metering-data
Clé API      : mtr_<clé-complète>
```

## Troubleshooting

| Symptôme | Cause | Solution |
|----------|-------|---------|
| `cron.schedule` échoue | `pg_cron` non activé | Dashboard → Extensions |
| `net.http_post` échoue | `pg_net` non activé | Dashboard → Extensions |
| Secrets vault absents | Vault mal configuré | Re-exécuter `vault.create_secret` |
| Edge Function 500 | Env var manquante | `supabase secrets list` |
| Tokens à 0 (streaming) | Manque `stream_options` | Ajouter `stream_options: { include_usage: true }` |
| Métriques à 0 | Pas de données | L'instrumentation n'est pas encore active / pas d'appel AI de test |

## Règles critiques

1. **Ne JAMAIS `await` le `trackTokenUsage()`** — fire-and-forget uniquement
2. **Streaming : TOUJOURS `stream_options: { include_usage: true }`**
3. **Créer la migration via fichier** — pas de `supabase db push --linked`
4. **Tester avec `supabase db reset`** avant de pousser en prod
5. **Stocker les secrets dans le Vault** — jamais en dur dans le SQL du cron
