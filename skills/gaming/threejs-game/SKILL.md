---
name: threejs-game
description: Three.js game development. Use for 3D web games, WebGL rendering, game mechanics, physics integration, character controllers, camera systems, lighting, animations, and interactive 3D experiences in the browser.
---

# Three.js Game Development Skill

Comprehensive assistance with Three.js game development using WebGL, covering 3D rendering, game mechanics, physics, animations, and interactive browser-based games.

## When to Use This Skill

Activate this skill when:
- Building 3D web games with Three.js
- Implementing game mechanics (player movement, collisions, scoring)
- Setting up cameras, lighting, and scene management
- Loading 3D models (GLTF, OBJ, FBX)
- Handling user input (keyboard, mouse, touch, gamepad)
- Creating animations and character controllers
- Integrating physics engines (Cannon.js, Ammo.js)
- Optimizing 3D game performance
- Working with shaders and materials for game visuals

## Quick Reference

### Basic Game Setup

```javascript
import * as THREE from 'three';

// Create scene, camera, renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Game loop
function animate(time) {
  requestAnimationFrame(animate);

  // Update game logic here
  updatePlayer(time);
  updateEnemies(time);
  checkCollisions();

  renderer.render(scene, camera);
}

animate();
```

### Player Controller (Third-Person)

```javascript
class PlayerController {
  constructor(camera, target) {
    this.camera = camera;
    this.target = target;
    this.distance = 10;
    this.height = 5;
    this.rotationSpeed = 0.005;
    this.moveSpeed = 0.1;
  }

  update(input) {
    // Movement
    const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(this.target.quaternion);
    const right = new THREE.Vector3(1, 0, 0).applyQuaternion(this.target.quaternion);

    if (input.forward) this.target.position.add(forward.multiplyScalar(this.moveSpeed));
    if (input.backward) this.target.position.add(forward.multiplyScalar(-this.moveSpeed));
    if (input.left) this.target.position.add(right.multiplyScalar(-this.moveSpeed));
    if (input.right) this.target.position.add(right.multiplyScalar(this.moveSpeed));

    // Rotation
    if (input.rotateLeft) this.target.rotation.y += this.rotationSpeed;
    if (input.rotateRight) this.target.rotation.y -= this.rotationSpeed;

    // Update camera position
    const offset = new THREE.Vector3(0, this.height, this.distance);
    offset.applyQuaternion(this.target.quaternion);
    this.camera.position.copy(this.target.position).add(offset);
    this.camera.lookAt(this.target.position);
  }
}
```

### Input Handling

```javascript
class InputManager {
  constructor() {
    this.keys = {};
    this.mouse = { x: 0, y: 0, buttons: {} };

    window.addEventListener('keydown', (e) => this.keys[e.code] = true);
    window.addEventListener('keyup', (e) => this.keys[e.code] = false);
    window.addEventListener('mousemove', (e) => {
      this.mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
      this.mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    });
  }

  getInput() {
    return {
      forward: this.keys['KeyW'] || this.keys['ArrowUp'],
      backward: this.keys['KeyS'] || this.keys['ArrowDown'],
      left: this.keys['KeyA'] || this.keys['ArrowLeft'],
      right: this.keys['KeyD'] || this.keys['ArrowRight'],
      jump: this.keys['Space'],
      action: this.keys['KeyE'],
      rotateLeft: this.keys['KeyQ'],
      rotateRight: this.keys['KeyE']
    };
  }
}
```

### Collision Detection (Raycasting)

```javascript
function checkCollisions(player, obstacles) {
  const raycaster = new THREE.Raycaster();
  const directions = [
    new THREE.Vector3(1, 0, 0),   // right
    new THREE.Vector3(-1, 0, 0),  // left
    new THREE.Vector3(0, 0, 1),   // forward
    new THREE.Vector3(0, 0, -1),  // backward
  ];

  for (const direction of directions) {
    raycaster.set(player.position, direction);
    const intersects = raycaster.intersectObjects(obstacles);

    if (intersects.length > 0 && intersects[0].distance < 1.0) {
      return {
        collision: true,
        object: intersects[0].object,
        distance: intersects[0].distance,
        point: intersects[0].point
      };
    }
  }

  return { collision: false };
}
```

### Loading 3D Models (GLTF)

```javascript
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const loader = new GLTFLoader();

function loadCharacter(path) {
  return new Promise((resolve, reject) => {
    loader.load(
      path,
      (gltf) => {
        const model = gltf.scene;
        model.scale.set(1, 1, 1);
        scene.add(model);

        // Setup animations if available
        const mixer = new THREE.AnimationMixer(model);
        const animations = {};
        gltf.animations.forEach(clip => {
          animations[clip.name] = mixer.clipAction(clip);
        });

        resolve({ model, mixer, animations });
      },
      (progress) => {
        console.log(`Loading: ${(progress.loaded / progress.total * 100).toFixed(2)}%`);
      },
      (error) => reject(error)
    );
  });
}

// Usage
const character = await loadCharacter('/models/character.glb');
character.animations.idle.play();
```

### Basic Physics (Gravity & Jumping)

```javascript
class PhysicsBody {
  constructor(mesh) {
    this.mesh = mesh;
    this.velocity = new THREE.Vector3();
    this.onGround = false;
    this.gravity = -9.8;
    this.jumpPower = 5;
  }

  update(deltaTime) {
    // Apply gravity
    if (!this.onGround) {
      this.velocity.y += this.gravity * deltaTime;
    }

    // Apply velocity
    this.mesh.position.add(this.velocity.clone().multiplyScalar(deltaTime));

    // Ground check
    if (this.mesh.position.y <= 0) {
      this.mesh.position.y = 0;
      this.velocity.y = 0;
      this.onGround = true;
    }
  }

  jump() {
    if (this.onGround) {
      this.velocity.y = this.jumpPower;
      this.onGround = false;
    }
  }
}
```

