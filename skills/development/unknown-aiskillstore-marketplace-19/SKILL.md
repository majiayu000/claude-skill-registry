---
name: zentao-api
description: 调用禅道（ZenTao）RESTful API v2.0 完成用户请求，覆盖项目集、产品、项目、执行、需求（Story/Epic/Requirement）、Bug、任务、测试用例、测试单、产品计划、版本、发布、反馈、工单、应用、用户、文件等 20 个模块的增删改查及状态流转操作。当用户提到禅道、zentao、查询项目进展、获取 Bug 列表、更新需求状态、创建任务等项目管理相关操作时使用本技能。
metadata:
  author: Sun Hao <sunhao@chandao.com>
  repository: https://github.com/easysoft/zentao-skills.git
  keywords: [zentao, 禅道, api, project-management]
  version: 1.0.4
---

# 禅道 API v2.0

## 配置

优先级从高到低：

| 变量 | 说明 |
|------|------|
| `ZENTAO_URL` | 服务器地址，如 `http://zentao.example.com` |
| `ZENTAO_TOKEN` | 直接指定 token，跳过登录和缓存（最高优先级），仍需提供服务器地址 |
| `ZENTAO_ACCOUNT` | 登录账号，有 token 时可选，但提供可更好回答与当前用户相关的问题 |
| `ZENTAO_PASSWORD` | 登录密码，有 token 时无需提供 |

**首次登录后 `ZENTAO_URL`、`ZENTAO_TOKEN`、`ZENTAO_ACCOUNT` 写入 `~/.zentao-token.json`，后续无需重复设置**。

若必要变量缺失，提示用户并给出 `export` 命令。用户直接提供服务器、账号和密码时直接使用，同时告知尽量设为环境变量。

## 认证流程

所有业务 API 需在 Header 携带 `token`。运行 `scripts/get-token.sh` 自动获取：

```bash
eval "$(bash scripts/get-token.sh)"
# 执行后可直接使用 $ZENTAO_URL、$ZENTAO_TOKEN、$ZENTAO_ACCOUNT
```

脚本依赖：`curl`、`node`

后续所有请求 Header 携带：`token: $ZENTAO_TOKEN`

## 执行 API 调用的步骤

1. 运行 `eval "$(bash scripts/get-token.sh)"` 获取凭证（自动处理缓存；仍缺失时提示用户）
2. 根据用户意图选择正确的 API 端点（参见 [api-reference.md](api-reference.md)）
3. 若为 PUT 编辑操作且用户未提供全部必填字段，先调用对应 GET 详情接口取回当前数据，再将用户指定的字段覆盖进去
4. 构造请求（方法、URL、Header、Body）并向用户确认写操作内容
5. 执行请求，解析响应
6. 以清晰易读的格式向用户展示结果

## 模块总览

API 基础路径：`$ZENTAO_URL/api.php/v2`

| 模块 | 资源路径 | 支持操作 |
|------|---------|---------|
| 项目集 Program | `/programs` | CRUD + 关联产品/项目列表 |
| 产品 Product | `/products` | CRUD + 关联需求/Bug/用例/计划/发布/反馈/工单/测试单/应用 |
| 项目 Project | `/projects` | CUD + 关联执行/需求/Bug/用例/版本/测试单 |
| 执行 Execution | `/executions` | CRUD + 关联需求/任务/Bug/用例/版本/测试单 |
| 需求 Story | `/stories` | CRUD + change/close/activate |
| 业务需求 Epic | `/epics` | CRUD + change/close/activate |
| 用户需求 Requirement | `/requirements` | CRUD + change/close/activate |
| Bug | `/bugs` | CRUD + resolve/close/activate |
| 任务 Task | `/tasks` | CRUD + start/finish/close/activate |
| 测试用例 Testcase | `/testcases` | CRUD |
| 产品计划 Productplan | `/productplans` | CUD + 按产品查列表 |
| 版本 Build | `/builds` | CUD + 按项目/执行查列表 |
| 发布 Release | `/releases` | CUD + 按产品查列表 |
| 测试单 Testtask | `/testtasks` | CUD + 按产品/项目/执行查列表 |
| 反馈 Feedback | `/feedbacks` | CRUD + close/activate |
| 工单 Ticket | `/tickets` | CRUD + close/activate |
| 应用 System | `/systems` | CU + 按产品查列表 |
| 用户 User | `/users` | CRUD |
| 文件 File | `/files` | 编辑名称 + 删除 |

