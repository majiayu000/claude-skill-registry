---
name: rancher-cluster-management
description: This skill should be used when the user asks to "list clusters", "show clusters", "cluster overview", "list projects", "which clusters", "compare clusters", "cluster status", "集群列表", "项目列表", "集群概览", "集群状态", "集群对比", or discusses Rancher cluster and project navigation (集群和项目管理).
version: 1.0.0
---

# Rancher 集群管理

导航和管理 Rancher 多集群环境。简单查询直接执行；复杂的多集群分析委托给 Sub-Agent。

## 直接操作（无需 Sub-Agent）

这些简单操作立即执行：

| 操作 | 工具 | 何时直接使用 |
|------|------|-------------|
| 列出集群 | `mcp__rancher__cluster_list` | 用户要求查看集群列表 |
| 按名称搜索集群 | `mcp__rancher__cluster_list` | 提供集群名称关键词 |
| 列出项目 | `mcp__rancher__project_list` | 用户要求查看项目列表 |
| 按集群列出项目 | `mcp__rancher__project_list` | 提供集群 ID |

## Sub-Agent 委托

### `rancher-cluster-explorer`
**用于**: 集群概览、容量分析、多集群对比

**何时委托**:
- 用户要求"集群概览"或"集群健康状况"
- 用户要求对比多个集群
- 用户需要集群容量和资源使用信息

**参数**:
```json
{
  "action": "cluster_overview" | "compare_clusters",
  "cluster": "c-abc123",
  "clusters": ["c-abc123", "c-def456"]
}
```

## 决策树

```
用户请求：
├─ "列出集群" / "list clusters" / "show all clusters"
│  └─ 直接使用 cluster_list
│
├─ "列出项目" / "list projects" + 集群名/ID
│  └─ 直接使用 project_list
│
├─ "集群概览" / "cluster overview" / "cluster health"
│  └─ 委托给 rancher-cluster-explorer（包含容量和节点分析）
│
├─ "对比集群 A 和 B" / "compare clusters"
│  └─ 委托给 rancher-cluster-explorer（并行分析多集群）
│
└─ "哪个集群有空间" / "which cluster has capacity"
   └─ 委托给 rancher-cluster-explorer（并行获取容量）
```

## 并行执行

### 多集群概览
```
用户: "对比 production 和 staging 集群"
→ 并行启动：
  Agent 1: rancher-cluster-explorer（集群 A 概览）
  Agent 2: rancher-cluster-explorer（集群 B 概览）
→ 合并对比展示
```

### 全集群扫描
```
用户: "所有集群的状态"
→ 步骤 1: 直接调用 cluster_list 获取所有集群
→ 步骤 2: 为每个集群并行启动 explorer Agent
→ 步骤 3: 汇总展示
```

## 工作流

### 步骤 1: 识别操作类型
- 简单列表？→ 直接调用 MCP 工具
- 需要概览/对比？→ 委托给 Sub-Agent

### 步骤 2: 获取集群 ID
如果用户提供集群名称而非 ID：
```
→ 使用 cluster_list（name: "关键词"）搜索
→ 获取匹配的集群 ID
```

### 步骤 3: 执行并展示结果

## 响应格式

### 集群列表
```
## 可用集群

| 集群 | ID | 状态 | 节点数 | Provider |
|------|-----|------|--------|----------|
| production | c-abc123 | Active | 5 | Custom |
| staging | c-def456 | Active | 3 | Custom |
```

### 集群概览
```
## 集群概览: production (c-abc123)

### 基本信息
- 状态: Active
- 节点数: 5
- 项目数: 3

### 资源容量
| 资源 | 请求 | 限制 | 实际使用 |
|------|------|------|----------|
| CPU | 65% | 120% | 45% |
| 内存 | 70% | 90% | 60% |

### 节点状态
| 节点 | 状态 | CPU | 内存 | Pod数 |
|------|------|-----|------|-------|
| node-1 | Ready | 55% | 62% | 42 |
| node-2 | Ready | 72% | 78% | 38 |
```

## 错误处理

- **集群未找到**: 列出所有可用集群供用户选择
- **权限不足**: 告知用户检查 Rancher token 权限
- **集群不可达**: 显示集群状态，建议检查网络连接
