---
name: ruoyi-project-navigator
description: |
  若依 RuoYi-Vue-Plus 框架项目结构导航与开发规范技能。
  
  **核心能力**：
  - Maven 多模块架构的职责定位与代码查找策略
  - Vue3 + TypeScript 前端分层结构与模块映射关系
  - 前后端分离架构下的文件组织与命名约定
  - 关键配置文件位置速查与全局配置修改指南
  - 新业务模块添加的标准流程与依赖管理
  
  **触发场景**：
  1. 查找功能实现位置（Controller/Service/Mapper/API/View）
  2. 理解模块间依赖关系（Maven/Pinia/Router）
  3. 添加新业务模块或功能
  4. 修改全局配置（安全/缓存/路由/权限）
  5. 排查前后端接口对应关系
  6. 分析代码分层结构与职责边界
  
  **触发关键词**：
  项目结构、目录导航、模块定位、代码组织、前后端分离、若依框架、RuoYi、
  Maven模块、Vue3目录、接口映射、分层架构、业务模块添加
---

# 若依 RuoYi-Vue-Plus 项目结构导航规范

> **框架背景**：RuoYi-Vue-Plus 是基于 SpringBoot + MyBatis-Plus + Vue3 + Element-Plus 的前后端分离快速开发框架，采用 Maven 多模块架构和现代化前端工程化方案。

## 核心规范

### 规范1：后端 Maven 模块职责定位与查找策略

**模块架构说明**：
若依后端采用多模块 Maven 架构，遵循「职责分离」和「分层解耦」原则。每个模块有明确的职责边界，代码查找时必须遵循模块职责原则。

**模块职责矩阵**：

| 模块名称 | 核心职责 | 典型内容 | 查找场景 |
|---------|---------|---------|---------|
| `ruoyi-admin` | 应用启动与接口入口 | Controller、Application启动类 | 查找API端点、启动配置 |
| `ruoyi-framework` | 框架核心功能 | 安全配置、拦截器、缓存、异常处理 | 修改全局配置、鉴权逻辑 |
| `ruoyi-common` | 通用工具与组件 | 工具类、注解、常量、枚举、异常类 | 查找工具方法、自定义注解 |
| `ruoyi-system` | 核心业务模块 | 用户/角色/菜单的 Domain/Mapper/Service | 系统管理相关业务逻辑 |
| 自定义模块 | 业务功能模块 | 特定业务的完整三层结构 | 业务功能开发 |

**完整目录结构**：

```text
ruoyi-vue-plus (父工程)
├── ruoyi-admin         # 【启动模块】管理后台入口
│   ├── src/main/java/com/ruoyi
│   │   ├── RuoYiApplication.java           # ⭐ SpringBoot 启动类
│   │   └── web/controller                  # ⭐ 控制器层 (RESTful API)
│   │       ├── system/SysUserController    # 用户管理接口
│   │       └── monitor/SysJobController    # 定时任务接口
│   └── src/main/resources
│       ├── application.yml                 # ⭐ 主配置文件
│       ├── application-dev.yml             # 开发环境配置
│       └── logback.xml                     # 日志配置
│
├── ruoyi-framework     # 【框架模块】底层支撑与核心功能
│   └── src/main/java/com/ruoyi/framework
│       ├── config                          # ⭐ 全局配置类
│       │   ├── SecurityConfig.java         # Spring Security 配置
│       │   ├── RedisConfig.java            # Redis 缓存配置
│       │   └── MybatisPlusConfig.java      # MyBatis-Plus 配置
│       ├── interceptor                     # 拦截器 (日志/权限/重复提交)
│       ├── aspectj                         # AOP 切面 (日志/数据权限)
│       └── web/exception                   # 全局异常处理器
│
├── ruoyi-common        # 【通用模块】工具类与公共组件
│   └── src/main/java/com/ruoyi/common
│       ├── utils                           # ⭐ 工具类库
│       │   ├── StringUtils.java            # 字符串工具
│       │   ├── DateUtils.java              # 日期工具
│       │   └── SecurityUtils.java          # 安全工具 (获取当前用户)
│       ├── annotation                      # ⭐ 自定义注解
│       │   ├── DataScope.java              # 数据权限注解
│       │   ├── Log.java                    # 操作日志注解
│       │   └── Excel.java                  # Excel 导出注解
│       ├── constant                        # 通用常量
│       ├── enums                           # 枚举类
│       ├── exception                       # 自定义异常类
│       └── core/domain                     # 通用实体基类
│           ├── BaseEntity.java             # 基础实体 (包含创建/修改信息)
│           └── R.java                      # 统一响应结果封装
│
├── ruoyi-system        # 【系统模块】核心业务功能
│   └── src/main/java/com/ruoyi/system
│       ├── domain                          # ⭐ 实体类 (Entity/DO)
│       │   ├── SysUser.java                # 用户实体
│       │   ├── SysRole.java                # 角色实体
│       │   └── SysMenu.java                # 菜单实体
│       ├── mapper                          # ⭐ MyBatis Mapper 接口
│       │   └── SysUserMapper.java          # 用户数据访问
│       ├── service                         # ⭐ 业务逻辑层
│       │   ├── ISysUserService.java        # 用户服务接口
│       │   └── impl
│       │       └── SysUserServiceImpl.java # 用户服务实现
│       └── domain/vo                       # 值对象 (View Object)
│           └── SysUserVo.java              # 用户视图对象
│
├── ruoyi-generator     # 【代码生成模块】代码生成器
├── ruoyi-quartz        # 【定时任务模块】任务调度
└── pom.xml             # ⭐ 父级依赖管理 (统一版本控制)
```

