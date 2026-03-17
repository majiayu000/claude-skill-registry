---
name: rancher-cluster-inspection
description: This skill should be used when the user asks to "inspection", "inspect cluster", "health check", "patrol", "cluster review", "巡检", "集群巡检", "健康检查", "集群体检", "日常巡检", "安全巡检", "变更前检查", "变更后检查", "定期检查", or discusses systematic cluster health inspection and patrol (系统化集群巡检和健康检查).
version: 2.0.0
---

# Rancher 集群巡检（多 Agent 并行版）

对 Kubernetes 集群做健康巡检，采用多 Agent 并行架构，6 个维度同时执行，显著提升巡检速度和覆盖深度。

## 架构概览

```
用户请求 → Skill 识别巡检类型 → 并行启动维度 Agent → 汇总报告
                                    ├─ cluster-info-inspector   (集群信息)
                                    ├─ node-health-inspector    (节点健康)
                                    ├─ capacity-inspector       (资源容量)
                                    ├─ workload-inspector       (工作负载)
                                    ├─ event-inspector          (异常事件)
                                    └─ system-inspector         (系统组件)
```

## 可用 Sub-Agent（6 个维度 Agent）

### 1. `rancher-cluster-info-inspector`
**维度**: 集群基础信息
**检查项**: 集群状态、K8s 版本、项目数量、命名空间数量、Provider 信息

### 2. `rancher-node-health-inspector`
**维度**: 节点健康
**检查项**: Ready 状态、MemoryPressure、DiskPressure、PIDPressure、Taints/Cordoned、kubelet 版本一致性

### 3. `rancher-capacity-inspector`
**维度**: 资源容量
**检查项**: CPU/内存请求/限制/使用率、Pod 数量、过度分配检测

### 4. `rancher-workload-inspector`
**维度**: 工作负载健康
**检查项**: Deployment/StatefulSet/DaemonSet 可用性、异常 Pod、高重启 Pod

### 5. `rancher-event-inspector`
**维度**: 异常事件
**检查项**: Warning 事件、OOMKilling、FailedScheduling、Evicted、高频重复事件

### 6. `rancher-system-inspector`
**维度**: 系统组件
**检查项**: CoreDNS、kube-proxy、metrics-server、cattle-agent、fleet-agent、Ingress Controller

## 决策树

```
用户请求：
├─ "集群巡检" / "cluster inspection" / "健康检查" / "集群体检"
│  └─ 并行启动 6 个维度 Agent（完整巡检）
│
├─ "快速检查" / "quick check" / "简单看看集群状态"
│  └─ 并行启动 3 个维度 Agent（cluster-info + node-health + event）
│
├─ "节点巡检" / "检查所有节点" / "node inspection"
│  └─ 并行启动 2 个维度 Agent（node-health + capacity）
│
├─ "工作负载巡检" / "应用健康检查" / "workload inspection"
│  └─ 并行启动 2 个维度 Agent（workload + event）
│
├─ "事件巡检" / "检查异常事件" / "event inspection"
│  └─ 启动 1 个维度 Agent（event）
│
├─ "系统组件巡检" / "检查系统组件" / "system inspection"
│  └─ 启动 1 个维度 Agent（system）
│
├─ "巡检所有集群" / "全部集群体检" / "inspect all clusters"
│  └─ 获取集群列表 → 为每个集群并行启动 6 个维度 Agent
│
├─ "变更前检查" / "pre-change check"
│  └─ 并行启动 6 个维度 Agent（完整巡检，记录基线）
│
└─ "变更后检查" / "post-change check"
   └─ 并行启动 6 个维度 Agent（完整巡检，与基线对比）
```

## 并行执行模式

### 模式 1: 单集群完整巡检（6 Agent 并行）
```
用户: "对 production 集群做一次完整巡检"

→ 步骤 1: 确定集群 ID（如需要，使用 cluster_list 搜索）
→ 步骤 2: 同时启动 6 个维度 Agent
  Agent 1: rancher-cluster-info-inspector（集群 c-abc123）
  Agent 2: rancher-node-health-inspector（集群 c-abc123）
  Agent 3: rancher-capacity-inspector（集群 c-abc123）
  Agent 4: rancher-workload-inspector（集群 c-abc123）
  Agent 5: rancher-event-inspector（集群 c-abc123）
  Agent 6: rancher-system-inspector（集群 c-abc123）
→ 步骤 3: 汇总 6 个维度报告，计算整体评分，生成完整巡检报告
```

