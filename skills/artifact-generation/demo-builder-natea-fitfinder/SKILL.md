---
name: demo-builder
description: Automatically generate playable game demos from concept documents. Parses game designs, creates Three.js prototypes with scoring, characters, textures, and music. Transforms ideas into interactive experiences.
---

# Demo Builder Skill

## Purpose

This skill automatically generates playable game prototypes from game concept documents. It:
- **Parses concept documents** to extract game mechanics, theme, genre
- **Generates Three.js game code** using the threejs-game skill
- **Creates first playable level** with scoring, objectives, characters
- **Generates assets** (textures, colors, basic models)
- **Integrates music** (Suno AI generation or 8-bit MIDI)
- **Produces web-ready demo** that runs in browser

**Output**: Fully functional game demo with HTML/JS/CSS that can be played immediately.

## When to Use This Skill

Use this skill when you have:
- ✅ Game concept document (from brainstorming/design phases)
- ✅ Need to validate gameplay quickly with playable prototype
- ✅ Want to pitch game with interactive demo vs. static mockups
- ✅ Require rapid prototyping for playtesting
- ✅ Need proof-of-concept before full development investment

## Prerequisites

### Required Input

**Game Concept Document** (from brainstorming or design)
- Location: `/docs/*-game-concepts-*.md` or `/docs/plans/*-design.md`
- Must include: Title, description, genre, core mechanics, theme
- Example: `fps-game-concepts-market-driven-2025-10-26.md`

### Dependencies

- **threejs-game skill** (for 3D game implementation)
- Three.js library (loaded via CDN in generated HTML)
- Optional: Suno API key for music generation (can use MIDI fallback)

## Core Workflow

### Phase 1: Concept Parsing

**1. Load Game Concept**

```javascript
GameConcept = {
  title: string,
  description: string,
  genre: string[],  // ["FPS", "Extraction", "Co-op"]
  theme: string,    // "cyberpunk", "military", "horror", etc.
  core_mechanics: string[],
  target_persona: string,
  price_point: number | "F2P"
}
```

**2. Extract Demo Requirements**

```javascript
DemoRequirements = {
  game_type: "FPS" | "third-person" | "top-down" | "side-scroller",
  camera_type: "first-person" | "third-person" | "fixed" | "isometric",
  movement_type: "WASD" | "mouse" | "touch" | "hybrid",
  primary_mechanic: "shooting" | "extraction" | "survival" | "puzzle",
  color_palette: extractColorPalette(theme),
  character_archetypes: extractCharacters(description),
  objectives: extractObjectives(description),
  music_style: extractMusicStyle(genre, theme)
}
```

### Phase 2: Demo Architecture Design

**3. Generate Demo Specifications**

Based on genre/mechanics, create demo spec:

**FPS Demo Template:**
```javascript
{
  level: {
    type: "arena" | "corridor" | "open-world-section",
    size: {x: 100, y: 50, z: 100},
    geometry: "modular" // Can be expanded
  },
  player: {
    type: "fps-controller",
    spawn: {x: 0, y: 2, z: 0},
    health: 100,
    weapons: ["basic_rifle"],
    movement_speed: 5,
    look_sensitivity: 0.002
  },
  enemies: [
    {type: "basic_enemy", count: 5, spawn_pattern: "random"},
    {type: "patrol_enemy", count: 3, patrol_routes: [[...]]}
  ],
  objectives: [
    {type: "eliminate_targets", target_count: 5, points: 100},
    {type: "survive_time", duration: 60, points: 50},
    {type: "collect_items", item_count: 3, points: 150}
  ],
  scoring: {
    enemy_kill: 20,
    item_collect: 50,
    time_bonus: 1  // per second survived
  },
  ui: {
    hud: ["health", "ammo", "score", "timer"],
    crosshair: true,
    minimap: false
  }
}
```

