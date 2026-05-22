---
name: nitro-api-development
description: 使用 Nitro v3 框架编写服务端接口的技能规范。适用于初始化纯后端 Nitro 项目、为 Vite 项目赋予全栈能力、编写符合规范的 Nitro 接口。当用户需要创建 Nitro 接口、初始化 Nitro 配置、或咨询 Nitro 开发规范时使用此技能。
metadata:
  version: "0.13.4"
---

# Nitro v3 接口开发技能规范

本技能用于指导使用 Nitro v3 框架编写服务端接口，包括项目初始化、配置、接口编写规范等完整流程。

## 1. 适用场景

- **纯后端 Nitro 项目初始化**：对非 Vite 的 Node.js 项目，初始化 Nitro 示例代码和配置
- **Vite 项目全栈化**：对 Vite 项目，初始化 Nitro 接口和配置，赋予全栈能力
- **接口开发与维护**：按规范编写 Nitro v3 格式的接口代码

## 2. 核心依赖

```bash
# Nitro v3 核心包
pnpm add nitro

# 可选：日志工具
pnpm add consola
```

## 3. 目录结构规范

Nitro 支持两种目录结构，根据项目规模选择：

### 3.1 扁平结构（推荐用于小型项目）

```plain
project-root/
├── server/                          # Nitro 服务端目录
│   ├── routes/                      # API 路由目录
│   │   ├── users.get.ts             # GET /users
│   │   ├── users.post.ts            # POST /users
│   │   └── health.get.ts            # GET /health
│   └── db/                          # 数据库相关（可选）
│       └── index.ts
├── nitro.config.ts                  # Nitro 配置文件
└── package.json
```

### 3.2 模块化结构（适用于大型项目）

```plain
project-root/
├── server/                          # Nitro 服务端目录
│   ├── api/                         # API 接口目录
│   │   └── {module}/{feature}/
│   │       ├── list.post.ts         # 列表查询接口
│   │       └── [id].get.ts          # 详情接口
│   └── utils/                       # 工具函数（可选）
│       └── filter-data.ts
├── nitro.config.ts                  # Nitro 配置文件
└── package.json
```

**文件路径映射规则**：文件路径直接映射为 API 路径

```plain
文件: server/routes/users.get.ts     -> GET /users
文件: server/api/users/list.post.ts  -> POST /api/users/list
```

## 4. 核心规范 [CRITICAL]

### 4.1 导入模块规范

```typescript
// 必须从 nitro/h3 导入，不是 h3
import { defineHandler, readBody } from "nitro/h3";

// 类型导入（根据项目实际定义）
import type { UserItem, QueryParams } from "./types";
```

### 4.2 基础接口模板

```typescript
/**
 * @file 用户列表接口
 * @description User list API
 * GET /users
 */

import { defineHandler } from "nitro/h3";

export default defineHandler(async (event) => {
	return {
		success: true,
		data: [
			{ id: "1", name: "John" },
			{ id: "2", name: "Jane" },
		],
	};
});
```

### 4.3 带参数的接口模板

```typescript
/**
 * @file 创建用户接口
 * @description Create user API
 * POST /users
 */

import { defineHandler, readBody } from "nitro/h3";

interface CreateUserBody {
	name: string;
	email: string;
}

export default defineHandler(async (event) => {
	const body = await readBody<CreateUserBody>(event);

	if (!body.name || !body.email) {
		return {
			success: false,
			message: "name 和 email 是必填字段",
		};
	}

	// 处理业务逻辑...

	return {
		success: true,
		message: "创建成功",
		data: { id: "new-id", ...body },
	};
});
```

### 4.4 关键要点检查清单

1. **导入来源**：`nitro/h3` 而非 `h3`
2. **处理器函数**：`defineHandler` 而非 `defineEventHandler`
3. **JSDoc 注释**：包含接口路径和描述
4. **类型约束**：为请求体和响应添加类型定义

## 5. 常见错误对比

