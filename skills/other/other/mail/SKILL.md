---
name: mail
description: 邮件管理技能，支持发送和接收邮件，支持Gmail、QQ邮箱、163邮箱等主流邮件服务。当用户需要发送邮件、接收邮件、管理邮件附件或配置邮件账户时使用此技能。
---

# 邮件管理技能

本技能提供完整的邮件管理功能，包括发送邮件、接收邮件、管理附件和配置邮件账户。

## 快速开始

### 1. 配置邮件账户

在.env文件中添加您的邮件配置：

```bash
# Gmail配置示例
MAIL_SMTP_SERVER=smtp.gmail.com
MAIL_SMTP_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_IMAP_SERVER=imap.gmail.com
MAIL_IMAP_PORT=993

# QQ邮箱配置示例
MAIL_SMTP_SERVER=smtp.qq.com
MAIL_SMTP_PORT=587
MAIL_USERNAME=your_email@qq.com
MAIL_PASSWORD=your_authorization_code
MAIL_IMAP_SERVER=imap.qq.com
MAIL_IMAP_PORT=993
```

### 2. 发送邮件

使用Python脚本发送邮件：

```python
# 导入邮件发送脚本
from scripts.send_mail import send_email

# 发送简单邮件
send_email(
    to="recipient@example.com",
    subject="邮件主题",
    body="邮件内容"
)

# 发送带附件的邮件
send_email(
    to="recipient@example.com",
    subject="带附件的邮件",
    body="请查看附件",
    attachments=["/path/to/file1.pdf", "/path/to/file2.jpg"]
)
```

### 3. 接收邮件

```python
# 导入邮件接收脚本
from scripts.receive_mail import fetch_emails

# 获取最新邮件
emails = fetch_emails(limit=10)

# 搜索特定邮件
emails = fetch_emails(search_criteria={
    "subject": "重要",
    "from": "boss@company.com"
})
```

## 详细功能

### 发送邮件功能

支持以下功能：
- 发送纯文本邮件
- 发送HTML格式邮件
- 添加多个附件
- 抄送(CC)和密送(BCC)
- 邮件优先级设置
- 发送回执请求

### 接收邮件功能

支持以下功能：
- 获取最新邮件列表
- 搜索邮件（按发件人、主题、日期等）
- 下载邮件附件
- 标记已读/未读
- 删除邮件
- 移动邮件到文件夹

### 邮件服务商支持

已测试支持的服务商：
- **Gmail**：需要启用"应用专用密码"
- **QQ邮箱**：需要获取"授权码"
- **163邮箱**：需要获取"客户端授权密码"
- **Outlook/Hotmail**：支持
- **企业邮箱**：支持自定义SMTP/IMAP服务器

## 脚本说明

### send_mail.py

主要发送邮件脚本，包含以下函数：

```python
def send_email(to, subject, body, cc=None, bcc=None, attachments=None, html=False):
    """
    发送邮件
    
    参数：
    - to: 收件人邮箱（字符串或列表）
    - subject: 邮件主题
    - body: 邮件内容
    - cc: 抄送（可选）
    - bcc: 密送（可选）
    - attachments: 附件路径列表（可选）
    - html: 是否使用HTML格式（默认False）
    """
```

### receive_mail.py

主要接收邮件脚本，包含以下函数：

```python
def fetch_emails(limit=10, search_criteria=None, download_attachments=False):
    """
    获取邮件
    
    参数：
    - limit: 获取邮件数量限制
    - search_criteria: 搜索条件字典
    - download_attachments: 是否下载附件
    
    返回：
    - 邮件列表，每个邮件包含：id, from, to, subject, date, body, attachments
    """
```

### mail_config.py

邮件配置管理：

```python
def get_mail_config():
    """从环境变量获取邮件配置"""
    
def test_mail_connection():
    """测试邮件连接是否正常"""
```

## 使用示例

### 示例1：发送简单邮件

```bash
# 使用命令行发送邮件
python scripts/send_mail.py --to "friend@example.com" --subject "问候" --body "你好，最近怎么样？"
```

### 示例2：发送带附件的邮件

```bash
python scripts/send_mail.py --to "colleague@company.com" \
  --subject "项目报告" \
  --body "请查收项目报告" \
  --attachments "report.pdf" "data.xlsx"
```

### 示例3：获取未读邮件

```bash
python scripts/receive_mail.py --unread --limit 5
```

### 示例4：搜索特定邮件

```bash
python scripts/receive_mail.py --search "from:boss subject:urgent"
```

## 故障排除

### 常见问题

1. **认证失败**
   - 检查用户名密码是否正确
   - Gmail需要"应用专用密码"，不是普通密码
   - QQ邮箱需要"授权码"

2. **连接超时**
   - 检查网络连接
   - 确认防火墙未阻止邮件端口
   - 尝试使用SSL/TLS不同端口

3. **附件过大**
   - 大多数邮件服务商限制25MB
   - 大文件建议使用云存储链接

### 安全建议

1. **不要明文存储密码**
   - 使用环境变量
   - 使用密钥管理服务

2. **启用两步验证**
   - 提高账户安全性

3. **定期更换密码**
   - 特别是应用专用密码

## 高级功能

### 邮件模板

支持使用Jinja2模板发送邮件：

```python
from scripts.mail_templates import send_template_email

send_template_email(
    to="user@example.com",
    template_name="welcome",
    template_vars={"name": "张三", "company": "ABC公司"}
)
```

### 批量发送

```python
from scripts.batch_mail import send_batch_emails

recipients = [
    {"email": "user1@example.com", "name": "用户1"},
    {"email": "user2@example.com", "name": "用户2"},
]

send_batch_emails(
    recipients=recipients,
    subject_template="尊敬的{name}，您好",
    body_template="这是给{name}的定制内容"
)
```

### 邮件调度

可以结合cron技能定时发送邮件：

```bash
# 每天9点发送日报
nanobot cron add --name "daily-report" --cron "0 9 * * *" \
  --command "python scripts/send_mail.py --to 'team@company.com' --subject '每日报告' --body '今日工作汇总...'"
```

## 参考文档

详细配置和API文档请查看：
- [references/gmail_setup.md](references/gmail_setup.md) - Gmail配置指南
- [references/qqmail_setup.md](references/qqmail_setup.md) - QQ邮箱配置指南
- [references/troubleshooting.md](references/troubleshooting.md) - 故障排除指南
- [references/security.md](references/security.md) - 安全最佳实践