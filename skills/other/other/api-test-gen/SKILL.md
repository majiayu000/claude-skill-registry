---
name: api-test-gen
description: "Skill de generation automatique de tests API. Scanne les endpoints d'un projet (API Platform, Express, etc.) et genere des tests couvrant les cas nominaux, les erreurs, les autorisations et les cas limites. Supporte PHPUnit ApiTestCase (Symfony) et peut s'adapter a d'autres frameworks. Ce skill devrait etre utilise quand l'utilisateur veut ajouter des tests a des endpoints existants ou generer une couverture de test pour un domaine."
---

# api-test-gen

## But

Generer des tests API automatiques (PHPUnit ApiTestCase ou equivalent) pour les endpoints existants.

## Modes

### Mode A : `--endpoint {route}`
Generer les tests pour un endpoint specifique.

### Mode B : `--entity {nom}`
Generer les tests pour tous les endpoints d'une entite.

### Mode C : `--domain {domaine}`
Generer les tests pour un domaine complet.

### Mode D : `--coverage`
Analyser la couverture de tests existante et proposer les manquants.

## Workflow

1. **Identifier les endpoints** : lire les attributs ApiResource/routes
2. **Pour chaque endpoint, generer** :
   - Test nominal (happy path)
   - Test d'autorisation (acces refuse, roles insuffisants)
   - Test de validation (donnees invalides, champs manquants)
   - Test de cas limites (entite inexistante, donnees vides)
3. **Suivre les patterns de test** de `~/evan-workflow/technos/symfony/patterns/testing.md`
4. **Generer les fixtures necessaires**
5. **Verifier que les tests passent**

## Conventions

- Un fichier de test par entite : `tests/Api/{Entity}Test.php`
- DataProviders pour les variations de roles
- Methodes helper pour les assertions courantes (`assertJsonContains`, `assertResponseStatusCodeSame`)
