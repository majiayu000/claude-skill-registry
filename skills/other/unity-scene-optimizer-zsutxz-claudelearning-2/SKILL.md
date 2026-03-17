---
name: Unity Scene Optimizer
description: Analyzes scenes for performance bottlenecks (draw calls, batching, textures, GameObjects). Use when optimizing scenes or investigating performance issues.
allowed-tools: Read, Grep, Glob
---

# Unity Scene Optimizer

Analyzes Unity scenes and provides performance optimization recommendations for rendering, physics, memory, and platform-specific concerns.

## What This Skill Analyzes

### 1. Rendering Performance
Analyzes draw calls (target: <100 mobile, <2000 desktop), identifies batching opportunities, recommends material consolidation and static batching.

### 2. Texture Optimization
Reviews compression formats (BC7/ASTC), mipmap usage, texture atlasing, and platform-specific import settings.

### 3. GameObject Hierarchy
Targets: <500 GameObjects mobile, <2000 desktop. Identifies deep nesting, recommends object pooling and LOD groups.

### 4. Lighting and Shadows
Recommends baked lighting over realtime (1-2 lights mobile, 3-4 desktop), minimal shadow-casting lights.

### 5. Physics Optimization
Analyzes Rigidbody count, collider complexity, collision matrix configuration. Recommends simple colliders over Mesh colliders.

### 6. Mobile-Specific
Platform targets: 60 FPS iOS (iPhone 12+), 30-60 FPS Android. See [mobile-checklist.md](mobile-checklist.md) for complete requirements.

## Optimization Workflow

1. **Measure**: Frame Debugger, Stats, Profiler metrics
2. **Identify**: GPU/CPU/Memory/Physics bottlenecks
3. **Apply**: Quick wins (static batching, compression) → Medium (atlases, pooling, LOD) → Major (hierarchy refactor, culling)
4. **Validate**: Compare before/after metrics

See [optimization-workflow.md](optimization-workflow.md) for detailed steps and timelines.

## Platform-Specific Targets

| Platform | Draw Calls | Triangles | Texture Memory | Lights |
|----------|-----------|-----------|----------------|--------|
| **Mobile Low** | <50 | <20k | <100MB | 1 |
| **Mobile Mid** | <100 | <50k | <250MB | 1-2 |
| **Mobile High** | <150 | <100k | <500MB | 2-3 |
| **PC Low** | <500 | <200k | <1GB | 3-4 |
| **PC Mid** | <1000 | <500k | <2GB | 4-6 |
| **PC High** | <2000 | <1M | <4GB | 6-8 |
| **Console** | <1000 | <800k | <3GB | 4-6 |

## Tools Reference

Frame Debugger, Profiler, Stats Window, Memory Profiler. See [tools-reference.md](tools-reference.md) for usage and commands.

## Output Format

Provides: Current metrics, bottleneck identification, prioritized recommendations, performance impact estimates, implementation steps.

## When to Use vs Other Components

**Use this Skill when**: Analyzing scene performance, identifying bottlenecks, or getting optimization recommendations

**Use @unity-performance agent when**: Implementing complex optimizations, profiling at runtime, or troubleshooting specific performance issues

**Use @unity-architect agent when**: Redesigning scene architecture, implementing object pooling systems, or planning large-scale optimizations

**Use /unity:optimize-scene command when**: Running comprehensive scene analysis with detailed reports

## Related Skills

- **unity-script-validator**: For script-level performance issues
- **unity-template-generator**: For optimized component templates
