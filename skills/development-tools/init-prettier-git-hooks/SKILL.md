---
name: init-prettier-git-hooks
description: 初始化基于 lint-staged + simple-git-hooks + prettier 的 git 提交前代码格式化流程。用于在任何 Node.js 项目中快速搭建代码格式化和 git 钩子配置。
user-invocable: true
metadata:
  version: "0.13.4"
---

# 初始化 Prettier + Git Hooks 格式化流程

本技能用于在任何 Node.js 项目中初始化基于 `lint-staged` + `simple-git-hooks` + `prettier` 的 git 提交前代码格式化流程。

## 1. 必须安装的依赖（devDependencies）

执行以下命令安装所有必要的依赖：

```bash
pnpm add -D prettier @prettier/plugin-oxc prettier-plugin-lint-md lint-staged simple-git-hooks commitlint
```

依赖说明：

|         依赖名称          |                说明                 |
| :-----------------------: | :---------------------------------: |
|        `prettier`         |         核心代码格式化工具          |
|  `@prettier/plugin-oxc`   |   使用 oxc 引擎解析 JS/TS，更快速   |
| `prettier-plugin-lint-md` |       Markdown 文件格式化插件       |
|       `lint-staged`       | 只对 git 暂存区文件执行 lint/format |
|    `simple-git-hooks`     |      轻量级 git hooks 管理工具      |
|       `commitlint`        |        git 提交信息规范校验         |

## 2. 必须创建/修改的配置文件

### 2.1. 创建 `prettier.config.mjs`

从模板复制：参见 [templates/prettier.config.mjs](./templates/prettier.config.mjs)

### 2.2. 创建 `lint-staged.config.js`

从模板复制：参见 [templates/lint-staged.config.js](./templates/lint-staged.config.js)

### 2.3. 创建 `simple-git-hooks.mjs`

从模板复制：参见 [templates/simple-git-hooks.mjs](./templates/simple-git-hooks.mjs)

### 2.4. 更新 `package.json`

需要在 `package.json` 中添加/修改以下内容：

**scripts 部分新增命令：**

```json
{
	"scripts": {
		"format": "prettier --experimental-cli --write .",
		"prepare": "<原有的 prepare 命令> && simple-git-hooks"
	}
}
```

说明：

|   命令    |                 说明                  |
| :-------: | :-----------------------------------: |
| `format`  |     手动格式化整个项目的所有文件      |
| `prepare` | 在 npm install 后自动初始化 git hooks |

**注意：** 如果项目原本没有 `prepare` 命令，则直接设置为 `"prepare": "simple-git-hooks"`。

## 3. 初始化 Git Hooks

配置文件创建完成后，需要执行以下命令来初始化 git hooks：

```bash
# 如果 simple-git-hooks 的 postinstall 脚本被阻止，需要先批准
pnpm approve-builds simple-git-hooks

# 执行初始化 git hooks
npx simple-git-hooks
```

成功后会看到类似输出：

```log
[INFO] Successfully set the pre-commit with command: npx lint-staged
[INFO] Successfully set the commit-msg with command: npx --no-install commitlint --edit ${1}
[INFO] Successfully set all git hooks
```

## 4. 自检清单

完成初始化后，请逐项检查以下内容：

- [ ] 1. **依赖安装**：`package.json` 的 `devDependencies` 中包含以下依赖：
  - [ ] `prettier`
  - [ ] `@prettier/plugin-oxc`
  - [ ] `prettier-plugin-lint-md`
  - [ ] `lint-staged`
  - [ ] `simple-git-hooks`
  - [ ] `commitlint`（或 `@commitlint/cli`）

- [ ] 2. **配置文件存在**：
  - [ ] `prettier.config.mjs` 存在
  - [ ] `lint-staged.config.js` 存在
  - [ ] `simple-git-hooks.mjs` 存在

- [ ] 3. **package.json scripts**：
  - [ ] 存在 `format` 命令
  - [ ] `prepare` 命令包含 `simple-git-hooks`

- [ ] 4. **Git hooks 初始化**：
  - [ ] 执行 `npx simple-git-hooks` 成功

- [ ] 5. **功能验证**：
  - [ ] 执行 `pnpm format` 能正常格式化代码
  - [ ] git commit 时会自动触发 lint-staged 格式化

## 5. 工作流程说明

当你执行 `git commit` 时，会自动触发以下流程：

1. **pre-commit 钩子**触发 → 执行 `npx lint-staged`
2. lint-staged 对暂存区的文件执行 `prettier --experimental-cli --write`
3. **commit-msg 钩子**触发 → 执行 `npx --no-install commitlint --edit ${1}` 校验提交信息格式

## 6. 注意事项

1. **修改 `simple-git-hooks.mjs` 后**，务必重新执行 `npx simple-git-hooks` 命令来更新 git hooks。
2. **首次安装依赖时**，如果 pnpm 提示 `simple-git-hooks` 的 postinstall 脚本被忽略，需要执行 `pnpm approve-builds simple-git-hooks` 来允许其运行。
3. **Prettier 使用 `--experimental-cli` 参数**，这是启用实验性 CLI 功能的必要参数。
