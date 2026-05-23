---
name: admin-documents
description: Document management, LLM pipeline, anonymization, Q&A generation, versioning
---

# Admin Documents Module — CEI-001

## Document Pipeline Architecture

```python
# app/services/document_pipeline.py
from typing import List, Dict, Any, AsyncGenerator
from openai import AsyncOpenAI
import tiktoken

class DocumentPipelineService:
    def __init__(self, openai_key: str):
        self.client = AsyncOpenAI(api_key=openai_key)
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")
    
    async def process_document(
        self,
        content: str,
        config: PipelineConfig
    ) -> Dict[str, Any]:
        """Run full pipeline on document"""
        
        result = {
            "original": content,
            "augmented": content,
            "qa_pairs": [],
            "chunks": [],
            "stats": {}
        }
        
        # 1. Anonymization
        if "anonymize" in config.transformations:
            result["augmented"] = await self._anonymize(result["augmented"])
        
        # 2. Whitelabel (remove specific references)
        if "whitelabel" in config.transformations:
            result["augmented"] = await self._whitelabel(result["augmented"])
        
        # 3. Normalize (tone, terminology)
        if "normalize" in config.transformations:
            result["augmented"] = await self._normalize(result["augmented"])
        
        # 4. Enrich summary
        if "enrich_summary" in config.transformations:
            summary = await self._generate_summary(result["augmented"])
            result["augmented"] = f"SUMMARY:\n{summary}\n\n{result['augmented']}"
        
        # 5. Generate Q&A
        if "enrich_qa" in config.transformations:
            result["qa_pairs"] = await self._generate_qa(result["augmented"])
        
        # 6. Chunk for RAG
        if "segment" in config.transformations:
            result["chunks"] = self._chunk_text(
                result["augmented"],
                chunk_size=config.chunk_size,
                overlap=config.chunk_overlap
            )
        
        return result
    
    async def _anonymize(self, content: str) -> str:
        """Remove PII and client-specific data"""
        prompt = """Anonymize this document:
- Replace company names with "Company X", "Company Y"
- Replace person names with "Manager", "User", etc.
- Keep structure and meaning
- Return only anonymized text

Content:
{content}"""
        
        response = await self.client.messages.create(
            model="gpt-4-turbo-preview",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt.format(content=content)}]
        )
        return response.content[0].text
    
    async def _whitelabel(self, content: str) -> str:
        """Neutralize client/tool-specific references"""
        prompt = """Neutralize this document for white-label use:
- "Our client X" → "manufacturing companies"
- "Genius ERP" → "ERP systems"
- "Our methodology" → "industry best practices"
- Keep exact same information, just generalized

Content:
{content}"""
        
        response = await self.client.messages.create(
            model="gpt-4-turbo-preview",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt.format(content=content)}]
        )
        return response.content[0].text
    
    async def _normalize(self, content: str) -> str:
        """Normalize tone, terminology, structure"""
        prompt = """Normalize this document for consistent style:
- Standardize terminology (use "ERP" not "ERP systems", "system")
- Consistent tone (professional, accessible)
- Fix grammar and clarity
- Maintain all information

Content:
{content}"""
        
        response = await self.client.messages.create(
            model="gpt-4-turbo-preview",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt.format(content=content)}]
        )
        return response.content[0].text
    
    async def _generate_summary(self, content: str) -> str:
        """Generate executive summary"""
        prompt = f"""Generate a 2-3 sentence executive summary:

{content}"""
        
        response = await self.client.messages.create(
            model="gpt-4-turbo-preview",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    async def _generate_qa(self, content: str, pairs_per_section: int = 3) -> List[Dict]:
        """Generate Q&A pairs for better RAG"""
        prompt = f"""Generate {pairs_per_section} Q&A pairs from this content:

{content}

Format as JSON:
[
  {{"question": "?", "answer": "?"}},
  ...
]"""
        
        response = await self.client.messages.create(
            model="gpt-4-turbo-preview",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            import json
            return json.loads(response.content[0].text)
        except:
            return []
    
    def _chunk_text(self, content: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
        """Chunk text smartly"""
        chunks = []
        paragraphs = content.split('\n\n')
        
        current_chunk = ""
        for para in paragraphs:
            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
```

## Admin API Routes

