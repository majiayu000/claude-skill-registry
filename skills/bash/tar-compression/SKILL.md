---
name: tar-compression
description: 归档与压缩
version: 1.0.0
author: terminal-skills
tags: [backup, tar, gzip, xz, compression, archive]
---

# 归档与压缩

## 概述
tar/gzip/xz 归档压缩、分卷备份技能。

## tar 基础

### 创建归档
```bash
# 创建 tar 归档
tar -cvf archive.tar /path/to/dir

# 创建并 gzip 压缩
tar -czvf archive.tar.gz /path/to/dir

# 创建并 bzip2 压缩
tar -cjvf archive.tar.bz2 /path/to/dir

# 创建并 xz 压缩
tar -cJvf archive.tar.xz /path/to/dir

# 多个目录/文件
tar -czvf archive.tar.gz dir1 dir2 file1.txt
```

### 解压归档
```bash
# 解压 tar
tar -xvf archive.tar

# 解压 gzip
tar -xzvf archive.tar.gz

# 解压 bzip2
tar -xjvf archive.tar.bz2

# 解压 xz
tar -xJvf archive.tar.xz

# 解压到指定目录
tar -xzvf archive.tar.gz -C /target/dir
```

### 查看内容
```bash
# 列出内容
tar -tvf archive.tar
tar -tzvf archive.tar.gz

# 搜索文件
tar -tzvf archive.tar.gz | grep "filename"
```

### 常用选项
```bash
# 排除文件/目录
tar -czvf archive.tar.gz --exclude='*.log' --exclude='cache' /path

# 从文件读取排除列表
tar -czvf archive.tar.gz --exclude-from=exclude.txt /path

# 保留权限
tar -czvf archive.tar.gz --preserve-permissions /path

# 增量备份
tar -czvf archive.tar.gz --newer='2024-01-01' /path
```

## 压缩工具

### gzip
```bash
# 压缩
gzip file.txt              # 生成 file.txt.gz，删除原文件
gzip -k file.txt           # 保留原文件
gzip -9 file.txt           # 最高压缩率

# 解压
gunzip file.txt.gz
gzip -d file.txt.gz

# 查看压缩文件
zcat file.txt.gz
zless file.txt.gz
zgrep "pattern" file.txt.gz
```

### bzip2
```bash
# 压缩
bzip2 file.txt
bzip2 -k file.txt          # 保留原文件
bzip2 -9 file.txt          # 最高压缩率

# 解压
bunzip2 file.txt.bz2
bzip2 -d file.txt.bz2

# 查看
bzcat file.txt.bz2
```

### xz
```bash
# 压缩
xz file.txt
xz -k file.txt             # 保留原文件
xz -9 file.txt             # 最高压缩率
xz -T 4 file.txt           # 多线程

# 解压
unxz file.txt.xz
xz -d file.txt.xz

# 查看
xzcat file.txt.xz
```

### zstd
```bash
# 压缩
zstd file.txt
zstd -19 file.txt          # 最高压缩率
zstd -T0 file.txt          # 自动多线程

# 解压
unzstd file.txt.zst
zstd -d file.txt.zst
```

## 分卷备份

### split 分割
```bash
# 按大小分割
split -b 100M archive.tar.gz archive.tar.gz.part_

# 按行分割
split -l 10000 largefile.txt part_

# 合并
cat archive.tar.gz.part_* > archive.tar.gz
```

### tar 分卷
```bash
# 创建分卷
tar -czvf - /path/to/dir | split -b 100M - backup.tar.gz.part_

# 解压分卷
cat backup.tar.gz.part_* | tar -xzvf -
```

## 常见场景

### 场景 1：网站备份
```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR="/backup"
WEB_DIR="/var/www/html"

# 创建备份
tar -czvf ${BACKUP_DIR}/web_${DATE}.tar.gz \
    --exclude='*.log' \
    --exclude='cache/*' \
    ${WEB_DIR}

# 保留最近 7 天
find ${BACKUP_DIR} -name "web_*.tar.gz" -mtime +7 -delete
```

### 场景 2：数据库备份压缩
```bash
# MySQL
mysqldump -u root -p database | gzip > db_backup.sql.gz

# 解压恢复
gunzip < db_backup.sql.gz | mysql -u root -p database

# PostgreSQL
pg_dump database | xz > db_backup.sql.xz
```

### 场景 3：增量备份
```bash
#!/bin/bash
SNAPSHOT="/backup/snapshot.snar"
BACKUP_DIR="/backup"
SOURCE="/data"

# 完整备份（首次）
tar -czvf ${BACKUP_DIR}/full.tar.gz -g ${SNAPSHOT} ${SOURCE}

# 增量备份
tar -czvf ${BACKUP_DIR}/incr_$(date +%Y%m%d).tar.gz -g ${SNAPSHOT} ${SOURCE}
```

### 场景 4：远程备份
```bash
# 本地压缩后传输
tar -czvf - /path/to/dir | ssh user@remote "cat > /backup/archive.tar.gz"

# 远程压缩
ssh user@remote "tar -czvf - /path/to/dir" > local_backup.tar.gz
```

## 压缩对比

| 格式 | 压缩率 | 速度 | 内存 | 适用场景 |
|------|--------|------|------|----------|
| gzip | 中 | 快 | 低 | 日常备份 |
| bzip2 | 高 | 慢 | 中 | 归档存储 |
| xz | 最高 | 最慢 | 高 | 长期存储 |
| zstd | 高 | 快 | 中 | 现代备份 |

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 解压失败 | 检查文件完整性、格式 |
| 空间不足 | 使用管道、分卷 |
| 权限丢失 | 使用 --preserve-permissions |
| 文件损坏 | 使用 gzip -t 测试 |

```bash
# 测试压缩文件
gzip -t file.gz
bzip2 -t file.bz2
xz -t file.xz

# 修复损坏的 gzip
gzrecover file.gz

# 查看压缩信息
gzip -l file.gz
```