| 错误写法                                  | 正确写法                                     |
| :---------------------------------------- | :------------------------------------------- |
| `import { defineEventHandler } from "h3"` | `import { defineHandler } from "nitro/h3"`   |
| `export default defineEventHandler(...)`  | `export default defineHandler(...)`          |
| 缺少类型约束的请求体读取                  | `readBody<YourType>(event)`                  |
| 直接返回对象无结构                        | 返回 `{ success, message, data }` 结构化响应 |

## 6. Nitro 配置

### 6.1 基础配置

```typescript
import { defineConfig } from "nitro";

export default defineConfig({
	serverDir: "server",
	imports: false,
	compatibilityDate: "2024-09-19",
	devServer: {
		port: 3000,
	},
});
```

### 6.2 完整配置示例

```typescript
import { defineConfig } from "nitro";

export default defineConfig({
	/** 服务端代码目录 */
	serverDir: "server",

	/** 禁用自动导入，显式声明所有依赖 */
	imports: false,

	/** 兼容性日期 */
	compatibilityDate: "2024-09-19",

	/** 开发服务器配置 */
	devServer: {
		port: 3000,
		watch: ["./server/**/*.ts"],
	},

	/** 路径别名配置（可选） */
	alias: {
		"@": "./src",
		server: "./server",
	},
});
```

### 6.3 Vite 集成

```typescript
// vite.config.ts 或 build/plugins/index.ts
import { nitro } from "nitro/vite";

export default defineConfig({
	plugins: [
		// 其他插件...
		nitro(),
	],
});
```

## 7. 部署配置

### 7.1 环境变量规范

```bash
# Nitro 运行时配置前缀必须为 NITRO_
NITRO_API_TOKEN="your-api-token"

# 部署预设
NITRO_PRESET=cloudflare_module  # Cloudflare Workers
NITRO_PRESET=vercel             # Vercel
NITRO_PRESET=node               # Node.js 服务器
```

### 7.2 环境变量访问

```typescript
import { defineHandler } from "nitro/h3";
import { useRuntimeConfig } from "nitro/runtime-config";

export default defineHandler((event) => {
	// 必须在事件处理器内访问
	const config = useRuntimeConfig();
	return { value: config.apiToken };
});
```

## 8. 响应格式规范

推荐使用统一的响应格式，便于前端处理：

### 8.1 基础响应结构

```typescript
interface ApiResponse<T> {
	success: boolean;
	message?: string;
	data?: T;
}
```

### 8.2 分页响应结构（可选）

```typescript
interface PageResponse<T> {
	success: boolean;
	message?: string;
	data: {
		list: T[];
		total: number;
		pageIndex: number;
		pageSize: number;
		totalPages: number;
	};
}
```

## 9. 项目初始化检查清单

### 9.1 纯后端项目

- [ ] 安装 `nitro` 依赖包
- [ ] 创建 `server/routes/` 目录结构
- [ ] 创建 `nitro.config.ts` 配置文件
- [ ] 添加开发和构建脚本到 `package.json`

### 9.2 Vite 项目全栈化

- [ ] 安装 `nitro` 依赖包
- [ ] 在 Vite 插件配置中添加 `nitro()` 插件
- [ ] 创建 `server/` 目录结构
- [ ] 创建 `nitro.config.ts` 配置文件

## 10. 可选功能

### 10.1 数据筛选工具函数

如果项目需要 Mock 数据和筛选功能，可创建 `server/utils/filter-data.ts`，详见 [templates.md](templates.md)。

### 10.2 Mock 数据模板

对于需要模拟数据的开发场景，可参考 [templates.md](templates.md) 中的 Mock 数据模板。

## 11. 附加资源

详细的代码模板和参考文档请查阅：

- **初始化模板**：[templates.md](templates.md) - 包含完整的配置和接口代码模板
- **快速参考**：[reference.md](reference.md) - 函数速查、配置选项和常用类型
- **项目规范文档**：查阅本项目的规范文档目录
- **官方文档**：https://v3.nitro.build/
