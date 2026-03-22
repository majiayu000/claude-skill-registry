---
name: api-pattern-extractor
description: API 模式提取工具。从捕获的流量中自动提取 API 模式、参数规范、认证方式、数据结构，生成 OpenAPI 规范和可复用代码。
version: 1.0
allowed-tools: Bash(neo:*), Bash(jq:*), Bash(python:*)
---

# API Pattern Extractor

从网站流量中自动提取 API 模式：
- **Endpoint 发现** - 识别所有 API 端点
- **参数推断** - 分析请求参数和响应结构
- **认证模式** - 识别认证方式（Cookie、Token、API Key）
- **依赖分析** - 发现 API 之间的数据依赖关系
- **OpenAPI 生成** - 自动生成 API 规范

## 核心功能

### 1. 从 Neo 捕获中提取

```bash
# 使用 neo 捕获数据
neo capture list target-site.com --json > captures.json

# 提取 API 模式
python ~/skills/api-pattern-extractor/tools/extract-patterns.py \
  --captures captures.json \
  --output patterns.yaml
```

### 2. 从 HAR 文件提取

```bash
# 导出 HAR
neo capture export target-site.com --format har > traffic.har

# 提取模式
python ~/skills/api-pattern-extractor/tools/har-to-openapi.py \
  --har traffic.har \
  --output openapi.yaml
```

### 3. 实时分析

```bash
# 监控模式
python ~/skills/api-pattern-extractor/tools/live-analyzer.py \
  --domain target-site.com \
  --watch
```

## 模式类型

### Endpoint 模式

```yaml
endpoints:
  - path: /api/v1/products
    method: GET
    parameters:
      - name: page
        type: integer
        default: 1
      - name: limit
        type: integer
        default: 20
      - name: category
        type: string
        required: false
    response:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: "#/components/schemas/Product"
        total:
          type: integer
        page:
          type: integer
```

### 认证模式

```yaml
authentication:
  type: bearer
  location: header
  header_name: Authorization
  token_prefix: "Bearer "
  refresh_endpoint: /api/auth/refresh
```

### 数据流模式

```yaml
data_flows:
  - name: add_to_cart
    steps:
      - endpoint: /api/cart/items
        method: POST
        requires:
          - product_id (from /api/products)
          - auth_token (from /api/auth/login)
        produces:
          - cart_id
      - endpoint: /api/cart/{cart_id}
        method: GET
        requires:
          - cart_id (from previous step)
```

## 命令详解

### extract-patterns

```bash
python extract-patterns.py [options]

选项:
  --captures FILE       捕获数据文件 (JSON)
  --har FILE           HAR 文件
  --domain DOMAIN      过滤特定域名
  --output FILE        输出文件
  --format FORMAT      输出格式 (yaml/json/openapi)
  --min-samples N      最小样本数 (默认: 2)
  --confidence LEVEL   置信度阈值 (0-1, 默认: 0.8)
```

### analyze-dependencies

```bash
python analyze-dependencies.py [options]

选项:
  --captures FILE      捕获数据文件
  --output FILE        输出文件
  --format FORMAT      输出格式 (json/dot/graphml)
```

### generate-openapi

```bash
python generate-openapi.py [options]

选项:
  --patterns FILE      模式文件
  --output FILE        输出文件
  --title STRING       API 标题
  --version STRING     API 版本
  --base-url URL       基础 URL
```

## 使用示例

### 电商网站 API 分析

```bash
# 1. 捕获购物流程
# 在浏览器中完成: 浏览 → 加购物车 → 结算 → 支付

# 2. 提取 API 模式
python ~/skills/api-pattern-extractor/tools/extract-patterns.py \
  --captures captures.json \
  --domain api.shop.com \
  --output shop-api-patterns.yaml

# 3. 分析购物流程依赖
python ~/skills/api-pattern-extractor/tools/analyze-dependencies.py \
  --captures captures.json \
  --output shop-deps.json

# 4. 生成 OpenAPI 规范
python ~/skills/api-pattern-extractor/tools/generate-openapi.py \
  --patterns shop-api-patterns.yaml \
  --title "Shop API" \
  --base-url https://api.shop.com \
  --output shop-openapi.yaml
```

### SaaS 平台 API 分析

```bash
# 1. 捕获认证流程
# 在浏览器中登录

# 2. 分析认证模式
python ~/skills/api-pattern-extractor/tools/analyze-auth.py \
  --captures captures.json \
  --output auth-patterns.yaml

# 3. 提取完整 API
python ~/skills/api-pattern-extractor/tools/extract-patterns.py \
  --captures captures.json \
  --domain api.saas.com \
  --output saas-api.yaml
```

## 输出结构

### 模式文件结构

```
api-patterns/
├── endpoints/          # 端点模式
│   ├── products.yaml
│   ├── cart.yaml
│   └── auth.yaml
├── schemas/            # 数据模型
│   ├── Product.yaml
│   ├── Cart.yaml
│   └── User.yaml
├── auth/               # 认证模式
│   └── bearer.yaml
├── flows/              # 数据流
│   ├── checkout.yaml
│   └── login.yaml
└── openapi.yaml        # 完整 OpenAPI 规范
```

## 高级功能

### 1. 智能推断

```bash
# 自动推断字段类型和约束
python extract-patterns.py \
  --captures captures.json \
  --infer-types \
  --infer-constraints \
  --infer-required
```

### 2. 去重和规范化

```bash
# 合并相似的端点
python extract-patterns.py \
  --captures captures.json \
  --deduplicate \
  --normalize-paths
```

### 3. 安全检测

```bash
# 检测敏感数据泄露
python analyze-security.py \
  --captures captures.json \
  --check-secrets \
  --check-pii
```

## 与其他 Skills 协作

### 配合 site-analyzer

```bash
# 1. Neo 捕获
neo capture list target-site.com --json > api-captures.json

# 2. 提取模式
python ~/skills/api-pattern-extractor/tools/extract-patterns.py \
  --captures api-captures.json \
  --output patterns.yaml

# 3. 生成知识
python ~/skills/knowledge-generator/tools/generate-skill.py \
  --patterns patterns.yaml \
  --output SKILL.md
```

## 参考资源

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [HAR Format](http://www.softwareishard.com/blog/har-12-spec/)
- [JSON Schema](https://json-schema.org/)