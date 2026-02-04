# 重命名 SKILL

> **目标**：重命名一个 SKILL（目录名 + name 字段 + 索引）
>
> **本质**：重命名 = 删除旧条目 + 添加新条目
>
> **完成后**：必须执行 [SYNC_INDEX.md](./SYNC_INDEX.md) 同步索引

---

## 步骤

### Step 1: 重命名目录

```bash
mv spec_stage_skill/{category}/old-name/ \
   spec_stage_skill/{category}/new-name/
```

### Step 2: 更新 SKILL.md

修改 frontmatter 中的 `name` 字段：

```yaml
---
name: new-name    # 改为新名称
description: ...
---
```

### Step 3: 更新索引

执行 [SYNC_INDEX.md](./SYNC_INDEX.md)：

1. **底层索引** `{category}/_INDEX.md`：
   ```markdown
   # 删除旧行
   | old-name | ... | `old-name/SKILL.md` |

   # 添加新行
   | new-name | ... | `new-name/SKILL.md` |
   ```

2. **上层索引** `_INDEX_STAGE_*.md`：同样更新

3. **全局索引** `_INDEX_ALL.md`：同样更新

### Step 4: 验证

执行 [VALIDATE_SKILL_AND_INDEX.md](./VALIDATE_SKILL_AND_INDEX.md) 确认：
- 路径正确
- 无悬空引用

---

## 跨目录迁移

如果需要将 SKILL 从一个目录移到另一个（如 `common/` → `requirements/`）：

### Step 1: 移动目录

```bash
mv spec_stage_skill/common/my-skill/ \
   spec_stage_skill/requirements/my-skill/
```

### Step 2: 更新旧位置索引

从 `common/_INDEX.md` 移除条目。

### Step 3: 更新新位置索引

在 `requirements/_INDEX.md` 添加条目。

### Step 4: 更新上层索引

- 从 `_INDEX_STAGE_2.md`、`_INDEX_STAGE_3.md` 移除（common 在多个 Stage）
- 添加到 `_INDEX_STAGE_1.md`（requirements 只在 Stage 1）

### Step 5: 验证

执行 [VALIDATE_SKILL_AND_INDEX.md](./VALIDATE_SKILL_AND_INDEX.md)

---

## 检查清单

- [ ] 目录已重命名
- [ ] SKILL.md 的 name 字段已更新
- [ ] 底层索引已更新
- [ ] 上层索引已更新
- [ ] 全局索引已更新
- [ ] 执行 [VALIDATE_SKILL_AND_INDEX.md](./VALIDATE_SKILL_AND_INDEX.md)

---

## AI Coding Agent 命令

```
请帮我将 old-name 重命名为 new-name：

1. 重命名目录
2. 更新 SKILL.md 的 name 字段
3. 更新所有索引
4. 验证正确性
```

```
请帮我将 my-skill 从 common/ 迁移到 requirements/：

1. 移动目录
2. 更新旧位置索引
3. 更新新位置索引
4. 更新上层索引
5. 验证正确性
```
