---
name: TaxasGE Project Orchestrator
description: Orchestre cycle de vie modules (planification, exécution, finalisation), génère rapports professionnels, met à jour RAPPORT_GENERAL
version: 2.0.0
---

# TaxasGE Project Orchestrator Skill

## Overview

Ce skill **orchestre le cycle de vie complet d'un module** TaxasGE, de la planification initiale jusqu'à la finalisation. Il coordonne les agents de développement, génère les rapports professionnels selon les templates standardisés, et maintient le RAPPORT_GENERAL à jour.

**Principe fondamental** : L'Orchestrator ne code pas, il coordonne et documente.

---

## When to Use This Skill

Claude invoquera automatiquement ce skill quand vous dites :
- "Démarre module {X}"
- "Planifie module {X}"
- "Finalise module {X}"
- "Clôture module {X}"
- "Mise à jour RAPPORT_GENERAL"

---

## Core Responsibilities

### 1. Planification Module (Début)

**Quand** : Avant première tâche du module

**Actions** :
- Lit définition module depuis `.claude/.agent/Tasks/PHASE_X.md`
- Analyse scope (backend + frontend)
- Identifie dépendances
- Génère `RAPPORT_PLANIFICATION_MODULE_XX.md`

**Template** : `.github/docs-internal/ias/STRUCTURE_DOCUMENTATION.md` Template 1

### 2. Suivi Quotidien

**Quand** : Fin de chaque journée de travail

**Actions** :
- Agrège progression tâches
- Met à jour métriques globales
- Met à jour `RAPPORT_GENERAL.md`

### 3. Finalisation Module (Fin)

**Quand** : Après validation dernière tâche du module

**Actions** :
- Agrège tous rapports tâches du module
- Calcule métriques finales module
- Génère `RAPPORT_MODULE_XX.md`
- Génère `RAPPORT_ORCHESTRATION_MODULE_XX.md`
- Met à jour `RAPPORT_GENERAL.md`

**Templates** : `.github/docs-internal/ias/STRUCTURE_DOCUMENTATION.md` Template 2 & 3

---

## Workflow Complet

### PHASE 1 : PLANIFICATION MODULE

#### Étape 1.1 : Lire Définition Module

**Source** : `.claude/.agent/Tasks/PHASE_X.md`

**Extraire** :
```markdown
- Nom module
- Objectif principal
- Nombre tâches (ex: TASK-P2-001 à TASK-P2-025)
- Durée estimée
- Dépendances (modules précédents requis)
- Endpoints backend à implémenter
- Pages frontend à créer
- Tests requis
```

**Exemple** :
```markdown
Lecture de `.claude/.agent/Tasks/PHASE_2.md` :

Module : 02 - Core Backend (Services fiscaux)
Tâches : TASK-P2-001 à TASK-P2-025 (25 tâches)
Durée : 6 semaines
Dépendances : Phase 0 (Setup) complétée
Backend : 32 endpoints
Frontend : 8 pages
Tests : Coverage >85%
```

---

#### Étape 1.2 : Analyser État Actuel (Baseline)

**Vérifications** :
```bash
# Backend existant
ls -la packages/backend/app/api/v1/
ls -la packages/backend/app/services/
ls -la packages/backend/app/database/repositories/

# Frontend existant
ls -la packages/web/src/app/(dashboard)/
ls -la packages/web/src/components/

# Tests existants
ls -la packages/backend/tests/
ls -la packages/web/tests/
```

**Calculer complétude** :
```markdown
Backend :
- Fichiers existants : 5/32 endpoints (15%)
- Services existants : 2/8 services (25%)

Frontend :
- Pages existantes : 1/8 pages (12%)
- Composants existants : 3/25 composants (12%)
```

---

#### Étape 1.3 : Identifier Dépendances

**Vérifier modules précédents** :
```markdown
Lecture `.github/docs-internal/ias/RAPPORT_GENERAL.md` :

Module 00 (Setup) : ✅ 100% - Validé
Module 01 (Auth) : ⚪ 70% - En Cours
Module 02 (Core Backend) : ⚪ 0% - En attente

Dépendances OK : Module 02 peut démarrer ✅
```

**Vérifier dépendances techniques** :
- Base données tables créées ?
- Variables environnement configurées ?
- Services externes accessibles (BANGE, OCR) ?

---

#### Étape 1.4 : Générer Rapport Planification

**Template** : `.github/docs-internal/ias/STRUCTURE_DOCUMENTATION.md` Template 1 (lignes 104-315)

