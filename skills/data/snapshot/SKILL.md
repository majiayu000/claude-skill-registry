---
name: snapshot
description: 快照管理
version: 1.0.0
author: terminal-skills
tags: [backup, snapshot, lvm, btrfs, zfs, cloud]
---

# 快照管理

## 概述
LVM 快照、文件系统快照、云快照管理技能。

## LVM 快照

### 创建快照
```bash
# 查看逻辑卷
lvs
lvdisplay

# 创建快照
lvcreate -L 10G -s -n snap_data /dev/vg0/data

# 创建薄快照
lvcreate -s -n snap_data /dev/vg0/thin_data

# 查看快照
lvs -a
lvdisplay /dev/vg0/snap_data
```

### 挂载快照
```bash
# 挂载只读
mount -o ro /dev/vg0/snap_data /mnt/snapshot

# 挂载读写
mount /dev/vg0/snap_data /mnt/snapshot
```

### 恢复数据
```bash
# 从快照恢复
lvconvert --merge /dev/vg0/snap_data

# 恢复前需卸载原卷
umount /dev/vg0/data
lvconvert --merge /dev/vg0/snap_data
mount /dev/vg0/data /data
```

### 删除快照
```bash
# 卸载并删除
umount /mnt/snapshot
lvremove /dev/vg0/snap_data
```

## Btrfs 快照

### 创建快照
```bash
# 创建只读快照
btrfs subvolume snapshot -r /data /snapshots/data_$(date +%Y%m%d)

# 创建可写快照
btrfs subvolume snapshot /data /snapshots/data_writable

# 查看子卷
btrfs subvolume list /
```

### 管理快照
```bash
# 删除快照
btrfs subvolume delete /snapshots/data_20240101

# 发送快照（备份）
btrfs send /snapshots/data_readonly | btrfs receive /backup/

# 增量发送
btrfs send -p /snapshots/old /snapshots/new | btrfs receive /backup/
```

## ZFS 快照

### 创建快照
```bash
# 创建快照
zfs snapshot pool/dataset@snap_$(date +%Y%m%d)

# 递归创建
zfs snapshot -r pool/dataset@snap_name

# 查看快照
zfs list -t snapshot
```

### 管理快照
```bash
# 回滚
zfs rollback pool/dataset@snap_name

# 克隆
zfs clone pool/dataset@snap_name pool/clone_dataset

# 删除
zfs destroy pool/dataset@snap_name

# 发送/接收
zfs send pool/dataset@snap | zfs receive backup/dataset
```

## 云快照

### AWS EBS
```bash
# 创建快照
aws ec2 create-snapshot \
    --volume-id vol-1234567890abcdef0 \
    --description "Backup $(date +%Y%m%d)"

# 查看快照
aws ec2 describe-snapshots --owner-ids self

# 从快照创建卷
aws ec2 create-volume \
    --snapshot-id snap-1234567890abcdef0 \
    --availability-zone us-east-1a

# 删除快照
aws ec2 delete-snapshot --snapshot-id snap-1234567890abcdef0
```

### 阿里云
```bash
# 创建快照
aliyun ecs CreateSnapshot --DiskId d-xxx --SnapshotName backup

# 查看快照
aliyun ecs DescribeSnapshots

# 删除快照
aliyun ecs DeleteSnapshot --SnapshotId s-xxx
```

## 常见场景

### 场景 1：数据库一致性快照
```bash
#!/bin/bash
# MySQL + LVM 快照
mysql -e "FLUSH TABLES WITH READ LOCK;"
lvcreate -L 10G -s -n db_snap /dev/vg0/mysql_data
mysql -e "UNLOCK TABLES;"

# 备份快照
mount -o ro /dev/vg0/db_snap /mnt/snap
tar -czvf /backup/mysql_$(date +%Y%m%d).tar.gz /mnt/snap
umount /mnt/snap
lvremove -f /dev/vg0/db_snap
```

### 场景 2：自动快照脚本
```bash
#!/bin/bash
# Btrfs 自动快照
SNAP_DIR="/snapshots"
MAX_SNAPS=7

# 创建快照
btrfs subvolume snapshot -r /data ${SNAP_DIR}/data_$(date +%Y%m%d_%H%M)

# 清理旧快照
ls -1d ${SNAP_DIR}/data_* | head -n -${MAX_SNAPS} | xargs -r btrfs subvolume delete
```

### 场景 3：快照前后钩子
```bash
#!/bin/bash
# 快照前
systemctl stop application
sync

# 创建快照
lvcreate -L 5G -s -n app_snap /dev/vg0/app_data

# 快照后
systemctl start application
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 快照空间满 | 扩展快照、减少变更 |
| 快照失效 | 检查 COW 空间 |
| 恢复失败 | 检查卷状态、依赖 |
| 性能下降 | 减少快照数量 |

```bash
# LVM 快照状态
lvs -a -o +snap_percent

# Btrfs 空间
btrfs filesystem df /
btrfs filesystem usage /

# ZFS 空间
zfs list -o space
```
