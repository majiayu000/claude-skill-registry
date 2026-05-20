---
name: rancher-deployment-management
description: This skill should be used when the user asks to "rollout history", "deployment changes", "watch deployment", "diff", "what changed", "compare deployments", "monitor rollout", "deployment status", "cross cluster diff", "部署历史", "发布历史", "变更", "部署对比", "监控部署", "跨集群对比", or discusses deployment tracking, change management, and release monitoring (部署追踪、变更管理和发布监控).
version: 1.0.0
---

# Rancher 部署管理

追踪 Deployment 变更、查看发布历史、对比资源差异、监控滚动更新。

## 主要 Sub-Agent

### `rancher-deployment-tracker`
**用于**: 所有部署追踪和变更管理任务

**能力**:
- 查看 Deployment 发布历史和修订版本
- 比较两个资源版本的 git-style 差异
- 跨集群比较同一资源的差异（staging vs production）
- 实时监控资源变更
- 分析部署状态和相关事件

**传递参数**:
```json
{
  "cluster": "c-abc123",
  "namespace": "production",
  "name": "api-server",
  "kind": "deployment",
  "action": "history" | "diff" | "watch" | "status" | "cross_cluster_diff"
}
```

## 工作流

### 步骤 1: 识别操作类型
解析用户请求，确定：
- 查看历史？→ `history`
- 比较差异？→ `diff` 或 `cross_cluster_diff`
- 监控变更？→ `watch`
- 检查状态？→ `status`

### 步骤 2: 启动部署追踪器
```
Task({
  subagent_type: "general-purpose",
  description: "追踪 Deployment " + name + " 的变更",
  prompt: `你是 rancher-deployment-tracker。${action_description}`
})
```

### 步骤 3: 展示结果

## 使用模式

### 查看发布历史
```
用户: "api-server 的发布历史"
→ 启动 rancher-deployment-tracker
   action: "history"
→ 展示修订版本列表和变更原因
```

### 跨集群资源对比
```
用户: "对比 staging 和 production 的 api-server Deployment"
→ 启动 rancher-deployment-tracker
   action: "cross_cluster_diff"
   使用 kubernetes_diff：
     kind: "deployment"
     left: { cluster: "staging-id", namespace: "app", name: "api-server" }
     right: { cluster: "prod-id", namespace: "app", name: "api-server" }
     ignoreMeta: true, ignoreStatus: true
→ 展示差异报告（镜像版本、副本数、环境变量等）
```

### 监控滚动更新
```
用户: "监控 api-server 的滚动更新"
→ 启动 rancher-deployment-tracker
   action: "watch"
   kubernetes_watch：kind: "deployment", intervalSeconds: 5, iterations: 12
→ 展示变更过程
```

### 部署全面分析
```
用户: "分析 api-server Deployment 的状况"
→ 启动 rancher-deployment-tracker
   action: "status"
→ 引擎内部并行获取：
   - 发布历史
   - 当前描述和事件
   - Pod 状态
→ 展示综合状态报告
```

## 并行执行

### 多 Deployment 对比
```
用户: "对比 api-server 和 web-server 的部署配置"
→ 并行启动：
  Agent 1: rancher-deployment-tracker（api-server 的详情）
  Agent 2: rancher-deployment-tracker（web-server 的详情）
→ 对比展示
```

### 多集群同一服务对比
```
用户: "api-server 在三个集群中的差异"
→ 使用 kubernetes_diff 进行两两对比：
  对比 1: staging vs production
  对比 2: production vs dr
→ 汇总差异报告
```

## 响应格式

### 发布历史
```
## 发布历史: api-server (production/c-abc123)

| 修订版本 | 变更原因 | 时间 |
|----------|----------|------|
| 5 (当前) | Update image to v2.1.0 | 2h ago |
| 4 | Scale to 5 replicas | 1d ago |
| 3 | Update env vars | 3d ago |
| 2 | Update image to v2.0.0 | 1w ago |
| 1 | Initial deployment | 2w ago |
```

### 资源差异
```
## 资源对比: api-server

### staging (c-staging) vs production (c-prod)

关键差异：
- 镜像: staging=v2.2.0-rc1, production=v2.1.0
- 副本数: staging=2, production=5
- 内存限制: staging=256Mi, production=512Mi

详细 diff:
--- staging/api-server
+++ production/api-server
@@ spec.replicas @@
-  replicas: 2
+  replicas: 5
@@ spec.template.spec.containers[0].image @@
-  image: api-server:v2.2.0-rc1
+  image: api-server:v2.1.0
```

### 变更监控
```
## 监控结果: api-server

监控时长: 60 秒 (5s x 12 次)
检测到 3 次变更:

### 变更 1 (10s)
replicas: 5 → 4 (缩容中)

### 变更 2 (25s)
replicas: 4 → 3 (继续缩容)

### 变更 3 (40s)
replicas: 3 → 3, readyReplicas: 2 → 3 (就绪)
```

## 注意事项

- `kubernetes_rollout_history` 仅支持 Deployment 类型
- 跨集群 diff 需要两个集群都有相同名称的资源
- watch 监控的总时长 = `intervalSeconds × iterations`
- 使用 `ignoreMeta: true` 和 `ignoreStatus: true` 减少无关差异
- watch 结果可能较大，建议使用较小的 iterations（如 6-12）
