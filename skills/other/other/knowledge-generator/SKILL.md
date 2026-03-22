---
name: knowledge-generator
description: 知识库生成工具。将网站分析结果转化为可复用的 Skill 文档、测试用例、代码模板。支持自动化文档生成和知识提取。
version: 1.0
allowed-tools: Bash(python:*), Bash(jq:*), Bash(neo:*)
---

# Knowledge Generator

将网站分析结果转化为可复用知识：
- **Skill 文档生成** - 自动生成 Claude Code Skill
- **测试用例生成** - 生成 API 和 UI 测试
- **代码模板** - 生成可复用代码片段
- **工作流文档** - 生成操作流程文档

## 核心功能

### 1. Skill 文档生成

```bash
# 从分析结果生成 Skill
python ~/skills/knowledge-generator/tools/generate-skill.py \
  --api-patterns patterns.yaml \
  --visual-analysis visual.json \
  --output SKILL.md \
  --name "site-name-api"
```

### 2. 测试用例生成

```bash
# 生成 API 测试
python ~/skills/knowledge-generator/tools/generate-tests.py \
  --patterns patterns.yaml \
  --output tests/ \
  --format pytest

# 生成 UI 测试
python ~/skills/knowledge-generator/tools/generate-ui-tests.py \
  --visual visual.json \
  --output ui-tests/ \
  --format playwright
```

### 3. 代码模板生成

```bash
# 生成 API 客户端
python ~/skills/knowledge-generator/tools/generate-client.py \
  --openapi openapi.yaml \
  --language python \
  --output client.py

# 生成 TypeScript 类型
python ~/skills/knowledge-generator/tools/generate-types.py \
  --openapi openapi.yaml \
  --output types.ts
```

## 工作流

### 完整知识库生成

```bash
#!/bin/bash
# generate-knowledge.sh

SITE=$1
OUTPUT_DIR="knowledge/$SITE"

mkdir -p "$OUTPUT_DIR"/{docs,tests,code}

# 1. 生成 Skill 文档
python ~/skills/knowledge-generator/tools/generate-skill.py \
  --api-patterns "analysis/$SITE/patterns.yaml" \
  --visual-analysis "analysis/$SITE/visual.json" \
  --output "$OUTPUT_DIR/docs/SKILL.md" \
  --name "$SITE-api"

# 2. 生成 OpenAPI 规范
python ~/skills/knowledge-generator/tools/generate-openapi.py \
  --patterns "analysis/$SITE/patterns.yaml" \
  --output "$OUTPUT_DIR/docs/openapi.yaml"

# 3. 生成测试用例
python ~/skills/knowledge-generator/tools/generate-tests.py \
  --patterns "analysis/$SITE/patterns.yaml" \
  --output "$OUTPUT_DIR/tests/" \
  --format pytest

# 4. 生成代码模板
python ~/skills/knowledge-generator/tools/generate-client.py \
  --openapi "$OUTPUT_DIR/docs/openapi.yaml" \
  --language python \
  --output "$OUTPUT_DIR/code/client.py"

echo "知识库已生成: $OUTPUT_DIR"
```

## 输出模板

### Skill 文档模板

```markdown
---
name: {site-name}-api
description: {site-name} API 自动化操作指南
version: 1.0
allowed-tools: Bash(curl:*), Bash(browser-use:*)
---

# {Site Name} API

## 认证

{auth-section}

## 核心 API

### {endpoint-group}

{endpoint-details}

## 工作流

### {workflow-name}

{workflow-steps}

## 示例代码

{code-examples}
```

### 测试用例模板

```python
import pytest
import requests

class Test{EndpointName}:
    """{endpoint-description}"""

    @pytest.fixture
    def base_url(self):
        return "{base-url}"

    @pytest.fixture
    def auth_headers(self):
        return {"Authorization": "Bearer {token}"}

    def test_{operation}_success(self, base_url, auth_headers):
        """测试成功场景"""
        response = requests.{method}(
            f"{base_url}/{endpoint}",
            headers=auth_headers,
            json={request-body}
        )
        assert response.status_code == 200
        assert "expected_field" in response.json()
```

