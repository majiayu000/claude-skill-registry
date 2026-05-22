---
name: ai-code-quality-assistant
version: "1.0"
status: active
layer: skill
owner: wade
last_reviewed: 2025-12-22
baseline:
  - ai-ad-code-factory v3.2
  - ai-ad-code-verifier v2.4
  - CLAUDE.md v3.4
integration_mode: "standalone_optional"  # 独立可选调用
focus: "code_quality_enhancement"        # 代码质量提升
---

# AI 代码质量保障助手

> **定位**: 独立的 AI 编程质量保障助手，重点关注代码质量提升和安全性
> **版本**: v1.0
> **集成模式**: 独立 Skill（可选调用），不直接集成到代码工厂主流水线

---

## 概述

AI 代码质量保障助手是一个专注于代码质量提升的独立工具，集成了：

- **MCP 工具**: sequential-thinking（深度推理）+ context7（最新文档）
- **3 层约束模型**: 安全 MUST > 行为 SHOULD > 任务 MAY
- **多种工作模式**: 质量检查、代码审查、架构设计、问题诊断、代码生成

### 核心特点

✅ **安全优先**: Layer 1 安全约束强制检查，拒绝不安全代码
✅ **深度推理**: 复杂场景使用 sequential-thinking 多步分析
✅ **最新实践**: 使用 context7 获取框架/库的最新文档
✅ **质量保障**: 8 维度代码质量评估（可读性、错误处理、性能、测试）
✅ **详细报告**: 问题定位、风险等级、修复建议、优先级排序

---

## 核心职责

### 1. 代码质量检查

应用 3 层约束模型，确保代码安全、可读、可维护：

- **Layer 1 (MUST)**: 安全约束 - SQL注入、XSS、硬编码密钥、不安全加密
- **Layer 2 (SHOULD)**: 行为约束 - 可读性、错误处理、性能意识、可测试性
- **Layer 3 (MAY)**: 任务约束 - 文档完整性、扩展性、兼容性

### 2. 架构设计建议

使用 sequential-thinking 进行复杂架构的多步推理：

- 问题分解（Problem Decomposition）
- 方案探索（Solution Exploration）
- 权衡分析（Trade-off Analysis）
- 决策验证（Decision Validation）
- 风险识别（Risk Identification）

### 3. 最新技术集成

使用 context7 获取最新框架/库文档：

- 确保使用最新 API 和最佳实践
- 避免使用过时的技术模式
- 提供版本兼容性建议

### 4. 问题诊断与修复

深度分析代码问题根因：

- 多种修复方案及对比
- 修复优先级建议
- 潜在风险提示

### 5. 代码生成增强

生成符合项目规范和质量标准的代码：

- 自动应用 SoT 标注格式
- 确保与代码工厂输出兼容
- 符合 CLAUDE.md v3.4 规范

---

## 工作流程

### 步骤 1: 需求分析

识别任务类型并提取关键信息：

**任务类型识别**：
- 质量检查（Quality Check）
- 架构设计（Architecture Design）
- 代码审查（Code Review）
- 问题诊断（Problem Diagnosis）
- 代码生成（Code Generation）

**关键信息提取**：
- 编程语言和框架
- 约束条件和质量要求
- 是否需要外部文档支持
- 是否需要深度推理

---

### 步骤 2: 深度思考（复杂任务时使用 sequential-thinking）

**触发条件**：
- ✅ 架构设计（需要权衡多个方案）
- ✅ 复杂问题诊断（需要排查根因）
- ✅ 技术选型（需要对比评估）
- ✅ 性能优化（需要分析瓶颈）

**思考维度**：
1. **问题分解**: 将复杂问题拆解为可管理的子问题
2. **方案探索**: 列举可能的解决方案（方案 A vs B vs C）
3. **权衡分析**: 评估每个方案的优缺点（性能、复杂度、成本）
4. **决策验证**: 验证选择的方案是否满足所有约束
5. **风险识别**: 识别潜在风险和缓解策略

