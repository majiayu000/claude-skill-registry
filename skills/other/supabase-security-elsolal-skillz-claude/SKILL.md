---
name: supabase-security
description: Audit de sécurité complet pour les projets Supabase. Lance un pentest automatisé qui vérifie RLS, buckets, auth, keys exposées, et génère un rapport avec remediation. Utiliser quand l'utilisateur dit "audit supabase", "sécurité supabase", "vérifier mon supabase", ou veut s'assurer que son backend Supabase est sécurisé.
model: opus
context: fork
agent: Explore
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - Task
  - TaskCreate
  - TaskUpdate
  - TaskList
argument-hint: <url-application> [--skip-auth-test] [--quick]
user-invocable: true
knowledge:
  core:
    - supabase-security/audit-checklist.md
    - supabase-security/severity-matrix.md
  advanced:
    - supabase-security/rls-patterns.md
    - supabase-security/remediation-templates.md
    - supabase-security/edge-functions-security.md
    - supabase-security/realtime-security.md
    - supabase-security/auth-configuration.md
---

# Supabase Security Audit

Audit de sécurité complet pour les applications utilisant Supabase comme backend.

## Activation

> **Checklist de démarrage**
> - [ ] URL de l'application fournie
> - [ ] Confirmation d'autorisation obtenue
> - [ ] Connexion internet disponible

## Rôle & Principes

**Rôle** : Pentester spécialisé Supabase qui audite la sécurité d'une application et produit un rapport actionnable.

**Principes** :
- Test en boîte grise (accès client-side uniquement)
- Evidence-based : chaque finding avec preuve reproductible
- Progressive writes : sauvegarder au fur et à mesure
- Remediation-first : chaque problème avec sa solution

**Règles** :
- ⛔ Ne JAMAIS lancer sans autorisation explicite
- ⛔ Ne JAMAIS stocker de données sensibles non-redactées
- ⛔ Ne JAMAIS modifier les données de production
- ✅ Toujours sauvegarder les preuves immédiatement
- ✅ Toujours proposer la remediation SQL/code
- ✅ Toujours générer des commandes curl reproductibles

---

## Process

### Phase 0 : INITIALISATION

**0.1 Confirmation d'autorisation**

```
╔═══════════════════════════════════════════════════════════════════╗
║  🔐 AUTORISATION REQUISE                                          ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  Cet audit va tester la sécurité de l'application ciblée.        ║
║                                                                   ║
║  Avant de continuer, confirmez que :                              ║
║  • Vous êtes propriétaire de cette application, OU                ║
║  • Vous avez une autorisation écrite pour la tester               ║
║                                                                   ║
║  Tapez "Je confirme être autorisé à tester cette application"    ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

**⏸️ STOP** - Attendre confirmation explicite

**0.2 Création de la structure d'audit**

```bash
# Créer la structure
mkdir -p .supabase-audit/evidence/{01-detection,02-extraction,03-api,04-storage,05-auth,06-functions}

# Initialiser les fichiers
touch .supabase-audit/context.json
touch .supabase-audit/curl-commands.sh
touch .supabase-audit/timeline.md
```

**0.3 Initialiser context.json**

```json
{
  "target_url": "<URL>",
  "started_at": "<ISO_TIMESTAMP>",
  "authorization_confirmed": true,
  "phases_completed": [],
  "supabase": {},
  "findings": []
}
```

**0.4 Initialiser curl-commands.sh**

```bash
#!/bin/bash
# Supabase Security Audit - Commandes Reproductibles
# Target: <URL>
# Date: <DATE>
#
# Usage: Remplacer les variables puis exécuter

SUPABASE_URL=""
ANON_KEY=""

# === Les commandes seront ajoutées au fur et à mesure ===
```

**0.5 Initialiser timeline.md**

```markdown
# Timeline de l'Audit

## <TIMESTAMP> - Audit démarré
- Cible : <URL>
- Autorisation : Confirmée
```

---

### Phase 1 : DETECTION

**Objectif** : Confirmer l'utilisation de Supabase et extraire l'URL du projet.

**1.1 Fetch et analyse du code client**

```bash
# Télécharger la page HTML
curl -s "<TARGET_URL>" -o .supabase-audit/evidence/01-detection/index.html

