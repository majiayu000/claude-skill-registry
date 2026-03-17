---
name: ticktick-cli
description: 使用 Python CLI 与 Dida365 Open API 交互以管理滴答清单任务/项目，适用于需要通过脚本或命令行调用滴答清单接口的场景（如项目/任务的查询、创建、更新、完成、删除）。
---

说明：以下调用方式均以当前 `SKILL.md` 文件所在文件夹为 workdir。

1) 常用子命令（覆盖日常场景）
- `project`
  - `list`
  - `get --project-id`
  - `data --project-id`
  - `create --name [--color --sort-order --view-mode --kind]`
  - `update --project-id [--name --color --sort-order --view-mode --kind]`
  - `delete --project-id`（危险，删除前需谨慎确认）
- `task`
  - `get --project-id --task-id`
  - `create --project-id --title [--content --desc --all-day --start-date --due-date --time-zone --reminder --repeat --priority --sort-order --item]`
  - `update --task-id --project-id [--title --content --desc --all-day --start-date --due-date --time-zone --reminder --repeat --priority --sort-order --item]`
  - `complete --project-id --task-id`
  - `delete --project-id --task-id`（危险，删除前需谨慎确认）

2) 输出格式
- 所有调用统一在脚本后、子命令前加 `--json`（示例：`./scripts/ticktick_cli.py --json task get --project-id ...`）

3) 冷门参数/字段怎么查
- 运行 `./scripts/ticktick_cli.py <command> --help` 查看该命令的参数
- 查看 `references/dida365-openapi.md` 了解完整参数、字段与响应结构

## Dida365 概念模型

- Project：项目，任务的容器，支持不同视图模式（list/kanban/timeline）。
  - 常用字段：
    - `name`（名称）
    - `color`（颜色）
    - `viewMode`（视图模式）
    - `kind`（类型）
    - `groupId`（分组）
    - `closed`（是否关闭）
    - `permission`（权限）
    - `sortOrder`（排序）
- Task：任务，隶属于某个 Project，可包含提醒、优先级、重复规则等。
  - 常用字段：
    - `title`（标题）
    - `content`（内容）
    - `desc`（描述/清单说明）
    - `tags`（标签）
    - `priority`（优先级）
    - `status`（状态）
    - `startDate`（开始时间）
    - `dueDate`（截止时间）
    - `timeZone`（时区）
    - `reminders`（提醒）
    - `repeatFlag`（重复规则）
    - `items`（子任务列表）
- ChecklistItem：任务下的子任务（清单项），用于拆分步骤。
  - 常用字段：
    - `title`（标题）
    - `status`（状态）
    - `startDate`（开始时间）
    - `completedTime`（完成时间）
    - `timeZone`（时区）
    - `sortOrder`（排序）
- Column：项目看板列，用于 kanban 视图的列信息。
  - 常用字段：
    - `name`（列名）
    - `sortOrder`（排序）
- ProjectData：项目详情聚合，包含项目本身、未完成任务与列信息。

## 资源

- [ticktick_cli.py](scripts/ticktick_cli.py)：主 CLI 入口，负责读取配置并发起 API 调用。
- [dida365-openapi.md](references/dida365-openapi.md)：官方 Open API 文档快照，便于离线检索参数与字段。
