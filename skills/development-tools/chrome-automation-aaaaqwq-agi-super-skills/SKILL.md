---
name: chrome-automation
description: Chrome 浏览器自动化操作。当用户需要自动化浏览器操作、网页测试、数据抓取或 UI 自动化时使用此技能。
allowed-tools: Bash, Read, Write, Edit
---

# Chrome 浏览器自动化

## 功能说明
此技能专门用于 Chrome 浏览器自动化,包括:
- 网页自动化操作
- E2E 测试
- 网页截图和 PDF 生成
- 表单自动填充
- 动态网页数据抓取
- 性能测试和监控

## 使用场景
- "自动化登录网站并抓取数据"
- "批量截取网页截图"
- "自动化测试购物流程"
- "监控网站性能指标"
- "自动填写表单并提交"
- "生成网页 PDF 报告"

## 技术栈

### 自动化工具
- **Puppeteer**:Chrome DevTools Protocol
- **Playwright**:跨浏览器自动化
- **Selenium**:经典自动化框架
- **Cypress**:现代 E2E 测试框架

### 辅助工具
- **puppeteer-extra**:Puppeteer 插件系统
- **puppeteer-stealth**:反检测插件
- **chrome-launcher**:Chrome 启动器

## 核心功能

### 1. 页面导航
```typescript
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({
  headless: false,  // 显示浏览器
  slowMo: 50        // 减慢操作速度
});

const page = await browser.newPage();

// 导航到页面
await page.goto('https://example.com', {
  waitUntil: 'networkidle2'  // 等待网络空闲
});

// 前进后退
await page.goBack();
await page.goForward();
await page.reload();

await browser.close();
```

### 2. 元素操作
```typescript
// 点击元素
await page.click('#submit-button');

// 输入文本
await page.type('#username', 'user@example.com');
await page.type('#password', 'password123');

// 选择下拉框
await page.select('#country', 'CN');

// 上传文件
const fileInput = await page.$('input[type="file"]');
await fileInput.uploadFile('/path/to/file.pdf');

// 等待元素
await page.waitForSelector('.result', { timeout: 5000 });

// 获取元素文本
const text = await page.$eval('.title', el => el.textContent);

// 获取多个元素
const items = await page.$$eval('.item', elements =>
  elements.map(el => el.textContent)
);
```

### 3. 表单自动化
```typescript
async function fillForm(page: Page) {
  // 填写文本输入框
  await page.type('#name', '张三');
  await page.type('#email', 'zhangsan@example.com');
  await page.type('#phone', '13800138000');

  // 选择单选按钮
  await page.click('input[name="gender"][value="male"]');

  // 选择复选框
  await page.click('#agree-terms');
  await page.click('#subscribe-newsletter');

  // 选择下拉框
  await page.select('#city', 'beijing');

  // 填写日期
  await page.type('#birthday', '1990-01-01');

  // 填写文本域
  await page.type('#message', '这是一条测试消息');

  // 提交表单
  await page.click('button[type="submit"]');

  // 等待提交完成
  await page.waitForNavigation();
}
```

### 4. 数据抓取
```typescript
async function scrapeData(url: string) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.goto(url);

  // 等待内容加载
  await page.waitForSelector('.product-list');

  // 抓取数据
  const products = await page.$$eval('.product-item', items =>
    items.map(item => ({
      title: item.querySelector('.title')?.textContent,
      price: item.querySelector('.price')?.textContent,
      image: item.querySelector('img')?.src,
      link: item.querySelector('a')?.href
    }))
  );

  await browser.close();
  return products;
}
```

### 5. 截图和 PDF
```typescript
// 全页截图
await page.screenshot({
  path: 'screenshot.png',
  fullPage: true
});

// 元素截图
const element = await page.$('.chart');
await element.screenshot({ path: 'chart.png' });

// 生成 PDF
await page.pdf({
  path: 'page.pdf',
  format: 'A4',
  printBackground: true,
  margin: {
    top: '20px',
    right: '20px',
    bottom: '20px',
    left: '20px'
  }
});
```

### 6. 性能监控
```typescript
async function measurePerformance(url: string) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // 开始性能追踪
  await page.tracing.start({ path: 'trace.json' });

  await page.goto(url, { waitUntil: 'networkidle2' });

  // 停止追踪
  await page.tracing.stop();

  // 获取性能指标
  const metrics = await page.metrics();
  console.log('性能指标:', metrics);

  // 获取 Performance API 数据
  const performanceData = await page.evaluate(() => {
    const timing = performance.timing;
    return {
      loadTime: timing.loadEventEnd - timing.navigationStart,
      domReady: timing.domContentLoadedEventEnd - timing.navigationStart,
      firstPaint: performance.getEntriesByType('paint')[0]?.startTime
    };
  });

  await browser.close();
  return performanceData;
}
```

## 高级功能

### 1. 拦截和修改请求
```typescript
await page.setRequestInterception(true);

page.on('request', request => {
  // 阻止图片加载
  if (request.resourceType() === 'image') {
    request.abort();
  }
  // 修改请求头
  else if (request.url().includes('api')) {
    request.continue({
      headers: {
        ...request.headers(),
        'Authorization': 'Bearer token'
      }
    });
  }
  else {
    request.continue();
  }
});
```