```python
# app/api/routes/admin_documents.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_admin_user
from app.schemas.admin_document import PipelineConfig, DocumentResponse
from app.services.document_pipeline import DocumentPipelineService

router = APIRouter(prefix="/api/admin/documents", tags=["admin"])

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    admin = Depends(get_admin_user)
) -> DocumentResponse:
    """Upload document (admin only)"""
    
    # Save file
    content = await file.read()
    
    # Create document record
    document = Document(
        title=file.filename,
        source_filename=file.filename,
        source_mimetype=file.content_type,
        status="draft",
        created_by=admin.id
    )
    db.add(document)
    await db.commit()
    
    return DocumentResponse.from_orm(document)

@router.post("/{doc_id}/pipeline")
async def start_pipeline(
    doc_id: str,
    config: PipelineConfig,
    db: AsyncSession = Depends(get_db),
    admin = Depends(get_admin_user)
):
    """Start LLM pipeline (admin only)"""
    
    # Get document
    document = await db.get(Document, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Mark processing
    document.status = "processing"
    await db.commit()
    
    # Run pipeline
    service = DocumentPipelineService(settings.OPENAI_API_KEY)
    result = await service.process_document(content, config)
    
    # Save version
    version = DocumentVersion(
        document_id=doc_id,
        version_number=document.current_version + 1,
        original_content=content,
        augmented_content=result["augmented"],
        generated_qa=result["qa_pairs"],
        pipeline_config=config.dict()
    )
    db.add(version)
    
    # Update document
    document.current_version += 1
    document.status = "review"
    
    await db.commit()
    
    return {"status": "completed", "version": version.version_number}

@router.post("/{doc_id}/publish")
async def publish_document(
    doc_id: str,
    db: AsyncSession = Depends(get_db),
    admin = Depends(get_admin_user)
):
    """Publish to Weaviate (admin only)"""
    
    document = await db.get(Document, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Get current version
    version = await db.get(DocumentVersion, {"document_id": doc_id, "version_number": document.current_version})
    
    # Index chunks
    rag_service = RAGService(settings.WEAVIATE_HOST)
    chunk_uuids = await rag_service.index_document(
        doc_id,
        version.augmented_content
    )
    
    # Update document
    document.status = "published"
    document.published_at = datetime.utcnow()
    
    await db.commit()
    
    return {"status": "published", "chunks_indexed": len(chunk_uuids)}
```

---

---
name: typescript-patterns
description: TypeScript type safety, enums, generics, custom hooks, form validation
---

# TypeScript Patterns — CEI-001

## Type Safety Strictness

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "noImplicitThis": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

## Enums for Constants

```typescript
// types/evaluation.ts
export enum ModuleType {
  VISION = 'vision',
  ORGANIZATION = 'organization',
  DATA = 'data',
  INFRASTRUCTURE = 'infrastructure',
  RESOURCES = 'resources',
  PITFALLS = 'pitfalls',
  IMPLEMENTATION = 'implementation',
  POST = 'post'
}

export enum QuestionType {
  YESNO = 'yesno',
  SCALE = 'scale',
  MULTIPLE = 'multiple'
}

export enum EvaluationStatus {
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  DRAFT = 'draft'
}
```

## Discriminated Unions

```typescript
// types/api.ts
type ApiResponse<T> =
  | { type: 'success'; data: T }
  | { type: 'error'; error: { code: string; message: string } }
  | { type: 'loading' };

// Type-safe usage
function handleResponse<T>(response: ApiResponse<T>) {
  if (response.type === 'success') {
    console.log(response.data); // T is available
  } else if (response.type === 'error') {
    console.log(response.error.code); // error is available
  }
}
```

## Generics

```typescript
// API client with generics
interface ApiClient {
  get<T>(url: string): Promise<T>;
  post<T, D>(url: string, data: D): Promise<T>;
  put<T, D>(url: string, id: string, data: D): Promise<T>;
}

// Usage
const users = await api.get<User[]>('/api/users');
const created = await api.post<User, CreateUserData>('/api/users', userData);
```

## Custom Hooks with Types

```typescript
// hooks/usePagination.ts
interface UsePaginationOptions {
  pageSize: number;
  initialPage?: number;
}

interface UsePaginationState {
  page: number;
  total: number;
  pageSize: number;
}

export function usePagination({
  pageSize,
  initialPage = 1
}: UsePaginationOptions) {
  const [state, setState] = useState<UsePaginationState>({
    page: initialPage,
    total: 0,
    pageSize
  });

  const nextPage = () => setState(prev => ({
    ...prev,
    page: Math.min(prev.page + 1, Math.ceil(prev.total / pageSize))
  }));

  const previousPage = () => setState(prev => ({
    ...prev,
    page: Math.max(prev.page - 1, 1)
  }));

  return { ...state, nextPage, previousPage };
}
```

## Form Validation with Zod

```typescript
// validation/evaluation.ts
import { z } from 'zod';

export const answerSchema = z.object({
  questionId: z.string().uuid(),
  answer: z.enum(['oui', 'non', 'partiellement']),
  comment: z.string().optional()
});

export type Answer = z.infer<typeof answerSchema>;

export const evaluationSchema = z.object({
  companyId: z.string().min(1),
  answers: z.array(answerSchema)
});

export type EvaluationData = z.infer<typeof evaluationSchema>;

// Usage with React Hook Form
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

export function AnswerForm() {
  const { control, handleSubmit } = useForm<Answer>({
    resolver: zodResolver(answerSchema)
  });
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

## Utility Types

```typescript
// Type helpers
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};

type Partial<T> = {
  [P in keyof T]?: T[P];
};

type Record<K extends string | number | symbol, T> = {
  [P in K]: T;
};

// Usage
type UserResponse = Readonly<User>;
type UserUpdate = Partial<User>;
type UserMap = Record<string, User>;
```

## Async Types

```typescript
type ApiResult<T> = Promise<T | null>;

async function fetchUser(id: string): ApiResult<User> {
  try {
    const response = await api.get<User>(`/api/users/${id}`);
    return response;
  } catch (error) {
    console.error(error);
    return null;
  }
}
```

## Conventions

- Interfaces for public APIs, types for internal
- Enums for constants instead of `as const`
- Generics for reusable logic
- Discriminated unions for variants
- Zod for runtime validation
- Strict mode always enabled
- No `any` type allowed
- Export types from `types/` folder
