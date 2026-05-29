# Email Automation Skill

邮箱自动化：读取、搜索、草拟、发送邮件。

## 支持的方式

### 方式 1: Gmail API (推荐)

**优点**: 功能完整，支持标签、搜索、草稿
**配置步骤**:

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建项目 → 启用 Gmail API
3. 创建 OAuth 2.0 凭据（桌面应用）
4. 下载 `credentials.json`
5. 存储到 `~/.config/gmail/credentials.json`

```bash
# 安装依赖
pip3 install google-auth-oauthlib google-api-python-client

# 首次授权（会打开浏览器）
python3 ~/clawd/skills/email-automation/gmail_auth.py
```

### 方式 2: IMAP/SMTP (通用)

**优点**: 支持任何邮箱
**配置**:

```bash
# 存储凭据
pass insert email/gmail-address    # 邮箱地址
pass insert email/gmail-app-pass   # 应用专用密码（非登录密码）
```

Gmail 应用专用密码获取：
1. 访问 https://myaccount.google.com/apppasswords
2. 选择"邮件" + "其他设备"
3. 生成 16 位密码

### 方式 3: n8n 工作流

使用 n8n 的 Gmail/IMAP 节点，通过 webhook 触发。

---

## 核心功能

### 读取邮件

```python
# gmail_read.py
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file('token.json')
service = build('gmail', 'v1', credentials=creds)

# 获取最新 10 封邮件
results = service.users().messages().list(
    userId='me', maxResults=10, q='is:unread'
).execute()

for msg in results.get('messages', []):
    detail = service.users().messages().get(
        userId='me', id=msg['id'], format='metadata'
    ).execute()
    headers = {h['name']: h['value'] for h in detail['payload']['headers']}
    print(f"From: {headers.get('From')}")
    print(f"Subject: {headers.get('Subject')}")
    print("---")
```

### 搜索邮件

```python
# Gmail 搜索语法
queries = {
    "未读": "is:unread",
    "今天": "newer_than:1d",
    "重要": "is:important",
    "带附件": "has:attachment",
    "来自某人": "from:someone@example.com",
    "主题包含": "subject:关键词",
}
```

### 发送邮件

```python
# gmail_send.py
import base64
from email.mime.text import MIMEText

def create_message(to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_email(service, to, subject, body):
    message = create_message(to, subject, body)
    service.users().messages().send(userId='me', body=message).execute()
```

### IMAP 方式（备选）

```python
import imaplib
import email

# 连接
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(EMAIL, APP_PASSWORD)
mail.select('inbox')

# 搜索未读
status, messages = mail.search(None, 'UNSEEN')
for num in messages[0].split():
    status, data = mail.fetch(num, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    print(f"From: {msg['from']}")
    print(f"Subject: {msg['subject']}")
```

---

## 安全策略

### 权限分层（参考 SECURITY.md）

| 操作 | 权限级别 |
|------|----------|
| 读取邮件列表 | 🟢 自由 |
| 读取邮件内容 | 🟢 自由 |
| 搜索邮件 | 🟢 自由 |
| 创建草稿 | 🟢 自由 |
| 发送邮件 | 🟡 需确认 |
| 删除邮件 | 🟡 需确认 |
| 修改标签 | 🟢 自由 |

### 发送确认流程

```
⚠️ 需要确认发送邮件：

收件人: xxx@example.com
主题: Re: 关于项目进度
内容预览:
---
你好，

关于项目进度...
---

回复 "确认" 发送，或 "取消" 放弃
```

---

## 自动化场景

### 1. 邮件摘要（每日）

```
每天早上检查未读邮件，生成摘要推送到 Telegram
```

### 2. 重要邮件提醒

```
监控特定发件人/关键词，立即通知
```

### 3. 自动回复草稿

```
收到邮件后自动生成回复草稿，等待确认后发送
```

---

## 配置清单

完成配置后，在 TOOLS.md 中记录：

```markdown
### Email
- Provider: Gmail
- Address: xxx@gmail.com
- Auth: OAuth 2.0 / App Password
- Token: ~/.config/gmail/token.json
- 权限: 读取 ✅ | 发送 ⚠️需确认
```

---

## 相关文件

- `gmail_auth.py` - OAuth 授权脚本
- `gmail_read.py` - 读取邮件
- `gmail_send.py` - 发送邮件
- `SECURITY.md` - 安全策略
