---
name: gameplay-mechanics
version: "2.0.0"
description: |
  Core gameplay mechanics implementation, system interactions, feedback loops,
  and iterative balance refinement for engaging player experiences.
sasmp_version: "1.3.0"
bonded_agent: 01-game-designer
bond_type: PRIMARY_BOND

parameters:
  - name: mechanic_type
    type: string
    required: false
    validation:
      enum: [combat, movement, puzzle, progression, economy]
  - name: complexity
    type: string
    required: false
    validation:
      enum: [simple, moderate, complex]

retry_policy:
  enabled: true
  max_attempts: 3
  backoff: exponential

observability:
  log_events: [start, complete, error]
  metrics: [engagement_time, action_frequency, balance_score]
---

# Gameplay Mechanics Implementation

## Core Mechanics Framework

```
┌─────────────────────────────────────────────────────────────┐
│                    ACTION → EFFECT LOOP                      │
├─────────────────────────────────────────────────────────────┤
│  INPUT          PROCESS          OUTPUT          FEEDBACK   │
│  ┌─────┐       ┌─────────┐      ┌─────────┐    ┌─────────┐ │
│  │Press│──────→│Validate │─────→│Update   │───→│Visual   │ │
│  │Button│      │& Execute│      │State    │    │Audio    │ │
│  └─────┘       └─────────┘      └─────────┘    │Haptic   │ │
│                                                 └─────────┘ │
│                                                              │
│  TIMING REQUIREMENTS:                                        │
│  • Input → Response: < 100ms (feels responsive)             │
│  • Animation start: < 50ms (feels instant)                  │
│  • Audio feedback: < 20ms (in sync with action)             │
└─────────────────────────────────────────────────────────────┘
```

## Feedback Loop Design

```
FEEDBACK TIMING LAYERS:
┌─────────────────────────────────────────────────────────────┐
│  IMMEDIATE (0-100ms):                                        │
│  ├─ Button press sound                                      │
│  ├─ Animation start                                         │
│  ├─ Screen shake                                            │
│  └─ Controller vibration                                    │
│                                                              │
│  SHORT-TERM (100ms-1s):                                      │
│  ├─ Damage numbers appear                                   │
│  ├─ Health bar updates                                      │
│  ├─ Enemy reaction animation                                │
│  └─ Particle effects                                        │
│                                                              │
│  LONG-TERM (1s+):                                            │
│  ├─ XP/Score increase                                       │
│  ├─ Level up notification                                   │
│  ├─ Achievement unlock                                      │
│  └─ Story progression                                       │
└─────────────────────────────────────────────────────────────┘
```

## Combat Mechanics

```csharp
// ✅ Production-Ready: Combat State Machine
public class CombatStateMachine : MonoBehaviour
{
    public enum CombatState { Idle, Attacking, Blocking, Recovering, Staggered }

    [Header("Combat Parameters")]
    [SerializeField] private float attackDamage = 10f;
    [SerializeField] private float attackRange = 2f;
    [SerializeField] private float attackCooldown = 0.5f;
    [SerializeField] private float blockDamageReduction = 0.7f;
    [SerializeField] private float staggerDuration = 0.3f;

    private CombatState _currentState = CombatState.Idle;
    private float _stateTimer;

    public event Action<CombatState> OnStateChanged;
    public event Action<float> OnDamageDealt;
    public event Action<float> OnDamageTaken;

    public bool TryAttack()
    {
        if (_currentState != CombatState.Idle) return false;

        TransitionTo(CombatState.Attacking);
        StartCoroutine(AttackSequence());
        return true;
    }

    private IEnumerator AttackSequence()
    {
        // Wind-up phase
        yield return new WaitForSeconds(0.1f);

        // Active hit frame
        var hits = Physics.OverlapSphere(transform.position + transform.forward, attackRange);
        foreach (var hit in hits)
        {
            if (hit.TryGetComponent<IDamageable>(out var target))
            {
                target.TakeDamage(attackDamage);
                OnDamageDealt?.Invoke(attackDamage);
            }
        }

        // Recovery phase
        yield return new WaitForSeconds(attackCooldown);
        TransitionTo(CombatState.Idle);
    }

    public float TakeDamage(float damage)
    {
        float finalDamage = _currentState == CombatState.Blocking
            ? damage * (1f - blockDamageReduction)
            : damage;

        OnDamageTaken?.Invoke(finalDamage);

        if (finalDamage > 5f) // Stagger threshold
        {
            TransitionTo(CombatState.Staggered);
            StartCoroutine(RecoverFromStagger());
        }

        return finalDamage;
    }

    private void TransitionTo(CombatState newState)
    {
        _currentState = newState;
        _stateTimer = 0f;
        OnStateChanged?.Invoke(newState);
    }
}
```

