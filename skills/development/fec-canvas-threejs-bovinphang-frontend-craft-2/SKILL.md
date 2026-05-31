---
name: fec-canvas-threejs
description: Use when building or reviewing Canvas 2D, Three.js/WebGL, React Three Fiber, GLSL shaders, ShaderToy-to-WebGL adaptation, 2D/3D visualization, game rendering, animation loops, GPU resource cleanup, or rendering performance. Do not use for standard DOM UI, charts already covered by a chart library, or non-graphical performance work; Chinese triggers include Canvas, Three.js, WebGL, GLSL, Shader, 3D, 数据可视化, 游戏.
---

# Canvas 与 Three.js

## Purpose

在浏览器中实现高性能 2D/3D 图形渲染。

## Procedure

1. 先选渲染层：标准 UI 用 DOM；简单 2D 图形/签名/粒子用 Canvas 2D；3D 模型、空间交互和复杂粒子用 Three.js/WebGL；React 项目中的声明式 3D 用 React Three Fiber。
2. 为渲染容器定义稳定尺寸、DPI 适配和 resize 行为；Canvas 不会自动随 CSS 清晰缩放。
3. 动画循环使用 `requestAnimationFrame`，不可见或无变化时暂停，卸载时取消。
4. Three.js 必须释放 geometry/material/texture/renderer，并移除事件监听和 observer。
5. Shader/WebGL 任务先识别是 SDF、ray marching、noise、particle、post-processing、multipass 还是调试问题，再决定是否需要原生 WebGL2、Three.js ShaderMaterial 或 R3F。
6. WebGL2 适配时检查 GLSL 版本、入口函数、varying/in-out、texture API、uniform 使用和函数声明顺序，避免白屏只留控制台错误。
7. 对不可访问的图形内容提供 `aria-label`、替代文本或 DOM 版摘要；交互式图形要有键盘兜底。

## Core Patterns

```ts
const dpr = Math.min(window.devicePixelRatio || 1, 2);
canvas.width = width * dpr;
canvas.height = height * dpr;
canvas.style.width = `${width}px`;
canvas.style.height = `${height}px`;
ctx.scale(dpr, dpr);
```

```ts
let animationId = 0;
function animate() {
  animationId = requestAnimationFrame(animate);
  renderer.render(scene, camera);
}

return () => {
  cancelAnimationFrame(animationId);
  geometry.dispose();
  material.dispose();
  renderer.dispose();
};
```

## Detailed References

涉及 Canvas 2D 绘图、动画循环、Three.js 场景搭建、React Three Fiber、InstancedMesh 和性能清理时，加载 [references/rendering-patterns.md](references/rendering-patterns.md)。

涉及着色器路由、WebGL2 适配、GLSL 调试、多 pass 预算和视觉验证时，加载 [references/shader-webgl-patterns.md](references/shader-webgl-patterns.md)。

## Constraints

- Canvas/WebGL 内容对屏幕阅读器不可见，必须提供替代语义。
- WebGL 消耗 GPU，低端设备需限制像素比、面数和纹理大小。
- Three.js 资源不会自动释放，遗漏 `dispose()` 会造成 GPU 内存泄漏。
- Canvas 响应式必须同步 CSS 尺寸、绘图尺寸和相机/viewport。
- 复杂布局/路径规划可联用后台线程 workflow，但渲染本身仍在主线程/渲染线程协调。
- Shader 主循环、采样层数和多 pass 数量必须有预算；低端设备上要降低 DPR、步数、粒子数或禁用重后处理。
- 交付前必须确认 canvas 非空、尺寸正确、resize 后不拉伸、控制台无 shader compile/link 错误。

## Expected Output

2D/3D 场景清晰、响应式、可清理，关键设备上接近 60fps；用户能通过替代文本或键盘路径理解/操作核心内容。
