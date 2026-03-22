---
name: "Unity Perf Audit"
description: "Audit statique de performance pour projets Unity. Triggers: /perf, /perf-audit, 'audit performance', 'optimiser performance', 'anti-pattern performance', 'frame rate', 'profiler', 'budget fps'. Analyse le code C# du projet pour detecter les anti-patterns de performance (CPU, GPU, memoire). Produit un rapport avec severite, localisation fichier:ligne, et correctifs concrets avant/apres."
---

# Unity Perf Audit

## Ce que fait cette skill

Analyse statique du code C# d'un projet Unity pour detecter les anti-patterns de performance. Pas besoin d'executer le jeu ni de profiler -- on scanne le code source avec Grep et Glob.

Produit :
- Un inventaire des fichiers C# du projet (compte, taille, fichiers volumineux)
- Un rapport d'anti-patterns detectes avec severite et localisation
- Les 5 correctifs prioritaires avec code avant/apres

## Prerequis

- Projet Unity avec des scripts C# dans `Assets/`
- Acces en lecture au dossier du projet
- Aucun package, aucun outil externe requis

## Arbre de decision

```
Symptome rapporte ?
|
+-- FPS bas en general --> Lancer le scan complet (etapes 1-5)
+-- Spikes ponctuels / stuttering --> Focus CPU (anti-patterns C1-C12)
+-- Memoire qui grimpe / crashs OOM --> Focus Memory (anti-patterns M1-M7)
+-- Rendu lent, draw calls hauts --> Focus GPU (anti-patterns G1-G5)
+-- Pas de symptome precis (audit preventif) --> Scan complet
```

## Demarrage rapide

1. Scanner la structure projet (Glob `**/*.cs`)
2. Detecter les anti-patterns CPU, GPU, memoire (Grep)
3. Scorer et categoriser chaque probleme
4. Produire le rapport avec fichier:ligne
5. Proposer les 5 fixes prioritaires

## Guide etape par etape

### Etape 1 : Scanner la structure projet

Utiliser Glob pour inventorier tous les fichiers C# du projet.

```
Glob: Assets/**/*.cs
```

Analyser :
- Nombre total de fichiers `.cs`
- Identifier les fichiers > 500 lignes (Read pour compter les lignes ou `wc -l`)
- Identifier les dossiers avec le plus de scripts (structure du projet)
- Exclure les dossiers `Plugins/`, `ThirdParty/`, `TextMesh Pro/` de l'analyse (code externe)

Commande Bash pour compter les lignes de tous les fichiers :
```bash
find <project>/Assets -name "*.cs" -not -path "*/Plugins/*" -not -path "*/ThirdParty/*" -not -path "*/TextMesh Pro/*" | xargs wc -l | sort -rn | head -20
```

Produire un resume :
```
## Structure projet
- **Fichiers C#** : 47
- **Lignes totales** : 12,340
- **Fichiers > 500 lignes** : PlayerManager.cs (623), GameController.cs (891)
- **Dossiers principaux** : Scripts/ (28), UI/ (12), Enemies/ (7)
```

### Etape 2 : Detecter les anti-patterns

Scanner les fichiers C# pour les anti-patterns CPU, GPU et memoire. Voir `references/anti-patterns.md` pour la table complete des patterns a detecter.

Pour chaque match, noter le fichier, le numero de ligne, et la ligne de code. Executer les recherches Grep sur tous les fichiers `.cs` du projet (hors exclusions).

### Etape 3 : Scorer et categoriser

Attribuer un score par fichier et global :

| Severite | Points | Impact |
|----------|--------|--------|
| Critical | 10 | Cause directe de lag visible (chaque frame) |
| High | 5 | Degradation significative sous charge |
| Medium | 2 | Impact mesurable au profiler |
| Low | 1 | Bonne pratique, impact minimal |

Score global :
- **0-10** : Propre. Pas d'action requise.
- **11-30** : Acceptable. Quelques points a corriger.
- **31-60** : Problematique. Corrections recommandees avant build.
- **61+** : Critique. Corrections obligatoires.

Ne scorer que les problemes reellement trouves dans le code. Ne jamais inventer de problemes hypothetiques.

### Etape 4 : Produire le rapport

