---
name: fec-alchemy
description: Use when absorbing ideas, capabilities, workflows, architecture, quality systems, ecosystem extensions, or engineering practices from any reference system into the current project through original, project-native redesign rather than copying.
---

# 项目吸收与原创化融合

## Purpose

将一个或多个参考系统中的优秀思想、能力和工程实践，转化为当前项目中原创、可维护、符合目标项目风格的改进。

适用于吸收、借鉴、对标、迁移或融合另一个代码库、产品、框架、库、服务、CLI、插件、文档体系、AI/Agent 工具链、架构或工程工作流。普通 Bug 修复、单独 API 使用问题或直接文件格式转换不应使用本 Skill，除非用户明确要求项目级吸收或适配。

## Procedure

1. 明确目标和参考系统：
   - 将当前仓库视为目标系统，它的架构、命名、测试、发布模型和维护边界是事实来源。
   - 将外部仓库、上传压缩包、文档、示例、产品描述或运行体验视为参考系统，它们只提供证据和启发。
   - 识别吸收范围：产品能力、架构模式、领域模型、接口协议、数据流、运行时行为、开发体验、质量体系、交付流程、文档知识或生态扩展。
   - 信息较多时可使用 [assets/intake-template.md](assets/intake-template.md) 建立简要清单。
2. 建立目标项目基线：
   - 先读取目标项目 README、包元数据、目录结构、配置、现有入口、扩展点、测试命令和发布说明。
   - 找出目标项目已有类似能力，判断应增强、合并、替换、拆分、文档化还是新增。
3. 扫描参考项目：
   - 优先查看 README、包元数据、源码布局、项目形态相关目录、关键模块、测试、示例和发布说明。
   - 将观察记录为能力、意图、模式和取舍，不记录为要复制的文件清单。
4. 提炼候选能力：
   - 对每个候选项说明它解决的问题、用户价值、适配度、依赖、风险、可验证性和与目标项目现状的关系。
   - 对许可证、来源不清楚或实现高度绑定参考项目的候选项，只提炼思想，不复用表达。
5. 映射到目标架构：
   - 使用目标项目原生命名、模块边界、依赖策略、编码约定和测试方式重新设计。
   - 避免创建与现有模块竞争的并行系统；避免因为参考项目用了某依赖就盲目引入依赖。
   - 非平凡变更可使用 [assets/absorption-plan-template.md](assets/absorption-plan-template.md)。
6. 原创化实现或计划：
   - 编写新代码或新文档，不复制参考项目中的非平凡代码、提示词、配置或文档表达。
   - 吸收生态扩展、提示词、命令、插件、自动化、Agent 或规则时，统一职责边界并删除重复指令。
   - 大型任务先交付垂直薄切片，并记录被拒绝或延期的候选项。
7. 验证和汇报：
   - 运行最相关的类型检查、Lint、测试、构建、文档校验或 Skill 校验。
   - 如果无法验证，明确说明阻塞原因、风险范围和需要用户确认的信息。
   - 必要时使用 [assets/review-checklist.md](assets/review-checklist.md) 做人工复核。

## Constraints

- 不把吸收任务变成机械化 diff 合并。
- 不整体照搬参考项目的命名体系、文件结构或实现细节。
- 不在许可证或用户意图不明确时逐字复用参考项目中的非平凡代码、文档、提示词或配置。
- 不为了匹配参考项目而削弱安全、隐私、权限边界、测试、可维护性或目标项目产品方向。
- 不声称原创化，除非输出能解释目标设计为何不同、为何适配目标项目、如何验证。
- 不把长篇参考材料塞进主说明；大型任务读取 [references/methodology.md](references/methodology.md)，许可证和原创风险读取 [references/originality-and-licensing.md](references/originality-and-licensing.md)。

## Expected Output

分析类任务输出：

- 吸收候选项
- 推荐目标设计
- 实现计划
- 风险与许可证说明
- 验证清单

实现类任务输出：

- 已完成变更
- 原创化说明
- 验证结果
- 剩余工作

仓库级任务中，如果宿主工具支持文件编辑，应创建或更新项目本地计划文档。

## References

- [references/methodology.md](references/methodology.md) - 详细吸收方法论。
- [references/originality-and-licensing.md](references/originality-and-licensing.md) - 原创性、许可证和来源风险约束。
