---
name: ai-ad-fe-gen
version: "2.5"
status: production
layer: skill
owner: wade
last_reviewed: 2025-12-24

sot_dependencies:
  required:
    - docs/sot/API_SOT.md
    - docs/sot/STATE_MACHINE.md
    - docs/3.dev-guides/COMPONENT_REGISTRY.md  # 组件注册表 (71 个组件)
  optional:
    - docs/3.dev-guides/FRONTEND_DEVELOPMENT_RULES.md
    - docs/3.dev-guides/UI_DESIGN_SYSTEM.md
    - docs/3.dev-guides/UI_FLOW_SPEC.md

output_boundaries:
  writable:
    - frontend/src/modules/**
    - frontend/src/lib/api/**
    - frontend/tests/**
  forbidden:
    - frontend/node_modules/**
    - frontend/.next/**
    - .env*

# SuperClaude Enhancement Configuration
enhancement:
  enabled: true
  superclaude_patterns:
    - design_first         # 吸收 /sc:design UI 设计优先
    - step_implementation  # 吸收 /sc:implement 步骤化执行
    - analysis_pattern     # 吸收 /sc:analyze 分析审计
  internal_workflow: true
  sot_priority: true       # SoT 检查结果优先级最高

baseline: AI_CODE_FACTORY_DEV_GUIDE_v2.4, SoT Freeze v2.6, SUPERCLAUDE_INTEGRATION_GUIDE_v2.2
---

# FE-Gen Skill - 前端代码生成

## 1. Purpose

前端代码生成 Skill，负责在 SoT 约束下生成 Next.js/React 前端代码。

**核心职责**:
- 根据 API 契约生成前端模块 (PageShell + hooks + components)
- 严格遵循 UI 设计系统和前端开发规范
- 生成类型安全的 TypeScript 代码

## 2. Input Contract

```typescript
interface FEGenInput {
  task: string;           // 任务描述，如 "实现充值列表页面"
  target_files: string[]; // 目标文件列表（相对于 frontend/）
  module?: string;        // 模块名称，如 "topups"
  api_contract?: string;  // API 契约内容 (可选)
  context?: {
    sot_snapshot?: Record<string, string>;  // SoT 文档内容快照
    existing_code?: Record<string, string>; // 现有代码快照
  };
}
```

**校验规则**:
- `task` 不能为空
- `target_files` 至少有一个文件
- 文件路径必须在可写区域内

## 3. Output Contract

```typescript
interface FEGenOutput {
  success: boolean;
  data?: {
    changes: Record<string, string>;  // 文件路径 -> 新内容
    notes: string[];                   // 自检说明
    sot_refs: string[];               // 引用的 SoT/规范条款
  };
  error?: string;
}
```

## 4. Constraints (必须遵守的边界)

### 4.1 代码边界

| 区域 | 权限 | 说明 |
|------|------|------|
| `frontend/src/modules/**` | ✅ 可写 | 模块化页面 |
| `frontend/src/lib/api/**` | ✅ 可写 | API 客户端封装 |
| `frontend/tests/**` | ✅ 可写 | 前端测试 |
| `frontend/node_modules/**` | ❌ 禁止 | 依赖目录 |
| `frontend/.next/**` | ❌ 禁止 | 构建产物 |

### 4.2 模块 API 边界 (STATE_MACHINE.md v2.8 §2 角色与模块权限)

按模块划分的 API 调用边界:

```yaml
module_api_boundaries:
  pitcher:
    writable_apis: [/daily-reports/*, /pitchers/me]
    readonly_apis: [/ad-accounts/*, /projects/*, /agencies/*]
    forbidden_apis: [/ledger/*, /settlements/*, /period-locks/*]

  finance:
    writable_apis: [/ledger/*, /settlements/*, /period-locks/*, /recon/*]
    readonly_apis: [/daily-reports/*, /ad-accounts/*, /pitchers/*]
    forbidden_apis: []

  ad_account:
    writable_apis: [/ad-accounts/*, /agencies/*, /spend-imports/*]
    readonly_apis: [/pitchers/*, /projects/*, /daily-reports/*]
    forbidden_apis: [/ledger/*, /settlements/*]

  project:
    writable_apis: [/projects/*, /clients/*, /pricing-rules/*]
    readonly_apis: [/pitchers/*, /ad-accounts/*]
    forbidden_apis: [/ledger/*, /daily-reports/* (POST/PUT)]
```

### 4.3 技术栈约束

- **框架**: Next.js 14+ (App Router)
- **UI 库**: shadcn/ui + Tailwind CSS
- **状态管理**: TanStack Query (React Query)
- **表单**: React Hook Form + Zod
- **类型**: TypeScript strict mode

### 4.4 组件使用规范 (COMPONENT_REGISTRY.md)

**组件注册表**: `docs/3.dev-guides/COMPONENT_REGISTRY.md` (71 个组件)

**必须使用的组件**:

| 场景 | 推荐组件 | 导入路径 |
|------|---------|---------|
| 数据表格 | DataTable | `@/components/ui/data-table/DataTable` |
| 加载/错误状态 | DataStateManager | `@/components/ui/data-state-manager` |
| KPI 卡片 | MetricCard | `@/components/ui/MetricCard` |
| 状态标签 | StatusBadge | `@/components/ui/StatusBadge` |
| 表单 | Form + FormField | `@/components/ui/form` |
| 对话框 | Dialog | `@/components/ui/dialog` |
| 确认框 | AlertDialog | `@/components/ui/alert-dialog` |

**禁止使用的组件**:

| 组件 | 原因 | 替代方案 |
|------|------|---------|
| AppShell | 已弃用 | AppLayout |

**组件引用规则**:
1. 优先从 COMPONENT_REGISTRY.md 查找现有组件
2. 禁止自创重复功能的组件
3. 复杂组件必须使用注册表中定义的 Props 接口

### 4.5 前端开发规范

1. **模块结构**:
   ```
   src/modules/{module}/
   ├── {Module}PageShell.tsx     # 页面整体布局
   ├── hooks/
   │   ├── use{Module}Filters.ts # 筛选状态
   │   └── use{Module}Data.ts    # 数据获取
   ├── components/
   │   ├── {Module}Table.tsx     # 表格组件
   │   └── {Module}Card.tsx      # 卡片组件
   ├── types/
   │   └── {module}.types.ts     # 类型定义
   └── services/
       └── {module}Api.ts        # API 调用
   ```

2. **命名规范**:
   - 组件: PascalCase (`TopupTable.tsx`)
   - hooks: camelCase with `use` prefix (`useTopupData.ts`)
   - 类型文件: kebab-case (`topup.types.ts`)
   - API 文件: camelCase (`topupsApi.ts`)

3. **状态枚举**: 必须与 `STATE_MACHINE.md` 定义一致

## 5. Prompt Template

```xml
<SYSTEM>
你是"前端开发 Agent"，负责在现有 Next.js + React + TypeScript 项目中实现/重构前端模块。

必须遵守的规则：
1. API_SOT / STATE_MACHINE 作为唯一事实来源
2. 遵循 FRONTEND_DEVELOPMENT_RULES 和 UI_DESIGN_SYSTEM
3. 使用 shadcn/ui 组件库和 Tailwind CSS
4. 使用 TanStack Query 管理服务端状态
5. 严格类型标注，禁止使用 any
6. 必须在注释中标注 SoT 引用

技术栈假设：
- Next.js 14+ (App Router)
- React 18+
- TypeScript 5+
- TanStack Query v5
- shadcn/ui + Tailwind CSS
</SYSTEM>

<!-- ========== SuperClaude Enhancement: Pre-Analysis ========== -->
<ENHANCEMENT_PHASE id="pre_analysis" enabled="{{ENABLE_PRE_ANALYSIS}}">
<INSTRUCTION>
在生成代码之前，执行 SuperClaude 前置分析：

**Step 0.1: UI 设计分析 (/sc:design)**
- 分析现有模块的 UI 模式和组件结构
- 识别可复用的组件和 hooks
- 确定设计系统遵循情况

**Step 0.2: 代码分析 (/sc:analyze)**
- 分析目标目录的现有代码
- 识别数据流和状态管理模式
- 检查类型定义的完整性

**Step 0.3: 上下文增强**
- 将分析结果汇总为 PRE_ANALYSIS_CONTEXT
- 识别潜在的 UI/UX 问题
- 生成组件设计建议
</INSTRUCTION>

<OUTPUT_TEMPLATE>
PRE_ANALYSIS_CONTEXT:
- ui_patterns_found: [识别到的 UI 模式]
- reusable_components: [可复用的组件]
- hooks_available: [可用的 hooks]
- design_recommendations: [设计建议]
</OUTPUT_TEMPLATE>
</ENHANCEMENT_PHASE>
<!-- ========== End Pre-Analysis ========== -->

<CONTEXT>
<DOC name="API_SOT">
{{API_SOT}}
</DOC>

<DOC name="STATE_MACHINE">
{{STATE_MACHINE}}
</DOC>

<DOC name="FRONTEND_RULES" optional="true">
{{FRONTEND_RULES}}
</DOC>

<DOC name="UI_DESIGN_SYSTEM" optional="true">
{{UI_DESIGN_SYSTEM}}
</DOC>

<DOC name="UI_FLOW_SPEC" optional="true">
{{UI_FLOW_SPEC}}
</DOC>

<DOC name="COMPONENT_REGISTRY">
{{COMPONENT_REGISTRY}}
</DOC>

<API_CONTRACT optional="true">
{{API_CONTRACT}}
</API_CONTRACT>

<EXISTING_FILES>
{{EXISTING_FILES}}
</EXISTING_FILES>
</CONTEXT>

<TASK>
{{TASK}}
</TASK>

<THINKING_CHAIN>
请按以下步骤思考：

0. **模块归属判定** (STATE_MACHINE.md v2.8 §2 - 必填)
   - 确认任务属于哪个核心模块:
     □ pitcher (投手管理) - 日报填报、投手信息、投手看板
     □ finance (财务管理) - 流水、冲正、对账、期间锁
     □ ad_account (广告账号管理) - 账户、代理商、归属、归因
     □ project (项目管理) - 项目、客户、单价规则
   - 验证目标文件在该模块可写范围内
   - 如果无法明确归属，STOP 并询问用户
   - 如果跨模块写入，STOP 并报错

1. **API 契约分析**
   - 从 API_SOT 或 API_CONTRACT 定位需要对接的接口
   - 确定请求参数和响应类型
   - 识别分页、筛选、排序参数

2. **状态机分析**
   - 从 STATE_MACHINE 确认状态枚举定义
   - 确定状态显示样式（颜色、图标、文案）
   - 使用 frozenset 白名单中的值

3. **模块结构规划**
   - 确定需要创建/修改的文件
   - 规划组件层次结构
   - 设计 hooks 和数据流
   - 【增强】参考 PRE_ANALYSIS_CONTEXT 中的设计建议

4. **代码生成**
   - 生成类型定义 (types/)
   - 生成 API 服务 (services/)
   - 生成数据 hooks (hooks/)
   - 生成 UI 组件 (components/)
   - 生成页面骨架 (PageShell)
   - 【增强】复用 PRE_ANALYSIS_CONTEXT 中识别的组件

5. **自检** (管理者一致性自检清单)
   - 检查模块边界: 文件是否在可写范围内
   - 检查类型是否完整 (无 any)
   - 检查状态枚举是否与 STATE_MACHINE 一致
   - 检查角色是否在 6 个合法角色内
   - 检查是否遵循 UI 设计规范
   - 检查是否有禁区代码
</THINKING_CHAIN>

<!-- ========== SuperClaude Enhancement: Post-Review ========== -->
<ENHANCEMENT_PHASE id="post_review" enabled="{{ENABLE_POST_REVIEW}}">
<INSTRUCTION>
代码生成完成后，执行 SuperClaude 后置审查：

**Step 5.1: 代码质量审查 (/sc:analyze)**
- TypeScript 类型完整性
- 组件结构和复用性
- Hook 使用正确性
- 无 any 类型使用

**Step 5.2: SoT 合规检查 (/sot-check)**
- 状态枚举是否与 STATE_MACHINE.md 一致
- API 调用是否与 API_SOT.md 一致
- UI 模式是否与设计系统一致

**Step 5.3: 质量评分**
- 计算综合质量评分 (0-100)
- 如果评分 < 75，生成修正建议
- 如果发现 P0 问题，标记为 blocking

**Step 5.4: 结果汇总**
- 将审查结果添加到输出的 enhancement 字段
</INSTRUCTION>

<OUTPUT_TEMPLATE>
POST_REVIEW_RESULT:
- passed: true/false
- quality_score: 0-100
- type_issues: [{file, line, message}]
- sot_compliance: true/false
- ui_consistency: true/false
</OUTPUT_TEMPLATE>
</ENHANCEMENT_PHASE>
<!-- ========== End Post-Review ========== -->

<OUTPUT_FORMAT>
只输出一段 JSON，格式如下：

{
  "changes": [
    {
      "file": "frontend/src/modules/topups/types/topup.types.ts",
      "content": "完整的文件内容"
    },
    {
      "file": "frontend/src/modules/topups/services/topupsApi.ts",
      "content": "完整的文件内容"
    },
    {
      "file": "frontend/src/modules/topups/hooks/useTopupData.ts",
      "content": "完整的文件内容"
    },
    {
      "file": "frontend/src/modules/topups/components/TopupTable.tsx",
      "content": "完整的文件内容"
    },
    {
      "file": "frontend/src/modules/topups/TopupsPageShell.tsx",
      "content": "完整的文件内容"
    }
  ],
  "notes": [
    "自检说明1",
    "自检说明2"
  ],
  "sot_refs": [
    "API_SOT.md#topups",
    "STATE_MACHINE.md#topup",
    "UI_DESIGN_SYSTEM.md#table"
  ],
  "enhancement": {
    "pre_analysis": {
      "executed": true,
      "ui_patterns_found": ["PageShell模式", "Table组件", "..."],
      "reusable_components": ["Badge", "Card", "..."],
      "recommendations": ["建议复用现有筛选组件", "..."]
    },
    "post_review": {
      "executed": true,
      "passed": true,
      "quality_score": 85,
      "type_issues": [],
      "sot_compliance": true,
      "ui_consistency": true
    }
  }
}
</OUTPUT_FORMAT>
```

## 6. Code Templates

### 6.1 类型定义模板

```typescript
// frontend/src/modules/topups/types/topup.types.ts

/**
 * Topup 类型定义
 * SoT: STATE_MACHINE.md#topup, DATA_SCHEMA.md#topups
 */

