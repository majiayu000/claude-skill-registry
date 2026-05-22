---
name: python-fastapi-dev
description: Python FastAPI 开发规范和最佳实践指南。适用于现代Web应用开发，涵盖项目架构、编码规范、异步编程、测试、部署等全方位内容。
---

# Python FastAPI 开发规范

## 技术栈

本项目基于 **FastAPI + SQLAlchemy + Pydantic + Alembic + PostgreSQL + Redis**

## 核心原则

- **PEP 8 编码规范**：Python代码风格指南
- **SOLID 原则**：单一职责、开闭原则、里氏替换、接口隔离、依赖倒置
- **DRY 原则**：Don't Repeat Yourself，避免代码重复
- **KISS 原则**：Keep It Simple, Stupid，保持简单
- **YAGNI 原则**：You Aren't Gonna Need It，不要过度设计
- **强制类型注解**：所有函数必须使用Type Hints
- **测试覆盖率**：单元测试覆盖率 ≥ 80%

## 项目架构

### 模块划分

```
project-root/
├── app/
│   ├── core/           # 核心配置模块
│   │   ├── config.py   # 配置管理
│   │   ├── security.py # 安全相关
│   │   └── deps.py     # 依赖注入
│   ├── api/            # API路由模块
│   │   ├── v1/         # API版本
│   │   └── deps.py     # API依赖
│   ├── services/       # 业务逻辑模块
│   ├── repositories/   # 数据访问模块
│   ├── models/         # 数据模型模块
│   │   ├── sqlalchemy/ # SQLAlchemy模型
│   │   └── pydantic/   # Pydantic模型
│   ├── utils/          # 工具函数模块
│   └── main.py         # 应用入口
├── alembic/            # 数据库迁移
│   └── versions/       # 迁移版本
├── tests/              # 测试模块
│   ├── unit/           # 单元测试
│   ├── integration/    # 集成测试
│   └── conftest.py     # 测试配置
├── scripts/            # 脚本目录
└── doc/                # 文档目录
    ├── sql/            # SQL文档
    └── api/            # API文档
```

## 分层架构规范

### API层 (`app/api`)

**职责**：
- 请求处理和响应
- 参数校验
- **禁止**编写业务逻辑

**调用规范**：
- 只能调用 `app/services` 下的Service方法
- 禁止直接调用Repository层

**路由规范**：
- 支持GET、POST、PUT、DELETE、PATCH
- 使用Pydantic模型进行参数验证
- 统一HTTP状态码和JSON响应
- 路径规范：
  - 管理接口: `/api/v1/admin/`
  - 用户接口: `/api/v1/users/`
  - 公共接口: `/api/v1/public/`

**示例**：
```python
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.user_service import UserService
from app.models.pydantic.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """创建用户"""
    return await user_service.create_user(user_data)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """获取用户信息"""
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user
```

### Service层 (`app/services`)

**职责**：
- 业务逻辑实现
- 数据验证
- 权限控制
- 事务协调

**调用规范**：
- Service层通过Repository访问数据
- 禁止直接操作数据库
- 入参和返参使用Pydantic模型
- **所有方法必须支持异步操作**

**设计原则**：
- 一个业务领域一个Service
- 一个功能一个方法
- 避免Service之间相互调用

**示例**：
```python
from typing import Optional
from app.repositories.user_repository import UserRepository
from app.models.pydantic.user import UserCreate, UserResponse
from app.core.security import hash_password

class UserService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """创建用户"""
        # 业务逻辑
        await self._validate_username(user_data.username)
        
        # 密码加密
        hashed_password = hash_password(user_data.password)
        
        # 创建用户
        user = await self._user_repo.create(user_data, hashed_password)
        
        return UserResponse.from_orm(user)
    
    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """根据ID获取用户"""
        user = await self._user_repo.get_by_id(user_id)
        if user:
            return UserResponse.from_orm(user)
        return None
    
    async def _validate_username(self, username: str) -> None:
        """验证用户名"""
        if len(username) < 3:
            raise ValueError("用户名长度至少3位")
        
        existing_user = await self._user_repo.get_by_username(username)
        if existing_user:
            raise ValueError("用户名已存在")
```

### Repository层 (`app/repositories`)

**职责**：
- 封装数据库访问
- 提供数据持久化抽象
- 复杂查询实现

**调用规范**：
- 仅供Service层调用
- 禁止API层直接调用
- 使用SQLAlchemy进行ORM操作
- 复杂查询使用原生SQL
- **必须支持事务管理**
- **使用asyncio和异步数据库驱动**

**设计原则**：
- 一个实体一个Repository
- 可组合调用其他Repository
- 避免循环依赖