## Resource Economy System

```
ECONOMY BALANCE FORMULA:
┌─────────────────────────────────────────────────────────────┐
│  INCOME vs EXPENDITURE:                                      │
│                                                              │
│  Hourly Income = (Enemies/hr × Gold/Enemy) + PassiveIncome  │
│  Hourly Spend  = (Upgrades + Consumables + Deaths)          │
│                                                              │
│  BALANCE RATIO:                                              │
│  • < 0.8: Too scarce (frustrating)                          │
│  • 0.8-1.2: Balanced (meaningful choices)                   │
│  • > 1.2: Too abundant (no tension)                         │
│                                                              │
│  EXAMPLE STAMINA SYSTEM:                                     │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Max: 100  │  Regen: 20/sec  │  On Hit: +10           │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │  Light Attack: -10  │  Heavy Attack: -25              │  │
│  │  Dodge: -15         │  Block: -5/hit                  │  │
│  │  Sprint: -5/sec     │  Jump: -8                       │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Progression Systems

```
PROGRESSION CURVE:
┌─────────────────────────────────────────────────────────────┐
│  Power                                                       │
│    ↑                                                         │
│    │                                    ╱───── Late Game     │
│    │                              ╱────╱       (slow, goals) │
│    │                        ╱────╱                           │
│    │                  ╱────╱                                 │
│    │            ╱────╱       Mid Game                        │
│    │      ╱────╱             (steady progress)               │
│    │ ╱───╱                                                   │
│    │╱ Early Game (fast, hook player)                        │
│    └────────────────────────────────────────────────→ Time   │
│                                                              │
│  XP CURVE FORMULA:                                           │
│  XP_needed(level) = base_xp × (level ^ growth_rate)         │
│  • growth_rate 1.5: Gentle curve (casual)                   │
│  • growth_rate 2.0: Standard curve (balanced)               │
│  • growth_rate 2.5: Steep curve (hardcore)                  │
└─────────────────────────────────────────────────────────────┘
```

```csharp
// ✅ Production-Ready: Progression Manager
public class ProgressionManager : MonoBehaviour
{
    [Header("Progression Config")]
    [SerializeField] private int baseXP = 100;
    [SerializeField] private float growthRate = 2.0f;
    [SerializeField] private int maxLevel = 50;

    private int _currentLevel = 1;
    private int _currentXP = 0;

    public event Action<int> OnLevelUp;
    public event Action<int, int> OnXPGained; // current, required

    public int XPForLevel(int level)
    {
        return Mathf.RoundToInt(baseXP * Mathf.Pow(level, growthRate));
    }

    public void AddXP(int amount)
    {
        _currentXP += amount;
        int required = XPForLevel(_currentLevel);

        OnXPGained?.Invoke(_currentXP, required);

        while (_currentXP >= required && _currentLevel < maxLevel)
        {
            _currentXP -= required;
            _currentLevel++;
            OnLevelUp?.Invoke(_currentLevel);
            required = XPForLevel(_currentLevel);
        }
    }

