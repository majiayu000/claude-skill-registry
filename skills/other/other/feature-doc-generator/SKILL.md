---
name: feature-doc-generator
description: >
  Générateur de documentation technique réutilisable pour les features implémentées dans des projets de développement logiciel sur mesure.
  Produit des guides de référence génériques (non liés à un projet spécifique) couvrant l'architecture, le front-end, le back-end, les APIs et les fournisseurs externes.
  Ces documents servent de blueprints pour réimplémenter la même feature dans d'autres projets via Claude Code.
  Utiliser ce skill quand : (1) on veut documenter une feature existante pour la réutiliser, (2) on veut créer un guide d'implémentation générique à partir d'un projet concret,
  (3) on dit "documente cette feature", "crée une référence technique", "fais un blueprint de cette fonctionnalité", "on veut réutiliser ce pattern",
  (4) on veut extraire les bonnes pratiques d'un projet pour les appliquer ailleurs.
---

# Feature Doc Generator

Transformer une feature concrète d'un projet en documentation de référence **générique** et **réutilisable**, prête à être poussée à Claude Code pour implémenter la même feature dans un autre projet.

## Workflow

1. **Identifier la feature** — Comprendre ce qu'on documente
2. **Analyser le code source** — Explorer le projet courant
3. **Poser des questions complémentaires** — Combler les trous
4. **Générer la documentation** — Produire les fichiers Markdown par couche
5. **Réviser et finaliser** — Valider avec l'utilisateur

## Étape 1 : Identifier la feature

Demander à l'utilisateur :
- Le nom de la feature (ex: "Gestion de fichiers audio et transcription")
- Une description en une phrase
- Les technologies principales impliquées (si connues)

## Étape 2 : Analyser le code source

Explorer le projet courant pour extraire l'information technique :

1. **Structure du projet** — Arborescence des dossiers pertinents
2. **Back-end** — Routes, modèles, services, migrations, config
3. **Front-end** — Composants UI, state management, appels API, routing
4. **APIs et intégrations** — Clients API externes, config fournisseurs, webhooks
5. **Configuration** — Variables d'environnement, fichiers de config, packages

Pour chaque couche, noter les patterns architecturaux, librairies clés, décisions techniques, et pièges résolus.

## Étape 3 : Questions complémentaires

Après l'analyse du code, poser des questions ciblées sur ce qui ne peut pas être déduit :
- Pourquoi tel fournisseur a été choisi
- Limitations connues et workarounds
- Considérations de coût/performance
- Alternatives évaluées et rejetées
- Edge cases importants découverts en production

## Étape 4 : Générer la documentation

Créer un dossier `docs/feature-references/<nom-de-la-feature>/` dans le projet.

### Fichiers à produire

Consulter le template de référence correspondant avant de rédiger chaque fichier :

| Fichier | Contenu | Template |
|---------|---------|----------|
| `overview.md` | Vue d'ensemble et architecture | `references/template-overview.md` |
| `backend.md` | Implémentation back-end | `references/template-backend.md` |
| `frontend.md` | Implémentation front-end | `references/template-frontend.md` |
| `api-providers.md` | APIs et fournisseurs externes | `references/template-api-providers.md` |
| `database.md` | Schéma de données et migrations | `references/template-database.md` |
| `implementation-guide.md` | Guide pas-à-pas pour réimplémenter | `references/template-implementation-guide.md` |

### Adaptation

Ne pas créer les fichiers non pertinents (ex: pas de `frontend.md` pour une feature sans front-end, pas de `api-providers.md` sans API externe).

### Règles de rédaction

- **Générique** : Ne jamais mentionner le nom du projet source. Utiliser "le projet", "l'application"
- **Exemples de code** : Inclure des snippets représentatifs mais renommer les éléments spécifiques au projet
- **Expliquer le pourquoi** : Justifier chaque décision technique
- **Lister les alternatives** : Mentionner les autres approches possibles
- **Inclure les gotchas** : Documenter les pièges et comment les éviter
- **Actionnable** : Un développeur ou Claude Code doit pouvoir suivre le guide et implémenter la feature

## Étape 5 : Réviser et finaliser

Présenter un résumé des documents générés. Demander s'il y a des ajustements ou des informations manquantes. Itérer si nécessaire.
