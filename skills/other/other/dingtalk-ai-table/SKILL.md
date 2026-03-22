---
name: dingtalk-ai-table
description: 钉钉 AI 表格（多维表格）操作。当用户提到"钉钉AI表格"、"AI表格"、"多维表格"、"工作表"、"字段"、"记录"、"新增记录"、"查询记录"、"更新记录"、"删除记录"、"新建字段"、"删除字段"、"dingtalk AI table"、"dingtalk notable"、"able文件"时使用此技能。支持工作表管理、字段管理、记录的增删改查等全部操作。
---

# 钉钉 AI 表格技能

负责钉钉 AI 表格（`.able` 格式多维表格）的所有操作。本文件为**策略指南**，仅包含决策逻辑和工作流程。完整 API 请求格式见文末「references/api.md 查阅索引」。

## 核心概念
- **AI 表格**（`.able` 文件）：多维表格，使用 Notable API（`/v1.0/notable`），**不是**普通电子表格
- **base_id**：AI 表格文件的 nodeId，从分享链接 `https://alidocs.dingtalk.com/i/nodes/<base_id>` 提取
- **工作表（Sheet）**：表格内的单张表，包含字段和记录
- **字段（Field）**：列定义，有名称和类型（`text`、`number`、`date`）
- **记录（Record）**：数据行，`fields` 中用**字段名称**（非 ID）作键
- **operatorId**：所有接口必须的 unionId 参数，通过 `dt_helper.sh --to-unionid` 自动转换

## 工作流程（每次执行前）
1. **先识别本次任务类型** → 例如：列工作表、创建字段、查询记录、更新记录、删除记录
2. **按本次任务校验所需配置** → 通过 `bash scripts/dt_helper.sh --get KEY` 读取；仅校验本任务必须项
3. **仅收集缺失配置** → 若缺少某项，**一次性询问用户**所有缺失值，用 `bash scripts/dt_helper.sh --set KEY=VALUE` 写入
4. **获取 Token / operatorId** → 直接调用 `bash scripts/dt_helper.sh`，token 获取与缓存细节无需关心
5. **执行操作** → 凡是包含变量替换、管道或多行逻辑的命令，写入 `/tmp/<task>.sh` 再 `bash /tmp/<task>.sh` 执行。不要把多行命令直接粘到终端里（终端工具会截断），也不要用 `<<'EOF'` 语法（heredoc 在工具中同样会被截断导致变量丢失）

### 按任务校验配置（必须先做）
- **所有任务通用必需**：`DINGTALK_APP_KEY`、`DINGTALK_APP_SECRET`、`DINGTALK_MY_USER_ID`
- **涉及任何 AI 表格 API 调用**：必须有 `DINGTALK_MY_OPERATOR_ID`（若缺失，先用 `bash scripts/dt_helper.sh --to-unionid` 自动转换并写回）
- **工作表/字段/记录相关操作**：必须有 `DINGTALK_AI_TABLE_BASE_ID`（若缺失，要求用户提供 AI 表格链接并提取 `/nodes/<base_id>`）

> 规则：未通过“本次任务配置校验”前，不得进入 API 调用步骤。

> 凭证禁止在输出中完整打印，确认时仅显示前 4 位 + `****`

### 所需配置
| 配置键 | 必填 | 说明 | 如何获取 |
|---|---|---|---|
| `DINGTALK_APP_KEY` | ✅ | 应用 AppKey | 钉钉开放平台 → 应用管理 → 凭证信息 |
| `DINGTALK_APP_SECRET` | ✅ | 应用 AppSecret | 同上 |
| `DINGTALK_MY_USER_ID` | ✅ | 当前用户的企业员工 ID（userId） | 管理后台 → 通讯录 → 成员管理 → 点击姓名查看 |
| `DINGTALK_MY_OPERATOR_ID` | ✅ | 当前用户的 unionId（operatorId） | 首次由 `bash scripts/dt_helper.sh --to-unionid` 自动转换并写入 |
| `DINGTALK_AI_TABLE_BASE_ID` | ✅ | AI 表格的 nodeId | 从 AI 表格分享链接 `/nodes/<id>` 提取 |

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
BASE_ID=$(bash "$HELPER" --get DINGTALK_AI_TABLE_BASE_ID)

# 在此追加具体 API 调用，例如列出工作表：
SHEETS=$(curl -s -X GET "https://api.dingtalk.com/v1.0/notable/bases/${BASE_ID}/sheets?operatorId=${OPERATOR_ID}" \
  -H "x-acs-dingtalk-access-token: $NEW_TOKEN")
echo "工作表列表: $SHEETS"
```

> **Token 失效处理**：dt_helper 仅按时间缓存，无法感知 token 被提前吊销。若 API 返回 401（token 无效/过期），用 `--nocache` 跳过缓存强制重新获取：
> ```bash
> NEW_TOKEN=$(bash "$HELPER" --token --nocache)
> ```

## references/api.md 查阅索引
确定好要做什么之后，用以下命令从 `references/api.md` 中提取对应章节的完整 API 细节（请求格式、参数说明、返回值示例）：
```bash
grep -A 20 "^## 1. 列出工作表" references/api.md
grep -A 15 "^## 2. 查询单个工作表" references/api.md
grep -A 30 "^## 3. 创建工作表" references/api.md
grep -A 15 "^## 4. 删除工作表" references/api.md
grep -A 25 "^## 5. 列出字段" references/api.md
grep -A 28 "^## 6. 创建字段" references/api.md
grep -A 15 "^## 7. 更新字段" references/api.md
grep -A 15 "^## 8. 删除字段" references/api.md
grep -A 25 "^## 9. 新增记录" references/api.md
grep -A 40 "^## 10. 查询记录列表" references/api.md
grep -A 18 "^## 11. 更新记录" references/api.md
grep -A 15 "^## 12. 删除记录" references/api.md
grep -A 10 "^## 错误码" references/api.md
grep -A 6  "^## 所需应用权限" references/api.md
```