**示例**：
```python
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sqlalchemy.user import UserModel

class UserRepository:
    def __init__(self, db: AsyncSession):
        self._db = db
    
    async def create(
        self, 
        user_data: UserCreate, 
        hashed_password: str
    ) -> UserModel:
        """创建用户"""
        user = UserModel(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password
        )
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        return user
    
    async def get_by_id(self, user_id: int) -> Optional[UserModel]:
        """根据ID获取用户"""
        result = await self._db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[UserModel]:
        """根据用户名获取用户"""
        result = await self._db.execute(
            select(UserModel).where(UserModel.username == username)
        )
        return result.scalar_one_or_none()
    
    async def list_users(
        self, 
        skip: int = 0, 
        limit: int = 10
    ) -> List[UserModel]:
        """获取用户列表"""
        result = await self._db.execute(
            select(UserModel).offset(skip).limit(limit)
        )
        return result.scalars().all()
```

### Model层 (`app/models`)

**职责**：
- SQLAlchemy模型：数据库表结构定义，仅用于数据持久化
- Pydantic模型：数据验证和序列化，用于API输入输出
- DTO模型：数据传输对象，用于层间数据传递

**命名规范**：
- SQLAlchemy: `{Entity}Model`
- Pydantic: `{Entity}Schema`、`{Entity}Create`、`{Entity}Update`

