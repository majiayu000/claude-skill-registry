---
name: jeecg-system
description: JeecgBoot 系统主数据查询与管理。Use when user asks to query/create/manage system master data, or says "查询角色", "查询用户", "查询部门", "查询字典", "创建字典", "创建角色", "查岗位", "查职务", "查租户", "查数据源", "查定时任务", "系统主数据", "query roles", "query users", "query depts", "create dict", "create role", "master data". Also triggers when other skills (desform, bpmn, codegen) need to look up or create roles, users, departments, dictionaries, or positions as dependencies — follows "先查后建" (query-first-create-later) principle.
---

# JeecgBoot 系统主数据查询与管理

查询和管理 JeecgBoot 系统中的角色、用户、部门、字典等主数据。遵循"先查后建"原则：优先使用系统已有数据，没有才创建。

## 前置条件

用户必须提供以下信息（或由 AI 引导确认）：

1. **API 地址**：JeecgBoot 后端地址（如 `https://boot3.jeecg.com/jeecgboot`）
2. **X-Access-Token**：JWT 登录令牌（从浏览器 F12 获取）

如果用户未提供，提示：
> 请提供 JeecgBoot 后端地址和 X-Access-Token（从浏览器 F12 → Network → 任意请求的 Request Headers 中复制）。

## 核心原则：先查后建

在任何 skill（流程设计、表单设计、代码生成等）需要使用主数据时，**必须先查询系统已有数据，确认不存在后才创建新数据**。

| 数据类型 | 查询函数 | 创建函数 | 一站式函数 |
|---------|---------|---------|-----------|
| 角色 | `query_roles()` / `find_role()` | `create_role()` | `find_or_create_role()` |
| 角色绑定用户 | — | `add_users_to_role(role_id, user_ids)` | — |
| 审批角色 | `query_approval_roles()` / `find_approval_role()` | `create_approval_role_group()` + `create_approval_role()` | `find_or_create_approval_role()` |
| 审批角色绑定用户 | — | `add_users_to_approval_role(role_id, user_ids)` | — |
| 用户 | `query_users()` / `find_user()` | — | — |
| 部门 | `query_depts()` / `find_dept()` | — | — |
| 岗位 | `query_dept_positions()` | — | — |
| 字典（普通） | `query_dict()` / `search_dict()` / `find_dict()` | `create_dict()` | `find_or_create_dict()` |
| 字典（SQL表） | `query_sql_table_dict()` | — | — |

## 使用方式

### 脚本位置

- `scripts/system_creator.py` — **通用命令行脚本**（推荐，无需生成临时 .py）
- `scripts/system_utils.py` — 工具库（供其他 skill 脚本 import）

### 方式一：通用脚本 + 命令行（推荐）

**单项查询（直接命令行，无需配置文件）：**

```bash
SCRIPT="<skill目录>/jeecg-system/scripts/system_creator.py"
API="<api_base>"
TOKEN="eyJ..."

# 查询角色列表
python "$SCRIPT" --api-base $API --token $TOKEN --action query-roles
python "$SCRIPT" --api-base $API --token $TOKEN --action query-roles --keyword 经理

# 查询用户列表
python "$SCRIPT" --api-base $API --token $TOKEN --action query-users --keyword 张

# 查询部门树
python "$SCRIPT" --api-base $API --token $TOKEN --action query-depts
python "$SCRIPT" --api-base $API --token $TOKEN --action query-depts --keyword 研发

# 查询字典列表
python "$SCRIPT" --api-base $API --token $TOKEN --action query-dicts --keyword 请假

# 查询字典项
python "$SCRIPT" --api-base $API --token $TOKEN --action query-dict --code sex

# 查询职务列表
python "$SCRIPT" --api-base $API --token $TOKEN --action query-positions

# 查询部门+岗位树
python "$SCRIPT" --api-base $API --token $TOKEN --action query-dept-positions

# 查询审批角色
python "$SCRIPT" --api-base $API --token $TOKEN --action query-approval-roles

# 查询租户列表
python "$SCRIPT" --api-base $API --token $TOKEN --action query-tenants

# 查询数据源
python "$SCRIPT" --api-base $API --token $TOKEN --action query-datasources

# 查询定时任务
python "$SCRIPT" --api-base $API --token $TOKEN --action query-quartz-jobs

# 查询分类字典
python "$SCRIPT" --api-base $API --token $TOKEN --action query-categories --code B01

# 输出结果到 JSON 文件
python "$SCRIPT" --api-base $API --token $TOKEN --action query-roles --output roles.json
```

**批量查找/创建（JSON 配置文件）：**

```bash
# 1. Write 工具写入 JSON 配置文件
# 2. 执行脚本
python "$SCRIPT" --api-base $API --token $TOKEN --config master_data.json
# 3. 删除临时 JSON 文件
```

