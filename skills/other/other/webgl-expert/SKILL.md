---
name: webgl-expert
description: Expert guide for WebGL API development including 3D graphics, shaders (GLSL), rendering pipeline, textures, buffers, performance optimization, and canvas rendering. Use when working with WebGL, 3D graphics, canvas rendering, shaders, GPU programming, or when user mentions WebGL, OpenGL ES, GLSL, vertex shaders, fragment shaders, texture mapping, or 3D web graphics.
---

# WebGL Expert

Expert guide for WebGL (Web Graphics Library) API development, covering both WebGL 1.0 and WebGL 2.0 for high-performance 2D and 3D graphics rendering in web browsers.

## Overview

WebGL is a JavaScript API that enables hardware-accelerated 3D graphics rendering within HTML canvas elements without requiring plugins. It closely conforms to OpenGL ES 2.0 (WebGL 1.0) and OpenGL ES 3.0 (WebGL 2.0) standards.

**Key capabilities:**
- Hardware-accelerated 2D and 3D rendering
- Programmable shader pipeline (GLSL)
- Texture mapping and advanced materials
- Lighting and transformation systems
- High-performance graphics for games and visualizations
- Cross-platform compatibility (all modern browsers)

## Core Interfaces

### WebGLRenderingContext (WebGL 1.0)

The foundational interface for WebGL operations, obtained via canvas context:

```javascript
const canvas = document.querySelector('canvas');
const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

if (!gl) {
    console.error('WebGL not supported');
}
```

### WebGL2RenderingContext (WebGL 2.0)

Enhanced interface with advanced features:

```javascript
const gl = canvas.getContext('webgl2');

if (!gl) {
    console.log('WebGL 2 not supported, falling back to WebGL 1');
    gl = canvas.getContext('webgl');
}
```

**WebGL 2 exclusive features:**
- 3D textures
- Sampler objects
- Uniform Buffer Objects (UBO)
- Transform Feedback
- Vertex Array Objects (VAO) - core feature
- Instanced rendering
- Multiple render targets
- Integer textures and attributes
- Query objects
- Occlusion queries

## Rendering Pipeline

### 1. Shader Creation and Compilation

Shaders are programs written in GLSL (OpenGL Shading Language) that run on the GPU:

**Vertex Shader** - Processes each vertex:
```glsl
attribute vec3 aPosition;
attribute vec2 aTexCoord;
uniform mat4 uModelViewProjection;
varying vec2 vTexCoord;

void main() {
    gl_Position = uModelViewProjection * vec4(aPosition, 1.0);
    vTexCoord = aTexCoord;
}
```

**Fragment Shader** - Determines pixel colors:
```glsl
precision mediump float;
varying vec2 vTexCoord;
uniform sampler2D uTexture;

void main() {
    gl_FragColor = texture2D(uTexture, vTexCoord);
}
```

**JavaScript shader setup:**
```javascript
function createShader(gl, type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        console.error('Shader compilation error:', gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
        return null;
    }
    return shader;
}

function createProgram(gl, vertexShader, fragmentShader) {
    const program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);

    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        console.error('Program linking error:', gl.getProgramInfoLog(program));
        gl.deleteProgram(program);
        return null;
    }
    return program;
}
```

### 2. Buffer Management

Buffers store vertex data (positions, colors, normals, texture coordinates):

```javascript
// Create buffer
const positionBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

// Upload data
const positions = new Float32Array([
    -1.0, -1.0, 0.0,
     1.0, -1.0, 0.0,
     0.0,  1.0, 0.0
]);
gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);

// Set up attribute pointer
const positionLocation = gl.getAttribLocation(program, 'aPosition');
gl.enableVertexAttribArray(positionLocation);
gl.vertexAttribPointer(positionLocation, 3, gl.FLOAT, false, 0, 0);
```

**Buffer usage patterns:**
- `gl.STATIC_DRAW` - Data doesn't change
- `gl.DYNAMIC_DRAW` - Data changes occasionally
- `gl.STREAM_DRAW` - Data changes every frame

### 3. Texture Handling

```javascript
function loadTexture(gl, url) {
    const texture = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, texture);

    // Placeholder until image loads
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE,
                  new Uint8Array([255, 0, 255, 255]));

    const image = new Image();
    image.onload = () => {
        gl.bindTexture(gl.TEXTURE_2D, texture);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);

        // Generate mipmaps if power of 2
        if (isPowerOf2(image.width) && isPowerOf2(image.height)) {
            gl.generateMipmap(gl.TEXTURE_2D);
        } else {
            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        }
    };
    image.src = url;
    return texture;
}

function isPowerOf2(value) {
    return (value & (value - 1)) === 0;
}
```

### 4. Rendering Loop

