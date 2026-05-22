---
name: dingtalk-message
description: 钉钉消息发送。当用户提到"钉钉消息"、"发消息"、"发通知"、"群通知"、"群消息"、"Webhook"、"机器人消息"、"机器人发消息"、"工作通知"、"单聊消息"、"群聊消息"、"撤回消息"、"消息已读"、"发送Markdown"、"发卡片消息"、"ActionCard"、"@某人"、"@员工"、"at某人"、"提醒某人"、"dingtalk message"、"send message"、"robot message"、"work notification"时使用此技能。支持：群自定义 Webhook 机器人（文本/Markdown/ActionCard/Link/FeedCard + 加签 + @某人）、企业内部应用机器人单聊和群聊发送、消息撤回、已读查询、工作通知等全部消息类操作。
---

# 钉钉消息技能

负责钉钉消息发送的所有操作。本文件为**策略指南**，仅包含决策逻辑和工作流程。完整 API 请求格式见文末的 `references/api.md` 查阅索引。

---

## 四种消息通道概览

| 通道 | 适用场景 | 认证方式 | 特点 |
|---|---|---|---|
| **Webhook 机器人** | 往指定群发通知 | 无需 token，URL 自带凭证 | 最简单；支持加签安全模式 |
| **企业内部应用机器人** | 单聊私信 / 群聊消息 | 新版 accessToken | 可撤回、查已读；需 userId 或 openConversationId |
| **工作通知** | 以应用身份推送到"工作通知"会话 | 旧版 access_token + agentId | 可推全员/部门；出现在工作通知而非聊天 |
| **sessionWebhook** | 回调中直接回复当前对话 | 无需任何认证 | 回调消息自带临时 URL，约 1.5 小时有效 |

---

### 工作流程（每次执行前）

