# Skill: Build Error Handler

**Purpose**: Automatically diagnose and resolve common build errors for Next.js frontend and FastAPI backend.

## Trigger Conditions

Invoke this skill when:
- `npm run build` or `next build` fails
- `pip install` or Python dependency issues occur
- TypeScript compilation errors appear
- User mentions "build failing" or "deployment error"

## Capabilities

### 1. Next.js Build Errors

#### Error: "Module not found"

**Cause**: Missing dependency or wrong import path.

**Solution**:
```bash
# Check if package is installed
npm ls <package-name>

# If missing, install it
npm install <package-name>

# For type definitions
npm install -D @types/<package-name>
```

#### Error: "Type 'X' is not assignable to type 'Y'"

**Cause**: TypeScript type mismatch.

**Solution**:
```typescript
// Option 1: Fix the type
const value: CorrectType = ...

// Option 2: Use type assertion (only if confident)
const value = something as ExpectedType

// Option 3: Add proper type annotation
interface Props {
  data: TaskType[];  // Be specific
}
```

#### Error: "Cannot find module 'X' or its corresponding type declarations"

**Solution**:
```bash
# Install type definitions
npm install -D @types/<module-name>

# Or create declaration file: types/<module>.d.ts
declare module '<module-name>' {
  const content: any;
  export default content;
}
```

#### Error: "Dynamic server usage" in App Router

**Cause**: Using dynamic features in static export.

**Solution**:
```typescript
// Add to page/layout that needs dynamic rendering
export const dynamic = 'force-dynamic'

// Or for specific route segments
export const revalidate = 0
```

### 2. FastAPI/Python Build Errors

#### Error: "No module named 'X'"

**Cause**: Missing Python package.

**Solution**:
```bash
# Check if installed
pip show <package-name>

# Install if missing
pip install <package-name>

# Update requirements.txt
pip freeze > requirements.txt
```

#### Error: "ImportError: cannot import name 'X'"

**Cause**: Circular import or wrong import path.

**Solution**:
```python
# Option 1: Use TYPE_CHECKING for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .models import Task

# Option 2: Import inside function
def get_task():
    from .models import Task
    return Task
```

#### Error: "pydantic_core._pydantic_core.ValidationError"

**Cause**: Invalid data passed to Pydantic model.

**Solution**:
```python
# Check field types match expected
class TaskCreate(BaseModel):
    title: str  # Ensure string, not None
    description: Optional[str] = None  # Mark optional fields

# Add validators for complex cases
@field_validator('title')
def validate_title(cls, v):
    if not v or not v.strip():
        raise ValueError('Title cannot be empty')
    return v.strip()
```

### 3. Common Deployment Errors

#### Error: "ENOENT: no such file or directory"

**Cause**: Missing file during build.

**Solution**:
```bash
# Ensure all files are committed
git status
git add .

# Check .gitignore isn't excluding needed files
cat .gitignore
```

#### Error: "Cannot read properties of undefined"

**Cause**: Environment variable not set.

**Solution**:
```typescript
// Always provide fallback or check existence
const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// For required vars, fail fast
if (!process.env.DATABASE_URL) {
  throw new Error('DATABASE_URL is required')
}
```

### 4. Quick Fix Scripts

Create `scripts/fix-build.sh`:

```bash
#!/bin/bash
echo "Fixing common build issues..."

# Frontend fixes
cd frontend

# Clear cache
rm -rf .next node_modules/.cache

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Type check
npx tsc --noEmit

# Try build
npm run build

cd ..

# Backend fixes
cd backend

# Recreate venv
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt

# Check for import errors
python -c "from app.main import app; print('Backend OK')"

echo "Build fix complete!"
```

## Error Decision Tree

```
Build Error
├── Frontend (Next.js)
│   ├── Module not found → npm install
│   ├── Type error → Fix TypeScript types
│   ├── Dynamic server → Add 'force-dynamic'
│   └── Env missing → Check .env.local
│
└── Backend (FastAPI)
    ├── Import error → Check circular imports
    ├── Validation error → Fix Pydantic model
    ├── Module missing → pip install
    └── DB error → Check DATABASE_URL
```

## Checklist

- [ ] Check error message for specific module/file mentioned
- [ ] Verify all dependencies are installed
- [ ] Check environment variables are set
- [ ] Clear caches (`.next/`, `__pycache__/`, `node_modules/.cache/`)
- [ ] Verify TypeScript/Python types match
- [ ] Test locally before deployment
