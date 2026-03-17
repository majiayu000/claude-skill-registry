---
name: game-development
description: Game development with Unity, Unreal Engine, and Godot. Use when building games, implementing game mechanics, physics, AI, or working with game engines.
---

# Game Development

Comprehensive guide for building games across major engines and platforms.

## Engine Comparison

| Engine | Language | Best For | Platforms |
|--------|----------|----------|-----------|
| **Unity** | C# | Mobile, indie, VR/AR | All |
| **Unreal** | C++, Blueprints | AAA, realistic graphics | All |
| **Godot** | GDScript, C# | 2D, indie, open source | All |

---

## Unity (C#)

### Project Structure

```
Assets/
├── Scripts/
│   ├── Player/
│   │   ├── PlayerController.cs
│   │   └── PlayerInput.cs
│   ├── Enemies/
│   ├── Systems/
│   └── Utils/
├── Prefabs/
├── Scenes/
├── Materials/
├── Animations/
└── Resources/
```

### Player Controller

```csharp
using UnityEngine;
using UnityEngine.InputSystem;

[RequireComponent(typeof(CharacterController))]
public class PlayerController : MonoBehaviour
{
    [Header("Movement")]
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private float sprintMultiplier = 1.5f;
    [SerializeField] private float jumpHeight = 2f;
    [SerializeField] private float gravity = -9.81f;

    [Header("Look")]
    [SerializeField] private float lookSensitivity = 2f;
    [SerializeField] private float maxLookAngle = 80f;

    private CharacterController _controller;
    private Vector2 _moveInput;
    private Vector2 _lookInput;
    private Vector3 _velocity;
    private float _xRotation;
    private bool _isSprinting;

    private void Awake()
    {
        _controller = GetComponent<CharacterController>();
        Cursor.lockState = CursorLockMode.Locked;
    }

    private void Update()
    {
        HandleMovement();
        HandleLook();
        ApplyGravity();
    }

    private void HandleMovement()
    {
        float speed = _isSprinting ? moveSpeed * sprintMultiplier : moveSpeed;
        Vector3 move = transform.right * _moveInput.x + transform.forward * _moveInput.y;
        _controller.Move(move * speed * Time.deltaTime);
    }

    private void HandleLook()
    {
        float mouseX = _lookInput.x * lookSensitivity * Time.deltaTime;
        float mouseY = _lookInput.y * lookSensitivity * Time.deltaTime;

        _xRotation -= mouseY;
        _xRotation = Mathf.Clamp(_xRotation, -maxLookAngle, maxLookAngle);

        Camera.main.transform.localRotation = Quaternion.Euler(_xRotation, 0f, 0f);
        transform.Rotate(Vector3.up * mouseX);
    }

    private void ApplyGravity()
    {
        if (_controller.isGrounded && _velocity.y < 0)
        {
            _velocity.y = -2f;
        }

        _velocity.y += gravity * Time.deltaTime;
        _controller.Move(_velocity * Time.deltaTime);
    }

    // Input System callbacks
    public void OnMove(InputAction.CallbackContext context) =>
        _moveInput = context.ReadValue<Vector2>();

    public void OnLook(InputAction.CallbackContext context) =>
        _lookInput = context.ReadValue<Vector2>();

    public void OnJump(InputAction.CallbackContext context)
    {
        if (context.performed && _controller.isGrounded)
        {
            _velocity.y = Mathf.Sqrt(jumpHeight * -2f * gravity);
        }
    }

    public void OnSprint(InputAction.CallbackContext context) =>
        _isSprinting = context.performed;
}
```

### State Machine

