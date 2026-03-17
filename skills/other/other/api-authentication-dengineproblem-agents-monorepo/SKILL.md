---
name: api-authentication
description: Эксперт по API аутентификации. Используй для OAuth 2.0, JWT, API keys, сессий, безопасности токенов и best practices.
---

# API Authentication Expert

Эксперт по аутентификации API с глубокими знаниями протоколов аутентификации, лучших практик безопасности и паттернов реализации.

## Основные методы аутентификации

### API Keys
```javascript
// Header-based API key
const response = await fetch('/api/data', {
  headers: {
    'X-API-Key': 'your-api-key-here',
    'Content-Type': 'application/json'
  }
});

// Query parameter (менее безопасно)
const response = await fetch('/api/data?api_key=your-api-key');
```

### JWT (JSON Web Tokens)
```python
import jwt
from datetime import datetime, timedelta

# Генерация JWT
def create_jwt_token(user_id, secret_key):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

# Верификация JWT
def verify_jwt_token(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
```

### OAuth 2.0 Authorization Code Flow
```javascript
// Шаг 1: Редирект на сервер авторизации
const authUrl = `https://auth.provider.com/oauth/authorize?
  client_id=${clientId}&
  redirect_uri=${redirectUri}&
  response_type=code&
  scope=read:user&
  state=${randomState}`;

// Шаг 2: Обмен кода на access token
async function exchangeCodeForToken(code) {
  const response = await fetch('https://auth.provider.com/oauth/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': `Basic ${btoa(`${clientId}:${clientSecret}`)}`
    },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code: code,
      redirect_uri: redirectUri
    })
  });
  return await response.json();
}
```

## Безопасное хранение токенов

### HttpOnly Cookies
```javascript
// Server-side cookie configuration
res.cookie('refreshToken', refreshToken, {
  httpOnly: true,
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'strict',
  maxAge: 7 * 24 * 60 * 60 * 1000 // 7 дней
});
```

### Рекомендации
- Всегда используйте HTTPS для передачи токенов
- Храните refresh токены в HttpOnly cookies
- Access токены храните в памяти (не в localStorage)
- Используйте короткоживущие access токены (15-60 минут)

## Rate Limiting

```python
from functools import wraps
from flask import request, jsonify
from time import time

def rate_limit(max_requests=100, window=3600):
    def decorator(f):
        requests_store = {}

        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time()

            # Очистка старых записей
            requests_store[client_ip] = [
                t for t in requests_store.get(client_ip, [])
                if current_time - t < window
            ]

            if len(requests_store.get(client_ip, [])) >= max_requests:
                return jsonify({'error': 'Rate limit exceeded'}), 429

            requests_store.setdefault(client_ip, []).append(current_time)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

## Middleware аутентификации

### Go
```go
func AuthMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if token == "" {
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
            return
        }

        // Remove "Bearer " prefix
        if strings.HasPrefix(token, "Bearer ") {
            token = token[7:]
        }

        userID, err := validateJWT(token)
        if err != nil {
            http.Error(w, "Invalid token", http.StatusUnauthorized)
            return
        }

        ctx := context.WithValue(r.Context(), "userID", userID)
        next(w, r.WithContext(ctx))
    }
}
```

### TypeScript/Express
```typescript
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

interface AuthRequest extends Request {
  userId?: string;
}

export const authMiddleware = (
  req: AuthRequest,
  res: Response,
  next: NextFunction
) => {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing token' });
  }

  const token = authHeader.slice(7);

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as { userId: string };
    req.userId = decoded.userId;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};
```

## Token Refresh Strategy

```typescript
class TokenManager {
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  async refreshTokens(): Promise<boolean> {
    try {
      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        credentials: 'include' // для httpOnly cookies
      });

      if (!response.ok) {
        throw new Error('Token refresh failed');
      }

      const { accessToken } = await response.json();
      this.accessToken = accessToken;
      return true;
    } catch (error) {
      this.logout();
      return false;
    }
  }

  async makeAuthenticatedRequest(url: string, options: RequestInit = {}) {
    if (this.isTokenExpired()) {
      const refreshed = await this.refreshTokens();
      if (!refreshed) {
        throw new Error('Session expired');
      }
    }

    return fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${this.accessToken}`
      }
    });
  }

  private isTokenExpired(): boolean {
    if (!this.accessToken) return true;

    const payload = JSON.parse(atob(this.accessToken.split('.')[1]));
    return payload.exp * 1000 < Date.now();
  }
}
```

## Multi-Factor Authentication (MFA)

```python
import pyotp
import qrcode
from io import BytesIO

def generate_totp_secret(user_email):
    secret = pyotp.random_base32()
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user_email,
        issuer_name="Your App Name"
    )

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)

    return secret, qr

def verify_totp(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)
```

## Security Headers

```javascript
const helmet = require('helmet');
const cors = require('cors');

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
    },
  },
}));

app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
  credentials: true,
  optionsSuccessStatus: 200
}));
```

## Key Rotation

```python
class KeyRotationManager:
    def __init__(self):
        self.current_key_id = self.get_current_key_id()
        self.keys = self.load_signing_keys()

    def sign_token(self, payload):
        key = self.keys[self.current_key_id]
        payload['kid'] = self.current_key_id
        return jwt.encode(payload, key, algorithm='RS256')

    def verify_token(self, token):
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get('kid')

        if kid not in self.keys:
            raise jwt.InvalidKeyError("Invalid key ID")

        return jwt.decode(token, self.keys[kid], algorithms=['RS256'])
```

## Лучшие практики

1. **Используйте HTTPS везде** — никогда не передавайте токены по HTTP
2. **Короткоживущие access токены** — 15-60 минут максимум
3. **Secure refresh tokens** — HttpOnly cookies, ротация при использовании
4. **Валидация на каждом запросе** — не кэшируйте результаты авторизации
5. **Логирование событий безопасности** — все попытки входа, ошибки токенов
6. **Rate limiting** — защита от brute force атак
7. **Ротация ключей** — регулярная смена signing keys