# Chercher les patterns Supabase
grep -E "(supabase\.co|supabase\.com|createClient|SUPABASE)" .supabase-audit/evidence/01-detection/index.html
```

**1.2 Patterns à détecter**

| Pattern | Type | Exemple |
|---------|------|---------|
| `*.supabase.co` | Domain | `abc123.supabase.co` |
| `NEXT_PUBLIC_SUPABASE_URL` | Env var | Next.js |
| `VITE_SUPABASE_URL` | Env var | Vite |
| `createClient(` | Code | SDK init |
| `/rest/v1/` | Endpoint | PostgREST |
| `/auth/v1/` | Endpoint | GoTrue |

**1.3 Extraire les fichiers JS et analyser**

```bash
# Lister les scripts
grep -oE 'src="[^"]+\.js"' index.html | cut -d'"' -f2

# Pour chaque script, chercher les patterns Supabase
curl -s "<SCRIPT_URL>" | grep -E "(supabase|SUPABASE)"
```

**1.4 Sauvegarder immédiatement**

Mettre à jour `context.json` :
```json
{
  "supabase": {
    "detected": true,
    "project_url": "https://abc123.supabase.co",
    "project_ref": "abc123"
  }
}
```

Log dans `timeline.md` :
```markdown
## <TIMESTAMP> - Detection terminée
- Supabase détecté : ✅
- Project URL : https://abc123.supabase.co
- Evidence : `01-detection/`
```

**Si Supabase non détecté** → Informer l'utilisateur et proposer de fournir l'URL manuellement.

---

### Phase 2 : EXTRACTION DES CREDENTIALS

**Objectif** : Identifier les clés exposées côté client.

**2.1 Extraire l'Anon Key (attendu)**

Pattern JWT Supabase :
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6I...
```

Décoder et vérifier le rôle :
```bash
# Extraire le payload (partie 2 du JWT)
echo "<JWT>" | cut -d'.' -f2 | base64 -d 2>/dev/null
```

Payload attendu pour anon key :
```json
{
  "role": "anon",  // ✅ OK si anon
  "iss": "supabase",
  "ref": "abc123"
}
```

**2.2 Détecter Service Key (CRITIQUE si trouvé)**

```bash
# Chercher dans tous les JS
grep -rE '"role":\s*"service_role"' .supabase-audit/evidence/
```

**🔴 P0 CRITIQUE si trouvé** :
```
SERVICE KEY EXPOSÉE !
- Bypass tous les RLS
- Accès complet à la BDD
- Action immédiate requise : ROTATION
```

**2.3 Détecter DB Connection String**

```bash
grep -rE "postgres://|postgresql://" .supabase-audit/evidence/
```

**🔴 P0 CRITIQUE si trouvé** :
```
CONNECTION STRING EXPOSÉE !
- Accès direct à PostgreSQL
- Bypass complet de Supabase
```

**2.4 Détecter JWT Secrets**

```bash
grep -rE "jwt_secret|JWT_SECRET|supabase_jwt" .supabase-audit/evidence/
```

**2.5 Sauvegarder les findings**

Pour chaque credential trouvé, créer un fichier evidence :
```json
{
  "evidence_id": "EXT-001",
  "timestamp": "<ISO>",
  "type": "anon_key_extraction",
  "severity": "INFO",
  "key_prefix": "eyJhbGciOiJIUzI1...",
  "decoded_role": "anon",
  "location": {
    "file": "/static/js/main.js",
    "line": 42
  }
}
```

Ajouter au `curl-commands.sh` :
```bash
# === EXTRACTION ===
# Clé anon extraite (safe pour client)
ANON_KEY="eyJhbGciOiJIUzI1NiI..."
```

---

### Phase 3 : API AUDIT

**Objectif** : Tester l'exposition des données via PostgREST.

**3.1 Lister les tables exposées**

```bash
curl -s "$SUPABASE_URL/rest/v1/" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ANON_KEY" \
  > .supabase-audit/evidence/03-api/openapi-schema.json
```

Parser le schéma OpenAPI pour extraire les tables.

**3.2 Pour chaque table, tester l'accès anonyme**

```bash
# Test SELECT
curl -s "$SUPABASE_URL/rest/v1/<TABLE>?select=*&limit=5" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ANON_KEY"
```

| Résultat | Signification | Sévérité |
|----------|---------------|----------|
| `[]` vide | RLS bloque | ✅ OK |
| Données retournées | RLS absent ou permissif | 🔴 P0/P1 |
| Erreur 401/403 | Accès bloqué | ✅ OK |

**3.3 Tests de bypass RLS**

**Test 1 : Filter bypass**
```bash
curl -s "$SUPABASE_URL/rest/v1/posts?or=(published.eq.true,published.eq.false)" \
  -H "apikey: $ANON_KEY"
```

**Test 2 : Join exploitation**
```bash
curl -s "$SUPABASE_URL/rest/v1/comments?select=*,posts(*)" \
  -H "apikey: $ANON_KEY"
```

**Test 3 : Insert test (avec rollback)**
```bash
curl -X POST "$SUPABASE_URL/rest/v1/<TABLE>" \
  -H "apikey: $ANON_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"test": "security-audit-delete-me"}'
```

**3.4 Tester les RPC functions**

```bash
# Lister les fonctions exposées (dans le schéma OpenAPI)
# Pour chaque fonction :
curl -X POST "$SUPABASE_URL/rest/v1/rpc/<FUNCTION_NAME>" \
  -H "apikey: $ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**3.5 Classification des findings**

| Table | RLS | Accès Anon | Données sensibles | Sévérité |
|-------|-----|------------|-------------------|----------|
| users | ❌ | SELECT * | emails, noms | 🔴 P0 |
| posts | ✅ | published only | - | ✅ OK |
| orders | ✅ | aucun | - | ✅ OK |

---

### Phase 4 : STORAGE AUDIT

**Objectif** : Vérifier la configuration des buckets de stockage.

**4.1 Lister les buckets**

```bash
curl -s "$SUPABASE_URL/storage/v1/bucket" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ANON_KEY" \
  > .supabase-audit/evidence/04-storage/buckets-list.json
```

**4.2 Pour chaque bucket, tester l'accès**

```bash
# Lister les fichiers
curl -s "$SUPABASE_URL/storage/v1/object/list/<BUCKET>" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ANON_KEY"
```

**4.3 Tester les URLs publiques**

```bash
# Format URL publique
curl -I "$SUPABASE_URL/storage/v1/object/public/<BUCKET>/<FILE>"
```

Si status 200 → Fichier accessible publiquement

**4.4 Classifier les buckets**

| Classification | Critères | Action |
|----------------|----------|--------|
| ✅ Approprié | avatars, images publiques | Aucune |
| 🟡 À revoir | uploads utilisateur, documents | Considérer private |
| 🔴 Critique | backups, exports, .env | Action immédiate |

**4.5 Patterns de fichiers sensibles**

```bash
# P0 - Jamais public
*.sql, *.env*, *backup*, *secret*, *credential*, *export*

# P1 - Généralement privé
*invoice*, *contract*, *passport*, *license*, *.pdf (selon contexte)
```

---

### Phase 5 : AUTH AUDIT

**Objectif** : Vérifier la configuration de l'authentification.

**5.1 Tester la configuration auth**

```bash
curl -s "$SUPABASE_URL/auth/v1/settings" \
  -H "apikey: $ANON_KEY" \
  > .supabase-audit/evidence/05-auth/settings.json
```

**5.2 Vérifier si signup est ouvert**

```bash
curl -X POST "$SUPABASE_URL/auth/v1/signup" \
  -H "apikey: $ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email": "test-probe@security-audit.local", "password": "TestProbe123!"}'
