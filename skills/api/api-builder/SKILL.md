---
name: api-builder
description: Generate complete FastAPI backend scaffolds from OpenAPI 3.x specifications. Automatically creates SQLAlchemy models, Pydantic schemas, FastAPI routers, CRUD operations, database migrations, pytest tests, and Next.js TypeScript clients. Use when user provides an OpenAPI/OpenSpec file (.yaml/.json) or pastes spec content, and wants to generate API code. Triggers on phrases like "generate API from spec", "build backend from OpenAPI", "create FastAPI from this spec", "implement these endpoints", or when user shares OpenAPI specification files. Supports Python 3.12+, FastAPI, SQLite, SQLAlchemy, Alembic, pytest, and Next.js App Router.
---

# API Builder

从 OpenAPI 3.x 规范自动生成完整的 FastAPI 后端脚手架，包括数据库模型、API 路由、测试和 Next.js client。

## 工作流程

### 阶段 1：验证输入

1. **获取 OpenAPI Spec**
   - 询问用户提供 OpenAPI spec：
     - 文件路径（.yaml 或 .json）
     - 粘贴 spec 内容（保存为临时文件）
     - URL（如果可访问，先下载）

2. **验证 Spec 格式**
   - 运行 `scripts/validate_spec.py`：
     ```bash
     python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_spec.py <spec-file>
     ```
   - 检查 exit code：0=成功，1=失败

   **如果验证失败**：停止并告知用户具体错误，询问是否修正

3. **选择生成范围**
   - 运行 `scripts/parse_openapi.py` 查看可用 endpoints：
     ```bash
     python3 ${CLAUDE_PLUGIN_ROOT}/scripts/parse_openapi.py <spec-file>
     ```
   - 询问用户：
     - 生成全部 endpoints？
     - 只生成特定的endpoints？（让用户选择，使用 `--resources` 参数）

### 阶段 2：检测现有项目结构

1. **检查是否为现有项目**
   - 查找 `app/` 或 `src/` 目录
   - 检查 `pyproject.toml`
   - 检查是否已有 `database.py`、`routers/`、`models/` 等

2. **确定集成策略**
   - **如果是现有项目**：
     - 复用现有的 `database.py`
     - 检查文件冲突（如 `app/routers/users.py` 已存在）
     - 询问用户如何处理冲突：覆盖/合并/重命名/跳过
   - **如果是新项目**：
     - 从 `assets/fastapi-template/` 复制基础结构
     - 创建完整的项目脚手架

### 阶段 3：生成后端代码

**使用 CLI 脚本（推荐）**：

运行完整的生成流程：
```bash
cd ${CLAUDE_PLUGIN_ROOT}/scripts
python3 cli.py \
  --spec <spec-file> \
  --output <output-dir> \
  [--resources users,posts]  # 可选：只生成特定资源
  [--conflict-strategy skip|backup|overwrite]  # 默认: skip
  [--dry-run]  # 预览模式，不写入文件
```

**冲突处理策略**：
- `skip`（默认）：跳过已存在的文件，不覆盖
- `backup`：备份已存在的文件后覆盖（推荐用于更新）
- `overwrite`：直接覆盖（危险！）

**预览模式**：使用 `--dry-run` 可以预览将要生成的文件，而不实际写入。

**生成内容**：
- `models/` - SQLAlchemy 数据库模型
- `schemas/` - Pydantic API schemas
- `routers/` - FastAPI 路由
- `__init__.py` - 包初始化文件
- `parsed.json` - 解析后的 spec 数据

**关键点**：
- 脚本自动处理类型映射（参考 `references/type-mapping.md`）
- 使用 Jinja2 模板（`assets/templates/`）生成代码
- 生成的代码包含 TODO comments 标记业务逻辑部分
- 添加时间戳字段（created_at, updated_at）
- Email 字段自动添加 unique 和 index

**手动步骤执行（高级）**：

如果需要更细粒度控制，可分步执行：

```bash
cd ${CLAUDE_PLUGIN_ROOT}/scripts

# 1. 解析 spec
python3 parse_openapi.py <spec-file> --output parsed.json

# 2. 生成代码
python3 generate_code.py \
  --parsed-data parsed.json \
  --output-dir <output-dir> \
  --templates-dir ${CLAUDE_PLUGIN_ROOT}/assets/templates
```

**参考文档**：
- `references/type-mapping.md` - 类型映射规则
- `references/fastapi-patterns.md` - FastAPI 最佳实践

#### 3.5 更新 Main.py

如果不存在 `app/main.py`，创建它：
- 从 `assets/fastapi-template/app/main.py` 复制基础结构
- 注册所有生成的 routers
- 配置 CORS 中间件
- 添加根路由

如果已存在，询问用户是否添加新的 router 注册代码。

#### 3.6 配置和运行数据库迁移（可选）

