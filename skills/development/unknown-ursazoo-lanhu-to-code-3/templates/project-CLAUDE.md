# [项目名称]

> 使用说明：将此文件复制到项目根目录，命名为 CLAUDE.md，按项目实际情况填写方括号内容。

## 构建命令

```bash
npm run dev        # 开发服务器
npm run build      # 生产构建
npm run lint       # ESLint 检查
npm run type-check # TypeScript 类型检查（如有）
```

## 技术栈

- 框架：[Vue 3 / React / ...]
- UI 库：[Element Plus / Ant Design / 无]
- 状态管理：[Pinia / Vuex / Zustand / 无]
- HTTP 客户端：[axios / fetch]
- CSS 方案：[UnoCSS / Tailwind / SCSS / CSS Modules]

## 文档目录（影响 code-format 生成质量）

| 文件 | 作用 | 缺失影响 |
|------|------|----------|
| `docs/components.md` | 可复用组件目录，含 props/用法 | 无法复用组件，生成重复代码 |
| `docs/tech-spec.md` | API 接口、枚举定义、交互逻辑 | 只能生成纯视图，数据逻辑全标 TODO |
| `docs/dev-spec.md` | 命名规范、文件结构、样式规范 | 可能不符合团队编码规范 |

## 架构边界

- 新增组件前必须查 `docs/components.md`，有近似组件优先复用
- API 路径必须来自 `docs/tech-spec.md`，找不到用 `// TODO:` 标记
- 枚举/常量使用 tech-spec.md 中定义的，禁止硬编码中文状态字符串

## 编码约定

- 参见 `docs/dev-spec.md`
- 缺失时扫描 `src/` 中现有文件推断风格，并在输出中说明

## NEVER / ALWAYS

**NEVER:**
- 用 `// ... rest of component` 等占位符省略代码
- 猜测 props 名称，必须以 `docs/components.md` 为准
- 自行发明 API 路径
- 硬编码枚举显示文字

**ALWAYS:**
- 写完整代码，不确定的逻辑用 `// TODO: 待确认` 标记
- 图片使用 `assets/` 中的实际文件路径
- 颜色/间距/字号精确匹配蓝湖数据

## 验证

```bash
npm run build && npm run lint
```

## Compact Instructions

<!-- 上下文压缩后 Claude 必须保留的信息 -->
技术栈：[填写技术栈摘要，如 "Vue 3 + Element Plus + Pinia + axios"]
组件文档：docs/components.md（code-format 必读）
接口约定：docs/tech-spec.md（API 路径/枚举来源）