```javascript
function render(gl, program) {
    // Clear canvas
    gl.clearColor(0.0, 0.0, 0.0, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // Enable depth testing
    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);

    // Use program
    gl.useProgram(program);

    // Set uniforms
    const projectionMatrix = mat4.create();
    mat4.perspective(projectionMatrix, Math.PI / 4, canvas.width / canvas.height, 0.1, 100.0);

    const uniformLocation = gl.getUniformLocation(program, 'uModelViewProjection');
    gl.uniformMatrix4fv(uniformLocation, false, projectionMatrix);

    // Draw
    gl.drawArrays(gl.TRIANGLES, 0, 3);

    // Animation loop
    requestAnimationFrame(() => render(gl, program));
}
```

## Matrix Mathematics

WebGL uses column-major matrices for transformations. Recommended libraries:
- **glMatrix** - Fast matrix/vector operations
- **three.js** - High-level 3D library with built-in math

**Common transformations:**
```javascript
// Model matrix (object transform)
const modelMatrix = mat4.create();
mat4.translate(modelMatrix, modelMatrix, [x, y, z]);
mat4.rotate(modelMatrix, modelMatrix, angle, [0, 1, 0]);
mat4.scale(modelMatrix, modelMatrix, [sx, sy, sz]);

// View matrix (camera)
const viewMatrix = mat4.create();
mat4.lookAt(viewMatrix, eyePosition, targetPosition, upVector);

// Projection matrix
const projectionMatrix = mat4.create();
mat4.perspective(projectionMatrix, fov, aspect, near, far);

// Combined MVP matrix
const mvpMatrix = mat4.create();
mat4.multiply(mvpMatrix, projectionMatrix, viewMatrix);
mat4.multiply(mvpMatrix, mvpMatrix, modelMatrix);
```

## Performance Optimization

### Best Practices

1. **Minimize state changes** - Batch draw calls with similar state
2. **Use Vertex Array Objects (VAO)** - Reduce attribute setup overhead
3. **Texture atlases** - Combine multiple textures into one
4. **Instanced rendering** - Draw many similar objects efficiently
5. **Frustum culling** - Don't render objects outside view
6. **Level of Detail (LOD)** - Use simpler models at distance
7. **Texture compression** - Use compressed texture formats (DXT, ETC, ASTC)
8. **Minimize shader complexity** - Keep fragment shaders simple
9. **Use uniform buffers** (WebGL 2) - Efficient uniform data sharing
10. **Avoid CPU-GPU synchronization** - Don't read back data frequently

### Instanced Rendering (WebGL 2)

```javascript
const ext = gl.getExtension('ANGLE_instanced_arrays'); // WebGL 1
// or use gl.drawArraysInstanced directly in WebGL 2

// Set up per-instance attribute
const instanceOffsetBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, instanceOffsetBuffer);
gl.bufferData(gl.ARRAY_BUFFER, offsetData, gl.STATIC_DRAW);

const offsetLocation = gl.getAttribLocation(program, 'aInstanceOffset');
gl.enableVertexAttribArray(offsetLocation);
gl.vertexAttribPointer(offsetLocation, 3, gl.FLOAT, false, 0, 0);
gl.vertexAttribDivisor(offsetLocation, 1); // Advance per instance

// Draw multiple instances
gl.drawArraysInstanced(gl.TRIANGLES, 0, vertexCount, instanceCount);
```

## Extension System

Check for and use extensions to access advanced features:

```javascript
function getExtension(gl, name) {
    const ext = gl.getExtension(name);
    if (!ext) {
        console.warn(`Extension ${name} not supported`);
    }
    return ext;
}

// Common extensions
const anisotropic = getExtension(gl, 'EXT_texture_filter_anisotropic');
const floatTextures = getExtension(gl, 'OES_texture_float');
const depthTexture = getExtension(gl, 'WEBGL_depth_texture');
const drawBuffers = getExtension(gl, 'WEBGL_draw_buffers');
const loseContext = getExtension(gl, 'WEBGL_lose_context'); // for testing
```

**Important extension categories:**
- **Texture formats:** WEBGL_compressed_texture_s3tc, WEBGL_compressed_texture_etc
- **Rendering:** WEBGL_draw_buffers, EXT_blend_minmax, EXT_frag_depth
- **Precision:** OES_texture_float, OES_texture_half_float
- **Instancing:** ANGLE_instanced_arrays (WebGL 1)
- **Debugging:** WEBGL_debug_renderer_info, WEBGL_debug_shaders

## Context Management

### Context Loss Handling

```javascript
canvas.addEventListener('webglcontextlost', (event) => {
    event.preventDefault();
    console.log('WebGL context lost');
    cancelAnimationFrame(animationId);
}, false);

canvas.addEventListener('webglcontextrestored', () => {
    console.log('WebGL context restored');
    initWebGL(); // Recreate all resources
    render();
}, false);
```

### Context Creation Options

```javascript
const gl = canvas.getContext('webgl2', {
    alpha: false,                    // No alpha channel (better performance)
    antialias: true,                 // Antialiasing (performance cost)
    depth: true,                     // Depth buffer
    stencil: false,                  // Stencil buffer
    premultipliedAlpha: true,        // Alpha premultiplication
    preserveDrawingBuffer: false,    // Keep buffer after render
    powerPreference: 'high-performance', // GPU preference
    failIfMajorPerformanceCaveat: false  // Fallback to software
});
```