1. **先理解用户意图** → 判断属于哪个消息通道（见下方「场景路由」）
2. **读取配置** → 用一条 `grep -E '^KEY1=|^KEY2='` 命令一次性读取该通道所需的全部键值，不要分多次查询。（跨会话保留，所有 dingtalk-skills 共用同一文件）具体需要哪些配置，见[各通道所需配置](### 各通道所需配置)表格
3. **仅收集该通道所需的缺失配置** → 一次性询问，不要逐条问
4. **持久化** → 写入 config，后续无需再问
5. **执行任务**

### 各通道所需配置

| 通道 | 所需配置 | 来源说明 |
|---|---|---|
| Webhook | `DINGTALK_WEBHOOK_URL` | 群设置 → 智能群助手 → 添加自定义机器人 |
| Webhook（加签） | 额外 `DINGTALK_WEBHOOK_SECRET` | 创建机器人时选择"加签"模式获得 |
| 机器人消息 | `DINGTALK_APP_KEY` + `DINGTALK_APP_SECRET` | 开放平台 → 应用管理 → 凭证信息 |
| 工作通知 | `DINGTALK_APP_KEY` + `DINGTALK_APP_SECRET` + `DINGTALK_AGENT_ID` | agentId 在应用管理 → 基本信息 |

> - `robotCode` = `appKey`（完全一致，无需额外配置）
> - 凭证禁止在输出中完整打印，确认时仅显示前 4 位 + `****`

### 执行规范(推荐)

**始终使用脚本文件执行**：凡是包含变量替换（`$(...)`）、管道（`|`）或多行逻辑的命令，一律用 `create_file` 写到 `/tmp/<task>.sh` 再 `bash /tmp/<task>.sh` 执行，不要内联到终端。内联命令会被终端工具截断或污染，导致变量读取失败。

**禁止** heredoc（`<<'EOF'`），会被工具截断。

典型脚本模板（读取配置 → 获取 token（带缓存）→ 执行 API）：
```bash
#!/bin/bash
set -e
CONFIG=~/.dingtalk-skills/config

# 一次性读取所有所需配置
APP_KEY=$(grep '^DINGTALK_APP_KEY=' "$CONFIG" | cut -d= -f2-)
APP_SECRET=$(grep '^DINGTALK_APP_SECRET=' "$CONFIG" | cut -d= -f2-)

# Token 缓存：有效期内复用，避免重复请求
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
  EXPIRY=$((NOW + 7000))  # token 有效期 2h，提前约 13 分钟过期
  # 更新缓存（先删旧值再追加）
  sed -i '/^DINGTALK_ACCESS_TOKEN=/d;/^DINGTALK_TOKEN_EXPIRY=/d' "$CONFIG"
  echo "DINGTALK_ACCESS_TOKEN=$TOKEN" >> "$CONFIG"
  echo "DINGTALK_TOKEN_EXPIRY=$EXPIRY" >> "$CONFIG"
fi

# 在此追加具体 API 调用
```

JSON 字段提取：`grep -o '"key":"[^"]*"' | cut -d'"' -f4`

### 消息内容缺失时的处理

用户未指定消息内容时，**不要自行编造**，应先询问用户想发送什么内容。仅当用户明确表示"随便发一条测试"时，才使用默认内容：`这是一条来自钉钉机器人的测试消息。`

---

## 场景路由（收到用户请求后的判断逻辑）

```
用户想发消息
├─ 发到群里？
│  ├─ 通用群消息（含 @某人）→ 询问用户选择发送方式（见下方「群消息发送方式选择」）
│  ├─ 明确需要撤回或查已读 → 企业机器人群聊（直接跳过询问）
│  └─ 正在处理机器人回调，直接回复 → sessionWebhook
├─ 发给个人？
│  ├─ 以机器人身份发私信 → 企业机器人单聊
│  └─ 以应用身份推工作通知 → 工作通知
├─ 撤回/查已读？
│  ├─ 机器人消息 → 企业机器人的撤回/已读 API
│  └─ 工作通知 → 工作通知的查询/撤回 API
└─ 回复机器人收到的消息？ → sessionWebhook
```

---

## 群消息发送方式选择

用户发起群消息请求时，**必须先询问**他们选择哪种方式，并说明各自需要什么配置：

> 请问您想通过哪种方式发这条群消息？
>
> | 方式 | 需要提供 | 如何获取 | 说明 |
> |---|---|---|---|
> | **Webhook 机器人** | `WEBHOOK_URL` | 群设置 → 智能群助手 → 添加自定义机器人 → 复制 URL | 无需应用权限，配置最简单；支持 @某人（`at.atUserIds`） |
> | **企业内部应用机器人** | `openConversationId`（群会话 ID） | 机器人收到群消息时，回调体的 `conversationId` 字段即为该值 | 需要 `APP_KEY`/`APP_SECRET`；支持撤回、查已读 |
>
> 推荐 **Webhook**，只需一个 URL 即可，无需任何应用权限。

收到用户选择后按以下方式收集配置：
- 选 **Webhook**：收集 `DINGTALK_WEBHOOK_URL`（若启用加签还需 `DINGTALK_WEBHOOK_SECRET`），持久化后执行
- 选 **企业机器人**：收集 `openConversationId`，复用已有的 `APP_KEY`/`APP_SECRET`（若未配置则一并收集），调用 `groupMessages/send`

---

执行 API 前按通道获取对应 token：

| 通道 | token 类型 | 获取方式 | 使用方式 |
|---|---|---|---|
| 机器人消息 | 新版 accessToken | `POST https://api.dingtalk.com/v1.0/oauth2/accessToken` | 请求头 `x-acs-dingtalk-access-token` |
| 工作通知 | 旧版 access_token | `GET https://oapi.dingtalk.com/gettoken?appkey=&appsecret=` | URL 参数 `?access_token=` |
| Webhook | 无需 token | — | 直接 POST 到 Webhook URL |
| sessionWebhook | 无需 token | — | 直接 POST 到回调中的 sessionWebhook URL |

> token 有效期均为 2 小时，遇 401 重新获取即可。具体请求/返回格式见 api.md 对应章节。

---

## 身份标识（关键决策知识）

**所有消息发送 API 均只接受 userId（staffId）**，不接受 unionId。这一点已通过实际 API 调用验证。

| 标识 | 作用域 | 能否用于发消息 |
|---|---|---|
| `userId`（= `staffId`） | 单个企业内唯一 | ✅ 唯一接受的 ID |
| `unionId` | 跨组织唯一 | ❌ 会被判定无效用户 |

### 如何获取 userId

1. **机器人回调**（最常用）：消息体的 `senderStaffId` 字段
2. **unionId → userId**：`POST /topapi/user/getbyunionid`
3. **手机号 → userId**：`POST /topapi/v2/user/getbymobile`
4. **管理后台**：PC 端钉钉 → 工作台 → 管理后台 → 通讯录

### 回调消息中的身份字段

| 字段 | 含义 | 可靠性 |
|---|---|---|
| `senderStaffId` | 发送者 userId | 企业内部群始终存在；外部群中外部用户可能为空 |
| `senderUnionId` | 发送者 unionId | 始终存在 |

> userId ↔ unionId 互转的 API 细节：`grep -A 8 "^#### userId ↔ unionId" references/api.md`
> 注意 `result.unionid`（无下划线）有值，`result.union_id`（有下划线）在部分企业中为空。

---

## 消息类型速查

### Webhook 消息类型

直接在请求 body 的 `msgtype` 字段指定：`text` | `markdown` | `actionCard` | `link` | `feedCard`

> 各类型完整 JSON 格式：`grep -A 30 "^#### 文本消息" references/api.md`（将 `文本消息` 替换为 `Markdown 消息`、`ActionCard` 等）

### 机器人消息类型

通过 `msgKey` + `msgParam`（JSON 字符串）指定：

| msgKey | 类型 | msgParam 关键字段 |
|---|---|---|
| `sampleText` | 文本 | `content` |
| `sampleMarkdown` | Markdown | `title`, `text` |
| `sampleActionCard` | ActionCard | `title`, `text`, `singleTitle`, `singleURL` |
| `sampleLink` | 链接 | `title`, `text`, `messageUrl`, `picUrl` |
| `sampleImageMsg` | 图片 | `photoURL` |

> **重要**：`msgParam` 必须是 **JSON 字符串**，不是对象。完整格式：`grep -A 16 "^### 消息类型" references/api.md`

### 工作通知消息类型

在 `msg` 对象的 `msgtype` 字段指定：`text` | `markdown` | `action_card`

> 注意工作通知的 `action_card` 用下划线（不同于 Webhook 的 `actionCard`）。完整格式：`grep -A 62 "^### 工作通知消息类型" references/api.md`

---

## 典型场景

### "发个群消息通知大家" / "@某人的群消息"
→ 先按「群消息发送方式选择」询问用户用 Webhook 还是企业机器人，收集对应配置后执行。
> Webhook 支持 @某人：body 中加 `at.atUserIds`（用户 ID 数组），正文同时写 `@userId` 以高亮显示。

### "用 Markdown 发个部署通知到群里"
→ 先询问发送方式（同上），确认选 Webhook 后用 `msgtype: markdown` 构造 body；若选企业机器人则用 `msgKey: sampleMarkdown`。

### "给张三发条消息"
→ **机器人单聊**。需 `APP_KEY`/`APP_SECRET` + 张三的 userId。调用 `oToMessages/batchSend`。

### "往研发群发个带按钮的消息"
→ 先按「群消息发送方式选择」询问用户用 Webhook 还是企业机器人，收集对应配置后执行。
> Webhook 用 `msgtype: actionCard`；企业机器人用 `msgKey: sampleActionCard`。

### "发工作通知给全员"
→ **工作通知**。需 `APP_KEY`/`APP_SECRET`/`AGENT_ID`。`to_all_user: true`。

### "撤回刚才那条消息"
→ 找到上一次发送返回的 `processQueryKey`（机器人）或 `task_id`（工作通知），调用对应撤回 API。

### "回复机器人收到的消息"
→ **sessionWebhook**。从回调取 `sessionWebhook` URL，直接 POST，无需任何认证。

---

## 错误处理速查

| 场景 | 错误特征 | 处理 |
|---|---|---|
| Webhook | `310000 keywords not in content` | 需包含自定义关键词 |
| Webhook | `310000 sign not match` | 检查签名计算和 timestamp |
| Webhook | `302033 send too fast` | 限 20 条/分钟，等待重试 |
| 机器人 | `invalidStaffIdList` 非空 | userId 无效，确认在组织内 |
| 机器人 | `flowControlledStaffIdList` 非空 | 限流，稍候重试 |
| 工作通知 | `errcode: 88` | agentId 错误 |
| 工作通知 | `errcode: 33` | access_token 过期 |
| 通用 | 401 / 403 | token 过期 / 权限不足 |

> 完整错误码表：`grep -A 33 "^## 错误码" references/api.md`

---

## 所需应用权限

| 功能 | 权限 |
|---|---|
| 机器人单聊 | `Robot.Message.Send` |
| 机器人群聊 | `Robot.GroupMessage.Send` |
| 消息已读查询 | `Robot.Message.Query` |
| 消息撤回 | `Robot.Message.Recall` |
| 工作通知 | `Message.CorpConversation.AsyncSend` |
| Webhook / sessionWebhook | 无需应用权限 |

---

## references/api.md 查阅索引

确定好要做什么之后，用以下命令从 `references/api.md` 中提取对应章节的完整 API 细节（请求格式、参数表、返回值示例）：

```bash
grep -A 196 "^## 一、群自定义 Webhook 机器人" references/api.md
grep -A 19 "^### 加签计算" references/api.md
grep -A 192 "^## 二、企业内部应用机器人" references/api.md
grep -A 36 "^#### 钉钉身份标识体系" references/api.md
grep -A 16 "^### 消息类型" references/api.md
grep -A 145 "^## 三、工作通知" references/api.md
grep -A 60 "^## 四、sessionWebhook" references/api.md
grep -A 33 "^## 错误码" references/api.md
grep -A 30 "^#### 文本消息" references/api.md
grep -A 30 "^### 批量发送单聊消息" references/api.md
grep -A 30 "^### 发送工作通知" references/api.md
```