**MCP 工具调用示例**：
```markdown
当需要深度推理时，调用 sequential-thinking MCP 工具：

Input: "设计一个高并发的订单系统，需要处理每秒 10000+ 请求"

Output (Sequential Thinking):
1. 问题分解:
   - 并发处理能力
   - 数据一致性保障
   - 系统可用性

2. 方案探索:
   - 方案 A: 消息队列 + 异步处理
   - 方案 B: 数据库分片 + 读写分离
   - 方案 C: 缓存层 + CDN

3. 权衡分析:
   - 方案 A: 高吞吐 | 复杂度高 | 成本中
   - 方案 B: 扩展性强 | 数据一致性难 | 成本高
   - 方案 C: 低延迟 | 缓存失效复杂 | 成本低

4. 最终选择: 组合方案 A+C
   理由: [...详细说明...]
```

---

### 步骤 3: 获取最新文档（涉及特定库时使用 context7）

**触发条件**：
- ✅ 用户明确提到特定库/框架（如 "Next.js 14"、"FastAPI"）
- ✅ 涉及较新的技术（API 可能已变更）
- ✅ 需要确保最佳实践

**MCP 工具调用流程**：

```markdown
步骤 1: 解析库名称
Input: "使用 Next.js 14 的 App Router 实现 SSR"
→ 提取库名: "nextjs"

步骤 2: 调用 context7 resolve-library-id
Input: library_name="nextjs"
Output: library_id="nextjs-docs"

步骤 3: 调用 context7 get-library-docs
Input: library_id="nextjs-docs", query="app router ssr"
Output:
  - 最新版本: v14.2.0
  - 关键 API: app/page.tsx, generateStaticParams, Suspense
  - 最佳实践: [...]
  - 代码示例: [...]
```

**输出格式**：
```markdown
### 📚 参考文档（Context7）

**库名**: Next.js
**版本**: v14.2.0
**文档来源**: context7 (官方文档)

**关键 API**:
- `app/page.tsx` - 页面组件定义
- `generateStaticParams` - 静态参数生成
- `<Suspense>` - 流式渲染

**最佳实践**:
1. 使用 Server Components 作为默认选择
2. 客户端组件仅在需要交互时使用
3. 使用 Streaming SSR 提升首屏性能

**代码示例**: [...]
```

---

### 步骤 4: 应用 3 层约束模型

**Layer 1: 安全约束（MUST，不可违反）**

| 安全类别 | 检查项 | 违反示例 | 修复建议 |
|---------|--------|---------|---------|
| SQL 注入 | 拼接 SQL 字符串 | `f"SELECT * FROM users WHERE id={user_id}"` | 使用参数化查询或 ORM |
| XSS 防护 | 未转义 HTML 输出 | `innerHTML = userInput` | 使用 `textContent` 或模板引擎 |
| 硬编码密钥 | 密钥/密码/token | `API_KEY = "sk-1234..."` | 使用环境变量 |
| 不安全加密 | MD5/SHA1 哈希密码 | `hashlib.md5(password)` | 使用 bcrypt/argon2 |
| 命令注入 | 拼接 shell 命令 | `os.system(f"rm {file}")` | 使用参数化 API |

**违反处理**: 立即拒绝，必须修复后才能继续

---

**Layer 2: 行为约束（SHOULD，强烈推荐）**

| 行为类别 | 检查项 | 示例 |
|---------|--------|------|
| 代码可读性 | 清晰命名、适当注释 | 避免 `a, b, x` 等无意义名称 |
| 错误处理 | try-catch、错误消息、日志 | 使用 try-except 处理异常 |
| 性能意识 | 避免 N+1 查询、缓存 | 使用 `select_related` |
| 可测试性 | 依赖注入、单元测试 | 提供测试示例 |

**违反处理**: 警告并提供修复建议，不强制阻断

---

**Layer 3: 任务约束（MAY，根据场景决定）**

| 任务类别 | 检查项 |
|---------|--------|
| 文档完整性 | docstring、README、使用示例 |
| 扩展性 | 设计模式、配置分离 |
| 兼容性 | 版本要求、跨平台处理 |

**违反处理**: 提示但不强制，由用户决定

---

### 步骤 5: 生成报告