**使用 CLI（推荐）**：

```bash
# 自动配置并运行迁移
cd ${CLAUDE_PLUGIN_ROOT}/scripts
python3 cli.py \
  --spec <spec-file> \
  --output <output-dir> \
  --setup-alembic \
  --run-migrations
```

**手动执行**：

如果用户想手动控制：
```bash
# 1. 配置 Alembic
cd ${CLAUDE_PLUGIN_ROOT}/scripts
python3 cli.py --spec <spec-file> --output <output-dir> --setup-alembic

# 2. 进入项目目录手动运行迁移
cd <output-dir>
alembic revision --autogenerate -m "Initial tables"
alembic upgrade head
```

**生成内容**：
- `alembic.ini` - Alembic 配置文件
- `alembic/env.py` - 迁移环境配置
- `alembic/versions/` - 迁移文件目录
- `alembic/script.py.mako` - 迁移模板

**何时使用迁移**：
- 全新项目：使用 `--setup-alembic --run-migrations` 立即创建数据库
- 已有项目更新schema：手动运行 `alembic revision --autogenerate`
- 生产环境：先测试迁移，再手动应用

### 阶段 4：生成测试

#### 4.1 更新 conftest.py

- 检查 `tests/conftest.py` 是否存在
- 如果不存在，从 `assets/fastapi-template/tests/conftest.py` 复制
- 为每个资源添加 fixtures：
  - `sample_{resource}_data`
  - `create_sample_{resource}`
- 使用 `assets/templates/conftest_fixture.py.j2` 模板

#### 4.2 生成 API 集成测试

- 使用 `assets/templates/test_api.py.j2` 模板
- 生成到 `tests/test_api/test_{resource}_api.py`
- 包含测试：
  - CRUD 操作（create, get, update, delete）
  - 错误处理（404, 400, 422）
  - 分页、验证

**参考**：`references/testing-patterns.md`

#### 4.3 生成 CRUD 单元测试

- 使用 `assets/templates/test_crud.py.j2` 模板
- 生成到 `tests/test_crud/test_{resource}_crud.py`

### 阶段 5：生成 Next.js Client（可选）

询问用户是否需要生成 Next.js TypeScript client。

如果需要：

**使用 CLI（推荐）**：

```bash
cd ${CLAUDE_PLUGIN_ROOT}/scripts
python3 cli.py \
  --spec <spec-file> \
  --output <backend-output-dir> \
  --generate-client \
  [--client-output <frontend-path>/api-client.ts]
```

**单独生成Client**：

```bash
cd ${CLAUDE_PLUGIN_ROOT}/scripts
python3 generate_client.py \
  --parsed-data parsed.json \
  --output <client-output-file>
```

**生成内容**：
- TypeScript接口定义（从OpenAPI schemas）
- API调用方法（从OpenAPI paths）
- ApiClient类（包含错误处理）
- 便捷的函数导出

**参考**：`references/type-mapping.md` 的 TypeScript 映射

**生成的client使用示例**：
```typescript
// Next.js App Router
import { apiClient } from '@/lib/api/api-client'

export default async function Page() {
  const users = await apiClient.list_users()
  return <div>{users.map(u => <div>{u.name}</div>)}</div>
}
```

### 阶段 6：验证和测试

1. **安装依赖**：
   ```bash
   uv add fastapi sqlalchemy alembic pydantic[email] python-multipart
   uv add --dev pytest pytest-cov httpx
   ```

2. **运行类型检查**：
   ```bash
   mypy app/
   ```
   如果有错误，修复后重新检查。

3. **运行迁移**：
   ```bash
   alembic upgrade head
   ```

4. **运行测试**：
   ```bash
   pytest tests/ -v
   ```
   **目标**：所有测试通过

5. **手动验证**：
   - 启动服务器：`uvicorn app.main:app --reload`
   - 访问 API 文档：http://localhost:8000/docs
   - 测试几个 endpoints

### 阶段 7：完成

1. **生成总结文档**：
   - 列出所有生成的文件
   - 标记需要用户补充的 TODO 项
   - 提供下一步指南

2. **TODO 清单**：
   - [ ] 实现业务逻辑（routers 中的 TODO comments）
   - [ ] 添加认证/授权
   - [ ] 配置环境变量（`.env` 文件）
   - [ ] 补充关系字段（如果有）
   - [ ] 添加自定义验证逻辑

## 类型映射

详细的 OpenAPI 到 Python/TypeScript 类型映射见：**[references/type-mapping.md](references/type-mapping.md)**

快速参考：
- `string` → `str` / `string`
- `integer` → `int` / `number`
- `string(email)` → `EmailStr` / `string`
- `string(date-time)` → `datetime` / `string`
- `array` → `List[T]` / `Array<T>`
- `enum` → `Enum` / `enum` 或 `union type`