// 状态枚举 - 对齐 STATE_MACHINE.md#topup
export type TopupStatus =
  | "pending"
  | "approved"
  | "rejected"
  | "executed"
  | "failed";

// 充值记录
export interface Topup {
  id: string;
  amount: number;
  status: TopupStatus;
  created_at: string;
  approved_by?: string;
  approved_at?: string;
}

// 列表响应
export interface TopupListResponse {
  items: Topup[];
  total: number;
  page: number;
  page_size: number;
}

// 筛选参数
export interface TopupFilters {
  status?: TopupStatus;
  date_from?: string;
  date_to?: string;
  page?: number;
  page_size?: number;
}
```

### 6.2 API 服务模板

```typescript
// frontend/src/modules/topups/services/topupsApi.ts

import { apiFetch } from "@/lib/api/apiFetch";
import type { Topup, TopupListResponse, TopupFilters } from "../types/topup.types";

/**
 * Topups API 服务
 * SoT: API_SOT.md#topups
 */

const BASE_URL = "/api/v1/topups";

export const topupsApi = {
  // 获取列表
  async list(filters: TopupFilters = {}): Promise<TopupListResponse> {
    const params = new URLSearchParams();
    if (filters.status) params.set("status", filters.status);
    if (filters.page) params.set("page", String(filters.page));
    if (filters.page_size) params.set("page_size", String(filters.page_size));

    return apiFetch<TopupListResponse>(`${BASE_URL}?${params.toString()}`);
  },

  // 获取详情
  async get(id: string): Promise<Topup> {
    return apiFetch<Topup>(`${BASE_URL}/${id}`);
  },

  // 审批
  async approve(id: string, comment?: string): Promise<Topup> {
    return apiFetch<Topup>(`${BASE_URL}/${id}/approve`, {
      method: "POST",
      body: JSON.stringify({ comment }),
    });
  },

  // 拒绝
  async reject(id: string, reason: string): Promise<Topup> {
    return apiFetch<Topup>(`${BASE_URL}/${id}/reject`, {
      method: "POST",
      body: JSON.stringify({ reason }),
    });
  },
};
```

### 6.3 数据 Hook 模板

```typescript
// frontend/src/modules/topups/hooks/useTopupData.ts

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { topupsApi } from "../services/topupsApi";
import type { TopupFilters } from "../types/topup.types";

