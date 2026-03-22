---
name: silo-generator
description: >
  Génère l'intégralité de la configuration d'un silo SomTech : docker-compose, services Fly.io,
  constitutions d'agents, et templates d'environnement. Valide les métadonnées d'application
  avant génération. À utiliser après validation initiale du client et avant déploiement.
---

# Skill: Silo Generator

## Contexte

SomTech construit du logiciel personnalisé. Chaque client/application reçoit un **silo** : ensemble
de 7 conteneurs AI agents orchestrés via Docker Compose et déployés sur Fly.io :

- **clientele** : Interface client (gestion compte, communications)
- **dev-orchestrator** : Orchestration des tâches de développement
- **dev-worker-1, dev-worker-2** : Exécution parallèle des tâches
- **security-auditor** : Audit de sécurité continu
- **security-validator** : Validation des changements de sécurité
- **devops** : Infrastructure, logs, monitoring

Le **Service Desk** (MCP Supabase Edge Function) est la source unique de vérité pour les métadonnées
d'application. Ce skill les lit, les valide, et génère tous les fichiers de configuration.

---

## Workflow : 6 Étapes

### Étape 1 : Récupérer les slugs
- Source : argument `--client-slug` et `--app-slug` OU requête `applications.list` via Service Desk MCP
- Valider : format slug (kebab-case, alphanumériques + tirets)

### Étape 2 : Lire la feuille Application
- Via Service Desk MCP : `applications.get(client_slug, app_slug)`
- Extraire métadonnées JSONB complet (10 sections)
- Stocker en mémoire pour les étapes suivantes

### Étape 3 : Valider les métadonnées
Vérifier la complétude de ces 10 sections (voir **Checklist de validation** ci-dessous) :
- ✓ identity
- ✓ repo
- ✓ frontend
- ✓ database
- ✓ stack
- ✓ providers
- ✓ client
- ✓ env_vars_template
- ✓ silo
- ✓ devenv

**Action** : Si validation échoue, afficher les sections manquantes et arrêter.

### Étape 4 : Charger les références
Lire depuis `references/` :
- `architecture.md` → topologie des conteneurs
- `nomenclature.md` → conventions de nommage
- `metadata-schema.json` → schéma JSONB attendu
- `constitution-template.md` → template Markdown pour constitutions
- `devenv-config.yaml` → template Fly.io/environnement

### Étape 5 : Générer les fichiers
Créer dans `config/silos/{client_slug}-{app_slug}/` :
- `docker-compose.silo-{client_slug}-{app_slug}.yml`
- `fly/{pg,rest,auth,kong,storage,studio}.toml`
- `.env.template`
- `constitutions/{clientele,dev-orchestrator,dev-worker,security-auditor,security-validator,devops}.md`
- `slack-channels.json`

### Étape 6 : Présentation pour revue
Afficher résumé génération → lister fichiers créés → proposer prévisualisation ou déploiement.

---

## Fichiers Générés

### docker-compose.silo-{client}-{app}.yml

```yaml
version: '3.8'
services:
  silo-{client}-{app}-clientele:
  silo-{client}-{app}-dev-orchestrator:
  silo-{client}-{app}-dev-worker-1:
  silo-{client}-{app}-dev-worker-2:
  silo-{client}-{app}-security-auditor:
  silo-{client}-{app}-security-validator:
  silo-{client}-{app}-devops:

networks:
  silo-{client}-{app}-net:
```

**Chaque conteneur reçoit** :
- `SILO_CLIENT_SLUG={client_slug}`
- `SILO_APP_SLUG={app_slug}`
- `AGENT_ROLE={role}`
- `SOMTECH_DESK_API_KEY=${SOMTECH_DESK_API_KEY}`

### Fly.io Services (fly/*.toml)

6 services Fly.io, nommés `devenv-{client}-{app}-{service}` :
- `devenv-{client}-{app}-pg` → PostgreSQL (from metadata.database.project_ref)
- `devenv-{client}-{app}-rest` → PostgREST API
- `devenv-{client}-{app}-auth` → Supabase Auth
- `devenv-{client}-{app}-kong` → API Gateway (Kong)
- `devenv-{client}-{app}-storage` → S3-compatible storage
- `devenv-{client}-{app}-studio` → Supabase Studio

