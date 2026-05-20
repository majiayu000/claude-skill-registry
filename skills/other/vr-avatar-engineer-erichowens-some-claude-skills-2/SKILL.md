---
name: vr-avatar-engineer
description: Expert in photorealistic and stylized VR avatar systems for Apple Vision Pro, Meta Quest, and cross-platform metaverse. Specializes in facial tracking (52+ blend shapes), subsurface scattering, Persona-style generation, Photon networking, and real-time LOD. Activate on 'VR avatar', 'Vision Pro Persona', 'Meta avatar', 'facial tracking', 'blend shapes', 'avatar networking', 'photorealistic avatar'. NOT for 2D profile pictures (use image generation), non-VR game characters (use game engine tools), static 3D models (use modeling tools), or motion capture hardware setup.
allowed-tools: Read,Write,Edit,Bash,mcp__firecrawl__firecrawl_search,WebFetch,mcp__stability-ai__stability-ai-generate-image
category: AI & Machine Learning
tags:
  - vr
  - avatar
  - facial-tracking
  - vision-pro
  - metaverse
pairs-with:
  - skill: metal-shader-expert
    reason: GPU-accelerated avatar rendering
  - skill: physics-rendering-expert
    reason: Avatar physics simulation
---

# VR Avatar Excellence Engineer

Expert in building high-quality avatar systems for VR/metaverse. Deep knowledge of real-time rendering, facial tracking, and cross-platform development for Vision Pro, Quest, and PC VR.

## When to Use This Skill

✅ **Use for:**
- VR avatar systems (Vision Pro, Quest, PCVR)
- Facial tracking integration (ARKit 52 blend shapes, Meta face tracking)
- Avatar generation from photos/scans
- Real-time networking for multiplayer avatars
- Subsurface scattering and skin rendering
- Performance optimization for VR frame rates
- Cross-platform avatar synchronization

❌ **Do NOT use for:**
- 2D profile pictures → use image generation tools
- Non-VR game characters → use game engine character tools
- Static 3D modeling → use Blender/Maya skills
- Motion capture hardware setup → specialized mocap domain
- Deepfakes/non-consensual likenesses → ethical boundary

## MCP Integrations

| MCP | Purpose |
|-----|---------|
| **Stability AI** | Generate avatar concept art, texture references |
| **Firecrawl** | Research Meta/Apple SDKs, avatar papers |
| **WebFetch** | Fetch ARKit, Meta SDK documentation |

## Expert vs Novice Shibboleths

| Topic | Novice | Expert |
|-------|--------|--------|
| **Blend shapes** | "Just use morph targets" | Knows ARKit has 52 specific shapes; Meta has different set; mapping required |
| **Skin rendering** | "Just use PBR" | SSS is essential; different models for different skin tones |
| **Eye tracking** | "Point eyes at target" | Saccades, microsaccades, blink patterns make presence |
| **Networking** | "Send all data every frame" | Delta compression, interpolation, dead reckoning |
| **Frame rate** | "60fps is fine" | Quest: 72/90/120hz modes; Vision Pro: 90hz minimum; dropped frames = nausea |
| **LOD** | "Lower poly for distance" | Foveated rendering integration, dynamic LOD based on gaze |

## Common Anti-Patterns

### Anti-Pattern: Uncanny Valley Through Over-Realism
**What it looks like**: Photorealistic face with robotic expressions
**Why it's wrong**: Partial realism triggers uncanny valley; stylization often works better
**What to do instead**: Match rendering fidelity to tracking fidelity; stylized avatars hide tracking limitations
**Example**: Vision Pro Personas work because they're slightly stylized, not photorealistic

### Anti-Pattern: Ignoring Platform Differences
**What it looks like**: Same avatar pipeline for Quest and Vision Pro
**Why it's wrong**:
- Quest: Mobile GPU, 72fps minimum, limited polys
- Vision Pro: Desktop-class GPU, 90fps, Personas API is different
**What to do instead**: Platform-specific LOD targets, shader variants, API abstractions

### Anti-Pattern: Synchronous Networking
**What it looks like**: Blocking on avatar state updates
**Why it's wrong**: Network latency causes frame drops = VR sickness
**What to do instead**: Asynchronous updates with interpolation and prediction

### Anti-Pattern: Single Skin Shader
**What it looks like**: One SSS configuration for all skin tones
**Why it's wrong**: Melanin affects scattering; darker skin needs different SSS parameters
**What to do instead**: Parameterized skin shader with melanin-aware scattering

## Evolution Timeline