### 2. 模拟移动设备
```typescript
const iPhone = puppeteer.devices['iPhone 12'];

await page.emulate(iPhone);
await page.goto('https://example.com');
```

### 3. 处理弹窗
```typescript
// 处理 alert/confirm/prompt
page.on('dialog', async dialog => {
  console.log(dialog.message());
  await dialog.accept();  // 或 dialog.dismiss()
});

// 处理新窗口
const newPagePromise = new Promise(resolve =>
  browser.once('targetcreated', target => resolve(target.page()))
);

await page.click('a[target="_blank"]');
const newPage = await newPagePromise;
```

### 4. Cookie 管理
```typescript
// 设置 Cookie
await page.setCookie({
  name: 'session',
  value: 'abc123',
  domain: 'example.com'
});

// 获取 Cookie
const cookies = await page.cookies();

// 删除 Cookie
await page.deleteCookie({ name: 'session' });
```

### 5. 执行 JavaScript
```typescript
// 在页面上下文中执行代码
const result = await page.evaluate(() => {
  return document.title;
});

// 传递参数
const sum = await page.evaluate((a, b) => {
  return a + b;
}, 5, 3);

// 暴露函数给页面
await page.exposeFunction('md5', (text: string) => {
  return crypto.createHash('md5').update(text).digest('hex');
});
```

## E2E 测试示例

### Playwright 测试
```typescript
import { test, expect } from '@playwright/test';

test.describe('登录功能', () => {
  test('成功登录', async ({ page }) => {
    await page.goto('https://example.com/login');

    await page.fill('#email', 'user@example.com');
    await page.fill('#password', 'password123');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL('https://example.com/dashboard');
    await expect(page.locator('h1')).toContainText('欢迎');
  });

  test('登录失败提示', async ({ page }) => {
    await page.goto('https://example.com/login');

    await page.fill('#email', 'wrong@example.com');
    await page.fill('#password', 'wrongpass');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error')).toBeVisible();
    await expect(page.locator('.error')).toContainText('用户名或密码错误');
  });
});
```

### Cypress 测试
```typescript
describe('购物车功能', () => {
  beforeEach(() => {
    cy.visit('/products');
  });

  it('添加商品到购物车', () => {
    cy.get('.product-item').first().within(() => {
      cy.get('.add-to-cart').click();
    });

    cy.get('.cart-badge').should('contain', '1');
  });

  it('从购物车删除商品', () => {
    cy.get('.cart-icon').click();
    cy.get('.cart-item').first().within(() => {
      cy.get('.remove-button').click();
    });

    cy.get('.cart-empty').should('be.visible');
  });
});
```

## 反检测技术

### Puppeteer Stealth
```typescript
import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';

puppeteer.use(StealthPlugin());

const browser = await puppeteer.launch({
  headless: true,
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-blink-features=AutomationControlled'
  ]
});

const page = await browser.newPage();

// 设置真实的 User-Agent
await page.setUserAgent(
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
);

// 设置视口大小
await page.setViewport({
  width: 1920,
  height: 1080
});

// 隐藏 webdriver 标识
await page.evaluateOnNewDocument(() => {
  Object.defineProperty(navigator, 'webdriver', {
    get: () => false
  });
});
```

## 最佳实践

### 1. 错误处理
```typescript
async function robustScrape(url: string) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  try {
    await page.goto(url, {
      waitUntil: 'networkidle2',
      timeout: 30000
    });

    const data = await page.evaluate(() => {
      // 数据提取逻辑
    });

    return data;
  } catch (error) {
    console.error('抓取失败:', error);
    // 截图保存错误现场
    await page.screenshot({ path: 'error.png' });
    throw error;
  } finally {
    await browser.close();
  }
}
```

### 2. 并发控制
```typescript
import pLimit from 'p-limit';

async function scrapeMultiplePages(urls: string[]) {
  const browser = await puppeteer.launch();
  const limit = pLimit(5);  // 最多 5 个并发

  const results = await Promise.all(
    urls.map(url =>
      limit(async () => {
        const page = await browser.newPage();
        try {
          await page.goto(url);
          return await page.evaluate(() => {
            // 提取数据
          });
        } finally {
          await page.close();
        }
      })
    )
  );

  await browser.close();
  return results;
}
```

### 3. 资源优化
```typescript
// 禁用不必要的资源
await page.setRequestInterception(true);
page.on('request', request => {
  const resourceType = request.resourceType();
  if (['image', 'stylesheet', 'font'].includes(resourceType)) {
    request.abort();
  } else {
    request.continue();
  }
});

// 设置超时
page.setDefaultTimeout(10000);
page.setDefaultNavigationTimeout(30000);
```

## 注意事项
- 遵守网站的 robots.txt 和服务条款
- 控制请求频率,避免对服务器造成压力
- 使用代理池避免 IP 被封
- 妥善处理验证码和登录
- 定期更新浏览器版本
- 注意内存泄漏,及时关闭页面和浏览器
- 使用无头模式提高性能
- 保存日志和错误截图便于调试
