---
name: dingtalk-todo
description: 钉钉待办管理。当用户提到"钉钉待办"、"待办任务"、"创建待办"、"新增待办"、"查看待办"、"完成待办"、"标记完成"、"删除待办"、"待办列表"、"我的待办"、"设置截止时间"、"指派待办"、"dingtalk todo"、"todo task"、"task management"时使用此技能。支持：创建待办（含描述/截止时间/优先级/参与者）、获取详情、查询列表（按完成状态过滤）、更新待办、标记完成、删除待办等全部待办类操作。
---

# 钉钉待办技能

负责钉钉待办（Todo）的所有操作。本文件为**策略指南**，仅包含决策逻辑和工作流程。完整 API 请求格式见文末「references/api.md 查阅索引」。

---

## 工作流程（每次执行前）

1. **读取配置** → 用一条 `grep -E` 命令一次性读取配置文件`~/.dingtalk-skills/config`, 所有所需配置键值（配置文件跨会话保留，无需重复询问）
2. **仅收集缺失配置** → 若配置文件不存在或缺少某项，**一次性询问用户**所有缺失的值，不要逐条问
3. **持久化** → 将收集到的值写入 `~/.dingtalk-skills/config` 文件，后续无需再问
4. **获取/复用 Token** → 有效期内复用缓存（缓存 7000 秒，约 2 小时），避免重复请求；遇 401 重新获取
5. **执行操作** → 凡是包含变量替换、管道或多行逻辑的命令，`/tmp/<task>.sh` 再 `bash /tmp/<task>.sh` 执行。不要把多行命令直接粘到终端里（终端工具会截断），也不要用 `<<'EOF'` 语法（heredoc 在工具中同样会被截断导致变量丢失）

> 凭证禁止在输出中完整打印，确认时仅显示前 4 位 + `****`

### 所需配置

| 配置键 | 说明 | 如何获取 |
|---|---|---|
| `DINGTALK_APP_KEY` | 应用 AppKey | 钉钉开放平台 → 应用管理 → 凭证信息 |
| `DINGTALK_APP_SECRET` | 应用 AppSecret | 同上 |
| `DINGTALK_MY_USER_ID` | 当前用户的企业员工 ID（userId） | 管理后台 → 通讯录 → 成员管理 → 点击姓名查看（不是手机号、不是 unionId） |
| `DINGTALK_MY_OPERATOR_ID` | 当前用户的 unionId | 首次由脚本自动通过 userId 转换获取并写入 |

### 身份标识说明

钉钉有两种用户 ID，不同 API 使用不同的 ID：

| 标识 | 说明 | 如何获取 |
|---|---|---|
| `userId`（= `staffId`） | 企业内部员工 ID，**最容易获取** | 管理后台 → 通讯录 → 成员管理 → 点击姓名查看；或调用手机号查询 API |
| `unionId` | 跨企业/跨应用唯一 | 通过 userId 调用 API 转换获取 |

- **待办 API 的路径参数 `{unionId}` 和查询参数 `operatorId` 均使用 unionId**
- **executorIds / participantIds（指派同事）也使用 unionId**
- 因此配置中优先收集 `userId`（用户容易拿到），由脚本自动转换为 `unionId`

#### userId → unionId 转换

需要旧版 access_token（与新版不同）：

```bash
# 1. 获取旧版 token
OLD_TOKEN=$(curl -s "https://oapi.dingtalk.com/gettoken?appkey=${APP_KEY}&appsecret=${APP_SECRET}" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

# 2. userId → unionId
UNION_ID=$(curl -s -X POST "https://oapi.dingtalk.com/topapi/v2/user/get?access_token=${OLD_TOKEN}" \
  -H 'Content-Type: application/json' \
  -d "{\"userid\":\"${USER_ID}\"}" | grep -o '"unionid":"[^"]*"' | cut -d'"' -f4)

# 3. 写入配置文件
echo "DINGTALK_MY_OPERATOR_ID=$UNION_ID" >> ~/.dingtalk-skills/config
```

> ⚠️ 注意：返回体中 `result.unionid`（无下划线）有值，`result.union_id`（有下划线）可能为空。

#### 给同事创建待办时

如果用户要给同事创建待办（指定 executorIds），需要同事的 **unionId**。向用户询问同事的 **userId**（管理后台可查），然后用上述方法转换。

### 执行脚本模板