**代码查找决策树**：

1. **查找 API 端点** → `ruoyi-admin/controller` 目录
2. **查找业务逻辑** → 对应业务模块的 `service` 包
3. **查找数据库操作** → 对应业务模块的 `mapper` 包
4. **查找实体定义** → 对应业务模块的 `domain` 包
5. **查找工具方法** → `ruoyi-common/utils` 包
6. **查找全局配置** → `ruoyi-framework/config` 包
7. **查找自定义注解** → `ruoyi-common/annotation` 包
8. **查找常量定义** → `ruoyi-common/constant` 包

### 规范2：前端 Vue3 目录映射与分层结构

**架构说明**：
若依前端基于 Vue3 + TypeScript + Vite + Pinia，采用「模块化」和「职责分层」设计。核心原则是 API 定义与页面组件解耦，路由结构与视图目录一一对应。

**目录职责矩阵**：

| 目录 | 职责 | 对应关系 | 命名规范 |
|-----|------|---------|---------|
| `src/api` | 接口定义层 | 与后端 Controller 路径对应 | 模块名/功能名.ts |
| `src/views` | 页面视图层 | 与路由配置对应 | 模块名/功能名/index.vue |
| `src/components` | 全局组件 | 跨页面复用 | 大驼峰命名 |
| `src/store` | 状态管理 | Pinia stores | 模块名+Store.ts |
| `src/router` | 路由配置 | 动态路由+静态路由 | index.ts |
| `src/utils` | 前端工具 | 公共函数库 | 功能名.ts |

**完整目录结构**：