### 模式 2: 多集群并行巡检（N 集群 × 6 Agent）
```
用户: "巡检所有集群"

→ 步骤 1: 调用 cluster_list 获取所有集群
→ 步骤 2: 为每个集群同时启动 6 个维度 Agent
  集群 production (c-abc123): 6 个维度 Agent
  集群 staging (c-def456):    6 个维度 Agent
  集群 dev (c-ghi789):        6 个维度 Agent
  （共 18 个 Agent 并行运行）
→ 步骤 3: 分别汇总每个集群的巡检报告
→ 步骤 4: 生成多集群巡检总览
```

### 模式 3: 快速巡检（3 Agent 并行）
```
用户: "快速检查一下 production 集群"

→ 并行启动 3 个维度 Agent：
  Agent 1: rancher-cluster-info-inspector
  Agent 2: rancher-node-health-inspector
  Agent 3: rancher-event-inspector
→ 汇总报告（仅含 3 个维度）
```

### 模式 4: 指定命名空间巡检
```
用户: "巡检 production 集群的 app 和 monitoring 命名空间"

→ 并行启动维度 Agent（传入 namespaces 参数）：
  Agent 1: rancher-workload-inspector（namespaces: ["app", "monitoring"]）
  Agent 2: rancher-event-inspector（namespaces: ["app", "monitoring"]）
→ 聚焦指定命名空间的检查结果
```

### 模式 5: 变更前后对比巡检
```
用户: "做一次变更前巡检"

→ 并行启动 6 个维度 Agent（完整巡检）
→ 保存报告作为基线

用户（变更后）: "做变更后检查"

→ 并行启动 6 个维度 Agent（完整巡检）
→ 与之前的基线对比，高亮变化项
```

## 工作流

### 步骤 1: 识别巡检类型
- 完整巡检 vs 快速巡检 vs 专项巡检？
- 单集群 vs 多集群？
- 是否指定命名空间？

### 步骤 2: 获取集群信息
如果用户提供集群名称而非 ID：
```
→ 使用 cluster_list（name: "关键词"）搜索
→ 获取匹配的集群 ID
```

如果用户要求巡检"所有集群"：
```
→ 使用 cluster_list 获取完整列表
```

### 步骤 3: 并行启动维度 Agent

**完整巡检（6 Agent 并行）：**
```javascript
// 同时启动 6 个维度 Agent
const tasks = [
  Task({
    subagent_type: "general-purpose",
    description: "巡检集群基础信息",
    prompt: `你是 rancher-cluster-info-inspector。对集群 ${cluster}（${name}）执行集群基础信息巡检。检查集群状态、K8s 版本、项目和命名空间概况。返回标准化维度报告（含 dimension、score、status、items、issues、recommendations）。`
  }),
  Task({
    subagent_type: "general-purpose",
    description: "巡检节点健康",
    prompt: `你是 rancher-node-health-inspector。对集群 ${cluster}（${name}）执行节点健康巡检。检查 Ready 状态、Conditions、Taints、kubelet 版本一致性。返回标准化维度报告。`
  }),
  Task({
    subagent_type: "general-purpose",
    description: "巡检资源容量",
    prompt: `你是 rancher-capacity-inspector。对集群 ${cluster}（${name}）执行资源容量巡检。检查 CPU/内存请求/限制/使用率、Pod 数量、过度分配。返回标准化维度报告。`
  }),
  Task({
    subagent_type: "general-purpose",
    description: "巡检工作负载",
    prompt: `你是 rancher-workload-inspector。对集群 ${cluster}（${name}）执行工作负载健康巡检。检查 Deployment/StatefulSet/DaemonSet 可用性、异常 Pod。返回标准化维度报告。`
  }),
  Task({
    subagent_type: "general-purpose",
    description: "巡检异常事件",
    prompt: `你是 rancher-event-inspector。对集群 ${cluster}（${name}）执行异常事件巡检。检查 Warning 事件、OOMKilling、FailedScheduling 等关键事件。返回标准化维度报告。`
  }),
  Task({
    subagent_type: "general-purpose",
    description: "巡检系统组件",
    prompt: `你是 rancher-system-inspector。对集群 ${cluster}（${name}）执行系统组件巡检。检查 kube-system、cattle-system 核心组件状态。返回标准化维度报告。`
  })
];
const results = await Promise.all(tasks);
```

**快速巡检（3 Agent 并行）：**
```javascript
const tasks = [
  Task({ ... description: "巡检集群基础信息", prompt: "rancher-cluster-info-inspector ..." }),
  Task({ ... description: "巡检节点健康", prompt: "rancher-node-health-inspector ..." }),
  Task({ ... description: "巡检异常事件", prompt: "rancher-event-inspector ..." })
];
```

