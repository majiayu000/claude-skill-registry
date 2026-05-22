---
name: ssl_checker
description: 查询域名的SSL证书信息，包括到期时间、颁发者等详情
---

# SSL 证书查询

查询指定域名的 SSL 证书信息，包括到期时间、剩余天数、颁发者等。

## 使用方法

- "查询 example.com 的 SSL 证书"
- "example.com 证书什么时候到期"
- "检查 example.com 的 HTTPS 证书"

## 返回信息

- 证书到期时间
- 剩余有效天数
- 证书颁发者
- 证书状态（正常/即将到期/已过期）

## 实现

使用 `scripts/execute.py` 通过 SSL 连接获取证书信息。