**JSON 配置格式：**

```json
{
  "roles": [
    {"roleName": "部门经理", "roleCode": "dept_manager"},
    {"roleName": "HR专员", "roleCode": "hr"}
  ],
  "dicts": [
    {
      "dictCode": "leave_type",
      "dictName": "请假类型",
      "items": [
        {"value": "1", "text": "事假"},
        {"value": "2", "text": "病假"},
        {"value": "3", "text": "年假"}
      ]
    }
  ],
  "users": [
    {"keyword": "admin"},
    {"username": "zhangsan"}
  ],
  "depts": [
    {"keyword": "研发部"},
    {"departName": "人力资源部"}
  ],
  "positions": [
    {"keyword": "总经理"}
  ]
}
```

脚本自动完成：
- 角色/字典：先查后建（已有则跳过，没有则创建）
- 用户/部门/职务：只查不建（返回查询结果）
- 汇总输出所有查找/创建结果
- 可通过 `--output result.json` 保存结果

### 方式二：在临时脚本中 import 工具库

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'jeecg-system', 'scripts'))
# 或直接用绝对路径: sys.path.insert(0, r'<skill目录>/jeecg-system/scripts')
from system_utils import *

init_api('<api_base>', '<token>')

# ====== 角色 ======
# 查询所有角色
roles = query_roles()
# 按名称模糊查询
roles = query_roles(keyword='经理')
# 查找单个角色
role = find_role('manager')  # 按编码或名称
# 查找或创建（推荐）
role_code = find_or_create_role('项目经理', 'project_manager')

# ====== 用户 ======
# 查询用户列表
users = query_users(keyword='张')
users = query_users(username='admin')
# 查找单个用户
user = find_user('admin')  # 按用户名或姓名

# ====== 部门 ======
# 查询部门树
depts = query_depts()
depts = query_depts(keyword='研发')
# 查找单个部门
dept = find_dept('研发部')
# 查询部门+岗位树
positions = query_dept_positions()

# ====== 字典 ======
# 查询字典项（普通字典，通过 /sys/api/getDictItems）
items = query_dict('sex')  # → [{'value': '1', 'text': '男'}, ...]
# 查询 SQL 表字典项（通过 /sys/dict/getDictItems/{dictCode}，需签名）
items_sql = query_sql_table_dict("sys_user,realname,id,username!='admin' order by create_time")
# 搜索字典（按名称/编码模糊匹配）
dicts = search_dict('请假')
# 查找字典（含字典项）
d = find_dict('sex')  # → {'dictCode': 'sex', 'dictName': '性别', 'items': [...]}
# 查找或创建字典（推荐）
dict_code = find_or_create_dict('leave_type', '请假类型', [
    {'value': '1', 'text': '事假'},
    {'value': '2', 'text': '病假'},
    {'value': '3', 'text': '年假'},
])

# ====== 系统角色绑定用户 ======
# 创建角色并自动绑定 admin（默认行为）
role_code = find_or_create_role('财务审核', 'finance_audit')
# 不绑定 admin
role_code = find_or_create_role('只读角色', 'readonly', add_admin=False)
# 手动绑定用户到角色
role = find_role('finance_audit')
add_users_to_role(role['id'], ['e9ca23d68d884d4ebb19d07889727dae'])

# ====== 审批角色 ======
# 一站式：查找或创建审批角色（自动创建分组 + 角色 + 绑定 admin）
role_id = find_or_create_approval_role('财务审批专员', group_name='财务分组')
# 分步创建
group_id = create_approval_role_group('HR分组')
role_id  = create_approval_role('HR审批专员', group_id, add_admin=True)
# 查询审批角色
res  = query_approval_roles('财务')   # {'roles': [...], 'persons': [...]}
role = find_approval_role('财务审批') # 单个或 None

# ====== 便捷打印 ======
print_roles()           # 打印角色列表
print_users(keyword='张')  # 打印用户列表
print_depts()           # 打印部门树
print_dict('sex')       # 打印字典项
print_dicts('请假')     # 搜索并打印字典列表
```

### 在其他 skill 脚本中使用

其他 skill 的脚本可以直接导入 `system_utils`（需先加载 jeecg-system skill，从 `Base directory for this skill: <skill_base_dir>` 取得路径）：

```python
import sys
sys.path.insert(0, r'<skill_base_dir>\scripts')
from system_utils import init_api, find_or_create_role, find_or_create_dict, query_dict, query_sql_table_dict

init_api(API_BASE, TOKEN)

# 流程设计时查询角色编码
role_code = find_or_create_role('部门经理', 'dept_manager')

