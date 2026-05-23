---
name: webgpu-canvas
description: WebGPU fundamentals for high-performance canvas rendering. Covers device initialization, buffer management, WGSL shaders, render pipelines, compute shaders, and web component integration. Use when building GPU-accelerated graphics, particle systems, or compute-intensive visualizations.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# WebGPU Canvas Development

Production patterns for WebGPU rendering integrated with web components. This skill covers device initialization, buffer management, shader development, and resource lifecycle management.

## Related Skills

- **`web-components`**: Component lifecycle for WebGPU cleanup, handleEvent pattern
- **`javascript`**: Async initialization, AbortController, memory management
- **`ux-accessibility`**: Reduced motion, canvas ARIA labels
- **`ux-animation-motion`**: Animation timing, frame-rate independence
- **`ipad-pro-design`**: Touch interactions, device pixel ratio

---

## WebGPU Browser Support (2025)

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome 113+ | Full support | Default enabled |
| Edge 113+ | Full support | Chromium-based |
| Safari 18+ | Full support | macOS/iOS |
| Firefox 139+ | Behind flag | Nightly only |

```javascript
// Feature detection
if (!navigator.gpu) {
  console.warn('WebGPU not supported, falling back to Canvas 2D');
  return;
}
```

---

## Rule 1: Initialize Once, Reuse Forever

Adapter and device acquisition is expensive. Initialize once at startup, store references.

```javascript
/**
 * WebGPU singleton for adapter/device management
 *
 * Skills applied:
 * - javascript: Singleton pattern, async initialization
 * - web-components: Integration with component lifecycle
 */
class WebGPUContext {
  static #adapter = null;
  static #device = null;
  static #initialized = false;
  static #initPromise = null;

  static async initialize() {
    // Prevent multiple initialization attempts
    if (this.#initPromise) return this.#initPromise;

    this.#initPromise = this.#doInitialize();
    return this.#initPromise;
  }

  static async #doInitialize() {
    if (this.#initialized) return { adapter: this.#adapter, device: this.#device };

    // Check support
    if (!navigator.gpu) {
      throw new Error('WebGPU not supported in this browser');
    }

    // Request adapter with fallback
    this.#adapter = await navigator.gpu.requestAdapter({
      powerPreference: 'high-performance' // or 'low-power' for battery
    });

    if (!this.#adapter) {
      throw new Error('No WebGPU adapter found');
    }

    // Request device with explicit limits
    this.#device = await this.#adapter.requestDevice({
      requiredFeatures: [],
      requiredLimits: {
        maxBindGroups: 4,
        maxUniformBufferBindingSize: 65536,
        maxStorageBufferBindingSize: 134217728 // 128MB
      }
    });

    // Handle device loss
    this.#device.lost.then((info) => {
      console.error('WebGPU device lost:', info.message);
      this.#initialized = false;
      this.#initPromise = null;

      // Attempt recovery if not destroyed intentionally
      if (info.reason !== 'destroyed') {
        this.initialize();
      }
    });

    this.#initialized = true;
    return { adapter: this.#adapter, device: this.#device };
  }

  static get adapter() { return this.#adapter; }
  static get device() { return this.#device; }
  static get initialized() { return this.#initialized; }
}

export { WebGPUContext };
```

**Why:** GPU device creation involves driver communication, memory allocation, and state setup. Multiple devices waste VRAM and cause performance issues.

---

## Rule 2: Configure Canvas Context Correctly

Canvas context configuration determines swap chain format, color space, and presentation mode.

```javascript
/**
 * Configure WebGPU canvas context
 *
 * @param {HTMLCanvasElement} canvas - Target canvas element
 * @param {GPUDevice} device - WebGPU device
 * @returns {GPUCanvasContext} Configured context
 */
function configureCanvasContext(canvas, device) {
  const context = canvas.getContext('webgpu');

  if (!context) {
    throw new Error('Failed to get WebGPU context from canvas');
  }

  // Get preferred format for this adapter
  const format = navigator.gpu.getPreferredCanvasFormat();

  context.configure({
    device,
    format,
    alphaMode: 'premultiplied', // or 'opaque' if no transparency needed
    colorSpace: 'srgb',         // Standard color space
    usage: GPUTextureUsage.RENDER_ATTACHMENT | GPUTextureUsage.COPY_SRC
  });

  return context;
}

// Handle device pixel ratio for crisp rendering
function resizeCanvasToDisplaySize(canvas) {
  const dpr = window.devicePixelRatio || 1;
  const displayWidth = Math.floor(canvas.clientWidth * dpr);
  const displayHeight = Math.floor(canvas.clientHeight * dpr);

  if (canvas.width !== displayWidth || canvas.height !== displayHeight) {
    canvas.width = displayWidth;
    canvas.height = displayHeight;
    return true; // Canvas was resized
  }
  return false;
}
```

