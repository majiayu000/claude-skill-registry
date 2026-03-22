---
name: "Unity Code Gen"
description: "Generation de code C# Unity production-ready a partir de specifications fonctionnelles. Analyse la codebase existante, choisit le bon pattern architectural, genere le code et les tests. Triggers: /unity-code-gen, 'generer script Unity', 'creer composant', 'nouveau MonoBehaviour', 'creer ScriptableObject', 'generer code Unity', 'nouveau systeme Unity', 'ajouter feature Unity'. Utiliser quand l'utilisateur demande de creer un nouveau script, composant, systeme ou feature dans Unity. Produit des fichiers C# respectant les conventions du projet avec tests NUnit associes."
---

# Unity Code Generation

Generation de code C# Unity production-ready. Analyse le projet existant, choisit le pattern adapte, genere code + tests.

## Ce que fait cette skill

1. Analyse la demande (feature, systeme, type de composant)
2. Inspecte la codebase existante (conventions, namespaces, assembly definitions)
3. Choisit le pattern architectural via un arbre de decision
4. Genere du C# propre avec les attributs Unity adequats
5. Genere les tests unitaires correspondants (NUnit)
6. Place les fichiers dans les bons repertoires

## Prerequis

- Un projet Unity existant avec une structure de dossiers identifiable
- Acces aux fichiers du projet via les outils Claude Code (Read, Write, Edit, Grep, Glob)
- Aucune dependance MCP Unity requise

## Demarrage rapide

1. L'utilisateur decrit la feature ou le composant souhaite
2. Inspecter le projet avec Glob/Grep pour comprendre les conventions
3. Appliquer l'arbre de decision pour choisir le pattern
4. Generer le code + tests dans les bons repertoires

## Arbre de decision

```
La chose a creer...
│
├─ Stocke des donnees configurables (stats, settings) ?
│  └─ OUI → ScriptableObject Data Container
│
├─ Sert de canal de communication entre systemes ?
│  └─ OUI → ScriptableObject Event Channel
│
├─ Vit sur un GameObject dans la scene ?
│  ├─ Controle du comportement runtime ? → MonoBehaviour
│  └─ Juste un data holder sur un GO ? → MonoBehaviour simple (struct-like)
│
├─ Definit un contrat que plusieurs classes implementent ?
│  └─ OUI → Interface (+ implementations MonoBehaviour ou pure C#)
│
├─ Logique pure sans dependance Unity (math, algo, parsing) ?
│  └─ OUI → Pure C# class (pas de MonoBehaviour)
│
├─ Utilitaire stateless reutilisable ?
│  └─ OUI → Static class ou extension methods
│
├─ Gestion d'etats discrets (joueur, IA, game flow) ?
│  └─ OUI → State Machine (enum + switch ou state classes)
│
├─ Gestion d'inputs avec undo/replay ?
│  └─ OUI → Command Pattern
│
├─ Objets crees/detruits frequemment (projectiles, VFX) ?
│  └─ OUI → Object Pool
│
├─ Logique asynchrone (chargement, timer, sequence) ?
│  └─ OUI → Async Awaitable Component (Unity 6+)
│
└─ Milliers d'entites similaires a traiter en parallele ?
   └─ OUI → ECS (DOTS) — hors scope de cette skill
```

## Guide etape par etape

### Etape 1 — Analyser la demande

Identifier clairement :
- **Quoi** : feature, systeme, composant, data container, event ?
- **Ou** : quel module du projet ? quel assembly definition ?
- **Interactions** : avec quels systemes existants ?
- **Donnees** : quelles donnees manipulees, persistees, serialisees ?

### Etape 2 — Inspecter la codebase existante

Avant d'ecrire une seule ligne, toujours executer ces recherches :

```
Glob("Assets/**/*.asmdef")              → assembly definitions, structure modules
Glob("Assets/**/*.cs", limit aux dossiers cibles) → fichiers existants
Grep("namespace ", type: "cs")           → conventions de namespace
Grep("class .* : MonoBehaviour", type: "cs") → MonoBehaviours existants
Grep("class .* : ScriptableObject", type: "cs") → SOs existants
Grep("\\[SerializeField\\]", fichier cible)  → style de serialisation
```

Identifier :
- Le pattern de nommage (`_camelCase` pour private ? prefixes ?)
- La structure de namespace (`Game.Core`, `Game.Player`, etc.)
- Les conventions d'attributs (`[Header]`, `[Tooltip]`, `[Range]`)
- Les patterns deja utilises (events, interfaces, state machines)

