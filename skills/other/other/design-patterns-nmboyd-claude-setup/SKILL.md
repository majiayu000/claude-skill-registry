---
name: design-patterns
description: Software design patterns for Python and C++ development. Use when implementing creational patterns (Factory, Builder, Singleton), structural patterns (Adapter, Decorator, Facade), or behavioral patterns (Strategy, Observer, Command). Covers Gang of Four patterns with language-specific implementations, when to use each pattern, and common anti-patterns to avoid.
---

# Software Design Patterns

## Purpose

Guide for applying classic software design patterns in Python and C++ codebases. Patterns help solve common design problems with proven, reusable solutions.

## When to Use This Skill

Automatically activates when working on:
- Creating factories or builders
- Implementing plugin systems
- Decoupling components
- Managing object creation complexity
- Adding extensibility to existing code
- Refactoring tightly-coupled code

---

## Pattern Categories

| Category | Purpose | Common Patterns |
|----------|---------|-----------------|
| **Creational** | Object creation mechanisms | Factory, Builder, Singleton |
| **Structural** | Object composition | Adapter, Decorator, Facade |
| **Behavioral** | Object communication | Strategy, Observer, Command |

---

## Quick Reference: When to Use Each Pattern

| Problem | Pattern | Key Benefit |
|---------|---------|-------------|
| Create objects without specifying exact class | **Factory** | Decouples creation from usage |
| Complex object with many optional parameters | **Builder** | Readable, step-by-step construction |
| Ensure only one instance exists | **Singleton** | Global access (use sparingly!) |
| Make incompatible interfaces work together | **Adapter** | Integration without modification |
| Add behavior without modifying class | **Decorator** | Runtime extension |
| Simplify complex subsystem | **Facade** | Single entry point |
| Swap algorithms at runtime | **Strategy** | Flexible behavior |
| Notify multiple objects of changes | **Observer** | Loose coupling |
| Encapsulate requests as objects | **Command** | Undo/redo, queuing |

---

## Most Common Patterns (Quick Examples)

### Factory Method

```python
# Python
class ControllerFactory:
    _controllers = {"joint": JointController, "cartesian": CartesianController}

    @classmethod
    def create(cls, controller_type: str) -> Controller:
        return cls._controllers[controller_type]()

controller = ControllerFactory.create("joint")
```

```cpp
// C++
class ControllerFactory {
public:
    static std::unique_ptr<Controller> Create(const std::string& type) {
        if (type == "joint") return std::make_unique<JointController>();
        if (type == "cartesian") return std::make_unique<CartesianController>();
        throw std::invalid_argument("Unknown type");
    }
};
```

### Builder

```python
# Python - Fluent builder
config = (
    RobotConfigBuilder("Apollo", joint_count=7)
    .with_velocity(2.0)
    .with_collision(False)
    .build()
)
```

```cpp
// C++
auto config = RobotConfig::Builder("Apollo", 7)
    .WithVelocity(2.0)
    .WithCollision(false)
    .Build();
```

### Strategy

```python
# Python - Swap algorithms at runtime
class MotionController:
    def __init__(self, generator: TrajectoryGenerator) -> None:
        self._generator = generator

    def set_generator(self, generator: TrajectoryGenerator) -> None:
        self._generator = generator

    def move(self, start: float, end: float) -> np.ndarray:
        return self._generator.generate(start, end)

controller = MotionController(LinearTrajectory())
controller.set_generator(CubicTrajectory())  # Swap at runtime
```

### Observer

```python
# Python - Publish/subscribe
class StatePublisher:
    def __init__(self) -> None:
        self._observers: list[StateObserver] = []

    def subscribe(self, observer: StateObserver) -> None:
        self._observers.append(observer)

    def update_state(self, state: RobotState) -> None:
        for observer in self._observers:
            observer.on_state_change(state)

publisher = StatePublisher()
publisher.subscribe(Logger())
publisher.subscribe(SafetyMonitor())
```

### Decorator

```python
# Python - Add behavior via decorators
@timing
@retry(max_attempts=3)
@log_calls
def send_command(joint_id: int, position: float) -> bool:
    ...
```

### Facade

```python
# Python - Simplify complex subsystem
class RobotFacade:
    def move_to(self, target: Pose) -> bool:
        if not self._safety.is_safe():
            return False
        trajectory = self._motion.plan(target)
        if self._collision.check(trajectory):
            return False
        return self._controller.execute(trajectory)

robot = RobotFacade()
robot.move_to(target_pose)  # Simple interface
```

---

## Choosing the Right Pattern

### Creational Patterns

| Pattern | Choose When |
|---------|-------------|
| **Factory** | Don't know exact class until runtime |
| **Abstract Factory** | Need families of related objects |
| **Builder** | Many optional parameters, complex construction |
| **Singleton** | Exactly one instance needed (hardware, config) |
| **Prototype** | Cloning is cheaper than creating |

### Structural Patterns

| Pattern | Choose When |
|---------|-------------|
| **Adapter** | Converting interface A to interface B |
| **Decorator** | Adding behavior without subclassing |
| **Facade** | Simplifying complex API |
| **Composite** | Tree structures, part-whole hierarchies |
| **Proxy** | Lazy loading, access control, caching |
| **Bridge** | Abstraction and implementation vary independently |

### Behavioral Patterns

| Pattern | Choose When |
|---------|-------------|
| **Strategy** | Multiple interchangeable algorithms |
| **Observer** | One-to-many event notification |
| **Command** | Undo/redo, request queuing |
| **State** | Behavior depends on object state |
| **Template Method** | Common algorithm, varying steps |
| **Chain of Responsibility** | Multiple potential handlers |

---

## Anti-Patterns to Avoid

❌ **Singleton overuse** - Hides dependencies, makes testing hard
❌ **God object** - One class that does everything
❌ **Premature abstraction** - Adding patterns before they're needed
❌ **Pattern mania** - Using patterns for their own sake
❌ **Ignoring YAGNI** - Building extensibility you'll never use

---

## Pattern Selection Flowchart

```
Need to create objects?
├── Don't know class until runtime → Factory
├── Many optional parameters → Builder
├── Need exactly one instance → Singleton (carefully!)
└── Need related object families → Abstract Factory

Need to structure objects?
├── Convert interface → Adapter
├── Add behavior dynamically → Decorator
├── Simplify complex API → Facade
└── Tree structure → Composite

Need to manage behavior?
├── Swap algorithms → Strategy
├── Notify on changes → Observer
├── Undo/redo support → Command
└── State-dependent behavior → State
```

---

## Resource Files

### [creational-patterns.md](resources/creational-patterns.md)
Factory, Abstract Factory, Builder, Prototype, Singleton with full examples

### [structural-patterns.md](resources/structural-patterns.md)
Adapter, Bridge, Composite, Decorator, Facade, Proxy with full examples

### [behavioral-patterns.md](resources/behavioral-patterns.md)
Strategy, Observer, Command, State, Template Method, Chain of Responsibility

---

## Related Resources

- [Refactoring Guru - Design Patterns](https://refactoring.guru/design-patterns)
- [python-dev-guidelines](../../python/python-dev-guidelines/SKILL.md)
- [cpp-dev-guidelines](../../cpp/cpp-dev-guidelines/SKILL.md)

---

**Skill Status**: COMPLETE ✅
**Line Count**: < 450 ✅
**Progressive Disclosure**: Resource files for detailed patterns ✅
