---
name: devops
description: "DevOps patterns: containerization, CI/CD, deployment strategies, monitoring. Use when containerizing apps, setting up pipelines, or deploying services."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# DevOps 模式

本技能提供 DevOps 实践的最佳实践和模式，支持多平台按需加载。

## 触发条件

- 容器化应用（Docker）
- 配置 CI/CD 流水线
- 部署服务到云平台
- 设置监控和告警
- 基础设施即代码

## 平台专属模式

根据项目需求，加载对应的平台专属文件：

| 平台   | 加载文件    | 内容                      |
| ------ | ----------- | ------------------------- |
| Docker | `docker.md` | 容器化、Compose、镜像优化 |
| CI/CD  | `ci-cd.md`  | GitHub Actions、GitLab CI |

**加载方式**: 检测项目中的 `Dockerfile`/`.github/workflows`/`k8s/` 等文件确定需求。

---

## 通用 DevOps 原则

### 12-Factor App 原则

```
┌─────────────────────────────────────────────────────────────┐
│                    12-Factor App 核心原则                     │
├─────────────────────────────────────────────────────────────┤
│  1. Codebase        一个代码库，多个部署                      │
│  2. Dependencies    显式声明依赖                             │
│  3. Config          配置存储在环境变量中                      │
│  4. Backing Services 将后端服务视为附加资源                   │
│  5. Build/Release/Run 严格分离构建、发布、运行                │
│  6. Processes       以无状态进程运行应用                      │
│  7. Port Binding    通过端口绑定导出服务                      │
│  8. Concurrency     通过进程模型扩展                         │
│  9. Disposability   快速启动和优雅终止                       │
│ 10. Dev/Prod Parity 保持开发、预发、生产环境尽量相似          │
│ 11. Logs            将日志视为事件流                         │
│ 12. Admin Processes 将管理任务作为一次性进程运行              │
└─────────────────────────────────────────────────────────────┘
```

### 环境管理

```
┌─────────────────────────────────────────────────────────────┐
│                      环境流转                                │
├─────────────────────────────────────────────────────────────┤
│  Development → Staging → Production                         │
│       ↓           ↓           ↓                             │
│   本地开发      预发验证      线上环境                        │
│   .env.local   .env.staging  .env.production                │
└─────────────────────────────────────────────────────────────┘
```

**环境变量管理**:

```bash
# .env.example（提交到 Git，作为模板）
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379
API_KEY=your-api-key-here

# .env.local（不提交，本地开发）
DATABASE_URL=postgresql://dev:dev@localhost:5432/myapp_dev
```

---

## 部署策略

| 策略         | 特点                                       | 适用场景             |
| ------------ | ------------------------------------------ | -------------------- |
| **蓝绿部署** | 双环境切换，零停机，回滚快                 | 关键业务，零停机要求 |
| **滚动部署** | 逐实例替换，maxSurge/maxUnavailable 控制   | 标准 K8s 部署        |
| **金丝雀**   | 5-10% 流量试验，渐进增量，监控错误率后全量 | 高风险功能发布       |

> 详细配置和流程图见 [docker.md](./docker.md) 和各云平台文档。

---

## 监控与可观测性

### 三大支柱

| 支柱        | 用途             | 工具                |
| ----------- | ---------------- | ------------------- |
| **Metrics** | 聚合的数值数据   | Prometheus, Datadog |
| **Logs**    | 离散的事件记录   | ELK, Loki           |
| **Traces**  | 请求的分布式追踪 | Jaeger, Zipkin      |

### 关键指标 (Golden Signals)

```
┌─────────────────────────────────────────────────────────────┐
│                   四个黄金信号                               │
├─────────────────────────────────────────────────────────────┤
│  Latency    响应时间 - p50, p95, p99                        │
│  Traffic    流量 - QPS, 请求数/秒                           │
│  Errors     错误率 - 5xx 比例, 失败请求                      │
│  Saturation 饱和度 - CPU, 内存, 磁盘使用率                   │
└─────────────────────────────────────────────────────────────┘
```