**Configuration** :
- Region : `metadata.devenv.fly_region` (défaut : `yul`)
- Org : `metadata.devenv.fly_org` (auto-généré : `{client}-{app}`, ex: `acme-erp`)
- Auto-stop : `metadata.devenv.auto_stop_minutes` (défaut : 30 min)

### .env.template

Énumère TOUS les noms de variables (JAMAIS les valeurs) :
- Section `[supabase]` : SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY
- Section `[auth]` : AUTH_SECRET, OAUTH_GITHUB_ID, etc.
- Section `[frontend]` : API_BASE_URL, ANALYTICS_ID, etc.
- Générées depuis `metadata.env_vars_template`

### Constitutions d'agents (constitutions/*.md)

Chaque agent a sa constitution Markdown incluant :

1. **Rôle & Responsabilités** : Décrire objectifs primaires
2. **MCP Tools autorisés** : Lister depuis matrice d'accès (voir ci-dessous)
3. **Stack technique** : Contexte depuis `metadata.stack`
4. **Conventions de code** : Depuis `metadata.repo.branch_convention`
5. **Règles de sécurité** : Privilege minimum, actions interdites

#### Matrice d'accès MCP

| Agent | somtech-desk | supabase | netlify | Sections autorisées |
|-------|--------------|----------|---------|-------------------|
| clientele | ✓ read | ✗ | ✗ | identity, client_config, silo.slack_channels |
| dev-orchestrator | ✓ read | ✗ | ✗ | identity, repo, stack, silo.containers |
| dev-worker | ✓ read | ✓ read | ✗ | identity, repo, stack, database, providers, env_vars |
| security-auditor | ✓ read | ✓ read | ✗ | ALL (audit-only) |
| security-validator | ✓ read | ✓ read | ✗ | ALL (validation-only) |
| devops | ✓ read | ✓ rw | ✓ debug | ALL |

### slack-channels.json

```json
{
  "client_slug": "{client_slug}",
  "app_slug": "{app_slug}",
  "channels": [
    "#silo-{client}-{app}-general",
    "#silo-{client}-{app}-dev",
    "#silo-{client}-{app}-security",
    "#silo-{client}-{app}-devops"
  ]
}
```

---

## Checklist de Validation

**Toutes ces conditions DOIVENT être vraies avant génération** :

- [ ] **identity** : client_slug + app_slug + client_name présents
- [ ] **repo** : repo_url + default_branch + silo_branch + branch_convention présents
- [ ] **frontend** : provider + site_id + build_command + publish_dir présents
- [ ] **database** : provider + project_ref + project_url + region présents
- [ ] **stack** : frontend_framework + language + auth_method + api_pattern présents
- [ ] **providers** : au moins 1 provider configuré (frontend OU database OU auth)
- [ ] **client** : contacts array non-vide + communication_language présents
- [ ] **env_vars_template** : au moins section `[supabase]` présente
- [ ] **silo** : containers array avec 7 rôles + slack_channels non-vide
- [ ] **devenv** : devenv_enabled = true + fly_org + fly_region présents

**Validation échouée** → Afficher liste des sections/champs manquants, retour à Étape 2.

---

## Références (répertoire `references/`)

- **architecture-silos.md** → Topologie SomTech, diagramme conteneurs, flux communications
- **nomenclature.md** → Conventions slug, noms services, variables d'environnement
- **metadata-schema.md** → Schéma JSONB complet (10 sections, tous les champs)
- **constitution-template.md** → Template Markdown de constitution agent
- **devenv-flyio.md** → Defaults Fly.io, ressources, régions disponibles

---

## Notes d'implémentation

- **Idempotence** : Si fichiers existent, proposer remplacement ou fusion
- **Logging** : Tracer chaque étape (validation → génération → résumé)
- **Erreurs** : Afficher contexte claire et suggestions correctives
- **Français** : Descriptions, messages d'erreur en français ; termes techniques en anglais
- **Sécurité** : JAMAIS de secrets dans .env.template (noms de vars SEULEMENT)

---

## Prochaines étapes après génération

Une fois ce skill exécuté avec succès :

1. **Review** : Équipe SomTech revoit les fichiers générés
2. **Ajustements** : Modifications manuelles si nécessaire
3. **Silo Deployer** : Skill de déploiement vers Fly.io et Docker Hub
4. **Agent Initialization** : Chaque conteneur reçoit sa constitution et commence à fonctionner

