---
name: pricing-app-ml-integration
description: MercadoLibre API integration patterns - OAuth, webhooks, item sync, order tracking
license: MIT
metadata:
  author: pricing-app
  version: "1.0.0"
  scope: [backend, root]
  auto_invoke:
    - "Working with MercadoLibre API"
    - "Implementing ML OAuth flow"
    - "Processing ML webhooks"
    - "Syncing items to/from MercadoLibre"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Pricing App - MercadoLibre Integration

---

## CRITICAL RULES - NON-NEGOTIABLE

### OAuth Token Management
- ALWAYS: Store refresh_token securely in environment variables
- ALWAYS: Check token expiration before API calls
- ALWAYS: Add 5-minute margin to token expiry: `expires_at - 300 seconds`
- ALWAYS: Update refresh_token if new one is provided in response
- NEVER: Hardcode tokens in code
- NEVER: Log access tokens or refresh tokens

### API Client Patterns
- ALWAYS: Use httpx.AsyncClient for async operations
- ALWAYS: Set reasonable timeouts (10-15 seconds)
- ALWAYS: Handle 404, 429 (rate limit), 401 (unauthorized) separately
- ALWAYS: Use batch endpoints when fetching multiple items (20 items max per batch)
- NEVER: Make synchronous blocking calls in FastAPI endpoints

### Webhook Handling
- ALWAYS: Validate webhook signatures (if ML provides them)
- ALWAYS: Respond quickly (< 3 seconds) to webhook calls
- ALWAYS: Queue webhook processing with background tasks
- ALWAYS: Store raw webhook payload for debugging
- NEVER: Process heavy logic in webhook endpoint

### Error Handling
- ALWAYS: Log errors with context (item_id, user_id, endpoint)
- ALWAYS: Return None or empty list on non-critical errors
- ALWAYS: Retry transient errors (network, 5xx) with exponential backoff
- NEVER: Let external API errors crash your app

---

## TECH STACK

httpx (async HTTP client) | MercadoLibre API v1 | OAuth 2.0 | FastAPI BackgroundTasks

---

## PATTERNS

### OAuth Client Implementation

```python
import httpx
import os
from typing import Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class MercadoLibreAPIClient:
    """Client for MercadoLibre API with OAuth handling"""
    
    def __init__(self):
        self.base_url = "https://api.mercadolibre.com"
        self.client_id = os.getenv("ML_CLIENT_ID")
        self.client_secret = os.getenv("ML_CLIENT_SECRET")
        self.user_id = os.getenv("ML_USER_ID")
        self.refresh_token = os.getenv("ML_REFRESH_TOKEN")
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
    
    async def get_access_token(self) -> str:
        """Get or refresh access token"""
        # Return cached token if still valid
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token
        
        # Refresh token
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/oauth/token",
                    data={
                        "grant_type": "refresh_token",
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "refresh_token": self.refresh_token
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                self.access_token = data["access_token"]
                expires_in = data.get("expires_in", 21600)  # 6 hours default
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)
                
                # Update refresh token if provided
                if "refresh_token" in data:
                    self.refresh_token = data["refresh_token"]
                    # TODO: Persist new refresh_token to secure storage
                
                return self.access_token
        
        except Exception as e:
            logger.error(f"Error refreshing ML token: {e}")
            raise
```

### Fetch Single Item

```python
async def get_item(self, item_id: str) -> Optional[dict]:
    """
    Fetch single item from MercadoLibre.
    
    Args:
        item_id: MLA/MLB item ID
    
    Returns:
        Item data or None if not found
    """
    try:
        token = await self.get_access_token()
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/items/{item_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 404:
                logger.warning(f"Item {item_id} not found")
                return None
            
            response.raise_for_status()
            return response.json()
    
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            logger.warning(f"Rate limit hit for item {item_id}")
        else:
            logger.error(f"HTTP error fetching item {item_id}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error fetching item {item_id}: {e}")
        return None
```

### Batch Fetch Items

```python
async def get_items_batch(self, item_ids: list[str]) -> dict[str, dict]:
    """
    Fetch multiple items in batch (max 20 per request).
    
    Args:
        item_ids: List of item IDs
    
    Returns:
        Dict mapping item_id -> item_data
    """
    results = {}
    
    if not item_ids:
        return results
    
    try:
        token = await self.get_access_token()
        
        # ML allows up to 20 items per request
        batch_size = 20
        for i in range(0, len(item_ids), batch_size):
            batch = item_ids[i:i + batch_size]
            ids_param = ",".join(batch)
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/items",
                    params={"ids": ids_param},
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                
                # Response is array of {code, body}
                data = response.json()
                for item_response in data:
                    if item_response.get("code") == 200:
                        body = item_response.get("body")
                        if body:
                            results[body["id"]] = body
    
    except Exception as e:
        logger.error(f"Error fetching batch: {e}")
    
    return results
```

