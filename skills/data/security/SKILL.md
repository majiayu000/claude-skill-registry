# Security Skill

## نظرة عامة
دليل شامل لتأمين تطبيقات الويب وحمايتها من الثغرات الشائعة.

---

## قائمة التحقق الأمنية (Security Checklist)

- [ ] **HTTPS**: استخدم HTTPS دائماً.
- [ ] **Headers**: قم بتعيين ترويسات الأمان (Security Headers).
- [ ] **Validation**: تحقق من جميع المدخلات.
- [ ] **Authentication**: استخدم آليات مصادقة قوية.
- [ ] **Dependencies**: حدث المكتبات بانتظام.

---

## ترويسات الأمان (Secure Headers)

استخدم مكتبة مثل `helmet` في Express لتعيين الترويسات تلقائياً.

```typescript
import helmet from 'helmet';
app.use(helmet());
```

هذا يضيف ترويسات مثل:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Strict-Transport-Security`

---

## حماية البيانات (Data Protection)

### تخزين كلمات المرور
لا تخزن كلمات المرور كنص عادي أبداً. استخدم `bcrypt` أو `argon2`.

```typescript
import bcrypt from 'bcrypt';

const saltRounds = 10;
const hash = await bcrypt.hash(password, saltRounds);

// للتحقق
const match = await bcrypt.compare(password, hash);
```

### منع حقن SQL (SQL Injection)
استخدم ORM (مثل Prisma, TypeORM) أو Parameterized Queries دائماً.

```typescript
// سيء
const query = `SELECT * FROM users WHERE id = ${id}`;

// جيد (Parameterized)
const query = 'SELECT * FROM users WHERE id = $1';
const values = [id];
```

---

## حماية XSS (Cross-Site Scripting)

- قم بتعقيم (Sanitize) المدخلات التي يتم عرضها للمستخدم.
- React يقوم بذلك تلقائياً، لكن احذر من `dangerouslySetInnerHTML`.
- استخدم `Content-Security-Policy (CSP)`.

---

## حماية CSRF (Cross-Site Request Forgery)

- استخدم `SameSite` cookies.
- استخدم CSRF Tokens للعمليات الحساسة إذا كنت تستخدم Cookies للمصادقة.

```typescript
// إعداد الكوكيز الآمنة
res.cookie('token', token, {
  httpOnly: true,
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'strict'
});
```

---

## أمان رفع الملفات (File Upload Security)

- تحقق من نوع الملف (MIME type) وامتداده.
- لا تستخدم اسم الملف الأصلي عند الحفظ.
- حدد حجم الملف المسموح به.
- افحص الملفات بحثاً عن فيروسات إذا أمكن.

```typescript
const upload = multer({
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
  fileFilter: (req, file, cb) => {
    if (file.mimetype !== 'image/png' && file.mimetype !== 'image/jpeg') {
      return cb(new Error('Only images are allowed'));
    }
    cb(null, true);
  }
});
```
