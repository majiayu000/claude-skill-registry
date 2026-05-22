---
name: Security Specialist
description: 专注于应用安全、认证授权与合规性。
---

# Security Specialist Skills

## 🤖 智能体与 MCP 增强 (Agent & MCP Enhancements)

本 Skill 支持并推荐配合特定的智能体角色和 MCP 工具使用，以获得最佳效果。

### 推荐智能体角色
*   **Security Auditor**: 详见 [AGENTS.md](AGENTS.md)。
    *   该角色具备“零信任”和“攻击者视角”，能够主动发现潜在风险。
    *   启用后，AI 将强制执行 OWASP 安全检查清单。

### 推荐 MCP 工具
*   **Git MCP**: 用于扫描历史提交中的敏感信息泄露。
*   **Filesystem MCP**: 用于检查文件权限和 `.gitignore` 配置。

---

提供全方位的安全保障，确保应用符合安全标准与法规。

## 包含的技能模块

### 1. [安全需求提取 (Security Requirements)](./安全需求提取.md)
- **核心价值**: 在设计阶段识别安全风险。
- **关键技术**: 威胁建模, STRIDE 分析, 安全用户故事.
- **使用场景**: 新功能安全评审、架构设计。

### 2. [认证实现模式 (Authentication)](./认证实现模式.md)
- **核心价值**: 实现安全可靠的用户身份验证。
- **关键技术**: JWT, OAuth2, OIDC, Session 管理.
- **使用场景**: 登录注册系统开发、第三方登录集成。

### 3. [GDPR 数据处理 (GDPR Compliance)](./GDPR数据处理.md)
- **核心价值**: 确保数据处理符合 GDPR 等隐私法规。
- **关键技术**: 数据最小化, 被遗忘权实现, 数据加密.
- **使用场景**: 出海应用开发、隐私合规审计。

## 如何使用

- **登录设计**: "请参考认证实现模式，帮我设计一个安全的 JWT 登录流程。"
- **合规检查**: "请检查我的数据库字段设计是否符合 GDPR 要求。"
