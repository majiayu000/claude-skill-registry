---
name: secrets-detection
description: |
  用于检测代码库中的敏感信息泄露风险。当用户需要检查敏感信息、安全扫描、代码安全审计、检测密钥泄露时触发此skill。
  
  触发场景：
  - "检查敏感信息"、"安全检查"、"检测密钥泄露"
  - "扫描代码中的敏感数据"、"查找密码泄露"
  - 提交代码前的安全检查
  - 代码审查前的安全扫描
  - 检查.gitignore是否正确配置
  
  检测范围：API密钥、密码、私钥、证书文件、数据库连接串、云服务凭证等敏感信息。
---

# 敏感信息检测 Skill

## 概述

此skill帮助检测代码库中可能泄露的敏感信息，包括：
- 已跟踪的敏感文件（.env, .pem, .key等）
- 代码中的硬编码密钥和密码
- 私钥和证书内容
- 云服务凭证（AWS, GitHub, Google等）
- 数据库连接字符串
- Git历史中的敏感文件

## 使用方法

### 步骤1：运行Python扫描脚本

首先运行自动化扫描脚本：

```bash
python <skill-path>/scripts/secrets_scanner.py <target-path>
```

参数说明：
- `<target-path>`: 要扫描的目录路径，默认为当前目录
- `--json`: 输出JSON格式结果
- `--quiet`: 静默模式

示例：
```bash
# 扫描当前目录
python ~/.my-skills-collection/skills/secrets-detection/scripts/secrets_scanner.py .

# 扫描指定目录并输出JSON
python ~/.my-skills-collection/skills/secrets-detection/scripts/secrets_scanner.py ./src --json
```

### 步骤2：额外检查（脚本不易覆盖）

扫描脚本完成后，执行以下额外检查：

#### 2.1 检查示例文件是否包含真实凭证

```bash
# 检查示例配置文件
grep -rE "(sk-|AKIA|ghp_|AIza)" --include="*.example" --include="*.sample" .
```

如果发现真实凭证，需要替换为占位符。

#### 2.2 检查README和文档中的凭证

```bash
# 检查文档中是否有泄露
grep -rE "(password|secret|token|key)\s*=\s*['\"][^'\"]{10,}['\"]" --include="*.md" .
```

#### 2.3 检查Docker配置

```bash
# 检查Dockerfile和docker-compose中的敏感信息
grep -rE "(ENV.*PASSWORD|ENV.*SECRET|ENV.*KEY|ENV.*TOKEN)" --include="Dockerfile*" --include="docker-compose*" .
```

#### 2.4 检查CI/CD配置

```bash
# 检查CI配置中的硬编码凭证
grep -rE "(password|secret|token|key)" --include="*.yml" --include="*.yaml" .github/ .gitlab-ci.yml Jenkinsfile 2>/dev/null | grep -v "\${{" | grep -v "secrets\."
```

### 步骤3：生成报告

根据扫描结果，生成如下格式的报告：

## 报告模板

```markdown
# 敏感信息扫描报告

## 扫描概述
- 扫描路径: <path>
- 扫描时间: <timestamp>
- 问题总数: <count>

## 发现的问题

### 严重问题 (Critical)
| 文件 | 行号 | 描述 | 建议 |
|------|------|------|------|
| ... | ... | ... | ... |

### 高危问题 (High)
| 文件 | 行号 | 描述 | 建议 |
|------|------|------|------|
| ... | ... | ... | ... |

### 中危问题 (Medium)
| 文件 | 行号 | 描述 | 建议 |
|------|------|------|------|
| ... | ... | ... | ... |

## 建议的修复措施

1. **立即轮换泄露的凭证**
2. **将敏感信息移至环境变量或密钥管理服务**
3. **更新.gitignore配置**
4. **从Git历史中移除敏感文件**（如已提交）

## .gitignore 推荐配置

确保以下模式在.gitignore中：
```gitignore
# 环境变量
.env
.env.local
.env.*.local

# 密钥和证书
*.pem
*.key
*.p12
*.pfx

# 凭证文件
credentials.json
secrets.yaml
```
```

## 检测规则说明

### 敏感文件模式
| 文件模式 | 风险级别 |
|----------|----------|
| .env, .env.local | 高 |
| *.pem, *.key | 严重 |
| id_rsa, id_ed25519 | 严重 |
| credentials.json | 高 |
| secrets.yaml | 高 |

### 密钥格式检测
| 格式 | 服务 |
|------|------|
| AKIA... | AWS Access Key |
| ghp_... | GitHub Token |
| sk-... | OpenAI API Key |
| AIza... | Google API Key |
| xox... | Slack Token |
| eyJ... | JWT Token |

### 关键词检测
- api_key, apikey, secret_key, private_key
- password, passwd, pwd
- access_token, auth_token, bearer
- aws_access_key_id, aws_secret_access_key

## 泄露后的处理流程

如果发现敏感信息已泄露：

1. **立即撤销/轮换密钥** - 最高优先级
2. **从代码中移除敏感信息**
3. **从Git历史中移除**：
   ```bash
   # 使用git filter-repo
   git filter-repo --path .env --invert-paths
   
   # 或使用BFG
   bfg --delete-files .env
   ```
4. **通知安全团队**（如适用）
5. **审计相关系统访问日志**

## 注意事项

- 扫描脚本会忽略 node_modules、.venv、.git 等目录
- 示例文件（.example）中的占位符会被忽略
- 某些模式可能产生误报，需要人工确认
- Git历史检查需要完整的Git仓库