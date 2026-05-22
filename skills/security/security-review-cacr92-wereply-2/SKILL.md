---
name: security-review
description: 当用户要求安全审查、安全检查、漏洞扫描或提到安全时使用。
---

# 安全审查 Skill

## 桌面应用安全重点
- ✅ 本地数据保护、API 密钥管理、Tauri 命令安全、SQL 注入防护
- ❌ 不适用：CSRF、CSP（Web 应用安全措施）

## 安全检查清单

### 1. 密钥管理
- [ ] 无硬编码 API 密钥、密码、tokens
- [ ] 所有密钥使用环境变量
- [ ] 敏感配置已加密存储

```rust
// ✓ 正确
let api_key = env::var("OPENAI_API_KEY")?;

// ✗ 错误
const API_KEY: &str = "sk-1234567890";
```

### 2. Tauri 命令安全
- [ ] 所有命令参数已验证
- [ ] 使用 validator crate
- [ ] 错误消息不暴露内部信息

```rust
#[derive(Deserialize, Validate, Type)]
pub struct CreateFormulaDto {
    #[validate(length(min = 2, max = 50))]
    pub name: String,
}

#[tauri::command]
#[specta::specta]
pub async fn create_formula(dto: CreateFormulaDto) -> ApiResponse<Formula> {
    if let Err(e) = dto.validate() {
        return api_err(format!("输入验证失败: {}", e));
    }
    // ...
}
```

### 3. SQL 注入防护
- [ ] 使用 SQLx 参数化查询
- [ ] 禁止字符串拼接 SQL
- [ ] 动态查询使用 QueryBuilder

```rust
// ✓ 正确
sqlx::query_as!(Formula, "SELECT * FROM formulas WHERE name = ?", name)

// ✗ 错误
let sql = format!("SELECT * FROM formulas WHERE name = '{}'", name);
```

### 4. 输入验证
- [ ] 前端验证（第一道防线）
- [ ] 后端验证（必须有）
- [ ] 文件路径验证防止路径遍历

```rust
pub fn validate_file_path(path: &str) -> Result<PathBuf> {
    let path = Path::new(path);
    if path.components().any(|c| c == std::path::Component::ParentDir) {
        return Err(anyhow!("不允许使用 .. 路径"));
    }
    Ok(path.to_path_buf())
}
```

### 5. 敏感数据保护
- [ ] 日志中无密钥、密码
- [ ] 错误消息不暴露内部信息

```rust
// ✓ 正确
info!(formula_id = formula.id, "配方创建成功");

// ✗ 错误
info!("API Key: {}", api_key);
```

### 6. 依赖安全
```bash
cargo audit      # 检查安全漏洞
cargo outdated   # 检查过时依赖
cargo update     # 更新依赖
```

## 安全审查触发条件
- [ ] 添加新的 Tauri 命令
- [ ] 修改数据库访问层
- [ ] 处理用户文件上传/导入
- [ ] 集成第三方 API
- [ ] 添加新的配置项

## 提交前检查
- [ ] `cargo clippy` 无安全警告
- [ ] `cargo audit` 无已知漏洞
- [ ] 无硬编码密钥
- [ ] 所有 SQL 查询使用参数化
- [ ] 所有 Tauri 命令参数已验证
- [ ] 日志中无敏感信息

## 常见安全陷阱
1. **信任前端验证** → 后端必须再次验证
2. **日志记录敏感信息** → 只记录必要信息
3. **SQL 字符串拼接** → 使用参数化查询
4. **过于详细的错误消息** → 返回通用错误消息