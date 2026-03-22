---
name: "Unity Addressables"
description: "Asset loading et content management avec Addressables. Organisation des groupes, chargement async, memory management, remote content. Triggers: /addressables, /assets, 'Addressables', 'AssetReference', 'chargement async', 'remote content', 'DLC', 'asset bundles', 'Resources.Load migration', 'loading screen'."
---

# Unity Addressables

## Ce que fait cette skill

Guider l'utilisation du systeme Addressables pour le chargement d'assets asynchrone, l'organisation en groupes, la gestion memoire et le contenu distant (CDN/DLC). Couvre la migration depuis `Resources.Load`, le preloading avec progression, le reference counting et les patterns de release pour eviter les memory leaks.

## Prerequis

- Package `com.unity.addressables` installe via Package Manager

## Demarrage rapide

1. Installer le package : Window > Package Manager > Unity Registry > Addressables
2. Ouvrir Window > Asset Management > Addressables > Groups
3. Marquer des assets comme "Addressable" (checkbox dans l'Inspector)
4. Organiser en groupes logiques (par feature, par scene, par download)
5. Charger avec `Addressables.LoadAssetAsync<T>`

## Arbre de decision

```
Comment charger cet asset ?
|
+-- Toujours en memoire, reference directe dans l'Inspector ?
|   --> Reference directe [SerializeField] (pas besoin d'Addressables)
|
+-- Charge a la demande, connu au compile-time ?
|   --> AssetReference dans l'Inspector + LoadAssetAsync
|
+-- Charge dynamiquement par label/nom ?
|   --> Addressables.LoadAssetsAsync avec label
|
+-- Contenu telechargeable (DLC, patches) ?
|   --> Remote group + catalog update
|
+-- Migration depuis Resources.Load ?
    --> Marquer les assets comme Addressable, remplacer Resources.Load par LoadAssetAsync
```

## Guide etape par etape

### Step 1 : Organisation des groupes

- **Groupe par feature** : `Characters`, `Levels`, `UI`, `Audio`
- **Groupe par download** : `Core` (inclus dans le build), `Optional` (telechargeable)
- **Groupe par scene** si loading par scene
- Eviter les groupes trop gros (> 50 MB) : splitter en sous-groupes par usage
- Utiliser les labels pour tagger les assets transversaux (`level1`, `boss`, `tutorial`)

### Step 2 : Chargement async avec handle

```csharp
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;

public class AssetLoader : MonoBehaviour
{
    [SerializeField] private AssetReference prefabRef;
    private AsyncOperationHandle<GameObject> handle;

    public async Awaitable<GameObject> LoadAndInstantiateAsync()
    {
        handle = Addressables.LoadAssetAsync<GameObject>(prefabRef);
        await handle.Task;

        if (handle.Status == AsyncOperationStatus.Succeeded)
            return Instantiate(handle.Result);

        Debug.LogError($"Failed to load: {prefabRef}");
        return null;
    }

    private void OnDestroy()
    {
        // CRITIQUE: toujours release le handle
        if (handle.IsValid())
            Addressables.Release(handle);
    }
}
```

Points cles :
- `AssetReference` dans l'Inspector evite les magic strings
- `await handle.Task` pour attendre le chargement
- Toujours verifier `handle.Status` avant d'utiliser `handle.Result`
- `Release` dans `OnDestroy` pour eviter les leaks

### Step 3 : Chargement par label

```csharp
public class LabelLoader : MonoBehaviour
{
    [SerializeField] private AssetLabelReference labelRef;
    private AsyncOperationHandle<IList<GameObject>> handle;

    public async Awaitable<IList<GameObject>> LoadAllAsync()
    {
        handle = Addressables.LoadAssetsAsync<GameObject>(labelRef, null);
        await handle.Task;

        if (handle.Status == AsyncOperationStatus.Succeeded)
            return handle.Result;

        Debug.LogError($"Failed to load label: {labelRef}");
        return null;
    }

    private void OnDestroy()
    {
        if (handle.IsValid())
            Addressables.Release(handle);
    }
}
```

### Step 4 : Migration Resources.Load vers Addressables

```csharp
// AVANT (synchrone, tout en memoire au build)
var prefab = Resources.Load<GameObject>("Enemies/Goblin");

// APRES (async, charge a la demande)
var handle = Addressables.LoadAssetAsync<GameObject>("Enemies/Goblin");
await handle.Task;
var prefab = handle.Result;
// ... utiliser prefab ...
Addressables.Release(handle);
```

Etapes de migration :
1. Deplacer les assets hors du dossier `Resources/`
2. Marquer chaque asset comme Addressable (Inspector checkbox)
3. Verifier que l'address correspond a l'ancien path `Resources/`
4. Remplacer `Resources.Load<T>(path)` par `Addressables.LoadAssetAsync<T>(address)`
5. Ajouter `Release()` quand l'asset n'est plus necessaire
6. Supprimer le dossier `Resources/` une fois la migration terminee

### Step 5 : Scenes Addressables

```csharp
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.ResourceProviders;

public class SceneLoader : MonoBehaviour
{
    [SerializeField] private AssetReference sceneRef;
    private AsyncOperationHandle<SceneInstance> sceneHandle;

    public async Awaitable LoadSceneAsync()
    {
        sceneHandle = Addressables.LoadSceneAsync(sceneRef);
        await sceneHandle.Task;
    }

    public async Awaitable UnloadSceneAsync()
    {
        if (sceneHandle.IsValid())
        {
            await Addressables.UnloadSceneAsync(sceneHandle).Task;
        }
    }
}
```

## Regles strictes

- **TOUJOURS** appeler `Addressables.Release(handle)` quand l'asset n'est plus necessaire
- **TOUJOURS** utiliser `AssetReference` dans l'Inspector (pas de string addresses en dur)
- **TOUJOURS** gerer le cas d'echec de chargement (`handle.Status`)
- **TOUJOURS** utiliser `Addressables.ReleaseInstance()` au lieu de `Destroy()` pour les objets crees via `InstantiateAsync`
- **JAMAIS** de `Resources.Load` dans un nouveau projet (utiliser Addressables)
- **JAMAIS** garder un handle sans le release (memory leak)
- **JAMAIS** charger le meme asset deux fois sans reference counting
- **PREFERER** `AssetReferenceT<T>` pour typer les references (`AssetReferenceGameObject`, `AssetReferenceSprite`, etc.)
- **PREFERER** `AssetLabelReference` dans l'Inspector plutot que des strings de labels

## Skills connexes

- `/perf-audit` : detecter memory leaks et assets non release
- `/unity-build-config` : build content et remote catalog
- `/unity-code-gen` : generer loading system et asset managers

## Troubleshooting

| Probleme | Solution |
|----------|----------|
| "InvalidKeyException" | L'address ou le label n'existe pas. Verifier dans Addressables Groups window |
| Memory leak | Oubli de `Release()`. Utiliser le Profiler Addressables (Event Viewer) |
| Build ne contient pas l'asset | L'asset n'est dans aucun groupe ou le groupe n'est pas inclus dans le build |
| Chargement lent | Groupes trop gros. Splitter en sous-groupes par usage |
| "Cannot instantiate" | L'asset n'est pas un prefab ou le chargement a echoue (verifier Status) |
| "Exception during init" | Addressables pas initialise. Appeler `Addressables.InitializeAsync()` d'abord |
| Duplication d'assets | Un asset est dans plusieurs groupes. Utiliser le Build Report pour detecter |
| Remote catalog pas a jour | Appeler `CheckForCatalogUpdates` puis `UpdateCatalogs` au lancement |
