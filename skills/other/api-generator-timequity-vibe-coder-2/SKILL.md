---
name: api-generator
description: |
  Generate CRUD API endpoints automatically. User doesn't see routes.
  Use when: features need backend logic.
  Triggers: internal use only.
---

# API Generator

Create endpoints from requirements. User never writes routes.

## Process

1. **Identify resources**
   - "Manage expenses" → /api/expenses
   - "User profile" → /api/users/me

2. **Generate CRUD**
   - GET (list, single)
   - POST (create)
   - PUT/PATCH (update)
   - DELETE (remove)

3. **Add validation**
   - Input schemas
   - Error handling
   - Auth middleware

4. **Generate OpenAPI**
   - Auto-document all endpoints
   - For future integrations

## Template-Specific

### Next.js API Routes
```typescript
// app/api/expenses/route.ts
export async function GET() {
  const expenses = await db.expenses.findMany();
  return Response.json(expenses);
}

export async function POST(req: Request) {
  const data = await req.json();
  const expense = await db.expenses.create({ data });
  return Response.json(expense);
}
```

### FastAPI
```python
@router.get("/expenses")
async def list_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()

@router.post("/expenses")
async def create_expense(data: ExpenseCreate, db: Session = Depends(get_db)):
    expense = Expense(**data.dict())
    db.add(expense)
    db.commit()
    return expense
```

### Hono
```typescript
app.get('/expenses', async (c) => {
  const expenses = await db.select().from(expensesTable);
  return c.json(expenses);
});

app.post('/expenses', async (c) => {
  const data = await c.req.json();
  const [expense] = await db.insert(expensesTable).values(data).returning();
  return c.json(expense);
});
```

## Auto-Generated Features

| Feature | Implementation |
|---------|----------------|
| Pagination | ?page=1&limit=20 |
| Filtering | ?category=food |
| Sorting | ?sort=amount&order=desc |
| Auth | Middleware checks token |
| Validation | Schema validates input |

## User Experience

User: "Add expense tracking"

Internally:
1. Generate /api/expenses endpoints
2. Add validation schemas
3. Connect to database
4. Add auth middleware
5. Generate OpenAPI spec

User sees: "✅ Expense API ready"