```bash
#!/bin/bash
set -e
CONFIG=~/.dingtalk-skills/config
APP_KEY=$(grep '^DINGTALK_APP_KEY=' "$CONFIG" | cut -d= -f2-)
APP_SECRET=$(grep '^DINGTALK_APP_SECRET=' "$CONFIG" | cut -d= -f2-)
USER_ID=$(grep '^DINGTALK_MY_USER_ID=' "$CONFIG" | cut -d= -f2-)

# 新版 Token 缓存（用于待办 API）
CACHED_TOKEN=$(grep '^DINGTALK_ACCESS_TOKEN=' "$CONFIG" 2>/dev/null | cut -d= -f2-)
TOKEN_EXPIRY=$(grep '^DINGTALK_TOKEN_EXPIRY=' "$CONFIG" 2>/dev/null | cut -d= -f2-)
NOW=$(date +%s)
if [ -n "$CACHED_TOKEN" ] && [ -n "$TOKEN_EXPIRY" ] && [ "$NOW" -lt "$TOKEN_EXPIRY" ]; then
  TOKEN=$CACHED_TOKEN
else
  RESP=$(curl -s -X POST https://api.dingtalk.com/v1.0/oauth2/accessToken \
    -H 'Content-Type: application/json' \
    -d "{\"appKey\":\"$APP_KEY\",\"appSecret\":\"$APP_SECRET\"}")
  TOKEN=$(echo "$RESP" | grep -o '"accessToken":"[^"]*"' | cut -d'"' -f4)
  sed -i '/^DINGTALK_ACCESS_TOKEN=/d;/^DINGTALK_TOKEN_EXPIRY=/d' "$CONFIG"
  echo "DINGTALK_ACCESS_TOKEN=$TOKEN" >> "$CONFIG"
  echo "DINGTALK_TOKEN_EXPIRY=$((NOW + 7000))" >> "$CONFIG"
fi

# unionId：优先从配置读取，未存储时自动从 userId 转换并写入
UNION_ID=$(grep '^DINGTALK_MY_OPERATOR_ID=' "$CONFIG" 2>/dev/null | cut -d= -f2-)
if [ -z "$UNION_ID" ]; then
  OLD_TOKEN=$(curl -s "https://oapi.dingtalk.com/gettoken?appkey=${APP_KEY}&appsecret=${APP_SECRET}" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
  UNION_ID=$(curl -s -X POST "https://oapi.dingtalk.com/topapi/v2/user/get?access_token=${OLD_TOKEN}" \
    -H 'Content-Type: application/json' \
    -d "{\"userid\":\"${USER_ID}\"}" | grep -o '"unionid":"[^"]*"' | cut -d'"' -f4)
  echo "DINGTALK_MY_OPERATOR_ID=$UNION_ID" >> "$CONFIG"
fi

# 在此追加具体 API 调用，例如创建待办：
RESULT=$(curl -s -X POST \
  "https://api.dingtalk.com/v1.0/todo/users/${UNION_ID}/tasks?operatorId=${UNION_ID}" \
  -H "x-acs-dingtalk-access-token: $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"subject\":\"今天完成需求评审\"}")
echo "$RESULT"
TASK_ID=$(echo "$RESULT" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "创建成功，taskId=$TASK_ID"
```

---

> ⚠️ 通过应用 API 创建的待办显示在钉钉「待办」的 **Teambition 分类**下，不是「个人」分类。
> ⚠️ 通过 API 创建的任务无法在钉钉 UI 里手动删除，只能通过 API 删除。

## references/api.md 查阅索引

确定好要做什么之后，用以下命令从 `references/api.md` 中提取对应章节的完整 API 细节（请求格式、参数说明、返回值示例）：

```bash
# 身份标识与 userId ↔ unionId 转换（28 行）
grep -A 28 "^## 身份标识" references/api.md

# 创建待办（含所有可选字段）（47 行）
grep -A 47 "^## 1. 创建待办" references/api.md

# 获取待办详情（29 行）
grep -A 29 "^## 2. 获取待办详情" references/api.md

# 查询待办列表（含分页）（42 行）
grep -A 42 "^## 3. 查询待办列表" references/api.md

# 更新待办（25 行）
grep -A 25 "^## 4. 更新待办" references/api.md

# 删除待办（16 行）
grep -A 16 "^## 5. 删除待办" references/api.md

# 错误码表（9 行）
grep -A 9 "^## 错误码" references/api.md

# 所需应用权限（7 行）
grep -A 7 "^## 所需应用权限" references/api.md
```
