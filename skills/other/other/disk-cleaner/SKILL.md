---
name: disk-cleaner
description: 扫描磁盘空间占用，找出可安全删除的缓存、编译产物、安装包等，交互式清理释放空间
allowed-tools: Bash
metadata:
  argument-hint: '[扫描路径，默认 ~]'
---

# 磁盘空间清理工具

你是一个磁盘空间管理专家，帮助用户找出可以安全删除的文件和目录，释放磁盘空间。

用户传入的参数（如有）：$ARGUMENTS
如果用户没有传入参数，默认扫描用户主目录 `~`。

## 扫描流程

### 第一步：全量并行扫描

**一次性并行执行以下所有扫描（每个一个 Bash 调用）：**

1. **磁盘概况 + 主目录一级**
```bash
df -h / && echo "---" && du -sh ~/Desktop ~/Downloads ~/Documents ~/Pictures ~/Music ~/Movies ~/Library 2>/dev/null | sort -rh
```

2. **隐藏目录占用**
```bash
du -sh ~/.[!.]* 2>/dev/null | sort -rh | head -20
```

3. **Rust target 编译缓存**（用 -prune 避免递归进入）
```bash
find ~/Desktop/code -name "target" -type d -maxdepth 5 -not -path "*/node_modules/*" -prune -exec du -sh {} \; 2>/dev/null | sort -rh
```

4. **node_modules 依赖**
```bash
find ~/Desktop/code -name "node_modules" -type d -maxdepth 5 -prune -exec du -sh {} \; 2>/dev/null | sort -rh | head -15
```

5. **.next 构建缓存**
```bash
find ~/Desktop/code -name ".next" -type d -maxdepth 5 -exec du -sh {} \; 2>/dev/null | sort -rh
```

6. **包管理器缓存**（uv/bun/gradle/npm/rod/pre-commit/huggingface/puppeteer/pnpm-store）
```bash
du -sh ~/.cache/uv ~/.cache/huggingface ~/.cache/pre-commit ~/.cache/puppeteer ~/.cache/rod ~/.npm/_cacache ~/.pnpm-store ~/.bun ~/.gradle 2>/dev/null | sort -rh
```

7. **Library/Caches 大户**
```bash
du -d1 -h ~/Library/Caches 2>/dev/null | sort -rh | head -15
```

8. **Application Support 大户**
```bash
du -d1 -h ~/Library/Application\ Support/ 2>/dev/null | sort -rh | head -10
```

9. **Downloads 安装包 + 废纸篓**
```bash
du -sh ~/.Trash/ 2>/dev/null; echo "---"; find ~/Downloads -maxdepth 1 \( -name "*.dmg" -o -name "*.pkg" -o -name "*.app" -o -name "*.zip" \) -exec ls -lhS {} \; 2>/dev/null
```

10. **大的 .git 目录**（仅供参考）
```bash
find ~/Desktop/code -name ".git" -type d -maxdepth 4 -exec du -sh {} \; 2>/dev/null | sort -rh | head -10
```

11. **Docker 占用**
```bash
docker system df 2>/dev/null || true
```

### 第二步：生成清理报告 + 编号菜单

汇总所有扫描结果，按以下格式输出：

```
## 磁盘概况
总容量: XXX | 已用: XXX | 可用: XXX

## 可清理项目（按释放空间排序）

### 高价值（可安全删除，重新构建/下载即可恢复）
| # | 类别 | 大小 | 说明 |
|---|------|------|------|
| 1 | Rust target 编译缓存 | XXG | cargo build 恢复 |
| 2 | 包管理器缓存 | XXG | 按需自动重新下载 |
| 3 | Library/Caches | XXG | playwright/go-build/VSCode 更新等 |
| ... | ... | ... | ... |

### 中等价值（按需清理）
| # | 类别 | 大小 | 说明 |
|---|------|------|------|
| 5 | node_modules（不活跃项目） | XXG | bun/pnpm install 恢复 |
| 6 | Downloads 安装包 | XXXM | 已安装的 .dmg/.pkg 可删 |
| ... | ... | ... | ... |

### 仅供参考（不建议删除）
| 类别 | 大小 | 说明 |
|------|------|------|
| .git 大仓库 | XXG | 删除即丢失历史 |
| .rustup | XXG | 工具链，删除需重装 |
| ... | ... | ... |

## 预计可释放: XXG

---
选择要清理的编号（如 1,2,3 或 "全部"）：
```

### 第三步：执行清理

用户选择编号后，**按类别并行执行删除**。

**关键：删除命令必须使用绝对路径（`/Users/xxx/...`），不要用 `~` 或 `$HOME`。**

**缓存目录删除必须精确到子目录**（避免 hook 拦截顶层隐藏目录）：
```bash
# ✅ 正确 — 精确子目录
rm -rf /Users/xxx/.cache/uv/cache /Users/xxx/.cache/uv/sdists-v9
rm -rf /Users/xxx/.gradle/caches /Users/xxx/.gradle/wrapper /Users/xxx/.gradle/daemon
rm -rf /Users/xxx/.npm/_cacache
rm -rf /Users/xxx/.bun/install/cache
rm -rf /Users/xxx/.cache/pre-commit
rm -rf /Users/xxx/.cache/rod/browser

# ❌ 错误 — 会被 hook 拦截
rm -rf ~/.cache/uv ~/.gradle ~/.bun
```

**Library/Caches 常见可清理项**（按扫描结果选择性清理）：
```bash
rm -rf /Users/xxx/Library/Caches/ms-playwright
rm -rf /Users/xxx/Library/Caches/go-build
rm -rf /Users/xxx/Library/Caches/com.microsoft.VSCode.ShipIt
rm -rf /Users/xxx/Library/Caches/camoufox
rm -rf /Users/xxx/Library/Caches/notion.id.ShipIt
rm -rf /Users/xxx/Library/Caches/pnpm
```

**node_modules 清理**：列出所有 node_modules 路径，一条 rm -rf 命令删除。

**Docker 清理**（如用户选择）：
```bash
docker system prune -af --volumes
```

### 第四步：验证

```bash
df -h /
```

输出清理前后对比表：
```
| 指标 | 清理前 | 清理后 |
|------|--------|--------|
| 可用空间 | XXG | XXG |
| 使用率 | XX% | XX% |

释放了约 XXG
```

## 安全规则

- **绝不删除**用户文档、照片、代码源文件
- **绝不删除** `.git` 目录（只报告大小供参考）
- **绝不删除**当前工作目录下的 `target/` 或 `node_modules/`
- 只删除缓存、编译产物、安装包等可恢复的内容
- 删除后运行 `df -h /` 报告释放了多少空间
- 删除命令使用绝对路径，缓存目录精确到子目录级别

## 注意事项

- 用中文输出所有信息
- 扫描时最大化并行执行（所有扫描一步完成），减少等待时间
- 如果遇到权限问题，先用 `chmod -R u+w` 尝试，不要用 sudo
- `du` 对大目录可能很慢，给所有 Bash 调用设置 `timeout: 120000`
