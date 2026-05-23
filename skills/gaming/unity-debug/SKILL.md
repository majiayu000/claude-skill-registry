---
name: "Unity Debug"
description: "Diagnostic et correction systematique de bugs Unity par analyse de code. Classifie le bug, trace le chemin d'execution, propose un fix avec prevention. Triggers: /unity-debug, /debug, 'bug Unity', 'NullReferenceException', 'crash Unity', 'erreur Unity', 'ne marche pas', 'comportement bizarre', 'MissingComponentException', 'glitch visuel', 'physics bug'. Utiliser quand l'utilisateur rapporte un bug, une erreur, un crash ou un comportement inattendu dans Unity. Produit un diagnostic structure : Symptome, Cause, Fix, Prevention."
---

# Unity Debug

Diagnostic et correction systematique de bugs Unity. Trace le chemin d'execution, identifie la cause racine, propose fix + prevention.

## Ce que fait cette skill

1. Collecte les symptomes (message d'erreur, stack trace, description)
2. Classifie le type de bug
3. Lit le code implique
4. Applique l'arbre diagnostique par categorie
5. Propose un fix avec explication
6. Ajoute du code defensif et des recommendations de prevention

## Prerequis

- Acces aux fichiers sources du projet Unity
- Idealement : le message d'erreur exact ou la stack trace
- Outils Claude Code uniquement (Read, Grep, Glob) — pas de MCP Unity requis

## Demarrage rapide

1. L'utilisateur decrit le bug ou colle l'erreur
2. Classifier le type de bug (voir categories)
3. Lire les fichiers impliques
4. Suivre l'arbre diagnostique
5. Produire le diagnostic au format : `Symptome | Cause | Fix | Prevention`

---

## Arbre de decision

```
Le bug est...
|
+-- Erreur de compilation (code rouge, pas de Play)
|   +-- COMPILE ERROR -> verifier syntaxe, references, asmdef
|
+-- Exception a l'execution (message en console, peut crasher)
|   +-- NullReferenceException        -> ARBRE NULL REF
|   +-- MissingComponentException     -> ARBRE MISSING COMPONENT
|   +-- MissingReferenceException     -> ARBRE DESTROYED OBJECT
|   +-- IndexOutOfRangeException      -> verifier tailles collections
|   +-- InvalidOperationException     -> verifier etat collection pendant iteration
|   +-- StackOverflowException        -> verifier recursion / boucle d'events
|   +-- OperationCanceledException    -> ARBRE ASYNC/AWAITABLE
|
+-- Comportement incorrect (pas d'erreur visible)
|   +-- LOGIC BUG -> tracer le chemin d'execution
|
+-- Performance (lag, stutter, freeze)
|   +-- Bug de perf specifique -> PERF ISSUE -> chercher allocations, Update lourd, physics
|   +-- Audit systematique     -> utiliser /perf-audit a la place
|
+-- Probleme visuel (rendu, UI, shader)
|   +-- VISUAL GLITCH -> verifier materials, sorting, render pipeline
|
+-- Probleme physique (traverse les murs, jitter)
|   +-- PHYSICS BUG -> verifier Update vs FixedUpdate, layers, scale
|
+-- Probleme async / Awaitable
    +-- ASYNC BUG -> ARBRE ASYNC/AWAITABLE
```

## Workflow de diagnostic

### 1 — Collecter les symptomes

Informations a obtenir de l'utilisateur :
- **Message d'erreur exact** (copie complete avec stack trace)
- **Quand ca arrive** (au lancement, apres une action, aleatoire)
- **Reproductibilite** (toujours, parfois, seulement en build)
- **Changements recents** (qu'est-ce qui a ete modifie avant que ca casse)

Si une stack trace est disponible, extraire :
- Le fichier et la ligne (`at Namespace.Class.Method () in File.cs:line X`)
- La chaine d'appel (qui appelle qui)

### 2 — Lire les fichiers impliques

```
Grep("class NomDuScript", type: "cs")        -> trouver le fichier
Read(fichier identifie)                       -> lire le code complet
Grep("GetComponent|Find|SendMessage", fichier) -> reperer les appels risques
Grep("void Update|void FixedUpdate", fichier)  -> reperer les hot paths
```

Pour les stack traces, lire CHAQUE fichier mentionne dans la chaine d'appel, du plus profond au plus haut.

### 3 — Appliquer l'arbre diagnostique

Arbres de diagnostic detailles : voir `references/diagnostic-trees.md`

### 4 — Proposer le fix

## Format de sortie

Format obligatoire pour chaque diagnostic :

```
## Diagnostic

**Symptome** : [description precise de ce qui se passe]
**Cause** : [explication technique de pourquoi ca arrive]
**Fix** : [code corrige avec diff ou snippet]
**Prevention** : [comment eviter ce bug a l'avenir]
```

## Code defensif — patterns

```csharp
// Null check avec log explicite
if (_target == null)
{
    Debug.LogWarning($"[{name}] Target reference is missing.", this);
    return;
}

// TryGetComponent au lieu de GetComponent
if (!TryGetComponent(out Rigidbody rb))
{
    Debug.LogError($"[{name}] Missing Rigidbody.", this);
    return;
}

// Verifier destruction avant callback
private IEnumerator DelayedAction()
{
    yield return new WaitForSeconds(1f);
    if (this == null) yield break;  // objet detruit pendant le wait
    DoAction();
}

// Desubscription propre
private void OnEnable() => _eventChannel.Subscribe(OnEvent);
private void OnDisable() => _eventChannel.Unsubscribe(OnEvent);
```

---

## Regles strictes

**TOUJOURS :**
- Lire le code source reel avant de diagnostiquer
- Tracer le chemin d'execution complet (pas de deduction sans preuve)
- Proposer une prevention en plus du fix
- Commencer par l'explication la plus simple (rasoir d'Occam)
- Verifier les references Inspector (champs `[SerializeField]` non assignes)
- Verifier l'ordre de lifecycle Unity (`Awake` -> `OnEnable` -> `Start`)
- Fournir le diagnostic au format `Symptome | Cause | Fix | Prevention`

**JAMAIS :**
- Deviner la cause sans lire le code
- Proposer un fix sans comprendre la cause racine
- Ignorer la stack trace (chaque ligne est un indice)
- Proposer `try/catch` comme fix (ca masque le bug, ca ne le resout pas)
- Supposer que le bug est dans Unity Engine (c'est presque toujours le code utilisateur)
- Proposer un fix qui introduit un nouveau probleme (regression)

---

## Skills connexes

- Le bug est un probleme de performance general, pas un cas specifique ? Utiliser `/perf-audit` (Unity Perf Audit)
- Le fix necessite un refactoring important ? Utiliser `/unity-refactor` (Unity Refactor)
- Le fix necessite de valider avec des tests ? Utiliser `/unity-test` (Unity Test)

## Troubleshooting

| Probleme | Solution |
|----------|----------|
| Pas de stack trace disponible | Demander a l'utilisateur de reproduire avec la console ouverte, ou chercher des `Debug.Log` existants pour tracer |
| Bug non reproductible | Chercher les race conditions, verifier si ca depend de l'ordre de chargement des scenes ou du framerate |
| Erreur dans un package tiers | Lire le code du package (`Library/PackageCache/`), chercher des issues connues, proposer un workaround |
| Bug seulement en build (pas en Editor) | Verifier : stripping de code (IL2CPP), differences de serialisation, `#if UNITY_EDITOR` mal place, SO modifies a runtime |
| Bug intermittent lie au framerate | Chercher du code dependant du frame dans `Update` qui devrait etre dans `FixedUpdate`, ou des comparaisons float sans epsilon |
| Performance degrade progressivement | Chercher des fuites : events non desubscrits, listes qui grandissent sans clear, objets instancies sans pool |

---

> Table des bugs courants : voir `references/common-bugs.md`