```text
ruoyi-ui (前端项目根目录)
├── public                  # 静态资源 (不经过编译)
│   └── favicon.ico
│
├── src                     # 源代码目录
│   ├── api                 # 【接口层】API 定义 (与后端 Controller 对应)
│   │   ├── system          # 系统模块接口组
│   │   │   ├── user.ts     # ⭐ 用户管理接口 → /system/user/*
│   │   │   ├── role.ts     # 角色管理接口 → /system/role/*
│   │   │   └── menu.ts     # 菜单管理接口 → /system/menu/*
│   │   ├── monitor         # 监控模块接口组
│   │   │   ├── online.ts   # 在线用户接口
│   │   │   └── job.ts      # 定时任务接口
│   │   └── login.ts        # ⭐ 登录/注销接口
│   │
│   ├── assets              # 【静态资源】样式/图片/图标
│   │   ├── styles          # 全局样式
│   │   │   ├── index.scss  # ⭐ 主样式入口
│   │   │   └── variables.scss  # CSS 变量
│   │   ├── images          # 图片资源
│   │   └── icons           # SVG 图标
│   │
│   ├── components          # 【全局组件】跨页面复用
│   │   ├── TableHeader     # 表格头部组件
│   │   ├── Upload          # 文件上传组件
│   │   ├── ImagePreview    # 图片预览组件
│   │   └── DictTag         # 字典标签组件
│   │
│   ├── layout              # 【布局组件】框架布局
│   │   ├── components
│   │   │   ├── Sidebar     # 侧边栏
│   │   │   ├── Navbar      # 顶部导航
│   │   │   └── TagsView    # 标签页
│   │   └── index.vue       # ⭐ 主布局容器
│   │
│   ├── router              # 【路由配置】
│   │   ├── index.ts        # ⭐ 路由主文件 (路由守卫/动态路由)
│   │   └── routes.ts       # 静态路由定义
│   │
│   ├── store               # 【状态管理】Pinia stores
│   │   ├── modules
│   │   │   ├── user.ts     # ⭐ 用户状态 (token/权限/角色)
│   │   │   ├── app.ts      # 应用状态 (侧边栏/主题)
│   │   │   └── permission.ts  # 权限状态 (动态路由)
│   │   └── index.ts        # store 入口
│   │
│   ├── utils               # 【工具函数】前端工具类
│   │   ├── request.ts      # ⭐ Axios 封装 (请求/响应拦截)
│   │   ├── auth.ts         # ⭐ Token 管理 (存取/清除)
│   │   ├── validate.ts     # 表单验证规则
│   │   └── dict.ts         # 字典数据工具
│   │
│   ├── views               # 【页面层】业务页面组件 (与路由对应)
│   │   ├── system          # 系统管理模块页面
│   │   │   ├── user        # ⭐ 用户管理页面
│   │   │   │   ├── index.vue       # 用户列表主页
│   │   │   │   ├── profile.vue     # 用户个人资料
│   │   │   │   └── authRole.vue    # 用户授权
│   │   │   ├── role        # 角色管理页面
│   │   │   │   └── index.vue
│   │   │   └── menu        # 菜单管理页面
│   │   │       └── index.vue
│   │   ├── monitor         # 系统监控模块页面
│   │   │   ├── online      # 在线用户
│   │   │   │   └── index.vue
│   │   │   └── job         # 定时任务
│   │   │       └── index.vue
│   │   ├── login.vue       # ⭐ 登录页
│   │   └── index.vue       # ⭐ 首页 Dashboard
│   │
│   ├── App.vue             # 根组件
│   ├── main.ts             # ⭐ 应用入口 (Vue实例创建)
│   └── permission.ts       # 权限控制 (路由守卫)
│
├── types                   # 【类型定义】TypeScript 类型声明
│   ├── api.d.ts            # API 接口类型
│   ├── global.d.ts         # 全局类型
│   └── vue-router.d.ts     # 路由类型扩展
│
├── .env.development        # ⭐ 开发环境变量 (API地址)
├── .env.production         # ⭐ 生产环境变量
├── index.html              # HTML 入口
├── vite.config.ts          # ⭐ Vite 构建配置 (代理/插件)
├── tsconfig.json           # TypeScript 配置
├── package.json            # ⭐ 依赖管理
└── .eslintrc.js            # ESLint 代码规范
```

**关键映射关系**：

1. **API → Controller 映射**：
   ```
   前端: src/api/system/user.ts
          ↓ 对应
   后端: ruoyi-admin/.../controller/system/SysUserController.java
   ```

2. **View → Router 映射**：
   ```
   路由: /system/user
          ↓ 对应
   页面: src/views/system/user/index.vue
   ```

3. **Store → 业务状态映射**：
   ```
   用户登录状态: src/store/modules/user.ts
   权限路由状态: src/store/modules/permission.ts
   ```

**组件通信与数据流**：

```
用户操作 → View 组件
         ↓
      调用 API (src/api/*.ts)
         ↓
      发起 HTTP 请求 (utils/request.ts)
         ↓
      后端 Controller 处理
         ↓
      返回数据 → 更新 View
         ↓ (如需全局状态)
      更新 Pinia Store
```

### 规范3：新业务模块添加标准流程

**场景说明**：当需要添加一个新的业务模块时（如「商品管理」、「订单系统」），需按以下标准流程操作，确保前后端结构一致性。

**后端模块添加流程**：