### 告警规则示例

```yaml
# Prometheus 告警规则
groups:
  - name: application
    rules:
      # 高错误率告警
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "高错误率: {{ $value | humanizePercentage }}"

      # 高延迟告警
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P95 延迟超过 1s"
```

---

## 基础设施即代码 (IaC)

| 工具      | 用途         | 关键原则                     |
| --------- | ------------ | ---------------------------- |
| Terraform | 基础设施编排 | 声明式、模块化、环境隔离     |
| Ansible   | 配置管理     | 幂等性、Playbook 可复用      |
| Scripts   | 部署/回滚    | deploy.sh + rollback.sh 成对 |

> 目录结构和 Terraform 示例详见 [ci-cd.md](./ci-cd.md#基础设施即代码-iac-附录)。

---

## 安全最佳实践

### 镜像安全

```dockerfile
# ✅ 使用特定版本，非 latest
FROM node:20-alpine

# ✅ 以非 root 用户运行
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# ✅ 扫描漏洞
# docker scan myimage:tag
```

### 密钥管理

| 方案         | 适用场景      | 工具                       |
| ------------ | ------------- | -------------------------- |
| 环境变量     | 开发/简单部署 | .env 文件                  |
| 密钥管理服务 | 生产环境      | AWS Secrets Manager, Vault |
| K8s Secrets  | Kubernetes    | kubectl create secret      |

```bash
# 创建 K8s Secret
kubectl create secret generic app-secrets \
  --from-literal=db-password=mysecretpassword \
  --from-literal=api-key=myapikey
```

### 网络安全

```yaml
# 网络策略示例 - 只允许特定来源访问
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
spec:
  podSelector:
    matchLabels:
      app: api
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - port: 8080
```

---

## 日志管理

### 结构化日志

```json
{
  "timestamp": "2025-01-23T10:00:00Z",
  "level": "info",
  "service": "user-service",
  "traceId": "abc123",
  "message": "用户登录成功",
  "userId": "user_456",
  "duration": 45,
  "environment": "production"
}
```

### 日志级别指南

| 级别  | 用途         | 生产环境 |
| ----- | ------------ | -------- |
| DEBUG | 详细调试信息 | 关闭     |
| INFO  | 正常操作事件 | 开启     |
| WARN  | 潜在问题     | 开启     |
| ERROR | 错误但可恢复 | 开启     |
| FATAL | 致命错误     | 开启     |

---

## 平台专属内容

详细的平台专属实现请参考：

- **Docker**: [docker.md](./docker.md) - 容器化、Compose、镜像优化
- **CI/CD**: [ci-cd.md](./ci-cd.md) - GitHub Actions、GitLab CI

> 💡 Kubernetes 基础概念已包含在本文件中（部署策略、网络策略等），如需深入学习请参考官方文档。

---

## 最佳实践

1. **配置外部化** - 不在代码中硬编码配置
2. **无状态设计** - 应用实例可随时销毁重建
3. **健康检查** - 配置 liveness 和 readiness 探针
4. **优雅终止** - 处理 SIGTERM 信号，完成进行中的请求
5. **日志标准化** - 结构化日志，统一格式
6. **监控告警** - 关键指标监控，及时告警
7. **回滚能力** - 保留多个版本，支持快速回滚
8. **安全扫描** - 镜像漏洞扫描，依赖检查
9. **资源限制** - 设置 CPU/内存限制，防止资源耗尽
10. **文档完善** - 记录部署流程和故障处理

---

## Maintenance

- Sources: 12-Factor App, CNCF, 各云平台文档
- Last updated: 2025-01-23
- Pattern: 通用原则 + 按需加载平台专属

> **记住**: DevOps 的目标是自动化一切可重复的操作——手动步骤越少，出错概率越低。
