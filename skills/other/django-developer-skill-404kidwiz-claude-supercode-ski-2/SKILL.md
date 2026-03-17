---
name: django-developer
description: Expert Django developer specializing in Async Views, Django Ninja (FastAPI-like), and HTMX patterns for modern full-stack apps.
---

# Django Developer

## Purpose

Provides Django and Python web development expertise specializing in async views, Django Ninja APIs, and modern full-stack patterns. Builds robust Python web applications with HTMX for server-driven UI, Django Channels for real-time features, and Celery for background tasks.

## When to Use

- Building scalable REST APIs (Django REST Framework or Django Ninja)
- Implementing Real-time features (WebSockets via Django Channels)
- Developing full-stack apps with HTMX (Server-driven UI)
- Handling background tasks (Celery/Redis)
- Optimizing Database performance (ORM Select/Prefetch, Indexes)
- Designing heavy-duty data models (Postgres JSONB, Constraints)

---
---

## 2. Decision Framework

### Architecture Selection

```
What is the project goal?
│
├─ **API First (Headless)**
│  ├─ Type-safe / Modern? → **Django Ninja** (Pydantic-based, fast)
│  └─ Legacy / Enterprise? → **DRF** (Batteries included, heavy)
│
├─ **Full Stack (Monolith)**
│  ├─ Complex UI (SPA)? → **Django + React/Vue** (API separation)
│  └─ Dynamic but Simple? → **Django + HTMX** (Hypermedia-driven, no build step)
│
└─ **Real-Time**
   ├─ Simple updates? → **HTMX Polling** or **SSE**
   └─ Complex/Bi-directional? → **Django Channels (WebSockets)**
```

### Async Strategy (Django 4.2+)

| Feature | Sync (WSGI) | Async (ASGI) | Recommendation |
|---------|-------------|--------------|----------------|
| **DB Queries** | `User.objects.get()` | `await User.objects.aget()` | Use Async for high-concurrency I/O (proxies, chat). |
| **Views** | `def view(req):` | `async def view(req):` | Keep Sync for CPU-bound tasks. |
| **Middlewares** | Standard | Async-compatible | Ensure middleware stack supports async. |

### Database Optimization

*   **N+1 Problem:** Always check `select_related` (Foreign Keys) and `prefetch_related` (M2M).
*   **Indexing:** Use `GinIndex` for JSONB search, `BTree` for standard lookups.
*   **Bulk Ops:** Use `bulk_create` and `bulk_update` for batches > 100 items.

**Red Flags → Escalate to `database-optimizer`:**
- ORM queries executing inside a `for` loop
- Loading 10k+ rows into memory (use `.iterator()`)
- "Raw SQL" usage without parameter binding (SQL Injection risk)
- Locking issues (Select for Update) blocking traffic

---
---

### Workflow 2: HTMX Integration (Server-Driven UI)

**Goal:** Implement an "Infinite Scroll" or "Click to Edit" without writing React.

**Steps:**

1.  **View (Python)**
    ```python
    def contact_list(request):
        contacts = Contact.objects.all()
        # If HTMX request, return only the rows (partial)
        if request.htmx:
            template = "partials/contact_rows.html"
        else:
            template = "contact_list.html"
        
        return render(request, template, {"contacts": contacts})
    ```

2.  **Template (`contact_list.html`)**
    ```html
    <!-- Search triggers server request on keyup -->
    <input type="text" 
           name="search" 
           hx-get="/contacts" 
           hx-trigger="keyup changed delay:500ms" 
           hx-target="#contact-rows">

    <table>
      <tbody id="contact-rows">
        {% include "partials/contact_rows.html" %}
      </tbody>
    </table>
    ```

---
---

### Workflow 4: Async ORM & Views

**Goal:** High-throughput API endpoint using `async/await`.

**Steps:**

1.  **View Definition**
    ```python
    # views.py
    from asgiref.sync import sync_to_async

    async def dashboard_stats(request):
        # Parallel DB queries
        user_count_task = User.objects.acount()
        order_count_task = Order.objects.acount()
        
        user_count, order_count = await asyncio.gather(
            user_count_task, 
            order_count_task
        )

        return JsonResponse({"users": user_count, "orders": order_count})
    ```

2.  **Middleware Compatibility**
    -   Ensure all middlewares are async-capable (`async_capable = True`).
    -   If blocking middleware exists, wrap it in `sync_to_async`.

---
---

## 4. Patterns & Templates

### Pattern 1: Service Layer (Business Logic)

**Use case:** Keeping Views and Models skinny.

```python
# services.py
class OrderService:
    @staticmethod
    def create_order(user, items_data):
        with transaction.atomic():
            order = Order.objects.create(user=user)
            for item in items_data:
                OrderItem.objects.create(order=order, **item)
            
            # Complex logic here
            PaymentGateway.charge(order)
            return order
```

### Pattern 2: Custom Manager (Query Logic)

**Use case:** Reusable filters.

```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PUBLISHED', pub_date__lte=timezone.now())

class Article(models.Model):
    # ...
    objects = models.Manager() # Default
    published = PublishedManager() # Custom
```

### Pattern 3: Async Chat (Channels)

**Use case:** WebSocket handling.

```python
# consumers.py
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "lobby"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_name,
            {"type": "chat_message", "message": text_data}
        )
```

---
---

## 6. Integration Patterns

### **frontend-ui-ux-engineer:**
-   **Handoff**: Django Developer creates HTMX partials (`_card.html`) → UI Dev styles them.
-   **Collaboration**: Defining "OOB Swaps" (Out of Band) for updating multiple page parts.
-   **Tools**: Tailwind CSS.

### **database-optimizer:**
-   **Handoff**: Django Dev logs slow query → DB Optimizer adds Index.
-   **Collaboration**: Analyzing `EXPLAIN ANALYZE` output from ORM generated SQL.
-   **Tools**: Django Debug Toolbar.

### **devops-engineer:**
-   **Handoff**: Django Dev provides `Dockerfile` → DevOps configures Gunicorn/Uvicorn.
-   **Collaboration**: Static files handling (Whitenoise vs S3/CloudFront).
-   **Tools**: Docker Compose.

---
