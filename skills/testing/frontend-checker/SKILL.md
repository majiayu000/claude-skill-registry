---
name: "frontend-checker"
description: "Kiểm tra sức khỏe frontend tự động using Puppeteer. Invoke khi user muốn tìm broken pages, console errors, hoặc verify frontend stability."
---

# Frontend Health Checker

Skill này tự động hóa việc phát hiện lỗi frontend (Console Errors, Network Failures, Broken Links) sử dụng Puppeteer.

## Khi nào sử dụng

- User muốn kiểm tra frontend health
- Phát hiện console errors/warnings
- Tìm broken links hoặc network failures
- Verify frontend stability sau khi deploy
- Audit các trang trước khi release

## Cách sử dụng

### 1. Chuẩn bị

Đảm bảo `puppeteer` đã được cài đặt:

```bash
cd frontend
npm install puppeteer
```

Đảm bảo frontend server đang chạy:
- Development: `http://localhost:3000`
- Production: `http://aicmr.local` hoặc domain khác

### 2. Thực thi check

Tạo Node.js script sử dụng Puppeteer để:

1. **Login** (nếu cần auth)
2. **Navigate** đến các trang quan trọng
3. **Capture** console errors, warnings, network failures
4. **Report** kết quả chi tiết

### 3. Chạy script

```bash
node _health_check.js
```

## Danh sách check mặc định

### Public Pages (không cần auth)
- `/` - Trang chủ
- `/login` - Đăng nhập
- `/register` - Đăng ký
- `/blog` - Blog

### Protected Pages (cần login)
- `/dashboard` - Dashboard chính
- `/dashboard/stats` - Thống kê
- `/dashboard/posts` - Quản lý bài viết
- `/dashboard/users-manager` - Quản lý users
- `/dashboard/settings` - Cài đặt
- `/user/profile` - Profile user

## Template script cơ bản

```javascript
const puppeteer = require('puppeteer');
const fs = require('fs');

const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';
const RESULTS = [];

async function checkPage(page, url, name, options = {}) {
  const errors = [];
  const warnings = [];
  const networkErrors = [];

  // Console listeners
  page.on('console', msg => {
    const type = msg.type();
    const text = msg.text();

    if (type === 'error') {
      errors.push({ type: 'console', text });
    } else if (type === 'warning') {
      warnings.push({ type: 'console', text });
    }
  });

  // Network listener
  page.on('response', response => {
    const status = response.status();
    if (status >= 400) {
      networkErrors.push({
        url: response.url(),
        status: status,
        text: response.statusText()
      });
    }
  });

  try {
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });

    // Check for broken links
    const links = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('a'))
        .map(a => a.href)
        .filter(href => href && !href.startsWith('javascript:'));
    });

    RESULTS.push({
      page: name,
      url: url,
      status: 'success',
      errors,
      warnings,
      networkErrors,
      linksCount: links.length
    });

  } catch (error) {
    RESULTS.push({
      page: name,
      url: url,
      status: 'failed',
      error: error.message
    });
  }
}

(async () => {
  const browser = await puppeteer.launch({
    headless: "new",
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--ignore-certificate-errors'],
    defaultViewport: { width: 1280, height: 800 }
  });

  const page = await browser.newPage();

  // Check public pages
  const publicPages = [
    ['/', 'Home'],
    ['/login', 'Login'],
    ['/register', 'Register'],
    ['/blog', 'Blog']
  ];

  for (const [path, name] of publicPages) {
    await checkPage(page, `${BASE_URL}${path}`, name);
  }

  // TODO: Add auth flow if needed
  // await page.goto(`${BASE_URL}/login`);
  // await page.type('input[name="email"]', 'test@example.com');
  // await page.type('input[name="password"]', 'password');
  // await page.click('button[type="submit"]');
  // await page.waitForNavigation();

  await browser.close();

  // Generate report
  console.log('\n=== FRONTEND HEALTH CHECK REPORT ===\n');
  console.log(`Total pages checked: ${RESULTS.length}`);

  const failedPages = RESULTS.filter(r => r.status === 'failed');
  const pagesWithErrors = RESULTS.filter(r => r.errors && r.errors.length > 0);
  const pagesWithNetworkErrors = RESULTS.filter(r => r.networkErrors && r.networkErrors.length > 0);

  console.log(`Failed pages: ${failedPages.length}`);
  console.log(`Pages with console errors: ${pagesWithErrors.length}`);
  console.log(`Pages with network errors: ${pagesWithNetworkErrors.length}\n`);

  // Detailed report
  RESULTS.forEach(result => {
    console.log(`\n--- ${result.page} (${result.url}) ---`);
    console.log(`Status: ${result.status}`);

    if (result.errors && result.errors.length > 0) {
      console.log(`Console Errors (${result.errors.length}):`);
      result.errors.forEach(e => console.log(`  - ${e.text}`));
    }

    if (result.networkErrors && result.networkErrors.length > 0) {
      console.log(`Network Errors (${result.networkErrors.length}):`);
      result.networkErrors.forEach(e => console.log(`  - ${e.url} [${e.status}]`));
    }
  });
})();
```

## Báo cáo kết quả

Format báo cáo nên bao gồm:

1. **Tổng quan**
   - Tổng số trang đã check
   - Số trang bị lỗi
   - Số trang có console errors
   - Số trang có network errors

2. **Chi tiết từng trang**
   - Tên trang + URL
   - Status (success/failed)
   - Console errors (nếu có)
   - Network errors (nếu có)
   - Broken links (nếu có)

3. **Đề xuất fix**
   - Gợi ý giải pháp cho các lỗi phổ biến
   - 404 API calls → Kiểm tra endpoint
   - React hydration errors → Kiểm tra server-side rendering
   - Missing assets → Kiểm tra file paths

## Best Practices

1. **Luôn chạy headless mode** cho CI/CD
2. **Set timeout phù hợp** cho mỗi page load
3. **Capture screenshots** khi có lỗi để debug
4. **Save results** ra file JSON để history tracking
5. **Integrate với CI/CD** để auto-check trước khi deploy

## Troubleshooting

### Puppeteer không install được
```bash
# Sử dụng puppeteer-core nếu gặp vấn đề với Chrome
npm install puppeteer-core
# Hoặc cài đặt Chrome riêng
```

### Timeout errors
- Tăng `timeout` trong `page.goto()`
- Kiểm tra network speed
- Disable unnecessary extensions

### Auth không hoạt động
- Kiểm tra selectors cho login form
- Thêm delay sau khi submit form
- Verify token/cookie được set đúng