```csharp
public interface IState
{
    void Enter();
    void Update();
    void Exit();
}

public class StateMachine
{
    private IState _currentState;

    public void ChangeState(IState newState)
    {
        _currentState?.Exit();
        _currentState = newState;
        _currentState.Enter();
    }

    public void Update() => _currentState?.Update();
}

// Example: Enemy AI States
public class IdleState : IState
{
    private readonly EnemyAI _enemy;

    public IdleState(EnemyAI enemy) => _enemy = enemy;

    public void Enter() => _enemy.Animator.SetTrigger("Idle");

    public void Update()
    {
        if (_enemy.CanSeePlayer())
        {
            _enemy.StateMachine.ChangeState(new ChaseState(_enemy));
        }
    }

    public void Exit() { }
}

public class ChaseState : IState
{
    private readonly EnemyAI _enemy;

    public ChaseState(EnemyAI enemy) => _enemy = enemy;

    public void Enter() => _enemy.Animator.SetTrigger("Run");

    public void Update()
    {
        _enemy.NavAgent.SetDestination(_enemy.Player.position);

        if (_enemy.InAttackRange())
        {
            _enemy.StateMachine.ChangeState(new AttackState(_enemy));
        }
        else if (!_enemy.CanSeePlayer())
        {
            _enemy.StateMachine.ChangeState(new IdleState(_enemy));
        }
    }

    public void Exit() { }
}
```

### Object Pooling

```csharp
public class ObjectPool<T> where T : Component
{
    private readonly T _prefab;
    private readonly Transform _parent;
    private readonly Queue<T> _pool = new();

    public ObjectPool(T prefab, int initialSize, Transform parent = null)
    {
        _prefab = prefab;
        _parent = parent;

        for (int i = 0; i < initialSize; i++)
        {
            CreateInstance();
        }
    }

    public T Get()
    {
        if (_pool.Count == 0) CreateInstance();

        T obj = _pool.Dequeue();
        obj.gameObject.SetActive(true);
        return obj;
    }

    public void Return(T obj)
    {
        obj.gameObject.SetActive(false);
        _pool.Enqueue(obj);
    }

    private void CreateInstance()
    {
        T obj = Object.Instantiate(_prefab, _parent);
        obj.gameObject.SetActive(false);
        _pool.Enqueue(obj);
    }
}
```

---

## Unreal Engine (C++)

### Actor Component

```cpp
// PlayerMovementComponent.h
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "PlayerMovementComponent.generated.h"

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class MYGAME_API UPlayerMovementComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UPlayerMovementComponent();

    virtual void TickComponent(float DeltaTime, ELevelTick TickType,
        FActorComponentTickFunction* ThisTickFunction) override;

    UFUNCTION(BlueprintCallable, Category = "Movement")
    void Move(FVector2D Input);

    UFUNCTION(BlueprintCallable, Category = "Movement")
    void Jump();

protected:
    virtual void BeginPlay() override;

private:
    UPROPERTY(EditAnywhere, Category = "Movement")
    float MoveSpeed = 600.0f;

    UPROPERTY(EditAnywhere, Category = "Movement")
    float JumpForce = 400.0f;

    UPROPERTY()
    class UCharacterMovementComponent* MovementComponent;
};

// PlayerMovementComponent.cpp
#include "PlayerMovementComponent.h"
#include "GameFramework/CharacterMovementComponent.h"

UPlayerMovementComponent::UPlayerMovementComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UPlayerMovementComponent::BeginPlay()
{
    Super::BeginPlay();

    if (ACharacter* Owner = Cast<ACharacter>(GetOwner()))
    {
        MovementComponent = Owner->GetCharacterMovement();
    }
}

void UPlayerMovementComponent::Move(FVector2D Input)
{
    if (!MovementComponent) return;

    FVector Forward = GetOwner()->GetActorForwardVector();
    FVector Right = GetOwner()->GetActorRightVector();

    FVector Direction = (Forward * Input.Y + Right * Input.X).GetSafeNormal();
    MovementComponent->AddInputVector(Direction * MoveSpeed);
}

void UPlayerMovementComponent::Jump()
{
    if (ACharacter* Character = Cast<ACharacter>(GetOwner()))
    {
        Character->Jump();
    }
}
```

### Gameplay Ability System (GAS)