**Destination** : `.github/docs-internal/ias/03_PHASES/MODULE_0X_NOM/RAPPORT_PLANIFICATION_MODULE_0X.md`

**Contenu** :
```markdown
# RAPPORT DE PLANIFICATION - MODULE 0X : NOM

**Module :** 0X - NOM_COMPLET
**Date :** 2025-10-31
**Version :** 1.0
**Auteur :** Claude Code
**Validé par :** [Vide jusqu'à validation]
**Statut :** 🟡 DRAFT

---

## 🎯 OBJECTIFS MODULE

### Objectif Principal
[Extrait de PHASE_X.md]

### Objectifs Secondaires
1. [Objectif mesurable 1]
2. [Objectif mesurable 2]
3. [Objectif mesurable 3]

---

## 📊 ÉTAT ACTUEL (Baseline)

### Backend
**Fichiers existants :**
- app/api/v1/auth.py : Endpoints auth (100%)
- app/api/v1/declarations.py : Endpoints déclarations (15%)

**Complétude estimée :** 15%

### Frontend
**Pages existantes :**
- app/(dashboard)/auth/login/page.tsx : Page login (100%)
- app/(dashboard)/declarations/page.tsx : Liste déclarations (50%)

**Complétude estimée :** 12%

---

## 🎯 SCOPE PRÉCIS

### Backend

#### Endpoints à Implémenter
| Endpoint | Méthode | Priorité | Existe? | Estimé (heures) |
|----------|---------|----------|---------|-----------------|
| /api/v1/declarations/ | POST | CRITIQUE | ❌ | 4h |
| /api/v1/declarations/{id} | GET | HAUTE | ⚠️ 50% | 2h |
| /api/v1/declarations/{id} | PUT | HAUTE | ❌ | 3h |
| /api/v1/declarations/{id} | DELETE | MOYENNE | ❌ | 2h |
| ... | ... | ... | ... | ... |

**Total Backend :** 32 endpoints, 120 heures

#### Services à Créer/Modifier
- declaration_service.py : Logique métier déclarations (16h)
- calculation_service.py : Calculs fiscaux (24h)
- notification_service.py : Notifications (8h)

#### Repositories à Créer/Modifier
- declaration_repository.py : CRUD déclarations (12h)
- tax_calculation_repository.py : Requêtes calculs (8h)

### Frontend

#### Pages à Créer
| Page | Route | Composants | Estimé (heures) |
|------|-------|------------|-----------------|
| Liste déclarations | /declarations | 5 | 8h |
| Création déclaration | /declarations/new | 12 | 16h |
| Détail déclaration | /declarations/[id] | 8 | 12h |
| ... | ... | ... | ... |

**Total Frontend :** 8 pages, 80 heures

#### Services API à Créer
- declarations-api.ts : Client API déclarations
- calculations-api.ts : Client API calculs

#### Stores à Créer
- declarations-store.ts : State management déclarations
- notifications-store.ts : State notifications

---

## 🧪 STRATÉGIE TESTS

### Tests Backend
**Framework :** pytest

**Tests à écrire :**
1. **Services :**
   - test_declaration_service.py : 25 tests
   - test_calculation_service.py : 18 tests
   - Target coverage : 85%

2. **Endpoints :**
   - test_declarations_endpoints.py : 32 tests
   - Target coverage : 90%

3. **Repositories :**
   - test_declaration_repository.py : 15 tests
   - Target coverage : 90%

**Total tests backend :** 90 tests

### Tests Frontend
**Framework :** Jest + Playwright

**Tests à écrire :**
1. **Unitaires (Jest) :**
   - declaration-form.test.tsx : 15 tests
   - declaration-list.test.tsx : 12 tests

2. **Intégration (Jest) :**
   - declarations-api.test.ts : 10 tests

3. **E2E (Playwright) :**
   - declaration-flow.spec.ts : 8 scénarios

**Total tests frontend :** 45 tests

---

## ⏱️ PLANNING DÉTAILLÉ

### Semaine 1-2 : Backend Core (TASK-P2-001 à P2-010)
**Tâches :**
- [ ] TASK-P2-001 : Endpoints déclarations CRUD
- [ ] TASK-P2-002 : Service déclarations
- [ ] TASK-P2-003 : Repository déclarations
- [ ] TASK-P2-004 : Tests déclarations
- [ ] TASK-P2-005 : Endpoints calculs
- [ ] TASK-P2-006 : Service calculs
- [ ] TASK-P2-007 : Tests calculs
- [ ] TASK-P2-008 : Integration tests
- [ ] TASK-P2-009 : Documentation Swagger
- [ ] TASK-P2-010 : Déploiement staging backend

**Livrable :** Backend fonctionnel, tests >85%

### Semaine 3-4 : Frontend Core (TASK-P2-011 à P2-020)
**Tâches :**
- [ ] TASK-P2-011 : Page liste déclarations
- [ ] TASK-P2-012 : Page création déclaration
- [ ] TASK-P2-013 : Page détail déclaration
- [ ] TASK-P2-014 : Composants formulaires
- [ ] TASK-P2-015 : API client
- [ ] TASK-P2-016 : Store state
- [ ] TASK-P2-017 : Tests unitaires
- [ ] TASK-P2-018 : Tests E2E
- [ ] TASK-P2-019 : Responsive design
- [ ] TASK-P2-020 : Déploiement staging frontend

**Livrable :** Frontend fonctionnel, Lighthouse >90

### Semaine 5 : Intégration (TASK-P2-021 à P2-023)
**Tâches :**
- [ ] TASK-P2-021 : Tests intégration backend-frontend
- [ ] TASK-P2-022 : Fix bugs intégration
- [ ] TASK-P2-023 : Smoke tests staging

**Livrable :** Flow complet fonctionne end-to-end

### Semaine 6 : Finalisation (TASK-P2-024 à P2-025)
**Tâches :**
- [ ] TASK-P2-024 : Documentation complète
- [ ] TASK-P2-025 : Validation finale Go/No-Go module

**Livrable :** Module prêt production

---

## 📏 CRITÈRES ACCEPTATION

### Backend
- [ ] 32/32 endpoints implémentés
- [ ] Tests coverage >85%
- [ ] 0 erreurs flake8/mypy
- [ ] Documentation Swagger complète
- [ ] Performance : P95 latency <500ms

### Frontend
- [ ] 8/8 pages fonctionnelles
- [ ] Tests E2E passent (100%)
- [ ] Lighthouse score >90
- [ ] Responsive mobile/tablet/desktop
- [ ] Accessibilité WCAG AA

### Intégration
- [ ] Flow déclaration complet fonctionne
- [ ] Gestion erreurs testée
- [ ] CORS configuré
- [ ] Authentication/Authorization OK

---

## 🚨 RISQUES IDENTIFIÉS

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Complexité calculs fiscaux | Élevée | Critique | Consultation expert fiscal + tests exhaustifs |
| Dépendance API BANGE | Moyenne | Élevé | Mock API pour dev + tests fallback |
| Performance calculs lourds | Moyenne | Élevé | Cache Redis + optimisation queries |

---

## 📊 MÉTRIQUES CIBLES

| Métrique | Baseline | Cible | Mesure |
|----------|----------|-------|--------|
| Coverage Backend | 0% | 85% | pytest --cov |
| Coverage Frontend | 0% | 75% | jest --coverage |
| Build Time Backend | N/A | <120s | CI logs |
| Build Time Frontend | N/A | <180s | CI logs |
| Test Execution | N/A | <90s | CI logs |

---

## ✅ VALIDATION

**Critères Go/No-Go :**
- [ ] Planning approuvé par chef de projet
- [ ] Ressources disponibles (agents + temps)
- [ ] Dépendances modules précédents OK (Phase 0, Module 1)
- [ ] Environnement dev/staging fonctionnel
- [ ] Base données tables créées
- [ ] Services externes accessibles

**Signatures :**
- **Planifié par :** Claude Code | Date : 2025-10-31
- **Approuvé par :** [Ton nom] | Date : ___________
```

