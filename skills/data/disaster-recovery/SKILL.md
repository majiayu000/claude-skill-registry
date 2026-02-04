---
name: disaster-recovery
description: 灾难恢复
version: 1.0.0
author: terminal-skills
tags: [backup, disaster-recovery, rto, rpo, failover, ha]
---

# 灾难恢复

## 概述
灾难恢复计划、RTO/RPO、故障切换技能。

## 核心概念

### RTO 与 RPO
```
RPO (Recovery Point Objective)
- 可接受的数据丢失量
- 决定备份频率

RTO (Recovery Time Objective)  
- 可接受的恢复时间
- 决定恢复策略

示例：
- RPO = 1小时 → 每小时备份
- RTO = 4小时 → 需要热备或快速恢复
```

### 恢复策略
```
冷备 (Cold)
- 最低成本
- 最长 RTO
- 适合非关键系统

温备 (Warm)
- 中等成本
- 中等 RTO
- 定期同步数据

热备 (Hot)
- 最高成本
- 最短 RTO
- 实时同步
```

## 数据库恢复

### MySQL 恢复
```bash
# 从备份恢复
mysql -u root -p < full_backup.sql

# 应用 binlog
mysqlbinlog mysql-bin.000001 | mysql -u root -p

# 时间点恢复
mysqlbinlog --stop-datetime="2024-01-15 10:00:00" mysql-bin.* | mysql -u root -p

# 主从切换
# 在从库执行
STOP SLAVE;
RESET SLAVE ALL;
# 应用程序切换连接
```

### PostgreSQL 恢复
```bash
# 从备份恢复
pg_restore -d database backup.dump

# PITR 恢复
# recovery.conf
restore_command = 'cp /archive/%f %p'
recovery_target_time = '2024-01-15 10:00:00'

# 主从切换
pg_ctl promote -D /var/lib/postgresql/data
```

### Redis 恢复
```bash
# 从 RDB 恢复
cp backup.rdb /var/lib/redis/dump.rdb
systemctl restart redis

# 从 AOF 恢复
cp backup.aof /var/lib/redis/appendonly.aof
redis-check-aof --fix appendonly.aof
systemctl restart redis
```

## 系统恢复

### 文件系统恢复
```bash
# 从 tar 备份恢复
tar -xzvf /backup/system.tar.gz -C /

# 从 rsync 备份恢复
rsync -avz /backup/system/ /

# 恢复权限
restorecon -Rv /
```

### 引导修复
```bash
# 进入救援模式
# 挂载根分区
mount /dev/sda1 /mnt
mount --bind /dev /mnt/dev
mount --bind /proc /mnt/proc
mount --bind /sys /mnt/sys
chroot /mnt

# 修复 GRUB
grub-install /dev/sda
update-grub
```

## 故障切换

### Keepalived 切换
```bash
# 检查状态
systemctl status keepalived
ip addr show | grep -w inet

# 手动切换
# 降低主节点优先级
# /etc/keepalived/keepalived.conf
vrrp_instance VI_1 {
    priority 50  # 降低
}
systemctl reload keepalived
```

### DNS 切换
```bash
# 修改 DNS 记录
# 降低 TTL（提前）
# 切换 A 记录指向备用 IP

# 验证
dig +short example.com
nslookup example.com
```

## 常见场景

### 场景 1：完整恢复流程
```bash
#!/bin/bash
# 1. 评估损失
echo "检查系统状态..."

# 2. 通知相关人员
# send_alert "开始灾难恢复"

# 3. 恢复基础设施
echo "恢复网络配置..."

# 4. 恢复数据
echo "恢复数据库..."
mysql -u root -p < /backup/latest.sql

# 5. 恢复应用
echo "启动应用服务..."
systemctl start application

# 6. 验证
echo "验证服务状态..."
curl -s http://localhost/health

# 7. 通知恢复完成
# send_alert "灾难恢复完成"
```

### 场景 2：DR 演练
```bash
#!/bin/bash
# DR 演练脚本
LOG="/var/log/dr-drill.log"

echo "$(date): 开始 DR 演练" >> $LOG

# 1. 切换到备用站点
echo "切换 DNS..." >> $LOG

# 2. 验证服务
echo "验证服务可用性..." >> $LOG
curl -s http://dr-site/health >> $LOG

# 3. 测试数据一致性
echo "验证数据一致性..." >> $LOG

# 4. 记录 RTO
echo "实际 RTO: $(计算时间)" >> $LOG

# 5. 切回主站点
echo "切回主站点..." >> $LOG
```

### 场景 3：自动故障转移
```bash
# Keepalived 配置
vrrp_script chk_app {
    script "/usr/local/bin/check_app.sh"
    interval 2
    weight -20
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 100
    
    track_script {
        chk_app
    }
    
    virtual_ipaddress {
        192.168.1.100
    }
}
```

## DR 检查清单

| 项目 | 检查内容 |
|------|----------|
| 备份 | 备份完整性、可恢复性 |
| 文档 | 恢复步骤、联系人 |
| 网络 | DNS、IP、防火墙 |
| 数据 | 数据一致性、同步状态 |
| 应用 | 配置、依赖、证书 |

## 故障排查

```bash
# 检查备份状态
ls -la /backup/
md5sum /backup/latest.tar.gz

# 检查复制状态
# MySQL
SHOW SLAVE STATUS\G

# PostgreSQL
SELECT * FROM pg_stat_replication;

# 检查网络连通性
ping dr-site
traceroute dr-site
```