## Common Patterns

### Framebuffer Rendering (Render to Texture)

```javascript
const framebuffer = gl.createFramebuffer();
gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffer);

const targetTexture = gl.createTexture();
gl.bindTexture(gl.TEXTURE_2D, targetTexture);
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, width, height, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);

gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, targetTexture, 0);

// Render to framebuffer
gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffer);
gl.viewport(0, 0, width, height);
// ... render scene ...

// Render to canvas
gl.bindFramebuffer(gl.FRAMEBUFFER, null);
gl.viewport(0, 0, canvas.width, canvas.height);
```

### Multiple Render Targets (WebGL 2)

```javascript
const ext = gl.getExtension('WEBGL_draw_buffers'); // WebGL 1
// Fragment shader outputs to multiple targets
gl.drawBuffers([
    gl.COLOR_ATTACHMENT0,
    gl.COLOR_ATTACHMENT1,
    gl.COLOR_ATTACHMENT2
]);
```

## Common Pitfalls

1. **Not checking compilation/linking errors** - Always check shader status
2. **Forgetting to enable attributes** - Call `gl.enableVertexAttribArray()`
3. **Incorrect data types** - Use `Float32Array`, `Uint16Array`, etc.
4. **Not handling context loss** - Add event listeners
5. **Mixing WebGL 1 and 2 APIs** - Check version compatibility
6. **Power-of-2 texture assumptions** - Handle non-POT textures correctly
7. **Z-fighting** - Insufficient depth buffer precision
8. **Coordinate system confusion** - WebGL uses clip space [-1, 1]
9. **Premature optimization** - Profile before optimizing
10. **Not clearing buffers** - Call `gl.clear()` each frame

## Debugging Tools

1. **Browser DevTools** - Check console for WebGL errors
2. **WebGL Inspector** - Browser extension for frame capture
3. **Spector.js** - WebGL debugging library
4. **gl.getError()** - Check for runtime errors
5. **WEBGL_debug_shaders** - Get translated shader source

```javascript
// Error checking
const error = gl.getError();
if (error !== gl.NO_ERROR) {
    console.error('WebGL error:', error);
}
```

## Popular Libraries and Frameworks

- **three.js** - Comprehensive 3D library with scene graph
- **Babylon.js** - Game engine with physics and VR support
- **PlayCanvas** - Cloud-based game engine
- **Pixi.js** - Fast 2D WebGL renderer
- **Phaser** - 2D game framework
- **regl** - Functional WebGL wrapper
- **twgl** - Tiny WebGL helper library
- **glMatrix** - High-performance matrix/vector library

## Learning Resources

- [MDN WebGL Tutorial](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/Tutorial)
- [WebGL Fundamentals](https://webglfundamentals.org/)
- [The Book of Shaders](https://thebookofshaders.com/)
- [Shadertoy](https://www.shadertoy.com/) - Shader examples
- [WebGL2 Fundamentals](https://webgl2fundamentals.org/)

## Quick Reference

See [reference.md](reference.md) for:
- Complete constant reference
- All WebGL methods
- GLSL built-in functions
- Extension compatibility matrix

See [examples](examples/) for:
- Basic triangle rendering
- Texture mapping
- Lighting models
- Advanced techniques

## Version Compatibility

When supporting both WebGL 1 and 2:

```javascript
function initWebGL(canvas) {
    const gl = canvas.getContext('webgl2');
    let version = 2;

    if (!gl) {
        gl = canvas.getContext('webgl');
        version = 1;
        console.log('Using WebGL 1');
    }

    // Feature detection
    const hasVAO = version === 2 || gl.getExtension('OES_vertex_array_object');
    const hasInstancing = version === 2 || gl.getExtension('ANGLE_instanced_arrays');

    return { gl, version, hasVAO, hasInstancing };
}
```

## Security Considerations

- **Cross-origin textures** - Use CORS properly
- **Shader validation** - Validate user-provided shader code
- **Resource limits** - Don't trust client-reported capabilities
- **Timing attacks** - Be aware of shader compilation timing
- **Context fingerprinting** - Users may block WebGL for privacy

---

When helping users with WebGL:

1. **Determine version** - Check if WebGL 1 or 2 is needed
2. **Check requirements** - Browser support, extensions needed
3. **Start simple** - Basic rendering before advanced features
4. **Debug systematically** - Check shaders, buffers, state in order
5. **Profile performance** - Use browser tools to identify bottlenecks
6. **Consider libraries** - Recommend three.js/Babylon.js for complex projects
7. **Validate inputs** - Check for null contexts, compilation errors
8. **Handle context loss** - Always implement recovery
9. **Optimize appropriately** - Don't over-optimize early
10. **Test across devices** - GPU capabilities vary significantly