```

| Résultat | Signification |
|----------|---------------|
| 200 + user créé | Signup ouvert |
| 400 "Signups disabled" | Signup fermé ✅ |
| 429 | Rate limited ✅ |

**5.3 Checklist Auth**

| Setting | Recommandé | Check |
|---------|------------|-------|
| Email confirmation | Enabled | |
| Password min length | 8+ | |
| Rate limiting | Enabled | |
| CAPTCHA | Recommandé | |

**5.4 [OPTIONNEL] Test IDOR avec user authentifié**

> ⚠️ Nécessite création d'un user test. Demander consentement.

```
Voulez-vous créer un utilisateur test pour détecter les vulnérabilités IDOR ?
- Email : pentest-<random>@security-audit.local
- Sera supprimé après l'audit (ou manuellement)

[O]ui / [N]on
```

Si oui :
1. Créer l'utilisateur
2. Obtenir le JWT
3. Comparer accès auth vs anon
4. Tester accès cross-user

---

### Phase 6 : REALTIME & FUNCTIONS

**Objectif** : Vérifier les canaux WebSocket et Edge Functions.

**6.1 Edge Functions**

```bash
# Découvrir les functions (si exposées)
curl -s "$SUPABASE_URL/functions/v1/" \
  -H "apikey: $ANON_KEY"
```

Pour chaque function détectée :
```bash
curl -X POST "$SUPABASE_URL/functions/v1/<FUNCTION>" \
  -H "apikey: $ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**6.2 Realtime channels**

Vérifier si des channels sont accessibles sans auth appropriée.

---

### Phase 7 : RAPPORT

**Objectif** : Générer le rapport final avec toutes les findings et remediations.

**7.1 Calculer le Security Score**

```
Score = 100 - (P0 × 25) - (P1 × 10) - (P2 × 5)

Bonus :
+ 10 si RLS sur toutes les tables
+ 10 si auth hardened (email confirm, strong password)
```

| Score | Grade | Description |
|-------|-------|-------------|
| 90-100 | A | Excellent |
| 80-89 | B | Bon, améliorations mineures |
| 70-79 | C | Acceptable, problèmes à traiter |
| 60-69 | D | Faible, problèmes significatifs |
| 0-59 | F | Critique, action immédiate |

**7.2 Générer le rapport**

Créer `docs/security/supabase-audit-YYYY-MM-DD.md` :

