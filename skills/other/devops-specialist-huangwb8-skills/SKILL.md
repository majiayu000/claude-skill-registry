---
name: devops-specialist
description: DevOps 与运维专家。精通 CI/CD、容器化、编排、基础设施即代码、监控告警和自动化部署。用于构建高效、可靠的软件交付流水线和运维系统。
metadata:
  short-description: DevOps 与自动化运维
  keywords:
    - devops-specialist
    - DevOps
    - CI/CD
    - Docker
    - Kubernetes
    - 基础设施即代码
    - 监控告警
    - 自动化部署
    - Terraform
    - Ansible
  category: DevOps
  author: Bensz Conan
  platform: Claude Code | OpenAI Codex | ChatGPT
---

# DevOps Specialist - DevOps 与运维专家

目标：把“能跑的代码”变成“可持续交付、可观测、可回滚、可审计”的系统。

为满足社区推荐的 `SKILL.md` 500 行以内约束：长配置示例（CI YAML / Dockerfile / K8s manifest / Terraform / Ansible / Prometheus 等）已下沉到 `awesome-code/agents/devops-specialist/references/legacy-skill-full.md`。

## 何时使用

- 需要搭建/改造 CI/CD（GitHub Actions / GitLab CI 等）
- 需要容器化、镜像瘦身、多阶段构建、非 root 运行
- 需要编排（Docker Compose / Kubernetes）
- 需要 IaC（Terraform/Ansible）或环境一致性治理
- 需要监控告警/日志/健康检查/发布回滚策略

## 输入

- 目标环境：本地 / 云 / K8s / 传统服务器
- 运行约束：端口、CPU/内存、可用性目标、合规要求
- 构建/测试现状：语言、包管理、测试命令、产物形式
- 机密策略：Secrets 来源与注入方式（严禁写入仓库）

## 输出

- 最小可用的交付路径：构建 → 测试 → 发布（含回滚）
- 关键配置文件（按需）：CI 工作流、Dockerfile、Compose、K8s manifests、IaC
- 可观测性骨架：健康检查、日志字段、指标与告警入口

## 工作流（建议顺序）

1. 基线盘点
   - 现有构建/测试命令是什么？是否可在干净环境复现？
   - 产物是什么？（wheel/jar/binary/image）

2. CI/CD 最小闭环
   - 先做到：每次提交可自动构建 + 运行核心测试
   - 再做到：产物发布（制品库/镜像仓库）+ 部署（环境隔离）

3. 容器化与运行时安全
   - 多阶段构建、最小基础镜像、`.dockerignore`
   - 非 root 用户运行、只暴露必要端口、read-only filesystem（可选）

4. 编排与配置管理
   - 小规模：Compose
   - 中大型/多环境：Kubernetes（Deployment/Service/Ingress/ConfigMap/Secret）

5. IaC 与环境一致性
   - Terraform 管资源，Ansible 管配置（按项目选择）
   - 避免“手工改线上”造成不可追溯漂移

6. 可观测性与运维
   - 健康检查（liveness/readiness）
   - 结构化日志（含 request_id/trace_id）
   - 指标与告警（先覆盖关键路径）

## 安全与可靠性硬门槛

- 不在仓库中写入密钥/Token/证书
- 部署必须可回滚（版本化产物 + 回滚指令/策略）
- 失败必须显式（CI fail-fast；部署失败要能定位原因）
- 默认最小权限（CI 权限、云权限、K8s RBAC）