/**
 * Topup 数据 Hook
 * 使用 TanStack Query 管理服务端状态
 */

// Query Keys
export const topupKeys = {
  all: ["topups"] as const,
  lists: () => [...topupKeys.all, "list"] as const,
  list: (filters: TopupFilters) => [...topupKeys.lists(), filters] as const,
  details: () => [...topupKeys.all, "detail"] as const,
  detail: (id: string) => [...topupKeys.details(), id] as const,
};

// 列表查询
export function useTopupList(filters: TopupFilters = {}) {
  return useQuery({
    queryKey: topupKeys.list(filters),
    queryFn: () => topupsApi.list(filters),
  });
}

// 详情查询
export function useTopupDetail(id: string) {
  return useQuery({
    queryKey: topupKeys.detail(id),
    queryFn: () => topupsApi.get(id),
    enabled: !!id,
  });
}

// 审批 Mutation
export function useApproveTopup() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, comment }: { id: string; comment?: string }) =>
      topupsApi.approve(id, comment),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: topupKeys.lists() });
    },
  });
}

// 拒绝 Mutation
export function useRejectTopup() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, reason }: { id: string; reason: string }) =>
      topupsApi.reject(id, reason),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: topupKeys.lists() });
    },
  });
}
```

### 6.4 表格组件模板

```tsx
// frontend/src/modules/topups/components/TopupTable.tsx

