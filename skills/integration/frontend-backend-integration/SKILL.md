---
name: frontend-backend-integration
description: 前后端对接。当用户需要检查前后端API对接、调试接口调用、确保数据格式一致时使用此技能。
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# 前后端对接

## 功能说明
此技能专门用于前后端API对接检查和调试，包括：
- 检查前后端接口文档
- 分析代码总结API规范
- 验证请求/响应格式一致性
- 确保数据结构正确映射
- 调试网络调用问题

## 使用场景
- "检查前后端对接是否正确"
- "前端调用后端API报错"
- "确保前后端数据格式一致"
- "调试接口调用问题"
- "新增API的对接工作"

## 对接流程

### 第一步：查看项目结构

首先了解项目的前后端目录结构：
```bash
# 查看前端目录
ls frontend/src/
ls frontend/src/api/
ls frontend/src/stores/

# 查看后端目录
ls backend/
ls backend/app/
```

### 第二步：查找或创建API文档

#### 优先查找现有文档
```bash
# 查找API文档
find docs/ -name "*api*" -o -name "*API*" -o -name "*接口*"
find backend/docs/ -type f
find frontend/docs/ -type f
```

#### 常见文档位置
- `docs/api-reference.md` - API参考文档
- `docs/frontend/` - 前端相关文档
- `backend/tests/test_*.py` - 后端测试文件（包含API行为）
- `backend/README.md` - 后端说明

### 第三步：分析后端API规范

#### 1. 查看后端主入口文件
```python
# backend/app/main.py 或类似文件
# 重点查找：
# - @app.get/post/put/delete 装饰器定义的路由
# - response_model 指定的响应格式
# - 参数定义（query, path, body）
```

#### 2. 查看Schema定义
```python
# backend/app/schemas.py
# 重点查找：
# - Pydantic模型定义
# - 字段类型和验证规则
# - ApiResponse格式
# - PaginatedResponse格式
```

#### 3. 查看测试文件
```python
# backend/tests/test_main.py
# 重点查找：
# - 测试请求的参数格式
# - 预期的响应格式
# - 断言检查的数据结构
```

### 第四步：分析前端API调用

#### 1. 查看API封装
```javascript
// frontend/src/api/index.js
// 重点查找：
// - baseURL配置
// - axios拦截器处理
// - 各个API方法的参数和返回值
```

#### 2. 查看Store状态管理
```javascript
// frontend/src/stores/*.js
// 重点查找：
// - API调用方式
// - 响应数据处理方式
// - 数据提取路径（res.data vs res.items）
```

#### 3. 查看页面组件
```vue
// frontend/src/views/*.vue
// 重点查找：
// - API调用时机
// - 数据使用方式
// - 错误处理
```

### 第五步：对比验证

#### 响应格式对照表

| 后端返回格式 | 前端应提取 | 验证点 |
|--------------|------------|--------|
| `ApiResponse {code, message, data}` | `res.data` | 前端是否用`.data` |
| `PaginatedResponse {items, total, page}` | `res.items`, `res.total` | 前端是否直接访问 |
| 嵌套对象 `{category: {id, name}}` | `item.category.name` | 组件是否正确访问 |
| 数组字段 `{tags: [...]}` | `item.tags.map()` | 是否作为数组处理 |

#### 端口配置验证

**后端配置**：
```python
# backend/app/config.py
# 查找 host, port 配置
# 默认通常是 0.0.0.0:8000
```

**前端代理配置**：
```javascript
// frontend/vite.config.js
// server.proxy['/api'] 应指向后端地址
// 例如：target: 'http://localhost:8000'
```

**前端baseURL**：
```javascript
// frontend/src/api/index.js
// baseURL 应为 '/api'（走代理）
```

### 第六步：检查清单

- [ ] 后端API端点路径与前端调用一致
- [ ] 请求方法（GET/POST/PUT/DELETE）匹配
- [ ] 请求参数名称和类型正确
- [ ] 响应格式处理正确（.data vs 直接访问）
- [ ] 数据字段映射正确（嵌套对象、数组）
- [ ] 错误处理覆盖异常情况
- [ ] CORS配置允许前端域名

## 常见问题

### 问题1：响应格式不一致

**症状**：前端获取不到数据，显示undefined

**原因**：后端有些API返回`ApiResponse`包装，有些直接返回数据

**解决方案**：
```javascript
// 检查后端返回格式，调整前端处理
// 如果是 ApiResponse 格式：
this.data = res.data

// 如果是直接返回格式：
this.data = res
```

### 问题2：CORS错误

**症状**：浏览器控制台显示CORS policy错误

**解决方案**：
```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 问题3：端口冲突

**症状**：前端启动后无法访问后端API

**解决方案**：
- 检查后端是否在正确端口运行（默认8000）
- 检查前端vite.config.js的proxy配置
- 使用`netstat -ano | findstr :8000`检查端口占用

### 问题4：字段名不匹配

**症状**：某些数据显示不正常

**解决方案**：
- 对比后端Schema定义和前端使用字段
- 检查snake_case vs camelCase转换
- 确认嵌套对象访问路径

## 实战案例

### 案例：Vue3 + FastAPI 对接

**后端（FastAPI）**：
```python
@app.get("/api/articles", response_model=PaginatedResponse)
async def list_articles(page: int = 1, page_size: int = 20):
    # 返回格式：{items: [...], total: 100, page: 1, page_size: 20, total_pages: 5}
    return PaginatedResponse(...)
```

**前端（Vue3 + Pinia）**：
```javascript
// stores/article.js
const res = await articleApi.getList({ page: 1, page_size: 20 })
// 直接访问，因为后端返回PaginatedResponse而不是ApiResponse
this.articles = res.items || []
this.pagination = {
  total: res.total || 0,
  page: res.page || 1,
  // ...
}
```

### 案例：React + Node.js 对接

**后端（Express）**：
```javascript
res.json({
  success: true,
  data: { items: [...], total: 100 }
})
```

**前端（React）**：
```javascript
const res = await api.get('/articles')
// 需要访问 .data.data.items
setItems(res.data.data.items)
```

## 文档模板

### API对接文档模板

```markdown
# 前后端API对接文档

## 服务地址
- 前端：http://localhost:5173
- 后端：http://localhost:8000
- API代理：/api -> http://localhost:8000/api

## API端点列表

### 文章列表
- **请求**：`GET /api/articles?page=1&page_size=20`
- **响应**：
  - 格式：直接 `PaginatedResponse`
  - 字段：`{items, total, page, page_size, total_pages}`

### 文章详情
- **请求**：`GET /api/articles/{id}`
- **响应**：
  - 格式：`ApiResponse {code, message, data}`
  - 数据在 `data` 字段中

## 数据结构

### 文章对象（列表）
```javascript
{
  id: number,
  title: string,
  slug: string,
  summary: string | null,
  cover_image: string | null,
  category: { id, name, slug } | null,
  tags: [{ id, name, slug }],
  author_name: string,
  views: number,
  published_at: string | null
}
```
```

## 注意事项

1. **响应格式不统一**：很多后端框架的列表接口直接返回分页数据，而详情接口返回包装格式
2. **日期格式**：后端通常返回ISO格式字符串，前端需要解析
3. **空值处理**：前端需要处理可能为null的字段
4. **错误处理**：确保拦截器正确处理HTTP错误状态
5. **类型安全**：使用TypeScript可以提前发现类型不匹配

## 工具推荐

- **API测试**：Postman, curl, HTTPie
- **网络抓包**：浏览器DevTools Network面板
- **文档生成**：FastAPI自动生成Swagger文档
- **类型检查**：TypeScript接口定义
