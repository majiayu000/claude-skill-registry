---
name: rainMcp-release
description: rainMcp 项目版本发布相关操作流程
---

## 版本升级流程

```bash
# 1. 查找当前版本号
grep -h "\"version\":" package.json src-tauri/Cargo.toml src-tauri/tauri.conf.json | head -1 | grep -oP '\d+\.\d+\.\d+'

# 2. 批量修改版本号（将 0.6.1 替换为 0.6.2）
sed -i '' 's/0\.6\.1/0.6.2/g' package.json src-tauri/Cargo.toml src-tauri/tauri.conf.json

# 3. 更新 Cargo.lock
cd src-tauri && cargo check

# 4. 运行检查
bun run lint
bun run format

# 5. 确认修改
git status
git diff

# 6. 提交和推送
git add package.json src-tauri/Cargo.toml src-tauri/Cargo.lock src-tauri/tauri.conf.json
git commit -m "chore: release version 0.6.2"
git tag v0.6.2
git push
git push --tags
```
