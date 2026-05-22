---
name: ai-ad-test-gen
version: "2.2"
status: production
layer: skill
owner: wade
last_reviewed: 2025-12-07

sot_dependencies:
  required:
    - docs/sot/STATE_MACHINE.md
    - docs/sot/DATA_SCHEMA.md
    - docs/sot/BUSINESS_RULES.md
    - docs/sot/ERROR_CODES_SOT.md
  optional:
    - docs/sot/API_SOT.md
    - docs/3.dev-guides/TESTING_STRATEGY.md

output_boundaries:
  writable:
    - backend/tests/**
  forbidden:
    - backend/models/**
    - migrations/**

# SuperClaude Enhancement Configuration (v2.0)
enhancement:
  enabled: true
  superclaude_patterns:
    - test_strategy        # 吸收 /sc:test 测试金字塔与维度矩阵
    - analysis_pattern     # 吸收 /sc:analyze 覆盖度分析
    - task_breakdown       # 吸收 /sc:pm 测试阶段分解
  internal_workflow: true
  sot_priority: true       # SoT 检查结果优先级最高

baseline: AI_CODE_FACTORY_DEV_GUIDE_v2.4, SoT Freeze v2.6, SUPERCLAUDE_INTEGRATION_GUIDE_v2.2
---

# Test-Gen Skill - 测试用例生成

## 1. Purpose

测试用例生成 Skill，负责根据 SoT 文档和业务代码生成 pytest 测试用例。

**核心职责**:
- 根据 Service/Router 代码生成对应的测试用例
- 覆盖正向路径、边界条件、错误状态
- 生成状态机转换测试和账本不变量测试

## 2. Input Contract

```typescript
interface TestGenInput {
  task: string;           // 任务描述，如 "为充值审批 Service 生成测试"
  target_files: string[]; // 被测代码文件列表
  test_type?: "service" | "api" | "state_machine" | "ledger";  // 测试类型
  context?: {
    sot_snapshot?: Record<string, string>;  // SoT 文档内容快照
    source_code?: Record<string, string>;   // 被测代码快照
  };
}
```

**校验规则**:
- `task` 不能为空
- `target_files` 至少有一个文件
- 被测文件必须存在

## 3. Output Contract

```typescript
interface TestGenOutput {
  success: boolean;
  data?: {
    changes: Record<string, string>;  // 测试文件路径 -> 内容
    test_cases: TestCase[];           // 测试用例摘要
    coverage_notes: string[];         // 覆盖说明
  };
  error?: string;
}

interface TestCase {
  name: string;          // 测试函数名
  type: "happy_path" | "boundary" | "error" | "state_machine" | "ledger";
  description: string;   // 测试描述
  sot_ref?: string;      // 引用的 SoT 条款
}
```

## 4. Constraints (必须遵守的边界)

### 4.1 测试类型

| 类型 | 说明 | 位置 |
|------|------|------|
| **Service 层测试** | 单元测试，Mock 数据库 | `backend/tests/services/` |
| **API 层测试** | 集成测试，TestClient | `backend/tests/api/` |
| **状态机测试** | 状态转换规则验证 | `backend/tests/test_state_machine*.py` |
| **账本测试** | 余额不变量验证 | `backend/tests/test_ledger*.py` |

### 4.2 测试覆盖要求

**每个 Service 函数必须覆盖**:
1. **Happy Path** - 正向成功路径
2. **边界条件** - 空数据、极值、None
3. **错误状态** - 非法状态转换、权限不足
4. **SoT 约束** - 状态机、业务规则

### 4.3 测试命名规范

```python
# 格式: test_{功能}_{场景}
def test_approve_topup_success():  # Happy path
def test_approve_topup_wrong_status():  # 边界
def test_approve_topup_no_permission():  # 权限
```

## 5. Prompt Template

```xml
<SYSTEM>
你是"测试 Agent"，负责为 FastAPI + pytest 项目生成高质量的测试用例。

必须遵守的规则：
1. 测试必须覆盖正向路径、边界条件、错误状态
2. 状态机测试必须验证 STATE_MACHINE.md 中的转换规则
3. 错误码必须与 ERROR_CODES_SOT.md 一致
4. 账本测试必须验证 DATA_SCHEMA.md §3.4.4 中的不变量
5. 使用 pytest 标准结构，支持 async

技术栈假设：
- pytest
- pytest-asyncio
- httpx (AsyncClient)
- SQLAlchemy 2.x (async session)
</SYSTEM>

<CONTEXT>
<DOC name="STATE_MACHINE">
{{STATE_MACHINE}}
</DOC>

<DOC name="DATA_SCHEMA">
{{DATA_SCHEMA}}
</DOC>

<DOC name="BUSINESS_RULES">
{{BUSINESS_RULES}}
</DOC>

<DOC name="ERROR_CODES">
{{ERROR_CODES}}
</DOC>

<DOC name="TESTING_STRATEGY" optional="true">
{{TESTING_STRATEGY}}
</DOC>

<SOURCE_CODE>
{{SOURCE_CODE}}
</SOURCE_CODE>
</CONTEXT>

<TASK>
{{TASK}}
</TASK>

<THINKING_CHAIN>
请按以下步骤思考：

1. **分析被测代码**
   - 识别被测函数/端点
   - 提取入参、返回值、异常类型
   - 识别依赖的状态机和业务规则

2. **测试用例设计**
   - Happy Path: 正常成功场景
   - 边界条件: 空值、极值、None
   - 错误场景: 非法状态、权限不足、数据不存在
   - 状态机: 允许/禁止的状态转换
   - 账本: 余额不变量（如果涉及）

3. **测试代码生成**
   - 遵循 pytest 规范
   - 使用 fixture 管理测试数据
   - 使用 parametrize 减少重复
   - 添加 SoT 注释

4. **覆盖度检查**
   - 确保所有公开函数都有测试
   - 确保关键业务规则都有验证
   - 确保状态机转换有正反测试
</THINKING_CHAIN>

<OUTPUT_FORMAT>
只输出一段 JSON，格式如下：

{
  "changes": [
    {
      "file": "backend/tests/services/test_topup_service.py",
      "content": "完整的测试文件内容"
    },
    {
      "file": "backend/tests/api/test_topups_api.py",
      "content": "完整的测试文件内容"
    }
  ],
  "test_cases": [
    {
      "name": "test_approve_topup_success",
      "type": "happy_path",
      "description": "成功审批充值申请",
      "sot_ref": "STATE_MACHINE.md#topup"
    },
    {
      "name": "test_approve_topup_wrong_status",
      "type": "error",
      "description": "已审批状态不能再次审批",
      "sot_ref": "STATE_MACHINE.md#topup"
    }
  ],
  "coverage_notes": [
    "覆盖了 approve_topup 的所有状态转换",
    "验证了 ledger_entries 写入逻辑"
  ]
}
</OUTPUT_FORMAT>
```

## 6. Test Template Examples

### 6.1 Service 层测试模板

```python
"""
测试模块: topup_service
SoT 依赖: STATE_MACHINE.md#topup, BUSINESS_RULES.md#BR-TP-001
"""
import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

from backend.services.topup_service import approve_topup
from backend.schemas.topup import TopupStatus
from backend.core.exceptions import BusinessError, AuthError


class TestApproveTopup:
    """测试充值审批 Service"""

    @pytest.fixture
    def mock_db(self):
        """Mock 数据库会话"""
        return AsyncMock()

    @pytest.fixture
    def admin_user(self):
        """Admin 用户 fixture"""
        return MagicMock(id=uuid4(), role="admin")

    @pytest.fixture
    def pending_topup(self):
        """待审批充值记录 fixture"""
        return MagicMock(
            id=uuid4(),
            status=TopupStatus.PENDING,
            amount=10000.00
        )

    # Happy Path
    async def test_approve_success(self, mock_db, admin_user, pending_topup):
        """正向路径: 成功审批
        SoT: STATE_MACHINE.md#topup (pending → approved)
        """
        mock_db.get.return_value = pending_topup

        result = await approve_topup(mock_db, pending_topup.id, admin_user, {})

        assert result.status == TopupStatus.APPROVED
        assert result.approved_by == admin_user.id

    # 边界条件
    async def test_approve_wrong_status(self, mock_db, admin_user):
        """边界: 已审批状态不能再次审批
        SoT: STATE_MACHINE.md#topup (approved → approved 禁止)
        """
        approved_topup = MagicMock(status=TopupStatus.APPROVED)
        mock_db.get.return_value = approved_topup

        with pytest.raises(BusinessError) as exc:
            await approve_topup(mock_db, approved_topup.id, admin_user, {})

        assert exc.value.code == "TOPUP_002"

    # 权限检查
    async def test_approve_no_permission(self, mock_db, pending_topup):
        """边界: 普通用户无审批权限
        SoT: AUTH_SPEC.md (role: admin/finance 可审批)
        """
        media_buyer = MagicMock(role="media_buyer")
        mock_db.get.return_value = pending_topup

        with pytest.raises(AuthError) as exc:
            await approve_topup(mock_db, pending_topup.id, media_buyer, {})

        assert exc.value.code == "AUTH_500"
```

### 6.2 API 层测试模板

```python
"""
测试模块: topups API
SoT 依赖: API_SOT.md#topups
"""
import pytest
from httpx import AsyncClient

from backend.main import app


class TestTopupApproveAPI:
    """测试充值审批 API"""

    @pytest.fixture
    async def client(self):
        """HTTP 客户端 fixture"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac

    # Happy Path
    async def test_approve_api_success(self, client, admin_token, test_topup_id):
        """API: 成功审批返回 200"""
        response = await client.post(
            f"/api/v1/topups/{test_topup_id}/approve",
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        assert response.status_code == 200
        assert response.json()["status"] == "approved"

    # 错误响应
    async def test_approve_api_forbidden(self, client, media_buyer_token, test_topup_id):
        """API: 无权限返回 403"""
        response = await client.post(
            f"/api/v1/topups/{test_topup_id}/approve",
            headers={"Authorization": f"Bearer {media_buyer_token}"}
        )

        assert response.status_code == 403
        assert response.json()["detail"]["code"] == "AUTH_500"
```

### 6.3 状态机测试模板

```python
"""
测试模块: Topup 状态机转换
SoT 依赖: STATE_MACHINE.md#topup
"""
import pytest

from backend.services.state_machine import can_transition, TopupStatus


class TestTopupStateMachine:
    """验证 Topup 状态机转换规则"""

    @pytest.mark.parametrize("from_state,to_state,expected", [
        # 允许的转换
        (TopupStatus.PENDING, TopupStatus.APPROVED, True),
        (TopupStatus.PENDING, TopupStatus.REJECTED, True),
        (TopupStatus.APPROVED, TopupStatus.EXECUTED, True),
        (TopupStatus.APPROVED, TopupStatus.FAILED, True),
        # 禁止的转换
        (TopupStatus.APPROVED, TopupStatus.PENDING, False),
        (TopupStatus.REJECTED, TopupStatus.APPROVED, False),
        (TopupStatus.EXECUTED, TopupStatus.PENDING, False),
    ])
    def test_state_transitions(self, from_state, to_state, expected):
        """验证状态转换规则
        SoT: STATE_MACHINE.md#topup
        """
        assert can_transition("topup", from_state, to_state) == expected
```

## 7. Self-Check Checklist

| 检查项 | 验证方法 | P0/P1 |
|--------|---------|-------|
| Happy Path 覆盖 | 每个公开函数至少一个 | P0 |
| 错误码验证 | 对比 ERROR_CODES_SOT | P0 |
| 状态机覆盖 | 允许/禁止转换都测试 | P0 |
| Fixture 复用 | 使用 conftest.py | P1 |
| Async 支持 | pytest-asyncio marker | P1 |

## 8. Version History

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0 | 2025-12-06 | 重构：对齐 AI_CODE_FACTORY_DEV_GUIDE_v2.0，增加测试模板 |
| v1.0 | 2025-11-01 | 初始版本 |

---

**文档控制**: Owner: wade | Baseline: AI_CODE_FACTORY_DEV_GUIDE_v2.0
