---
name: vercel-design
description: "Vercel 设计指南 - 构建高质量 Web 应用的最佳实践，包含现代 UI/UX 原则、性能优化和无障碍标准。"
---

# Vercel 设计指南技能

Vercel 设计原则和最佳实践的全面参考。在构建 Web 应用程序时使用此技能以确保：

- **UI 卓越** - 清晰、直观且易于访问的用户界面
- **性能** - 快速、响应式的用户体验
- **国际化** - 支持区域设置和语言友好
- **无障碍** - 符合 WCAG 标准且支持屏幕阅读器
- **一致的设计** - 连贯的视觉语言和交互

## 快速参考

### 导航
- [UI 指南](#ui-指南)
- [国际化](#国际化)
- [表单](#表单)
- [性能](#性能)
- [视觉设计](#视觉设计)
- [文案写作](#文案写作)

---

## UI 指南

### 锚点和导航

**为标题设置 scroll-margin-top 以便链接到章节：**
```css
h2, h3, h4 {
  scroll-margin-top: 1rem;
}
```

### 用户生成内容

**对用户生成内容具有弹性。** 布局应能处理短、平均和非常长的内容。

### 无障碍

**无障碍内容：**
- 设置准确的名称（`aria-label`）
- 隐藏装饰（`aria-hidden`）
- 在[无障碍树](https://developer.chrome.com/blog/full-accessibility-tree)中验证

**仅图标按钮需要命名：**
```jsx
<button aria-label="关闭模态框">×</button>
```

**语义优于 ARIA：** 优先使用原生元素（`button`、`a`、`label`、`table`），然后再使用 `aria-*`。

**标题和跳转链接：** 使用层级化的 `<h1–h6>` 和"跳转到内容"链接。

**粘合术语使用不换行空格：** 使用 `&nbsp;` 保持单位、快捷键和名称在一起：
- `10 MB` → `10&nbsp;MB`
- `⌘ + K` → `⌘&nbsp;+&nbsp;K`
- `Vercel SDK` → `Vercel&nbsp;SDK`
- 不需要空格时使用 `&#x2060;`

### 品牌资源

**从 Logo 获取品牌资源：** 右键单击导航 Logo 可快速访问品牌资源。

---

## 国际化

### 语言和区域设置

**区域感知格式：** 根据用户的区域设置格式化日期、时间、数字、分隔符和货币。

**优先选择语言设置而非位置：** 通过 `Accept-Language` 头和 `navigator.languages` 检测语言。永远不要依赖 IP/GPS 来确定语言。

### 日期/时间格式化

使用区域感知的格式化器：

```javascript
// JavaScript
const date = new Date(2024, 0, 15);
date.toLocaleDateString('zh-CN', { 
  year: 'numeric',
  month: 'long',
  day: 'numeric' 
});
// → "2024年1月15日"

date.toLocaleTimeString('zh-CN', { 
  hour: 'numeric', 
  minute: '2-digit' 
});
// → "上午9:00"
```

### 数字和货币

**一致的货币格式：** 在任何给定上下文中，货币显示应为 0 或 2 位小数，不要混用。

```javascript
// 一致的 0 位小数
¥50

// 一致的 2 位小数
¥50.00

// 不要在同一上下文中混用：¥50 和 ¥50.00
```

**数字和单位之间用空格分隔：**
- `10 MB`（而不是 `10MB`）
- 使用不换行空格：`10&nbsp;MB`

---

## 表单

### 键盘交互

**回车提交：** 当文本输入框被聚焦时，如果是唯一控件，回车键提交。如果有多个控件，对最后一个控件应用此规则。

**文本区域行为：** 在 `<textarea>` 中，⌘/⌃+Enter 提交；Enter 插入新行。

### 标签

**所有地方都要有标签：** 每个控件都有 `<label>` 或与标签关联，以支持辅助技术。

```jsx
// 显式标签
<label>
  电子邮箱
  <input type="email" name="email" />
</label>

// 隐式关联
<label for="email">电子邮箱</label>
<input id="email" type="email" name="email" />
```

**标签激活：** 单击 `<label>` 会聚焦关联的控件。

### 提交

**提交规则：** 在提交开始前保持提交按钮启用；然后在请求进行中时禁用，显示加载指示器，并包含幂等键。

**不要预先禁用提交：** 允许提交不完整的表单以显示验证反馈。

**未保存的更改：** 当可能丢失数据时，在导航前警告用户。

### 验证

**不要阻止输入：** 即使字段只接受数字，也允许任何输入并显示验证反馈。完全阻止按键会令人困惑，因为用户无法获得解释。

**错误放置：** 在字段旁边显示错误；提交时，聚焦第一个错误。

### 输入最佳实践

**自动完成和名称：** 设置 `autocomplete` 和有意义的 `name` 值以启用自动填充。

```jsx
<input type="email" name="email" autocomplete="email" />
<input type="tel" name="phone" autocomplete="tel" />
<input type="text" name="username" autocomplete="username" />
```

**选择性拼写检查：** 对电子邮件、代码、用户名等禁用。

```jsx
<input type="email" name="email" spellcheck="false" />
```

**正确的类型和输入模式：** 使用正确的 `type` 和 `inputmode` 以获得更好的键盘和验证。

```jsx
<input type="email" inputmode="email" />
<input type="tel" inputmode="tel" />
<input type="number" inputmode="numeric" />
```

**占位符表示为空：** 以省略号结尾。

```jsx
<input placeholder="请输入您的电子邮箱..." />
```

**占位符值：** 将占位符设置为例值或模式：
- `+1 (123) 456-7890`
- `sk-012345679…`

### 控件和点击区域

**控件上没有死区：** 复选框和单选按钮避免死区；标签和控件共享一个宽大的点击目标。

**Windows `<select>` 背景：** 在原生 `<select>` 上显式设置 `background-color` 和 `color` 以避免 Windows 上的暗模式对比度错误。

### 认证字段

**密码管理器和 2FA：** 确保兼容性并允许粘贴一次性验证码。

**不要为非认证字段触发密码管理器：** 对于"搜索"等输入，避免保留名称（例如密码），使用 `autocomplete="off"` 或特定标记如 `autocomplete="one-time-code"` 用于 OTP 字段。

**文本替换和扩展：** 某些输入方法会添加尾随空格。输入应修剪值以避免显示令人困惑的错误消息。

---

## 性能

### 测试和测量

**设备/浏览器矩阵：** 测试 iOS 低功耗模式和 macOS Safari。

**可靠测量：** 禁用增加开销或改变运行时行为的扩展。

**跟踪重渲染：** 最小化并加快重渲染。使用 [React DevTools](https://react.dev/learn/react-developer-tools) 或 [React Scan](https://react-scan.com/)。

**分析时限制：** 使用 CPU 和网络限制进行测试。

### 布局和渲染

**最小化布局工作：** 批量读取/写入；避免不必要的重排/重绘。

**网络延迟预算：** `POST/PATCH/DELETE` 在 <500ms 内完成。

**按键成本：** 优先使用非受控输入；使受控循环成本低廉。

### 列表和大型内容

**大型列表：** 虚拟化大型列表（例如 [virtua](https://github.com/inokawa/virtua) 或 `content-visibility: auto`）。

### 图像和媒体

**智能预加载：** 仅预加载首屏图像；延迟加载其余部分。

**无图像导致的 CLS：** 设置明确的图像尺寸并保留空间。

```jsx
<img 
  src="hero.jpg" 
  alt="Hero 图像"
  width="800" 
  height="400"
  loading="lazy"
/>
```

**预连接到源：** 使用 `<link rel="preconnect">` 连接资源/CDN 域名（需要时使用 crossorigin）以减少 DNS/TLS 延迟。

```html
<link rel="preconnect" href="https://cdn.example.com" />
<link rel="preconnect" href="https://cdn.example.com" crossorigin />
```

### 字体

**预加载字体：** 对于关键文本以避免闪烁和布局偏移。

```html
<link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin />
```

**子集字体：** 通过 unicode-range 仅发送您使用的码点/脚本（将可变轴限制在您需要的范围内）以缩小大小。

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-var.woff2') format('woff2');
  unicode-range: U+0000-00FF;
}
```

### 工作线程

**不要将主线程用于昂贵的工作：** 将特别长的任务移至 [Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API) 以避免阻塞页面的交互。

```javascript
// main.js
const worker = new Worker('expensive-task.js');

worker.postMessage({ data: largeDataset });

worker.onmessage = (event) => {
  console.log('结果:', event.data);
};
```

---

## 视觉设计

### 阴影

**分层阴影：** 使用至少两层模拟环境光和直射光。

```css
box-shadow: 
  0 1px 1px rgba(0, 0, 0, 0.05),
  0 4px 6px rgba(0, 0, 0, 0.1);
```

### 边框

**清晰的边框：** 结合边框和阴影；半透明边框提高边缘清晰度。

```css
border: 1px solid rgba(0, 0, 0, 0.1);
```

### 边框圆角

**嵌套圆角：** 子元素圆角 ≤ 父元素圆角且同心，使曲线对齐。

```css
.card {
  border-radius: 12px;
}

.card .button {
  border-radius: 8px; /* ≤ 12px */
}
```

### 颜色

**色调一致性：** 在非中性背景上，边框/阴影/文本向相同色调着色。

```css
.surface-blue {
  border-color: rgba(59, 130, 246, 0.2);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
}
```

**无障碍图表：** 使用色盲友好的调色板。

**最小对比度：** 优先使用 [APCA](https://apcacontrast.com/) 而非 [WCAG 2](https://webaim.org/resources/contrastchecker/) 以获得更准确的感知对比度。

**交互增加对比度：** `:hover`、`:active`、`:focus` 比静止状态具有更多对比度。

```css
button {
  background: #2563eb;
}

button:hover {
  background: #1d4ed8; /* 更深以增加对比度 */
}

button:focus {
  outline: 2px solid #000;
  outline-offset: 2px;
}
```

### 浏览器集成

**浏览器 UI 匹配您的背景：** 设置 `<meta name="theme-color" content="#000000">` 以将浏览器的主题颜色与页面背景对齐。

```html
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)" />
```

**设置适当的 color-scheme：** 在暗主题中为 `<html>` 标签设置 `color-scheme: dark`，以便滚动条和其他设备 UI 具有适当的对比度。

```css
:root {
  color-scheme: light dark;
}
```

### 排版

**文本抗锯齿和变换：** 缩放文本可能会改变平滑度。优先动画化包装器而不是文本节点。如果持续存在伪影，设置 `translateZ(0)` 或 `will-change: transform` 将其提升到自己的图层。

```css
.scale-wrapper {
  transform: scale(1.1);
  will-change: transform;
}
```

### 渐变

**避免渐变条纹：** 某些颜色和显示类型会有颜色条纹。可以使用遮罩代替。

---

## 文案写作

### 语气和语调

**主动语态：**
- ❌ "CLI 将被安装"
- ✅ "安装 CLI"

**标题和按钮使用标题大小写**（[芝加哥](https://title.sh/)）。在营销页面上，使用句子大小写。

**清晰简洁：** 使用尽可能少的词语。

**优先使用 `&` 而非 `and`。**

**以行动为导向的语言：**
- ❌ "您将需要 CLI…"
- ✅ "安装 CLI…"

**保持名词一致：** 引入尽可能少的独特术语。

**使用第二人称：** 避免第一人称。

### 占位符和示例

**使用一致的占位符：**
- 字符串：`YOUR_API_TOKEN_HERE`
- 数字：`0123456789`

### 数字和度量

**使用数字表示计数：**
- ❌ "八个部署"
- ✅ "8 个部署"

**数字和单位之间用空格分隔：**
- ❌ `10MB`
- ✅ `10 MB`
- 使用不换行空格：`10&nbsp;MB`

### 错误消息

**默认使用积极语言：** 以鼓励性和解决问题的方式表达消息，即使是错误消息。

- ❌ "您的部署失败"
- ✅ "出现了问题—请重试或联系支持。"

**错误消息引导退出：** 不要只说明出了什么问题—告诉用户如何修复它。

- ❌ "无效的 API 密钥"
- ✅ "您的 API 密钥不正确或已过期。在您的账户设置中生成新密钥。"

文案和按钮/链接应该教育并提供明确的操作。

### 清晰度

**避免歧义：** 标签清晰且具体。

- ❌ 按钮标签"继续"
- ✅ "保存 API 密钥"

---

## 资源

- [Vercel 设计指南](https://vercel.com/design/guidelines)
- [Chrome 无障碍树](https://developer.chrome.com/blog/full-accessibility-tree)
- [APCA 对比度](https://apcacontrast.com/)
- [React DevTools](https://react.dev/learn/react-developer-tools)
- [React Scan](https://react-scan.com/)
- [Virtua 虚拟化](https://github.com/inokawa/virtua)
- [Web Workers API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API)
- [标题大小写转换器](https://title.sh/)

---

## 使用示例

### 构建表单

1. 使用正确的输入类型和自动完成属性
2. 为所有控件添加标签
3. 处理键盘交互（回车提交）
4. 不要阻止输入；显示验证反馈
5. 在字段旁边显示错误
6. 在提交期间禁用提交，显示加载指示器

### 优化性能

1. 设置明确的图像尺寸
2. 预加载首屏内容
3. 延迟加载下方的图像
4. 预连接到 CDN 源
5. 对昂贵操作使用 Web Workers
6. 虚拟化大型列表

### 改善无障碍

1. 使用语义化 HTML 元素
2. 为仅图标按钮添加 ARIA 标签
3. 设置适当的标题层次结构
4. 添加跳转到内容链接
5. 确保足够的颜色对比度
6. 使用屏幕阅读器测试

### 国际化

1. 通过 Accept-Language 头检测语言
2. 为用户的区域设置格式化日期/数字/货币
3. 对粘合术语使用不换行空格
4. 不要依赖 IP/GPS 进行语言检测