> CRUD = 创建(POST) + 读取(GET) + 更新(PUT) + 删除(DELETE)；CUD = 无独立全局列表接口

## 分页与筛选

所有列表接口支持统一的查询参数：

| 参数 | 说明 |
|------|------|
| `browseType` 或 `status` | 筛选状态，如 `all`, `doing`, `unclosed`, `undone` 等（不同模块参数名和可选值不同，详见 [api-reference.md](api-reference.md)） |
| `orderBy` | 排序，格式 `字段_asc` 或 `字段_desc`，如 `id_desc`, `title_asc` |
| `recPerPage` | 每页数量，最大 1000 |
| `pageID` | 页码，从 1 开始 |

**筛选参数名不一致**：Program 列表、Execution 全局列表、Task 列表用 `status`，其余用 `browseType`。

## 常用操作示例

### 获取进行中的项目及其执行

```bash
curl -s "$ZENTAO_URL/api.php/v2/projects?browseType=doing&recPerPage=100" -H "token: $ZENTAO_TOKEN"
curl -s "$ZENTAO_URL/api.php/v2/projects/{projectID}/executions?browseType=doing" -H "token: $ZENTAO_TOKEN"
```

### 创建需求（必填：productID, title）

```bash
curl -s -X POST "$ZENTAO_URL/api.php/v2/stories" \
  -H "token: $ZENTAO_TOKEN" -H "Content-Type: application/json" \
  -d '{"productID": 1, "title": "需求标题", "grade": 1, "pri": 3, "assignedTo": "admin", "spec": "需求描述"}'
```

### 创建业务需求（Epic）

```bash
curl -s -X POST "$ZENTAO_URL/api.php/v2/epics" \
  -H "token: $ZENTAO_TOKEN" -H "Content-Type: application/json" \
  -d '{"productID": 1, "title": "业务需求标题", "grade": 1, "pri": 3, "reviewer": ["admin"]}'
```

### 创建用户需求（Requirement）

```bash
curl -s -X POST "$ZENTAO_URL/api.php/v2/requirements" \
  -H "token: $ZENTAO_TOKEN" -H "Content-Type: application/json" \
  -d '{"productID": 1, "title": "用户需求标题", "parent": 1001, "grade": 1, "pri": 3, "reviewer": ["admin"]}'
```

### 创建 Bug（必填：productID, title, openedBuild）

```bash
curl -s -X POST "$ZENTAO_URL/api.php/v2/bugs" \
  -H "token: $ZENTAO_TOKEN" -H "Content-Type: application/json" \
  -d '{"productID": 1, "title": "Bug标题", "openedBuild": ["trunk"], "severity": 2, "type": "codeerror"}'
```

### 解决 Bug（必填：resolution）

```bash
curl -s -X PUT "$ZENTAO_URL/api.php/v2/bugs/{bugID}/resolve" \
  -H "token: $ZENTAO_TOKEN" -H "Content-Type: application/json" \
  -d '{"resolution": "fixed"}'
```

### 创建任务（必填：name, executionID）

```bash
curl -s -X POST "$ZENTAO_URL/api.php/v2/tasks" \
  -H "token: $ZENTAO_TOKEN" -H "Content-Type: application/json" \
  -d '{"executionID": 1, "name": "任务名", "type": "devel", "assignedTo": "admin", "estimate": 4}'
```

### 完成任务（必填：currentConsumed, realStarted, finishedDate）

```bash
curl -s -X PUT "$ZENTAO_URL/api.php/v2/tasks/{taskID}/finish" \
  -H "token: $ZENTAO_TOKEN" -H "Content-Type: application/json" \
  -d '{"currentConsumed": 4, "realStarted": "2026-03-25", "finishedDate": "2026-03-25"}'
```

### 关闭需求（必填：closedReason）

```bash
curl -s -X PUT "$ZENTAO_URL/api.php/v2/stories/{storyID}/close" \
  -H "token: $ZENTAO_TOKEN" -H "Content-Type: application/json" \
  -d '{"closedReason": "done"}'
```

## 常用枚举值速查