**Actions après génération** :
```bash
# Commit rapport planification
git add .github/docs-internal/ias/03_PHASES/MODULE_0X_NOM/RAPPORT_PLANIFICATION_MODULE_0X.md
git commit -m "docs(planning): Add MODULE_0X planning report"
git push origin $(git branch --show-current)

echo "✅ Rapport planification généré"
echo "📊 MODULE_0X peut démarrer après validation utilisateur"
```

---

### PHASE 2 : SUIVI QUOTIDIEN

#### Étape 2.1 : Agréger Progression Tâches

**Source** : `.claude/.agent/Reports/PHASE_X/TASK_PX_*.md`

**Calculer** :
```markdown
Lecture tous rapports tâches :
- Tâches complétées : 15/25 (60%)
- Tâches en cours : 1/25 (4%)
- Tâches pending : 9/25 (36%)

Coverage moyen :
- Backend : 87% (agrégation tous modules)
- Frontend : 82% (agrégation tous modules)

Bugs actifs :
- P0 (critiques) : 0
- P1 (majeurs) : 2
- P2 (mineurs) : 5
```

---

#### Étape 2.2 : Mettre à Jour RAPPORT_GENERAL

**Fichier** : `.github/docs-internal/ias/RAPPORT_GENERAL.md`

**Template** : `.github/docs-internal/ias/STRUCTURE_DOCUMENTATION.md` lignes 504-588