**Extraction Shooter Demo Template:**
```javascript
{
  level: {
    type: "extraction-zone",
    zones: ["hot_zone", "neutral", "extract_point"],
    size: {x: 80, y: 30, z: 80}
  },
  player: {
    type: "tactical-controller",
    inventory_slots: 8,
    health: 100,
    stamina: 100
  },
  loot: [
    {type: "resource", count: 10, value: 10},
    {type: "rare_item", count: 3, value: 50}
  ],
  enemies: {
    type: "AI_guards",
    difficulty: "medium",
    count: 4
  },
  objectives: [
    {type: "extract_with_loot", min_value: 100, points: 200},
    {type: "extract_alive", points: 100}
  ],
  extraction_point: {x: 70, y: 1, z: 70},
  time_limit: 180  // 3 minutes
}
```

### Phase 3: Asset Generation

**4. Generate Color Palettes**

```javascript
function generateColorPalette(theme) {
  const palettes = {
    "cyberpunk": {
      primary: 0x00ffff,    // Cyan
      secondary: 0xff00ff,   // Magenta
      accent: 0xffff00,      // Yellow
      environment: 0x1a1a2e, // Dark blue-gray
      enemy: 0xff0080        // Pink
    },
    "military": {
      primary: 0x4a6741,     // Olive green
      secondary: 0x8b7355,   // Tan
      accent: 0xff6b35,      // Orange
      environment: 0x5a6650, // Gray-green
      enemy: 0xb71c1c        // Red
    },
    "horror": {
      primary: 0x1b1b1b,     // Almost black
      secondary: 0x8b0000,   // Dark red
      accent: 0xffffff,      // White
      environment: 0x2d2d2d, // Dark gray
      enemy: 0x4a0e0e        // Blood red
    },
    "space/sci-fi": {
      primary: 0x0a2e4a,     // Deep blue
      secondary: 0x2a9d8f,   // Teal
      accent: 0xe76f51,      // Orange-red
      environment: 0x000814, // Space black
      enemy: 0xf72585        // Bright pink
    }
  };

  return palettes[theme] || palettes["military"];
}
```

**5. Generate Textures (Procedural)**

```javascript
function generateTexture(type, color, size = 512) {
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');

  if (type === "floor") {
    // Grid pattern
    ctx.fillStyle = `#${color.toString(16).padStart(6, '0')}`;
    ctx.fillRect(0, 0, size, size);
    ctx.strokeStyle = '#000000';
    ctx.lineWidth = 2;
    for (let i = 0; i < size; i += size / 8) {
      ctx.beginPath();
      ctx.moveTo(i, 0);
      ctx.lineTo(i, size);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, i);
      ctx.lineTo(size, i);
      ctx.stroke();
    }
  } else if (type === "wall") {
    // Brick/panel pattern
    ctx.fillStyle = `#${color.toString(16).padStart(6, '0')}`;
    ctx.fillRect(0, 0, size, size);
    // Add panel lines
    const lighterColor = Math.min(color + 0x202020, 0xffffff);
    ctx.strokeStyle = `#${lighterColor.toString(16).padStart(6, '0')}`;
    ctx.lineWidth = 3;
    for (let i = 0; i < size; i += size / 4) {
      ctx.strokeRect(i, 0, size / 4, size);
    }
  }

  return new THREE.CanvasTexture(canvas);
}
```

**6. Generate Characters (Geometric)**

```javascript
function generateCharacter(type, color) {
  const group = new THREE.Group();

  if (type === "player") {
    // Simple capsule body
    const body = new THREE.Mesh(
      new THREE.CapsuleGeometry(0.5, 1.5, 4, 8),
      new THREE.MeshPhongMaterial({ color: color })
    );
    body.position.y = 1;
    group.add(body);

    // Weapon (for FPS)
    const weapon = new THREE.Mesh(
      new THREE.BoxGeometry(0.1, 0.1, 0.8),
      new THREE.MeshPhongMaterial({ color: 0x333333 })
    );
    weapon.position.set(0.3, 0.8, -0.5);
    group.add(weapon);

  } else if (type === "enemy") {
    // Hostile NPC
    const body = new THREE.Mesh(
      new THREE.BoxGeometry(0.8, 1.6, 0.6),
      new THREE.MeshPhongMaterial({ color: color })
    );
    body.position.y = 0.8;
    group.add(body);

    // Enemy marker (head)
    const head = new THREE.Mesh(
      new THREE.SphereGeometry(0.3, 8, 8),
      new THREE.MeshPhongMaterial({ color: 0xff0000, emissive: 0x330000 })
    );
    head.position.y = 2;
    group.add(head);
  }

  return group;
}
```

### Phase 4: Music Generation

**7. Generate Music (Suno AI or MIDI)**

```javascript
async function generateMusic(style, concept_name) {
  // Option 1: Suno API (if API key available)
  if (SUNO_API_KEY) {
    const prompt = generateMusicPrompt(style, concept_name);
    const musicUrl = await callSunoAPI(prompt);
    return musicUrl;
  }

  // Option 2: 8-bit MIDI fallback
  return generate8BitMIDI(style);
}

