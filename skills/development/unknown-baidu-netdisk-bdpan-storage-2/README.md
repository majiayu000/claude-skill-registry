<h1 align="center">baidu-wenku-aippt-personal</h1>

<p align="center">
  <b>百度文库智能PPT个人版</b>
</p>

<p align="center">
  <a href="https://github.com/BaiduNetdiskAIBot/bdpan-storage/releases"><img src="https://img.shields.io/badge/version-v1.0.0-blue" alt="Version"></a>
  <a href="../../LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-green" alt="License"></a>
  <a href="https://pan.baidu.com/apaastobui/developer#/developer/skill"><img src="https://img.shields.io/badge/skill-baidu--wenku--aippt-orange" alt="Skill"></a>
</p>

<p align="center">
  面向个人用户提供职场汇报材料、教育课件生成、营销方案等各行业场景核心应用场景，提供AI驱动的PPT自动生成服务，显著提升工作产出效率。其根据用户输入的PPT主题内容指令，匹配合适的模板自动生成PPT文件，并以可下载链接的形式提供。<br/>
  适配 Claude Code · OpenClaw · DuClaw · KimiClaw · Manus 等 AI Agent
</p>

---

## 一键安装

```bash
npx skills add https://github.com/baidu-netdisk/bdpan-storage/skills --skill baidu-wenku-aippt-personal
```

首次使用时，Skill 会自动引导完成 CLI 工具安装和百度网盘登录授权。

## 用自然语言生成 PPT

安装完成后，在你的 AI Agent 中直接说：

```
帮我做一个关于人工智能在医疗领域应用的PPT
```

```
生成一份年终总结PPT，大概20页，商务风格
```

```
做一个中国风的传统节日介绍PPT
```

```
帮我制作一个关于英国摇滚乐队历史与现状的演示文稿
```

Skill 自动识别意图、智能匹配风格参数、生成 PPT 并返回预览链接。

## 功能参数

| 参数 | 可选值 | 默认 |
|------|--------|------|
| **页数** | 1-10、11-20、21-30、31-40、40+ | 11-20 |
| **风格** | 默认、创意趣味、年终总结、卡通手绘、扁平简约、文艺清新、中国风、企业商务、未来科技、文化艺术 | 默认 |
| **场景** | 默认、晚会表彰、传统节日、婚姻爱情、生日祝福、医学科普、建筑报告、工作总结、年终总结、工作汇报 | 默认 |
| **配色** | 默认、绿色、蓝色、紫色、橙色、黄色、红色、黑色、白色 | 默认 |

> Agent 会根据你的描述自动选择最匹配的参数组合，无需手动指定。

## 使用示例

### 简单主题

```
帮我做一个关于人工智能的PPT
```

```
PPT 生成成功!
文件：人工智能发展与应用.pptx
已保存到：我的应用数据/bdpan/百度文库智能PPT/人工智能发展与应用.pptx
预览链接：https://pan.baidu.com/pfile/docview?path=...
```

### 指定风格和页数

```
做一个30页左右的企业商务风格的季度工作汇报PPT
```

```
PPT 生成成功!
文件：季度工作汇报.pptx
已保存到：我的应用数据/bdpan/百度文库智能PPT/季度工作汇报.pptx
预览链接：https://pan.baidu.com/pfile/docview?path=...
```

## 安全设计

| 特性 | 说明 |
|------|------|
| **OAuth 2.0** | 授权码模式认证，不存储用户密码 |
| **Token 保护** | 配置文件含 Token，Agent 禁止读取或输出其内容 |
| **安全传码** | 授权码通过 stdin 传递，不暴露在进程列表中 |
| **SHA256 校验** | 安装和更新的二进制文件强制完整性校验 |
| **更新需确认** | 禁止自动或静默更新，必须用户明确指令并确认 |

## 系统支持

| 平台 | 架构 | 状态 |
|------|------|:----:|
| macOS | arm64 / amd64 | &#x2705; |
| Linux | arm64 / amd64 | &#x2705; |
| Windows (WSL) | amd64 | &#x2705; |
| Windows (原生) | — | &#x274C; |

## 故障排除

遇到问题时，直接对 Skill 说：

- **Token 过期** — "token 过期了" → 自动引导重新登录
- **检查状态** — "检查登录状态" → 显示当前认证信息
- **更新** — "更新一下" → 检查并更新 Skill 和 CLI

更多故障排查指南参见 [reference/troubleshooting.md](./reference/troubleshooting.md)。

## 项目结构

```
skills/baidu-wenku-aippt-personal/
├── SKILL.md                    # Skill 定义（Agent 行为规范）
├── VERSION                     # 版本号
├── README.md                   # 本文件
├── reference/                  # 参考文档
│   ├── aippt-examples.md       # AI PPT 使用示例
│   ├── authentication.md       # 认证流程说明
│   └── troubleshooting.md      # 故障排查
└── scripts/                    # 管理脚本
    ├── install.sh              # 安装
    ├── login.sh                # 登录
    ├── update.sh               # 更新
    └── uninstall.sh            # 卸载
```

## 许可证

[Apache License 2.0](../../LICENSE)
