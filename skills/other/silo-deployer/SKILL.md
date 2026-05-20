---
name: silo-deployer
description: >
  Exécute le déploiement complet d'une silo après sa génération : conteneurs Docker,
  environnement de développement Fly.io, branche Git, et configuration Netlify.
  Transforme les configs générées en infrastructure active avec URLs stables et
  builds automatisés.
---

## Context

Le `/deploy-silo` skill orchestre la phase de **déploiement** qui suit immédiatement `/generate-silo`.

Il prend les configurations générées (docker-compose.yml, fly/*.toml, etc.) et les materialise en infrastructure :
- **Docker** : 7 agents de la silo démarrés et vérifiés
- **Fly.io** : 6 services (pg, rest, auth, kong, storage, studio) déployés avec URLs stables
- **Git** : branche silo créée et poussée
- **Netlify** : configuration ONE-TIME pour branch deploys automatisés

**MCPs utilisées** :
- `somtech-desk` : mise à jour du statut et événements de silo
- `netlify` : configuration des branches et variables d'environnement

## Prérequis

### Configurations
- ✅ `config/silos/{client}-{app}/` existe et contient :
  - `docker-compose.silo-{client}-{app}.yml`
  - `fly/pg.toml`, `fly/rest.toml`, `fly/auth.toml`, `fly/kong.toml`, `fly/storage.toml`, `fly/studio.toml`
  - `netlify.env.silo`

### Secrets (Service Desk MCP)
- `SOMTECH_DESK_API_KEY` : authentification Service Desk
- `NETLIFY_AUTH_TOKEN` : authentification Netlify

### Outils disponibles
- Docker & docker-compose
- `flyctl` (Fly CLI) avec `$FLY_API_TOKEN` configuré
- Git (push/branch)
- `supabase` CLI (database migrations)

## Étapes de déploiement

### Étape 1 : VALIDATE
**Vérifier que tout est prêt avant d'agir**

- ✅ Confirmer que `config/silos/{client}-{app}/` existe et est complet
- ✅ Re-lire la fiche Application via MCP pour données fraîches
- ✅ Présenter un **plan de déploiement** détaillé (7 conteneurs, 6 services Fly, etc.)
- ✅ **Demander confirmation humaine** avant de continuer

*Si pas de confirmation : abort*

### Étape 2 : DOCKER CONTAINERS (7 agents)

```bash
docker compose -f docker-compose.silo-{client}-{app}.yml up -d
```

- Vérifier que chaque conteneur démarre (`docker ps`)
- Tester les health checks
- ⚠️ **Échec partiel** : logger l'erreur, proposer de continuer sans le conteneur défaillant
  - Exemple : "rest-api failed to start → continue avec auth + db + worker"

### Étape 3 : FLY.IO ORGANIZATION + DEV-ENV (6 services)

**Créer l'organisation Fly.io** (une seule fois par app) :

```bash
flyctl orgs create {client}-{app}
```

- Si l'org existe déjà, skip cette sous-étape
- L'org isole la facturation et les accès par client/app

**Déployer les 6 services** dans l'org :

```bash
flyctl apps create devenv-{client}-{app}-{service} --org {client}-{app}
flyctl deploy --config fly/{service}.toml
```

**Après tous les déploiements** :
```bash
supabase db push  # migrations
```

**Collecter** `connection_info` :
- `silo_pg_url` → `postgres://devenv-{c}-{a}-pg.fly.dev:...`
- `silo_anon_key` → depuis service role
- `silo_service_role_key`

⚠️ **Échec** : Détruire les services Fly déjà créés (`flyctl apps destroy devenv-{c}-{a}-{service}`)

**Important** : Les URLs Fly sont STABLES. `devenv-{c}-{a}-kong.fly.dev` ne change jamais après création.

### Étape 4 : GIT BRANCH

```bash
git branch silo/{client}-{app} main
git push origin silo/{client}-{app}
```

- ⚠️ **Si branche existe** : demander confirmation avant overwrite

### Étape 5 : NETLIFY CONFIGURATION (ONE-TIME ONLY)

**CRITIQUE** : Cette étape se fait UNE SEULE FOIS ici. Jamais reconfigurée après.

Via `netlify-project-services` MCP :

```
- Enable branch deploy : silo/{client}-{app}
- Set branch context env vars:
  VITE_SUPABASE_URL = https://devenv-{client}-{app}-kong.fly.dev
  VITE_SUPABASE_ANON_KEY = {anon_key from step 3}
  VITE_APP_ENV = development
  VITE_API_URL = https://devenv-{client}-{app}-rest.fly.dev
```

Via `netlify-deploy-services` MCP :

```
- Trigger first build of silo/{client}-{app}
- Wait for build completion
- Verify deploy succeeded
- Collect silo_preview_url (https://silo-{client}-{app}--{netlify-id}.netlify.app)
```

⚠️ **Échec build** : Logger l'erreur, set silo status = "error", ne pas continuer

### Étape 6 : UPDATE SERVICE DESK

Via MCP `somtech-desk` :

```
update_silo_status(client, app, "active", {
  containers_count: 7,
  docker_status: "running",
  deployment_timestamp: ISO8601
})

log_silo_event(client, app, "provisioned", "silo-manager", {
  configs_applied: [...],
  fly_services: 6,
  silo_branch: "silo/{client}-{app}",
  silo_preview_url: "https://..."
})

applications.update(client, app, {
  silo: {
    silo_preview_url: "https://...",
    silo_deployed_at: ISO8601,
    silo_status: "active",
    silo_docker_status: "running",
    silo_pg_url: "postgres://...",
    silo_anon_key: "..."
  }
})
```

### Étape 7 : FINAL REPORT

Afficher le **résumé de déploiement** :

```
✅ SILO DEPLOYED : {client}-{app}

Docker Containers (7) : ✅
  • postgres, rest-api, auth, kong, storage, studio, worker-queue

Fly.io Services (6) : ✅
  • devenv-{c}-{a}-pg.fly.dev
  • devenv-{c}-{a}-rest.fly.dev
  • devenv-{c}-{a}-auth.fly.dev
  • devenv-{c}-{a}-kong.fly.dev
  • devenv-{c}-{a}-storage.fly.dev
  • devenv-{c}-{a}-studio.fly.dev

Git Branch : ✅
  • silo/{client}-{app}

Netlify Branch Deploy : ✅
  • Preview URL : https://silo-{client}-{app}--xyz.netlify.app

Next Steps:
  1. Create Slack channels : #silo-{client}-{app}, #silo-{client}-{app}-alerts
  2. Share preview URL with client
  3. Notify dev-workers : branch ready for pushes
  4. dev-workers push code → Netlify auto-deploys (NO manual config needed)
```

## Stratégie de gestion des erreurs

| Étape | Échec | Rollback |
|-------|-------|----------|
| Docker | Conteneur X ne démarre pas | Log + skip + continue |
| Fly.io | Déploiement échoue | `flyctl apps destroy devenv-{c}-{a}-*` |
| Git | Branch existe | Demander confirmation avant push force |
| Netlify | Build échoue | Set silo_status = "error", abort |
| Service Desk | MCP timeout | Retry 3x, log pour ops |

**Jamais laisser Service Desk dans un état inconsistant.**

## Périmètre : Qui fait quoi après déploiement

| Rôle | Action | Autorisé ? | Qui ? |
|------|--------|-----------|-------|
| dev-worker | Push code sur silo/{c}-{a} | ✅ | dev-worker (via git) |
| dev-worker | Reconfigurer Netlify | ❌ | **JAMAIS** |
| devops | Démarrer/arrêter la silo | ✅ | devops (via MCP) |
| devops | Reconfigurer Netlify | ❌ | **JAMAIS** |
| silo-deployer | Configurer Netlify | ✅ | **UNE SEULE FOIS** (ici) |
| anyone | Modifier env vars production | ❌ | **Manual process only** |

Les URLs Fly sont stables → env vars Netlify ne bougent jamais après cette étape.

## Références

- `references/deployment-checklist.md` — checklist d'avant-déploiement et étapes opérationnelles
- `references/rollback-procedures.md` — procédures de rollback par étape