# 表单设计时查询普通字典
items = query_dict('sex')

# 查询 SQL 表字典（带签名）
items_sql = query_sql_table_dict("sys_user,realname,id,username!='admin' order by create_time")

# 创建字典
dict_code = find_or_create_dict('leave_type', '请假类型', [
    {'value': '1', 'text': '事假'},
    {'value': '2', 'text': '病假'},
])
```

## 典型场景

### 场景1：流程审批人配置角色

```python
# 需要配置"部门经理"角色作为审批人
role_code = find_or_create_role('部门经理', 'dept_manager')
# → 系统已有则返回现有编码，没有则创建后返回
# 在 BPMN 中使用: candidateGroups="{role_code}", groupType="role"
```

### 场景2：表单下拉字段配置字典

```python
# 需要"请假类型"字典
d = find_dict('leave_type')
if d:
    print(f'已有字典: {d["dictCode"]}, {len(d["items"])} 项')
    # 直接使用现有字典编码
else:
    # 创建新字典
    find_or_create_dict('leave_type', '请假类型', [
        {'value': '1', 'text': '事假'},
        {'value': '2', 'text': '病假'},
    ])
```

### 场景3：查询部门/用户信息

```python
# 查找用户用于流程指定审批人
user = find_user('张三')
if user:
    username = user['username']  # 用于 flowable:assignee

# 查找部门用于审批配置
dept = find_dept('人力资源部')
if dept:
    dept_id = dept['id']  # 用于 candidateGroups, groupType="dept"
