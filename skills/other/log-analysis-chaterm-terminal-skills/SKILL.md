---
name: log-analysis
description: 日志分析与处理
version: 1.0.0
author: terminal-skills
tags: [server, log, analysis, grep, awk, monitoring]
---

# 日志分析与处理

## 概述
日志聚合、分析工具、告警配置等技能。

## 日志查看

### 基础命令
```bash
# 实时查看
tail -f /var/log/syslog
tail -f /var/log/nginx/access.log

# 多文件同时查看
tail -f /var/log/nginx/*.log
multitail /var/log/nginx/access.log /var/log/nginx/error.log

# 查看最后N行
tail -n 100 /var/log/syslog

# 查看开头
head -n 100 /var/log/syslog

# 分页查看
less /var/log/syslog
less +F /var/log/syslog             # 类似 tail -f
```

### 按时间过滤
```bash
# 使用 sed 按时间范围
sed -n '/2024-01-15 10:00/,/2024-01-15 11:00/p' /var/log/app.log

# 使用 awk
awk '/2024-01-15 10:/ && /2024-01-15 11:/' /var/log/app.log

# 使用 journalctl
journalctl --since "2024-01-15 10:00" --until "2024-01-15 11:00"
journalctl --since "1 hour ago"
journalctl --since today
```

## 文本搜索

### grep
```bash
# 基础搜索
grep "error" /var/log/syslog
grep -i "error" /var/log/syslog     # 忽略大小写
grep -r "error" /var/log/           # 递归搜索

# 正则表达式
grep -E "error|warning" /var/log/syslog
grep -P "\d{4}-\d{2}-\d{2}" /var/log/syslog  # Perl 正则

# 上下文
grep -A 3 "error" /var/log/syslog   # 后3行
grep -B 3 "error" /var/log/syslog   # 前3行
grep -C 3 "error" /var/log/syslog   # 前后3行

# 统计
grep -c "error" /var/log/syslog     # 计数
grep -l "error" /var/log/*.log      # 只显示文件名

# 排除
grep -v "debug" /var/log/syslog     # 排除包含 debug 的行
```

### ripgrep (rg)
```bash
# 更快的搜索
rg "error" /var/log/
rg -i "error" /var/log/             # 忽略大小写
rg -C 3 "error" /var/log/           # 上下文
rg --type log "error"               # 按文件类型
```

## 文本处理

### awk
```bash
# 打印特定列
awk '{print $1, $4}' /var/log/nginx/access.log

# 条件过滤
awk '$9 == 500' /var/log/nginx/access.log
awk '$9 >= 400 && $9 < 500' /var/log/nginx/access.log

# 统计
awk '{sum += $10} END {print sum}' /var/log/nginx/access.log
awk '{count[$9]++} END {for (c in count) print c, count[c]}' /var/log/nginx/access.log

# 自定义分隔符
awk -F: '{print $1}' /etc/passwd
awk -F'[ :]' '{print $1, $2}' /var/log/syslog
```

### sed
```bash
# 替换
sed 's/old/new/g' file.log
sed -i 's/old/new/g' file.log       # 原地修改

# 删除行
sed '/pattern/d' file.log
sed '1,10d' file.log                # 删除前10行

# 提取行
sed -n '10,20p' file.log            # 打印10-20行
sed -n '/start/,/end/p' file.log    # 打印匹配范围
```

### sort & uniq
```bash
# 排序
sort file.log
sort -r file.log                    # 逆序
sort -n file.log                    # 数字排序
sort -k2 file.log                   # 按第2列排序

# 去重统计
sort file.log | uniq
sort file.log | uniq -c             # 计数
sort file.log | uniq -c | sort -rn  # 按频率排序
```

## Nginx 日志分析

### 常用分析
```bash
# 访问量统计
wc -l /var/log/nginx/access.log

# IP 访问排行
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -20

# 状态码统计
awk '{print $9}' access.log | sort | uniq -c | sort -rn

# URL 访问排行
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -20

# 每小时访问量
awk '{print substr($4,14,2)}' access.log | sort | uniq -c

# 慢请求（响应时间 > 1s）
awk '$NF > 1' access.log | head -20

# 404 错误
awk '$9 == 404 {print $7}' access.log | sort | uniq -c | sort -rn

# 带宽统计
awk '{sum += $10} END {print sum/1024/1024 " MB"}' access.log
```

### GoAccess 实时分析
```bash
# 安装
apt install goaccess

# 实时分析
goaccess /var/log/nginx/access.log -c

# 生成 HTML 报告
goaccess /var/log/nginx/access.log -o report.html --log-format=COMBINED

# 实时 HTML
goaccess /var/log/nginx/access.log -o /var/www/html/report.html --real-time-html
```

## 日志轮转

### logrotate 配置
```bash
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    daily                           # 每天轮转
    rotate 7                        # 保留7个
    compress                        # 压缩
    delaycompress                   # 延迟压缩
    missingok                       # 文件不存在不报错
    notifempty                      # 空文件不轮转
    create 0640 www-data www-data   # 创建新文件
    sharedscripts
    postrotate
        systemctl reload nginx > /dev/null 2>&1 || true
    endscript
}
```

### 手动轮转
```bash
# 测试配置
logrotate -d /etc/logrotate.d/myapp

# 强制轮转
logrotate -f /etc/logrotate.d/myapp
```

## 常见场景

### 场景 1：错误日志分析
```bash
# 统计错误类型
grep -E "ERROR|WARN|FATAL" /var/log/app.log | \
    awk '{print $3}' | sort | uniq -c | sort -rn

# 最近1小时的错误
awk -v date="$(date -d '1 hour ago' '+%Y-%m-%d %H')" \
    '$0 ~ date && /ERROR/' /var/log/app.log
```

### 场景 2：性能分析
```bash
# 响应时间分布
awk '{print int($NF)}' access.log | sort -n | uniq -c | \
    awk '{printf "%ds: %d\n", $2, $1}'

# 慢请求 Top 10
awk '{print $NF, $7}' access.log | sort -rn | head -10
```

### 场景 3：安全分析
```bash
# 失败登录尝试
grep "Failed password" /var/log/auth.log | \
    awk '{print $(NF-3)}' | sort | uniq -c | sort -rn

# 可疑 IP
awk '$9 ~ /4[0-9][0-9]/ {print $1}' access.log | \
    sort | uniq -c | sort -rn | head -20
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 日志太大 | 配置 logrotate、按时间过滤 |
| 搜索慢 | 使用 ripgrep、建立索引 |
| 格式不统一 | 使用 awk 自定义解析 |
| 实时监控 | tail -f、GoAccess |
| 历史分析 | ELK Stack、Loki |
