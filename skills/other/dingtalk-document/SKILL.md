---
name: dingtalk-document
description: 钉钉知识库和文档管理操作。当用户提到"钉钉文档"、"知识库"、"新建文档"、"查看文档目录"、"读取文档内容"、"写入文档"、"更新文档"、"文档成员"、"dingtalk doc"、"knowledge base"时使用此技能。支持：创建知识库、查询知识库列表、新建文档/文件夹、读取/写入文档正文内容、管理成员权限等全部文档类操作。
---

# 钉钉文档技能

负责钉钉知识库和文档的所有操作。本文件为**策略指南**，仅包含决策逻辑和工作流程。完整 API 请求格式见文末「references/api.md 查阅索引」。

> `dt_helper.sh` 位于本 `SKILL.md` 同级目录的 `scripts/dt_helper.sh`。

## 核心概念
- **知识库（Workspace）**：文档容器，有 `workspaceId` 和 `rootNodeId`
- **节点（Node）**：文件或文件夹，`type` 为 `FILE` 或 `FOLDER`
- **文档标识（用于 `/v1.0/doc/suites/documents/{id}`）**：可用 `docKey` 或 `dentryUuid`
  - 创建文档响应会返回：`docKey`、`dentryUuid`、`nodeId`
  - 其中 `docKey` / `dentryUuid` 可用于读写正文；`nodeId` 用于删除和文档管理类接口
  - `wiki/nodes` 返回的 `nodeId` 实际上是 `dentryUuid`，可直接用于正文读写
- **operatorId**：所有接口必须的 unionId 参数，通过 `bash scripts/dt_helper.sh --to-unionid` 自动转换

## 工作流程（每次执行前）
1. **先识别本次任务类型** → 例如：列知识库、读文档、写文档、创建文档、成员管理
2. **按本次任务校验所需配置** → 通过 `bash scripts/dt_helper.sh --get KEY` 读取；仅校验本任务必须项
3. **仅收集缺失配置** → 若缺少某项，**一次性询问用户**所有缺失值，用 `bash scripts/dt_helper.sh --set KEY=VALUE` 写入
4. **获取 Token / operatorId** → 直接调用 `bash scripts/dt_helper.sh`，token 获取与缓存细节无需关心
5. **执行操作** → 凡是包含变量替换、管道或多行逻辑的命令，写入 `/tmp/<task>.sh` 再 `bash /tmp/<task>.sh` 执行。不要把多行命令直接粘到终端里（终端工具会截断），也不要用 `<<'EOF'` 语法（heredoc 在工具中同样会被截断导致变量丢失）

### 按任务校验配置（必须先做）
- **所有任务通用必需**：`DINGTALK_APP_KEY`、`DINGTALK_APP_SECRET`、`DINGTALK_MY_USER_ID`
- **涉及任何文档/知识库 API 调用**：必须有 `DINGTALK_MY_OPERATOR_ID`（若缺失，先用 `bash scripts/dt_helper.sh --to-unionid` 自动转换并写回）
- **创建/读取/写入/删除/成员管理**：除上述通用项外，无额外固定配置键；`workspaceId`/`nodeId`/`docKey` 属于任务参数，运行时从用户输入或 API 响应中获取

> 规则：未通过“本次任务配置校验”前，不得进入 API 调用步骤。

> 凭证禁止在输出中完整打印，确认时仅显示前 4 位 + `****`

### 所需配置
| 配置键 | 必填 | 说明 | 如何获取 |
|---|---|---|---|
| `DINGTALK_APP_KEY` | ✅ | 应用 AppKey | 钉钉开放平台 → 应用管理 → 凭证信息 |
| `DINGTALK_APP_SECRET` | ✅ | 应用 AppSecret | 同上 |
| `DINGTALK_MY_USER_ID` | ✅ | 当前用户的企业员工 ID（userId） | 管理后台 → 通讯录 → 成员管理 → 点击姓名查看 |
| `DINGTALK_MY_OPERATOR_ID` | ✅ | 当前用户的 unionId（operatorId） | 首次由 `bash scripts/dt_helper.sh --to-unionid` 自动转换并写入 |

### 身份标识说明
| 标识 | 说明 |
|---|---|
| `userId`（= `staffId`） | 企业内部员工 ID，可通过管理后台 -> 通讯录 -> 成员管理 -> 点击姓名查看 |
| `unionId` | 跨企业/跨应用唯一标识，可通过 `bash scripts/dt_helper.sh --to-unionid <userid>` 获取 |

### 执行脚本模板
```bash
#!/bin/bash
set -e
HELPER="./scripts/dt_helper.sh"
NEW_TOKEN=$(bash "$HELPER" --token)
OPERATOR_ID=$(bash "$HELPER" --get DINGTALK_MY_OPERATOR_ID)

# 在此追加具体 API 调用，例如查询知识库列表：
WORKSPACES=$(curl -s -X GET "https://api.dingtalk.com/v2.0/wiki/workspaces?operatorId=${OPERATOR_ID}&maxResults=20" \
  -H "x-acs-dingtalk-access-token: $NEW_TOKEN")
echo "知识库列表: $WORKSPACES"
```

> **Token 失效处理**：dt_helper 仅按时间缓存，无法感知 token 被提前吊销。若 API 返回 401（token 无效/过期），用 `--nocache` 跳过缓存强制重新获取：
> ```bash
> NEW_TOKEN=$(bash "$HELPER" --token --nocache)
> ```

## references/api.md 查阅索引
确定好要做什么之后，用以下命令从 `references/api.md` 中提取对应章节的完整 API 细节（请求格式、参数说明、返回值示例）：
```bash
grep -A 30 "^## 1. 查询知识库列表" references/api.md
grep -A 10 "^## 2. 查询知识库信息" references/api.md
grep -A 35 "^## 3. 查询节点列表" references/api.md
grep -A 10 "^## 4. 查询单个节点" references/api.md
grep -A 15 "^## 5. 通过 URL 查询节点" references/api.md
grep -A 28 "^## 6. 创建文档" references/api.md
grep -A 10 "^## 7. 删除文档" references/api.md
grep -A 30 "^## 8. 读取文档内容" references/api.md
grep -A 15 "^## 9. 覆盖写入文档内容" references/api.md
grep -A 12 "^## 10. 追加文本到段落" references/api.md
grep -A 18 "^## 11. 添加文档成员" references/api.md
grep -A 12 "^## 12. 更新文档成员权限" references/api.md
grep -A 10 "^## 13. 移除文档成员" references/api.md
grep -A 10 "^## 错误码" references/api.md
grep -A 10 "^## 所需应用权限" references/api.md
```
