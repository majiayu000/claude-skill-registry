---
name: security
description: "Security review skill: comprehensive security checklist and patterns. Use when adding authentication, handling user input, working with secrets, or creating API endpoints."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
parent: quality
---

# 安全审查技能

> 关联 Agent: `security-reviewer`（安全审查主力）、`code-reviewer`（代码审查中的安全维度）

本技能确保所有代码遵循安全最佳实践，识别潜在漏洞。

## 快速参考

- **核心职责**: 确保代码遵循安全最佳实践，识别潜在漏洞
- **覆盖范围**: 密钥管理、输入验证、SQL 注入、认证授权、XSS/CSRF 防护、速率限制、敏感数据、依赖安全、命令注入、路径遍历
- **关键原则**: 安全不是可选项，有疑问时选择更安全的方案

## 触发条件

- 实现认证或授权
- 处理用户输入或文件上传
- 创建新的 API 端点
- 使用密钥或凭证
- 实现支付功能
- 存储或传输敏感数据
- 集成第三方 API

## 安全检查速查

| 类别         | 核心规则                            | 检查项                                     |
| ------------ | ----------------------------------- | ------------------------------------------ |
| **密钥管理** | 环境变量，不硬编码                  | `.env.local` 在 .gitignore，Git 历史无密钥 |
| **输入验证** | Schema 验证（zod/pydantic），白名单 | 文件上传限制（大小/类型/扩展名）           |
| **SQL 注入** | 参数化查询，不拼接 SQL              | ORM 正确使用                               |
| **认证授权** | httpOnly cookies，RBAC              | Token 不放 localStorage                    |
| **XSS**      | DOMPurify 净化，CSP 头              | 无未验证的动态渲染                         |
| **CSRF**     | CSRF Token，SameSite=Strict         | 状态变更操作有保护                         |
| **速率限制** | 所有 API 有限制                     | 昂贵操作更严格                             |
| **敏感数据** | 日志脱敏，通用错误消息              | 堆栈跟踪不暴露                             |
| **依赖**     | npm audit clean，Lock 已提交        | 启用 Dependabot                            |
| **命令注入** | execFile 非 exec，shell=False       | 不拼接用户输入                             |
| **路径遍历** | os.path.basename 过滤               | 不直接拼接路径                             |

## 子文件索引

| 文件                                         | 内容                                |
| -------------------------------------------- | ----------------------------------- |
| [owasp-patterns.md](./owasp-patterns.md)     | OWASP Top 10 详细防护模式和代码示例 |
| [verify-checklist.md](./verify-checklist.md) | 安全测试示例 + 部署前安全检查清单   |
| [cloud-security.md](./cloud-security.md)     | IAM、密钥管理、CI/CD、网络安全      |
| [config-audit.md](./config-audit.md)         | 配置审计清单                        |

## 参考资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Web 安全学院](https://portswigger.net/web-security)

---

> **记住**：安全不是可选项。一个漏洞可能危及整个平台。有疑问时，选择更安全的方案。