### Alpha Mode Selection

| Mode | Use Case |
|------|----------|
| `'opaque'` | Full-screen renders, no transparency |
| `'premultiplied'` | Compositing with HTML (default) |

**Why:** Wrong alpha mode causes artifacts when compositing WebGPU content with HTML elements.

---

## Rule 3: Buffer Creation Patterns

Buffers are GPU memory allocations. Choose the right usage flags and update strategy.

### Buffer Usage Flags

| Flag | Purpose |
|------|---------|
| `GPUBufferUsage.VERTEX` | Vertex data (positions, UVs, normals) |
| `GPUBufferUsage.INDEX` | Index data for indexed drawing |
| `GPUBufferUsage.UNIFORM` | Small, frequently updated data (matrices) |
| `GPUBufferUsage.STORAGE` | Large read/write data (compute, particles) |
| `GPUBufferUsage.COPY_SRC` | Source for copy operations |
| `GPUBufferUsage.COPY_DST` | Destination for writes |
| `GPUBufferUsage.MAP_READ` | CPU-readable (readback) |
| `GPUBufferUsage.MAP_WRITE` | CPU-writable (staging) |

### Vertex Buffer

```javascript
function createVertexBuffer(device, data) {
  const buffer = device.createBuffer({
    size: data.byteLength,
    usage: GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST,
    mappedAtCreation: true
  });

  // Write data while mapped
  new Float32Array(buffer.getMappedRange()).set(data);
  buffer.unmap();

  return buffer;
}

// Usage
const positions = new Float32Array([
  // Triangle: x, y, z for each vertex
  0.0,  0.5, 0.0,
 -0.5, -0.5, 0.0,
  0.5, -0.5, 0.0
]);

const vertexBuffer = createVertexBuffer(device, positions);
```

### Uniform Buffer

```javascript
function createUniformBuffer(device, size) {
  return device.createBuffer({
    size: Math.max(size, 16), // Minimum 16 bytes for alignment
    usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST
  });
}

// Update uniform buffer
function updateUniformBuffer(device, buffer, data) {
  device.queue.writeBuffer(buffer, 0, data);
}

// Usage: MVP matrix (64 bytes = 16 floats)
const uniformBuffer = createUniformBuffer(device, 64);
const mvpMatrix = new Float32Array(16);
// ... compute matrix
updateUniformBuffer(device, uniformBuffer, mvpMatrix);
```

### Storage Buffer (Compute/Particles)

```javascript
function createStorageBuffer(device, size, initialData = null) {
  const buffer = device.createBuffer({
    size,
    usage: GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_DST | GPUBufferUsage.COPY_SRC,
    mappedAtCreation: !!initialData
  });

  if (initialData) {
    new Float32Array(buffer.getMappedRange()).set(initialData);
    buffer.unmap();
  }

  return buffer;
}

// Particle system: position (vec3) + velocity (vec3) + life (f32) = 7 floats per particle
const PARTICLE_COUNT = 10000;
const PARTICLE_STRIDE = 7 * 4; // 28 bytes
const particleBuffer = createStorageBuffer(device, PARTICLE_COUNT * PARTICLE_STRIDE);
```

**Why:** Correct usage flags enable GPU optimizations. Missing `COPY_DST` prevents updates; missing `STORAGE` prevents compute access.

---

## Rule 4: WGSL Shader Fundamentals

WGSL (WebGPU Shading Language) is the shader language for WebGPU. Write type-safe, GPU-optimized code.

### Basic Vertex Shader

```wgsl
// Uniforms bound to group 0, binding 0
struct Uniforms {
  mvp: mat4x4<f32>,
  time: f32,
}

@group(0) @binding(0) var<uniform> uniforms: Uniforms;

// Vertex input
struct VertexInput {
  @location(0) position: vec3<f32>,
  @location(1) color: vec3<f32>,
}

// Vertex output (to fragment shader)
struct VertexOutput {
  @builtin(position) position: vec4<f32>,
  @location(0) color: vec3<f32>,
}

@vertex
fn vs_main(input: VertexInput) -> VertexOutput {
  var output: VertexOutput;
  output.position = uniforms.mvp * vec4<f32>(input.position, 1.0);
  output.color = input.color;
  return output;
}
```

