---
name: flame-docs
description: "[Flame] Flame engine quick reference. Component lifecycle, Collision, Effects, Camera and core API reference. (project)"
---

# Flame Engine Quick Reference

## Component Lifecycle

```
onLoad() → onMount() → update(dt)/render(canvas) → onRemove()
```

| Method | Timing | Purpose |
|--------|--------|---------|
| `onLoad()` | Once, async | Resource loading, initialization |
| `onMount()` | On tree addition | Set parent/game references |
| `update(dt)` | Every frame | State update (dt = delta seconds) |
| `render(canvas)` | Every frame | Draw to screen |
| `onRemove()` | On removal | Cleanup |

---

## Core Classes

| Class | Purpose | Key Properties/Methods |
|-------|---------|------------------------|
| `FlameGame` | Game root | `pauseEngine()`, `resumeEngine()`, `overlays` |
| `World` | Hosts game components | `add()`, `children` |
| `Component` | Base component | `add()`, `remove()`, `children`, `parent` |
| `PositionComponent` | Position/size/rotation | `position`, `size`, `angle`, `anchor`, `scale` |
| `SpriteComponent` | Static sprite | `sprite`, `paint` |
| `SpriteAnimationComponent` | Animation | `animation`, `playing` |
| `CameraComponent` | Camera control | `follow()`, `moveTo()`, `setBounds()`, `viewport` |

### Shape Components
- `RectangleComponent` - Rectangle
- `CircleComponent` - Circle
- `PolygonComponent` - Polygon

---

## Collision Detection

### Enable
```dart
// Add to Game or World
class MyGame extends FlameGame with HasCollisionDetection {}
```

### Hitbox Types
| Hitbox | Purpose |
|--------|---------|
| `RectangleHitbox` | Rectangular collision area |
| `CircleHitbox` | Circular collision area |
| `PolygonHitbox` | Polygon (convex only) |
| `ScreenHitbox` | Screen boundaries |
| `CompositeHitbox` | Composite hitbox |

### Collision Callbacks
```dart
class MyComponent extends PositionComponent with CollisionCallbacks {
  @override
  void onCollisionStart(Set<Vector2> points, PositionComponent other) {}

  @override
  void onCollision(Set<Vector2> points, PositionComponent other) {}

  @override
  void onCollisionEnd(PositionComponent other) {}
}
```

### Collision Type (Performance)
- `CollisionType.active` - Checks against all hitboxes
- `CollisionType.passive` - Only checked by active (better performance)
- `CollisionType.inactive` - Ignored

---

## Effects System

| Effect | Purpose | Example |
|--------|---------|---------|
| `MoveEffect.to()` | Move to target | Character movement |
| `MoveEffect.by()` | Move by offset | Relative movement |
| `RotateEffect.to()` | Rotate to angle | Direction change |
| `ScaleEffect.to()` | Change size | Zoom in/out |
| `ColorEffect` | Color/opacity | Hit effect |
| `SequenceEffect` | Sequential execution | Complex animation |
| `OpacityEffect` | Opacity | Fade in/out |

### Effect Controller
```dart
MoveEffect.to(
  Vector2(100, 100),
  EffectController(duration: 1.0, curve: Curves.easeInOut),
);
```

---

## Camera & World

### Camera Methods
| Method | Purpose |
|--------|---------|
| `follow(target)` | Follow target |
| `moveTo(position)` | Move to coordinates |
| `moveBy(offset)` | Move by offset |
| `stop()` | Stop movement |
| `setBounds(shape)` | Limit camera movement |
| `canSee(component)` | Check visibility |

### Viewport Types
| Viewport | Purpose |
|----------|---------|
| `MaxViewport` | Expand to max space (default) |
| `FixedResolutionViewport` | Fixed resolution + aspect ratio |
| `FixedAspectRatioViewport` | Fixed aspect ratio, scales |
| `FixedSizeViewport` | Fixed size |

---

## Bridge Packages

### flame_riverpod (State Management)
```dart
// Game
class MyGame extends FlameGame with RiverpodGameMixin {}

// Component
class MyComponent extends Component with RiverpodComponentMixin {
  @override
  void onMount() {
    super.onMount();
    final state = ref.watch(myProvider);
  }
}

// Widget
RiverpodAwareGameWidget<MyGame>(
  game: game,
)
```

### flame_forge2d (Physics Engine)
```dart
class MyGame extends Forge2DGame {}

class MyBody extends BodyComponent {
  @override
  Body createBody() {
    final shape = CircleShape()..radius = 10;
    final fixtureDef = FixtureDef(shape);
    final bodyDef = BodyDef(type: BodyType.dynamic);
    return world.createBody(bodyDef)..createFixture(fixtureDef);
  }
}
```

### flame_audio (Audio)
```dart
// Sound effects
FlameAudio.play('explosion.mp3');

// BGM
FlameAudio.bgm.play('background.mp3');
FlameAudio.bgm.stop();
FlameAudio.bgm.pause();
FlameAudio.bgm.resume();
```

---

## Common Patterns

### Add Component
```dart
await add(MyComponent());  // In onLoad
add(MyComponent());        // In update
```

### Remove Component
```dart
removeFromParent();  // Self
component.removeFromParent();  // Other component
```

### Query Children
```dart
children.query<Enemy>();  // Find by type
componentsAtPoint(position);  // Find by position
findByKey(ComponentKey.named('player'));  // Find by key
```

### Priority (Z-order)
```dart
class MyComponent extends PositionComponent {
  MyComponent() : super(priority: 10);  // Higher = rendered on top
}
```

---

## Official Docs
- [Flame Docs](https://docs.flame-engine.org/latest/)
- [Components](https://docs.flame-engine.org/latest/flame/components.html)
- [Collision](https://docs.flame-engine.org/latest/flame/collision_detection.html)
- [Effects](https://docs.flame-engine.org/latest/flame/effects/effects.html)
- [Camera](https://docs.flame-engine.org/latest/flame/camera.html)