**Sections mises à jour** :

```markdown
# RAPPORT GÉNÉRAL PROJET TAXASGE

**Dernière mise à jour :** 2025-10-31 18:00
**Version :** 2.5
**Statut global :** 🟡 EN COURS

---

## 📊 VUE D'ENSEMBLE

**Phase actuelle :** Module 02 - Core Backend
**Progression globale :** 45% (15/25 tâches Module 02 terminées)
**Timeline :** Dans les temps (Semaine 3/6)
**Budget :** Dans budget (75% consommé, 80% work done)

---

## 🎯 STATUT MODULES

| Module | Statut | Progression | Fin Prévue | Fin Réelle | Écart |
|--------|--------|-------------|------------|------------|-------|
| Phase 0 (Setup) | ✅ | 100% | 2025-10-15 | 2025-10-14 | -1j |
| Module 1 (Auth) | ✅ | 100% | 2025-10-25 | 2025-10-24 | -1j |
| Module 2 (Core Backend) | 🟡 | 60% | 2025-11-15 | En cours | TBD |
| Module 3 (Declarations) | ⚪ | 0% | 2025-11-30 | TBD | TBD |

---

## 📈 MÉTRIQUES GLOBALES

### Code Quality
- Backend Coverage : 87% (cible : 85%) ✅
- Frontend Coverage : 82% (cible : 75%) ✅
- Bugs critiques ouverts : 0 ✅

### Performance
- Backend P95 latency : 320ms (cible : <500ms) ✅
- Frontend Lighthouse : 92/100 (cible : >90) ✅

### Déploiement
- Staging uptime : 99.8%
- Production uptime : N/A (pas encore déployé)

---

## 🚨 RISQUES ACTIFS

| Risque | Score | Mitigation | Responsable |
|--------|-------|------------|-------------|
| Complexité calculs fiscaux | 85 | Consultation expert + tests exhaustifs | DEV_AGENT |
| Performance queries lourdes | 60 | Optimisation + cache Redis | DEV_AGENT |

---

## 📋 DÉCISIONS PRISES (Dernières 7 jours)

1. **DECISION_005** - Cache Redis calculs - 2025-10-29 - Implémentation cache pour améliorer perfs
2. **DECISION_006** - Mock API BANGE - 2025-10-30 - Mock pour développement sans dépendance externe

---

## 🔗 RAPPORTS RÉCENTS

### Phase Actuelle
- [RAPPORT_PLANIFICATION_MODULE_02](./03_PHASES/MODULE_02_CORE_BACKEND/RAPPORT_PLANIFICATION_MODULE_02.md) - 2025-10-20
- [RAPPORT_ORCHESTRATION_31_10_2025_TASK_P2_015](./03_PHASES/MODULE_02_CORE_BACKEND/RAPPORT_ORCHESTRATION_31_10_2025_TASK_P2_015.md) - 2025-10-31

### Validations
- [GONOGO_TASK_P2_015](./04_VALIDATION/GONOGO_TASK_P2_015.md) - 2025-10-31 - Score: 87/100 - GO ✅

### Incidents
- Aucun incident critique ✅

---

## 📅 PROCHAINES ÉTAPES (7 jours)

**Cette semaine :**
- [ ] TASK-P2-016 : Store state management
- [ ] TASK-P2-017 : Tests unitaires frontend
- [ ] TASK-P2-018 : Tests E2E

**Semaine prochaine :**
- [ ] TASK-P2-019 : Responsive design
- [ ] TASK-P2-020 : Déploiement staging frontend
```

**Actions après mise à jour** :
```bash
# Commit RAPPORT_GENERAL mis à jour
git add .github/docs-internal/ias/RAPPORT_GENERAL.md
git commit -m "docs(report): Update RAPPORT_GENERAL - MODULE_02 60% complete"
git push origin $(git branch --show-current)

echo "✅ RAPPORT_GENERAL mis à jour"
```

---

### PHASE 3 : FINALISATION MODULE

#### Étape 3.1 : Vérifier Toutes Tâches Complétées

