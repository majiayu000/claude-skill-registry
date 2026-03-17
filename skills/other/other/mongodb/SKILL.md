---
name: mongodb
description: MongoDB 数据库管理
version: 1.0.0
author: terminal-skills
tags: [database, mongodb, nosql, document]
---

# MongoDB 数据库管理

## 概述
MongoDB 操作、索引优化、分片集群等技能。

## 连接管理

```bash
# 本地连接
mongosh
mongosh --port 27017

# 远程连接
mongosh "mongodb://hostname:27017"
mongosh "mongodb://user:password@hostname:27017/database"

# 副本集连接
mongosh "mongodb://host1:27017,host2:27017,host3:27017/database?replicaSet=rs0"

# 执行脚本
mongosh script.js
mongosh --eval "db.collection.find()"
```

## 基础操作

### 数据库操作
```javascript
// 显示数据库
show dbs

// 切换/创建数据库
use mydb

// 删除数据库
db.dropDatabase()

// 数据库统计
db.stats()
```

### 集合操作
```javascript
// 显示集合
show collections

// 创建集合
db.createCollection("users")

// 删除集合
db.users.drop()

// 集合统计
db.users.stats()
```

### CRUD 操作
```javascript
// 插入
db.users.insertOne({ name: "John", age: 30 })
db.users.insertMany([{ name: "Jane" }, { name: "Bob" }])

// 查询
db.users.find()
db.users.find({ age: { $gt: 25 } })
db.users.findOne({ name: "John" })
db.users.find().limit(10).skip(20).sort({ age: -1 })

// 更新
db.users.updateOne({ name: "John" }, { $set: { age: 31 } })
db.users.updateMany({ age: { $lt: 18 } }, { $set: { status: "minor" } })
db.users.replaceOne({ name: "John" }, { name: "John", age: 32 })

// 删除
db.users.deleteOne({ name: "John" })
db.users.deleteMany({ status: "inactive" })
```

## 索引管理

```javascript
// 查看索引
db.users.getIndexes()

// 创建索引
db.users.createIndex({ email: 1 })                    // 升序
db.users.createIndex({ name: 1, age: -1 })            // 复合索引
db.users.createIndex({ email: 1 }, { unique: true })  // 唯一索引
db.users.createIndex({ location: "2dsphere" })        // 地理索引
db.users.createIndex({ content: "text" })             // 文本索引

// 后台创建（不阻塞）
db.users.createIndex({ field: 1 }, { background: true })

// 删除索引
db.users.dropIndex("email_1")
db.users.dropIndexes()                                // 删除所有

// 索引使用分析
db.users.find({ email: "test@example.com" }).explain("executionStats")
```

## 聚合操作

```javascript
// 基础聚合
db.orders.aggregate([
    { $match: { status: "completed" } },
    { $group: { _id: "$customer", total: { $sum: "$amount" } } },
    { $sort: { total: -1 } },
    { $limit: 10 }
])

// 常用聚合操作符
// $match - 过滤
// $group - 分组
// $sort - 排序
// $limit - 限制
// $skip - 跳过
// $project - 投影
// $unwind - 展开数组
// $lookup - 关联查询

// 关联查询
db.orders.aggregate([
    {
        $lookup: {
            from: "users",
            localField: "userId",
            foreignField: "_id",
            as: "user"
        }
    }
])
```

## 备份与恢复

```bash
# 备份数据库
mongodump --db mydb --out /backup/
mongodump --uri="mongodb://user:pass@host:27017/mydb" --out /backup/

# 备份集合
mongodump --db mydb --collection users --out /backup/

# 压缩备份
mongodump --db mydb --gzip --archive=/backup/mydb.gz

# 恢复
mongorestore --db mydb /backup/mydb/
mongorestore --uri="mongodb://user:pass@host:27017" /backup/

# 恢复压缩备份
mongorestore --gzip --archive=/backup/mydb.gz

# 导出 JSON
mongoexport --db mydb --collection users --out users.json

# 导入 JSON
mongoimport --db mydb --collection users --file users.json
```

## 副本集管理

```javascript
// 查看副本集状态
rs.status()
rs.conf()

// 初始化副本集
rs.initiate({
    _id: "rs0",
    members: [
        { _id: 0, host: "mongo1:27017" },
        { _id: 1, host: "mongo2:27017" },
        { _id: 2, host: "mongo3:27017" }
    ]
})

// 添加成员
rs.add("mongo4:27017")
rs.addArb("arbiter:27017")          // 添加仲裁节点

// 移除成员
rs.remove("mongo4:27017")

// 强制主节点切换
rs.stepDown()
```

## 性能监控

```javascript
// 服务器状态
db.serverStatus()

// 当前操作
db.currentOp()
db.currentOp({ "active": true, "secs_running": { "$gt": 5 } })

// 终止操作
db.killOp(opid)

// 慢查询日志
db.setProfilingLevel(1, { slowms: 100 })
db.system.profile.find().sort({ ts: -1 }).limit(10)

// 集合扫描统计
db.users.stats()

// 连接数
db.serverStatus().connections
```

## 常见场景

### 场景 1：查询优化
```javascript
// 分析查询
db.users.find({ email: "test@example.com" }).explain("executionStats")

// 检查是否使用索引
// "stage": "IXSCAN" 表示使用索引
// "stage": "COLLSCAN" 表示全表扫描

// 强制使用索引
db.users.find({ name: "John" }).hint({ name: 1 })
```

### 场景 2：数据迁移
```javascript
// 复制集合
db.source.aggregate([{ $out: "target" }])

// 跨数据库复制
db.source.find().forEach(function(doc) {
    db.getSiblingDB("otherdb").target.insert(doc)
})
```

### 场景 3：批量更新
```javascript
// 批量更新
db.users.updateMany(
    { status: "pending" },
    { $set: { status: "active", updatedAt: new Date() } }
)

// 使用 bulkWrite
db.users.bulkWrite([
    { updateOne: { filter: { _id: 1 }, update: { $set: { x: 1 } } } },
    { updateOne: { filter: { _id: 2 }, update: { $set: { x: 2 } } } },
    { deleteOne: { filter: { _id: 3 } } }
])
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 查询慢 | `explain()`, 检查索引 |
| 连接数过多 | `db.serverStatus().connections` |
| 内存不足 | 检查 WiredTiger 缓存配置 |
| 副本集同步延迟 | `rs.status()`, 检查 oplog |
| 磁盘空间 | `db.stats()`, compact 操作 |
