---
name: debugging-lessons
description: 调试经验教训和通用原则
---

# 调试经验总结

## 本次对话中的教训

### 1. Hyprland 快捷键覆盖
**问题**: 修改 `UserKeybinds.conf` 后，同名快捷键没有覆盖默认绑定，导致两个绑定同时存在。

**原因**: Hyprland 不会自动覆盖同名绑定，后面的 `bindd` 只是追加，不会替换。

**解决方案**: 在覆盖绑定前，必须先 `unbind`：
```ini
unbind = $mainMod SHIFT, S
unbind = ALT SHIFT, S
bindd = $mainMod SHIFT, S, 新功能, exec, ...
```

**教训**: 应该先查阅 Hyprland Wiki 或 `hyprctl binds` 验证绑定行为。

---

### 2. Arch Linux Python 包管理
**问题**: 直接建议 `pip install --user` 导致 `externally-managed-environment` 错误。

**原因**: Arch Linux 从 2023 年开始实施 PEP 668，禁止直接用 pip 安装到系统 Python。

**解决方案**:
- 使用虚拟环境: `python -m venv .venv && .venv/bin/pip install ...`
- 或使用 AUR 包: `paru -S python-xxx`
- 或用 `--break-system-packages`（不推荐）

**教训**: 在 Arch Linux 上涉及 Python 包时，应先检查系统限制。

---

### 3. 配置修改前应验证当前状态
**问题**: 多次修改配置后才发现问题（快捷键没覆盖、pip 不能用）。

**教训**:
- 修改前先用 `hyprctl binds` / `hyprctl getoption` 验证当前配置
- 涉及系统包时先检查 `pacman -Q` 或发行版特性
- 搜索官方文档/论坛了解常见陷阱

---

## 通用调试原则

### 先搜索，后动手
1. 遇到问题时，先用 WebSearch 搜索官方文档和论坛
2. 查看 GitHub Issues 中是否有类似问题
3. 检查 Arch Wiki（如果是 Arch 系）

### 验证再修改
1. 修改配置前，检查当前状态（`hyprctl`、`git status` 等）
2. 理解配置加载顺序和覆盖机制
3. 小步修改，每次验证

### 环境感知
1. 检查操作系统和版本
2. 检查已安装的依赖和版本冲突
3. 注意发行版特有的限制（如 Arch 的 PEP 668）