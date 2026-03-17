---
name: elasticsearch
description: Elasticsearch 集群管理
version: 1.0.0
author: terminal-skills
tags: [database, elasticsearch, search, elk, nosql]
---

# Elasticsearch 集群管理

## 概述
Elasticsearch 索引管理、查询 DSL、集群运维等技能。

## 集群管理

### 集群状态
```bash
# 集群健康
curl -X GET "localhost:9200/_cluster/health?pretty"

# 集群状态
curl -X GET "localhost:9200/_cluster/state?pretty"

# 集群统计
curl -X GET "localhost:9200/_cluster/stats?pretty"

# 节点信息
curl -X GET "localhost:9200/_nodes?pretty"
curl -X GET "localhost:9200/_nodes/stats?pretty"

# 分片分配
curl -X GET "localhost:9200/_cat/shards?v"
curl -X GET "localhost:9200/_cat/allocation?v"
```

### Cat API
```bash
# 常用 cat 命令
curl -X GET "localhost:9200/_cat/health?v"
curl -X GET "localhost:9200/_cat/nodes?v"
curl -X GET "localhost:9200/_cat/indices?v"
curl -X GET "localhost:9200/_cat/shards?v"
curl -X GET "localhost:9200/_cat/segments?v"
curl -X GET "localhost:9200/_cat/count?v"
curl -X GET "localhost:9200/_cat/recovery?v"
curl -X GET "localhost:9200/_cat/thread_pool?v"
```

## 索引管理

### 索引操作
```bash
# 创建索引
curl -X PUT "localhost:9200/my_index" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "content": { "type": "text" },
      "timestamp": { "type": "date" },
      "status": { "type": "keyword" }
    }
  }
}'

# 删除索引
curl -X DELETE "localhost:9200/my_index"

# 查看索引
curl -X GET "localhost:9200/my_index?pretty"
curl -X GET "localhost:9200/my_index/_mapping?pretty"
curl -X GET "localhost:9200/my_index/_settings?pretty"

# 索引别名
curl -X POST "localhost:9200/_aliases" -H 'Content-Type: application/json' -d'
{
  "actions": [
    { "add": { "index": "my_index_v2", "alias": "my_index" } },
    { "remove": { "index": "my_index_v1", "alias": "my_index" } }
  ]
}'
```

### 索引设置
```bash
# 修改设置
curl -X PUT "localhost:9200/my_index/_settings" -H 'Content-Type: application/json' -d'
{
  "index": {
    "number_of_replicas": 2
  }
}'

# 关闭/打开索引
curl -X POST "localhost:9200/my_index/_close"
curl -X POST "localhost:9200/my_index/_open"

# 刷新索引
curl -X POST "localhost:9200/my_index/_refresh"

# 强制合并
curl -X POST "localhost:9200/my_index/_forcemerge?max_num_segments=1"
```

## 文档操作

### CRUD
```bash
# 创建文档
curl -X POST "localhost:9200/my_index/_doc" -H 'Content-Type: application/json' -d'
{
  "title": "Hello World",
  "content": "This is a test document",
  "timestamp": "2024-01-15T10:00:00"
}'

# 指定 ID 创建
curl -X PUT "localhost:9200/my_index/_doc/1" -H 'Content-Type: application/json' -d'
{
  "title": "Document 1"
}'

# 获取文档
curl -X GET "localhost:9200/my_index/_doc/1?pretty"

# 更新文档
curl -X POST "localhost:9200/my_index/_update/1" -H 'Content-Type: application/json' -d'
{
  "doc": {
    "title": "Updated Title"
  }
}'

# 删除文档
curl -X DELETE "localhost:9200/my_index/_doc/1"

# 批量操作
curl -X POST "localhost:9200/_bulk" -H 'Content-Type: application/json' -d'
{"index":{"_index":"my_index","_id":"1"}}
{"title":"Doc 1"}
{"index":{"_index":"my_index","_id":"2"}}
{"title":"Doc 2"}
'
```

## 查询 DSL

