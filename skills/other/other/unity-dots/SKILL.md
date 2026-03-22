---
name: "Unity DOTS"
description: "Data-Oriented Technology Stack (ECS, Job System, Burst). Authoring, baking, systems, queries, jobs paralleles. Triggers: /dots, /ecs, 'DOTS', 'ECS', 'ISystem', 'SystemAPI', 'IJobEntity', 'Burst', 'NativeArray', 'Entity', 'IComponentData', 'data oriented'."
---

# Unity DOTS — Data-Oriented Technology Stack

## Ce que fait cette skill

Guide l'implementation DOTS (Entity Component System + Job System + Burst Compiler) dans Unity 6+. Couvre le workflow complet authoring -> baking -> system -> query -> job pour des scenarios haute performance (milliers d'entites). Se concentre sur les API modernes : `ISystem`, `SystemAPI.Query`, `IJobEntity`. Les API depreciees (`Entities.ForEach`, `SystemBase` comme choix par defaut) ne sont pas recommandees.

## Prerequis

**Packages obligatoires** (via Package Manager ou `manifest.json`) :
- `com.unity.entities` (>= 1.3.x pour Unity 6)
- `com.unity.burst` (>= 1.8.x)
- `com.unity.collections` (>= 2.4.x)

**Optionnels** :
- `com.unity.entities.graphics` — rendu DOTS (Entities Graphics / Hybrid Renderer)
- `com.unity.physics` — physique DOTS (remplace PhysX classique pour les entites)
- `com.unity.transforms` — inclus dans entities, gestion LocalTransform

**Connaissances** : MonoBehaviour de base pour comprendre la transition authoring -> baking.

## Demarrage rapide

1. Installer les packages DOTS via Package Manager
2. Creer un authoring MonoBehaviour + un IComponentData (struct)
3. Creer un Baker pour la conversion authoring -> entity
4. Placer le GameObject dans un **SubScene** (obligatoire pour le baking)
5. Creer un ISystem avec SystemAPI.Query pour la logique
6. Ajouter `[BurstCompile]` sur le system et les jobs

## Arbre de decision

DOTS n'est pas toujours necessaire. Evaluer avant d'adopter :

```
Mon projet a-t-il besoin de DOTS ?
|
+-- Prototype / petit jeu (< 100 entites dynamiques) ?
|   --> NON. MonoBehaviour est plus simple et suffisant
|
+-- Jeu moyen (100-1000 entites) ?
|   --> PROBABLEMENT NON. Optimiser les MonoBehaviours d'abord
|
+-- Simulation massive (1000+ entites similaires) ?
|   --> OUI. DOTS brille ici (foules, particules custom, voxels, RTS)
|
+-- Besoin de calcul CPU intensif (pathfinding, IA, physique custom) ?
|   --> Job System + Burst SANS ECS. On peut utiliser les jobs seuls
|
+-- Migration d'un projet existant ?
|   --> Hybride : garder MonoBehaviours + ajouter DOTS pour les systemes critiques
|
+-- Nouveau projet from scratch avec beaucoup d'entites ?
    --> Full DOTS avec authoring/baking
```

### Roadmap ECS (Unity 6.4+)

- **Unity 6.4** : le package `com.unity.entities` transite vers un package core (integre a l'editeur, plus besoin de l'installer manuellement)
- **Unity 6.5 (prevu)** : changements structurels sur le type `Entity` (passage a un ID 64-bit). Impact : la serialisation custom et le stockage d'`Entity` dans des `NativeContainer` pourront etre affectes. Anticiper en evitant de persister des `Entity` bruts — utiliser des identifiants metier a la place.

Ces changements ne cassent pas le code existant dans Unity 6.0-6.3 mais sont importants pour les decisions d'architecture a long terme.

## Guide etape par etape

### Step 1 : Component (data only)

```csharp
// IComponentData = struct pure, pas de logique, juste des donnees
public struct MoveSpeed : IComponentData
{
    public float Value;
}

public struct RotationSpeed : IComponentData
{
    public float RadiansPerSecond;
}
```

Regles : pas de types managed (string, class, List), pas de methodes complexes. Un component = un aspect de l'entite.

### Step 2 : Authoring + Baker