| 字段 | 可选值 |
|------|-------|
| 项目模式 `model` | `scrum`, `waterfall`, `kanban`, `agileplus`, `waterfallplus` |
| Bug 类型 `type` | `codeerror`, `config`, `install`, `security`, `performance`, `standard`, `automation`, `designdefect`, `others` |
| Bug 解决方案 `resolution` | `fixed`, `notrepro`, `bydesign`, `duplicate`, `external`, `postponed`, `willnotfix`, `tostory` |
| 需求关闭原因 `closedReason` | `done`, `subdivided`, `duplicate`, `postponed`, `willnotdo`, `cancel`, `bydesign` |
| 需求来源 `source` | `customer`, `user`, `po`, `market`, `service`, `operation`, `support`, `competitor`, `partner`, `dev`, `tester`, `bug`, `forum`, `other` |
| 需求类别 `category` | `feature`, `interface`, `performance`, `safe`, `experience`, `improve`, `other` |
| 用例类型 `type` | `unit`, `interface`, `feature`, `install`, `config`, `performance`, `security`, `other` |
| 测试单类型 `type` | `integrate`, `system`, `acceptance`, `performance`, `safety` |
| 发布状态 `status` | `wait`, `normal`, `fail`, `terminate` |
| 反馈关闭原因 `closedReason` | `commented`, `repeat`, `refuse` |
| 工单类型 `type` | `code`, `data`, `stuck`, `security`, `affair` |
| 产品类型 `type` | `normal`, `branch`, `platform` |
| 产品访问控制 `acl` | `open`, `private` |
| 执行类型 `lifetime` | `short`, `long`, `ops` |

## 意图识别规则

| 用户意图关键词 | 对应操作 |
|--------------|---------|
| 进行中的执行/迭代/Sprint | GET /projects?browseType=doing → GET /projects/{id}/executions |
| 获取所有产品/项目/项目集 | GET /products, /projects, /programs |
| 某产品/项目/执行的 Bug | GET /products/{id}/bugs, /projects/{id}/bugs, /executions/{id}/bugs |
| 创建/新增 Bug | POST /bugs（必填：productID, title, openedBuild） |
| 更新/修改 Bug | PUT /bugs/{id} |
| 解决 Bug | PUT /bugs/{id}/resolve（必填：resolution） |
| 关闭 Bug | PUT /bugs/{id}/close |
| 激活 Bug | PUT /bugs/{id}/activate |
| 创建需求 | POST /stories（必填：productID, title） |
| 关闭/激活/变更需求 | PUT /stories/{id}/close, /activate, /change |
| 业务需求 | /epics（同 stories 结构） |
| 用户需求 | /requirements（同 stories 结构） |
| 创建任务 | POST /tasks（必填：name, executionID） |
| 启动任务 | PUT /tasks/{id}/start（必填：realStarted） |
| 完成任务 | PUT /tasks/{id}/finish（必填：currentConsumed, realStarted, finishedDate） |
| 关闭任务 | PUT /tasks/{id}/close |
| 测试用例 | /testcases（CRUD） |
| 测试单 | /testtasks（CUD + 按产品/项目/执行查列表） |
| 产品计划 | /productplans（CUD + 按产品查列表） |
| 版本/Build | /builds（CUD + 按项目/执行查列表） |
| 发布 | /releases（CUD + 按产品查列表） |
| 反馈 | /feedbacks（CRUD + close/activate） |
| 工单 | /tickets（CRUD + close/activate） |
| 应用/系统 | /systems（CU + 按产品查列表） |
| 获取用户列表 | GET /users |

## 注意事项

- URL 中的 `{id}` 需替换为实际 ID；不知道 ID 时先调列表接口获取
- **创建 Epic / Requirement / Story 时，建议始终显式传 `grade`，不要依赖接口默认值。** 已有用户反馈某些禅道实例在未传 `grade` 时会把需求层级写成 `0`，导致界面中 BR / UR / SR 标签显示异常。
- **PUT 编辑接口**：先 GET 详情获取当前完整数据，再将用户修改的字段覆盖进去一并提交
- **状态流转操作** (resolve/close/activate/start/finish/change) 通常有独立的必填字段，不需要先 GET 详情
- 写操作前向用户确认，用户明确要求不确认则直接执行
- 401 响应表示 token 已失效，执行 `rm ~/.zentao-token.json` 清除缓存后重新运行
- **字段名不一致注意**：POST builds 用 `executionID`，PUT builds 用 `execution`；PUT testcases 的模块字段为 `moudule`（规范中的拼写）

## 完整 API 参考

详细的端点列表、必填/可选字段、枚举值和查询参数见 [api-reference.md](api-reference.md)。

## 备用资源

- 禅道 API 2.0 官方文档：https://www.zentao.net/book/api/2309.html
- 1.0 API 文档（备用）：https://www.zentao.net/book/api/1397.html