### Basic Fragment Shader

```wgsl
struct FragmentInput {
  @location(0) color: vec3<f32>,
}

@fragment
fn fs_main(input: FragmentInput) -> @location(0) vec4<f32> {
  return vec4<f32>(input.color, 1.0);
}
```

### Compute Shader (Particle Update)

```wgsl
struct Particle {
  position: vec3<f32>,
  velocity: vec3<f32>,
  life: f32,
}

struct SimParams {
  deltaTime: f32,
  gravity: vec3<f32>,
}

@group(0) @binding(0) var<uniform> params: SimParams;
@group(0) @binding(1) var<storage, read_write> particles: array<Particle>;

@compute @workgroup_size(256)
fn cs_main(@builtin(global_invocation_id) id: vec3<u32>) {
  let index = id.x;

  // Bounds check
  if (index >= arrayLength(&particles)) {
    return;
  }

  var p = particles[index];

  // Skip dead particles
  if (p.life <= 0.0) {
    return;
  }

  // Update physics
  p.velocity += params.gravity * params.deltaTime;
  p.position += p.velocity * params.deltaTime;
  p.life -= params.deltaTime;

  particles[index] = p;
}
```

### WGSL Type Reference

| WGSL Type | Size | Description |
|-----------|------|-------------|
| `f32` | 4 bytes | 32-bit float |
| `i32` | 4 bytes | 32-bit signed int |
| `u32` | 4 bytes | 32-bit unsigned int |
| `vec2<f32>` | 8 bytes | 2D float vector |
| `vec3<f32>` | 12 bytes | 3D float vector |
| `vec4<f32>` | 16 bytes | 4D float vector |
| `mat4x4<f32>` | 64 bytes | 4x4 float matrix |

**Alignment rules:** `vec3` aligns to 16 bytes in uniform buffers. Use `vec4` or pad manually.

---

## Rule 5: Render Pipeline Creation

Pipelines define the complete render state. Create once, reuse every frame.

```javascript
async function createRenderPipeline(device, format, shaderCode) {
  const shaderModule = device.createShaderModule({
    code: shaderCode
  });

  // Check for compilation errors
  const compilationInfo = await shaderModule.getCompilationInfo();
  for (const message of compilationInfo.messages) {
    if (message.type === 'error') {
      throw new Error(`Shader error: ${message.message}`);
    }
    console.warn(`Shader ${message.type}: ${message.message}`);
  }

  return device.createRenderPipeline({
    layout: 'auto', // Auto-generate bind group layout
    vertex: {
      module: shaderModule,
      entryPoint: 'vs_main',
      buffers: [
        {
          arrayStride: 24, // 6 floats: position (3) + color (3)
          attributes: [
            { shaderLocation: 0, offset: 0, format: 'float32x3' },  // position
            { shaderLocation: 1, offset: 12, format: 'float32x3' }  // color
          ]
        }
      ]
    },
    fragment: {
      module: shaderModule,
      entryPoint: 'fs_main',
      targets: [{ format }]
    },
    primitive: {
      topology: 'triangle-list',
      cullMode: 'back',
      frontFace: 'ccw'
    },
    depthStencil: {
      format: 'depth24plus',
      depthWriteEnabled: true,
      depthCompare: 'less'
    }
  });
}
```

### Vertex Format Reference

| Format | Components | Bytes |
|--------|------------|-------|
| `'float32'` | 1 | 4 |
| `'float32x2'` | 2 | 8 |
| `'float32x3'` | 3 | 12 |
| `'float32x4'` | 4 | 16 |
| `'uint32'` | 1 | 4 |
| `'sint32'` | 1 | 4 |
| `'uint8x4'` | 4 | 4 |
| `'unorm8x4'` | 4 | 4 |

---

## Rule 6: Bind Groups and Resources

Bind groups connect shader bindings to actual GPU resources.