### Update Item Price

```python
async def update_item_price(self, item_id: str, new_price: float) -> bool:
    """
    Update item price on MercadoLibre.
    
    Args:
        item_id: MLA/MLB item ID
        new_price: New price (float)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        token = await self.get_access_token()
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.put(
                f"{self.base_url}/items/{item_id}",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json={"price": new_price}
            )
            
            response.raise_for_status()
            logger.info(f"Updated price for {item_id} to {new_price}")
            return True
    
    except Exception as e:
        logger.error(f"Error updating price for {item_id}: {e}")
        return False
```

### Webhook Endpoint

```python
from fastapi import APIRouter, BackgroundTasks, Request
from app.services.ml_webhook_service import process_ml_notification

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("/mercadolibre")
async def ml_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    MercadoLibre webhook endpoint.
    Responds quickly and queues processing.
    """
    try:
        # Get raw body for logging
        body = await request.json()
        
        # Log received notification
        logger.info(f"ML webhook received: {body.get('topic')}")
        
        # Queue background processing
        background_tasks.add_task(process_ml_notification, body)
        
        # Respond immediately (ML requires < 3 seconds)
        return {"status": "ok"}
    
    except Exception as e:
        logger.error(f"Error receiving ML webhook: {e}")
        return {"status": "error"}, 500
```

### Background Webhook Processor

```python
async def process_ml_notification(notification: dict):
    """
    Process ML notification in background.
    
    Notification types:
    - orders: New order created
    - items: Item updated
    - questions: New question
    """
    try:
        topic = notification.get("topic")
        resource = notification.get("resource")
        
        if topic == "orders_v2":
            # Fetch full order data
            order_id = resource.split("/")[-1]
            await sync_order_from_ml(order_id)
        
        elif topic == "items":
            # Item was updated (price, stock, etc.)
            item_id = resource.split("/")[-1]
            await sync_item_from_ml(item_id)
        
        elif topic == "questions":
            # New question received
            question_id = resource.split("/")[-1]
            await handle_new_question(question_id)
        
        else:
            logger.warning(f"Unknown webhook topic: {topic}")
    
    except Exception as e:
        logger.error(f"Error processing ML notification: {e}")
```

---

## COMMON PITFALLS

- ❌ Don't fetch items one-by-one → Use batch endpoint (20 items per request)
- ❌ Don't ignore token expiration → Always check before API calls
- ❌ Don't process webhooks synchronously → Use BackgroundTasks
- ❌ Don't retry on 4xx errors → Only retry 5xx and network errors
- ❌ Don't log sensitive data → Never log access tokens
- ❌ Don't assume webhook order → ML may send duplicates or out-of-order

---

## ENVIRONMENT VARIABLES

```bash
# MercadoLibre OAuth
ML_CLIENT_ID=your_client_id
ML_CLIENT_SECRET=your_client_secret
ML_USER_ID=your_user_id
ML_REFRESH_TOKEN=your_refresh_token

# Optional
ML_WEBHOOK_SECRET=your_webhook_secret  # For signature validation
```

---

## REFERENCES

### External
- MercadoLibre API Docs: https://developers.mercadolibre.com/
- OAuth Guide: https://developers.mercadolibre.com/es_ar/autenticacion-y-autorizacion
- Items API: https://developers.mercadolibre.com/es_ar/items-y-busquedas
- Orders API: https://developers.mercadolibre.com/es_ar/gestiona-ventas
- Webhooks: https://developers.mercadolibre.com/es_ar/notificaciones-webhooks

### Internal
- [ML API Endpoints Reference](references/ml-api-endpoints.md) - Quick reference for common endpoints
- [ML Sync Process](../../backend/app/scripts/README_ML_SYNC.md) - Catalog sync documentation
- ML API Client: [ml_api_client.py](../../backend/app/services/ml_api_client.py)
- ML Sync Service: [ml_sync.py](../../backend/app/services/ml_sync.py)
- ML Webhook Service: [ml_webhook_service.py](../../backend/app/services/ml_webhook_service.py)