**Condition déclenchement** : Dernière tâche module validée GO ✅

**Vérification** :
```bash
# Compter rapports Go/No-Go module
GONOGO_COUNT=$(ls -1 .github/docs-internal/ias/04_VALIDATION/GONOGO_TASK_P2_*.md | wc -l)
EXPECTED_COUNT=25

if [ $GONOGO_COUNT -eq $EXPECTED_COUNT ]; then
  echo "✅ Toutes tâches validées ($GONOGO_COUNT/$EXPECTED_COUNT)"
  echo "🎯 Module 02 prêt pour finalisation"
else
  echo "⚠️ Tâches manquantes : $((EXPECTED_COUNT - GONOGO_COUNT))"
  exit 1
fi
```

---

#### Étape 3.2 : Agréger Métriques Finales Module

**Sources** :
- Tous `GONOGO_TASK_P2_*.md`
- Tous `TASK_P2_*_REPORT.md`
- Tous `RAPPORT_ORCHESTRATION_*_TASK_P2_*.md`

**Calculs** :
```markdown
## Métriques Backend
- Endpoints réalisés : 32/32 (100%)
- Coverage moyen : 87% (min: 82%, max: 92%)
- Lint errors : 0
- Type errors : 0

## Métriques Frontend
- Pages réalisées : 8/8 (100%)
- Coverage moyen : 82% (min: 78%, max: 88%)
- Lighthouse moyen : 92/100

## Métriques Intégration
- Tests E2E passés : 8/8 (100%)
- API calls success rate : 100%

## Timeline
- Durée planifiée : 6 semaines
- Durée réelle : 5.8 semaines
- Écart : -3 jours (avance)

## Bugs
- Bugs P0 résolus : 0 (aucun critique)
- Bugs P1 résolus : 2
- Bugs P2 résolus : 5
```

---

#### Étape 3.3 : Générer Rapport Final Module

**Template** : `.github/docs-internal/ias/STRUCTURE_DOCUMENTATION.md` Template 3 (lignes 408-500)

**Destination** : `.github/docs-internal/ias/03_PHASES/MODULE_0X_NOM/RAPPORT_MODULE_0X.md`

**Contenu** :
```markdown
# RAPPORT FINAL - MODULE 02 : CORE BACKEND

**Module :** 02 - Services Fiscaux Core
**Date début :** 2025-10-20
**Date fin :** 2025-11-14
**Durée totale :** 40 jours (planifié : 42 jours)
**Statut :** ✅ VALIDÉ

---

## 🎯 OBJECTIFS vs RÉALISATIONS

| Objectif | Planifié | Réalisé | Statut |
|----------|----------|---------|--------|
| Endpoints backend | 32 | 32 | ✅ 100% |
| Pages frontend | 8 | 8 | ✅ 100% |
| Tests coverage backend | >85% | 87% | ✅ |
| Tests coverage frontend | >75% | 82% | ✅ |
| Performance P95 | <500ms | 320ms | ✅ |
| Lighthouse | >90 | 92 | ✅ |

---

## 📊 MÉTRIQUES FINALES

### Backend
| Métrique | Target | Réalisé | Écart | Statut |
|----------|--------|---------|-------|--------|
| Endpoints | 32 | 32 | 0 | ✅ |
| Coverage | 85% | 87% | +2% | ✅ |
| Build Time | <120s | 95s | -25s | ✅ |
| Lint Errors | 0 | 0 | 0 | ✅ |
| Type Errors | 0 | 0 | 0 | ✅ |

### Frontend
| Métrique | Target | Réalisé | Écart | Statut |
|----------|--------|---------|-------|--------|
| Pages | 8 | 8 | 0 | ✅ |
| Lighthouse | >90 | 92 | +2 | ✅ |
| Coverage | 75% | 82% | +7% | ✅ |
| Build Time | <180s | 145s | -35s | ✅ |

---

## 🚀 DÉPLOIEMENT STAGING

**URL Staging Backend :** https://taxasge-backend-staging.run.app
**URL Staging Frontend :** https://staging.taxasge.com

**Tests Smoke :**
- [x] Health check OK (200)
- [x] Login fonctionne
- [x] Création déclaration fonctionne
- [x] Calcul fiscal fonctionne
- [x] Performance acceptable (<500ms P95)

---

## 📚 LEÇONS APPRISES

### Positives
1. Cache Redis a amélioré perfs calculs de 60% (decision_005)
2. Mock API BANGE a accéléré développement (decision_006)
3. Tests exhaustifs calculs ont évité bugs critiques

### Négatives
1. Sous-estimation complexité calculs fiscaux (risque_001)
2. Dépendance API BANGE a causé 2j retard initialement

### Améliorations Process
1. Prévoir consultation expert métier dès planification
2. Toujours créer mocks services externes dès début
3. Augmenter buffer temps pour modules complexes

---

## 📋 DETTE TECHNIQUE CRÉÉE

| Item | Criticité | Effort Fix | Planifié Pour |
|------|-----------|------------|---------------|
| Optimisation queries calculs | Moyenne | 2j | Module 5 (Performance) |
| Refactoring service calculs | Faible | 1j | Module 6 (Refactoring) |

---

## ✅ VALIDATION FINALE

**Critères Go/No-Go Module Suivant :**
- [x] Toutes tâches validées GO
- [x] Déployé staging avec succès
- [x] Smoke tests OK
- [x] Documentation complète
- [x] 0 bugs critiques

**Go/No-Go :** ✅ GO

**Signatures :**
- **Développé par :** Claude Code | Date : 2025-11-14
- **Validé par :** [Ton nom] | Date : ___________
- **Approuvé pour MODULE_03 :** [Ton nom] | Date : ___________
```

