---
name: cron
description: 定时任务管理
version: 1.0.0
author: terminal-skills
tags: [server, cron, crontab, schedule, automation]
---

# 定时任务管理

## 概述
Cron 定时任务配置、日志监控、故障排查等技能。

## Crontab 基础

### 管理命令
```bash
# 编辑当前用户的 crontab
crontab -e

# 查看当前用户的 crontab
crontab -l

# 删除当前用户的 crontab
crontab -r

# 管理其他用户的 crontab（需要 root）
crontab -u username -e
crontab -u username -l
```

### 时间格式
```
┌───────────── 分钟 (0-59)
│ ┌───────────── 小时 (0-23)
│ │ ┌───────────── 日 (1-31)
│ │ │ ┌───────────── 月 (1-12)
│ │ │ │ ┌───────────── 星期 (0-7, 0和7都是周日)
│ │ │ │ │
* * * * * command
```

### 特殊字符
```bash
*       # 任意值
,       # 列表 (1,3,5)
-       # 范围 (1-5)
/       # 步长 (*/5 每5分钟)

# 示例
0 * * * *       # 每小时整点
*/15 * * * *    # 每15分钟
0 9-17 * * *    # 9点到17点每小时
0 0 * * 1-5     # 工作日零点
0 0 1,15 * *    # 每月1号和15号零点
```

### 特殊时间字符串
```bash
@reboot         # 系统启动时
@yearly         # 每年 (0 0 1 1 *)
@monthly        # 每月 (0 0 1 * *)
@weekly         # 每周 (0 0 * * 0)
@daily          # 每天 (0 0 * * *)
@hourly         # 每小时 (0 * * * *)
```

## 配置文件

### 用户 crontab
```bash
# 位置
/var/spool/cron/crontabs/username   # Debian/Ubuntu
/var/spool/cron/username            # CentOS/RHEL

# 格式
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
MAILTO=admin@example.com

# 任务
0 2 * * * /usr/local/bin/backup.sh
```

### 系统 crontab
```bash
# /etc/crontab
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

# 格式：多了用户字段
# 分 时 日 月 周 用户 命令
0 2 * * * root /usr/local/bin/backup.sh
```

### cron.d 目录
```bash
# /etc/cron.d/myapp
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin

0 * * * * appuser /opt/myapp/hourly-task.sh
0 2 * * * root /opt/myapp/daily-backup.sh
```

### 预定义目录
```bash
/etc/cron.hourly/       # 每小时执行
/etc/cron.daily/        # 每天执行
/etc/cron.weekly/       # 每周执行
/etc/cron.monthly/      # 每月执行

# 放入可执行脚本即可
chmod +x /etc/cron.daily/myscript
```

## 最佳实践

### 脚本模板
```bash
#!/bin/bash
# /usr/local/bin/cron-task.sh

# 日志文件
LOG_FILE="/var/log/cron-task.log"

# 锁文件（防止重复执行）
LOCK_FILE="/var/run/cron-task.lock"

# 检查锁
if [ -f "$LOCK_FILE" ]; then
    echo "$(date): Task already running" >> "$LOG_FILE"
    exit 1
fi

# 创建锁
trap "rm -f $LOCK_FILE" EXIT
touch "$LOCK_FILE"

# 记录开始
echo "$(date): Task started" >> "$LOG_FILE"

# 执行任务
/path/to/actual/command >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

# 记录结束
echo "$(date): Task finished with exit code $EXIT_CODE" >> "$LOG_FILE"

exit $EXIT_CODE
```

### Crontab 条目
```bash
# 推荐写法
# 1. 使用绝对路径
# 2. 重定向输出
# 3. 添加注释

# 每日备份 - 凌晨2点
0 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1

# 每5分钟健康检查
*/5 * * * * /usr/local/bin/healthcheck.sh > /dev/null 2>&1

# 每周日志清理 - 周日凌晨3点
0 3 * * 0 /usr/local/bin/cleanup-logs.sh >> /var/log/cleanup.log 2>&1
```

### 环境变量
```bash
# 在 crontab 中设置
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
HOME=/home/user
MAILTO=admin@example.com

# 或在脚本中加载
#!/bin/bash
source /etc/profile
source ~/.bashrc
```

## 日志与监控

### 查看日志
```bash
# 系统日志
grep CRON /var/log/syslog           # Debian/Ubuntu
grep CRON /var/log/cron             # CentOS/RHEL

# 实时监控
tail -f /var/log/syslog | grep CRON

# 查看邮件（如果配置了 MAILTO）
cat /var/mail/username
```

### 调试技巧
```bash
# 手动测试脚本
/usr/local/bin/myscript.sh

# 模拟 cron 环境
env -i /bin/bash --noprofile --norc -c '/usr/local/bin/myscript.sh'

# 检查 cron 服务状态
systemctl status cron               # Debian/Ubuntu
systemctl status crond              # CentOS/RHEL
```

## 常见场景

### 场景 1：数据库备份
```bash
# 每天凌晨2点备份 MySQL
0 2 * * * /usr/bin/mysqldump -u root -p'password' database | gzip > /backup/db_$(date +\%Y\%m\%d).sql.gz

# 注意：% 需要转义为 \%
```

### 场景 2：日志轮转
```bash
# 每天压缩并清理7天前的日志
0 0 * * * find /var/log/myapp -name "*.log" -mtime +7 -delete
0 1 * * * gzip /var/log/myapp/*.log.1
```

### 场景 3：监控告警
```bash
# 每5分钟检查服务状态
*/5 * * * * /usr/local/bin/check-service.sh || /usr/local/bin/send-alert.sh
```

### 场景 4：使用 flock 防止重复
```bash
# 使用 flock 确保单实例运行
*/5 * * * * /usr/bin/flock -n /var/lock/mytask.lock /usr/local/bin/mytask.sh
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 任务不执行 | 检查 cron 服务状态、日志 |
| 权限错误 | 检查脚本权限、用户权限 |
| 环境变量问题 | 在脚本中设置 PATH |
| 命令找不到 | 使用绝对路径 |
| 输出丢失 | 重定向到日志文件 |

```bash
# 检查 cron 服务
systemctl status cron

# 检查用户是否被禁止
cat /etc/cron.allow
cat /etc/cron.deny

# 检查语法
crontab -l | grep -v '^#' | while read line; do
    echo "Checking: $line"
done
```
