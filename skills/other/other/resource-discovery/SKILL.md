---
name: rancher-resource-discovery
description: This skill should be used when the user asks to "list resources", "find resources", "get all", "dependency tree", "what depends on", "show dependencies", "resource inventory", "what's in namespace", "recently created", "资源列表", "依赖关系", "资源清单", "命名空间资源", "最近创建", or discusses Kubernetes resource discovery, inventory, and dependency analysis (资源发现、清单和依赖分析).
version: 1.0.0
---

# Rancher 资源发现

发现、搜索和探索 Kubernetes 资源及其依赖关系。

## 主要 Sub-Agent

### `rancher-resource-scout`
**用于**: 资源清单、搜索、依赖关系分析

**能力**:
- 获取命名空间或集群中的所有资源（类似 ketall）
- 按类型、标签、名称搜索资源
- 展示资源的依赖和被依赖关系树
- 查找最近创建的资源
- 多命名空间或多集群资源搜索

**传递参数**:
```json
{
  "cluster": "c-abc123",
  "namespace": "production",
  "kind": "deployment",
  "name": "nginx",
  "label_selector": "app=nginx",
  "action": "inventory" | "search" | "dependencies" | "dependents",
  "since": "1h"
}
```

## 决策树

```
用户查询提到：
├─ "命名空间里有什么" / "get all" / "资源清单"
│  └─ 使用: rancher-resource-scout（action: "inventory"）
│
├─ "找到所有 X 类型资源" / "list deployments"
│  └─ 使用: rancher-resource-scout（action: "search"）
│
├─ "什么依赖 X" / "依赖关系" / "dependency tree"
│  └─ 使用: rancher-resource-scout（action: "dependencies" 或 "dependents"）
│
├─ "最近创建的资源" / "recent resources"
│  └─ 使用: rancher-resource-scout（action: "inventory"，since: "1h"）
│
└─ "跨集群搜索" / "在所有集群中找"
   └─ 为每个集群并行启动 rancher-resource-scout
```

## 并行执行模式

### 模式 1: 多命名空间资源清查
```
用户: "对比 staging 和 production 命名空间的资源"

→ 并行启动：
  Agent 1: rancher-resource-scout（namespace: "staging"）
  Agent 2: rancher-resource-scout（namespace: "production"）
→ 对比资源清单
```

### 模式 2: 跨集群资源搜索
```
用户: "在所有集群中找到 app=nginx 的 Deployment"

→ 步骤 1: 获取集群列表
→ 步骤 2: 为每个集群并行启动 resource-scout
→ 步骤 3: 汇总跨集群搜索结果
```

### 模式 3: 资源全面分析
```
用户: "分析 Service nginx 的完整依赖关系"

→ 启动 rancher-resource-scout
→ Agent 内部并行：
   kubernetes_dep（direction: "dependencies"）-- 依赖什么
   kubernetes_dep（direction: "dependents"）-- 被什么依赖
   kubernetes_describe -- 资源详情
→ 展示完整关系图谱
```

## 工作流

### 步骤 1: 解析用户请求
- 要查找什么？（资源类型、名称、标签）
- 在哪里查找？（集群、命名空间）
- 关注什么方面？（清单、依赖关系、搜索）

### 步骤 2: 确定策略
- 简单列表 → 一个 Agent
- 多命名空间/多集群 → 多个 Agent 并行
- 依赖分析 → 一个 Agent 内部并行

### 步骤 3: 启动 Sub-Agent
```
Task({
  subagent_type: "general-purpose",
  description: "发现命名空间 " + namespace + " 的资源",
  prompt: `你是 rancher-resource-scout。获取集群 ${cluster} 命名空间 ${namespace} 中的所有资源清单。`
})
```

### 步骤 4: 展示结果

## 响应格式

### 资源清单
```
## 资源清单: production (c-abc123)

### 概览
- 总资源数: 150
- 命名空间: production

### 按类型统计
| 类型 | 数量 |
|------|------|
| Pod | 45 |
| Deployment | 12 |
| Service | 15 |
| ConfigMap | 30 |
| Secret | 20 |
| Ingress | 5 |
| ServiceAccount | 8 |
| Role/RoleBinding | 10 |
| PVC | 5 |
```

### 依赖关系树
```
## 依赖关系: Deployment/api-server

### 被依赖方（Dependents）
Deployment/api-server
├── ReplicaSet/api-server-6d4f5b7c8
│   ├── Pod/api-server-6d4f5b7c8-abc12
│   └── Pod/api-server-6d4f5b7c8-def34
└── HPA/api-server-hpa

### 依赖方（Dependencies）
Deployment/api-server
├── ConfigMap/api-server-config
├── Secret/api-server-secrets
├── ServiceAccount/api-server-sa
└── PVC/api-server-data
```

### 搜索结果
```
## 搜索结果: app=nginx

在 3 个集群中找到 8 个匹配资源：

### production (c-abc123)
| 类型 | 命名空间 | 名称 | 状态 |
|------|----------|------|------|
| Deployment | web | nginx | 3/3 Ready |
| Service | web | nginx-svc | ClusterIP |

### staging (c-def456)
| 类型 | 命名空间 | 名称 | 状态 |
|------|----------|------|------|
| Deployment | web | nginx | 2/2 Ready |
| Service | web | nginx-svc | ClusterIP |
```

## 注意事项

- `kubernetes_get_all` 可能返回大量数据，始终使用 `namespace` 限制范围
- 使用 `since` 参数查找最近创建的资源（如 `'1h'`、`'2d'`、`'1w'`）
- `kubernetes_dep` 默认方向为 `dependents`（被什么依赖），使用 `dependencies` 查看依赖什么
- 依赖树的 `depth` 参数范围 1-20，默认 10
- `kubernetes_get_all` 默认排除事件（`excludeEvents: true`）
- 使用 `scope: "namespaced"` 或 `scope: "cluster"` 过滤资源范围
