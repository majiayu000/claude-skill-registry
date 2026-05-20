---
name: cloud-backup
description: 云备份方案
version: 1.0.0
author: terminal-skills
tags: [backup, cloud, s3, oss, azure-blob, lifecycle]
---

# 云备份方案

## 概述
S3/OSS 备份、跨区域复制、生命周期管理技能。

## AWS S3 备份

### 基础操作
```bash
# 上传文件
aws s3 cp backup.tar.gz s3://my-bucket/backups/

# 上传目录
aws s3 sync /backup s3://my-bucket/backups/

# 下载
aws s3 cp s3://my-bucket/backups/backup.tar.gz ./
aws s3 sync s3://my-bucket/backups/ /restore/

# 列出文件
aws s3 ls s3://my-bucket/backups/
aws s3 ls s3://my-bucket/backups/ --recursive
```

### 高级选项
```bash
# 排除文件
aws s3 sync /backup s3://my-bucket/ --exclude "*.log"

# 存储类型
aws s3 cp backup.tar.gz s3://my-bucket/ --storage-class STANDARD_IA
aws s3 cp backup.tar.gz s3://my-bucket/ --storage-class GLACIER

# 服务端加密
aws s3 cp backup.tar.gz s3://my-bucket/ --sse AES256
aws s3 cp backup.tar.gz s3://my-bucket/ --sse aws:kms --sse-kms-key-id alias/my-key

# 多部分上传
aws s3 cp large-file.tar.gz s3://my-bucket/ --expected-size 10737418240
```

### 生命周期策略
```json
{
  "Rules": [
    {
      "ID": "BackupLifecycle",
      "Status": "Enabled",
      "Filter": {"Prefix": "backups/"},
      "Transitions": [
        {"Days": 30, "StorageClass": "STANDARD_IA"},
        {"Days": 90, "StorageClass": "GLACIER"}
      ],
      "Expiration": {"Days": 365}
    }
  ]
}
```

```bash
# 应用策略
aws s3api put-bucket-lifecycle-configuration \
    --bucket my-bucket \
    --lifecycle-configuration file://lifecycle.json
```

### 跨区域复制
```bash
# 启用版本控制
aws s3api put-bucket-versioning \
    --bucket source-bucket \
    --versioning-configuration Status=Enabled

# 配置复制规则
aws s3api put-bucket-replication \
    --bucket source-bucket \
    --replication-configuration file://replication.json
```

## 阿里云 OSS 备份

### 基础操作
```bash
# 上传
ossutil cp backup.tar.gz oss://my-bucket/backups/
ossutil cp -r /backup oss://my-bucket/backups/

# 下载
ossutil cp oss://my-bucket/backups/backup.tar.gz ./

# 同步
ossutil sync /backup oss://my-bucket/backups/

# 列出
ossutil ls oss://my-bucket/backups/
```

### 存储类型
```bash
# 低频访问
ossutil cp backup.tar.gz oss://my-bucket/ --meta x-oss-storage-class:IA

# 归档
ossutil cp backup.tar.gz oss://my-bucket/ --meta x-oss-storage-class:Archive
```

## Azure Blob 备份

### 基础操作
```bash
# 上传
az storage blob upload \
    --account-name myaccount \
    --container-name backups \
    --name backup.tar.gz \
    --file backup.tar.gz

# 下载
az storage blob download \
    --account-name myaccount \
    --container-name backups \
    --name backup.tar.gz \
    --file backup.tar.gz

# 同步
azcopy sync /backup "https://myaccount.blob.core.windows.net/backups"
```

## rclone 通用工具

### 配置
```bash
# 交互式配置
rclone config

# 配置文件 ~/.config/rclone/rclone.conf
[s3]
type = s3
provider = AWS
access_key_id = xxx
secret_access_key = xxx
region = us-east-1

[oss]
type = s3
provider = Alibaba
access_key_id = xxx
secret_access_key = xxx
endpoint = oss-cn-hangzhou.aliyuncs.com
```

### 操作
```bash
# 同步
rclone sync /backup s3:my-bucket/backups

# 复制
rclone copy /backup s3:my-bucket/backups

# 加密备份
rclone sync /backup crypt:backups
```

## 常见场景

### 场景 1：自动备份脚本
```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR="/backup"
S3_BUCKET="s3://my-bucket/backups"

# 创建备份
tar -czvf ${BACKUP_DIR}/backup_${DATE}.tar.gz /data

# 上传到 S3
aws s3 cp ${BACKUP_DIR}/backup_${DATE}.tar.gz ${S3_BUCKET}/

# 清理本地
find ${BACKUP_DIR} -name "backup_*.tar.gz" -mtime +7 -delete

# 验证
aws s3 ls ${S3_BUCKET}/backup_${DATE}.tar.gz
```

### 场景 2：数据库云备份
```bash
#!/bin/bash
# MySQL 备份到 S3
mysqldump -u root -p database | gzip | \
    aws s3 cp - s3://my-bucket/mysql/backup_$(date +%Y%m%d).sql.gz

# PostgreSQL 备份到 S3
pg_dump database | gzip | \
    aws s3 cp - s3://my-bucket/postgres/backup_$(date +%Y%m%d).sql.gz
```

### 场景 3：增量同步
```bash
#!/bin/bash
# 使用 aws s3 sync 增量同步
aws s3 sync /data s3://my-bucket/data/ \
    --exclude "*.tmp" \
    --delete

# 使用 rclone
rclone sync /data remote:bucket/data --progress
```

### 场景 4：灾备复制
```bash
# 跨区域复制配置
{
  "Role": "arn:aws:iam::account:role/replication-role",
  "Rules": [{
    "Status": "Enabled",
    "Priority": 1,
    "Filter": {},
    "Destination": {
      "Bucket": "arn:aws:s3:::dest-bucket",
      "StorageClass": "STANDARD_IA"
    }
  }]
}
```

## 成本优化

| 存储类型 | 适用场景 | 成本 |
|----------|----------|------|
| Standard | 频繁访问 | 高 |
| IA | 月访问 | 中 |
| Glacier | 年访问 | 低 |
| Deep Archive | 归档 | 最低 |

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 上传失败 | 检查权限、网络、大小限制 |
| 同步慢 | 使用多线程、分片上传 |
| 成本高 | 检查存储类型、生命周期 |
| 恢复慢 | Glacier 需要先解冻 |

```bash
# 检查 S3 权限
aws s3api get-bucket-policy --bucket my-bucket

# 检查上传状态
aws s3api list-multipart-uploads --bucket my-bucket

# Glacier 解冻
aws s3api restore-object \
    --bucket my-bucket \
    --key backups/archive.tar.gz \
    --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Standard"}}'
```
