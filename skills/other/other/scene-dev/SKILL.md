---
name: scene-dev
description: >
  NextFrame Scene 组件开发规范。创建新 scene、修改 scene、审查 scene 质量。
  确保每个 scene 满足 ADR-008 强制契约：4 接口 + 主题预设 + AI 元数据 + preview + validate 全绿。
  TRIGGER: "写组件"、"新 scene"、"做 scene"、"加组件"、"scene 开发"、"组件开发"、
  "写背景"、"写标题"、"写图表"、"写叠加层"、"新 scene"。
  DO NOT TRIGGER when: 使用已有 scene 写 timeline、修 engine 代码。
---

# NextFrame Scene 开发规范（ADR-008 强制契约）

## 核心原则（违反 = 打回重做）

### 1. 一个 scene = 一个视觉原子

**一个 scene 只做一件事。** 不混合多个视觉职责。

| 正确 | 错误 |
|------|------|
| flowDiagram 只画节点+箭头 | flowDiagram 同时画标题+流程图+引语 |
| titleCard 只画标题 | titleCard 同时画标题+代码块 |
| subtitleBar 只画字幕 | subtitleBar 同时画字幕+进度条 |

**判断标准：如果你的 scene 里有两种"能独立存在"的内容，就该拆成两个 scene。**

标题是标题 scene。引语是引语 scene。流程图是流程图 scene。组合靠 timeline 的 layers。

### 2. 参数不写死视觉

- 颜色、位置、大小 → 全部走 params，不硬编码
- 文字内容如果支持 HTML（加粗/变色）→ 在 meta.params 里标注 `semantic: "supports inline HTML"`
- 不支持 HTML 的文字 → 必须 `esc()` 转义

### 3. 先预览后提交

写完 index.js + preview.html → **必须打开 preview.html 自己看一遍** → 确认无溢出、无错位、动画流畅 → 才能提交。

## 开发流程（必须按顺序，每步都有阻断检查）

```
1. 确定职责 → 这个 scene 只做什么？（一句话说清，超过一句就该拆）
2. 确定比例 + 类别 → 创建目录
3. 写 index.js（meta 全字段 → render → screenshots → lint）
4. 写 preview.html（自包含，file:// 可打开，不依赖服务器）
5. ⛔ 打开 preview.html 自己看 → 确认视觉正确
6. validate-scene.js 全绿
7. 测试 lint 拦截（故意传错参数）
8. 做一个 demo timeline 验证组合效果（和其他 scene 叠加）
9. 提交
```

**步骤 5 是阻断点。** 不看 preview 不许提交。看到问题必须修完再走下一步。

## 目录结构（强制）

```
src/nf-core/scenes/{ratio}/{category}/{sceneName}/
├── index.js        ← 必须：meta + render + screenshots + lint
└── preview.html    ← 必须：自包含，file:// 直接打开
```

比例目录（禁止 universal）：`16x9/` | `9x16/` | `4x3/`
类别目录：`backgrounds/` | `typography/` | `data/` | `shapes/` | `overlays/` | `media/` | `browser/`

## index.js — 4 个必须导出 + 强制 meta 字段

### meta（全字段必填）

