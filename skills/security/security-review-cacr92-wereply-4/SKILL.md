# 安全审查 Skill

## 核心目标

在代码提交前识别和防止常见安全漏洞（针对 Tauri 桌面应用）。

---

## 桌面应用安全重点

本项目是 Tauri 桌面应用，安全重点与 Web 应用不同：
- ✅ 重点：本地数据保护、API 密钥管理、Tauri 命令安全、SQL 注入防护
- ❌ 不适用：CSRF、CSP（这些是 Web 应用的安全措施）

---

## 安全检查清单

### 1. 密钥管理 ✓
- [ ] 无硬编码 API 密钥
- [ ] 无硬编码密码
- [ ] 无硬编码 tokens
- [ ] 所有密钥使用环境变量
- [ ] 敏感配置已加密存储

**✓ 正确示例**：
```rust
use std::env;

let api_key = env::var("OPENAI_API_KEY")
    .context("OPENAI_API_KEY 环境变量未设置")?;
```

**✗ 错误示例**：
```rust
const API_KEY: &str = "sk-1234567890";  // ✗ 硬编码密钥
```

---

### 2. Tauri 命令安全 ✓
- [ ] 所有命令参数已验证
- [ ] 使用 validator crate 验证输入
- [ ] 敏感操作有权限检查
- [ ] 错误消息不暴露内部信息

**✓ 正确示例**：
```rust
use validator::Validate;

#[derive(Deserialize, Validate, Type)]
pub struct CreateFormulaDto {
    #[validate(length(min = 2, max = 50))]
    pub name: String,

    #[validate(length(equal = 3))]
    pub species_code: String,
}

#[tauri::command]
#[specta::specta]
pub async fn create_formula(
    dto: CreateFormulaDto,
    state: State<'_, TauriAppState>,
) -> ApiResponse<Formula> {
    // 验证输入
    if let Err(e) = dto.validate() {
        return api_err(format!("输入验证失败: {}", e));
    }

    // 处理逻辑...
}
```

---

### 3. SQL 注入防护 ✓
- [ ] 使用 SQLx 参数化查询
- [ ] 禁止字符串拼接 SQL
- [ ] 动态查询使用 QueryBuilder

**✓ 正确示例**：
```rust
// 参数化查询
sqlx::query_as!(
    Formula,
    "SELECT * FROM formulas WHERE name = ?",
    name
)
.fetch_one(&self.pool)
.await?;

// 动态查询使用 QueryBuilder
let mut query = QueryBuilder::new("SELECT * FROM formulas WHERE 1=1");
if let Some(name) = filters.name {
    query.push(" AND name LIKE ");
    query.push_bind(format!("%{}%", name));
}
```

**✗ 错误示例**：
```rust
// ✗ 字符串拼接 SQL
let sql = format!("SELECT * FROM formulas WHERE name = '{}'", name);
```

---

### 4. 输入验证 ✓
- [ ] 前端验证（第一道防线）
- [ ] 后端验证（必须有）
- [ ] 文件上传验证类型和大小
- [ ] 路径验证防止路径遍历

**前端验证**：
```typescript
<Form.Item
  name="name"
  rules={[
    { required: true, message: '请输入配方名称' },
    { min: 2, max: 50, message: '名称长度为 2-50 个字符' },
    { pattern: /^[\u4e00-\u9fa5a-zA-Z0-9_-]+$/, message: '只能包含中文、字母、数字、下划线和连字符' }
  ]}
>
  <Input />
</Form.Item>
```

**后端验证**：
```rust
#[derive(Deserialize, Validate, Type)]
pub struct CreateFormulaDto {
    #[validate(length(min = 2, max = 50))]
    #[validate(regex = "FORMULA_NAME_REGEX")]
    pub name: String,
}
```

**文件路径验证**：
```rust
pub fn validate_file_path(path: &str) -> Result<PathBuf> {
    let path = Path::new(path);

    // 检查路径遍历攻击
    if path.components().any(|c| c == std::path::Component::ParentDir) {
        return Err(anyhow!("不允许使用 .. 路径"));
    }

    Ok(path.to_path_buf())
}
```

---

### 5. 敏感数据保护 ✓
- [ ] 日志中无密钥
- [ ] 日志中无密码
- [ ] 错误消息不暴露内部信息
- [ ] 敏感字段已加密存储

**✓ 正确示例**：
```rust
// 日志记录
info!(
    formula_id = formula.id,
    "配方创建成功"
);
// ✓ 不记录 API 密钥、密码等

// 错误处理
match repository.find_by_id(id).await {
    Ok(formula) => api_ok(formula),
    Err(e) => {
        error!(error = %e, "查询配方失败");
        // 返回通用错误消息
        api_err("查询配方失败，请稍后重试".to_string())
    }
}
```

**✗ 错误示例**：
```rust
// ✗ 记录敏感信息
info!("API Key: {}", api_key);

// ✗ 暴露内部错误
api_err(format!("数据库错误: {}", db_error))
```

---

### 6. XSS 防护（桌面应用风险较低）✓
- [ ] React 默认转义内容
- [ ] 如需渲染 HTML，使用 DOMPurify
- [ ] 避免 dangerouslySetInnerHTML

**✓ 正确示例**：
```typescript
// React 默认转义
<div>{userInput}</div>

// 如需渲染 HTML
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userInput);
<div dangerouslySetInnerHTML={{ __html: clean }} />
```