```javascript
function createBindGroup(device, pipeline, uniformBuffer, texture, sampler) {
  return device.createBindGroup({
    layout: pipeline.getBindGroupLayout(0), // Group 0
    entries: [
      {
        binding: 0,
        resource: { buffer: uniformBuffer }
      },
      {
        binding: 1,
        resource: texture.createView()
      },
      {
        binding: 2,
        resource: sampler
      }
    ]
  });
}

// Create sampler
const sampler = device.createSampler({
  magFilter: 'linear',
  minFilter: 'linear',
  mipmapFilter: 'linear',
  addressModeU: 'repeat',
  addressModeV: 'repeat',
  maxAnisotropy: 16
});
```

### Bind Group Layout

For explicit control, define layouts manually:

```javascript
const bindGroupLayout = device.createBindGroupLayout({
  entries: [
    {
      binding: 0,
      visibility: GPUShaderStage.VERTEX | GPUShaderStage.FRAGMENT,
      buffer: { type: 'uniform' }
    },
    {
      binding: 1,
      visibility: GPUShaderStage.FRAGMENT,
      texture: { sampleType: 'float' }
    },
    {
      binding: 2,
      visibility: GPUShaderStage.FRAGMENT,
      sampler: { type: 'filtering' }
    }
  ]
});

const pipelineLayout = device.createPipelineLayout({
  bindGroupLayouts: [bindGroupLayout]
});
```

---

## Rule 7: Render Pass Encoding

Command encoders record GPU commands. Submit batched commands for efficiency.

```javascript
function render(device, context, pipeline, vertexBuffer, bindGroup, vertexCount) {
  // Get current swap chain texture
  const textureView = context.getCurrentTexture().createView();

  // Create command encoder
  const commandEncoder = device.createCommandEncoder();

  // Begin render pass
  const renderPass = commandEncoder.beginRenderPass({
    colorAttachments: [{
      view: textureView,
      clearValue: { r: 0.1, g: 0.1, b: 0.15, a: 1.0 },
      loadOp: 'clear',
      storeOp: 'store'
    }],
    depthStencilAttachment: {
      view: depthTextureView,
      depthClearValue: 1.0,
      depthLoadOp: 'clear',
      depthStoreOp: 'store'
    }
  });

  // Set pipeline and resources
  renderPass.setPipeline(pipeline);
  renderPass.setBindGroup(0, bindGroup);
  renderPass.setVertexBuffer(0, vertexBuffer);

  // Draw
  renderPass.draw(vertexCount);

  // End pass
  renderPass.end();

  // Submit commands
  device.queue.submit([commandEncoder.finish()]);
}
```

### Load/Store Operations

| Operation | loadOp | storeOp | Use Case |
|-----------|--------|---------|----------|
| Clear then render | `'clear'` | `'store'` | Normal rendering |
| Preserve previous | `'load'` | `'store'` | Multi-pass rendering |
| Don't care | `'load'` | `'discard'` | Depth-only pass |

---

## Rule 8: Compute Shader Dispatch

Compute shaders run parallel workgroups. Calculate dispatch size correctly.

```javascript
async function createComputePipeline(device, shaderCode) {
  const shaderModule = device.createShaderModule({ code: shaderCode });

  return device.createComputePipeline({
    layout: 'auto',
    compute: {
      module: shaderModule,
      entryPoint: 'cs_main'
    }
  });
}

function dispatchCompute(device, pipeline, bindGroup, workgroupCount) {
  const commandEncoder = device.createCommandEncoder();
  const computePass = commandEncoder.beginComputePass();

  computePass.setPipeline(pipeline);
  computePass.setBindGroup(0, bindGroup);

  // Dispatch workgroups
  computePass.dispatchWorkgroups(
    workgroupCount.x,
    workgroupCount.y || 1,
    workgroupCount.z || 1
  );

  computePass.end();
  device.queue.submit([commandEncoder.finish()]);
}

// Calculate workgroup count
function calculateWorkgroups(itemCount, workgroupSize = 256) {
  return {
    x: Math.ceil(itemCount / workgroupSize),
    y: 1,
    z: 1
  };
}

// Usage: 10000 particles, workgroup size 256
const workgroups = calculateWorkgroups(10000, 256); // { x: 40, y: 1, z: 1 }
dispatchCompute(device, computePipeline, computeBindGroup, workgroups);
```

### Workgroup Size Guidelines

| Use Case | Recommended Size | Notes |
|----------|------------------|-------|
| 1D data (particles) | 256 | Good occupancy |
| 2D data (images) | 16x16 (256) | Cache-friendly |
| 3D data (volumes) | 8x8x4 (256) | Balance dimensions |

---

## Rule 9: Texture Creation and Loading

