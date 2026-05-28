---
name: type-checker
description: 執行 TypeScript 類型檢查並修復類型錯誤。當遇到類型錯誤、需要類型定義、或用戶提到「type」、「類型」時使用。
allowed-tools: Read, Grep, Bash, Edit
---

# TypeScript Type Checker Skill

專門處理 TypeScript 類型檢查和類型錯誤修復。

## 🎯 執行時機

- 用戶提到「類型錯誤」、「type error」
- 執行 `npm run typecheck` 發現錯誤
- 需要定義或修復 TypeScript 類型
- 代碼中出現 `any` 需要替換為具體類型

## 📋 執行流程

### 1. 執行類型檢查

```bash
npm run typecheck
```

### 2. 分析錯誤輸出

TypeScript 錯誤格式：

```
src/components/Login.tsx:42:15 - error TS7006: Parameter 'user' implicitly has an 'any' type.
```

需要提取：

- 檔案路徑: `src/components/Login.tsx`
- 行號: `42`
- 錯誤碼: `TS7006`
- 錯誤訊息: `Parameter 'user' implicitly has an 'any' type`

### 3. 閱讀相關檔案

**必須閱讀的檔案（按順序）：**

1. **錯誤所在檔案** - 理解上下文
2. **相關類型定義檔案** - 檢查是否已有類型定義
   ```bash
   # 搜尋類型定義檔案
   Glob: pattern="**/types/**/*.ts"
   Glob: pattern="**/*.d.ts"
   ```
3. **相關的 interface/type** - 尋找可重用的類型
   ```bash
   # 在檔案中搜尋 interface 定義
   Grep: pattern="^(export\\s+)?(interface|type)\\s+" output_mode="content"
   ```

### 4. 修復策略

#### 策略 A: 使用現有類型

```typescript
// ❌ 錯誤
function handleUser(user: any) {}

// ✅ 使用專案中已定義的類型
import { User } from "@/types/user";
function handleUser(user: User) {}
```

#### 策略 B: 定義新類型

如果專案中沒有合適的類型，在適當位置定義：

```typescript
// 在 src/types/[domain].ts 中定義
export interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: "admin" | "user" | "guest";
}
```

#### 策略 C: 使用泛型

```typescript
// ❌ 錯誤
function fetchData(url: string): Promise<any> {}

// ✅ 使用泛型
function fetchData<T>(url: string): Promise<T> {}
```

### 5. 常見類型錯誤修復

#### TS7006: 隱式 any 參數

```typescript
// ❌ 錯誤
const handleClick = (e) => {};

// ✅ 修復
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {};
```

#### TS2339: 屬性不存在

```typescript
// ❌ 錯誤
interface User {
  name: string;
}
user.email; // Property 'email' does not exist

// ✅ 修復：擴展 interface
interface User {
  name: string;
  email: string;
}
```

#### TS2345: 參數類型不匹配

```typescript
// ❌ 錯誤
function greet(name: string) {}
greet(123);

// ✅ 修復：確保參數類型正確
greet(String(123));
// 或
greet(userId.toString());
```

#### TS18046: 可能為 undefined

```typescript
// ❌ 錯誤
const user = users.find((u) => u.id === id);
console.log(user.name); // 'user' is possibly 'undefined'

// ✅ 修復：加入 null check
const user = users.find((u) => u.id === id);
if (user) {
  console.log(user.name);
}
// 或使用可選鏈
console.log(user?.name);
```

### 6. React 特定類型

```typescript
// Props 類型
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

// Event handlers
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {};
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {};
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {};

// State 類型
const [user, setUser] = useState<User | null>(null);
const [items, setItems] = useState<Item[]>([]);

// Ref 類型
const inputRef = useRef<HTMLInputElement>(null);
```

## 📋 修復流程

1. **Read 錯誤檔案**
2. **Grep 搜尋相關類型定義**
3. **決定修復策略**（使用現有/定義新/使用泛型）
4. **Edit 修復類型錯誤**
5. **Bash 執行 `npm run typecheck` 驗證**
6. **重複直到所有錯誤修復**

## 🚨 絕對禁止

```typescript
// ❌ 永遠不要這樣做
const data: any = fetchData();
function process(input: any): any {}
// @ts-ignore
const result = riskyOperation();
```

## ✅ 最佳實踐

1. **優先使用現有類型** - 檢查 `src/types/` 目錄
2. **類型定義集中管理** - 放在 `src/types/[domain].ts`
3. **使用嚴格模式** - 確保 tsconfig.json 開啟 strict
4. **Export 可重用類型** - 方便其他檔案使用
5. **使用 Type Guards** - 提供 runtime 類型安全

## 📝 回報格式

````markdown
## TypeScript 類型修復報告

### 修復的錯誤

1. **src/components/Login.tsx:42**
   - 錯誤: TS7006 - Parameter 'user' implicitly has an 'any' type
   - 修復: 使用 `User` interface from `@/types/user`
   - 狀態: ✅ 已修復

2. **src/api/auth.ts:15**
   - 錯誤: TS2345 - Argument type mismatch
   - 修復: 調整參數類型為 `LoginCredentials`
   - 狀態: ✅ 已修復

### 驗證結果

```bash
npm run typecheck
```
````

✅ 無類型錯誤

### 新增的類型定義

- `src/types/auth.ts` - LoginCredentials, AuthResponse

```

## 🔗 參考資源

- TypeScript 官方文檔: https://www.typescriptlang.org/docs/
- React TypeScript Cheatsheet: https://react-typescript-cheatsheet.netlify.app/
- 專案規範: `/home/user/maihouses/CLAUDE.md`
```