**SQLAlchemy模型示例**：
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class UserModel(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

**Pydantic模型示例**：
```python
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=6, max_length=50)
    
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含至少一个数字')
        return v

class UserUpdate(BaseModel):
    """用户更新模型"""
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True
```

## 编码规范

### PEP 8 规范

```python
# 缩进：使用4个空格，禁止使用Tab
# 行长度：每行最多88个字符（Black格式化器标准）

# 命名规范
user_name = "test"              # 变量和函数：snake_case
class UserService:               # 类名：PascalCase
    pass

MAX_RETRY_COUNT = 3              # 常量：UPPER_SNAKE_CASE
_private_field = "value"         # 私有属性：_leading_underscore

# 导入顺序
import os                        # 标准库导入
import sys
from datetime import datetime

from fastapi import FastAPI     # 第三方库导入
from sqlalchemy.orm import Session

from app.core.config import settings   # 本地模块导入
from app.models.user import UserModel
```

### 类型注解规范

```python
from typing import Optional, List, Dict, Union, Any
from pydantic import BaseModel

# 函数类型注解
async def get_user_by_id(user_id: int) -> Optional[UserResponse]:
    """根据ID获取用户信息"""
    user = await user_repository.get_by_id(user_id)
    if user:
        return UserResponse.from_orm(user)
    return None

# 复杂类型注解
from typing import TypedDict

class UserFilters(TypedDict):
    username: Optional[str]
    email: Optional[str]
    is_active: Optional[bool]

async def list_users(
    filters: UserFilters,
    skip: int = 0,
    limit: int = 10
) -> List[UserResponse]:
    """获取用户列表"""
    users = await user_repository.list_users(filters, skip, limit)
    return [UserResponse.from_orm(user) for user in users]

# 类属性类型注解
class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo: UserRepository = user_repo
```

### 文档字符串规范

```python
def create_user(
    user_data: UserCreate,
    user_repo: UserRepository
) -> UserResponse:
    """创建新用户
    
    Args:
        user_data: 用户创建数据
        user_repo: 用户仓储
    
    Returns:
        创建的用户信息
    
    Raises:
        ValueError: 当用户数据无效时
        UserExistsError: 当用户已存在时
    """
    # 验证用户数据
    if not user_data.username or len(user_data.username) < 3:
        raise ValueError("用户名长度至少3位")
    
    # 检查用户是否已存在
    existing_user = await user_repo.get_by_username(user_data.username)
    if existing_user:
        raise UserExistsError("用户名已存在")
    
    # 创建用户
    user = await user_repo.create(user_data)
    return UserResponse.from_orm(user)
```

## 依赖管理

### Poetry使用

**依赖定义**：
```toml
# pyproject.toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "My FastAPI Project"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.0"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
sqlalchemy = "^2.0.0"
alembic = "^1.12.0"
pydantic = "^2.5.0"
pydantic-settings = "^2.1.0"
python-jose = {extras = ["cryptography"], version = "^3.3.0"}
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
python-multipart = "^0.0.6"
redis = "^5.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
httpx = "^0.25.0"
black = "^23.11.0"
isort = "^5.12.0"
mypy = "^1.7.0"
```

**虚拟环境**：
```bash
# 创建虚拟环境
poetry install

# 激活虚拟环境
poetry shell

# 运行命令
poetry run uvicorn app.main:app --reload
```

### 包导入规范

```python
# 标准库导入
import os
import sys
from datetime import datetime, timedelta
from typing import List, Optional

# 第三方库导入
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

# 本地模块导入
from app.core.config import settings
from app.models.user import UserModel
from app.repositories.user_repository import UserRepository
```

## 异常处理

### 异常分类

```python
class BusinessException(Exception):
    """业务逻辑异常"""
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(message)

class ValidationError(BusinessException):
    """数据验证异常"""
    def __init__(self, message: str):
        super().__init__(400, message)

class DatabaseError(Exception):
    """数据库操作异常"""
    pass

class AuthenticationError(BusinessException):
    """认证异常"""
    def __init__(self, message: str = "认证失败"):
        super().__init__(401, message)

class AuthorizationError(BusinessException):
    """授权异常"""
    def __init__(self, message: str = "权限不足"):
        super().__init__(403, message)
```

### 异常处理原则

```python
from app.core.exceptions import BusinessException
from fastapi import Request
from fastapi.responses import JSONResponse

# 全局异常处理器
async def business_exception_handler(
    request: Request, 
    exc: BusinessException
):
    """业务异常处理"""
    return JSONResponse(
        status_code=exc.code,
        content={
            "code": exc.code,
            "message": exc.message,
            "data": None
        }
    )

async def database_exception_handler(
    request: Request,
    exc: DatabaseError
):
    """数据库异常处理"""
    logger.error(f"数据库异常：{str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "系统异常，请稍后重试",
            "data": None
        }
    )

# Service层异常处理
async def get_user(user_id: int, user_repo: UserRepository) -> UserResponse:
    try:
        user = await user_repo.get_by_id(user_id)
        if not user:
            raise BusinessException(404, f"用户 {user_id} 不存在")
        return UserResponse.from_orm(user)
    except DatabaseError as e:
        logger.error(f"数据库查询失败: {e}", exc_info=True)
        raise
```

## 日志记录

### 日志配置

```python
import logging
from app.core.config import settings

# 日志格式配置
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)

logger = logging.getLogger(__name__)
```

### 日志使用

```python
# 信息日志
logger.info(f"用户 {user_id} 登录成功")

# 错误日志
logger.error(f"用户创建失败: {str(e)}", exc_info=True)

# 调试日志
logger.debug(f"查询参数: {query_params}")

# 警告日志
logger.warning(f"用户 {user_id} 尝试访问未授权资源")
```

## 测试规范

### 测试结构

```
tests/
├── unit/               # 单元测试
│   ├── test_service.py
│   └── test_repository.py
├── integration/        # 集成测试
│   ├── test_api.py
│   └── test_database.py
└── conftest.py         # 测试配置
```

### 测试编写

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """测试用户创建"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    response = await client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_create_user_duplicate(client: AsyncClient):
    """测试用户名重复"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    # 第一次创建
    await client.post("/api/v1/users/", json=user_data)
    # 第二次创建相同用户
    response = await client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400
    assert "用户名已存在" in response.json()["message"]
```

## 严格禁止事项

1. **直接数据库操作**：禁止在Service层直接使用SQLAlchemy Session
2. **同步代码**：禁止在异步环境中使用同步代码
3. **硬编码**：禁止硬编码配置信息，必须使用环境变量
4. **无类型注解**：禁止编写无类型注解的函数和方法
5. **循环导入**：避免模块间的循环导入
6. **全局变量**：避免使用全局变量，使用依赖注入

## 性能优化

### 异步编程

```python
import asyncio

# 异步函数：所有I/O操作必须使用异步函数
async def get_users_data(user_ids: List[int]) -> List[UserResponse]:
    """获取多个用户数据（并发）"""
    tasks = [get_user_by_id(user_id) for user_id in user_ids]
    users = await asyncio.gather(*tasks, return_exceptions=True)
    return [user for user in users if isinstance(user, UserResponse)]

# 连接池：使用数据库连接池管理连接
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

### 缓存策略

```python
from app.core.redis import redis_client

async def get_user_by_id(user_id: int) -> Optional[UserResponse]:
    """获取用户（带缓存）"""
    # 先查缓存
    cache_key = f"user:{user_id}"
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return UserResponse.parse_raw(cached_data)
    
    # 查数据库
    user = await user_repository.get_by_id(user_id)
    if not user:
        return None
    
    response = UserResponse.from_orm(user)
    
    # 写缓存（7天过期）
    await redis_client.setex(
        cache_key,
        60 * 60 * 24 * 7,
        response.json()
    )
    
    return response
```

## 代码质量工具

### 格式化工具

```toml
# pyproject.toml

[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
```

### 静态检查

```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

### 配置示例

```bash
# 代码格式化
poetry run black app tests
poetry run isort app tests

# 类型检查
poetry run mypy app

# 安全检查
poetry run bandit -r app

# 代码风格检查
poetry run flake8 app
```

## 最佳实践总结

### 关注点分离
- API层专注请求处理
- Service层专注业务逻辑
- Repository层专注数据访问

### 可维护性
- 强制使用类型注解
- 完善的文档字符串
- 统一的异常处理
- 完整的日志记录

### 性能优化
- 异步编程
- 批量操作
- 合理使用缓存
- 连接池管理
