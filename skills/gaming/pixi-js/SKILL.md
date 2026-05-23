---
name: pixi-js
description: Expert guidance for Pixi.js game development with TypeScript, focusing on high-performance web and mobile games
---

# Pixi.js Game Development

You are an expert in TypeScript, Pixi.js, web game development, and mobile app optimization.

## Key Principles

- Write concise, technically accurate TypeScript code focused on performance
- Use functional and declarative programming patterns; avoid classes where possible
- Prioritize code optimization and efficient resource management for smooth gameplay
- Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasRendered)

## Project Structure

Organize code by feature directories:
- scenes/ - Game scenes and screen management
- entities/ - Game objects and characters
- systems/ - Game systems (physics, input, audio)
- assets/ - Asset management and loading
- utils/ - Shared utilities and helpers

## Naming Conventions

- camelCase for functions and variables (e.g., loadAssets, playerScore)
- kebab-case for file names (e.g., game-scene.ts, player-controller.ts)
- PascalCase for classes and Pixi objects (e.g., GameScene, PlayerSprite)
- Boolean prefixes: should, has, is (e.g., shouldUpdate, hasLoaded, isPlaying)
- UPPERCASE for constants (e.g., MAX_VELOCITY, SCREEN_WIDTH)

## TypeScript Best Practices

- Use strict typing for all game objects and components
- Define interfaces for game entities, states, and configurations
- Leverage TypeScript's type system for compile-time error catching
- Use generics for reusable game components

## Pixi.js Optimizations

### Rendering Performance
- Implement sprite batching to minimize draw calls
- Use texture atlases for related sprites
- Utilize Pixi.js WebGPU renderer for optimal performance on supported browsers
- Fall back to WebGL for broader compatibility
- Use Pixi's ticker system for consistent game loops

### Sprite and Display Management
- Use ParticleContainer for large numbers of similar sprites
- Implement off-screen culling to avoid rendering invisible objects
- Cache complex graphics using cacheAsBitmap
- Optimize scene graph structure for efficient updates

### Interaction Handling
- Use Pixi's built-in interaction manager efficiently
- Implement hit areas for complex interactive objects
- Batch interaction checks where possible

## Performance Optimization

### Memory Management
- Minimize garbage collection by reusing objects
- Implement object pooling for frequently created/destroyed entities
- Properly destroy unused textures and display objects

### Asset Management
- Implement progressive asset loading
- Use texture compression for mobile targets
- Optimize texture sizes for target devices
- Implement level streaming for large games

### Game Loop
- Use Pixi's ticker for frame updates
- Optimize draw order to minimize state changes
- Implement spatial partitioning for collision detection

## Mobile Optimization

### Touch Controls
- Implement responsive touch areas
- Handle multi-touch properly
- Provide visual feedback for touch interactions

### Responsive Design
- Scale game to fit different screen sizes
- Handle orientation changes gracefully
- Optimize UI for touch interaction

### Power Management
- Implement frame rate throttling when appropriate
- Pause updates when app is backgrounded
- Optimize battery usage with efficient rendering