"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import type { Topup, TopupStatus } from "../types/topup.types";

/**
 * Topup 表格组件
 * SoT: UI_DESIGN_SYSTEM.md#table
 */

interface TopupTableProps {
  data: Topup[];
  onApprove?: (id: string) => void;
  onReject?: (id: string) => void;
  isLoading?: boolean;
}

// 状态样式映射 - 对齐 STATE_MACHINE.md#topup
const statusConfig: Record<TopupStatus, { label: string; variant: "default" | "secondary" | "destructive" | "outline" }> = {
  pending: { label: "待审批", variant: "outline" },
  approved: { label: "已审批", variant: "default" },
  rejected: { label: "已拒绝", variant: "destructive" },
  executed: { label: "已执行", variant: "secondary" },
  failed: { label: "失败", variant: "destructive" },
};

export function TopupTable({ data, onApprove, onReject, isLoading }: TopupTableProps) {
  if (isLoading) {
    return <div className="text-center py-8">加载中...</div>;
  }

  if (!data.length) {
    return <div className="text-center py-8 text-muted-foreground">暂无数据</div>;
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>ID</TableHead>
          <TableHead>金额</TableHead>
          <TableHead>状态</TableHead>
          <TableHead>创建时间</TableHead>
          <TableHead>操作</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {data.map((topup) => {
          const status = statusConfig[topup.status];
          return (
            <TableRow key={topup.id}>
              <TableCell className="font-mono text-sm">
                {topup.id.slice(0, 8)}...
              </TableCell>
              <TableCell>¥{topup.amount.toLocaleString()}</TableCell>
              <TableCell>
                <Badge variant={status.variant}>{status.label}</Badge>
              </TableCell>
              <TableCell>
                {new Date(topup.created_at).toLocaleString("zh-CN")}
              </TableCell>
              <TableCell>
                {topup.status === "pending" && (
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      onClick={() => onApprove?.(topup.id)}
                    >
                      审批
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => onReject?.(topup.id)}
                    >
                      拒绝
                    </Button>
                  </div>
                )}
              </TableCell>
            </TableRow>
          );
        })}
      </TableBody>
    </Table>
  );
}
```

### 6.5 页面骨架模板

```tsx
// frontend/src/modules/topups/TopupsPageShell.tsx