1. **创建 Maven 模块**（可选，简单功能可放在 ruoyi-system）：
   ```xml
   <!-- 在父 pom.xml 中添加模块 -->
   <module>ruoyi-product</module>
   ```

2. **创建标准三层结构**：
   ```text
   ruoyi-product/src/main/java/com/ruoyi/product
   ├── domain
   │   └── Product.java           # 实体类 (继承 BaseEntity)
   ├── mapper
   │   └── ProductMapper.java     # Mapper 接口
   ├── service
   │   ├── IProductService.java   # 服务接口
   │   └── impl
   │       └── ProductServiceImpl.java  # 服务实现
   └── controller (在 ruoyi-admin 中)
       └── ProductController.java # 控制器
   ```

3. **配置 Mapper XML**（如果使用 XML 方式）：
   ```text
   ruoyi-product/src/main/resources/mapper/product
   └── ProductMapper.xml
   ```

4. **添加依赖关系**：
   ```xml
   <!-- ruoyi-admin 的 pom.xml 中添加 -->
   <dependency>
       <groupId>com.ruoyi</groupId>
       <artifactId>ruoyi-product</artifactId>
   </dependency>
   ```

**前端模块添加流程**：

1. **创建 API 接口文件**：
   ```typescript
   // src/api/product/product.ts
   import request from '@/utils/request'
   
   // 查询商品列表
   export function listProduct(query: any) {
     return request({
       url: '/product/list',
       method: 'get',
       params: query
     })
   }
   ```

2. **创建页面视图**：
   ```text
   src/views/product
   ├── index.vue          # 列表页面
   ├── detail.vue         # 详情页面
   └── components         # 页面专属组件
       └── ProductForm.vue
   ```

3. **配置路由**：
   ```typescript
   // src/router/index.ts 或通过后端动态路由返回
   {
     path: '/product',
     component: Layout,
     children: [
       {
         path: 'list',
         name: 'ProductList',
         component: () => import('@/views/product/index.vue'),
         meta: { title: '商品管理', icon: 'product' }
       }
     ]
   }
   ```

4. **添加状态管理**（可选，复杂状态才需要）：
   ```typescript
   // src/store/modules/product.ts
   import { defineStore } from 'pinia'
   
   export const useProductStore = defineStore('product', {
     state: () => ({
       productList: []
     }),
     actions: {
       setProductList(list: any[]) {
         this.productList = list
       }
     }
   })
   ```

### 规范4：关键配置文件速查表

**后端关键配置**：

| 配置文件 | 路径 | 配置内容 |
|---------|------|---------|
| 主配置文件 | `ruoyi-admin/src/main/resources/application.yml` | 端口/数据库/Redis/日志级别 |
| 开发环境 | `application-dev.yml` | 开发环境特定配置 |
| 生产环境 | `application-prod.yml` | 生产环境配置 |
| MyBatis配置 | `mybatis-config.xml` 或 Java Config | Mapper 扫描/插件配置 |
| 日志配置 | `logback.xml` | 日志输出格式/级别/文件 |
| Maven依赖 | 各模块 `pom.xml` | 依赖版本/插件配置 |

**前端关键配置**：

| 配置文件 | 路径 | 配置内容 |
|---------|------|---------|
| Vite配置 | `vite.config.ts` | 代理/插件/构建优化 |
| 环境变量 | `.env.development` / `.env.production` | API地址/全局变量 |
| TypeScript | `tsconfig.json` | 编译选项/路径别名 |
| ESLint | `.eslintrc.js` | 代码规范配置 |
| 包管理 | `package.json` | 依赖版本/脚本命令 |

**常用配置示例**：

```yaml
# application.yml - 修改端口
server:
  port: 8080

# application.yml - 数据库配置
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/ry-vue-plus?useSSL=false
    username: root
    password: password
```

```typescript
// vite.config.ts - 配置代理
export default defineConfig({
  server: {
    proxy: {
      '/dev-api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/dev-api/, '')
      }
    }
  }
})
```

```bash
# .env.development - 配置API地址
VITE_APP_BASE_API = '/dev-api'
VITE_APP_ENV = 'development'
```

## 禁止事项

### 后端开发禁止事项