function generateMusicPrompt(style, concept_name) {
  const prompts = {
    "fps": `Epic action game music, intense electronic beats, military drums, adrenaline pumping, 140 BPM, game soundtrack, ${concept_name} theme`,
    "horror": `Dark atmospheric horror game music, eerie synths, unsettling ambience, tension building, 80 BPM, survival horror soundtrack`,
    "cyberpunk": `Synthwave cyberpunk game music, neon aesthetic, retro futuristic, energetic, 130 BPM, electronic game soundtrack`,
    "tactical": `Tactical stealth game music, suspenseful, orchestral strings, slow build tension, 90 BPM, espionage theme`,
    "roguelike": `Retro roguelike dungeon music, chiptune style, 8-bit adventure, upbeat tempo, 120 BPM, classic game feel`
  };

  return prompts[style] || prompts["fps"];
}

function generate8BitMIDI(style) {
  // Generate simple 8-bit style music pattern
  // Using Web Audio API for procedural chiptune
  const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

  const patterns = {
    fps: {
      tempo: 140,
      notes: ["C4", "E4", "G4", "C5", "G4", "E4"],  // Energetic pattern
      rhythm: [0.25, 0.25, 0.5, 0.25, 0.25, 0.5]
    },
    ambient: {
      tempo: 80,
      notes: ["C3", "E3", "G3", "B3", "G3", "E3"],  // Slower, eerie
      rhythm: [1, 1, 0.5, 0.5, 1, 1]
    }
  };

  return createChiptuneLoop(audioCtx, patterns[style] || patterns.fps);
}
```

### Phase 5: Game Code Generation

**8. Generate Complete Game Files**

Using threejs-game skill, generate:

**index.html:**
```html
<!DOCTYPE html>
<html>
<head>
  <title>[Game Title] - Demo</title>
  <style>
    body { margin: 0; overflow: hidden; font-family: Arial, sans-serif; }
    canvas { display: block; }
    #hud {
      position: absolute;
      top: 20px;
      left: 20px;
      color: white;
      font-size: 20px;
      text-shadow: 2px 2px 4px #000;
      pointer-events: none;
      z-index: 100;
    }
    #crosshair {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 20px;
      height: 20px;
      border: 2px solid white;
      border-radius: 50%;
      pointer-events: none;
    }
    #instructions {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(0,0,0,0.8);
      color: white;
      padding: 40px;
      text-align: center;
      border-radius: 10px;
    }
    .hidden { display: none !important; }
  </style>
</head>
<body>
  <div id="hud">
    <div>Health: <span id="health">100</span></div>
    <div>Score: <span id="score">0</span></div>
    <div>Enemies: <span id="enemies">0</span></div>
    <div>Time: <span id="timer">0</span></div>
  </div>
  <div id="crosshair"></div>
  <div id="instructions">
    <h1>[Game Title]</h1>
    <p>[Objective description]</p>
    <p><strong>Controls:</strong></p>
    <p>WASD - Move | Mouse - Look | Left Click - Shoot</p>
    <p>ESC - Pause</p>
    <button onclick="startGame()" style="padding: 15px 30px; font-size: 18px; cursor: pointer;">
      START DEMO
    </button>
  </div>

  <script type="importmap">
  {
    "imports": {
      "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
      "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
    }
  }
  </script>
  <script type="module" src="game.js"></script>
</body>
</html>
```

**game.js** (using threejs-game patterns):
```javascript
import * as THREE from 'three';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';

// Game state
const gameState = {
  running: false,
  health: 100,
  score: 0,
  enemies: [],
  startTime: 0,
  objectives: [/* parsed from concept */]
};

// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

// FPS Controls
const controls = new PointerLockControls(camera, renderer.domElement);

