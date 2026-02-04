# TypeScript Development Skill

## نظرة عامة
أفضل الممارسات لكتابة كود TypeScript قوي، آمن، وقابل للصيانة.

---

## الأساسيات (Basics)

### تعريف الأنواع (Type Definitions)

```typescript
// استخدام Interface للكائنات
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
  isActive: boolean;
  createdAt: Date;
}

// استخدام Type للاتحادات (Unions) والتقاطعات (Intersections)
type Status = 'pending' | 'approved' | 'rejected';
type UserResponse = User & { status: Status };
```

### النمط الصارم (Strict Mode)
تأكد من تفعيل `strict: true` في `tsconfig.json` لضمان أقصى درجات الأمان.

---

## الواجهات والأنواع المتقدمة (Advanced Interfaces & Types)

### Generics

استخدم Generics لإنشاء مكونات ودوال قابلة لإعادة الاستخدام مع الحفاظ على سلامة الأنواع.

```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

async function fetchData<T>(url: string): Promise<ApiResponse<T>> {
  const response = await fetch(url);
  return response.json();
}

// الاستخدام
const user = await fetchData<User>('/api/user');
```

### Utility Types

استخدم Utility Types المدمجة لتقليل التكرار:

- `Partial<T>`: جعل كل الخصائص اختيارية.
- `Pick<T, K>`: اختيار مجموعة محددة من الخصائص.
- `Omit<T, K>`: استبعاد مجموعة محددة من الخصائص.
- `Readonly<T>`: جعل الكائن للقراءة فقط.

```typescript
type UpdateUserDto = Partial<Omit<User, 'id' | 'createdAt'>>;
```

---

## حراس النوع (Type Guards)

استخدم Type Guards للتحقق من النوع في وقت التشغيل.

```typescript
function isAdmin(user: User): user is User & { role: 'admin' } {
  return user.role === 'admin';
}

if (isAdmin(currentUser)) {
  // TypeScript يعرف الآن أن currentUser هو admin
  console.log('Admin Access Granted');
}
```

---

## أفضل الممارسات (Best Practices)

1.  **تجنب `any`**: استخدم `unknown` إذا كنت لا تعرف النوع، ثم قم بالتحقق منه.
2.  **استخدم `const`**: للمتغيرات التي لا تتغير قيمتها.
3.  **Async/Await**: استخدم `async/await` بدلاً من `then/catch` لقراءة أفضل.
4.  **Explicit Return Types**: حدد نوع الإرجاع للدوال المهمة لتوثيق الكود ومنع الأخطاء العرضية.

```typescript
// سيء
function getData(id) {
  return db.find(id);
}

// جيد
async function getData(id: string): Promise<User | null> {
  return await db.find(id);
}
```

---

## اختبار الأنواع (Testing Types)

تأكد من أن الأنواع تعمل كما هو متوقع، خاصة عند استخدام مكتبات خارجية أو أنواع معقدة.

```typescript
import { expectType } from 'tsd';

expectType<string>(someFunction());
```
