---
name: rsync
description: rsync 文件同步与备份
version: 1.0.0
author: terminal-skills
tags: [backup, rsync, sync, recovery]
---

# rsync 文件同步与备份

## 概述
rsync 是强大的文件同步工具，支持增量传输、远程同步、备份等场景。

## 基础用法

```bash
# 本地同步
rsync -av source/ dest/

# 远程同步（推送）
rsync -av source/ user@remote:/path/dest/

# 远程同步（拉取）
rsync -av user@remote:/path/source/ dest/

# 常用参数
# -a  归档模式（保留权限、时间等）
# -v  详细输出
# -z  压缩传输
# -P  显示进度 + 断点续传
# -n  模拟运行（dry-run）
```

## 常用参数组合

```bash
# 标准备份
rsync -avz source/ dest/

# 带进度显示
rsync -avzP source/ dest/

# 删除目标多余文件（镜像同步）
rsync -avz --delete source/ dest/

# 排除文件
rsync -avz --exclude='*.log' --exclude='.git' source/ dest/

# 使用排除文件
rsync -avz --exclude-from='exclude.txt' source/ dest/

# 限制带宽（KB/s）
rsync -avz --bwlimit=1000 source/ dest/
```

## 远程同步

```bash
# 通过 SSH（默认）
rsync -avz -e ssh source/ user@host:/path/

# 指定 SSH 端口
rsync -avz -e 'ssh -p 2222' source/ user@host:/path/

# 使用 SSH 密钥
rsync -avz -e 'ssh -i ~/.ssh/key' source/ user@host:/path/

# rsync daemon 模式
rsync -avz source/ rsync://user@host/module/
```

## 备份策略

### 增量备份
```bash
# 使用硬链接实现增量备份
rsync -avz --link-dest=/backup/latest source/ /backup/$(date +%Y%m%d)/

# 更新 latest 链接
ln -snf /backup/$(date +%Y%m%d) /backup/latest
```

### 定时备份脚本
```bash
#!/bin/bash
set -euo pipefail

SOURCE="/data/"
DEST="/backup/"
DATE=$(date +%Y%m%d_%H%M%S)
LATEST="$DEST/latest"
BACKUP="$DEST/$DATE"

# 增量备份
rsync -avz --delete --link-dest="$LATEST" "$SOURCE" "$BACKUP"

# 更新 latest 链接
ln -snf "$BACKUP" "$LATEST"

# 保留最近 7 天
find "$DEST" -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \;
```

## 常见场景

### 场景 1：网站文件同步
```bash
# 同步网站文件，排除缓存和日志
rsync -avz --delete \
  --exclude='cache/' \
  --exclude='*.log' \
  --exclude='uploads/tmp/' \
  /var/www/html/ backup@remote:/backup/www/
```

### 场景 2：数据库备份同步
```bash
# 先导出数据库
mysqldump -u root -p database > /backup/db.sql

# 同步到远程
rsync -avzP /backup/db.sql backup@remote:/backup/mysql/
```

### 场景 3：断点续传大文件
```bash
# 使用 -P 参数支持断点续传
rsync -avzP large_file.tar.gz user@remote:/path/

# 如果中断，重新执行相同命令即可继续
```

## 故障排查

| 问题 | 解决方法 |
|------|----------|
| 权限错误 | 检查目标目录权限，使用 `--chmod` |
| 连接超时 | 检查网络、SSH 配置、防火墙 |
| 空间不足 | 清理目标磁盘，使用 `--max-size` 限制 |
| 同步慢 | 使用 `-z` 压缩，`--bwlimit` 限速 |
| 文件被跳过 | 检查 `--exclude` 规则，使用 `-v` 查看详情 |

## 注意事项

```bash
# 源路径末尾的 / 很重要！
rsync -av source/ dest/   # 同步 source 目录内容到 dest
rsync -av source dest/    # 同步 source 目录本身到 dest/source

# 先用 -n 模拟
rsync -avzn --delete source/ dest/

# 确认无误后执行
rsync -avz --delete source/ dest/
```