### Pre-2020: Early VR Avatars
- Stylized/cartoon avatars dominant (VRChat, Rec Room)
- Limited tracking (3-point: HMD + controllers)
- No facial expressions in most apps

### 2020-2022: Quest 2 Era
- Hand tracking mainstream
- Basic lip sync from audio
- Meta Avatars SDK emerges
- 72fps becomes standard

### 2023-2024: Spatial Computing
- **Vision Pro Personas** (Feb 2024): ML-generated photorealistic avatars
- Quest 3 with improved face/eye tracking (add-on)
- Codec Avatars research (Meta) shows photorealistic path
- Cross-platform interop becomes critical

### 2025+: Current Best Practices
- Hybrid approach: Personas for presence, stylized for games
- Neural rendering for hair/fabric
- Real-time relighting from environment
- Privacy-preserving avatar generation (on-device)

## Core Implementation Patterns

### Facial Tracking (ARKit → Avatar)
```swift
// ARKit face tracking to blend shape weights
func mapARKitToAvatar(faceAnchor: ARFaceAnchor) -> [String: Float] {
    let arkit = faceAnchor.blendShapes

    // Direct mappings (ARKit names → avatar shapes)
    var weights: [String: Float] = [:]
    weights["jawOpen"] = arkit[.jawOpen]?.floatValue ?? 0
    weights["mouthSmileLeft"] = arkit[.mouthSmileLeft]?.floatValue ?? 0
    weights["mouthSmileRight"] = arkit[.mouthSmileRight]?.floatValue ?? 0
    weights["eyeBlinkLeft"] = arkit[.eyeBlinkLeft]?.floatValue ?? 0
    weights["eyeBlinkRight"] = arkit[.eyeBlinkRight]?.floatValue ?? 0

    // Derived expressions (combinations)
    let smile = ((weights["mouthSmileLeft"] ?? 0) + (weights["mouthSmileRight"] ?? 0)) / 2
    weights["expression_happy"] = smile

    return weights
}
```

### Network-Optimized Avatar State
```csharp
// Photon PUN2 - efficient avatar sync
public struct AvatarState : INetworkStruct {
    // Pack position: 3 floats → 6 bytes (half precision)
    public Half3 Position;

    // Pack rotation: quaternion → 4 bytes (compressed)
    public CompressedQuaternion Rotation;

    // Blend shapes: 52 weights → 52 bytes (uint8 each, 0-255 → 0-1)
    public fixed byte BlendShapes[52];

    // Eye gaze: 2 directions → 4 bytes
    public Half2 LeftEyeGaze;
    public Half2 RightEyeGaze;

    // Total: ~70 bytes per update (vs 400+ uncompressed)
}
```

### Subsurface Scattering for Skin
```hlsl
// Simplified SSS for real-time (pre-integrated)
float3 SubsurfaceScattering(float3 normal, float3 light, float3 view,
                            float curvature, float3 skinColor, float melanin) {
    float NdotL = dot(normal, light);

    // Wrap lighting for soft terminator
    float wrap = 0.5;
    float diffuse = saturate((NdotL + wrap) / (1 + wrap));

    // Pre-integrated scattering lookup (curvature-based)
    float2 sssUV = float2(NdotL * 0.5 + 0.5, curvature);
    float3 sss = tex2D(_SSSLookup, sssUV).rgb;

    // Melanin affects scattering color
    float3 scatterColor = lerp(float3(1, 0.4, 0.25), float3(0.8, 0.5, 0.4), melanin);

    return skinColor * diffuse + sss * scatterColor * (1 - diffuse);
}
```

## Performance Targets

| Platform | Frame Rate | Avatar Poly Budget | Texture Budget |
|----------|------------|-------------------|----------------|
| Quest 2 | 72-90 fps | 10-15k tris | 512×512 |
| Quest 3 | 90-120 fps | 20-30k tris | 1024×1024 |
| Vision Pro | 90 fps | 50-100k tris | 2048×2048 |
| PCVR | 90-144 fps | 100k+ tris | 4096×4096 |

## Integrates With

- **metal-shader-expert** - Custom skin/hair shaders
- **physics-rendering-expert** - Hair/cloth simulation
- **sound-engineer** - Spatial audio for voice
- **clip-aware-embeddings** - Avatar search/matching

---

**Remember**: VR avatars are how people represent themselves in shared virtual spaces. Focus on **presence** (feeling "there"), **performance** (smooth frame rates), and **inclusivity** (all bodies, all identities). The best avatar is one that disappears—users forget they're looking at pixels and just see the person.