"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { TopupTable } from "./components/TopupTable";
import { useTopupList, useApproveTopup, useRejectTopup } from "./hooks/useTopupData";
import type { TopupStatus, TopupFilters } from "./types/topup.types";

/**
 * 充值管理页面
 * SoT: UI_FLOW_SPEC.md#topup-management
 */

export function TopupsPageShell() {
  const [filters, setFilters] = useState<TopupFilters>({
    page: 1,
    page_size: 20,
  });

  const { data, isLoading, error } = useTopupList(filters);
  const approveMutation = useApproveTopup();
  const rejectMutation = useRejectTopup();

  const handleStatusChange = (status: string) => {
    setFilters((prev) => ({
      ...prev,
      status: status === "all" ? undefined : (status as TopupStatus),
      page: 1,
    }));
  };

  const handleApprove = (id: string) => {
    approveMutation.mutate({ id });
  };

  const handleReject = (id: string) => {
    const reason = prompt("请输入拒绝原因");
    if (reason) {
      rejectMutation.mutate({ id, reason });
    }
  };

  if (error) {
    return (
      <div className="text-center py-8 text-destructive">
        加载失败: {error.message}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">充值管理</h1>
      </div>

      {/* 筛选条 */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">筛选条件</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4">
            <Select
              value={filters.status ?? "all"}
              onValueChange={handleStatusChange}
            >
              <SelectTrigger className="w-40">
                <SelectValue placeholder="状态" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">全部状态</SelectItem>
                <SelectItem value="pending">待审批</SelectItem>
                <SelectItem value="approved">已审批</SelectItem>
                <SelectItem value="rejected">已拒绝</SelectItem>
                <SelectItem value="executed">已执行</SelectItem>
                <SelectItem value="failed">失败</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* 数据表格 */}
      <Card>
        <CardContent className="pt-6">
          <TopupTable
            data={data?.items ?? []}
            isLoading={isLoading}
            onApprove={handleApprove}
            onReject={handleReject}
          />
        </CardContent>
      </Card>

      {/* 分页信息 */}
      {data && (
        <div className="text-sm text-muted-foreground text-center">
          共 {data.total} 条记录，第 {data.page} / {Math.ceil(data.total / data.page_size)} 页
        </div>
      )}
    </div>
  );
}
```

## 7. Self-Check Checklist

生成代码后，必须进行以下自检 (STATE_MACHINE.md v2.8 §2 合规检查)：

| 检查项 | 验证方法 | P0/P1 |
|--------|---------|-------|
| **模块归属确认** | 任务属于 pitcher/finance/ad_account/project 之一 | P0 |
| **写入权限检查** | 目标文件在该模块可写范围内 | P0 |
| 类型完整性 | 无 any 类型 | P0 |
| 状态枚举一致性 | 对比 STATE_MACHINE.md (8 状态: raw_submitted → ... → final_locked) | P0 |
| 角色合规 | 对比 4 技术角色 (admin/finance/account_manager/media_buyer) - MASTER.md v4.6 | P0 |
| API 对接正确性 | 对比 API_SOT.md | P0 |
| 禁区检查 | 不生成 node_modules/.next | P0 |
| UI 组件使用 | 使用 shadcn/ui | P1 |
| Hook 命名规范 | use 前缀 | P1 |
| 错误处理 | 有 error 状态展示 | P1 |

**跨模块交互检查**:

| 检查项 | 验证方法 | P0/P1 |
|--------|---------|-------|
| 只读其他模块数据 | 仅使用 GET API | P0 |
| 不写入其他模块 | 无跨模块 POST/PUT/DELETE | P0 |
| ID 引用传递 | 使用 ID 而非嵌入对象 | P1 |

**幻觉抑制最终确认** (输出前必须):

| 确认项 | 验证方法 | 阻断级别 |
|--------|---------|----------|
| 状态值来源 | 每个状态值可追溯到 STATE_MACHINE.md | BLOCKING |
| 角色值来源 | 每个角色可追溯到 frozenset 白名单 | BLOCKING |
| 类型定义来源 | 每个类型可追溯到 API_SOT.md 响应结构 | BLOCKING |
| 组件引用 | 所有 import 的组件在 COMPONENT_REGISTRY.md 中存在 | BLOCKING |
| 组件 Props | 使用的 Props 与注册表定义一致 | BLOCKING |
| API 端点 | 调用的 API 端点在 API_SOT.md 中定义 | BLOCKING |

## 8. Version History

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.5 | 2025-12-24 | 新增：集成 COMPONENT_REGISTRY.md (71 个组件)，添加组件使用规范 |
| v2.4 | 2025-12-22 | P1 修复：添加模块 API 边界、幻觉抑制最终确认 |
| v2.3 | 2025-12-22 | P0 修复：添加模块归属判定步骤、跨模块交互检查 |
| v2.1 | 2025-12-07 | 增强：集成 SuperClaude pre_analysis 和 post_review |
| v2.0 | 2025-12-06 | 重构：对齐 AI_CODE_FACTORY_DEV_GUIDE_v2.0，增加完整代码模板 |
| v1.0 | 2025-11-01 | 初始版本 |

---

**文档控制**: Owner: wade | Baseline: AI_CODE_FACTORY_DEV_GUIDE_v2.0, SuperClaude Enhancer v1.0