Textures store 2D image data on the GPU.

```javascript
async function loadTexture(device, url) {
  // Fetch image
  const response = await fetch(url);
  const blob = await response.blob();
  const imageBitmap = await createImageBitmap(blob);

  // Create texture
  const texture = device.createTexture({
    size: [imageBitmap.width, imageBitmap.height, 1],
    format: 'rgba8unorm',
    usage: GPUTextureUsage.TEXTURE_BINDING |
           GPUTextureUsage.COPY_DST |
           GPUTextureUsage.RENDER_ATTACHMENT
  });

  // Copy image to texture
  device.queue.copyExternalImageToTexture(
    { source: imageBitmap },
    { texture },
    [imageBitmap.width, imageBitmap.height]
  );

  return texture;
}

// Create depth texture
function createDepthTexture(device, width, height) {
  return device.createTexture({
    size: [width, height, 1],
    format: 'depth24plus',
    usage: GPUTextureUsage.RENDER_ATTACHMENT
  });
}
```

### Texture Formats

| Format | Use Case |
|--------|----------|
| `'rgba8unorm'` | Standard color textures |
| `'rgba8unorm-srgb'` | sRGB color textures |
| `'depth24plus'` | Depth buffer |
| `'depth32float'` | High-precision depth |
| `'r32float'` | Single-channel float |
| `'rgba16float'` | HDR textures |
| `'rgba32float'` | Compute textures |

---

## Rule 10: Web Component Integration

Integrate WebGPU with web components following project patterns.

```javascript
/**
 * WebGPU Canvas Component
 *
 * Skills applied:
 * - web-components: No querySelector, handleEvent, cleanup
 * - javascript: Async initialization, AbortController
 * - webgpu-canvas: All rules
 */
class GPUCanvas extends HTMLElement {
  // Direct element references - NO querySelector
  #canvas;
  #device = null;
  #context = null;
  #pipeline = null;
  #animationId = null;
  #resizeObserver = null;
  #lastTime = 0;

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    // Build DOM imperatively
    const style = document.createElement('style');
    style.textContent = `
      :host {
        display: block;
        contain: strict;
      }
      canvas {
        width: 100%;
        height: 100%;
        display: block;
      }
    `;

    this.#canvas = document.createElement('canvas');
    this.#canvas.setAttribute('part', 'canvas');

    this.shadowRoot.appendChild(style);
    this.shadowRoot.appendChild(this.#canvas);
  }

  async connectedCallback() {
    // Initialize WebGPU
    try {
      const { device } = await WebGPUContext.initialize();
      this.#device = device;
      this.#context = configureCanvasContext(this.#canvas, device);
      await this.#createResources();

      // Observe resize
      this.#resizeObserver = new ResizeObserver(() => this.#handleResize());
      this.#resizeObserver.observe(this);

      // Start render loop
      this.#startRenderLoop();
    } catch (error) {
      console.error('WebGPU initialization failed:', error);
      this.dispatchEvent(new CustomEvent('gpu-error', {
        bubbles: true,
        detail: { error }
      }));
    }
  }

  disconnectedCallback() {
    // Cancel animation loop
    if (this.#animationId) {
      cancelAnimationFrame(this.#animationId);
      this.#animationId = null;
    }

    // Disconnect resize observer
    if (this.#resizeObserver) {
      this.#resizeObserver.disconnect();
      this.#resizeObserver = null;
    }

    // Destroy GPU resources
    this.#destroyResources();
  }

  #handleResize() {
    if (resizeCanvasToDisplaySize(this.#canvas)) {
      this.#recreateDepthTexture();
    }
  }

  async #createResources() {
    // Create pipeline, buffers, etc.
    // Implementation depends on specific use case
  }

  #destroyResources() {
    // Destroy buffers explicitly
    // Note: WebGPU resources are garbage collected, but explicit
    // destruction is good practice for large resources
  }

  #startRenderLoop() {
    const frame = (timestamp) => {
      // Calculate delta time (frame-rate independent)
      const deltaTime = (timestamp - this.#lastTime) / 1000;
      this.#lastTime = timestamp;

      // Render
      this.#render(deltaTime);

      // Request next frame
      this.#animationId = requestAnimationFrame(frame);
    };

    this.#animationId = requestAnimationFrame(frame);
  }

  #render(deltaTime) {
    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia(
      '(prefers-reduced-motion: reduce)'
    ).matches;

    // Implement render logic
    // Update uniforms, encode commands, submit
  }

  #recreateDepthTexture() {
    // Recreate depth texture on resize
  }
}

customElements.define('gpu-canvas', GPUCanvas);
```

