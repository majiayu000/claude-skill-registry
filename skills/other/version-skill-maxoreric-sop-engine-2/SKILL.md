---
name: version-skill
description: Skill 版本管理的 Skill。当需要 A/B test、切换版本、回滚时触发。触发词：版本、version、A/B test、切换、回滚、promote。
---

# 版本管理

管理 Skill 的版本，支持 A/B test、版本切换和回滚。

## 功能

### 1. 查看版本历史

列出所有版本：
```
versions/
├── SKILL.v1.md
├── SKILL.v2.md
└── SKILL.v3.md
```

### 2. A/B Test

同时执行两个版本，对比结果：

1. 读取当前版本和对比版本
2. 用相同输入分别执行
3. 对比产出
4. 记录对比结果

输出 `workspace/ab-test-result.md`：
```markdown
# A/B Test 结果

## 版本 A（当前）
[产出摘要]

## 版本 B（v{n}）
[产出摘要]

## 对比
| 维度 | 版本 A | 版本 B |
|-----|-------|-------|
| ... | ... | ... |

## 结论
[推荐哪个版本]
```

### 3. 版本切换（Promote）

将某个版本设为主版本：

1. 备份当前主版本到 versions/
2. 将目标版本复制为 SKILL.md
3. 更新 status.json

### 4. 回滚

恢复到之前的版本：

1. 找到目标版本
2. 执行版本切换

## 命令格式

- 查看：`查看 [skill-name] 的版本历史`
- A/B test：`对比 [skill-name] 的 v1 和 v2`
- 切换：`把 [skill-name] 切换到 v2`
- 回滚：`回滚 [skill-name] 到上一个版本`

## 原则

- 版本号只增不减
- 切换前先备份
- A/B test 要用相同输入
- 保留足够的历史版本