### Interactive Objects (Picking)

```javascript
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

function onMouseClick(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(interactableObjects);

  if (intersects.length > 0) {
    const object = intersects[0].object;
    object.userData.onInteract?.();
  }
}

window.addEventListener('click', onMouseClick);
```

### Health & Damage System

```javascript
class Entity {
  constructor(mesh, maxHealth) {
    this.mesh = mesh;
    this.maxHealth = maxHealth;
    this.health = maxHealth;
    this.isDead = false;
  }

  takeDamage(amount) {
    if (this.isDead) return;

    this.health = Math.max(0, this.health - amount);

    if (this.health === 0) {
      this.die();
    }

    return this.health;
  }

  heal(amount) {
    this.health = Math.min(this.maxHealth, this.health + amount);
    return this.health;
  }

  die() {
    this.isDead = true;
    this.mesh.visible = false;
    // Trigger death animation, effects, etc.
  }
}
```

## Key Concepts

### Scene Graph
- Organize game objects hierarchically
- Use groups for complex objects
- Parent-child transformations

### Game Loop
- Use `requestAnimationFrame` for 60fps
- Calculate delta time for frame-independent movement
- Separate update logic from rendering

### Camera Systems
- **PerspectiveCamera**: First/third-person games
- **OrthographicCamera**: 2D/isometric games
- Implement camera follow and smooth transitions

### Lighting
- **AmbientLight**: Base illumination
- **DirectionalLight**: Sun/moonlight with shadows
- **PointLight**: Torches, explosions
- **SpotLight**: Flashlights, stage lights

### Performance Optimization
- Use instancing for repeated objects
- Implement frustum culling
- Use LOD (Level of Detail) for distant objects
- Minimize draw calls
- Use texture atlases
- Enable shadow map optimization

### Asset Loading
- Preload all assets before game start
- Show loading progress bar
- Use LoadingManager for coordination
- Cache loaded assets

## Common Game Patterns

### State Machine (Game States)

```javascript
class GameStateMachine {
  constructor() {
    this.states = {
      menu: new MenuState(),
      playing: new PlayingState(),
      paused: new PausedState(),
      gameOver: new GameOverState()
    };
    this.currentState = this.states.menu;
  }

  changeState(stateName) {
    this.currentState.exit();
    this.currentState = this.states[stateName];
    this.currentState.enter();
  }

  update(deltaTime) {
    this.currentState.update(deltaTime);
  }
}
```

### Object Pooling

```javascript
class ObjectPool {
  constructor(factory, initialSize = 10) {
    this.factory = factory;
    this.available = [];
    this.inUse = [];

    for (let i = 0; i < initialSize; i++) {
      this.available.push(factory());
    }
  }

  acquire() {
    let obj = this.available.pop();
    if (!obj) obj = this.factory();
    this.inUse.push(obj);
    return obj;
  }

  release(obj) {
    const index = this.inUse.indexOf(obj);
    if (index > -1) {
      this.inUse.splice(index, 1);
      this.available.push(obj);
    }
  }
}

// Usage
const bulletPool = new ObjectPool(() => createBullet(), 20);
const bullet = bulletPool.acquire();
// ... use bullet
bulletPool.release(bullet);
```

## Reference Files

Detailed documentation organized by topic:

- **getting_started.md** - Three.js fundamentals, setup, and basic concepts
- **game_development.md** - Game loop, player controllers, game mechanics
- **scene_graph.md** - Scene organization, hierarchy, transformations
- **materials.md** - Material types, shaders, visual effects
- **textures.md** - Texture loading, UV mapping, atlases
- **lighting.md** - Light types, shadows, HDR
- **cameras.md** - Camera types, controls, viewport management
- **geometry.md** - Built-in geometries, custom geometry, buffers
- **loading.md** - Asset loading (models, textures, audio)
- **animation.md** - Animation system, skeletal animation, tweens
- **interactivity.md** - Raycasting, picking, UI integration
- **effects.md** - Post-processing, particles, fog

## Resources

### Official Documentation
- Three.js Manual: https://threejs.org/manual/
- Three.js API: https://threejs.org/docs/
- Three.js Examples: https://threejs.org/examples/

### Physics Integration
- **Cannon.js**: Lightweight 3D physics
- **Ammo.js**: Full Bullet physics engine port
- **Rapier**: High-performance physics

### Useful Libraries
- **three-mesh-bvh**: Fast raycasting
- **three-pathfinding**: Navigation meshes
- **postprocessing**: Advanced effects

## Working with This Skill

### For Beginners
1. Start with basic scene setup
2. Learn the coordinate system
3. Understand the game loop
4. Practice with simple shapes before models

### For Game Development
1. Plan your game architecture
2. Implement input handling first
3. Build a simple player controller
4. Add gameplay mechanics incrementally
5. Optimize performance throughout

### For Advanced Features
1. Integrate physics engines
2. Implement advanced shaders
3. Add post-processing effects
4. Build multiplayer networking

## Notes

- Three.js uses a right-handed coordinate system (X right, Y up, Z out)
- Optimize early: profile regularly, minimize draw calls
- Use development builds for debugging, production builds for release
- Consider WebGL 2 features for modern browsers
- Mobile performance requires careful optimization