---

## Rule 11: Error Handling and Device Recovery

Handle GPU errors gracefully with recovery strategies.

```javascript
class RobustGPUContext {
  #device = null;
  #onDeviceLost = null;

  async initialize(onDeviceLost) {
    this.#onDeviceLost = onDeviceLost;

    const adapter = await navigator.gpu?.requestAdapter();
    if (!adapter) {
      throw new Error('No WebGPU adapter available');
    }

    this.#device = await adapter.requestDevice();

    // Handle device loss
    this.#device.lost.then(async (info) => {
      console.error(`WebGPU device lost: ${info.reason}`, info.message);

      if (info.reason === 'destroyed') {
        // Intentional destruction, don't recover
        return;
      }

      // Notify and attempt recovery
      this.#onDeviceLost?.(info);

      try {
        await this.initialize(this.#onDeviceLost);
        console.log('WebGPU device recovered');
      } catch (error) {
        console.error('WebGPU recovery failed:', error);
      }
    });

    return this.#device;
  }

  // Validation error handling
  pushErrorScope(filter = 'validation') {
    this.#device.pushErrorScope(filter);
  }

  async popErrorScope() {
    const error = await this.#device.popErrorScope();
    if (error) {
      console.error(`WebGPU ${error.constructor.name}:`, error.message);
    }
    return error;
  }
}

// Usage with error scope
const gpu = new RobustGPUContext();
await gpu.initialize((info) => {
  showUserMessage('Graphics reset, please wait...');
});

gpu.pushErrorScope('validation');
// ... WebGPU operations
const error = await gpu.popErrorScope();
if (error) {
  // Handle validation error
}
```

### Error Types

| Error Type | Cause | Recovery |
|------------|-------|----------|
| `GPUValidationError` | Invalid API usage | Fix code, re-run |
| `GPUOutOfMemoryError` | VRAM exhausted | Free resources, retry |
| Device lost (destroyed) | Tab closed, context lost | Reinitialize |
| Device lost (unknown) | Driver crash, GPU reset | Auto-recover |

---

## Rule 12: Performance Optimization

Optimize for consistent frame times and efficient GPU utilization.

### Double/Triple Buffering

```javascript
class BufferPool {
  #buffers = [];
  #currentIndex = 0;
  #size;

  constructor(device, size, usage, count = 3) {
    this.#size = size;
    for (let i = 0; i < count; i++) {
      this.#buffers.push(device.createBuffer({ size, usage }));
    }
  }

  // Get next buffer (round-robin)
  next() {
    const buffer = this.#buffers[this.#currentIndex];
    this.#currentIndex = (this.#currentIndex + 1) % this.#buffers.length;
    return buffer;
  }
}

// Usage: Triple-buffered uniform updates
const uniformPool = new BufferPool(
  device,
  256,
  GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST,
  3
);

// Each frame, use next buffer
function updateFrame(data) {
  const buffer = uniformPool.next();
  device.queue.writeBuffer(buffer, 0, data);
  return buffer;
}
```

### Batch Rendering

```javascript
// Bad: One draw call per object
for (const obj of objects) {
  renderPass.setVertexBuffer(0, obj.buffer);
  renderPass.draw(obj.vertexCount);
}

// Good: Instance rendering
const instanceBuffer = createInstanceBuffer(device, instanceData);
renderPass.setVertexBuffer(0, vertexBuffer);
renderPass.setVertexBuffer(1, instanceBuffer);
renderPass.draw(vertexCount, instanceCount);
```

### Timing Queries (Debug)

```javascript
async function measureGPUTime(device, commandEncoder, operation) {
  // Check for timestamp query support
  if (!device.features.has('timestamp-query')) {
    operation();
    return null;
  }

  const querySet = device.createQuerySet({
    type: 'timestamp',
    count: 2
  });

  const resolveBuffer = device.createBuffer({
    size: 16,
    usage: GPUBufferUsage.QUERY_RESOLVE | GPUBufferUsage.COPY_SRC
  });

  commandEncoder.writeTimestamp(querySet, 0);
  operation();
  commandEncoder.writeTimestamp(querySet, 1);

  commandEncoder.resolveQuerySet(querySet, 0, 2, resolveBuffer, 0);

  // Read back results (requires additional staging buffer)
  // Returns time in nanoseconds
}
```

