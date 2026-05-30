---
name: fec-list-virtualization
description: Use when optimizing or reviewing large lists, virtual scrolling, windowing, react-window, TanStack Virtual, variable-height rows, dynamic measurement, infinite scroll, grid virtualization, or scroll performance; Chinese triggers include 虚拟列表, 大列表优化, 滚动性能.
---

# 列表虚拟化优化

## Purpose

通过窗口化只渲染可视区域，解决大列表 DOM 过多和滚动卡顿。

## Procedure

1. 先确认列表规模和瓶颈：500+ 项、滚动掉帧、DOM 节点过多或内存飙升才引入虚拟化。
2. 固定高度列表用 `react-window`；动态高度、跨框架或高级场景用 TanStack Virtual；遗留项目可维护 `react-virtualized`。
3. 明确 item size、overscan、容器高度、key、滚动容器和 resize 行为。
4. 无限滚动时分离数据分页和 DOM 虚拟化；数据获取可联用数据获取 workflow。
5. 验证 DOM 节点数、滚动 FPS、键盘/屏幕阅读器体验和 Ctrl+F/SEO 限制。

## Detailed References

涉及固定高度列表、可变/动态高度、无限滚动、网格虚拟化和性能注意事项时，加载 [references/virtualization-patterns.md](references/virtualization-patterns.md)。

## Constraints

- SEO 关键内容不要只存在于虚拟项中。
- 浏览器原生 Ctrl+F 无法搜索未挂载项目。
- Row 根元素必须透传虚拟库提供的 style/measure ref。
- overscan 过大会浪费内存，过小会白屏。
- 动态高度测量要处理 ResizeObserver 和布局抖动。

## Expected Output

10000+ 项列表滚动接近 60fps，DOM 节点数稳定在可视区域及缓冲区范围，内存从 O(n) 降至 O(visible)。
