---
name: api-rayanalanzi88886-dev-mlham999
description: إرشادات لبناء واجهات برمجة تطبيقات (REST APIs) قوية، آمنة، وسهلة الاستخدام.
---

# API Development Skill

## نظرة عامة
إرشادات لبناء واجهات برمجة تطبيقات (REST APIs) قوية، آمنة، وسهلة الاستخدام.

---

## تصميم RESTful API

### تسمية الموارد (Resource Naming)
- استخدم الأسماء (Nouns) وليس الأفعال (Verbs).
- استخدم الجمع للمجموعات.

```
GET /users          // جلب قائمة المستخدمين
GET /users/123      // جلب مستخدم محدد
POST /users         // إنشاء مستخدم جديد
PUT /users/123      // تحديث مستخدم بالكامل
PATCH /users/123    // تحديث جزئي لمستخدم
DELETE /users/123   // حذف مستخدم
```

### رموز الحالة (Status Codes)
استخدم رموز HTTP القياسية:
- `200 OK`: نجاح الطلب.
- `201 Created`: تم إنشاء المورد بنجاح.
- `400 Bad Request`: خطأ في المدخلات.
- `401 Unauthorized`: غير مسجل الدخول.
- `403 Forbidden`: لا تملك صلاحية.
- `404 Not Found`: المورد غير موجود.
- `500 Internal Server Error`: خطأ في الخادم.

---

## المصادقة والتفويض (Authentication & Authorization)

### JWT (JSON Web Tokens)
استخدم JWT للمصادقة في التطبيقات الحديثة.

```typescript
// Middleware للتحقق من التوكن
const authenticate = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ message: 'No token provided' });

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    res.status(401).json({ message: 'Invalid token' });
  }
};
```

---

## التحقق من المدخلات (Validation)

لا تثق أبداً بمدخلات المستخدم. استخدم مكتبات مثل `Zod` أو `Joi`.

```typescript
import { z } from 'zod';

const createUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(2)
});

app.post('/users', (req, res) => {
  const result = createUserSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json(result.error);
  }
  // ... إنشاء المستخدم
});
```

---

## معالجة الأخطاء (Error Handling)

استخدم middleware مركزي لمعالجة الأخطاء.

```typescript
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    message: 'Something went wrong!',
    error: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});
```

---

## التوثيق (Documentation)

وثّق الـ API باستخدام Swagger/OpenAPI.

```yaml
/users:
  get:
    summary: Returns a list of users.
    responses:
      200:
        description: A JSON array of user names
```

---

## تحديد المعدل (Rate Limiting)

احمِ الـ API من الهجمات والاستخدام المفرط.

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.use(limiter);
```