```markdown
# Supabase Security Audit Report

**Cible :** <URL>
**Projet :** <PROJECT_REF>.supabase.co
**Date :** <DATE>
**Score :** <SCORE>/100 (Grade: <GRADE>)

---

## Executive Summary

Cet audit a identifié **X vulnérabilités** :
- 🔴 **X P0** (Critiques) - Action immédiate requise
- 🟠 **X P1** (Hautes) - Traiter sous 7 jours
- 🟡 **X P2** (Moyennes) - Traiter sous 30 jours

### Problèmes les plus critiques

1. **[P0-001]** <Titre>
2. **[P0-002]** <Titre>

### Actions immédiates

1. <Action 1>
2. <Action 2>

---

## Findings Critiques (P0)

### P0-001: <Titre>

**Sévérité :** 🔴 Critique
**Composant :** <Composant>
**CVSS :** <Score>

#### Description
<Description du problème>

#### Preuve
```bash
<Commande curl reproductible>
```

#### Impact
- <Impact 1>
- <Impact 2>

#### Remediation

**Immédiat :**
```sql
<Code SQL de fix>
```

**Long terme :**
<Recommandation>

---

## Findings Hautes (P1)
...

## Findings Moyennes (P2)
...

---

## Analyse par Composant

### API (PostgREST)

| Table | RLS | Accès Anon | Status |
|-------|-----|------------|--------|
| ... | ... | ... | ... |

### Storage

| Bucket | Public | Fichiers sensibles | Status |
|--------|--------|-------------------|--------|
| ... | ... | ... | ... |

### Auth

| Setting | Valeur | Recommandé | Status |
|---------|--------|------------|--------|
| ... | ... | ... | ... |

---

## Plan de Remediation

### Phase 1 : Immédiat (Aujourd'hui)
| ID | Action | Priorité |
|----|--------|----------|
| P0-001 | ... | 🔴 |

### Phase 2 : Cette semaine
| ID | Action | Priorité |
|----|--------|----------|
| P1-001 | ... | 🟠 |

### Phase 3 : Ce mois
| ID | Action | Priorité |
|----|--------|----------|
| P2-001 | ... | 🟡 |

---

## Annexe

### Méthodologie

Tests effectués :
- Détection Supabase (patterns client-side)
- Extraction de credentials (keys, JWT)
- API audit (tables, RLS, RPC)
- Storage audit (buckets, fichiers publics)
- Auth audit (config, signup, rate limiting)
- Functions audit (Edge Functions)

### Evidence

Toutes les preuves sont disponibles dans `.supabase-audit/evidence/`

### Commandes de reproduction

Voir `.supabase-audit/curl-commands.sh`

---

*Rapport généré par /supabase-security*
*Skillz-Claude D-EPCT+R Workflow*
```

---

## Output Validation

### Checklist de validation

| Critère | Requis |
|---------|--------|
| Autorisation confirmée | ✅ |
| Supabase détecté | ✅ |
| Evidence sauvegardée progressivement | ✅ |
| Tous les tests exécutés | ✅ |
| Rapport généré | ✅ |
| curl-commands.sh complet | ✅ |
| Remediation pour chaque finding | ✅ |

### Score minimum

**Aucun** - C'est un audit, on rapporte ce qu'on trouve.

---

## Auto-Chain

Après génération du rapport :

```markdown
## 🔗 Prochaine étape

✅ Audit Supabase terminé. Rapport sauvegardé.

Voulez-vous :
→ **[S]** Lancer `/security-auditor` pour un audit code complémentaire ?
→ **[F]** Créer des issues GitHub pour les findings ?
→ **[R]** Relancer l'audit après corrections ?
→ **[N]** Non, terminer

---
```

---

## Transitions

- **Vers `security-auditor`** : "Voulez-vous aussi auditer le code (OWASP Top 10, dépendances) ?"
- **Vers `pm-stories`** : "Créer des issues pour tracker les remediations ?"

---

## Options

| Option | Description |
|--------|-------------|
| `--skip-auth-test` | Ne pas tester création user (IDOR) |
| `--quick` | Audit rapide (detection + extraction + RLS) |
| `--verbose` | Afficher tous les détails pendant l'exécution |

---

## Notes importantes

### Progressive Writes

⚠️ **OBLIGATOIRE** : Sauvegarder les findings AU FUR ET À MESURE.

```
Avant chaque test → Log dans timeline.md
Après chaque découverte → Update context.json
Après chaque requête → Ajouter à curl-commands.sh
```

### Redaction des données

Ne JAMAIS stocker en clair :
- Emails complets → `[REDACTED]@example.com`
- Noms → `[REDACTED]`
- Clés API (sauf préfixe) → `sk_live_[REDACTED]`

### .gitignore

Recommander d'ajouter :
```
.supabase-audit/
```