---

#### Étape 3.4 : Générer Rapport Orchestration Module

**Template** : Nouveau (à créer)

**Destination** : `.github/docs-internal/ias/RAPPORT_ORCHESTRATION_14_11_2025_MODULE_02.md`

**Contenu** :
```markdown
# RAPPORT ORCHESTRATION - MODULE 02 : CORE BACKEND

**Date finalisation :** 2025-11-14 18:00
**Durée totale :** 40 jours
**Tâches :** 25/25 complétées
**Statut :** ✅ VALIDÉ

---

## 📊 TIMELINE MODULE

| Tâche | Agent | Début | Fin | Durée | Score Go/No-Go | Décision |
|-------|-------|-------|-----|-------|----------------|----------|
| TASK-P2-001 | DEV_AGENT | 2025-10-20 | 2025-10-22 | 2j | 89/100 | GO ✅ |
| TASK-P2-002 | DEV_AGENT | 2025-10-22 | 2025-10-23 | 1j | 92/100 | GO ✅ |
| TASK-P2-003 | DEV_AGENT | 2025-10-23 | 2025-10-25 | 2j | 87/100 | GO ✅ |
| ... | ... | ... | ... | ... | ... | ... |
| TASK-P2-025 | DEV_AGENT | 2025-11-13 | 2025-11-14 | 1j | 91/100 | GO ✅ |

**Total durée :** 40 jours (planifié : 42 jours) - Avance : 2 jours

---

## 🎯 AGENTS INVOQUÉS

### DEV_AGENT (Fullstack)
**Type :** Agent fullstack (backend + frontend)
**Tâches :** 25/25
**Skills invoqués :** taxasge-backend-dev + taxasge-frontend-dev
**Workflow :** DEV_WORKFLOW.md
**Durée totale :** 35 jours
**Succès :** 100%
**Garantie :** Cohérence backend/frontend absolue

### TEST_AGENT
**Invocations :** 25 (1 par tâche via Go/No-Go Validator)
**Workflow :** TEST_WORKFLOW.md
**Tests exécutés :** 135 tests backend + 45 tests frontend
**Taux succès :** 100%

### DOC_AGENT
**Invocations :** 25 (1 par tâche via Go/No-Go Validator)
**Workflow :** DOC_WORKFLOW.md
**Documentation générée :** 32 endpoints Swagger + 8 READMEs
**Complétude :** 100%

---

## 📈 MÉTRIQUES AGRÉGÉES

### Qualité Code
- Coverage backend moyen : 87% (min: 82%, max: 92%)
- Coverage frontend moyen : 82% (min: 78%, max: 88%)
- Lint errors total : 0
- Type errors total : 0

### Performance
- Build time backend moyen : 95s (cible : <120s) ✅
- Build time frontend moyen : 145s (cible : <180s) ✅
- Test execution moyen : 78s (cible : <90s) ✅

### Go/No-Go
- Score moyen : 89/100
- Score min : 85/100 (TASK-P2-012)
- Score max : 94/100 (TASK-P2-008)
- Décisions GO : 25/25 (100%)
- Décisions NO-GO : 0/25 (0%)

---

## 🔄 DÉCISIONS TECHNIQUES MODULE

### DECISION_005 : Cache Redis pour calculs
**Date :** 2025-10-29
**Contexte :** Performance calculs fiscaux insuffisante
**Choix :** Implémentation cache Redis avec TTL 1h
**Impact :** Amélioration 60% performance
**Référence :** `.github/docs-internal/ias/01_DECISIONS/DECISION_005.md`

### DECISION_006 : Mock API BANGE
**Date :** 2025-10-30
**Contexte :** Dépendance API externe bloque développement
**Choix :** Mock API BANGE pour environnement dev/test
**Impact :** Accélération développement +2j
**Référence :** `.github/docs-internal/ias/01_DECISIONS/DECISION_006.md`

---

## 🚨 INCIDENTS & RÉSOLUTIONS

### INCIDENT_001 : API BANGE indisponible
**Date :** 2025-10-28
**Impact :** Bloquage TASK-P2-007 pendant 4h
**Résolution :** Création mock API (DECISION_006)
**Durée :** 4h
**Prévention :** Toujours créer mocks dès début module

---

## 📚 LEÇONS APPRISES GLOBALES

### Best Practices Identifiées
1. Consultation expert métier dès planification évite surprises
2. Mocks services externes dès début accélèrent développement
3. Tests exhaustifs calculs évitent bugs critiques production

### Patterns Réutilisables
1. Architecture 3-tiers (Routes → Services → Repositories) bien adaptée
2. Cache Redis pour opérations lourdes très efficace
3. Go/No-Go par tâche maintient qualité constante

### Améliorations Process
1. Augmenter buffer temps modules complexes (fiscalité) de 20%
2. Toujours prévoir mock services externes dès planification
3. Planifier reviews experts métier en milieu module

---

## 🎯 PROCHAINE ÉTAPE

**MODULE_03 : Declarations Avancées**
**Début prévu :** 2025-11-18 (après validation utilisateur)
**Durée estimée :** 4 semaines
**Tâches :** TASK-P3-001 à TASK-P3-018
**Dépendances :** MODULE_02 ✅ validé
```

