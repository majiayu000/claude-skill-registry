---
name: security-test-generator
description: 基于NFR安全要求，生成STRIDE/OWASP威胁模型和测试场景。L3级别专用，当设计和需求确认后使用。
stage: IMPLEMENTATION_PLANNING
level_supported: [L3]
---

## security-test-generator: 安全测试生成器

### 描述
基于CRAFT L3的NFR安全要求，生成STRIDE威胁模型和OWASP Top 10测试场景。确保应用安全性测试覆盖。

### 适用场景
- **WORKFLOW_STEP_5 Task S5-2**: 创建test_suites.md中的安全测试章节（L3专用）
- **WORKFLOW_STEP_5 Task S5-3**: Self-Reflection分析安全测试覆盖
- **L3项目**: 安全需求明确的系统

### 输入
- requirements/（特别是NFR中的安全要求）
- goal_breakdown.md（关键业务GOAL）
- design/architecture.md（架构设计，含安全边界）
- 应用类型（Web/API/移动/桌面等）

### 输出
- 安全测试计划报告（markdown）
- STRIDE威胁模型（Spoofing/Tampering/Repudiation/Information/Denial/Elevation）
- OWASP Top 10映射（SQL注入/身份认证/敏感数据/XML外部实体/访问控制等）
- 生成的安全测试场景（Given-When-Then格式）
- 关键安全验收条件

### 执行策略

**第1步: 提取安全NFR**
从requirements/NFR中识别安全需求，映射到安全维度：
- 认证: 用户身份验证方式（密码/OAuth/MFA等）
- 授权: 访问控制策略（RBAC/ABAC等）
- 加密: 数据加密需求（传输/存储）
- 审计: 日志记录和监控需求
- 合规: 法规要求（GDPR/PCI-DSS等）

**第2步: STRIDE威胁映射**
根据应用类型应用STRIDE框架：
| 威胁 | Web应用 | API | 移动应用 |
|------|--------|-----|---------|
| Spoofing | 身份冒充 | 令牌伪造 | 设备冒充 |
| Tampering | 数据篡改 | 请求篡改 | 本地数据篡改 |
| Repudiation | 操作否认 | 调用否认 | 操作否认 |
| Information | 信息泄露 | API响应泄露 | 本地存储泄露 |
| Denial | DoS攻击 | API限流绕过 | 资源耗尽 |
| Elevation | 权限提升 | 权限越界 | 沙箱逃逸 |

**第3步: OWASP Top 10映射**
为每个NFR安全需求映射OWASP风险：
- A01: 访问控制缺陷 → 授权NFR
- A02: 密码学失败 → 加密NFR
- A03: 注入 → 输入验证
- A04: 不安全设计 → 架构安全
- A05: 安全配置缺陷 → 部署安全
- A06: 易受攻击和过时组件 → 依赖安全
- A07: 身份认证失败 → 认证NFR
- A08: 软件和数据完整性失败 → 更新安全
- A09: 日志和监控失败 → 审计NFR
- A10: SSRF → 网络安全

**第4步: 生成测试场景**
为每个威胁生成Given-When-Then场景：
- 正常场景: 安全检查通过
- 异常场景: 尝试安全绕过（注入/越权/暴力等）
- 边界场景: 边界值测试

**第5步: L1/L2/L3分级**
- **L1**: 仅覆盖OWASP Top 3（注入/认证/访问控制）
- **L2**: 覆盖OWASP Top 7 + 基础STRIDE
- **L3**: 完整STRIDE + OWASP Top 10 + 合规要求

**第6步: 优先级排序**
- Critical: 影响数据安全或用户隐私
- High: 影响系统可用性或业务逻辑
- Medium: 影响用户体验或信息泄露
- Low: 边界情况或低风险场景

### 价值
- **SPEC组织**: 将安全需求转化为具体可测试的场景
- **Sec/QA**: 系统化的安全测试覆盖，符合行业标准
- **Dev**: 了解安全实现要求，提升代码安全性

### 验收标准（L3）
- 覆盖所有NFR安全要求
- STRIDE威胁完整映射
- OWASP Top 10各项至少1条测试场景
- 给定-当-那 格式清晰规范
- 优先级标注（Critical/High/Medium/Low）