- ❌ **禁止将业务逻辑代码放入 `ruoyi-common` 模块**  
  → `common` 模块只能存放无状态的通用工具类、注解、常量、枚举，不能包含任何业务逻辑。  
  → 反例：在 `common` 中写用户登录验证、订单计算逻辑。  
  → 正例：在 `common` 中写字符串处理、日期格式化工具。

- ❌ **禁止在 `ruoyi-admin` 模块中编写深层业务逻辑**  
  → `admin` 模块只能包含 Controller、Application 启动类、全局配置类。  
  → 反例：在 Controller 中直接写复杂的数据库查询、业务计算逻辑。  
  → 正例：Controller 只负责参数校验、调用 Service、返回结果。

- ❌ **禁止随意修改 `ruoyi-framework` 中的核心安全配置**  
  → 除非完全理解 Spring Security 配置对全局鉴权、CSRF、CORS 的影响。  
  → 修改前必须：备份配置 → 理解影响范围 → 本地测试 → 代码审查。

- ❌ **禁止在 Java 实体类（Domain/Entity）中编写业务方法**  
  → 实体类应保持为纯 POJO（Plain Old Java Object），只包含属性、getter/setter。  
  → 反例：在 `SysUser.java` 中写 `checkPassword()` 业务验证方法。  
  → 正例：将业务方法放在 Service 层或工具类中。

- ❌ **禁止跨模块循环依赖**  
  → Maven 模块间只能单向依赖，不能出现 A 依赖 B，B 又依赖 A 的情况。  
  → 依赖方向：业务模块 → framework → common。

- ❌ **禁止在 Mapper 层写复杂业务逻辑**  
  → Mapper 只负责数据访问，SQL 查询应尽量简洁。  
  → 复杂的数据处理、业务判断应放在 Service 层。

- ❌ **禁止硬编码敏感信息**  
  → 数据库密码、API密钥、Token密钥等必须写在配置文件或环境变量中。  
  → 使用 Jasypt 等工具对敏感配置加密。

### 前端开发禁止事项

- ❌ **禁止在 `src/views` 目录中直接书写 API 调用逻辑**  
  → 必须将 API 定义解耦至 `src/api` 目录，保持页面组件的纯粹性。  
  → 反例：在 `index.vue` 中直接写 `axios.get('/system/user/list')`。  
  → 正例：导入 `import { listUser } from '@/api/system/user'` 并调用。

- ❌ **禁止破坏 `api` 与 `views` 的目录对应关系**  
  → API 目录结构必须与后端 Controller 模块保持一致。  
  → 反例：`api/user.ts` 对应后端 `/system/user` 和 `/monitor/online`。  
  → 正例：分别创建 `api/system/user.ts` 和 `api/monitor/online.ts`。

- ❌ **禁止在全局组件中包含业务逻辑**  
  → `src/components` 中的组件应该是无状态的、可复用的展示组件。  
  → 反例：在全局组件中调用特定业务 API、写死业务数据。  
  → 正例：通过 props 传递数据，emit 事件通知父组件。

- ❌ **禁止在页面组件中直接操作 LocalStorage/SessionStorage**  
  → 应该封装在 `src/utils/auth.ts` 等工具文件中统一管理。  
  → 避免 Token、用户信息的存取逻辑散落在各个页面。

- ❌ **禁止滥用 Pinia Store**  
  → 只有需要跨组件共享的状态才放入 Store（如用户信息、权限、主题）。  
  → 页面内部状态使用 Vue 的 `ref`/`reactive` 即可。

- ❌ **禁止忽略 TypeScript 类型检查**  
  → 不要使用 `any` 类型逃避类型检查，应定义明确的接口类型。  
  → 反例：`const data: any = response.data`。  
  → 正例：`const data: UserInfo = response.data`。

- ❌ **禁止在生产环境暴露 console.log 和调试代码**  
  → 使用 Vite 的环境变量控制日志输出。  
  → 构建时应移除所有 `console.log`、`debugger`。

- ❌ **禁止硬编码路由路径和 API 地址**  
  → 路由路径应定义为常量或使用路由对象的 `name` 属性。  
  → API 地址应使用环境变量（`.env` 文件）配置。

### 前后端协作禁止事项

