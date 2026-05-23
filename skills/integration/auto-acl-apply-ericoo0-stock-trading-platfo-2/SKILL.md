---
name: auto-acl-apply
description: 用于自动生成 Neptune ACL 申请报文并直接发起申请。支持多环境（BOE, Online-CN, i18n-BD）、多区域选择、源/目标集群指定，并自动处理非 BOE 环境下的 Pre-release 申请。
---

# auto-acl-apply

## 概述
本 Skill 旨在自动化字节跳动内部 Neptune 平台的 ACL 申请流程。它通过接收核心元数据（PSM、方法名、集群等），自动组装成符合 Neptune API 规范的请求，并直接发起 HTTP 申请。

## 使用指引

### 0. 自动获取 JWT Token (推荐)
为了简化操作，Agent 可以使用 `playwright-extention` 自动从 Neptune 获取所需的 `x-jwt-token`。

#### 步骤：
1. **导航至 Neptune 页面**: 根据目标环境，使用 `browser_navigate` 访问以下 URL：
   - **BOE**: `https://cloud-boe.bytedance.net/neptune/service/bitable.domain.application/secure/config`
   - **Online-CN**: `https://cloud.bytedance.net/neptune/service/bitable.extend.application/`
   - **i18n-BD**: `https://cloud.byteintl.net/neptune/service/tiktok.feed.fyp_api/`
2. **抓取网络请求**: 页面加载后，使用 `browser_network_requests` 获取请求列表。
3. **提取 Token**: 在请求的 Headers 中寻找 `x-jwt-token` 或 `x-neptune-jwt-token`。
4. **使用 Token**: 将提取到的值作为 `--jwt` 参数传入后续脚本。

### 1. 准备参数
在调用此 Skill 之前，请确保已获取以下信息：
- **--source**: 调用方 PSM。支持逗号分隔的多选 (例如 `s1,s2`)。别名: `--caller`。
- **--target**: 被调用方 PSM。支持逗号分隔的多选 (例如 `t1,t2`)。别名: `--callee`。
- **--method**: RPC 方法路径。支持逗号分隔的多选 (例如 `m1,m2`)。
- **--env**: 申请的环境。可选: `BOE` (默认), `Online-CN`, `i18n-BD`。
- **--source-cluster**: 调用方集群。支持逗号分隔多选 (默认: `default`)。
- **--target-cluster**: 被调用方集群。支持逗号分隔多选 (默认: `default`)。
- **--cluster**: 同时设置 source 和 target 集群。支持逗号分隔多选。
- **--zones**: 申请的区域，支持逗号分隔的多选 (例如 `BOE`, 或 `CN,VA`)。默认: `BOE`。
- **--jwt**: Neptune `x-jwt-token`。也可通过环境变量 `NEPTUNE_JWT` 传入。
- **--cookie**: 可选。也可通过环境变量 `NEPTUNE_COOKIE` 传入。

### 2. 发起 ACL 申请

#### 示例 1: 批量申请 (多方法、多集群)
```bash
python3 .coco/skills/auto-acl-apply/scripts/apply_acl.py \
  --source "bitable.extend.application" \
  --target "bitable.domain.application" \
  --method "/api/m1, /api/m2" \
  --cluster "default, lf, hq" \
  --env "BOE"
```

#### 示例 2: 多个 PSM 组合申请
```bash
python3 .coco/skills/auto-acl-apply/scripts/apply_acl.py \
  --source "s1, s2" \
  --target "t1, t2" \
  --method "/api/info" \
  --env "Online-CN"
```
注意：这会发起 4 次 (2x2) 独立的 PSM 维度申请（若是非 BOE 环境则为 8 次，含 pre-release）。

### 3. 注意事项
1. **JWT Token**: 必须从 Neptune 平台手动获取（参考浏览器开发者工具中的 `x-jwt-token` Header）。
2. **自动化逻辑**: 脚本会根据指定的 `--env` 自动选择对应的 Neptune 域名及 Pre-release 申请逻辑。

## 资源说明

### scripts/
- `apply_acl.py`: 核心申请脚本，负责参数解析、环境映射及 API 请求发送。