```js
export const meta = {
  // ─── 身份 ───
  id: "sceneName",              // 唯一 ID
  version: 1,                   // 改接口就 +1
  ratio: "9:16",                // 必填，禁止 null，和目录一致

  // ─── 分类与发现 ───
  category: "backgrounds",      // 小写
  label: "Scene Name",          // 英文名
  description: "中文描述，说清楚视觉效果和动画行为",
  tags: ["tag1", "tag2", "tag3"], // 至少 3 个搜索标签
  mood: ["calm", "energetic"],    // 情绪标签
  theme: ["tech", "business"],    // 适用主题

  // ─── 渲染 ───
  tech: "canvas2d",             // canvas2d | webgl | svg | dom | video | lottie
  duration_hint: 12,            // 建议时长（秒）
  loopable: true,               // 能否循环
  z_hint: "bottom",             // bottom | middle | top

  // ─── 主题预设（至少 3 个）───
  default_theme: "theme-name",
  themes: {
    "theme-name": { /* params 子集 */ },
    // 至少 3 个预设
  },

  // ─── 参数 ───
  params: {
    paramName: {
      type: "number",           // number | string | boolean | color | enum | array | object | file
      default: 270,             // 必须有（除非 required: true）
      range: [0, 360],          // number 必须有
      step: 1,                  // number 必须有
      label: "中文名",          // 必须有
      semantic: "english desc for AI", // 必须有，写清楚含义和取值范围的效果
      group: "color",           // content | color | style | animation | shape
    },
  },

  // ─── AI 指南（全字段必填）───
  ai: {
    when: "什么场景适合用，中文",
    how: "怎么在 timeline 里用，中文",
    example: { /* 完整 params 示例 */ },
    theme_guide: "每个 theme 的中文一句话说明",
    avoid: "什么情况不要用",
    pairs_with: ["scene-id-1", "scene-id-2"],
  },
};
```

### render(t, params, vp) → HTML string

```js
export function render(t, params, vp) {
  const { width, height } = vp; // 画布尺寸（像素）
  // 返回 HTML 片段
}
```

**强制规则：**
- 纯函数 — 相同 (t, params, vp) → 相同输出
- 禁止 Math.random()（除非用 seed）、Date.now()、全局状态
- 禁止 setTimeout / setInterval / requestAnimationFrame / fetch
- 返回的 HTML 宽高 = vp.width × vp.height
- **只做自己那一件事的 HTML。** 不画别的 scene 该画的东西

**按 tech 类型的输出格式：**

| tech | 返回什么 | 注意 |
|------|---------|------|
| canvas2d | `<canvas width={W} height={H}>` + `<script>绘制</script>` | canvas 尺寸 = vp，不要写死 1080 |
| svg | `<svg viewBox="0 0 {W} {H}">` | viewBox 天然缩放 |
| dom | `<div style="width:{W}px;height:{H}px">` | 尺寸跟 vp 走 |
| webgl | `<canvas>` + WebGL init `<script>` | — |
| video | `<video src currentTime={t}>` | — |
| lottie | Lottie player 定位到 t 帧 | — |

**⚠️ 踩坑记录：Canvas 和 DOM 混合渲染时，所有 scene 必须用同一个 viewport 尺寸。不要 Canvas 用 1080 而 DOM 用 380。**

### screenshots() → 截图时间点

```js
export function screenshots() {
  return [
    { t: 0,   label: "开始" },
    { t: 2.5, label: "动画中" },
    { t: 4.5, label: "完成" },
  ];
}
```

至少 3 个：开始、中间、结束。label 用中文。

### lint(params, vp) → 检查结果

```js
export function lint(params, vp) {
  const errors = [];
  // 必须检查：
  // 1. 文字溢出安全区（viewport × 0.9）
  // 2. 数组长度合理
  // 3. required 参数非空
  // 4. 数值在 range 内
  // 5. theme 名字在 themes{} 里存在
  // 每个 error 格式："描述。Fix: 修复建议"
  return { ok: errors.length === 0, errors };
}
```

## preview.html 规范

**必须自包含：** `file://` 直接打开，不依赖服务器，不用 ES module import。render 函数直接内联到 HTML 里。

**必须有的 UI 元素：**

1. 正确比例的画布（16:9 → 960×540 缩放容器）
2. 进度条（可拖动跳转）
3. 播放/暂停按钮
4. 时间显示
5. 暖棕背景 `#1a1510`（模拟真实合成环境）

**渲染规则：**
- Canvas：画在显示尺寸上（不要画 1080 再 CSS 缩小，会卡）
- SVG：用 viewBox，天然清晰
- DOM：用 1920×1080 内部容器 + transform:scale(0.5) 缩放

## 渲染技术选择