```cpp
// MyGameplayAbility.h
#pragma once

#include "Abilities/GameplayAbility.h"
#include "MyGameplayAbility.generated.h"

UCLASS()
class MYGAME_API UMyGameplayAbility : public UGameplayAbility
{
    GENERATED_BODY()

public:
    UMyGameplayAbility();

    virtual void ActivateAbility(const FGameplayAbilitySpecHandle Handle,
        const FGameplayAbilityActorInfo* ActorInfo,
        const FGameplayAbilityActivationInfo ActivationInfo,
        const FGameplayEventData* TriggerEventData) override;

    virtual void EndAbility(const FGameplayAbilitySpecHandle Handle,
        const FGameplayAbilityActorInfo* ActorInfo,
        const FGameplayAbilityActivationInfo ActivationInfo,
        bool bReplicateEndAbility, bool bWasCancelled) override;

protected:
    UPROPERTY(EditDefaultsOnly, Category = "Ability")
    float Damage = 50.0f;

    UPROPERTY(EditDefaultsOnly, Category = "Ability")
    TSubclassOf<UGameplayEffect> DamageEffect;
};
```

---

## Godot (GDScript)

### Player Controller

```gdscript
extends CharacterBody3D

@export var move_speed: float = 5.0
@export var jump_velocity: float = 4.5
@export var mouse_sensitivity: float = 0.002

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")

@onready var camera: Camera3D = $Camera3D

func _ready() -> void:
    Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _input(event: InputEvent) -> void:
    if event is InputEventMouseMotion:
        rotate_y(-event.relative.x * mouse_sensitivity)
        camera.rotate_x(-event.relative.y * mouse_sensitivity)
        camera.rotation.x = clamp(camera.rotation.x, -PI/2, PI/2)

func _physics_process(delta: float) -> void:
    # Gravity
    if not is_on_floor():
        velocity.y -= gravity * delta

    # Jump
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity

    # Movement
    var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
    var direction := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

    if direction:
        velocity.x = direction.x * move_speed
        velocity.z = direction.z * move_speed
    else:
        velocity.x = move_toward(velocity.x, 0, move_speed)
        velocity.z = move_toward(velocity.z, 0, move_speed)

    move_and_slide()
```

### State Machine (GDScript)

```gdscript
# state_machine.gd
class_name StateMachine
extends Node

@export var initial_state: State

var current_state: State
var states: Dictionary = {}

func _ready() -> void:
    for child in get_children():
        if child is State:
            states[child.name.to_lower()] = child
            child.transitioned.connect(_on_child_transitioned)

    if initial_state:
        initial_state.enter()
        current_state = initial_state

func _process(delta: float) -> void:
    if current_state:
        current_state.update(delta)

func _physics_process(delta: float) -> void:
    if current_state:
        current_state.physics_update(delta)

func _on_child_transitioned(state: State, new_state_name: String) -> void:
    if state != current_state:
        return

    var new_state: State = states.get(new_state_name.to_lower())
    if not new_state:
        return

    current_state.exit()
    new_state.enter()
    current_state = new_state

# state.gd
class_name State
extends Node

signal transitioned(state: State, new_state_name: String)

func enter() -> void:
    pass

func exit() -> void:
    pass

func update(_delta: float) -> void:
    pass

func physics_update(_delta: float) -> void:
    pass
```

---

## Game Patterns

### Entity Component System (ECS)

```csharp
// Unity DOTS example
using Unity.Entities;
using Unity.Mathematics;
using Unity.Transforms;

public struct MoveSpeed : IComponentData
{
    public float Value;
}

public partial class MovementSystem : SystemBase
{
    protected override void OnUpdate()
    {
        float deltaTime = SystemAPI.Time.DeltaTime;

        Entities.ForEach((ref LocalTransform transform, in MoveSpeed speed) =>
        {
            transform.Position += new float3(0, 0, speed.Value * deltaTime);
        }).ScheduleParallel();
    }
}
```

### Event System