```

## API 接口速查

> 完整接口文档见 `references/api-reference.md`

### 各模块基础路径

| 模块 | 基础路径 | Controller |
|------|---------|-----------|
| 用户 | `/sys/user` | SysUserController |
| 角色 | `/sys/role` | SysRoleController |
| 部门（公司/子公司/岗位） | `/sys/sysDepart` | SysDepartController |
| 职务/职级 | `/sys/position` | SysPositionController |
| 字典 | `/sys/dict` | SysDictController |
| 字典项 | `/sys/dictItem` | SysDictItemController |
| 租户 | `/sys/tenant` | SysTenantController |
| 分类字典 | `/sys/category` | SysCategoryController |
| 数据源 | `/sys/dataSource` | SysDataSourceController |
| 定时任务 | `/sys/quartzJob` | QuartzJobController |
| 审批角色 | `/sys/approvalRole` | ApprovalRoleController |
| 用户组 | `/sys/ugroup` | SysUserGroupController |
| 菜单权限 | `/sys/permission` | SysPermissionController |
| 通知公告 | `/sys/annountCement` | SysAnnouncementController |

### 高频接口（system_utils.py 已封装）

| 接口 | 方法 | 说明 | 对应函数 |
|------|------|------|---------|
| `/sys/role/list` | GET | 角色列表（分页） | `query_roles()` |
| `/sys/role/add` | POST | 创建系统角色 | `create_role()` |
| `/sys/user/addSysUserRole` | POST | 角色绑定用户（body: `{roleId, userIdList}`） | `add_users_to_role()` |
| `/sys/approvalRole/search` | GET | 搜索审批角色（需传 `keyword=`） | `query_approval_roles()` |
| `/sys/approvalRole/rootList` | GET | 审批角色分组列表 | — |
| `/sys/approvalRole/childList` | GET | 分组下审批角色列表（需传 `pid=`） | — |
| `/sys/approvalRole/group/add` | POST | 创建审批角色分组（body: `{name, pid:"0"}`） | `create_approval_role_group()` |
| `/sys/approvalRole/role/add` | POST | 创建审批角色（body: `{name, pid:groupId}`） | `create_approval_role()` |
| `/sys/approvalRoleUser/add` | POST | 审批角色绑定用户（body: `{approvalRoleId, userIds, bizScope, includeSub}`） | `add_users_to_approval_role()` |
| `/sys/user/list` | GET | 用户列表（分页） | `query_users()` |
| `/sys/sysDepart/queryTreeList` | GET | 部门树 | `query_depts()` |
| `/sys/sysDepart/queryDepartAndPostTreeSync` | GET | 部门+岗位树 | `query_dept_positions()` |
| `/sys/dict/list` | GET | 字典列表（分页） | `search_dict()` |
| `/sys/dict/add` | POST | 创建字典 | `create_dict()` |
| `/sys/api/getDictItems?dictCode=` | GET | 查询字典项（普通字典） | `query_dict()` |
| `/sys/dict/getDictItems/{dictCode}` | GET | 查询 SQL 表字典项（需签名） | `query_sql_table_dict()` |
| `/sys/dictItem/add` | POST | 创建字典项 | `create_dict()` 内部调用 |

### 常用查询接口（尚未封装，可直接调 `_request()`）

| 接口 | 方法 | 说明 |
|------|------|------|
| `/sys/role/queryall` | GET | 全部角色（租户隔离） |
| `/sys/role/queryallNoByTenant` | GET | 全部角色（不做租户隔离） |
| `/sys/user/queryById` | GET | 按ID查用户 |
| `/sys/user/queryByIds` | GET | 按多ID批量查用户 |
| `/sys/user/queryUserRole` | GET | 查用户拥有的角色 |
| `/sys/user/selectUserList` | GET | 流程用户选择组件查询 |
| `/sys/sysDepart/searchBy` | GET | 关键词搜索部门 |
| `/sys/sysDepart/queryDepartTreeSync` | GET | 异步加载部门树节点 |
| `/sys/sysDepart/getDepartmentHead` | GET | 部门负责人列表 |
| `/sys/position/list` | GET | 职务列表 |
| `/sys/position/queryByCode` | GET | 按code查职务 |
| `/sys/dict/getDictText/{code}/{key}` | GET | 获取字典文本值 |
| `/sys/dict/loadDict/{code}` | GET | 下拉搜索异步加载字典 |
| `/sys/category/loadTreeRoot` | GET | 分类字典根节点列表（必须传 `async=false&pcode=`） |
| `/sys/category/loadAllData` | GET | 指定节点的子节点列表（必须传 `code=<节点code>`） |
| `/sys/category/add` | POST | 创建分类节点（body: `{pid, name}`，**禁止传 code，后端自动生成**） |
| `/sys/category/delete` | DELETE | 删除分类节点（param: `id=`） |
| `/sys/tenant/list` | GET | 租户列表 |
| `/sys/tenant/getCurrentUserTenant` | GET | 当前用户所有租户 |
| `/sys/dataSource/list` | GET | 数据源列表 |
| `/sys/quartzJob/list` | GET | 定时任务列表 |
| `/sys/quartzJob/pause` | GET | 暂停任务 |
| `/sys/quartzJob/resume` | GET | 启动任务 |
| `/sys/quartzJob/execute` | GET | 立即执行一次 |
| `/sys/permission/list` | GET | 菜单列表 |
| `/sys/permission/queryRolePermission` | GET | 查角色权限 |
| `/sys/approvalRole/search` | GET | 搜索审批角色 |

### 主要数据结构

**SysUser:** `id`, `username`, `realname`, `password`, `avatar`, `birthday`, `sex`(1男/2女), `email`, `phone`, `orgCode`, `status`(0冻结/1正常), `post`(岗位ID), `userIdentity`(1普通/2上级)

**SysRole:** `id`, `roleName`, `roleCode`, `description`, `tenantId`

**SysDepart:** `id`, `parentId`, `departName`, `orgCode`, `orgCategory`(1公司/4子公司/2部门/3岗位), `departOrder`

**SysPosition:** `id`, `code`, `name`, `postLevel`(1高管/2中层/3基层/4实习)

**SysDict:** `id`, `dictName`, `dictCode`, `description`

**SysDictItem:** `id`, `dictId`, `itemText`, `itemValue`, `itemColor`, `sortOrder`, `status`(0禁用/1启用)

**SysTenant:** `id`, `name`, `beginDate`, `endDate`, `status`(0禁用/1正常)

**SysCategory:** `id`, `pid`, `name`, `code`（**`code` 由后端自动生成，禁止在 add 请求中传入**，根节点示例 `B06`，子节点示例 `B06A01`）

> **⚠️ 分类字典创建规则：**
>
> 1. **禁止传 `code`**：`/sys/category/add` 的 body 只传 `pid` 和 `name`，不要传 `code`，后端会自动按层级规则生成（根节点 `B06`、子节点 `B06A01`...）。
> 2. **获取生成的 code**：`add` 接口在新版本会在 `result` 中返回 `code`，但老版本不返回。如果响应 `result` 为 null 或不含 `code`，必须立即调用 `loadTreeRoot`（根节点）或 `loadAllData`（子节点）主动查询，拿到 `code` 后再继续创建子级，不可假设或跳过。
> 3. **查询接口参数**：`loadTreeRoot` 必须传 `async=false&pcode=`（pcode 为空字符串表示根节点）；`loadAllData` 必须传 `code=<父节点的code>`。
> 4. **删除用 DELETE 方法**：`/sys/category/delete` 需要 HTTP DELETE，传 param `id=`。

**QuartzJob:** `id`, `jobClassName`, `cronExpression`, `parameter`, `description`, `status`(0停用/-1删除/1运行)

## 源码位置

- 前端API：各模块下的 `*.api.ts` 文件（如 `user/user.api.ts`, `role/role.api.ts`）
