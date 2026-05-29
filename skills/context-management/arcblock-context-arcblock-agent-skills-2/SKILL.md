---
name: arcblock-context
description: Load ArcBlock company context (products, technical architecture, strategy) on demand. Use `/arcblock-context` to see available topics, or `/arcblock-context <topic>` to load specific context.
---

# ArcBlock Context

ArcBlock 公司知识库快速访问入口。

## Usage

```
/arcblock-context              # 显示可用主题列表
/arcblock-context <topic>      # 加载特定主题
/arcblock-context all          # 加载全部概览
```

## Workflow

### Step 1: 解析参数

检查用户是否提供了参数：
- 无参数 → 显示可用主题列表
- 有参数 → 加载对应上下文

### Step 2: 无参数时 - 显示可用主题

输出以下列表：

```
## ArcBlock 公司知识库

### 产品 (Products)
- `arcsphere` - AI-native 浏览器与 Shell
- `agent-fleet` - AI-native Blocklet 运行时
- `blocklet-server` - 部署平台
- `blocklet-developer` - 开发者心智模型
- `did-wallet` - 多链多资产身份钱包
- `docsmith` - AI-native 文档工具
- `paymentkit` - 抽象支付层
- `promotion-kits` - 增长驱动营销工具集
- `did-spaces` - 去中心化个人数据空间
- `did-connect` - 应用-钱包交互协议
- `did-names` - DID 原生域名系统
- `aigne` - AI 原生软件工程框架
- `aigne-hub` - LLM 后端统一管理服务
- `aistro` - AI 占星应用
- `discuss-kit` - 综合内容可组合 Blocklet
- `live-document` - AI Vibe Coding 时代的新出版形态

### 技术 (Technical)
- `afs` - Agentic File System
- `aine` - AI Native Engineering
- `did-capability` - 身份与能力
- `blocklet` - Blocklet/Chamber/Scaffold
- `abt-staking` - Staking for X 通用框架
- `nft-vc` - NFT 作为 Digital Twin
- `credittoken` - USD 计费合规设计
- `chain` - 链架构

### 战略 (Strategy)
- `strategy` - 公司战略方向

### 快捷方式
- `products` - 加载产品概览
- `technical` - 加载技术概览
- `all` - 加载全部概览

用法: `/arcblock-context <topic>`
示例: `/arcblock-context afs` 或 `/arcblock-context arcsphere`
```

### Step 3: 有参数时 - 加载上下文

根据参数加载对应文件：

| 参数 | 加载文件 |
|------|---------|
| **Products** | |
| `arcsphere` | `products/arcsphere.md` |
| `agent-fleet` | `products/agent-fleet.md` |
| `blocklet-server` | `products/blocklet-server.md` |
| `blocklet-developer` | `products/blocklet-developer.md` |
| `did-wallet` | `products/did-wallet.md` |
| `docsmith` | `products/docsmith.md` |
| `paymentkit` | `products/paymentkit.md` |
| `promotion-kits` | `products/promotion-kits.md` |
| `did-spaces` | `products/did-spaces.md` |
| `did-connect` | `products/did-connect.md` |
| `did-names` | `products/did-names.md` |
| `aigne` | `products/aigne.md` |
| `aigne-hub` | `products/aigne-hub.md` |
| `aistro` | `products/aistro.md` |
| `discuss-kit` | `products/discuss-kit.md` |
| `live-document` | `products/live-document.md` |
| **Technical** | |
| `afs` | `technical/afs.md` |
| `aine` | `technical/aine.md` |
| `did-capability` | `technical/did-capability.md` |
| `blocklet` | `technical/blocklet.md` |
| `abt-staking` | `technical/abt-staking.md` |
| `nft-vc` | `technical/nft-vc-design.md` |
| `credittoken` | `technical/credittoken-design.md` |
| `chain` | `technical/chain-architecture.md` |
| **Strategy** | |
| `strategy` | `strategy/README.md` |
| **快捷方式** | |
| `products` | `products/README.md` |
| `technical` | `technical/README.md` |
| `all` | `products/README.md` + `technical/README.md` + `strategy/README.md` |

### Step 4: 加载后输出摘要

读取文件后，输出：

```
✓ 已加载: <文件名>

<文件中的高密度摘要或核心内容>

---
提示: 你现在可以询问关于 <主题> 的任何问题。
```

## File Loading Priority

加载文件时按以下优先级查找：

1. **Project override**: `./.claude/arcblock-context/{path}`
2. **User override**: `~/.claude/arcblock-context/{path}`
3. **Plugin default**: This plugin's `{path}`

## Examples

### 查看可用主题
```
User: /arcblock-context
Claude: [显示完整主题列表]
```

### 加载特定产品
```
User: /arcblock-context arcsphere
Claude: ✓ 已加载: products/arcsphere.md
        [输出 ArcSphere 摘要]
```

### 加载技术概览
```
User: /arcblock-context technical
Claude: ✓ 已加载: technical/README.md
        [输出技术架构概览]
```

### 加载多个主题
```
User: /arcblock-context afs aine
Claude: ✓ 已加载: technical/afs.md, technical/aine.md
        [输出两个主题的摘要]
```

## Core Principles

加载上下文后，记住 ArcBlock 的核心原则：

- **一切皆 Blocklet**：任何服务端都是 Blocklet
- **一切皆可 Self-Host**：任何部件均可去中心化独立部署
- **一切 ID 皆 DID**：所有身份都用 DID，所有验证都用 VC
- **AFS + AINE 是"母体"**：其他产品都是自然衍生