- ❌ **禁止前后端接口不匹配**  
  → 接口变更必须同步更新前端 API 定义和后端 Controller。  
  → 使用接口文档（Swagger/Apifox）作为唯一真相源。

- ❌ **禁止未经约定修改接口返回格式**  
  → 后端统一使用 `R<T>` 封装响应，前端统一在拦截器处理。  
  → 任何格式变更必须团队讨论并更新规范。

- ❌ **禁止在前端绕过权限校验**  
  → 权限控制必须前后端双重校验，前端隐藏按钮不代表后端可以不校验。  
  → 后端接口必须使用 `@PreAuthorize` 或数据权限注解保护。

## 参考代码与关键文件路径

### 后端关键文件

**启动与配置**：
- `ruoyi-admin/src/main/java/com/ruoyi/RuoYiApplication.java` - SpringBoot 启动类
- `ruoyi-admin/src/main/resources/application.yml` - 主配置文件
- `ruoyi-admin/src/main/resources/application-dev.yml` - 开发环境配置
- `ruoyi-admin/src/main/resources/logback.xml` - 日志配置
- `pom.xml` - 根目录父 POM（查看模块依赖关系）

**核心框架**：
- `ruoyi-framework/src/main/java/com/ruoyi/framework/config/SecurityConfig.java` - 安全配置
- `ruoyi-framework/src/main/java/com/ruoyi/framework/config/RedisConfig.java` - 缓存配置
- `ruoyi-framework/src/main/java/com/ruoyi/framework/interceptor/RepeatSubmitInterceptor.java` - 重复提交拦截器
- `ruoyi-framework/src/main/java/com/ruoyi/framework/aspectj/DataScopeAspect.java` - 数据权限切面

**工具类参考**：
- `ruoyi-common/src/main/java/com/ruoyi/common/utils/SecurityUtils.java` - 安全工具（获取当前用户）
- `ruoyi-common/src/main/java/com/ruoyi/common/utils/StringUtils.java` - 字符串工具
- `ruoyi-common/src/main/java/com/ruoyi/common/core/domain/R.java` - 统一响应结果封装
- `ruoyi-common/src/main/java/com/ruoyi/common/annotation/Log.java` - 操作日志注解

**业务代码示例**：
- `ruoyi-system/src/main/java/com/ruoyi/system/domain/SysUser.java` - 用户实体类
- `ruoyi-system/src/main/java/com/ruoyi/system/mapper/SysUserMapper.java` - 用户 Mapper
- `ruoyi-system/src/main/java/com/ruoyi/system/service/impl/SysUserServiceImpl.java` - 用户服务实现
- `ruoyi-admin/src/main/java/com/ruoyi/web/controller/system/SysUserController.java` - 用户控制器

### 前端关键文件

**核心配置**：
- `ruoyi-ui/src/main.ts` - Vue 应用入口
- `ruoyi-ui/vite.config.ts` - Vite 构建配置（代理/插件）
- `ruoyi-ui/.env.development` - 开发环境变量（API地址）
- `ruoyi-ui/tsconfig.json` - TypeScript 配置
- `ruoyi-ui/package.json` - 依赖管理

**路由与权限**：
- `ruoyi-ui/src/router/index.ts` - 路由主文件（路由守卫/动态路由）
- `ruoyi-ui/src/permission.ts` - 全局权限控制
- `ruoyi-ui/src/store/modules/permission.ts` - 权限状态管理

**工具类参考**：
- `ruoyi-ui/src/utils/request.ts` - Axios 封装（请求/响应拦截器）
- `ruoyi-ui/src/utils/auth.ts` - Token 管理工具
- `ruoyi-ui/src/utils/validate.ts` - 表单验证规则

**API 定义示例**：
- `ruoyi-ui/src/api/login.ts` - 登录/登出接口
- `ruoyi-ui/src/api/system/user.ts` - 用户管理接口
- `ruoyi-ui/src/api/system/menu.ts` - 菜单管理接口

**页面组件示例**：
- `ruoyi-ui/src/views/login.vue` - 登录页面
- `ruoyi-ui/src/views/index.vue` - 首页 Dashboard
- `ruoyi-ui/src/views/system/user/index.vue` - 用户管理列表页
- `ruoyi-ui/src/views/system/user/profile.vue` - 用户个人资料