---

## Rule 13: Memory Management

Track and limit GPU memory usage to prevent crashes.

```javascript
class GPUResourceTracker {
  #allocations = new Map();
  #totalBytes = 0;
  #maxBytes;

  constructor(maxBytes = 512 * 1024 * 1024) { // 512MB default limit
    this.#maxBytes = maxBytes;
  }

  track(resource, bytes, label = 'unnamed') {
    if (this.#totalBytes + bytes > this.#maxBytes) {
      console.warn(`GPU memory limit exceeded, cannot allocate ${label}`);
      return false;
    }

    this.#allocations.set(resource, { bytes, label });
    this.#totalBytes += bytes;
    return true;
  }

  release(resource) {
    const allocation = this.#allocations.get(resource);
    if (allocation) {
      this.#totalBytes -= allocation.bytes;
      this.#allocations.delete(resource);
    }
  }

  get used() { return this.#totalBytes; }
  get available() { return this.#maxBytes - this.#totalBytes; }

  report() {
    console.log(`GPU Memory: ${(this.#totalBytes / 1024 / 1024).toFixed(2)} MB used`);
    for (const [resource, info] of this.#allocations) {
      console.log(`  ${info.label}: ${(info.bytes / 1024).toFixed(2)} KB`);
    }
  }
}
```

---

## Complete Example: Particle System

```javascript
// particle-system.js
const PARTICLE_SHADER = `
struct Particle {
  position: vec3<f32>,
  velocity: vec3<f32>,
  life: f32,
  _padding: f32, // Align to 32 bytes
}

struct SimParams {
  deltaTime: f32,
  gravity: f32,
  _padding: vec2<f32>,
}

@group(0) @binding(0) var<uniform> params: SimParams;
@group(0) @binding(1) var<storage, read_write> particles: array<Particle>;

@compute @workgroup_size(256)
fn update(@builtin(global_invocation_id) id: vec3<u32>) {
  let idx = id.x;
  if (idx >= arrayLength(&particles)) { return; }

  var p = particles[idx];
  if (p.life <= 0.0) { return; }

  p.velocity.y -= params.gravity * params.deltaTime;
  p.position += p.velocity * params.deltaTime;
  p.life -= params.deltaTime;

  particles[idx] = p;
}
`;

class ParticleSystem extends HTMLElement {
  static PARTICLE_COUNT = 10000;
  static PARTICLE_STRIDE = 32; // 8 floats, aligned

  #canvas;
  #device = null;
  #computePipeline = null;
  #particleBuffer = null;
  #uniformBuffer = null;
  #bindGroup = null;
  #animationId = null;
  #lastTime = 0;

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    const style = document.createElement('style');
    style.textContent = `:host { display: block; } canvas { width: 100%; height: 100%; }`;

    this.#canvas = document.createElement('canvas');
    this.shadowRoot.append(style, this.#canvas);
  }

  async connectedCallback() {
    const { device } = await WebGPUContext.initialize();
    this.#device = device;

    await this.#initializeParticles();
    this.#startLoop();
  }

