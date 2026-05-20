---
name: "Unity Animation"
description: "Animation avancee dans Unity : Animator, IK, Root Motion, Timeline, Playables API, Animation Rigging, blend trees. Triggers: /anim, /animation, 'Animator avance', 'IK', 'Root Motion', 'Timeline', 'Playables API', 'Animation Rigging', 'blend tree', 'state machine animation', 'animation events'."
---

# Unity Animation

## Ce que fait cette skill

Guider l'implementation d'animations avancees dans Unity. Couvre l'integration code-Animator, IK, Root Motion, Animation Rigging, Timeline, Playables API et blend trees avances.

Cette skill va au-dela de la simple configuration d'Animator Controller : elle fournit les patterns de code production-ready pour piloter les animations depuis le code, synchroniser la logique gameplay avec les keyframes, et exploiter les systemes avances (IK, Playables API, Timeline).

## Prerequis

- **Animator Controller** configure avec les states et transitions de base
- **Animation clips** importes (Humanoid ou Generic rig selon le cas)
- **(Optionnel)** Package **Animation Rigging** (`com.unity.animation.rigging`) pour l'IK
- **(Optionnel)** Package **Timeline** (`com.unity.timeline`) pour les cutscenes

## Demarrage rapide

1. Choisir le systeme d'animation adapte au besoin (voir arbre de decision)
2. Configurer l'Animator Controller (states, transitions, parametres)
3. Integrer avec le code (hash caches, parametres, events)
4. Affiner avec IK, blending avance, layers

## Arbre de decision

```
Quel systeme d'animation ?
|
+-- Animation simple (porte, plateforme, UI) ?
|   --> Animation component simple (legacy) ou Animator avec 1-2 states
|
+-- Personnage joueur ou ennemi avec etats (idle, run, attack) ?
|   --> Animator Controller + State Machine + code integration
|
+-- Animation cinematique / cutscene ?
|   --> Timeline (PlayableDirector + tracks)
|
+-- Melange dynamique d'animations a runtime ?
|   --> Playables API (mixer custom)
|
+-- IK (personnage regarde/attrape un objet) ?
|   --> Animation Rigging package (Rig Builder + constraints)
|
+-- Besoin de performance extreme (milliers d'entites) ?
    --> DOTS Animation (voir /unity-dots)
```

## Guide etape par etape

### Step 1 : Setup Animator + code integration

```csharp
[RequireComponent(typeof(Animator))]
public class CharacterAnimator : MonoBehaviour
{
    private Animator animator;

    // TOUJOURS cacher les hash (evite les string lookups chaque frame)
    private static readonly int SpeedHash = Animator.StringToHash("Speed");
    private static readonly int IsGroundedHash = Animator.StringToHash("IsGrounded");
    private static readonly int JumpTrigger = Animator.StringToHash("Jump");
    private static readonly int AttackTrigger = Animator.StringToHash("Attack");

    private void Awake() => animator = GetComponent<Animator>();

    public void SetSpeed(float speed) => animator.SetFloat(SpeedHash, speed);
    public void SetGrounded(bool grounded) => animator.SetBool(IsGroundedHash, grounded);
    public void TriggerJump() => animator.SetTrigger(JumpTrigger);
    public void TriggerAttack() => animator.SetTrigger(AttackTrigger);
}
```

### Step 2 : Animation Events

```csharp
// Appele depuis un clip d'animation a un keyframe precis
public void OnFootstep()
{
    audioService.PlaySFX(footstepClip);
}

public void OnAttackHit()
{
    // Activer hitbox au bon moment de l'animation
    hitbox.SetActive(true);
}

public void OnAttackEnd()
{
    hitbox.SetActive(false);
}
```

### Step 3 : StateMachineBehaviour (logique attachee aux states)

```csharp
public class AttackState : StateMachineBehaviour
{
    public override void OnStateEnter(
        Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
    {
        animator.GetComponent<CombatSystem>().OnAttackStart();
    }

    public override void OnStateExit(
        Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
    {
        animator.GetComponent<CombatSystem>().OnAttackEnd();
    }
}
```