| 场景类型 | 推荐 tech | 原因 |
|---------|----------|------|
| 渐变/粒子/噪声 | canvas2d | 像素级操作 |
| 3D/Shader | webgl | GPU 加速 |
| 图表/图形 | svg | 矢量不糊 |
| 文字排版/卡片/毛玻璃 | dom | CSS 排版 + backdrop-filter |
| 视频片段 | video | HTML5 Video |
| 设计师动画 | lottie | .json 格式 |

## 主题系统

```json
// timeline 里用法（3 种）：
// 1. 只选 theme（AI 安全选择）
{ "scene": "auroraGradient", "theme": "ocean-teal" }

// 2. theme + 微调
{ "scene": "auroraGradient", "theme": "ocean-teal", "params": { "intensity": 1.5 } }

// 3. 纯自定义
{ "scene": "auroraGradient", "params": { "hueA": 150 } }
```

合并优先级：`params.default < themes[name] < timeline.params`

## 验证命令

```bash
# 验证单个（16 项检查）
node src/nf-core/scenes/validate-scene.js <scene-dir>

# 验证全部
for d in $(find src/nf-core/scenes -name "index.js" -exec dirname {} \;); do
  node src/nf-core/scenes/validate-scene.js "$d"
done

# 测试 lint 拦截
node src/nf-core/scenes/validate-scene.js <dir> --params '{"text":"超长文字..."}'

# 预览
open <scene-dir>/preview.html

# 做 demo timeline 测试组合
# 参考 output/demo-9x16.html
```

## 质量标准（全部必须满足）

| # | 检查项 | 标准 |
|---|--------|------|
| 1 | **单一职责** | scene 只做一件事，能一句话说清 |
| 2 | **无溢出** | preview 里看不到任何内容超出画布/容器 |
| 3 | validate-scene.js | 16/16 通过 |
| 4 | preview.html | 打开能看到流畅动画，file:// 直接可用 |
| 5 | lint 拦截 | 故意传溢出/空值能报错带 Fix 建议 |
| 6 | render 纯函数 | 相同输入 → 相同输出 |
| 7 | 主题预设 | 至少 3 个 theme，default_theme 有效 |
| 8 | AI 元数据 | when/how/example/theme_guide/avoid/pairs_with 全有 |
| 9 | 组合测试 | 在 demo timeline 里和其他 scene 叠加不冲突 |

## 常见错误（做 scene 时必须检查）

| 错误 | 怎么发现 | 怎么修 |
|------|---------|--------|
| 一个 scene 混了多种内容 | description 要写两句话才能说清 | 拆成多个 scene |
| 文字溢出容器 | preview 里文字超出画布边界 | 自适应字号 / 限制最大宽度 / lint 拦截 |
| HTML 标签被转义显示 | 看到 `<span>` 字样 | 支持 HTML 的字段不 esc()，在 semantic 里标注 |
| 颜色硬编码 | 换 theme 颜色不变 | 全部走 params，themes 覆盖 |
| preview 需要服务器 | file:// 打开白屏 | 不用 ES module import，render 函数内联 |
| 不自验就提交 | 用户看到溢出/错位 | **必须 open preview 自己看一遍** |

## 已有 scene 组件（16:9）

| Scene | 类别 | 职责（一件事） |
|-------|------|---------------|
| auroraGradient | backgrounds | 渐变光斑背景 |
| codeTerminal | browser | 终端代码块 |
| slideChrome | overlays | 顶栏 + 水印 |
| titleCard | typography | 大标题 + 副标题 |
| tagCompare | typography | 两个对比标签 |
| eventList | data | 竖排圆点列表 |
| flowDiagram | data | 节点箭头流程图（不含标题/引语） |
| subtitleBar | overlays | 底部字幕 |
| progressBar | overlays | 进度条 |
| barChartReveal | data | 柱状图 |
| kineticHeadline | typography | 逐字出现标题 |

**缺的（待做）：**
- `headlineCenter` — 居中大标题（独立于 titleCard 的全屏居中版）
- `quoteBlock` — 金色斜体引语
- `comparisonPanel` — 左右对比卡片（主 Agent vs 子 Agent）
- `stackedCards` — 堆叠卡片列表（九层配置等）
