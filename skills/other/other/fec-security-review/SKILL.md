---
name: fec-security-review
description: Use when reviewing frontend security risks such as XSS, CSRF, sensitive data exposure, unsafe DOM APIs, untrusted user input, authentication/token handling, payment flows, file upload, CSP, dependency risk, or third-party scripts; Chinese triggers include 安全审查, 安全检查.
---

# 前端安全审查

## Purpose

识别前端代码中的客户端安全风险，并给出可执行修复建议。

## Procedure

1. 先确认审查面：用户输入、动态 HTML、URL 跳转、认证态、文件上传、支付/删除等敏感操作、第三方脚本和依赖。
2. 搜索高危模式：`dangerouslySetInnerHTML`、`v-html`、`innerHTML`、`document.write`、动态 script、未校验 redirect、明文 token。
3. 按风险类型审查：XSS、CSP、敏感数据、CSRF、依赖、输入校验和文件上传。
4. 高危问题标记为阻塞合并；前端校验只能改善体验，不能作为唯一安全边界。
5. 输出分级安全报告；报告格式见 [references/report-template.md](references/report-template.md)。

## Detailed References

- Load [references/security-checklist.md](references/security-checklist.md) for XSS, CSP, sensitive data, CSRF, dependency, and input validation details.
- Load [references/report-template.md](references/report-template.md) when writing the security review report.

## Constraints

- 不要为了方便开发而绕过安全机制。
- 不要依赖前端校验作为唯一安全防线。
- 不要信任任何来自客户端的数据。
- 发现高危问题时必须标记为阻塞合并。
- 与通用代码质量 review 分工：本 skill 关注威胁、攻击面和数据泄露。

## Expected Output

输出 CRITICAL/HIGH/MEDIUM/LOW 分级安全审查报告，每个问题关联具体文件和行号，给出修复建议；报告保存为 `reports/security-review-YYYY-MM-DD-HHmmss.md`。

## Related Skills / Boundary

- `fec-frontend-code-review` — 综合代码质量、架构和可维护性评审。
- `fec-accessibility-check` — 无障碍专项，不处理威胁建模。
- `fec-browser-storage` — 存储方案选择；敏感数据泄露风险仍以本 skill 为准。

## 与子代理的配合

需要结合 `npm audit`、OWASP 清单、Grep 高危 DOM/API 模式时，可委托 `frontend-security-reviewer` 子代理。
