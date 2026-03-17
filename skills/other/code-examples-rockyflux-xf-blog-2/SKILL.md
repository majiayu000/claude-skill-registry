---
name: code-examples
description: 生成高质量的技术代码示例，支持多种编程语言和框架。使用时需要创建代码示例、演示用法、提供配置模板时。
---

# 代码示例生成助手

## 支持的语言和框架

### 编程语言
- **JavaScript/TypeScript**：前端开发、Node.js、工具脚本
- **Python**：数据处理、AI应用、自动化脚本
- **Bash/Shell**：系统管理、部署脚本、工具配置
- **Go**：后端服务、CLI工具、系统编程
- **Rust**：系统编程、性能敏感应用

### 框架和工具
- **前端**：Vue.js, React, Vite, Webpack
- **后端**：Express, FastAPI, Gin
- **数据库**：MySQL, PostgreSQL, MongoDB
- **部署**：Docker, Kubernetes, CI/CD

## 示例质量标准

### 代码要求
- **完整性**：可直接运行的完整代码
- **注释**：关键步骤有中文注释说明
- **错误处理**：包含基本的错误处理
- **最佳实践**：遵循语言和框架的最佳实践

### 文档要求
- **场景描述**：明确的使用场景
- **依赖说明**：列出所需的依赖包
- **运行说明**：如何执行代码
- **输出示例**：预期的运行结果

## 常用示例模板

### Node.js API 服务
```javascript
const express = require('express');
const app = express();

// 中间件配置
app.use(express.json());

// API 路由
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 启动服务
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`服务运行在端口 ${PORT}`);
});

module.exports = app;
```

### Python 数据处理
```python
import pandas as pd
from typing import List, Dict

def process_data(file_path: str) -> Dict[str, any]:
    """
    处理 CSV 数据文件

    Args:
        file_path: CSV 文件路径

    Returns:
        包含统计信息的字典
    """
    try:
        # 读取数据
        df = pd.read_csv(file_path)

        # 数据清洗
        df = df.dropna()
        df = df.drop_duplicates()

        # 基本统计
        stats = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'column_names': df.columns.tolist(),
            'summary': df.describe().to_dict()
        }

        return stats

    except Exception as e:
        raise Exception(f"数据处理失败: {str(e)}")

# 使用示例
if __name__ == "__main__":
    result = process_data("data.csv")
    print(f"处理了 {result['total_rows']} 行数据")
```

### Bash 部署脚本
```bash
#!/bin/bash

# 部署脚本
# 使用方法: ./deploy.sh [environment]

set -e  # 遇到错误立即退出

ENVIRONMENT=${1:-production}
PROJECT_DIR="/var/www/myapp"
BACKUP_DIR="/var/backups"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

# 备份当前版本
backup_current_version() {
    log "创建备份..."
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    tar -czf "${BACKUP_DIR}/app_${TIMESTAMP}.tar.gz" -C "$PROJECT_DIR" .
}

# 部署新版本
deploy() {
    log "部署到 $ENVIRONMENT 环境..."

    # 拉取最新代码
    git pull origin main

    # 安装依赖
    npm ci

    # 构建应用
    npm run build

    # 重启服务
    pm2 restart ecosystem.config.js --env $ENVIRONMENT

    log "部署完成！"
}

# 主函数
main() {
    log "开始部署流程..."

    backup_current_version
    deploy

    log "部署成功完成！"
}

# 执行部署
main "$@"
```

### Docker 配置
```dockerfile
# 多阶段构建示例
FROM node:18-alpine AS builder

WORKDIR /app

# 复制依赖文件
COPY package*.json ./
RUN npm ci --only=production

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 生产镜像
FROM nginx:alpine

# 复制构建结果
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制 nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

## 示例生成指南

### 根据场景选择
1. **快速原型**：提供最小可运行示例
2. **生产就绪**：包含错误处理、日志、配置
3. **学习示例**：详细注释，逐步解释
4. **最佳实践**：遵循行业标准和约定

### 结构化组织
- **引入部分**：导入语句和依赖
- **配置部分**：常量、配置项定义
- **核心逻辑**：主要功能实现
- **工具函数**：辅助函数
- **入口点**：程序启动逻辑

### 测试和验证
- 包含单元测试示例
- 提供测试数据
- 说明如何验证功能

## 语言特定规范

### JavaScript/TypeScript
- 使用 ES6+ 语法
- 添加 JSDoc 注释
- 使用 async/await 处理异步
- 遵循 Airbnb 代码规范

### Python
- 使用类型注解
- 遵循 PEP 8 规范
- 添加 docstring 文档
- 使用虚拟环境管理依赖

### Shell 脚本
- 添加错误处理 (set -e)
- 使用函数组织代码
- 添加使用说明和帮助信息
- 支持命令行参数