```csharp
public class MoveSpeedAuthoring : MonoBehaviour
{
    public float Speed = 5f;
}

public class MoveSpeedBaker : Baker<MoveSpeedAuthoring>
{
    public override void Bake(MoveSpeedAuthoring authoring)
    {
        var entity = GetEntity(TransformUsageFlags.Dynamic);
        AddComponent(entity, new MoveSpeed { Value = authoring.Speed });
    }
}
```

L'authoring MonoBehaviour va sur le GameObject dans le SubScene. Le Baker convertit les donnees en entity au bake time.

### Step 3 : System (logique)

```csharp
[BurstCompile]
public partial struct MoveForwardSystem : ISystem
{
    [BurstCompile]
    public void OnUpdate(ref SystemState state)
    {
        float dt = SystemAPI.Time.DeltaTime;

        foreach (var (transform, speed) in
            SystemAPI.Query<RefRW<LocalTransform>, RefRO<MoveSpeed>>())
        {
            transform.ValueRW.Position +=
                transform.ValueRO.Forward() * speed.ValueRO.Value * dt;
        }
    }
}
```

### Step 4 : Job parallele (optionnel, pour encore plus de perf)

```csharp
[BurstCompile]
public partial struct MoveJob : IJobEntity
{
    public float DeltaTime;

    void Execute(ref LocalTransform transform, in MoveSpeed speed)
    {
        transform.Position += transform.Forward() * speed.Value * DeltaTime;
    }
}

// Dans le system :
[BurstCompile]
public void OnUpdate(ref SystemState state)
{
    new MoveJob { DeltaTime = SystemAPI.Time.DeltaTime }
        .ScheduleParallel();
}
```

## Regles strictes

**TOUJOURS** :
- Utiliser `ISystem` (struct) au lieu de `SystemBase` (class) — compatible Burst
- Ajouter `[BurstCompile]` sur les ISystem et les jobs
- Utiliser `SystemAPI.Query` (pas `Entities.ForEach` qui est deprecie)
- Utiliser `RefRO<T>` (lecture) / `RefRW<T>` (ecriture) pour l'acces aux components
- Placer les GameObjects authoring dans un **SubScene**
- Dispose les NativeContainers (sauf Allocator.Temp)
- Preferer `IJobEntity` pour le traitement parallele sur entites
- Preferer les enableable components (`IEnableableComponent`) aux ajouts/retraits dynamiques

**JAMAIS** :
- De types managed (string, class, List, arrays) dans les IComponentData
- D'acces au main thread depuis un job (pas de Debug.Log, pas d'API Unity classique)
- De NativeContainer sans Dispose (memory leak)
- De `Entities.ForEach` (deprecie Unity 6+)
- De `SystemBase` comme choix par defaut (sauf si managed types necessaires)

## Troubleshooting

| Probleme | Solution |
|----------|----------|
| "Burst compilation failed" | Types managed dans le code Burst. Utiliser `FixedString` au lieu de `string`, `NativeArray` au lieu de `List` |
| Entity pas creee | Baker manquant ou authoring pas dans un SubScene |
| System pas execute | Verifier le World. Ajouter `[UpdateInGroup(typeof(...))]` si necessaire |
| Performance pas meilleure | Verifier `[BurstCompile]` present. Profiler avec Burst Inspector |
| NativeArray leak warning | Toujours `Dispose()` dans `OnDestroy` ou utiliser `Allocator.Temp` |
| Query retourne 0 resultats | Verifier que les components sont bien ajoutes dans le Baker |
| "InvalidOperationException" dans un job | Acces concurrent. Utiliser `[NativeDisableParallelForRestriction]` ou revoir le design |
| SubScene ne bake pas | Reimporter le SubScene (clic droit > Reimport) ou redemarrer l'editeur |

## Skills connexes

- `/perf-audit` — Evaluer si DOTS est justifie pour le cas d'usage
- `/unity-code-gen` — Generation de boilerplate authoring/baker
- `/unity-animation` — DOTS animation (Entities Graphics animation)

## References

- Voir `references/ecs-patterns.md` pour les patterns de base (authoring, baking, queries, jobs)
- Voir `references/ecs-advanced.md` pour les patterns avances (Burst, NativeContainers, hybride, Aspects, DynamicBuffer)
- [Unity DOTS documentation officielle](https://docs.unity3d.com/Packages/com.unity.entities@latest)
- [Unity DOTS samples](https://github.com/Unity-Technologies/EntityComponentSystemSamples)
