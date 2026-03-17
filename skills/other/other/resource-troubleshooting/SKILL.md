---
name: rancher-resource-troubleshooting
description: This skill should be used when the user asks to "diagnose pod", "pod logs", "why is pod failing", "check events", "troubleshoot", "investigate", "pod not ready", "crashloopbackoff", "pod restart", "container logs", "what's wrong with", "诊断 Pod", "排查问题", "查看日志", "为什么 Pod 失败", "事件查询", or discusses Kubernetes resource troubleshooting and diagnostics (资源排查和诊断).
version: 1.0.0
---

# Rancher 资源排查

诊断和排查 Kubernetes 资源问题。简单日志/事件查询直接执行；复杂诊断委托给 Sub-Agent。

## 直接操作（无需 Sub-Agent）

| 操作 | 工具 | 何时直接使用 |
|------|------|-------------|
| 查看 Pod 日志 | `mcp__rancher__kubernetes_logs` | 提供明确的集群、命名空间和 Pod 名称 |
| 查看事件 | `mcp__rancher__kubernetes_events` | 查看命名空间或特定资源的事件 |
| 描述资源 | `mcp__rancher__kubernetes_describe` | 查看单个资源的详细信息 |
| 获取资源 | `mcp__rancher__kubernetes_get` | 获取单个资源的 YAML/JSON |

## Sub-Agent 委托

### 1. `rancher-pod-diagnostician`
**用于**: Pod 全面诊断、多 Pod 对比、工作负载级排查

**何时委托**:
- 用户要求"诊断 Pod"或"为什么 Pod 失败"
- 需要综合分析日志、事件和资源状态
- 多 Pod 并行诊断
- Deployment/StatefulSet 级别排查

**参数**:
```json
{
  "cluster": "c-abc123",
  "namespace": "production",
  "pod_name": "api-server-abc123",
  "keyword": "error",
  "tail_lines": 200
}
```

### 2. `rancher-deployment-tracker`
**用于**: 部署相关问题排查

**何时委托**:
- 部署失败后排查变更原因
- 需要查看发布历史和版本差异
- 监控滚动更新过程

## 决策树

```
用户请求：
├─ "查看 Pod 日志" + 提供 Pod 名
│  └─ 直接使用 kubernetes_logs
│
├─ "查看事件" + 命名空间/资源
│  └─ 直接使用 kubernetes_events
│
├─ "描述资源 X"
│  └─ 直接使用 kubernetes_describe
│
├─ "诊断 Pod" / "为什么 Pod 失败" / "Pod 不就绪"
│  └─ 委托给 rancher-pod-diagnostician
│
├─ "排查 Deployment" / "部署失败"
│  └─ 委托给 rancher-pod-diagnostician + rancher-deployment-tracker
│
├─ "多 Pod 对比" / "这些 Pod 有什么问题"
│  └─ 并行启动多个 rancher-pod-diagnostician
│
└─ "工作负载日志" / "所有 Pod 的日志"
   └─ 直接使用 kubernetes_logs（labelSelector 聚合多 Pod 日志）
```

## 并行执行

### 多 Pod 诊断
```
用户: "诊断命名空间 production 中所有失败的 Pod"
→ 步骤 1: kubernetes_list 获取 Pod 列表，筛选异常 Pod
→ 步骤 2: 为每个异常 Pod 并行启动 diagnostician
→ 步骤 3: 汇总诊断结果
```

### Deployment 全面排查
```
用户: "排查 Deployment api-server 的问题"
→ 并行启动：
  Agent 1: rancher-pod-diagnostician（诊断关联 Pod）
  Agent 2: rancher-deployment-tracker（检查发布历史和变更）
→ 综合分析
```

## 工作流

### 步骤 1: 识别排查目标
- 什么资源？（Pod、Deployment、Service 等）
- 什么集群和命名空间？
- 有没有具体的错误描述？

### 步骤 2: 确定排查策略
- 简单查询 → 直接调用 MCP 工具
- Pod 诊断 → 委托 pod-diagnostician
- 部署问题 → 委托 deployment-tracker
- 复杂场景 → 并行多个 Agent

### 步骤 3: 启动排查
```
Task({
  subagent_type: "general-purpose",
  description: "诊断 Pod " + pod_name,
  prompt: `你是 rancher-pod-diagnostician。诊断集群 ${cluster} 命名空间 ${namespace} 中 Pod ${pod_name} 的问题。获取 Pod 详情、日志和事件，分析根因。`
})
```

### 步骤 4: 展示结果并建议

## 响应格式

### Pod 诊断
```
## Pod 诊断: api-server-abc123

### 状态
- Phase: Running
- Ready: 0/1 容器就绪
- 重启次数: 15
- 节点: node-2

### 问题发现
1. **CrashLoopBackOff**: 容器 `app` 反复崩溃
   - 最近退出码: 137 (OOMKilled)
   - 内存限制: 256Mi
   - 建议: 增加内存限制到 512Mi

### 关键日志
```
[error] Out of memory: Kill process 1 (app)
```

### 相关事件
| 时间 | 类型 | 原因 | 消息 |
|------|------|------|------|
| 2m ago | Warning | OOMKilling | Memory limit exceeded |
| 5m ago | Normal | Pulled | Container image pulled |

### 建议
1. 增加内存限制
2. 检查应用内存泄漏
3. 添加资源监控
```

## 日志查询技巧

- **关键词过滤**: `keyword: "error"` 快速定位错误
- **时间范围**: `sinceSeconds: 3600` 查看最近 1 小时
- **多 Pod 聚合**: `labelSelector: "app=nginx"` 聚合所有 nginx Pod 日志
- **崩溃日志**: `previous: true` 查看已崩溃容器的日志
- **特定容器**: `container: "sidecar"` 查看特定容器日志

## 错误处理

- **Pod 不存在**: 使用 `kubernetes_list` 搜索类似名称的 Pod
- **日志为空**: 检查容器状态，尝试 `previous: true`
- **权限不足**: 提示检查 RBAC 配置
