---
description: 同花顺 iFinD 专业金融数据 HTTP API 底层封装，是其他 ths-* skill 的共用底座。当需要直接调用同花顺 iFinD API 时使用。
---

# ths-skill

同花顺 iFinD 金融数据底层 JS 封装。

## 核心能力

- 同花顺 iFinD HTTP API 统一调用
- ACCESS_TOKEN 认证管理（从 .env 读取）
- 是 ths-edb-skill、insurance-skill 等的底层依赖

## 配置

```bash
# .env
THS_ACCESS_TOKEN=your_token_here
```

## 使用

```javascript
const ths = require("$SKILLS_ROOT/ths-skill/index.js");
// 调用 iFinD API
```

## 注意

- 需要同花顺 iFinD 专业版账号
- TOKEN 配置在项目根目录 .env 文件中
