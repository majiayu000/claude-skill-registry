# JeecgBoot UniApp3 项目架构参考

## 项目根目录

> **`<uniapp_project_root>`** 为动态路径，由用户在 Step 0 确认，如 `D:\projects\jeecgboot-uniapp3`。

```
<uniapp_project_root>/
├── env/                    # 环境变量配置 (.env, .env.development, .env.production)
├── src/                    # 源码根目录
├── pages.config.ts         # uni-pages 全局配置（globalStyle、easycom、tabBar）
├── manifest.config.ts      # 应用清单配置
├── vite.config.ts          # Vite 构建配置
├── package.json            # 依赖：vue3.4, pinia, wot-design-uni, z-paging, dayjs
└── tsconfig.json           # TypeScript 配置
```

## src/ 目录结构

```
src/
├── App.vue                 # 应用入口
├── main.ts                 # 主入口，初始化插件
├── pages.json              # 页面路由配置（由 <route> 标签自动生成 + 手动配置）
├── uni.scss                # 全局 SCSS 变量
│
├── pages/                  # 主包页面（tabBar 页面在此）
│   ├── components/         # tabBar 页面组件
│   │   ├── index/          # 首页
│   │   ├── message/        # 消息
│   │   ├── portal/         # 门户
│   │   └── user/           # 个人
│   ├── home/               # 主页
│   ├── login/              # 登录页
│   └── workHome/           # 工作台
│
├── pages-home/             # 分包：业务功能页面（推荐新增 CRUD 页面放这里）
│   ├── about/
│   ├── annotation/
│   ├── demo/               # 组件演示
│   └── ...
│
├── pages-sub/              # 分包：Online 表单、VPN、WebLink
│   ├── online/             # Online 动态表单渲染
│   └── ...
│
├── pages-super/            # 分包：高级业务模块
│   ├── applyform/          # 申请单（请假、公文、出差）
│   ├── attendance/         # 考勤
│   ├── collaboration/      # 协作
│   ├── desform/            # 表单设计器
│   ├── flow/               # 流程审批
│   ├── knowledge/          # 知识库
│   ├── mail/               # 邮件
│   ├── meeting/            # 会议
│   ├── news/               # 新闻
│   ├── schedule/           # 日程
│   ├── supervise/          # 督办
│   └── ...
│
├── pages-user/             # 分包：个人中心
├── pages-work/             # 分包：工作相关
├── pages-message/          # 分包：消息
├── pages-appPortal/        # 分包：APP 门户
│
├── components/             # 全局共享组件
│   ├── PageLayout/         # 页面布局容器（每个页面必用）
│   ├── DateTime/           # 日期时间选择器
│   ├── CategorySelect/     # 分类树选择
│   ├── TreeSelect/         # 自定义树选择
│   ├── Popup/              # 弹窗表单选择
│   ├── PopupDict/          # 弹窗字典选择
│   ├── SelectUser/         # 用户选择
│   ├── SelectDept/         # 部门选择
│   ├── SelectMulti/        # 多选
│   ├── Grid/               # 九宫格
│   ├── ImgPreview/         # 图片预览
│   ├── ProgressMap/        # 流程进度
│   └── online/             # Online 组件集合
│       └── view/           # online 表单控件
│           ├── online-select.vue
│           ├── online-radio.vue
│           ├── online-checkbox.vue
│           ├── online-multi.vue
│           ├── online-date.vue
│           ├── online-time.vue
│           ├── online-image.vue
│           ├── online-file.vue
│           ├── online-file-custom.vue
│           ├── online-pca.vue
│           └── online-popup-link-record.vue
│
├── hooks/                  # 组合式函数
│   ├── usePageList.ts      # 分页列表 hook（核心！CRUD 列表页必用）
│   ├── useRequest.ts       # 通用请求 hook
│   ├── useUpload.ts        # 上传 hook
│   ├── useGeoPosition.ts   # 地理定位
│   └── useGeoSign.ts       # 地理签到
│
├── utils/                  # 工具函数
│   ├── http.ts             # HTTP 请求封装（核心！）
│   ├── is.ts               # 类型判断工具
│   ├── platform.ts         # 平台判断（isH5, isMp, isApp）
│   └── signMd5Utils.ts     # API 签名
│
├── service/                # 全局 API 服务
│   └── api.ts              # 公共 API（如 duplicateCheck 唯一性校验）
│
├── store/                  # Pinia 状态管理
│   ├── index.ts            # Store 导出
│   ├── user.ts             # 用户信息 store
│   └── page-params.ts      # 页面参数持久化 store
│
├── router/                 # 路由配置
│   └── index.ts            # uni-mini-router 路由（路由名 = 路径最后一级）
│
├── plugin/                 # 插件
│   └── uni-mini-router/    # 路由插件
│
├── layouts/                # 布局
│   └── default.vue         # 默认布局
│
├── interceptors/           # 请求拦截器
│   └── request.ts          # 请求拦截（添加 token 等）
│
├── style/                  # 全局样式
├── static/                 # 静态资源
└── types/                  # 类型定义
```

