---
name: "Unity Refactor"
description: "Refactoring incremental et securise de code C# Unity. Detecte les code smells, propose un plan priorise par risque, et execute les changements un par un avec verification de compilation. Triggers: /unity-refactor, 'refactor', 'code smell', 'clean code', 'dette technique', 'refactoring unity'. Produit du code restructure sans changement de comportement."
---

# Unity Refactor

## Ce que fait cette skill

Cette skill analyse une codebase Unity C# pour detecter les code smells, propose un plan de refactoring priorise par niveau de risque, puis execute les changements un par un avec verification apres chaque modification. L'objectif est d'ameliorer la qualite du code sans jamais changer le comportement existant.

## Prerequis

- Projet Unity avec du code C# existant dans `Assets/Scripts/`
- Pas de dependance MCP Unity : utilise uniquement Read, Write, Edit, Grep, Glob, Bash

## Arbre de decision

```
Quel type de dette technique ?
|
+-- Code trop long / illisible ?
|   +-- Fichier > 500 lignes --> God class split (risque eleve)
|   +-- Methode > 50 lignes --> Extraction de methodes (risque faible)
|
+-- Couplage fort entre classes ?
|   +-- References directes cross-systeme --> Event Channel SO (risque moyen)
|   +-- Singleton partout --> SO / Service Locator (risque eleve)
|
+-- API obsolete ?
|   +-- Old Input --> New Input System (risque moyen, recette 6)
|   +-- Coroutines --> async Awaitable (risque moyen, recette 4)
|
+-- Code smells generaux ?
    +-- Magic strings --> Constantes / enum (risque faible)
    +-- Champs publics --> [SerializeField] private (risque faible)
```

Voir le catalogue de refactoring ci-dessous pour les recettes detaillees.

## Demarrage rapide

1. Scanner la codebase pour detecter les code smells
2. Classer et prioriser les refactorings par risque
3. Presenter le plan a l'utilisateur
4. Executer UN refactoring a la fois
5. Verifier compilation + references apres chaque changement
6. Repeter jusqu'a completion du plan

## Guide etape par etape

### Etape 1 : Scanner la codebase pour les code smells

Lancer toutes les detections en parallele avec Grep, Glob et Bash :

```
Glob : Assets/Scripts/**/*.cs                                    # Tous les fichiers C#
Bash : find Assets/Scripts -name "*.cs" -exec wc -l {} + | sort -rn | head -20  # Fichiers volumineux
Grep : "static\s+\w+\s+Instance" dans Assets/Scripts/**/*.cs    # Singletons
Grep : "void\s+Update\s*\(\)" dans Assets/Scripts/**/*.cs       # Update polling
Grep : "Find\(\"" dans Assets/Scripts/**/*.cs                    # Magic strings (Find)
Grep : "CompareTag\(\"" dans Assets/Scripts/**/*.cs              # Magic strings (Tags)
Grep : "StartCoroutine" dans Assets/Scripts/**/*.cs              # Coroutine spaghetti
Grep : "public\s+(?!void|static|override|class)" dans *.cs      # Champs publics exposes
Grep : "class\s+\w+\s*:\s*\w+" dans Assets/Scripts/**/*.cs      # Heritage (tracer les chaines)
```

### Etape 2 : Classer et prioriser

Utiliser le catalogue de refactoring ci-dessous pour classer chaque smell detecte.

#### Catalogue de refactoring Unity

| Smell | Pattern de detection (Grep) | Refactoring | Risque |
|-------|----------------------------|-------------|--------|
| God Manager (>500 lignes) | Fichiers .cs avec "Manager" > 500 lignes | Split en services focuses | Eleve |
| Singleton MonoBehaviour | `static.*Instance.*get` dans MonoBehaviour | Remplacer par SO + Service Locator | Eleve |
| Heritage profond (>3 niveaux) | Chaines de `class X : Y` sur >3 niveaux | Aplatir avec composition + interfaces | Eleve |
| Update polling | `Update()` avec checks booleens | Remplacer par events/callbacks | Moyen |
| God Update | `Update()` avec >5 responsabilites | Separer en composants distincts | Moyen |
| Feature envy | Methodes accedant intensivement aux donnees d'une autre classe | Deplacer la methode vers le proprietaire des donnees | Moyen |
| Primitive obsession | Groupes repetes de int/float/string | Extraire en value types/structs | Moyen |
| Magic strings | `"string"` dans Find/CompareTag/Animator | Remplacer par const/enum/SO | Faible |
| Champs publics Inspector | Nombreux champs `public` | `[SerializeField] private` + SO config | Faible |
| Methode geante (>50 lignes) | Methodes longues | Extraire des sous-methodes | Faible |

#### Seuils de detection

| Metrique | Seuil | Verdict |
|----------|-------|---------|
| Lignes par classe | > 500 | God class |
| Lignes par methode | > 50 | Methode trop longue |
| Methodes par classe | > 15 | Trop de responsabilites |
| Parametres par methode | > 5 | Parameter object necessaire |
| Niveaux d'heritage | > 3 | Aplatir la hierarchie |

Ordre de priorite : **Faible** (magic strings, champs publics, methodes longues) puis **Moyen** (Update polling, feature envy, God Update) puis **Eleve** (singletons, God classes, heritage).