---

### 7. 文件操作安全 ✓
- [ ] 路径验证
- [ ] 文件类型验证
- [ ] 文件大小限制

**路径验证**：
```rust
pub fn validate_file_path(path: &str) -> Result<PathBuf> {
    let path = Path::new(path);

    if path.components().any(|c| c == std::path::Component::ParentDir) {
        return Err(anyhow!("不允许使用 .. 路径"));
    }

    if path.is_absolute() {
        return Err(anyhow!("不允许使用绝对路径"));
    }

    Ok(path.to_path_buf())
}
```

**文件类型验证**：
```rust
pub fn validate_import_file(path: &Path) -> Result<()> {
    let extension = path.extension()
        .and_then(|s| s.to_str())
        .ok_or_else(|| anyhow!("无效的文件扩展名"))?;

    match extension.to_lowercase().as_str() {
        "xlsx" | "xls" | "csv" => Ok(()),
        _ => Err(anyhow!("不支持的文件类型: {}", extension)),
    }
}
```

---

### 8. 依赖安全 ✓
- [ ] 依赖包已更新
- [ ] 无已知安全漏洞
- [ ] 审查新依赖

**检查命令**：
```bash
# 检查过时的依赖
cargo outdated

# 检查安全漏洞
cargo audit

# 更新依赖
cargo update
```

---

### 9. Rust 特定安全 ✓
- [ ] 避免 unsafe 代码（除非必要）
- [ ] 使用 sqlx 宏防止 SQL 注入
- [ ] 使用 secrecy crate 保护密钥
- [ ] 使用 Result 进行错误处理

**✓ 正确示例**：
```rust
// 使用 Option 而非空指针
pub fn find_material(code: &str) -> Option<Material> { }

// 使用 Result 进行错误处理
pub fn calculate_nutrition(material: &Material) -> Result<Nutrition> { }

// 使用借用检查器防止数据竞争
pub fn process_formulas(formulas: &[Formula]) -> Vec<Result> { }
```

---

### 10. 前端安全（React）✓
- [ ] 验证 Tauri 命令响应
- [ ] 使用 message 组件显示错误
- [ ] 禁止 console.log（桌面应用）

**✓ 正确示例**：
```typescript
const result = await commands.getFormula(id);
if (!result.success) {
  message.error(result.message);
  return;
}

// 验证数据结构
if (!result.data || typeof result.data.id !== 'number') {
  message.error('数据格式错误');
  return;
}

setFormula(result.data);
```

---

## 安全响应协议

### 发现漏洞时的处理流程
1. **立即停止工作**
2. **评估漏洞严重性**
   - 高危：可能导致数据泄露、系统破坏
   - 中危：可能导致功能异常
   - 低危：理论风险，实际影响小
3. **修复漏洞**
4. **轮换暴露的密钥**（如适用）
5. **审计整个代码库**查找类似问题
6. **更新安全检查清单**

---

## 安全审查触发条件

以下情况必须进行安全审查：
- [ ] 添加新的 Tauri 命令
- [ ] 修改数据库访问层
- [ ] 处理用户文件上传/导入
- [ ] 集成第三方 API
- [ ] 添加新的配置项
- [ ] 修改认证/授权逻辑（如有）

---

## 提交前安全检查清单

- [ ] 运行 `cargo clippy` 无安全警告
- [ ] 运行 `cargo audit` 无已知漏洞
- [ ] 无硬编码密钥
- [ ] 所有 SQL 查询使用参数化
- [ ] 所有 Tauri 命令参数已验证
- [ ] 敏感数据已加密存储
- [ ] 日志中无敏感信息
- [ ] 错误消息不暴露内部细节
- [ ] 无不必要的 `unsafe` 代码
- [ ] 前端无 `dangerouslySetInnerHTML`（或已清理��

---

## 常见安全陷阱

### 1. 信任前端验证
**✗ 错误**：只在前端验证，后端不验证
**✓ 正确**：前后端都验证，后端验证是最后防线

### 2. 日志记录敏感信息
**✗ 错误**：`info!("API Key: {}", key)`
**✓ 正确**：`info!("API 调用成功")`

### 3. SQL 字符串拼接
**✗ 错误**：`format!("SELECT * FROM users WHERE id = {}", id)`
**✓ 正确**：`sqlx::query_as!(..., "WHERE id = ?", id)`

### 4. 过于详细的错误消息
**✗ 错误**：`api_err(format!("数据库连接失败: {}", db_error))`
**✓ 正确**：`api_err("操作失败，请稍后重试".to_string())`

---

## 何时使用此 Skill

- ✅ 添加新 Tauri 命令时
- ✅ 修改数据库访问层时
- ✅ 处理用户文件上传时
- ✅ 集成第三方 API 时
- ✅ 代码审查时
- ✅ 用户明确要求安全审查时

---

## 与其他 Skill 的配合

- 与 `code-review` skill 配合进行全面审查
- 与 `debugging` skill 配合排查安全问题
- 与 `testing-strategy` skill 配合编写安全测试

---

## 参考资源

- [Rust Security Guidelines](https://anssi-fr.github.io/rust-guide/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Tauri Security](https://tauri.app/v1/references/architecture/security/)
- 项目规范：`.claude/rules/06-security-standards.md`