Format du rapport : tableau avec colonnes `#`, `Probleme`, `Severite`, `Fichier:Ligne`, `Description`. Grouper par severite (Critical > High > Medium > Low). Ajouter un resume par severite (nombre + score). Inclure un score global avec le verdict (Propre / Acceptable / Problematique / Critique).

### Etape 5 : Proposer les 5 fixes prioritaires

Pour chaque fix, montrer le code avant et apres. Prendre les problemes par ordre de severite (Critical d'abord). Format : titre, severite, ligne, impact, puis code avant/apres.

Patterns de fix courants :

| Anti-pattern | Fix standard |
|-------------|-------------|
| GetComponent dans Update | Cache dans Awake avec champ prive |
| Find en runtime | Cache dans Awake ou injecter via SerializeField |
| Camera.main dans Update | `private Camera _cam; void Awake() => _cam = Camera.main;` |
| String concat dans Update | `StringBuilder` ou `string.Format` ou supprimer le log |
| Instantiate dans Update | Object pooling (Queue + activation/desactivation) |
| foreach dans Update | Boucle `for` avec `List<T>` |
| SendMessage | Interface directe ou event C# |
| .tag == | `.CompareTag("name")` |
| new WaitForSeconds repete | Cache `static readonly WaitForSeconds` |
| Event sans unsubscribe | Ajouter `-=` dans `OnDisable()` ou `OnDestroy()` |
| Resources.Load sans Unload | Ajouter `Resources.UnloadUnusedAssets()` apres usage ou passer a Addressables |

## Regles strictes

**TOUJOURS :**
- Reporter uniquement les problemes trouves dans le code reel (pas d'hypotheses)
- Indiquer le fichier et le numero de ligne exact pour chaque probleme
- Fournir un correctif concret avec code avant/apres
- Prioriser par impact (Critical en premier)
- Exclure le code tiers (Plugins/, ThirdParty/, TextMesh Pro/)
- Verifier le contexte : un `GetComponent` dans `Start()` est acceptable, dans `Update()` non

**JAMAIS :**
- Suggerer d'optimiser du code qui ne s'execute qu'une fois (Start, Awake, OnEnable initial, loading screens)
- Inventer des problemes non presents dans le code
- Recommander des refactors massifs (on corrige les hot paths, pas l'architecture)
- Suggerer des outils externes ou packages payants
- Reporter un `foreach` sur une collection fixe hors hot path comme un probleme
- Ignorer les faux positifs : verifier que le pattern est bien dans le contexte problematique avant de le reporter

## Skills connexes

- Diagnostiquer un bug de performance specifique (crash, freeze ponctuel) ? Utiliser `/unity-debug` (Unity Debug)
- Appliquer les corrections detectees avec refactoring structure ? Utiliser `/unity-refactor` (Unity Refactor)
- Tester apres correction ? Utiliser `/unity-test` (Unity Test)

## Troubleshooting

| Probleme | Solution |
|----------|----------|
| Trop de faux positifs GetComponent | Verifier la methode englobante. `GetComponent` dans `Awake`/`Start`/`OnEnable` n'est pas un probleme. Utiliser `-B 20` dans Grep pour voir le contexte. |
| Pattern detecte dans un commentaire | Filtrer les lignes qui commencent par `//` ou sont dans un bloc `/* */`. Lire le fichier pour confirmer. |
| Fichier trop gros pour analyser | Lire par sections avec offset/limit. Se concentrer sur les methodes Update, FixedUpdate, LateUpdate. |
| Le projet n'a pas de dossier Assets/ | Verifier le path du projet. Demander a l'utilisateur de confirmer la racine du projet Unity. |
| Score tres eleve sur un prototype | Contextualiser : un prototype n'a pas besoin d'optimisation poussee. Mentionner les problemes mais reduire l'urgence. |
| Anti-pattern dans du code desactive | Verifier s'il y a `#if` / `[System.Obsolete]` / commentaire indiquant du code mort. Ne pas reporter le code mort. |
| Pas de fichiers .cs trouves | Le projet est peut-etre vide ou les scripts sont dans un package. Verifier avec `Glob **/*.cs` sans filtre de dossier. |
| Event leak faux positif | Verifier les patterns : si `+=` est dans `OnEnable` et `-=` est dans `OnDisable`, c'est correct. Verifier aussi les lambdas anonymes (impossible a unsubscribe). |

Table complete des anti-patterns : voir `references/anti-patterns.md`