### Step 4 : Animator Layers (animations partielles)

```csharp
// Controle dynamique du poids d'un layer (ex: upper body attack)
private static readonly int UpperBodyLayer = 1;

public void EnableUpperBodyOverride(float weight)
{
    animator.SetLayerWeight(UpperBodyLayer, weight);
}
```

- **Layer 0** : Base (locomotion complete)
- **Layer 1** : Upper Body Override (attaque, interaction) avec Avatar Mask
- **Layer 2** : Additive (breathing, hit reactions)

### Step 5 : Blend Trees pour la locomotion

Dans l'Animator Controller :
- Creer un Blend Tree 2D Freeform Directional
- Parametres : `MoveX` (float), `MoveY` (float)
- Motions : idle (0,0), walk forward (0,0.5), run forward (0,1), strafe left (-1,0), strafe right (1,0)

```csharp
private static readonly int MoveXHash = Animator.StringToHash("MoveX");
private static readonly int MoveYHash = Animator.StringToHash("MoveY");

public void SetMovement(Vector2 input)
{
    // Smooth damp pour eviter les changements brusques
    animator.SetFloat(MoveXHash, input.x, 0.1f, Time.deltaTime);
    animator.SetFloat(MoveYHash, input.y, 0.1f, Time.deltaTime);
}
```

## Regles strictes

**TOUJOURS :**
- Cacher les hash avec `Animator.StringToHash` (pas de strings dans Update)
- Utiliser les Animation Events pour synchroniser logique et animation (pas de timers manuels)
- Utiliser des Animator Layers pour les animations partielles (upper body attack + lower body run)
- Utiliser `SetFloat` avec damping pour des transitions fluides dans les blend trees
- Detruire les `PlayableGraph` dans `OnDestroy()` pour eviter les fuites memoire

**JAMAIS :**
- `GetComponent<Animator>()` dans Update -- cacher la reference dans Awake
- `transition duration = 0` sauf pour les state machines purement logiques (cause des snaps visuels)
- Modifier `transform.position` manuellement quand Root Motion est actif
- Utiliser `Play()` ou `CrossFade()` sans raison -- preferer les transitions de l'Animator Controller

**PREFERER :**
- Les Blend Trees 2D Freeform pour le mouvement directionnel
- Les Sub-State Machines pour organiser les Animator Controllers complexes
- Les Override Controllers pour reutiliser une state machine avec des clips differents
- Animation Rigging plutot que `OnAnimatorIK()` pour les nouveaux projets

## Skills connexes

- `/unity-code-gen` -- generer des StateMachineBehaviour et boilerplate Animator
- `/proto` -- prototyper rapidement avec des animations simples
- `/unity-dots` -- DOTS animation pour des milliers d'entites animees
- `/2d` -- animation 2D avec Sprite Library et Sprite Swap

## Troubleshooting

| Probleme | Solution |
|----------|----------|
| Animation ne joue pas | Verifier que le state est atteignable (transitions connectees), que le parametre est set correctement |
| Personnage glisse/flotte | Root Motion mal configure -- verifier "Apply Root Motion" sur l'Animator et les curves du clip |
| Blend Tree saccade | Verifier que les clips ont la meme cadence de pas (foot cycle). Ajuster le threshold |
| IK ne fonctionne pas | Verifier que le layer a "IK Pass" active dans l'Animator Controller |
| Animation Event pas appele | La methode doit etre publique, sur le meme GameObject que l'Animator, avec la bonne signature |
| Transition bloquee | Verifier les conditions de transition, desactiver "Has Exit Time" si transition immediate souhaitee |
| Layer override ne marche pas | Verifier l'Avatar Mask du layer, et que le weight > 0 |
| PlayableGraph leak | Toujours appeler `graph.Destroy()` dans `OnDestroy()` |
