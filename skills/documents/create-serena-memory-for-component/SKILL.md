---
name: create-serena-memory-for-component
description: 为任意组件或模块创建/更新 Serena memory 的工作流与格式规范。用于用户要求“源码级梳理并写入 Serena memory”的场景，例如“对 X 进行源码级梳理并写入 Y.md”，或者“分析 X 并生成Serena memory”。适用于组件类/接口名或模块名（如 OACModule_*），并要求输出包含概述/职责/涉及文件/架构/依赖/注意事项/调用方等章节。
---

# Create Serena Memory For Component

## 目标
- 生成或更新某组件/模块的 Serena memory。
- 保持与现有组件 memory 的格式一致与内容精炼。
- 仅写入有依据的信息，不确定则标注或省略。

## 工作流（顺序）
1. 解析目标与命名
   - 从用户请求中提取组件/模块名与目标 memory 文件名。
   - 若用户已给出 memory 文件名，直接使用。
   - 若是组件类/接口名（例如 `CCrashpadService`、`ICrashpadService`），去掉前缀 `C`/`I` 作为 memory 名（`CrashpadService.md`）。
   - 若是模块名（例如 `OACModule_Crashpad`），保持原名（`OACModule_Crashpad.md`）。
   - 若命名仍不明确，先向用户确认。

2. 检查已有 memory
   - 使用 `list_memories` 检查是否已存在同名 memory。
   - 若已存在，先 `read_memory` 并以增量方式更新（`edit_memory`）。
   - 若用户强调“格式与其他组件一致”，读取一个相近组件的 memory 作为格式参考。

3. 收集证据
   - 优先使用 Serena 工具做定点定位：`get_symbols_overview` → `find_symbol` → `find_referencing_symbols`。
   - 必要时使用 `search_for_pattern` 或 `list_dir` 限定范围。
   - 记录涉及文件的仓库相对路径，避免泛化描述。

4. 写入 memory
   - 使用下方模板，保持标题与顺序固定。
   - 每个章节内容简洁、可追溯。
   - “调用方”仅在确认调用关系时填写。

5. 落盘/更新
   - 新建：`write_memory`。
   - 更新：`edit_memory`，避免重复与冗余。

## 输出模板（固定结构）

```
# <组件或模块名>

## 概述
<一句话到两句话说明该组件/模块做什么>

## 职责
- <职责1>
- <职责2>

## 涉及文件 (不要带行号)
- <相对路径/文件1>
- <相对路径/文件2>

## 架构
<核心对象、模块划分、关键流程或调用链的简述,能有流程图的最好有流程图>

## 依赖
- <内部依赖或外部库>
- <配置/资源依赖（如有）>

## 注意事项
- <容易踩坑点/边界条件/性能问题/多线程竞态冲突/可能导致崩溃或预期外行为的地方>

## 调用方（可选）
- <已确认的调用方>
```

## 触发语句示例（用于匹配）
- 对 `OACEngine/OACModuleManager` 进行源码级梳理，并将该组件的概述/架构写入 Serena memory：`OACModuleManager.md`
- 详细分析 `OACModule\OACModule_Crashpad` 并将该业务模块的概述/架构以 serena memory 的形式写入 `OACModule_Crashpad.md`
- 对 `OACEngine/NetworkSystem` 进行源码级梳理，并将该组件的概述/架构写入 Serena memory：`NetworkSystem.md`
- 详细分析 `GrahpicCaptureService` 的架构/业务逻辑，并写入 Serena memory：`GrahpicCaptureService.md`