## 项目结构

生成的项目结构（模块化）：

```
project/
├── app/
│   ├── main.py              # FastAPI 应用入口
│   ├── database.py          # 数据库配置
│   ├── models/              # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   └── {resource}.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   └── {resource}.py
│   ├── routers/             # API 路由
│   │   ├── __init__.py
│   │   └── {resource}.py
│   └── crud/                # CRUD 操作
│       ├── __init__.py
│       ├── base.py
│       └── {resource}.py
├── alembic/                 # 数据库迁移
│   ├── versions/
│   └── env.py
├── tests/                   # 测试
│   ├── conftest.py
│   ├── test_api/
│   └── test_crud/
├── .env.example             # 环境变量示例
├── alembic.ini              # Alembic 配置
└── pyproject.toml           # 项目配置
```

详见：**[references/project-structure.md](references/project-structure.md)**

## 最佳实践

详细的 FastAPI 最佳实践见：**[references/fastapi-patterns.md](references/fastapi-patterns.md)**

关键模式：
- 使用依赖注入（`Depends(get_db)`）
- CRUD 基类继承模式
- 统一错误处理
- 响应模型验证
- 分页和查询参数

## 测试模式

详细的测试模式见：**[references/testing-patterns.md](references/testing-patterns.md)**

测试结构：
- `conftest.py` - 共享 fixtures（DB session, test client）
- `test_api/` - API 集成测试
- `test_crud/` - CRUD 单元测试

运行测试：
```bash
pytest tests/ -v --cov=app
```

## 错误处理

### 无效的 OpenAPI Spec
**症状**：YAML 解析错误、缺少必需字段

**处理**：
1. 停止生成
2. 显示具体错误信息
3. 询问用户是否修正或提供新 spec

### 文件冲突
**症状**：要生成的文件已存在

**处理**：
1. 列出冲突文件
2. 询问用户：覆盖/合并/重命名/跳过
3. 按用户选择执行

### 类型映射失败
**症状**：OpenAPI 类型无法映射到 Python

**处理**：
1. 使用默认类型（`Any`）
2. 添加 TODO comment
3. 提醒用户检查

### 测试失败
**症状**：pytest 报错

**处理**：
1. 分析错误信息
2. 修复代码
3. 重新运行测试
4. 如果 3 次尝试失败，询问用户

## 技术栈

- **Python**: 3.12+
- **Framework**: FastAPI
- **Database**: SQLite (via SQLAlchemy)
- **ORM**: SQLAlchemy
- **Migration**: Alembic
- **Validation**: Pydantic
- **Testing**: pytest, httpx
- **Package Manager**: uv
- **Frontend** (可选): Next.js (App Router) + TypeScript

## 示例使用场景

### 场景 1：从头创建新项目

**用户**："我有一个 petstore.yaml OpenAPI spec，帮我生成完整的 FastAPI 后端"

**执行**：
1. 读取 petstore.yaml
2. 验证格式
3. 询问是否生成全部 endpoints
4. 创建项目结构（从 assets/fastapi-template/）
5. 生成所有代码（models, schemas, routers, crud, tests）
6. 生成迁移
7. 运行测试验证
8. 提供总结和 TODO 清单

### 场景 2：集成到现有项目

**用户**："根据这个 spec（粘贴内容）生成 API，集成到现有项目"

**执行**：
1. 解析粘贴的 spec
2. 检测现有项目结构
3. 询问选择哪些 endpoints
4. 检查文件冲突
5. 生成新代码（避免覆盖已有文件）
6. 更新 main.py 注册新 routers
7. 更新测试
8. 运行测试验证

### 场景 3：只生成部分 endpoints

**用户**："从 spec 里只生成 /users 和 /posts 相关的 API"

**执行**：
1. 验证 spec
2. 显示所有可用 endpoints
3. 用户选择 /users 和 /posts
4. 只为这两个资源生成代码
5. 测试验证

## 注意事项

1. **认证/授权**：生成的代码**不包含**认证实现，只有 TODO 占位符
2. **业务逻辑**：CRUD 操作是脚手架，需要用户补充业务逻辑
3. **关系**：复杂的数据库关系需要用户手动调整
4. **环境变量**：记得配置 `.env` 文件
5. **生产部署**：生成的代码用于开发，生产环境需额外配置（如 Gunicorn、HTTPS、CORS 限制）

## 资源文件

- **references/type-mapping.md** - OpenAPI 到 Python/TypeScript 类型映射
- **references/project-structure.md** - 推荐的项目结构
- **references/fastapi-patterns.md** - FastAPI 最佳实践模式
- **references/testing-patterns.md** - 测试模式和最佳实践
- **assets/fastapi-template/** - FastAPI 项目基础模板
- **assets/templates/** - Jinja2 代码生成模板