// Input handling
const input = {
  forward: false,
  backward: false,
  left: false,
  right: false,
  shoot: false
};

// Initialize game
function init() {
  // Renderer setup
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.shadowMap.enabled = true;
  document.body.appendChild(renderer.domElement);

  // Lighting (themed)
  const ambient = new THREE.AmbientLight([color from theme], 0.4);
  scene.add(ambient);

  const directional = new THREE.DirectionalLight(0xffffff, 0.6);
  directional.position.set(10, 20, 10);
  directional.castShadow = true;
  scene.add(directional);

  // Build level
  buildLevel(scene, [demo spec]);

  // Spawn enemies
  spawnEnemies(scene, [demo spec enemies]);

  // Setup input listeners
  setupInputListeners();
}

// Main game loop
function animate(time) {
  requestAnimationFrame(animate);

  if (!gameState.running) return;

  const delta = clock.getDelta();

  // Update player movement
  updatePlayer(delta);

  // Update enemies (AI patrol, chase)
  updateEnemies(delta);

  // Check collisions
  checkCollisions();

  // Update HUD
  updateHUD();

  // Check win/lose conditions
  checkObjectives();

  renderer.render(scene, camera);
}

// [Additional game logic functions generated based on concept]
```

### Phase 6: Demo Package Generation

**9. Create Complete Demo Package**

Generate folder structure:
```
demos/
  [game-name]-demo/
    index.html          (Main entry point)
    game.js             (Game logic using Three.js)
    assets/
      music.mp3         (Generated music)
      README.md         (Controls, objectives)
    package.json        (For npm serve if needed)
```

**10. Add Instructions README**

```markdown
# [Game Name] - Playable Demo

Auto-generated demo from game concept document.

## How to Play

1. Open `index.html` in a modern web browser
2. Click "START DEMO" and allow pointer lock
3. Use WASD to move, mouse to look
4. [Game-specific controls]
5. Complete objectives to win!

## Objectives

[Parsed from concept document]

## Controls

- **W/A/S/D**: Movement
- **Mouse**: Look around
- **Left Click**: [Primary action - shoot/interact]
- **ESC**: Pause/Menu

## About

This is an auto-generated prototype demonstrating core mechanics of [Game Name].

**Concept**: [Description from doc]
**Genre**: [Genre tags]
**Target**: [Persona summary]

Generated by demo-builder skill on [date]
```

## Implementation Protocol

### Step 1: Parse Concept Document

```javascript
TodoWrite([
  "Load game concept document from /docs",
  "Parse game title, description, genre, theme",
  "Extract core mechanics and objectives",
  "Identify camera type (FPS, third-person, etc.)",
  "Generate color palette from theme",
  "Extract character archetypes",
  "Determine music style",
  "Create demo specification document"
])
```

### Step 2: Generate Demo Architecture

```javascript
// Select appropriate demo template based on genre
if (genre.includes("FPS")) {
  demoTemplate = FPS_DEMO_TEMPLATE;
} else if (genre.includes("extraction")) {
  demoTemplate = EXTRACTION_DEMO_TEMPLATE;
} else if (genre.includes("roguelike")) {
  demoTemplate = ROGUELIKE_DEMO_TEMPLATE;
}

// Customize template with concept-specific details
demoSpec = customizeTemplate(demoTemplate, conceptData);
```

### Step 3: Generate Assets (Parallel)

```javascript
[Single Message - Parallel Asset Generation]:
  generateColorPalette(theme)
  generateTextures(palette)
  generateCharacterModels(archetypes, palette)
  generateMusicPrompt(genre, theme)
```

### Step 4: Generate Code (Using threejs-game skill)

Leverage threejs-game skill to generate:
- Scene setup with themed lighting
- Player controller (FPS or third-person)
- Enemy AI (patrol, chase behaviors)
- Scoring system
- Collision detection
- Win/lose conditions
- HUD elements

### Step 5: Package and Test

```javascript
[Single Message - Package Creation]:
  Write("demos/[game-name]-demo/index.html", htmlContent)
  Write("demos/[game-name]-demo/game.js", gameJsContent)
  Write("demos/[game-name]-demo/assets/README.md", instructions)
  Bash("npx serve demos/[game-name]-demo -p 3000")  // Test locally