### 代码模板

```python
class {SiteName}Client:
    """{Site Name} API 客户端"""

    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        })

    {method-implementations}
```

## 命令详解

### generate-skill

```bash
python generate-skill.py [options]

选项:
  --api-patterns FILE     API 模式文件
  --visual-analysis FILE  视觉分析文件
  --flows FILE           数据流文件
  --output FILE          输出文件
  --name STRING          Skill 名称
  --description STRING   Skill 描述
  --template FILE        自定义模板
```

### generate-tests

```bash
python generate-tests.py [options]

选项:
  --patterns FILE      API 模式文件
  --output DIR        输出目录
  --format FORMAT     测试格式 (pytest/jest/playwright)
  --include-auth      包含认证测试
  --include-error     包含错误场景测试
```

### generate-client

```bash
python generate-client.py [options]

选项:
  --openapi FILE      OpenAPI 规范文件
  --language LANG     编程语言 (python/typescript/go/java)
  --output FILE       输出文件
  --async-client      生成异步客户端
```

## 分析合并

### 合并多种分析结果

```bash
# 合并 API 和视觉分析
python ~/skills/knowledge-generator/tools/merge-analysis.py \
  --api api-patterns.yaml \
  --visual visual-analysis.json \
  --flows data-flows.yaml \
  --output merged-analysis.json
```

**输出结构**：
```json
{
  "site": "example.com",
  "pages": [
    {
      "url": "/products",
      "ui_elements": [...],
      "api_triggers": [...]
    }
  ],
  "apis": [...],
  "workflows": [...],
  "schemas": [...]
}
```

### UI/API 映射

```bash
# 分析 UI 操作触发的 API
python ~/skills/knowledge-generator/tools/map-ui-api.py \
  --captures captures.json \
  --visual visual.json \
  --output ui-api-map.yaml
```

**输出示例**：
```yaml
mappings:
  - ui_element: "加入购物车按钮"
    api_call:
      endpoint: /api/cart/items
      method: POST
      payload:
        product_id: "${product_id}"
        quantity: 1
    triggers:
      - click
```

## 高级功能

### 1. 智能命名

```bash
# 自动推断 API 语义名称
python generate-skill.py \
  --patterns patterns.yaml \
  --infer-names \
  --name-style restful
```

### 2. 文档增强

```bash
# 添加详细描述和示例
python generate-skill.py \
  --patterns patterns.yaml \
  --enhance-docs \
  --include-examples
```

### 3. 多语言支持

```bash
# 生成多语言文档
python generate-skill.py \
  --patterns patterns.yaml \
  --language zh-CN \
  --output SKILL_zh.md
```

## 示例输出

### 完整 Skill 文档

```markdown
---
name: shop-api
description: Shop API 自动化操作，支持商品浏览、购物车管理、订单处理
version: 1.0
---

# Shop API

## 快速开始

### 认证
```bash
curl -X POST https://api.shop.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "xxx"}'
```

## 核心 API

### 商品列表
```bash
curl "https://api.shop.com/api/v1/products?page=1&limit=20"
```

### 加入购物车
```bash
curl -X POST https://api.shop.com/api/cart/items \
  -H "Authorization: Bearer {token}" \
  -d '{"product_id": 123, "quantity": 1}'
```

## 工作流

### 完整购物流程
1. 浏览商品: GET /api/v1/products
2. 加入购物车: POST /api/cart/items
3. 查看购物车: GET /api/cart
4. 创建订单: POST /api/orders
5. 支付: POST /api/payments
```

## 参考资源

- [OpenAPI Generator](https://openapi-generator.tech/)
- [Playwright Codegen](https://playwright.dev/python/docs/codegen)
- [pytest](https://docs.pytest.org/)