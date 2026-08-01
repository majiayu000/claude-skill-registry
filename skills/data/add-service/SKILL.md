---
name: add-service
description: '새 API 서비스를 생성합니다. service + hook + type 세트를 함께 생성합니다. 사용법: /add-service
  EntityName'
---

---
name: add-service
description: 새 API 서비스를 생성합니다. service + hook + type 세트를 함께 생성합니다. 사용법: /add-service EntityName
---

# Add Service

새 API 도메인 추가 시 서비스, 훅, 타입을 한 번에 생성합니다.

## Instructions

1. 사용자로부터 엔티티 이름(PascalCase)을 받습니다
2. 다음 3개 파일을 생성합니다:
   - `src/types/{entityName}.ts`
   - `src/services/{entityName}Service.ts`
   - `src/hooks/use{EntityName}s.ts`
3. API_SPEC.md와 엔드포인트가 일치하는지 확인합니다

## Type Template

```typescript
// src/types/{entityName}.ts
export interface ${EntityName} {
  id: string;
  projectId: string;
  // TODO: Add entity-specific fields
  createdAt: string;
  updatedAt: string;
}

export interface Create${EntityName}Input {
  projectId: string;
}

export interface Update${EntityName}Input {
  // TODO: Add updatable fields
}
```

## Service Template

```typescript
// src/services/${entityName}Service.ts
import api from "@/api/client";
import type { ApiResponse } from "@/types/api";
import type { ${EntityName}, Create${EntityName}Input, Update${EntityName}Input } from "@/types/${entityName}";

const BASE_URL = "/api";

export const ${entityName}Service = {
  getAll: async (projectId: string): Promise<ApiResponse<${EntityName}[]>> => {
    const response = await api.get(`${BASE_URL}/projects/${projectId}/${entityName}s`);
    return response.data;
  },

  getById: async (id: string): Promise<ApiResponse<${EntityName}>> => {
    const response = await api.get(`${BASE_URL}/${entityName}s/${id}`);
    return response.data;
  },

  create: async (payload: Create${EntityName}Input): Promise<ApiResponse<${EntityName}>> => {
    const response = await api.post(
      `${BASE_URL}/projects/${payload.projectId}/${entityName}s`,
      payload
    );
    return response.data;
  },

  update: async (id: string, payload: Update${EntityName}Input): Promise<ApiResponse<${EntityName}>> => {
    const response = await api.patch(`${BASE_URL}/${entityName}s/${id}`, payload);
    return response.data;
  },

  delete: async (id: string): Promise<ApiResponse<void>> => {
    const response = await api.delete(`${BASE_URL}/${entityName}s/${id}`);
    return response.data;
  },
};
```

## Hook

add-hook Skill을 사용하여 훅을 생성합니다.

## Checklist

- 타입 파일에 필수 필드 정의
- API_SPEC.md와 엔드포인트 일치 확인
- barrel export 추가

## Examples

```
/add-service Bookmark
```

→ 3개 파일 생성:

- `src/types/bookmark.ts`
- `src/services/bookmarkService.ts`
- `src/hooks/useBookmarks.ts`
