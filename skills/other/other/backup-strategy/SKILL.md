---
name: backup-strategy
description: 备份策略设计
version: 1.0.0
author: terminal-skills
tags: [backup, strategy, 3-2-1, retention, verification]
---

# 备份策略设计

## 概述
3-2-1 策略、备份验证、保留策略设计技能。

## 3-2-1 备份策略

### 核心原则
```
3 - 至少保留 3 份数据副本
2 - 存储在 2 种不同介质上
1 - 至少 1 份异地存储

扩展 3-2-1-1-0：
3 份副本
2 种介质
1 份异地
1 份离线/不可变
0 个错误（验证通过）
```

### 实施示例
```bash
# 本地备份（副本 1）
tar -czvf /backup/local/data_$(date +%Y%m%d).tar.gz /data

# NAS 备份（副本 2，不同介质）
rsync -avz /backup/local/ nas:/backup/

# 云备份（副本 3，异地）
aws s3 sync /backup/local/ s3://backup-bucket/
```

## 备份类型

### 完整备份
```bash
# 每周完整备份
tar -czvf /backup/full_$(date +%Y%m%d).tar.gz /data
```

### 增量备份
```bash
# 基于时间戳
tar -czvf /backup/incr_$(date +%Y%m%d).tar.gz \
    --newer-mtime="1 day ago" /data

# 基于快照文件
tar -czvf /backup/incr.tar.gz -g /backup/snapshot.snar /data
```

### 差异备份
```bash
# 基于完整备份时间
tar -czvf /backup/diff_$(date +%Y%m%d).tar.gz \
    --newer-mtime="$(cat /backup/last_full_date)" /data
```

## 保留策略

### GFS 策略
```bash
# Grandfather-Father-Son
# 日备份：保留 7 天
# 周备份：保留 4 周
# 月备份：保留 12 个月
# 年备份：保留 7 年

#!/bin/bash
BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d)
DOW=$(date +%u)  # 1-7
DOM=$(date +%d)  # 01-31

# 日备份
tar -czvf ${BACKUP_DIR}/daily/backup_${DATE}.tar.gz /data

# 周备份（周日）
if [ "$DOW" -eq 7 ]; then
    cp ${BACKUP_DIR}/daily/backup_${DATE}.tar.gz ${BACKUP_DIR}/weekly/
fi

# 月备份（1号）
if [ "$DOM" -eq "01" ]; then
    cp ${BACKUP_DIR}/daily/backup_${DATE}.tar.gz ${BACKUP_DIR}/monthly/
fi

# 清理
find ${BACKUP_DIR}/daily -mtime +7 -delete
find ${BACKUP_DIR}/weekly -mtime +28 -delete
find ${BACKUP_DIR}/monthly -mtime +365 -delete
```

### 滚动保留
```bash
#!/bin/bash
# 保留最近 N 个备份
BACKUP_DIR="/backup"
KEEP=10

ls -1t ${BACKUP_DIR}/*.tar.gz | tail -n +$((KEEP+1)) | xargs -r rm
```

## 备份验证

### 完整性检查
```bash
# 校验和验证
md5sum backup.tar.gz > backup.md5
md5sum -c backup.md5

# tar 测试
tar -tzvf backup.tar.gz > /dev/null

# gzip 测试
gzip -t backup.tar.gz
```

### 恢复测试
```bash
#!/bin/bash
# 定期恢复测试
TEST_DIR="/tmp/restore_test"
mkdir -p $TEST_DIR

# 解压测试
tar -xzvf /backup/latest.tar.gz -C $TEST_DIR

# 验证文件数量
ORIG_COUNT=$(find /data -type f | wc -l)
REST_COUNT=$(find $TEST_DIR -type f | wc -l)

if [ "$ORIG_COUNT" -eq "$REST_COUNT" ]; then
    echo "验证通过"
else
    echo "验证失败：文件数量不匹配"
fi

rm -rf $TEST_DIR
```

## 常见场景

### 场景 1：企业备份方案
```bash
#!/bin/bash
# 综合备份脚本
CONFIG="/etc/backup/config"
LOG="/var/log/backup.log"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> $LOG; }

# 数据库备份
log "开始数据库备份"
mysqldump --all-databases | gzip > /backup/db_$(date +%Y%m%d).sql.gz

# 文件备份
log "开始文件备份"
tar -czvf /backup/files_$(date +%Y%m%d).tar.gz /data

# 同步到 NAS
log "同步到 NAS"
rsync -avz /backup/ nas:/backup/

# 上传到云
log "上传到云存储"
aws s3 sync /backup/ s3://backup-bucket/

# 验证
log "验证备份"
gzip -t /backup/*.gz

# 清理
log "清理旧备份"
find /backup -mtime +7 -delete

log "备份完成"
```

### 场景 2：备份监控
```bash
#!/bin/bash
# 检查备份状态
BACKUP_DIR="/backup"
MAX_AGE=86400  # 24小时

LATEST=$(ls -1t ${BACKUP_DIR}/*.tar.gz 2>/dev/null | head -1)

if [ -z "$LATEST" ]; then
    echo "CRITICAL: 无备份文件"
    exit 2
fi

AGE=$(($(date +%s) - $(stat -c %Y "$LATEST")))

if [ $AGE -gt $MAX_AGE ]; then
    echo "WARNING: 备份超过 24 小时"
    exit 1
fi

echo "OK: 最新备份 $(basename $LATEST)"
exit 0
```

## 策略对比

| 策略 | 存储空间 | 恢复速度 | 复杂度 |
|------|----------|----------|--------|
| 完整 | 高 | 快 | 低 |
| 增量 | 低 | 慢 | 高 |
| 差异 | 中 | 中 | 中 |
| GFS | 中 | 中 | 中 |

## 最佳实践

```
1. 自动化备份，避免人工遗漏
2. 定期验证备份可恢复性
3. 加密敏感数据备份
4. 监控备份状态和空间
5. 文档化恢复流程
6. 定期演练恢复过程
```