```

### Step 6: Generate Music (Async)

If Suno API available:
```javascript
// Generate music in background while demo playable
musicPrompt = generateMusicPrompt(genre, theme, concept_name);
// Call Suno API (async, doesn't block demo generation)
// Add music file to assets/ when ready
```

Otherwise:
```javascript
// Use Web Audio API for procedural 8-bit music
generate8BitChiptune(style, tempo);
// Integrated directly in game.js
```

## Output Structure

### Minimal Demo (< 5 minutes to generate)

- **1 playable level** (~100x100 units)
- **Player character** with basic movement
- **3-5 enemies** with simple AI
- **1-2 objectives** (kill targets, survive time, collect items)
- **Basic scoring system**
- **Themed colors** (no custom textures)
- **Simple geometric shapes** for characters/environment
- **Procedural 8-bit music**

### Full Demo (< 15 minutes to generate)

Everything in Minimal +
- **Procedural textures** (floors, walls, objects)
- **More varied enemies** (5-10 with different behaviors)
- **Multiple objectives** (3-4 different types)
- **Power-ups/collectibles**
- **Win/lose screens**
- **Suno-generated music** (if API available)
- **Particle effects** (muzzle flash, explosions, impacts)

## Best Practices

### DO:
✅ Start with simplest playable version (iterate complexity)
✅ Use geometric primitives for speed (cubes, spheres, capsules)
✅ Generate procedural textures vs. loading image assets
✅ Implement core mechanic first (shooting, extraction, etc.)
✅ Test in browser immediately after generation
✅ Keep demo scope small (1 level, 5-10 minutes playtime)
✅ Add clear objectives and win conditions

### DON'T:
❌ Try to implement every feature from concept doc
❌ Load heavy 3D models (use geometric shapes)
❌ Create open-world demos (scope to arena/corridor)
❌ Implement complex AI (use simple patrol/chase)
❌ Wait for music generation to complete (async or skip)
❌ Require build tools (pure HTML/JS/CDN)

## Integration with Other Skills

### Required:
- **threejs-game**: Core 3D game implementation

### Optional:
- **brainstorming**: Provides concept docs as input
- **market-analyst**: Can prioritize which concepts to demo first
- **monetization-analyzer**: Demo top 3 monetizable concepts

### Typical Workflow:

```
brainstorming → game concepts document
           ↓
market-analyst → identify top concepts
           ↓
monetization-analyzer → rank by revenue potential
           ↓
demo-builder → generate playable demos of top 3
           ↓
playtesting → validate mechanics
           ↓
product-roadmap → plan full development
```

## Example: FPS Demo from Concept

**Input**: Sentinel Protocol concept (tactical 5v5 extraction shooter)

**Generated Demo**:
- **Level**: 80x80 unit tactical facility with rooms and corridors
- **Player**: FPS controller with rifle model
- **Enemies**: 5 AI guards with patrol routes
- **Objective**: Extract data (reach marked zone) while avoiding/eliminating guards
- **Scoring**: +50 per guard eliminated, +200 for successful extraction, -25 per hit taken
- **Theme**: Near-future corporate (cyan/gray color palette)
- **Music**: Synthwave tactical espionage (Suno-generated)
- **Win Condition**: Reach extraction zone with data
- **Time Limit**: 3 minutes

**Generation Time**: ~8 minutes
**Playable**: Yes, immediately in browser
**File Size**: ~100KB (HTML/JS), ~3MB (music)

## Summary

The Demo Builder Skill transforms game concept documents into playable prototypes by:

1. ✅ **Parsing concept docs** to extract mechanics, theme, objectives
2. ✅ **Generating demo architecture** using genre-specific templates
3. ✅ **Creating assets** (procedural textures, colors, geometric models)
4. ✅ **Leveraging threejs-game skill** for 3D implementation
5. ✅ **Integrating music** (Suno AI or procedural 8-bit)
6. ✅ **Packaging web-ready demo** (HTML/JS, no build required)

Output enables:
- Rapid validation of game concepts
- Interactive pitches for investors/publishers
- Playtesting core mechanics pre-production
- Demo reels for marketing
- Proof-of-concept for team alignment