    public float GetProgressToNextLevel()
    {
        return (float)_currentXP / XPForLevel(_currentLevel);
    }
}
```

## Movement Mechanics

```
PLATFORMER FEEL PARAMETERS:
┌─────────────────────────────────────────────────────────────┐
│  MOVEMENT:                                                   │
│  • Walk Speed: 5-8 units/sec                                │
│  • Run Speed: 10-15 units/sec                               │
│  • Acceleration: 20-50 units/sec²                           │
│  • Deceleration: 30-60 units/sec² (snappier = higher)       │
│                                                              │
│  JUMP:                                                       │
│  • Jump Height: 2-4 units                                   │
│  • Jump Duration: 0.3-0.5 sec                               │
│  • Gravity: 20-40 units/sec²                                │
│  • Fall Multiplier: 1.5-2.5x (faster fall = tighter)       │
│                                                              │
│  FEEL ENHANCERS:                                             │
│  • Coyote Time: 0.1-0.15 sec (jump after leaving edge)      │
│  • Jump Buffer: 0.1-0.15 sec (early jump input)             │
│  • Variable Jump: Release = shorter jump                    │
│  • Air Control: 50-80% of ground control                    │
└─────────────────────────────────────────────────────────────┘
```

## Event-Driven Architecture

```
EVENT SYSTEM PATTERN:
┌─────────────────────────────────────────────────────────────┐
│  ACTION EXECUTED                                             │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              EVENT DISPATCHER                        │    │
│  │  DamageDealt(amount, position, type)                │    │
│  └─────────────────────────────────────────────────────┘    │
│       │                                                      │
│       ├──→ VFX System: Spawn damage numbers                 │
│       ├──→ Audio System: Play hit sound                     │
│       ├──→ UI System: Update health bar                     │
│       ├──→ Camera System: Screen shake                      │
│       ├──→ AI System: Alert nearby enemies                  │
│       └──→ Analytics: Log combat event                      │
│                                                              │
│  BENEFITS:                                                   │
│  • Systems don't need direct references                     │
│  • Easy to add/remove observers                             │
│  • Same event triggers multiple effects                     │
│  • Easy networking (replicate events)                       │
└─────────────────────────────────────────────────────────────┘
```

## Balance Iteration

```
RAPID BALANCE WORKFLOW:
┌─────────────────────────────────────────────────────────────┐
│  1. PLAYTEST (15-30 min)                                     │
│     → Watch players, note friction points                   │
│                                                              │
│  2. ANALYZE (5-15 min)                                       │
│     → What felt wrong? Too easy/hard?                       │
│     → Check telemetry data                                  │
│                                                              │
│  3. ADJUST (5-10 min)                                        │
│     → Change ONE variable at a time                         │
│     → Document the change                                   │
│                                                              │
│  4. TEST (5 min)                                             │
│     → Verify change has intended effect                     │
│                                                              │
│  5. REPEAT                                                   │
│     → Target: 4-6 iterations per hour                       │
└─────────────────────────────────────────────────────────────┘

BALANCE SPREADSHEET FORMAT:
┌──────────┬────────┬─────────┬─────────┬──────────┐
│ Weapon   │ Damage │ Speed   │ Range   │ DPS      │
├──────────┼────────┼─────────┼─────────┼──────────┤
│ Sword    │ 10     │ 1.0/sec │ 2m      │ 10.0     │
│ Axe      │ 20     │ 0.5/sec │ 1.5m    │ 10.0     │
│ Dagger   │ 5      │ 2.0/sec │ 1m      │ 10.0     │
│ Spear    │ 12     │ 0.8/sec │ 3m      │ 9.6      │
└──────────┴────────┴─────────┴─────────┴──────────┘
```

## 🔧 Troubleshooting

```
┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Controls feel unresponsive                         │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Add immediate audio/visual feedback on input              │
│ → Reduce input-to-action delay (< 100ms)                    │
│ → Add input buffering for combo actions                     │
│ → Check for frame rate issues                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: One strategy dominates all others                  │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Nerf dominant option OR buff alternatives                 │
│ → Add situational counters                                  │
│ → Create rock-paper-scissors relationships                  │
│ → Add resource costs to powerful options                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Players don't understand mechanic                  │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Add clearer visual/audio feedback                         │
│ → Create safe tutorial space                                │
│ → Use consistent visual language                            │
│ → Add UI hints or tooltips                                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Progression feels grindy                           │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Reduce XP requirements                                    │
│ → Add more XP sources                                       │
│ → Give meaningful rewards more frequently                   │
│ → Add catch-up mechanics for late content                   │
└─────────────────────────────────────────────────────────────┘
```

## Mechanic Comparison

| Mechanic | Skill Floor | Skill Ceiling | Feedback Speed |
|----------|-------------|---------------|----------------|
| Button Mash | Low | Low | Instant |
| Timing-Based | Medium | High | Instant |
| Resource Management | Medium | High | Delayed |
| Combo System | High | Very High | Instant |
| Strategic | Medium | Very High | Delayed |

---

**Use this skill**: When implementing core mechanics, balancing systems, or designing player feedback.