### Etape 3 : Presenter le plan a l'utilisateur

Avant toute modification, presenter un tableau : `# | Fichier | Smell | Refactoring | Risque | Fichiers impactes`. Proposer `tout / selection / annuler`. Attendre la validation avant de commencer.

### Etape 4 : Executer UN refactoring a la fois

Pour chaque refactoring du plan valide :

```
1. Read : Lire le fichier cible completement
2. Grep : Identifier TOUTES les references au code qui va changer
         Grep : "NomClasse" dans Assets/Scripts/**/*.cs
         Grep : "NomMethode" dans Assets/Scripts/**/*.cs
3. Edit : Effectuer le changement (une seule modification atomique)
4. Edit : Mettre a jour toutes les references trouvees
5. Grep : Verifier qu'aucune reference orpheline ne subsiste
6. Passer au refactoring suivant
```

### Etape 5 : Verifier apres chaque changement

Apres chaque refactoring individuel :

```
1. Grep pour les anciens noms de classes/methodes : doit retourner 0 resultats
2. Grep pour les references cassees : "using.*OldNamespace" absent
3. Verifier coherence : les nouveaux fichiers sont dans le bon dossier
4. Verifier que les [SerializeField] et references Inspector ne sont pas casses
```

Si un probleme est detecte, annuler le changement et notifier l'utilisateur avant de continuer.

### Etape 6 : Repeter jusqu'a completion

Parcourir le plan dans l'ordre de priorite (risque faible en premier). Apres chaque refactoring termine, indiquer la progression :

```
[2/8] Termine : EnemyController.cs - Extraction de methodes
       Fichiers modifies : 1
       References mises a jour : 0
       Status : OK
```

## Recettes de refactoring

6 recettes detaillees avec code avant/apres dans `references/refactor-recipes.md` :

| Recette | Risque | Description |
|---------|--------|-------------|
| Singleton vers SO Service | Eleve | Remplacer les singletons MonoBehaviour par des ScriptableObjects injectes |
| God Manager vers services | Eleve | Decouper un manager monolithique en services focuses |
| Magic strings vers constantes | Faible | Extraire les strings en constantes et Animator.StringToHash |
| Coroutines vers async Awaitable | Moyen | Migrer les IEnumerator vers async Awaitable (Unity 6+) |
| References directes vers Event Channel | Moyen | Decouple publisher/subscriber avec ScriptableObject events |
| Old Input vers New Input System | Moyen | Migrer de UnityEngine.Input vers InputSystem |

## Regles strictes

- **JAMAIS** faire 2 refactorings en meme temps sur le meme fichier
- **JAMAIS** changer le comportement observable (refactoring != nouvelle feature)
- **JAMAIS** renommer un champ `[SerializeField]` sans avertir que les references Inspector seront perdues
- **JAMAIS** supprimer du code sans verifier toutes les references (Grep dans tout le projet)
- **JAMAIS** refactorer un fichier sans l'avoir lu completement d'abord
- **TOUJOURS** verifier la compilation apres chaque changement individuel
- **TOUJOURS** verifier les references cassees avec Grep apres un renommage
- **TOUJOURS** presenter le plan complet avant la premiere modification
- **TOUJOURS** commencer par les refactorings a risque faible
- **TOUJOURS** preferer le plus petit changement possible
- **TOUJOURS** utiliser Edit (pas Write) pour les modifications de fichiers existants
- **TOUJOURS** preserver les attributs Unity (`[SerializeField]`, `[Header]`, `[Tooltip]`, etc.)

## Skills connexes

- Generer du nouveau code propre ? Utiliser `/unity-code-gen` (Unity Code Gen)
- Audit de performance (detection sans refactoring) ? Utiliser `/perf-audit` (Unity Perf Audit)
- Tester le code apres refactoring ? Utiliser `/unity-test` (Unity Test)
- Diagnostiquer un bug decouvert pendant le refactoring ? Utiliser `/unity-debug` (Unity Debug)

## Troubleshooting

| Probleme | Solution |
|----------|----------|
| References Inspector cassees apres renommage de champ | Le champ `[SerializeField]` a ete renomme. Utiliser `[FormerlySerializedAs("oldName")]` pour migrer les donnees serialisees |
| Erreur de compilation apres split de classe | Verifier les `using` manquants dans les nouveaux fichiers et les references d'assembly definition |
| Comportement change apres refactoring | Annuler le changement (Edit pour restaurer), analyser la difference, et refaire avec une approche plus conservatrice |
| Prefab override perdu | Le champ a change de nom ou de type. Ajouter `[FormerlySerializedAs]` et re-verifier les prefabs concernes |
| Circular dependency apres split | Extraire une interface dans un assembly partage, ou inverser la dependance avec un event channel SO |
| Tests cassent apres refactoring | Les tests testaient l'implementation (noms de methodes) plutot que le comportement. Mettre a jour les tests pour utiliser les nouveaux noms |
| AnimatorController reference cassee | Les string parameters ont ete remplaces par des hash. Verifier que `Animator.StringToHash` est utilise avec la meme string que dans le controller |
| ScriptableObject reference null | L'asset SO n'a pas ete cree dans le projet. Creer l'asset via le menu `Create` et l'assigner dans l'Inspector |
