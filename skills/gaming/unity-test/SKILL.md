---
name: "Unity Test"
description: "Generation et execution de tests Unity (NUnit, EditMode, PlayMode). Analyse le code existant, extrait la logique testable, genere les tests adaptes. Triggers: /test, /unity-test, 'NUnit', 'test unitaire Unity', 'PlayMode test', 'EditMode test', 'TDD Unity', 'ecrire des tests', 'tester mon code'."
---

# Unity Test

## Ce que fait cette skill

Generation de tests Unity production-ready. Analyse le code cible, determine le type de test optimal (EditMode ou PlayMode), extrait la logique testable des MonoBehaviours vers du C# pur, et genere les tests NUnit correspondants.

## Prerequis

- **Unity Test Framework** : package `com.unity.test-framework` (inclus par defaut)
- **NUnit** : inclus avec Unity Test Framework
- **Assembly Definitions** : un `.asmdef` par dossier de tests (EditMode et PlayMode separes)
- **Structure projet** : dossier `Tests/` a la racine d'`Assets/` avec sous-dossiers `EditMode/` et `PlayMode/`

## Demarrage rapide

1. Analyser le code cible (identifier dependances, side effects, I/O)
2. Determiner EditMode vs PlayMode via l'arbre de decision
3. Extraire la logique testable si le code est colle a un MonoBehaviour
4. Ecrire le test en suivant le template adapte
5. Verifier via Unity Test Runner (`Window > General > Test Runner`)

## Arbre de decision

```
Le code a tester...
|
+-- Est de la logique pure (maths, state, data) ?
|   +-- EditMode test (rapide, pas besoin de scene)
|
+-- Depend du lifecycle MonoBehaviour (Start, Update, OnCollision) ?
|   +-- PlayMode test (simule une scene)
|
+-- Utilise des coroutines ou Awaitable ?
|   +-- PlayMode test avec [UnityTest] ou async
|
+-- Valide un ScriptableObject ?
|   +-- EditMode test (instancie avec ScriptableObject.CreateInstance)
|
+-- Teste une integration multi-systemes ?
    +-- PlayMode Integration test (scene dediee)
```

**Regle principale** : si le code peut tourner sans `MonoBehaviour`, `GameObject`, ou scene Unity, c'est un EditMode test. Sinon, PlayMode.

## Guide etape par etape

### Step 1 : Analyser le code cible

Avant d'ecrire un test, identifier :
- **Entrees** : parametres, champs serialises, dependances injectees
- **Sorties** : valeurs de retour, changements d'etat, events emis
- **Side effects** : appels a `Destroy`, `Instantiate`, modifications de scene
- **Dependances Unity** : `MonoBehaviour`, `Transform`, `Physics`, `Time.deltaTime`

### Step 2 : Extraire la logique testable

Appliquer le pattern **"Extract to Testable"** quand la logique est collee a un MonoBehaviour.

```csharp
// AVANT : logique collee au MonoBehaviour (dur a tester)
public class PlayerHealth : MonoBehaviour
{
    [SerializeField] private int maxHealth = 100;
    private int currentHealth;

    private void Start() => currentHealth = maxHealth;

    public void TakeDamage(int amount)
    {
        currentHealth = Mathf.Max(0, currentHealth - amount);
        if (currentHealth <= 0) Die();
    }

    private void Die() { /* destroy, VFX, etc. */ }
}

// APRES : logique pure extraite (facile a tester en EditMode)
public static class HealthCalculator
{
    public static int CalculateDamage(int currentHealth, int damage)
        => Mathf.Max(0, currentHealth - damage);

    public static bool IsDead(int health) => health <= 0;
}

// Le MonoBehaviour delegue a la logique pure
public class PlayerHealth : MonoBehaviour
{
    [SerializeField] private int maxHealth = 100;
    private int currentHealth;

    private void Start() => currentHealth = maxHealth;

    public void TakeDamage(int amount)
    {
        currentHealth = HealthCalculator.CalculateDamage(currentHealth, amount);
        if (HealthCalculator.IsDead(currentHealth)) Die();
    }

    private void Die() { /* destroy, VFX, etc. */ }
}
```