  disconnectedCallback() {
    if (this.#animationId) {
      cancelAnimationFrame(this.#animationId);
    }
  }

  async #initializeParticles() {
    const device = this.#device;

    // Create compute pipeline
    const shaderModule = device.createShaderModule({ code: PARTICLE_SHADER });
    this.#computePipeline = device.createComputePipeline({
      layout: 'auto',
      compute: { module: shaderModule, entryPoint: 'update' }
    });

    // Initialize particle data
    const initialData = new Float32Array(ParticleSystem.PARTICLE_COUNT * 8);
    for (let i = 0; i < ParticleSystem.PARTICLE_COUNT; i++) {
      const offset = i * 8;
      initialData[offset + 0] = (Math.random() - 0.5) * 2; // x
      initialData[offset + 1] = Math.random() * 2;          // y
      initialData[offset + 2] = (Math.random() - 0.5) * 2; // z
      initialData[offset + 3] = (Math.random() - 0.5) * 0.5; // vx
      initialData[offset + 4] = Math.random() * 2;           // vy
      initialData[offset + 5] = (Math.random() - 0.5) * 0.5; // vz
      initialData[offset + 6] = Math.random() * 5 + 2;       // life
      initialData[offset + 7] = 0;                           // padding
    }

    this.#particleBuffer = createStorageBuffer(
      device,
      initialData.byteLength,
      initialData
    );

    this.#uniformBuffer = createUniformBuffer(device, 16);

    this.#bindGroup = device.createBindGroup({
      layout: this.#computePipeline.getBindGroupLayout(0),
      entries: [
        { binding: 0, resource: { buffer: this.#uniformBuffer } },
        { binding: 1, resource: { buffer: this.#particleBuffer } }
      ]
    });
  }

  #startLoop() {
    const frame = (timestamp) => {
      const deltaTime = Math.min((timestamp - this.#lastTime) / 1000, 0.1);
      this.#lastTime = timestamp;

      this.#update(deltaTime);
      this.#animationId = requestAnimationFrame(frame);
    };

    this.#animationId = requestAnimationFrame(frame);
  }

  #update(deltaTime) {
    const device = this.#device;

    // Update uniforms
    const uniforms = new Float32Array([deltaTime, 9.8, 0, 0]);
    device.queue.writeBuffer(this.#uniformBuffer, 0, uniforms);

    // Dispatch compute
    const commandEncoder = device.createCommandEncoder();
    const computePass = commandEncoder.beginComputePass();

    computePass.setPipeline(this.#computePipeline);
    computePass.setBindGroup(0, this.#bindGroup);
    computePass.dispatchWorkgroups(
      Math.ceil(ParticleSystem.PARTICLE_COUNT / 256)
    );

    computePass.end();
    device.queue.submit([commandEncoder.finish()]);
  }
}

customElements.define('particle-system', ParticleSystem);
```

---

## Checklist

Before shipping WebGPU code:

- [ ] Feature detection with graceful fallback
- [ ] Device/adapter initialized once (singleton)
- [ ] Canvas context configured with correct format and alpha mode
- [ ] Device pixel ratio handled for crisp rendering
- [ ] Resize observer for canvas size changes
- [ ] Render loop uses requestAnimationFrame
- [ ] Frame-rate independent updates (delta time)
- [ ] Device lost handler with recovery
- [ ] Error scopes for validation during development
- [ ] Resources cleaned up in disconnectedCallback
- [ ] Reduced motion preference respected
- [ ] WGSL shaders checked for compilation errors
- [ ] Buffer alignment correct (16 bytes for uniforms)
- [ ] Workgroup sizes optimized for target hardware

---

## Quick Reference

### Initialization

```javascript
const adapter = await navigator.gpu.requestAdapter();
const device = await adapter.requestDevice();
const context = canvas.getContext('webgpu');
context.configure({ device, format: navigator.gpu.getPreferredCanvasFormat() });
```

### Buffer Creation

```javascript
// Vertex
device.createBuffer({ size, usage: GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST });

// Uniform
device.createBuffer({ size, usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST });

// Storage (compute)
device.createBuffer({ size, usage: GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_DST });
```

### Render Loop

```javascript
const frame = (timestamp) => {
  const deltaTime = (timestamp - lastTime) / 1000;
  lastTime = timestamp;

  // Update & render
  update(deltaTime);
  render();

  requestAnimationFrame(frame);
};
requestAnimationFrame(frame);
```

### Command Submission

```javascript
const encoder = device.createCommandEncoder();
const pass = encoder.beginRenderPass({ colorAttachments: [{ view, loadOp: 'clear', storeOp: 'store' }] });
pass.setPipeline(pipeline);
pass.setBindGroup(0, bindGroup);
pass.setVertexBuffer(0, vertexBuffer);
pass.draw(vertexCount);
pass.end();
device.queue.submit([encoder.finish()]);
```

---

## Files

This skill integrates with:
- `js/utils/webgpu-context.js` - Singleton WebGPU context
- `css/styles/accessibility.css` - Reduced motion tokens
- `js/components/` - Web component integration patterns

### Project WebGPU Effects

The project includes these ready-to-use WebGPU effect components:

| Component | File | Purpose |
|-----------|------|---------|
| `<magical-motes>` | `js/components/effects/magical-motes.js` | Ambient floating particles |
| `<ink-trail>` | `js/components/effects/ink-trail.js` | Typing feedback particles |
| `<particle-burst>` | `js/components/effects/particle-burst.js` | Celebration explosions |
| `<rank-aura>` | `js/components/effects/rank-aura.js` | Wizard rank orbital glow |

Import all effects:
```javascript
import '/js/components/effects/index.js';
```
