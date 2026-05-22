---
name: yunxiao
description: 云效 DevOps CLI，支持代码评审、任务管理和发布。当用户说「创建 MR」「提交评审」「推送代码」「更新任务」「查看任务」「发布版本」「打 tag」时触发。
---

# 云效 CLI

阿里云云效 DevOps 命令行工具。涵盖代码评审、发布管理和任务跟踪。

---

## 工具选择

| 任务 | 推荐工具 |
|------|----------|
| 创建/查看 MR | 本页工作流 + aliyun CLI |
| 更新 MR 描述 | `aliyun devops UpdateMergeRequest` |
| 查询任务列表 | `mcp__yunxiao__search_workitems` |
| 更新任务状态 | `mcp__yunxiao__update_work_item` 或 REST API |
| 添加任务评论 | REST API（见下方示例） |

---

## 创建 MR 完整流程（最常用）

**一键执行，无需额外查询。** 适用于：用户说"创建 MR"、"提交代码评审"、"推送分支并创建 MR"。

### 步骤 1：提取 ID（从 git remote 自动获取）

```bash
# 从 git remote 提取组织 ID
ORG_ID=$(git remote get-url origin | sed -E 's|.*codeup.aliyun.com[:/]([^/]+)/.*|\1|')
echo "组织 ID: $ORG_ID"

# 从 git remote 提取仓库名
REPO_NAME=$(git remote get-url origin | sed -E 's|.*/([^/]+?)(\.git)?$|\1|')
echo "仓库名: $REPO_NAME"

# 获取仓库 ID（⚠️ 注意：字段是大写 Id，不是 id）
REPO_ID=$(aliyun devops ListRepositories --organizationId $ORG_ID \
  | jq -r ".result[] | select(.name == \"$REPO_NAME\") | .Id")
echo "仓库 ID: $REPO_ID"
```

### 步骤 2：创建分支、提交、推送

```bash
# 创建并切换分支
git checkout -b feature/your-feature

# 添加改动并提交
git add .
git commit -m "feat: your commit message"

# 推送分支到远程
git push -u origin feature/your-feature
```

### 步骤 3：创建 MR

```bash
aliyun devops CreateMergeRequest \
  --organizationId $ORG_ID \
  --repositoryId $REPO_ID \
  --body '{
    "title": "feat: your MR title",
    "description": "## Summary\n\n- Change 1\n- Change 2",
    "sourceBranch": "feature/your-feature",
    "targetBranch": "main",
    "sourceProjectId": '$REPO_ID',
    "targetProjectId": '$REPO_ID',
    "createFrom": "WEB"
  }'
```

**⚠️ 关键点：**
- 仓库 ID 字段是 `Id`（大写 I），不是 `id`
- `sourceProjectId`、`targetProjectId`、`createFrom: "WEB"` 三个字段**必须提供**

---

## 更新 MR 描述

已创建的 MR 可以通过 `UpdateMergeRequest` 更新标题、描述等信息。

```bash
aliyun devops UpdateMergeRequest \
  --organizationId $ORG_ID \
  --repositoryId $REPO_ID \
  --localId <mr-local-id> \
  --body '{
    "title": "feat: updated title",
    "description": "## Summary\n\n- Updated description"
  }'
```

**参数说明：**

- `--localId`: MR 的本地编号（在 URL 中可见，如 `/mergerequests/56` 中的 `56`）
- `--body`: 要更新的字段，支持 `title`、`description` 等

**获取 MR localId：**

```bash
# 列出仓库的 MR
aliyun devops ListMergeRequests \
  --organizationId $ORG_ID \
  --repositoryId $REPO_ID \
  | jq -r '.result[] | "\(.localId): \(.title) [\(.state)]"'
```

---

## 已知 ID 速查表

**首次使用前必须获取这些 ID，后续可直接复用：**

```bash
# 获取组织 ID（必须加 --minAccessLevel 5）
aliyun devops ListOrganizations --minAccessLevel 5 \
  | jq -r '.result[] | "\(.organizationId): \(.organizationName)"'

# 获取项目 ID
aliyun devops ListProjects --organizationId <org-id> --category Project \
  | jq -r '.projects[] | "\(.identifier): \(.name)"'

# 获取任务类型 ID
aliyun devops ListProjectWorkitemTypes \
  --organizationId <org-id> --projectId <project-id> \
  --category Task --spaceType Project \
  | jq -r '.workitemTypes[] | "\(.identifier): \(.name)"'

# 获取状态 ID 列表
aliyun devops ListWorkItemWorkFlowStatus \
  --organizationId <org-id> \
  --spaceIdentifier <project-id> \
  --spaceType Project \
  --workitemTypeIdentifier <task-type-id> \
  --workitemCategoryIdentifier Task \
  | jq -r '.statuses[] | "\(.identifier): \(.name)"'
```

**常见状态 ID（大多数项目通用）：**

| 状态 | identifier |
|------|------------|
| 待处理 | `100005` |
| 处理中 | `100010` |
| 已完成 | `100014` |

---

## 任务管理（一次成功模板）

### 查看任务列表

```bash
aliyun devops ListWorkitems \
  --organizationId <org-id> \
  --spaceIdentifier <project-id> \
  --spaceType Project \
  --category Task \
  | jq -r '.workitems[] | "\(.identifier): \(.subject) [\(.status)]"'
```

### 更新任务状态为"已完成"

**⚠️ 必须用 REST API 方式（`aliyun devops POST /path`），不能用命令行参数方式**

```bash
aliyun devops POST /organization/<org-id>/workitems/updateWorkitemField \
  --body '{
    "workitemIdentifier": "<workitem-id>",
    "updateWorkitemPropertyRequest": [
      {"fieldIdentifier": "status", "fieldValue": "100014"}
    ]
  }'
```