**Benefice** : `HealthCalculator` est testable en EditMode, instantanement, sans scene.

### Step 3 : Setup Assembly Definitions

Creer deux fichiers `.asmdef` :

- `Assets/Tests/EditMode/Game.Tests.EditMode.asmdef` — plateforme `Editor` uniquement
- `Assets/Tests/PlayMode/Game.Tests.PlayMode.asmdef` — toutes plateformes

Les deux doivent referencer l'assembly runtime du jeu et avoir `UNITY_INCLUDE_TESTS` en `defineConstraints`.

Voir les templates complets dans `references/test-templates.md`.

### Step 4 : Ecrire le test

Suivre le template adapte au type de test. Conventions de nommage :

```
[MethodName]_[Condition]_[ExpectedResult]
```

Exemples :
- `CalculateDamage_NormalHit_ReducesHealth`
- `TakeDamage_Overkill_ClampsToZero`
- `Start_OnInitialize_SetsMaxHealth`

### Step 5 : Runner et verifier

1. Ouvrir Unity Test Runner : `Window > General > Test Runner`
2. Selectionner l'onglet EditMode ou PlayMode
3. Cliquer `Run All` ou selectionner des tests specifiques
4. Pour le coverage : `Window > Analysis > Code Coverage`

## Regles strictes

1. **TOUJOURS** utiliser `[SetUp]` pour initialiser et `[TearDown]` pour nettoyer
2. **TOUJOURS** nommer les tests : `MethodName_Condition_ExpectedResult`
3. **JAMAIS** de `Thread.Sleep` — utiliser `yield return null` ou `await`
4. **JAMAIS** d'acces filesystem ou reseau dans les EditMode tests
5. **TOUJOURS** utiliser `Assert.AreEqual(expected, actual, tolerance)` pour les floats
6. **Un test = un assert** (ou un groupe d'asserts sur le meme concept)
7. **Assembly definitions obligatoires** — ne jamais mettre les tests dans le main assembly
8. **TOUJOURS** detruire les GameObjects crees dans `[TearDown]` avec `Object.DestroyImmediate`
9. **TOUJOURS** utiliser `[TestCase]` pour les tests parametriques plutot que dupliquer
10. **JAMAIS** de dependance entre tests — chaque test est independant et idempotent

## Mocking sans framework externe

Unity n'inclut pas de framework de mocking. Utiliser des **interfaces + test doubles manuels** : creer une interface (ex: `IInputProvider`), implementer un mock avec des proprietes settables, injecter via `[SerializeField]` ou setter public.

Exemples complets dans `references/test-templates.md`.

## Skills connexes

- `/unity-code-gen` — generer les tests en meme temps que le code
- `/unity-refactor` — extraire la logique testable d'un MonoBehaviour existant
- `/unity-debug` — quand un test revele un bug a corriger
- `/perf-audit` — audit statique de performance (detecte les anti-patterns sans executer)

## Troubleshooting

| Probleme | Cause probable | Solution |
|----------|----------------|----------|
| Tests non detectes | `.asmdef` manquant ou mal configure | Verifier `defineConstraints` et `references` |
| PlayMode tres lent | Scene setup trop lourd | Minimiser : creer GameObjects vides, pas de prefabs complexes |
| Async test timeout | `CancellationToken` non gere | Passer le token, verifier la duree max |
| `NullReferenceException` dans `Start` | `yield return null` manquant apres `AddComponent` | Toujours yielder un frame apres creation |
| Tests passent en EditMode mais pas en build | Code conditionnel `#if UNITY_EDITOR` | Separer le code editor du code runtime |
| `Assert.AreEqual` echoue sur floats | Comparaison exacte de flottants | Utiliser la surcharge avec tolerance : `Assert.AreEqual(1.0f, val, 0.001f)` |