---

#### Étape 3.5 : Mettre à Jour RAPPORT_GENERAL (Final)

**Fichier** : `.github/docs-internal/ias/RAPPORT_GENERAL.md`

**Mise à jour section "STATUT MODULES"** :
```markdown
| Module | Statut | Progression | Fin Prévue | Fin Réelle | Écart |
|--------|--------|-------------|------------|------------|-------|
| Phase 0 (Setup) | ✅ | 100% | 2025-10-15 | 2025-10-14 | -1j |
| Module 1 (Auth) | ✅ | 100% | 2025-10-25 | 2025-10-24 | -1j |
| Module 2 (Core Backend) | ✅ | 100% | 2025-11-15 | 2025-11-14 | -1j |  ← MIS À JOUR
| Module 3 (Declarations) | 🟡 | 0% | 2025-11-30 | En attente | TBD |  ← PRÊT
```

**Mise à jour "VUE D'ENSEMBLE"** :
```markdown
**Phase actuelle :** MODULE_03 - Declarations (après validation)
**Progression globale :** 60% (3/5 modules terminés)
**Timeline :** Avance 3 jours
**Budget :** 72% consommé, 75% work done ✅
```

---

#### Étape 3.6 : Git Commit + Push

**Actions automatiques** :
```bash
#!/bin/bash
# Script finalisation module

MODULE_ID=$1
MODULE_NAME=$2
DATE=$(date +%d_%m_%Y)

# 1. Commit rapport final module
git add .github/docs-internal/ias/03_PHASES/${MODULE_ID}_${MODULE_NAME}/RAPPORT_MODULE_${MODULE_ID}.md
git commit -m "docs(module): Add final report MODULE_${MODULE_ID} - 100% complete"

# 2. Commit rapport orchestration module
git add .github/docs-internal/ias/RAPPORT_ORCHESTRATION_${DATE}_${MODULE_ID}.md
git commit -m "docs(orchestration): Add MODULE_${MODULE_ID} orchestration report"

# 3. Commit RAPPORT_GENERAL mis à jour
git add .github/docs-internal/ias/RAPPORT_GENERAL.md
git commit -m "docs(report): Update RAPPORT_GENERAL - MODULE_${MODULE_ID} validated"

# 4. Push
git push origin $(git branch --show-current)

echo "✅ MODULE_${MODULE_ID} finalisé et documenté"
echo "📊 Rapports générés :"
echo "  - RAPPORT_MODULE_${MODULE_ID}.md"
echo "  - RAPPORT_ORCHESTRATION_${DATE}_${MODULE_ID}.md"
echo "  - RAPPORT_GENERAL.md (mis à jour)"
echo ""
echo "⚠️ VALIDATION REQUISE POUR MODULE SUIVANT"
```

