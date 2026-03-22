---
name: zinc-dual-index-pattern
description: >
  War3Lib 的 Zinc/JASS “双重索引 + 紧凑数组”实例管理模式：全局遍历 + 分组遍历（双视图）
  与尾部交换删除（swap-remove / 尾部交换法），用于高频 create/destroy 的 Buff/Effect/Queue/中央计时器等；
  当你需要写 Lists/groupLists、removeAt、O(1) 删除并保持数组紧凑时使用。
---

# Zinc 双重索引 + 紧凑数组模式（War3Lib）

按需加载参考文档；本 Skill 的目标是让你在 War3Lib 里快速、稳定地实现：

- **紧凑遍历**：数组无空洞，`for` 遍历不需要跳过空位
- **O(1) 删除**：用尾部交换（swap-remove）移除元素
- **双视图索引**：同一实例同时存在于“全局列表”和“分组列表”，并能分别遍历/查询

## References（按需打开）

- `references/overview.md`
- `references/swap-remove.md`
- `references/dual-index-template.md`
- `references/war3lib-examples.md`
- `references/checklist.md`