## 页面注册机制

### 方式 1: `<route>` 标签（推荐）

在 `.vue` 文件顶部使用 `<route>` 标签，由 `@uni-helper/vite-plugin-uni-pages` 插件自动解析并注入 `pages.json`：

```vue
<route lang="json5" type="page">
{
  layout: 'default',
  style: {
    navigationBarTitleText: '页面标题',
    navigationStyle: 'custom',
  },
}
</route>
```

### 方式 2: 手动配置 pages.json

对于分包页面，需要在 `src/pages.json` 的 `subPackages` 数组中注册。

**重要：** 项目使用 `uni-mini-router`，路由名称自动取路径最后一级（如 `pages-home/demo/demo` → 路由名 `demo`）。因此同一项目内不能有同名页面文件。

### 分包选择建议

| 场景 | 推荐分包 |
|------|----------|
| 通用业务 CRUD | `pages-home/` |
| Online 动态表单 | `pages-sub/` |
| 高级业务模块（流程、协作等） | `pages-super/` |
| 个人中心相关 | `pages-user/` |

## 核心依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| vue | 3.4.21 | 框架 |
| pinia | 2.0.36 | 状态管理 |
| wot-design-uni | ^1.9.1 | UI 组件库（wd-* 前缀） |
| z-paging | ^2.8.6 | 分页加载组件 |
| dayjs | 1.11.10 | 日期处理 |
| uni-mini-router | 内置 | 路由管理 |

## usePageList Hook 详解

`src/hooks/usePageList.ts` 是列表页的核心 hook，签名：

```typescript
export default function usePageList<T = string>(listUrl: string, params?: object)
```

- `listUrl`: 后端分页列表接口路径（如 `/test/demo/list`）
- `params`: 额外查询参数（可选）

返回值：

| 属性 | 类型 | 说明 |
|------|------|------|
| toast | Toast | wot-design-uni 的 toast 实例 |
| router | Router | uni-mini-router 路由实例 |
| paging | Ref | z-paging 组件的 ref 引用 |
| paramsStore | Store | 页面参数 store |
| dataList | Ref<any[]> | 列表数据 |
| queryParams | Function | 获取查询参数（含 pageNo, pageSize, order, column） |
| queryList | Function(pageNo, pageSize) | 执行查询的函数（由 z-paging 自动调用） |
| extraParams | Ref<object> | 额外搜索参数（可动态修改） |

默认排序：`order: 'desc', column: 'createTime'`

## HTTP 工具详解

`src/utils/http.ts` 封装了 `uni.request`，自动处理：
- Token 注入（`X-Access-Token`）
- 租户 ID（`X-Tenant-Id`）
- API 签名（`X-Sign`, `V-Sign`）
- GET 请求防缓存（`_t` 时间戳）
- 401 自动跳转登录页

使用方式：
```typescript
import { http } from '@/utils/http'

// GET
http.get('/api/path', { param1: 'value' })

// POST
http.post('/api/path', { field1: 'value' })

// DELETE
http.delete('/api/path?id=xxx', { id: 'xxx' })

// PUT
http.put('/api/path', { field1: 'value' })
```

返回值是 Promise，resolve 的数据结构：
```typescript
interface IResData<T> {
  success: boolean
  message: string
  result: T       // 列表接口时为 { records: T[], total: number }
  code: number
}
```