```csharp
public static class GameEvents
{
    public static event Action<int> OnScoreChanged;
    public static event Action<float> OnHealthChanged;
    public static event Action OnGameOver;

    public static void ScoreChanged(int newScore) => OnScoreChanged?.Invoke(newScore);
    public static void HealthChanged(float newHealth) => OnHealthChanged?.Invoke(newHealth);
    public static void GameOver() => OnGameOver?.Invoke();
}

// Usage
public class UIManager : MonoBehaviour
{
    private void OnEnable()
    {
        GameEvents.OnScoreChanged += UpdateScoreUI;
        GameEvents.OnHealthChanged += UpdateHealthUI;
    }

    private void OnDisable()
    {
        GameEvents.OnScoreChanged -= UpdateScoreUI;
        GameEvents.OnHealthChanged -= UpdateHealthUI;
    }
}
```

### Save System

```csharp
[Serializable]
public class SaveData
{
    public int Level;
    public float PlayTime;
    public Vector3Serializable PlayerPosition;
    public List<string> UnlockedAchievements;
}

public static class SaveSystem
{
    private static readonly string SavePath =
        Path.Combine(Application.persistentDataPath, "save.json");

    public static void Save(SaveData data)
    {
        string json = JsonUtility.ToJson(data, true);
        File.WriteAllText(SavePath, json);
    }

    public static SaveData Load()
    {
        if (!File.Exists(SavePath)) return new SaveData();

        string json = File.ReadAllText(SavePath);
        return JsonUtility.FromJson<SaveData>(json);
    }
}
```

---

## Performance Optimization

### LOD (Level of Detail)

```csharp
// Unity LOD Group setup
[RequireComponent(typeof(LODGroup))]
public class LODSetup : MonoBehaviour
{
    public Renderer[] lodRenderers;
    public float[] screenRelativeTransitions = { 0.5f, 0.2f, 0.01f };

    void Start()
    {
        LODGroup lodGroup = GetComponent<LODGroup>();
        LOD[] lods = new LOD[lodRenderers.Length];

        for (int i = 0; i < lodRenderers.Length; i++)
        {
            lods[i] = new LOD(screenRelativeTransitions[i], new[] { lodRenderers[i] });
        }

        lodGroup.SetLODs(lods);
        lodGroup.RecalculateBounds();
    }
}
```

### Spatial Partitioning

```csharp
public class QuadTree<T> where T : class
{
    private readonly int _maxObjects = 10;
    private readonly int _maxLevels = 5;
    private readonly int _level;
    private readonly List<(Rect bounds, T obj)> _objects = new();
    private readonly Rect _bounds;
    private QuadTree<T>[] _nodes;

    public QuadTree(int level, Rect bounds)
    {
        _level = level;
        _bounds = bounds;
    }

    public void Insert(Rect objBounds, T obj)
    {
        if (_nodes != null)
        {
            int index = GetIndex(objBounds);
            if (index != -1)
            {
                _nodes[index].Insert(objBounds, obj);
                return;
            }
        }

        _objects.Add((objBounds, obj));

        if (_objects.Count > _maxObjects && _level < _maxLevels)
        {
            if (_nodes == null) Split();

            int i = 0;
            while (i < _objects.Count)
            {
                int index = GetIndex(_objects[i].bounds);
                if (index != -1)
                {
                    var item = _objects[i];
                    _objects.RemoveAt(i);
                    _nodes[index].Insert(item.bounds, item.obj);
                }
                else i++;
            }
        }
    }

    public List<T> Retrieve(Rect area)
    {
        List<T> result = new();
        RetrieveAll(area, result);
        return result;
    }
}
```

---

## Checklist

### Pre-Production
- [ ] Game Design Document (GDD)
- [ ] Technical Design Document
- [ ] Art style guide
- [ ] Target platforms defined
- [ ] Performance budgets set

### Development
- [ ] Version control setup
- [ ] CI/CD for builds
- [ ] Automated testing
- [ ] Performance profiling regular
- [ ] Memory leak checks

### Release
- [ ] Platform certification requirements
- [ ] Localization complete
- [ ] Accessibility options
- [ ] Analytics integration
- [ ] Crash reporting
