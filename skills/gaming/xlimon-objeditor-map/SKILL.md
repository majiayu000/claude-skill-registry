---
name: xlimon-objeditor-map
description: War3Lib 物编生成与改造规范。用于在 `UnitTestMap/table`、`Jass/**/*.w3a|w3u|w3i` 及项目内 `db` 中安全新增/修改对象，重点处理 4 位 ID 去重（含大小写冲突）、主动技能通魔模板与唯一 OrderID、隐藏按钮位点写法，以及紧凑行尾注释风格。
---

# War3Lib 物编 Skill

按需读取：
- `references/workflow.md`
- `references/snippets.md`
- `references/templates-unit.md`
- `references/templates-ability.md`
- `references/templates-passive.md`
- `references/templates-spellbook.md`
- `scripts/check_obj_ids.py`

## 执行流程

1. 先从 skill 内置模板（`references/templates-*.md`）选择最接近的模板类型，再定位目标对象文件（优先 `.w3a/.w3u/.w3i`，单测注入可落到 `UnitTestMap/table/*.ini`）。
2. 先分配 ID，再基于模板最小改动。新增前必须执行：
   - `python3 .codex/skills/xlimon-objeditor-map/scripts/check_obj_ids.py --id <ID>`
3. 若是主动技能，优先使用“通魔”模板（通常 `_parent = "ANcl"`），并确保 `Order` / `DataF` 不与既有技能冲突。
4. 从 `db/list/List_Order.ini` 查可用命令字；把已使用项按你的习惯标记 `//`。
5. 需要隐藏图标时，允许使用按钮位点 bug（见 snippets）。
6. 生成时优先写紧凑格式：值后追加行尾注释 `-- 注释`，便于查阅。
7. 输出前再次运行检查脚本，确认无冲突后再提交修改。

## 路径约定

- 单测地图物编：`UnitTestMap/table/`
- 库内对象文件：`Jass/**/*.w3a`、`Jass/**/*.w3u`、`Jass/**/*.w3i`（以及同类 `.w3*`）
- 常用命令字清单：`db/list/List_Order.ini`
- 原生数据库参照：`db/`（项目内相对路径）

## 强约束

- 把 4 位对象 ID 视为大小写不敏感唯一键：`[A01a]` 与 `[A01A]` 视为冲突。
- 同时检查两类冲突：
  - 项目对象文件冲突（`UnitTestMap/table` + `Jass/**/*.w3*`）
  - 与项目 `db` 冲突（对应 ini 文件）
- 主动技能避免重复 `Order`，否则可能出现按键/命令冲突。
- 修改 `db/list/List_Order.ini` 时保留现有格式，不改动无关条目。

## 生成行为

- 默认先做“最小变更”：只新增/修改必要段落。
- 保持原有字段顺序与风格，不擅自大规模重排。
- 若检测环境缺少某路径，显式说明并继续处理可落地部分。
