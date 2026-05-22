---
name: database-replication-setup
description: Эксперт DB replication. Используй для настройки репликации MySQL, PostgreSQL, MongoDB, failover и high availability.
---

# Database Replication Expert

Эксперт по системам репликации баз данных с глубокими знаниями архитектур репликации master-slave, master-master и кластерных решений.

## Основные принципы репликации

### Типы репликации
- **Асинхронная**: Высокая производительность, возможная потеря данных при сбоях
- **Синхронная**: Гарантия консистентности данных, повышенная задержка
- **Полусинхронная**: Баланс между производительностью и консистентностью
- **Master-Slave**: Масштабирование чтения, резервное копирование
- **Master-Master**: Географическое распределение, высокая доступность

## Настройка репликации MySQL

### Конфигурация Master
```sql
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog-format = ROW
sync_binlog = 1

CREATE USER 'repl_user'@'%' IDENTIFIED BY 'secure_password';
GRANT REPLICATION SLAVE ON *.* TO 'repl_user'@'%';
```

### Конфигурация Slave
```sql
[mysqld]
server-id = 2
relay-log = relay-bin
read_only = 1

CHANGE MASTER TO
    MASTER_HOST='master-server',
    MASTER_USER='repl_user',
    MASTER_PASSWORD='secure_password',
    MASTER_LOG_FILE='mysql-bin.000001',
    MASTER_LOG_POS=154;

START SLAVE;
```

## Потоковая репликация PostgreSQL

### Основной сервер
```bash
# postgresql.conf
wal_level = replica
max_wal_senders = 3
max_replication_slots = 3
```

```sql
CREATE USER repl_user REPLICATION LOGIN PASSWORD 'secure_password';
```

### Резервный сервер
```bash
pg_basebackup -h primary-server -D /var/lib/postgresql/main -U repl_user -v -P

# postgresql.conf
primary_conninfo = 'host=primary-server port=5432 user=repl_user password=secure_password'
```

## MongoDB Replica Set

```javascript
rs.initiate({
  _id: "myReplicaSet",
  members: [
    { _id: 0, host: "mongo1:27017", priority: 2 },
    { _id: 1, host: "mongo2:27017", priority: 1 },
    { _id: 2, host: "mongo3:27017", arbiterOnly: true }
  ]
});
```

## Мониторинг репликации

### MySQL
```bash
SHOW SLAVE STATUS\G;
# Проверка: Slave_IO_Running, Slave_SQL_Running, Seconds_Behind_Master
```

### PostgreSQL
```sql
SELECT client_addr, state, sent_lsn, replay_lsn,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS lag_bytes
FROM pg_stat_replication;
```

## Стратегии Failover

### Автоматическое переключение с HAProxy
```bash
listen mysql-cluster
    bind *:3306
    option mysql-check user haproxy_check
    server mysql-1 mysql1:3306 check weight 1
    server mysql-2 mysql2:3306 check weight 1 backup
```

## Лучшие практики

- Используйте SSL/TLS для трафика репликации
- Мониторьте задержку репликации
- Тестируйте процедуры failover регулярно
- Документируйте процедуры восстановления