**全局组件示例**：
- `ruoyi-ui/src/components/DictTag/index.vue` - 字典标签组件
- `ruoyi-ui/src/layout/index.vue` - 主布局容器

### 代码生成器

- `ruoyi-generator` - 代码生成模块（一键生成 Controller/Service/Mapper/Vue页面）
- 访问：`http://localhost:8080/tool/gen` 可在线使用代码生成器

## 工作流程与检查清单

### 代码定位工作流

当需要查找或修改某个功能时，按以下流程操作：

1. **确定功能模块** → 判断属于哪个业务模块（system/monitor/自定义模块）
2. **后端代码定位**：
   - [ ] 查找 Controller → `ruoyi-admin/.../controller/{模块名}/{功能}Controller.java`
   - [ ] 查找 Service → 对应模块 `.../service/{功能}Service.java`
   - [ ] 查找 Mapper → 对应模块 `.../mapper/{功能}Mapper.java`
   - [ ] 查找 Entity → 对应模块 `.../domain/{功能}.java`
3. **前端代码定位**：
   - [ ] 查找 API → `src/api/{模块名}/{功能}.ts`
   - [ ] 查找页面 → `src/views/{模块名}/{功能}/index.vue`
   - [ ] 查找路由 → `src/router/index.ts` 或后端动态路由

### 新功能开发检查清单

**后端开发**：
- [ ] 是否在正确的 Maven 模块中创建代码
- [ ] 是否遵循标准三层结构（Controller → Service → Mapper）
- [ ] 是否继承了 `BaseEntity` 基类（需要创建/修改时间等字段）
- [ ] Controller 是否添加了权限注解（`@PreAuthorize`）
- [ ] 是否使用了统一响应封装（`R<T>`）
- [ ] 是否添加了操作日志注解（`@Log`）
- [ ] Mapper 方法是否使用了 MyBatis-Plus（避免写 XML）
- [ ] 是否处理了异常情况（`try-catch` 或声明式异常）
- [ ] 是否更新了 `pom.xml` 依赖关系（新模块）

**前端开发**：
- [ ] 是否将 API 定义与页面组件分离
- [ ] API 文件路径是否与后端 Controller 对应
- [ ] 页面路径是否与路由配置对应
- [ ] 是否使用了 TypeScript 类型定义（避免 `any`）
- [ ] 是否使用了全局组件（表格/表单/上传等）
- [ ] 是否添加了权限指令（`v-hasPermi`）
- [ ] 是否处理了 API 错误（拦截器已统一处理）
- [ ] 是否适配了移动端（响应式布局）
- [ ] 是否进行了代码格式化（ESLint/Prettier）

**前后端联调**：
- [ ] 接口文档是否同步更新（Swagger）
- [ ] 请求参数和返回格式是否匹配
- [ ] 权限控制是否前后端一致
- [ ] 是否进行了接口测试（Postman/Apifox）
- [ ] 是否测试了异常情况（参数错误/权限不足）

### 问题排查检查清单

**接口调用失败**：
- [ ] 检查网络请求是否发出（浏览器 Network 面板）
- [ ] 检查 API 地址是否正确（环境变量配置）
- [ ] 检查后端接口是否正常运行（日志/Swagger）
- [ ] 检查请求参数格式是否匹配
- [ ] 检查权限配置是否正确（Token/角色/权限）
- [ ] 检查 CORS 跨域配置（开发环境代理）

**页面显示异常**：
- [ ] 检查路由配置是否正确
- [ ] 检查组件导入路径是否正确
- [ ] 检查数据格式是否符合组件预期
- [ ] 检查浏览器控制台错误信息
- [ ] 检查 CSS 样式是否被覆盖

**数据库操作失败**：
- [ ] 检查数据库连接配置（application.yml）
- [ ] 检查 SQL 语句是否正确（MyBatis 日志）
- [ ] 检查实体类字段是否与数据库表对应
- [ ] 检查是否有事务冲突
- [ ] 检查数据权限配置（`@DataScope`）

### 代码审查检查清单

