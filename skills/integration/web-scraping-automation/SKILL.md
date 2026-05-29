---
name: web-scraping-automation
description: 自动化爬取网站数据和 API 接口。当用户需要抓取网页内容、调用 API、解析数据或创建爬虫脚本时使用此技能。
allowed-tools: Bash, Read, Write, Edit, WebFetch, WebSearch
---

# 网站爬取与 API 自动化

## 功能说明
此技能专门用于自动化网站数据爬取和 API 接口调用，包括：
- 分析和爬取网站结构
- 调用和测试 REST/GraphQL API
- 创建自动化爬虫脚本
- 数据解析和清洗
- 处理反爬虫机制
- 定时任务和数据存储

## 使用场景
- "爬取这个网站的产品信息"
- "帮我调用这个 API 并解析返回数据"
- "创建一个脚本定时抓取新闻"
- "分析这个网站的 API 接口文档"
- "绕过这个网站的反爬虫限制"

## 技术栈
### Python 爬虫
- **requests**：HTTP 请求库
- **BeautifulSoup4**：HTML 解析
- **Scrapy**：专业爬虫框架
- **Selenium**：浏览器自动化
- **Playwright**：现代浏览器自动化

### JavaScript 爬虫
- **axios**：HTTP 客户端
- **cheerio**：服务端 jQuery
- **puppeteer**：Chrome 自动化
- **node-fetch**：Fetch API

## 工作流程
1. **目标分析**：
   - 检查网站结构和数据位置
   - 分析 API 接口和认证方式
   - 评估反爬虫机制

2. **方案设计**：
   - 选择合适的技术栈
   - 设计数据提取策略
   - 规划错误处理和重试机制

3. **脚本开发**：
   - 编写爬虫代码
   - 实现数据解析逻辑
   - 添加日志和监控

4. **测试优化**：
   - 验证数据准确性
   - 优化性能和稳定性
   - 处理边界情况

## 最佳实践
- 遵守 robots.txt 规则
- 设置合理的请求间隔
- 使用 User-Agent 和请求头
- 实现错误重试机制
- 数据去重和验证
- 使用代理池（如需要）
- 保存原始数据和日志

## 常见场景示例

### 1. 简单网页爬取
```python
import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取数据
    data = []
    for item in soup.select('.product'):
        data.append({
            'title': item.select_one('.title').text,
            'price': item.select_one('.price').text
        })
    return data
```

### 2. API 调用
```python
import requests

def call_api(endpoint, params=None):
    headers = {
        'Authorization': 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    }
    response = requests.get(endpoint, headers=headers, params=params)
    return response.json()
```

### 3. 动态网页爬取
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_dynamic_page(url):
    driver = webdriver.Chrome()
    driver.get(url)

    # 等待页面加载
    driver.implicitly_wait(10)

    # 提取数据
    elements = driver.find_elements(By.CLASS_NAME, 'item')
    data = [elem.text for elem in elements]

    driver.quit()
    return data
```

## 反爬虫应对策略
- **请求头伪装**：模拟真实浏览器
- **代理轮换**：使用代理池
- **验证码处理**：OCR 或第三方服务
- **Cookie 管理**：维护会话状态
- **请求频率控制**：避免触发限制
- **JavaScript 渲染**：使用 Selenium/Playwright

## 数据存储方案
- **CSV/Excel**：简单数据导出
- **JSON**：结构化数据存储
- **数据库**：MySQL、PostgreSQL、MongoDB
- **云存储**：S3、OSS
- **数据仓库**：用于大规模数据分析
