---
name: fec-svg-animation
description: 用于实现或审查 SVG 动画、路径绘制、图标动效、Logo 动画、插画动效、微交互、CSS/SMIL/Framer Motion/GSAP 选型、动效无障碍或降级行为；中文触发词包括 SVG 动画、路径描边、动效。
---

# SVG 动画实现

## 用途

为 SVG 图标、插画和数据可视化提供可维护、可访问、性能可控的动画方案。

## 适用场景

- 需要实现 SVG 图标、Logo、插画或路径描边动画。
- 需要在 React/Vue 组件中接入 Framer Motion、GSAP 或 CSS 动画。
- 需要根据 `prefers-reduced-motion` 提供动效降级。
- 不用于复杂 3D/WebGL 场景；此类场景优先使用 Canvas / Three.js workflow。

## 流程

### 1. 选择动画方式

按复杂度和运行时需求选型：

| 场景 | 推荐 |
| --- | --- |
| hover/focus、opacity、transform | CSS animation/transition |
| 路径描边、简单重复动效 | CSS + `stroke-dasharray` |
| React 组件状态驱动动画 | Framer Motion |
| 时间轴、复杂编排、滚动触发 | GSAP |
| 需要保持零依赖的静态 SVG | CSS 或 SMIL |

如果动效跨越页面转场、滚动叙事或复杂组件编排，应先按交互动效 workflow 判断强度、懒加载和 reduced-motion 策略；本 skill 只负责 SVG 图形本身的路径、形变和图标 motion。

### 2. 使用 CSS 实现路径描边

```tsx
export function CheckmarkIcon() {
  return (
    <svg viewBox="0 0 24 24" className="checkmark" aria-hidden="true">
      <path
        className="checkmark-path"
        d="M5 12.5l4.5 4.5L19 7"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
```

```css
.checkmark-path {
  stroke-dasharray: 24;
  stroke-dashoffset: 24;
  animation: draw-checkmark 420ms ease-out forwards;
}

@keyframes draw-checkmark {
  to {
    stroke-dashoffset: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .checkmark-path {
    animation: none;
    stroke-dashoffset: 0;
  }
}
```

### 3. 在 React 中使用 Framer Motion

```tsx
import { motion, useReducedMotion } from "framer-motion";

export function AnimatedSparkline({ path }: { path: string }) {
  const reduceMotion = useReducedMotion();

  return (
    <svg viewBox="0 0 120 40" role="img" aria-label="趋势图">
      <motion.path
        d={path}
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        initial={reduceMotion ? false : { pathLength: 0, opacity: 0 }}
        animate={{ pathLength: 1, opacity: 1 }}
        transition={{ duration: 0.7, ease: "easeOut" }}
      />
    </svg>
  );
}
```

### 4. 使用 GSAP 编排复杂时间轴

```tsx
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";

export function LogoReveal() {
  const rootRef = useRef<SVGSVGElement>(null);

  useLayoutEffect(() => {
    if (!rootRef.current) return;
    const ctx = gsap.context(() => {
      gsap.timeline({ defaults: { ease: "power2.out" } })
        .from(".logo-mark", { scale: 0.9, opacity: 0, duration: 0.25 })
        .from(".logo-line", { strokeDashoffset: 80, duration: 0.55 }, "-=0.1");
    }, rootRef);

    return () => ctx.revert();
  }, []);

  return (
    <svg ref={rootRef} viewBox="0 0 120 32" aria-hidden="true">
      <circle className="logo-mark" cx="16" cy="16" r="10" />
      <path className="logo-line" d="M36 16h68" stroke="currentColor" />
    </svg>
  );
}
```

### 5. 控制运行成本

- 大型 SVG 拆成静态底图和少量可动画节点，不要让每个 path 都参与时间轴。
- 图标库或 Lottie 替代方案必须按需加载，不进入所有页面的基础包。
- 循环动画只在可见区域运行，页面隐藏或组件卸载时停止。
- 移动端减少滤镜、mask、clipPath 和大量渐变叠加。

## 约束

- 优先动画 `transform`、`opacity` 和 SVG 路径属性；避免高频修改 layout 相关属性。
- 交互控件必须保留可见 focus 状态，动画不能替代状态表达。
- 所有非装饰性 SVG 必须有可访问名称；装饰性 SVG 使用 `aria-hidden="true"`。
- 默认尊重 `prefers-reduced-motion`，复杂动效必须提供静态或弱动效降级。
- 不要把大型 SVG 内联到频繁重渲染的组件中；提取为 memoized 组件或外部资源。
- 不用动画改变可点击区域、阅读顺序或焦点位置。
- 不让 SVG 滤镜、模糊、mask 或 clipPath 成为移动端掉帧主因；复杂效果需要设备降级。

## 预期输出

产出一个可复用的 SVG 动画组件或样式方案，包含选型理由、动效降级和可访问性处理。验证时检查动画流畅、无布局抖动、键盘与 reduced-motion 场景可用。