### Etape 3 — Choisir le pattern

Appliquer l'arbre de decision ci-dessus. En cas de doute, privilegier la composition et les patterns simples.

### Etape 4 — Generer le code C#

Appliquer systematiquement ces conventions Unity :

**Attributs obligatoires :**
- `[SerializeField] private` pour les champs editables dans l'Inspector (jamais `public`)
- `[RequireComponent(typeof(X))]` quand le script depend d'un autre composant
- `[Header("Section")]` pour organiser l'Inspector par groupes logiques
- `[Tooltip("Explication")]` sur les champs non evidents
- `[Range(min, max)]` sur les valeurs numeriques bornees

**Structure d'un fichier :**
```csharp
// 1. Namespace
// 2. Attributs de classe ([RequireComponent], [DisallowMultipleComponent])
// 3. Declaration de classe
// 4. Constantes
// 5. [SerializeField] champs groupes par [Header]
// 6. Events publics
// 7. Proprietes publiques (read-only si possible)
// 8. Champs prives
// 9. Awake / OnEnable / Start
// 10. OnDisable / OnDestroy
// 11. Update / FixedUpdate (si necessaire)
// 12. Methodes publiques
// 13. Methodes privees
// 14. Coroutines
```

**Namespace :** matcher la structure existante. Si le projet utilise `Game.Player`, ne pas inventer `MyNamespace.Scripts`.

### Etape 5 — Generer les tests

Pour chaque fichier genere, creer le test correspondant :

- **EditMode tests** : logique pure, calculs, state machines, data validation
- **PlayMode tests** : comportement MonoBehaviour, interactions composants, coroutines

Placement des tests :
```
Assets/Tests/EditMode/  → tests logique (assembly ref: Game.Core, etc.)
Assets/Tests/PlayMode/  → tests comportement (assembly ref + UnityEngine.TestRunner)
```

### Etape 6 — Placer les fichiers

- Respecter les assembly definitions et la structure de dossiers existante
- Les tests vont dans le dossier `Tests/` miroir
- Produire : fichier(s) C# source, tests NUnit, resume (pattern choisi, fichiers crees)

## Regles strictes

**TOUJOURS :**
- Inspecter la codebase existante avant de generer (Glob + Grep)
- Matcher les conventions de nommage du projet
- Generer les tests en meme temps que le code
- Utiliser `[SerializeField] private` pour les champs Inspector
- Utiliser des namespaces coherents avec la structure projet
- Ajouter `[Header]` et `[Tooltip]` pour la lisibilite Inspector
- Privilegier la composition sur l'heritage
- Desubscribe les events dans `OnDisable` ou `OnDestroy`

**JAMAIS :**
- Coder sans avoir inspecte le projet existant
- Utiliser le pattern Singleton MonoBehaviour (preferer SO ou Service Locator)
- Utiliser des champs `public` (utiliser `[SerializeField] private` + propriete)
- Utiliser `Find*()` ou `SendMessage()` avec des strings
- Ecrire de la logique dans `Update()` sans cacher les references
- Generer du code sans tests
- Creer un fichier de plus de 500 lignes (modulariser)
- Hardcoder des valeurs magiques (utiliser SO ou `const`)

---

## Skills connexes

- Prototype rapide sans architecture ? Utiliser `/proto` (Unity Rapid Proto)
- Refactorer du code existant ? Utiliser `/unity-refactor` (Unity Refactor)
- Creer un custom inspector pour le composant genere ? Utiliser `/unity-editor-tools` (Unity Editor Tools)
- Generer et executer les tests NUnit ? Utiliser `/unity-test` (Unity Test)

## Troubleshooting

| Probleme | Solution |
|----------|----------|
| Pas de convention claire dans le projet | Utiliser les conventions Unity standard (`_camelCase`, `PascalCase`) et creer un patron coherent |
| Pas d'assembly definition existante | Generer le code dans le dossier principal, proposer de creer des asmdef si le projet grossit |
| Le namespace ne correspond a rien | Utiliser le nom du projet + module, ex: `ProjectName.Module` |
| Tests impossibles car tout est couple | Extraire la logique dans des classes pure C# testables, garder le MonoBehaviour comme "glue" |
| Le projet utilise des Singletons partout | Ne pas en ajouter de nouveaux, proposer une migration progressive vers SO/Service Locator |
| Conflit de nommage avec un package tiers | Prefixer le namespace avec le nom du projet |

Templates de code detailles : voir `references/code-templates.md`.