**⚠️ PAUSE WORKFLOW** :
```markdown
┌─────────────────────────────────────────────────────────┐
│ ✅ MODULE 02 FINALISÉ ET VALIDÉ                         │
│                                                          │
│ Durée : 40 jours (planifié : 42j) - Avance : 2j        │
│ Tâches : 25/25 validées GO ✅                           │
│ Score moyen : 89/100                                    │
│                                                          │
│ Rapports générés :                                      │
│ - Rapport final : ias/03_PHASES/MODULE_02/RAPPORT_...  │
│ - Orchestration : ias/RAPPORT_ORCHESTRATION_...        │
│ - RAPPORT_GENERAL mis à jour                           │
│                                                          │
│ ⚠️ VALIDATION REQUISE POUR MODULE SUIVANT               │
│                                                          │
│ MODULE_03 : Declarations Avancées                      │
│ - Début prévu : 2025-11-18                             │
│ - Durée : 4 semaines                                   │
│ - Tâches : 18                                          │
│                                                          │
│ Que voulez-vous faire ?                                 │
│ 1. GO MODULE_03 → Démarre planification MODULE_03      │
│ 2. Review rapports MODULE_02                           │
│ 3. Pause projet                                        │
└─────────────────────────────────────────────────────────┘
```

---

## References

### Agents
- `.claude/.agent/Tasks/DEV_AGENT.md` - Agent développement fullstack (backend + frontend)
- `.claude/.agent/Tasks/TEST_AGENT.md` - Agent tests
- `.claude/.agent/Tasks/DOC_AGENT.md` - Agent documentation
- `.claude/.agent/Tasks/FRONTEND_AGENT.md` - [ARCHIVED] Consolidé dans DEV_AGENT fullstack

### Workflows
- `.claude/.agent/SOP/DEV_WORKFLOW.md` - Processus développement
- `.claude/.agent/SOP/TEST_WORKFLOW.md` - Processus tests
- `.claude/.agent/SOP/DOC_WORKFLOW.md` - Processus documentation

### Phases
- `.claude/.agent/Tasks/PHASE_X.md` - Définitions modules

### Templates Rapports
- `.github/docs-internal/ias/STRUCTURE_DOCUMENTATION.md` - Templates officiels
  - Template 1 (lignes 104-315) : RAPPORT_PLANIFICATION
  - Template 2 (lignes 319-404) : RAPPORT_BACKEND/FRONTEND
  - Template 3 (lignes 408-500) : RAPPORT_FINAL_MODULE

### Skills
- `.claude/skills/taxasge-gonogo-validator/Skill.md` - Validation tâches

---

## Success Criteria

Une orchestration module est réussie si :
- ✅ Rapport planification généré AVANT première tâche
- ✅ RAPPORT_GENERAL mis à jour quotidiennement
- ✅ Rapport final module généré APRÈS dernière tâche validée
- ✅ Rapport orchestration module généré avec timeline complète
- ✅ Toutes métriques agrégées correctement
- ✅ Git commit + push automatique
- ✅ Workflow pause pour validation utilisateur

---

## Example Usage

**User says:** "Démarre module 2"

**Skill actions (Phase 1 - Planification):**
1. Lit `.claude/.agent/Tasks/PHASE_2.md`
2. Analyse baseline (fichiers existants)
3. Identifie dépendances (Module 1 validé ✅)
4. Génère `RAPPORT_PLANIFICATION_MODULE_02.md`
5. Git commit + push
6. Affiche : "✅ MODULE_02 planifié. Attente validation pour démarrage"

**User says:** "GO planification"

**Skill actions:**
7. DEV_AGENT démarre TASK-P2-001

[...40 jours + 25 tâches plus tard...]

**User says:** "Finalise module 2"

**Skill actions (Phase 3 - Finalisation):**
8. Vérifie 25/25 tâches validées GO ✅
9. Agrège métriques (coverage, scores, timeline)
10. Génère `RAPPORT_MODULE_02.md`
11. Génère `RAPPORT_ORCHESTRATION_14_11_2025_MODULE_02.md`
12. Met à jour `RAPPORT_GENERAL.md` (Module 2 : 100%)
13. Git commit + push
14. Affiche validation requise MODULE_03

---

**Skill created by:** TaxasGE Backend Team  
**Date:** 2025-10-31  
**Version:** 2.0.0  
**Status:** ✅ READY FOR USE
