---
name: har-to-vue
description: 将 HAR（HTTP Archive）文件转换为 Vue 源代码。支持批量转换网络请求为 Vue 组件、API 调用或页面数据结构，用于复刻网站或快速生成基于现有 API 的 Vue 应用。当 Claude 需要处理 HAR 文件以：（1）从浏览器抓包数据生成 Vue 代码，（2）批量转换多个请求为 API 服务，（3）复刻现有网站的 Vue 技术栈实现，（4）生成带有数据绑定的组件模板时使用。
---

# HAR to Vue 转换器

将 HAR 文件转换为 Vue 源代码，支持批量处理网络请求并生成可复用的 Vue 组件和 API 服务。

## 快速开始

### 基本转换

```bash
# 转换单个 HAR 文件为 Vue 组件
bun scripts/har_to_vue.ts input.har -o output.vue

# 批量转换所有请求为 API 服务
bun scripts/har_to_vue.ts input.har --mode api -o services/
```

### 常用场景

**复刻网站组件：**
```bash
bun scripts/har_to_vue.ts capture.har --mode component --template composition -o components/
```

**生成 API 服务：**
```bash
bun scripts/har_to_vue.ts capture.har --mode api --library axios -o api/
```

**完整页面生成：**
```bash
bun scripts/har_to_vue.ts capture.har --mode page -o pages/home/
```

## 转换模式

### Component 模式

将 HAR 请求转换为 Vue 组件，包含数据绑定和模板结构。

**生成内容：**
- 响应数据的响应式状态（ref/reactive）
- 数据获取逻辑（onMounted/computed）
- 基于 JSON 结构的模板

**选项：**
- `--template <composition|options>`: 使用 Composition API 或 Options API
- `--typescript`: 生成 TypeScript 类型定义
- `--with-props`: 从请求参数生成 props 定义

### API 模式

将 HAR 请求转换为 API 服务函数。

**生成内容：**
- 每个请求对应的函数
- TypeScript 类型定义
- 请求/响应接口
- 错误处理

**选项：**
- `--library <fetch|axios|ky>`: HTTP 客户端库
- `--base-url`: 注入基础 URL
- `--group-by <path|domain>`: 分组策略

### Page 模式

生成完整的 Vue 页面，包含布局、路由和状态管理。

**生成内容：**
- 页面组件
- 路由配置
- API 服务文件
- 类型定义
- Store（Pinia/Vuex）集成

**选项：**
- `--with-router`: 生成路由配置
- `--with-store`: 生成状态管理
- `--layout <default|admin|blank>`: 布局模板

## HAR 解析规则

### 请求映射

| HAR 字段 | Vue 映射 |
|---------|---------|
| `request.method` | HTTP 方法（GET/POST/PUT/DELETE） |
| `request.url` | API 端点路径 |
| `request.headers` | 请求头配置 |
| `request.postData` | 请求体（JSON/FormData） |
| `response.content` | 响应数据结构 |

### 类型推断

- 自动从 JSON 响应推断 TypeScript 接口
- 数组项提取为独立类型
- 枚举值生成为 union types
- 可选字段标记为 `?`

### 命名规范

- URL 路径 → 函数名（`/api/users` → `getUsers`）
- 驼峰转换（`user_profile` → `UserProfile`）
- 移除重复前缀（`getUserList` → `getList`）

## 输出结构

### Component 模式输出

```
UserList.vue
├── <script setup>
│   ├── imports（ref, onMounted, 等）
│   ├── types（接口定义）
│   ├── state（响应式数据）
│   ├── methods（数据获取）
│   └── lifecycle（onMounted）
├── <template>
│   └── 基于 JSON 结构的绑定
└── <style>
    └── 基础样式
```

### API 模式输出

```
api/
├── index.ts          # 导出所有 API
├── types.ts          # 类型定义
├── users.ts          # 用户相关 API
├── products.ts       # 产品相关 API
└── utils.ts          # 请求工具（拦截器、错误处理）
```

### Page 模式输出

```
pages/
└── dashboard/
    ├── index.vue     # 页面组件
    ├── api.ts        # API 服务
    ├── types.ts      # 类型定义
    ├── router.ts     # 路由配置
    └── store.ts      # 状态管理
```

## 高级功能

### 请求分组

按 URL 模式自动分组 API：

```bash
# 按路径分组
bun scripts/har_to_vue.ts input.har --group-by path

# 按域名分组
bun scripts/har_to_vue.ts input.har --group-by domain

# 自定义分组规则
bun scripts/har_to_vue.ts input.har --group-config custom-rules.json
```

### 过滤请求

```bash
# 仅包含特定域名
bun scripts/har_to_vue.ts input.har --filter-domain api.example.com

# 排除静态资源
bun scripts/har_to_vue.ts input.har --exclude-extensions css,js,png,jpg

# 仅包含特定方法
bun scripts/har_to_vue.ts input.har --methods GET,POST
```

### 模板定制

使用自定义模板文件：

```bash
bun scripts/har_to_vue.ts input.har --template-file templates/custom.vue
```

模板变量：
- `{{ requests }}`: 请求列表
- `{{ types }}`: 类型定义
- `{{ imports }}`: 导入语句
- `{{ componentName }}`: 组件名称

## 配置文件

支持配置文件 `har-to-vue.config.json`：

```json
{
  "mode": "component",
  "template": "composition",
  "typescript": true,
  "library": "axios",
  "output": "./src",
  "filter": {
    "includeDomains": ["api.example.com"],
    "excludeExtensions": ["css", "js", "png"]
  },
  "naming": {
    "style": "camelCase",
    "removePrefixes": ["get", "fetch"]
  }
}
```

## 最佳实践

### 1. 清理 HAR 文件

转换前清理不必要的请求：
- 过滤静态资源（图片、CSS、JS）
- 移除开发工具请求（hot reload、sourcemaps）
- 保留业务相关 API

### 2. 类型优化

手动优化生成的类型：
- 合并重复的类型定义
- 提取通用接口
- 添加适当的注释

### 3. 错误处理

添加统一的错误处理：
```typescript
// utils.ts
export async function fetchWithErrorHandler(url: string) {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(response.statusText);
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}
```

### 4. 环境变量

使用环境变量管理 API 配置：
```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://api.example.com';
```

## 参考资料

- [HAR 格式规范](references/HAR_SPEC.md)
- [Vue 3 Composition API](references/VUE_COMPOSITION.md)
- [TypeScript 类型推断](references/TS_INFERENCE.md)
- [Axios 拦截器](references/AXIOS_INTERCEPTORS.md)
- [常见转换模式](references/PATTERNS.md)