### 基础查询
```bash
# 匹配所有
curl -X GET "localhost:9200/my_index/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} }
}'

# 全文搜索
curl -X GET "localhost:9200/my_index/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "content": "search text"
    }
  }
}'

# 精确匹配
curl -X GET "localhost:9200/my_index/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "term": {
      "status": "published"
    }
  }
}'

# 范围查询
curl -X GET "localhost:9200/my_index/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "range": {
      "timestamp": {
        "gte": "2024-01-01",
        "lte": "2024-01-31"
      }
    }
  }
}'
```

### 复合查询
```bash
# Bool 查询
curl -X GET "localhost:9200/my_index/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        { "match": { "title": "elasticsearch" } }
      ],
      "filter": [
        { "term": { "status": "published" } },
        { "range": { "timestamp": { "gte": "2024-01-01" } } }
      ],
      "should": [
        { "match": { "content": "tutorial" } }
      ],
      "must_not": [
        { "term": { "status": "draft" } }
      ]
    }
  }
}'
```

### 聚合查询
```bash
# 聚合
curl -X GET "localhost:9200/my_index/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "status_count": {
      "terms": { "field": "status" }
    },
    "avg_score": {
      "avg": { "field": "score" }
    },
    "date_histogram": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "day"
      }
    }
  }
}'
```

## 备份与恢复

```bash
# 注册快照仓库
curl -X PUT "localhost:9200/_snapshot/my_backup" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/backup/elasticsearch"
  }
}'

# 创建快照
curl -X PUT "localhost:9200/_snapshot/my_backup/snapshot_1?wait_for_completion=true"

# 查看快照
curl -X GET "localhost:9200/_snapshot/my_backup/_all?pretty"

# 恢复快照
curl -X POST "localhost:9200/_snapshot/my_backup/snapshot_1/_restore" -H 'Content-Type: application/json' -d'
{
  "indices": "my_index",
  "rename_pattern": "(.+)",
  "rename_replacement": "restored_$1"
}'

# 删除快照
curl -X DELETE "localhost:9200/_snapshot/my_backup/snapshot_1"
```

## 常见场景

### 场景 1：重建索引
```bash
# Reindex
curl -X POST "localhost:9200/_reindex" -H 'Content-Type: application/json' -d'
{
  "source": { "index": "old_index" },
  "dest": { "index": "new_index" }
}'

# 带查询条件
curl -X POST "localhost:9200/_reindex" -H 'Content-Type: application/json' -d'
{
  "source": {
    "index": "old_index",
    "query": { "term": { "status": "active" } }
  },
  "dest": { "index": "new_index" }
}'
```

### 场景 2：分片迁移
```bash
# 排除节点
curl -X PUT "localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'
{
  "transient": {
    "cluster.routing.allocation.exclude._name": "node_to_remove"
  }
}'

# 取消排除
curl -X PUT "localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'
{
  "transient": {
    "cluster.routing.allocation.exclude._name": null
  }
}'
```

### 场景 3：性能优化
```bash
# 禁用刷新（批量导入时）
curl -X PUT "localhost:9200/my_index/_settings" -H 'Content-Type: application/json' -d'
{
  "index": { "refresh_interval": "-1" }
}'

# 恢复刷新
curl -X PUT "localhost:9200/my_index/_settings" -H 'Content-Type: application/json' -d'
{
  "index": { "refresh_interval": "1s" }
}'
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 集群 RED | `_cluster/health`, `_cat/shards` |
| 分片未分配 | `_cluster/allocation/explain` |
| 查询慢 | `_nodes/hot_threads`, Profile API |
| 磁盘满 | `_cat/allocation`, 清理旧索引 |
| 内存不足 | `_nodes/stats`, 调整 JVM |

```bash
# 分片未分配原因
curl -X GET "localhost:9200/_cluster/allocation/explain?pretty"

# 热点线程
curl -X GET "localhost:9200/_nodes/hot_threads"

# 任务列表
curl -X GET "localhost:9200/_tasks?detailed=true&actions=*search"
```