**代码质量**：
- [ ] 是否遵循了项目命名规范
- [ ] 是否添加了必要的注释（类/方法/复杂逻辑）
- [ ] 是否消除了魔法值（使用常量代替）
- [ ] 是否移除了无用代码和注释
- [ ] 是否进行了代码格式化

**性能优化**：
- [ ] SQL 查询是否添加了索引
- [ ] 是否避免了 N+1 查询
- [ ] 是否使用了分页查询（大数据量）
- [ ] 是否添加了缓存（Redis）
- [ ] 前端是否使用了懒加载/虚拟滚动

**安全性**：
- [ ] 是否进行了 SQL 注入防护（MyBatis-Plus 自动防护）
- [ ] 是否进行了 XSS 防护（前端输入过滤）
- [ ] 是否进行了 CSRF 防护（Spring Security 配置）
- [ ] 敏感信息是否加密存储
- [ ] 是否对用户输入进行了校验

### 快速参考命令

**Maven 相关**：
```bash
# 清理并编译项目
mvn clean install

# 跳过测试编译
mvn clean install -DskipTests

# 运行 Spring Boot 应用
mvn spring-boot:run
```

**npm/pnpm 相关**：
```bash
# 安装依赖
npm install  或  pnpm install

# 启动开发服务器
npm run dev  或  pnpm dev

# 构建生产版本
npm run build  或  pnpm build

# 代码格式化
npm run lint  或  pnpm lint
```

**Git 相关**：
```bash
# 查看当前分支和状态
git status

# 创建新功能分支
git checkout -b feature/module-name

# 提交代码
git add .
git commit -m "feat: 添加xxx功能"
git push origin feature/module-name
```

## 使用指南

### 如何使用此 SKILL

当你遇到以下场景时，应该参考本 SKILL 文档：

1. **不知道某个功能的代码在哪里** → 查看「核心规范」中的代码查找决策树
2. **需要添加新的业务模块** → 按照「规范3：新业务模块添加标准流程」操作
3. **修改配置但不知道文件位置** → 查看「规范4：关键配置文件速查表」
4. **不确定代码应该放在哪个模块** → 查看「模块职责矩阵」
5. **接口调用失败或页面异常** → 使用「问题排查检查清单」
6. **代码审查前** → 使用「代码审查检查清单」自查

### SKILL 设计原则

本 SKILL 遵循以下设计原则：

- **职责分离**：后端 Maven 模块、前端目录结构都遵循单一职责原则
- **分层解耦**：API 定义与页面组件分离，业务逻辑与数据访问分离
- **约定优于配置**：统一的命名规范、目录结构、代码组织方式
- **前后端对应**：前端 API 目录与后端 Controller 路径保持一致
- **可维护性优先**：清晰的模块边界、完善的文档、规范的代码风格

### 常见误区

1. **误区：工具类可以调用 Service**  
   ✓ 正确：工具类应该是无状态的纯函数，不依赖任何业务逻辑

2. **误区：前端页面可以直接写 axios 请求**  
   ✓ 正确：必须将 API 定义抽取到 `src/api` 目录，保持组件纯粹

3. **误区：所有状态都要放到 Pinia Store**  
   ✓ 正确：只有跨组件共享的状态才需要 Store，页面内部状态用 ref/reactive

4. **误区：Controller 可以直接调用 Mapper**  
   ✓ 正确：Controller → Service → Mapper，不能跳过 Service 层

5. **误区：前端权限控制就够了，后端不需要**  
   ✓ 正确：前端权限只是 UI 隐藏，后端必须有权限校验保护 API

### 扩展资源

- **官方文档**：[RuoYi-Vue-Plus 文档](https://plus-doc.dromara.org/)
- **Gitee 仓库**：[RuoYi-Vue-Plus](https://gitee.com/dromara/RuoYi-Vue-Plus)
- **技术栈文档**：
  - Spring Boot: https://spring.io/projects/spring-boot
  - MyBatis-Plus: https://baomidou.com/
  - Vue3: https://vuejs.org/
  - Element-Plus: https://element-plus.org/
  - Vite: https://vitejs.dev/
  - Pinia: https://pinia.vuejs.org/

---

**版本信息**：适用于 RuoYi-Vue-Plus 5.x 版本  
**最后更新**：2026-01-26  
**维护者**：请根据实际项目情况调整本文档内容