**关键点：**
- `updateWorkitemPropertyRequest` 必须是**数组** `[{...}]`
- 字段名是 `fieldIdentifier` 和 `fieldValue`（不是 `propertyKey/propertyValue`）

### 添加任务评论

```bash
aliyun devops POST /organization/<org-id>/workitems/comment \
  --body '{
    "workitemIdentifier": "<workitem-id>",
    "content": "## 评论标题\n\n评论内容，支持 Markdown",
    "formatType": "MARKDOWN"
  }'
```

**关键点：** `formatType` 必须指定（`MARKDOWN` 或 `RICHTEXT`）

### 完整示例：完成任务并添加评论

```bash
ORG_ID="<your-org-id>"
WORKITEM_ID="<your-workitem-id>"

# 1. 更新状态为已完成
aliyun devops POST /organization/${ORG_ID}/workitems/updateWorkitemField \
  --body "{
    \"workitemIdentifier\": \"${WORKITEM_ID}\",
    \"updateWorkitemPropertyRequest\": [
      {\"fieldIdentifier\": \"status\", \"fieldValue\": \"100014\"}
    ]
  }"

# 2. 添加完成评论
aliyun devops POST /organization/${ORG_ID}/workitems/comment \
  --body "{
    \"workitemIdentifier\": \"${WORKITEM_ID}\",
    \"content\": \"## 实现完成\\n\\n- 功能已实现\\n- 测试已通过\",
    \"formatType\": \"MARKDOWN\"
  }"
```

---

## 创建任务

### 步骤 1：获取必填字段配置

**⚠️ 不同项目可能有不同的必填自定义字段，创建前必须先查询：**

```bash
# 使用 MCP 工具查询字段配置
mcp__yunxiao__get_work_item_type_field_config(
  organizationId="<org-id>",
  projectId="<project-id>",
  workItemTypeId="<task-type-id>"
)
```

常见必填字段示例：
- `assignedTo` - 负责人（用户 accountId）
- `priority` - 优先级（如 `c31cc0589797babd16889232e4` = 中）
- 自定义字段如「任务类别」「端」等

### 步骤 2：获取用户 accountId

```bash
# 列出组织成员
aliyun devops ListOrganizationMembers --organizationId <org-id> \
  | jq -r '.members[] | "\(.accountId): \(.organizationMemberName)"'
```

**⚠️ 注意：** 没有直接获取「当前用户」的 API，需要从成员列表中找到对应用户。

### 步骤 3：创建任务

```bash
aliyun devops CreateWorkitem \
  --organizationId <org-id> \
  --body '{
    "subject": "任务标题",
    "space": "<project-id>",
    "spaceIdentifier": "<project-id>",
    "spaceType": "Project",
    "category": "Task",
    "workitemType": "<task-type-id>",
    "workitemTypeIdentifier": "<task-type-id>",
    "assignedTo": "<user-accountId>",
    "description": "任务描述，支持 Markdown",
    "fieldValueList": [
      {"fieldIdentifier": "priority", "value": "<priority-id>"},
      {"fieldIdentifier": "<custom-field-id>", "value": "<value>"}
    ]
  }'
```

**关键点：**
- `space` 和 `spaceIdentifier` 必须**同时提供**，值相同
- `workitemType` 和 `workitemTypeIdentifier` 必须**同时提供**，值相同
- `assignedTo` 是**必填**的，值为用户的 `accountId`
- `fieldValueList` 中需包含项目定义的所有必填自定义字段

---

## 创建发布 Tag

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

---

## 常见错误速查

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `组织不存在` | organizationId 错误 | 用 `ListOrganizations --minAccessLevel 5` 获取 |
| 仓库 ID 返回 `null` | jq 用了小写 `id` | 改用大写 `.Id`（API 返回的字段名是大写） |
| `MissingworkitemCategoryIdentifier` | ListWorkItemWorkFlowStatus 缺参数 | 加 `--workitemCategoryIdentifier Task` |
| `MissingfieldIdentifier` | UpdateWorkitemField 参数名错误 | 用 `fieldIdentifier` 不是 `propertyKey` |
| `InvalidJSON Array parsing error` | updateWorkitemPropertyRequest 格式错误 | 必须是数组 `[{...}]` |
| `MissingformatType` | CreateWorkitemComment 缺参数 | 加 `formatType: "MARKDOWN"` |
| `category is mandatory` | ListProjects 缺参数 | 加 `--category Project` |
| `Missingspace` | CreateWorkitem 缺参数 | body 中同时包含 `space` 和 `spaceIdentifier` |
| `MissingsourceProjectId` | CreateMergeRequest 缺参数 | 加 `sourceProjectId`, `targetProjectId` |
| `MissingcreateFrom` | CreateMergeRequest 缺参数 | 加 `createFrom: "WEB"` |
| `MissingassignedTo` | CreateWorkitem 缺参数 | 用 `ListOrganizationMembers` 获取用户 accountId |
| `字段【xxx】不能为空` | 项目有必填自定义字段 | 用 MCP 工具查询字段配置后添加到 `fieldValueList` |

---

## 依赖工具

| 工具 | 用途 | 安装方式 |
|------|------|----------|
| Git | 所有操作 | 大多数系统已预装 |
| aliyun CLI | 云效 API 操作 | `brew install aliyun-cli` |

---

## 详细指南

- **AI 助手必读:** 见 [references/cheatsheet.md](references/cheatsheet.md) - 所有必须遵守的规则
- **OpenAPI 参考:** 见 [references/openapi.md](references/openapi.md) - 完整 API 文档和 MR 操作指南
