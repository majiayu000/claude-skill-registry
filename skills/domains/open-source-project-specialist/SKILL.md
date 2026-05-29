---
name: open-source-project-specialist
description: 提供开源项目专属技能的组织与索引能力。当任务依赖特定第三方开源项目的深度实践、约定或扩展模式时使用。
---
# Open Source Project Specialist

提供开源项目专属技能的组织与索引能力。当任务依赖特定第三方开源项目的深度实践、约定或扩展模式时使用。

## Skill Index

<!-- AUTO-GENERATED-SKILL-INDEX:START -->
以下索引由 `node scripts/update-skill-index.js` 自动生成，用于让 Claude 在顶层专家触发后继续路由到最相关的子技能。

### Claude 使用说明

1. 先将用户当前任务与每个子技能的 `触发语义` 进行语义匹配，不要只看目录名。
2. 一旦找到最相关的子技能，立即打开其 `入口文件` 指向的 `SKILL.md`，把它作为下一层入口。
3. 进入子技能后，再根据该子技能自己的说明按需加载同目录下的 `references/`、`scripts/`、`assets/`，不要在顶层专家中预先展开大段细节。
4. 如果多个子技能都相关，先加载最贴近主目标的那个，再按需补充其他子技能，避免一次性加载过多上下文。
5. 下方 `入口文件` 路径相对于项目根目录，可直接用于 `Read` 操作。

### 子技能索引

#### projects (1)
- `ruoyi-framework`
  - 触发语义: 使用 RuoYi-Vue 框架（SpringBoot + Spring Security + MyBatis + JWT + Vue）时应该使用此技能。它提供了环境设置、项目结构、后端 CRUD 开发、高级后端功能（权限、日志记录、调度、数据范围、多数据源）、前端开发（路由、请求处理、组件、i18n）、代码生成和插件集成（Docker、PostgreSQL、SpringBoot3、OSS）的指导。。由 RuoYi、ruoyi、PageHelper、@Excel、@PreAuthorize、@DataScope、@Log、ExcelUtil、AjaxResult、vue-element-admin、Element UI admin 等关键字触发。
  - 入口文件: `.claude/skills/open-source-project-specialist/references/domains/projects/ruoyi/SKILL.md`

<!-- AUTO-GENERATED-SKILL-INDEX:END -->

## Notes

- 顶层 `SKILL.md` 仅做索引导航，不承载大体量细节内容。
- 详细资料下沉到 `references/domains/`，按树形结构组织。