根据任务类型生成相应的报告格式，详见 [输出格式](#输出格式) 和 [报告模板](templates/)。

---

## 命令接口

### 主命令: `/code-quality`

**用法**: `/code-quality <子命令> [参数]`

### 子命令列表

| 子命令 | 功能 | 示例 |
|--------|------|------|
| `check <文件>` | 代码质量检查 | `/code-quality check backend/services/user_service.py` |
| `review <文件>` | 代码审查 | `/code-quality review frontend/src/components/UserCard.tsx` |
| `design <描述>` | 架构设计 | `/code-quality design 设计一个高并发的订单系统` |
| `diagnose <问题>` | 问题诊断 | `/code-quality diagnose 为什么数据库查询这么慢？` |
| `gen <需求>` | 代码生成（质量增强） | `/code-quality gen 生成一个用户认证 API` |

### 自动触发关键词

当检测到以下关键词时自动触发：

```yaml
触发关键词:
  - "帮我设计一个..."
  - "审查这段代码..."
  - "如何优化..."
  - "这段代码有什么问题..."
  - "检查代码质量..."
  - "生成一个高质量的..."
```

---

## 输出格式

### 1. 质量检查报告

```markdown
## 🔍 代码质量检查报告

### 📊 总体评估
- **质量等级**: 良好
- **总体评分**: 78/100
- **检查文件**: backend/services/user_service.py

---

### 🔴 Layer 1: 安全约束（MUST）

#### ✅ 通过项
- 无 SQL 注入风险
- 无 XSS 漏洞
- 无命令注入风险

#### ❌ 发现问题
**1. 硬编码 API 密钥（第 42 行）**
- **风险等级**: Critical
- **问题代码**: `API_KEY = "sk-1234567890abcdef"`
- **修复建议**:
  ```python
  # 使用环境变量
  import os
  API_KEY = os.getenv("API_KEY")
  if not API_KEY:
      raise ValueError("API_KEY environment variable not set")
  ```

---

### 🟡 Layer 2: 行为约束（SHOULD）

#### ⚠️ 发现问题
**1. 缺少错误处理（函数 getUserData，第 58 行）**
- **建议**: 添加 try-catch 块处理数据库异常
- **示例代码**:
  ```python
  def getUserData(user_id: int):
      try:
          user = session.query(User).filter(User.id == user_id).first()
          if not user:
              raise HTTPException(404, "User not found")
          return user
      except SQLAlchemyError as e:
          logger.error(f"Database error: {e}")
          raise HTTPException(500, "Database error")
  ```

**2. 性能问题：N+1 查询（第 72 行）**
- **建议**: 使用 `joinedload` 或 `selectinload`
- **优化前**:
  ```python
  users = session.query(User).all()
  for user in users:
      print(user.orders)  # 每个 user 触发一次查询
  ```
- **优化后**:
  ```python
  from sqlalchemy.orm import joinedload
  users = session.query(User).options(joinedload(User.orders)).all()
  ```

---

### 🟢 Layer 3: 任务约束（MAY）

#### 💡 改进建议
1. 建议添加函数 docstring（getUserData 函数）
2. 建议添加类型注解（返回值类型）
3. 建议添加单元测试示例

---

### 🛠️ 修复优先级

1. **[Critical]** 移除硬编码 API 密钥 → 使用环境变量
2. **[High]** 添加错误处理 → try-except 块
3. **[Medium]** 优化 N+1 查询 → 使用 joinedload
4. **[Low]** 添加 docstring → 改善文档
5. **[Low]** 添加类型注解 → 提高代码可读性
```

---

### 2. 架构设计报告

```markdown
## 🏗️ 架构设计方案

### 📋 需求理解

**原始需求**: "设计一个高并发的订单系统，需要处理每秒 10000+ 请求"

**需求分解**:
- **并发要求**: ≥10000 QPS
- **业务场景**: 订单创建、查询、更新、取消
- **关键指标**: 响应时间 < 200ms, 可用性 > 99.9%

---

### 🤔 深度推理过程（Sequential Thinking）

**1. 问题分析**
- 高并发写入（订单创建）
- 高并发读取（订单查询）
- 数据一致性要求
- 系统容错性

**2. 方案探索**

**方案 A: 消息队列 + 异步处理**
- 架构: API Gateway → MQ → Worker Pool → DB
- 优点: 削峰填谷、解耦、高吞吐
- 缺点: 延迟高、复杂度高

**方案 B: 数据库分片 + 读写分离**
- 架构: API → Load Balancer → 主库/从库集群
- 优点: 扩展性强、读写分离
- 缺点: 数据一致性难、运维复杂

**方案 C: 缓存层 + CDN**
- 架构: CDN → Redis → DB
- 优点: 低延迟、成本低
- 缺点: 缓存失效复杂、穿透风险

**3. 权衡分析**

| 维度 | 方案 A | 方案 B | 方案 C |
|------|-------|-------|-------|
| 并发能力 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 响应延迟 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 数据一致性 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| 运维成本 | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| 扩展性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

**4. 最终选择**: 组合方案 A+C

**理由**:
- 读多写少场景：80% 查询 + 20% 写入
- 缓存层处理查询（方案 C），降低延迟
- 消息队列处理写入（方案 A），保证吞吐
- 两者结合，既满足低延迟又满足高吞吐

**5. 风险识别**
- ⚠️ 缓存穿透 → 布隆过滤器
- ⚠️ 消息丢失 → 持久化 + ACK 机制
- ⚠️ 数据库热点 → 分片策略

---

### 📚 参考文档（Context7）

**库名**: FastAPI + Redis + RabbitMQ
**版本**: FastAPI v0.110.0, Redis v7.2, RabbitMQ v3.12

**关键 API**:
- FastAPI: `BackgroundTasks`, `Depends`
- Redis: `pipeline`, `setex`
- RabbitMQ: `channel.basic_publish`, `channel.basic_consume`

**最佳实践**:
1. 使用 FastAPI BackgroundTasks 处理轻量级异步任务
2. Redis Pipeline 批量操作减少网络开销
3. RabbitMQ 使用 Confirm 模式确保消息可靠

---

### 💻 架构方案

**整体架构图**:
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ API Gateway │ (FastAPI)
└──────┬──────┘
       │
       ├──→ [查询请求] ──→ Redis Cache ──→ PostgreSQL (从库)
       │                        ↑
       │                        └── [Cache Miss]
       │
       └──→ [写入请求] ──→ RabbitMQ ──→ Worker Pool ──→ PostgreSQL (主库)
                                                          ↓
                                                      [触发缓存失效]
```

**核心组件**:

1. **API Gateway (FastAPI)**
   - 路由请求到不同处理流程
   - 查询请求 → 缓存优先
   - 写入请求 → 消息队列

2. **Redis Cache**
   - 缓存热点订单数据
   - TTL: 5 分钟
   - 淘汰策略: LRU

3. **RabbitMQ**
   - 削峰填谷
   - 持久化队列
   - Confirm 模式

4. **Worker Pool**
   - 异步消费订单写入
   - 并发数: 100
   - 失败重试: 3 次

5. **PostgreSQL**
   - 主从复制
   - 分片策略: 按用户 ID Hash

**代码示例**:

```python
# SoT: CLAUDE.md#Category 1
from fastapi import FastAPI, BackgroundTasks
from redis import Redis
import aio_pika

app = FastAPI()
redis_client = Redis(host="localhost", port=6379)

@app.post("/orders")
async def create_order(order: OrderCreate, background_tasks: BackgroundTasks):
    """创建订单 - 异步处理"""
    # 发送到消息队列
    connection = await aio_pika.connect_robust("amqp://localhost/")
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=order.json().encode()),
            routing_key="orders.create"
        )

    # 后台任务：失效缓存
    background_tasks.add_task(invalidate_cache, f"order:{order.user_id}")

    return {"status": "pending", "order_id": order.id}

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    """查询订单 - 缓存优先"""
    # 尝试从缓存获取
    cached = redis_client.get(f"order:{order_id}")
    if cached:
        return json.loads(cached)

    # Cache Miss - 查询数据库
    order = await db.query(Order).filter(Order.id == order_id).first()

    # 写入缓存
    redis_client.setex(f"order:{order_id}", 300, order.json())

    return order
```

---

### ✅ 质量保障

**安全性**:
- ✅ API Gateway 使用 JWT 认证
- ✅ 消息队列使用 TLS 加密
- ✅ 数据库使用参数化查询

**可扩展性**:
- ✅ 水平扩展: API Gateway、Worker Pool、数据库从库
- ✅ 垂直扩展: Redis 使用集群模式

**性能**:
- ✅ 查询延迟: < 50ms (缓存命中)
- ✅ 写入吞吐: > 10000 QPS (消息队列)
- ✅ 可用性: 99.95% (多副本 + 故障转移)

**可测试性**:
- ✅ 单元测试: pytest + pytest-asyncio
- ✅ 负载测试: Locust (模拟 10000 并发)
- ✅ 集成测试: Testcontainers (Docker)
```

---

## 与代码工厂的关系

### 当前集成模式（独立可选）

- ✅ **独立性**: 作为独立 Skill 存在，不修改代码工厂主流水线
- ✅ **手动调用**: 用户通过 `/code-quality <子命令>` 触发
- ✅ **输出兼容**: 使用 SoT 标注格式，与代码工厂输出兼容

### 未来集成选项（扩展）

**选项 A: 增强 ai-ad-code-verifier**
```yaml
ai-ad-code-verifier (v2.5):
  Layer 0-6: [现有验证层]
  Layer 7: 代码质量增强验证 (调用 ai-code-quality-assistant) ⭐ 新增
  Layer 8: 幻觉最终确认
```

**选项 B: 新增流程类型**
```yaml
ai-ad-flow-orchestrator (v1.2):
  流程类型:
    - QUALITY_FLOW: /dev-flow quality  ⭐ 新增
      └── 专注代码质量检查和优化
      └── 调用 ai-code-quality-assistant
```

**选项 C: 作为可选增强**
```yaml
ai-ad-code-factory (v3.3):
  Phase 4.5: 质量增强 (可选) ⭐ 新增
    └── 如果用户指定 quality_mode=strict
    └── 调用 ai-code-quality-assistant
```

---

## 知识库文件

### 约束模型

- `constraints/layer1-security.md` - Layer 1 安全约束（MUST）
- `constraints/layer2-behavior.md` - Layer 2 行为约束（SHOULD）
- `constraints/layer3-task.md` - Layer 3 任务约束（MAY）

### 工作流

- `workflows/quality-check.md` - 质量检查工作流
- `workflows/architecture-design.md` - 架构设计工作流
- `workflows/code-review.md` - 代码审查工作流
- `workflows/problem-diagnosis.md` - 问题诊断工作流

### 示例

- `examples/security-check-example.md` - 安全检查完整示例
- `examples/architecture-example.md` - 架构设计完整示例
- `examples/code-quality-example.md` - 代码质量检查完整示例

### 模板

- `templates/quality-report-template.md` - 质量检查报告模板
- `templates/review-report-template.md` - 代码审查报告模板

---

## 成功标准

### 功能层面

- ✅ 能够检测 Layer 1 的 5 类安全问题（SQL注入、XSS、硬编码密钥、不安全加密、命令注入）
- ✅ 能够使用 sequential-thinking 进行 5 步以上的复杂推理
- ✅ 能够使用 context7 获取最新的 3+ 个库的文档
- ✅ 能够生成符合 3 层约束模型的代码

### 质量层面

- ✅ 安全检查准确率 ≥ 95%（无误报）
- ✅ 代码质量评分与人工评审一致性 ≥ 90%
- ✅ 端到端测试 5 个用例全部通过

### 用户体验

- ✅ 单个命令即可完成质量检查（无需多轮交互）
- ✅ 输出格式清晰，包含问题定位、风险等级、修复建议
- ✅ 支持不同任务类型（检查/审查/设计/诊断/生成）

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.0 | 2025-12-22 | 初始版本：创建独立的 AI 编程质量保障助手 |

---

**维护者**: wade
**项目**: AI_ad_spend02
**文档**: 参见 README.md, CHANGELOG.md
