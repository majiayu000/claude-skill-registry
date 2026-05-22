---
name: Bevy Game Engine
description: Data-driven game engine with ECS architecture.
metadata:
  labels: [rust, bevy, game, ecs]
  triggers:
    files: ['**/main.rs', 'assets/**']
    keywords: [bevy, App, Component, Query, Resource, Commands]
---

# Bevy Standards

## App Setup

```rust
use bevy::prelude::*;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, setup)
        .add_systems(Update, (movement, collision).chain())
        .run();
}

fn setup(mut commands: Commands) {
    commands.spawn(Camera2dBundle::default());
}
```

## Components

```rust
#[derive(Component)]
struct Player {
    speed: f32,
}

#[derive(Component)]
struct Health(u32);

#[derive(Component)]
struct Velocity(Vec2);

// Spawn entity with components
fn spawn_player(mut commands: Commands) {
    commands.spawn((
        Player { speed: 200.0 },
        Health(100),
        Velocity(Vec2::ZERO),
        SpriteBundle {
            transform: Transform::from_xyz(0.0, 0.0, 0.0),
            ..default()
        },
    ));
}
```

## Systems

```rust
// Query components
fn movement(
    time: Res<Time>,
    input: Res<Input<KeyCode>>,
    mut query: Query<(&Player, &mut Transform, &mut Velocity)>,
) {
    for (player, mut transform, mut velocity) in &mut query {
        let mut direction = Vec2::ZERO;
        if input.pressed(KeyCode::W) { direction.y += 1.0; }
        if input.pressed(KeyCode::S) { direction.y -= 1.0; }
        if input.pressed(KeyCode::A) { direction.x -= 1.0; }
        if input.pressed(KeyCode::D) { direction.x += 1.0; }

        velocity.0 = direction.normalize_or_zero() * player.speed;
        transform.translation += velocity.0.extend(0.0) * time.delta_seconds();
    }
}

// Filter queries
fn damage_enemies(
    mut query: Query<&mut Health, (With<Enemy>, Without<Player>)>,
) {
    for mut health in &mut query {
        health.0 = health.0.saturating_sub(10);
    }
}
```

## Resources

```rust
#[derive(Resource)]
struct GameState {
    score: u32,
    level: u32,
}

#[derive(Resource, Default)]
struct GameAssets {
    player_texture: Handle<Image>,
}

// Insert resource
app.insert_resource(GameState { score: 0, level: 1 });

// Access in system
fn update_score(mut state: ResMut<GameState>) {
    state.score += 10;
}
```

## Events

```rust
#[derive(Event)]
struct CollisionEvent {
    entity_a: Entity,
    entity_b: Entity,
}

// Send event
fn detect_collision(mut events: EventWriter<CollisionEvent>) {
    events.send(CollisionEvent { entity_a, entity_b });
}

// Read events
fn handle_collision(mut events: EventReader<CollisionEvent>) {
    for event in events.read() {
        println!("Collision: {:?} <-> {:?}", event.entity_a, event.entity_b);
    }
}

// Register event
app.add_event::<CollisionEvent>();
```

## States

```rust
#[derive(States, Debug, Clone, Eq, PartialEq, Hash, Default)]
enum GameState {
    #[default]
    Menu,
    Playing,
    Paused,
    GameOver,
}

app.add_state::<GameState>()
   .add_systems(OnEnter(GameState::Playing), start_game)
   .add_systems(OnExit(GameState::Playing), cleanup_game)
   .add_systems(Update, game_logic.run_if(in_state(GameState::Playing)));

// Change state
fn pause_game(mut next_state: ResMut<NextState<GameState>>) {
    next_state.set(GameState::Paused);
}
```

## Assets

```rust
fn load_assets(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    let texture = asset_server.load("player.png");
    commands.insert_resource(GameAssets { player_texture: texture });
}

// Spawn with texture
fn spawn_sprite(
    mut commands: Commands,
    assets: Res<GameAssets>,
) {
    commands.spawn(SpriteBundle {
        texture: assets.player_texture.clone(),
        ..default()
    });
}
```

## Plugins

```rust
pub struct PlayerPlugin;

impl Plugin for PlayerPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_player)
           .add_systems(Update, (movement, animation));
    }
}

// Use plugin
app.add_plugins(PlayerPlugin);
```

## Best Practices

1. **ECS**: Prefer composition over inheritance
2. **Systems**: Keep small, single responsibility
3. **Queries**: Use filters (`With`, `Without`) for performance
4. **Resources**: For global state, not per-entity data
5. **Events**: Decouple systems, avoid direct dependencies