**多集群巡检（N × 6 Agent 并行）：**
```javascript
const clusters = await cluster_list();
const tasks = clusters.flatMap(c => [
  Task({ ... prompt: `rancher-cluster-info-inspector for ${c.id}` }),
  Task({ ... prompt: `rancher-node-health-inspector for ${c.id}` }),
  Task({ ... prompt: `rancher-capacity-inspector for ${c.id}` }),
  Task({ ... prompt: `rancher-workload-inspector for ${c.id}` }),
  Task({ ... prompt: `rancher-event-inspector for ${c.id}` }),
  Task({ ... prompt: `rancher-system-inspector for ${c.id}` })
]);
const results = await Promise.all(tasks);
// 按集群分组汇总
```

### 步骤 4: 汇总巡检报告
- 收集所有维度 Agent 的返回结果
- 汇总评分概览表格
- 合并各维度的详细检查结果
- 合并问题清单（按严重程度排序）
- 合并改进建议（按优先级排序）
- 计算整体评分（取各维度最低分）

## 响应格式

### 单集群巡检报告
```
## 集群巡检报告: production (c-abc123)

### 巡检概览
- 巡检时间: 2025-01-15 10:30
- 巡检范围: 完整巡检（6 维度并行）
- **整体评分: B（良好）**

### 评分概览
| 维度 | Agent | 评分 | 状态 |
|------|-------|------|------|
| 集群基础信息 | cluster-info-inspector | A | ✅ 正常 |
| 节点健康 | node-health-inspector | B | ⚠️ 注意 |
| 资源容量 | capacity-inspector | A | ✅ 正常 |
| 工作负载健康 | workload-inspector | B | ⚠️ 注意 |
| 异常事件 | event-inspector | A | ✅ 正常 |
| 系统组件 | system-inspector | A | ✅ 正常 |

### 问题清单
| 严重程度 | 维度 | 问题 | 建议 |
|----------|------|------|------|
| ⚠️ | 节点健康 | node-5 NotReady | 检查 kubelet |
| ⚠️ | 工作负载 | 2 个 Pod CrashLoopBackOff | 查看日志 |

### 改进建议
1. **[紧急]** 修复 node-5
2. **[建议]** 排查崩溃 Pod
```

### 多集群巡检总览
```
## 多集群巡检总览

| 集群 | 评分 | 集群信息 | 节点 | 容量 | 工作负载 | 事件 | 系统 | 关键问题 |
|------|------|----------|------|------|----------|------|------|----------|
| production | B | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | 1 节点 NotReady |
| staging | A | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 无 |
| dev | C | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ | 容量不足 |

### 集群详情
[各集群独立巡检报告...]
```

## 巡检范围 → Agent 映射速查表

| 范围 | Agent 数量 | 维度 Agent |
|------|-----------|------------|
| full | 6 | cluster-info + node-health + capacity + workload + event + system |
| quick | 3 | cluster-info + node-health + event |
| nodes | 2 | node-health + capacity |
| workloads | 2 | workload + event |
| events | 1 | event |
| system | 1 | system |

## 巡检最佳实践

1. **日常巡检**：每天执行 quick 巡检（3 Agent），关注节点和事件
2. **周巡检**：每周执行 full 巡检（6 Agent），覆盖所有维度
3. **变更巡检**：重大变更前后各做一次 full 巡检，对比差异
4. **事件驱动**：收到告警后执行对应专项巡检
5. **多集群**：定期对所有集群做 full 巡检，生成健康趋势

## 错误处理

- **维度 Agent 失败**: 在报告中标注该维度为"巡检失败"，不影响其他维度评分
- **metrics-server 未安装**: capacity-inspector 跳过实际使用率，报告中注明
- **集群不可达**: 标记为巡检失败，报告集群连接问题
- **权限不足**: 各 Agent 尽可能巡检可访问资源，注明权限限制
- **数据不完整**: 基于可用数据生成报告，标注缺失项

## 与其他技能的关系

| 巡检发现问题 | 后续行动 | 使用技能 |
|-------------|----------|----------|
| 节点 NotReady | 深入分析节点 | capacity-analysis |
| Pod CrashLoopBackOff | 诊断 Pod | resource-troubleshooting |
| Deployment 不可用 | 查看部署变更 | deployment-management |
| 资源不足 | 容量规划 | capacity-analysis |
| 可疑事件 | 追溯资源变更 | resource-discovery |
