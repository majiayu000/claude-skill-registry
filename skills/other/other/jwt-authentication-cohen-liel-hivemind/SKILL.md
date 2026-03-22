---
name: jwt-authentication
description: JWT authentication implementation patterns. Use when implementing login, registration, token refresh, password reset, or any authentication/authorization system.
---

# JWT Authentication Patterns

## Token Strategy
- **Access token**: short-lived (15 min), stateless JWT
- **Refresh token**: long-lived (7 days), stored in DB for revocation
- **Storage**: access in memory (JS var), refresh in httpOnly cookie

## Implementation (FastAPI + Python-Jose)
```python
# auth/tokens.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = settings.SECRET_KEY  # 32+ char random string from env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(minutes=15)
REFRESH_TOKEN_EXPIRE = timedelta(days=7)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: int) -> str:
    return jwt.encode(
        {"sub": str(user_id), "exp": datetime.utcnow() + ACCESS_TOKEN_EXPIRE, "type": "access"},
        SECRET_KEY, algorithm=ALGORITHM
    )

def create_refresh_token(user_id: int) -> str:
    return jwt.encode(
        {"sub": str(user_id), "exp": datetime.utcnow() + REFRESH_TOKEN_EXPIRE, "type": "refresh"},
        SECRET_KEY, algorithm=ALGORITHM
    )

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
```

## Login Endpoint
```python
@router.post("/login", response_model=TokenResponse)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        # Same error for both cases — don't reveal which field was wrong
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Rate limit check (use Redis counter)
    await check_login_rate_limit(user.id)

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    # Store refresh token hash in DB for revocation
    await store_refresh_token(db, user.id, refresh_token)

    response = JSONResponse({"access_token": access_token, "token_type": "bearer"})
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite="lax")
    return response
```

## Auth Dependency
```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")
    user = await db.get(User, int(payload["sub"]))
    if not user or user.is_disabled:
        raise HTTPException(status_code=401, detail="User not found or disabled")
    return user
```

## Refresh Token Rotation
```python
@router.post("/refresh")
async def refresh(request: Request, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")
    payload = decode_token(refresh_token)
    # Verify token exists in DB (revocation check)
    stored = await get_refresh_token(db, refresh_token)
    if not stored:
        raise HTTPException(status_code=401, detail="Token revoked")
    # Rotate: delete old, issue new
    await delete_refresh_token(db, refresh_token)
    new_access = create_access_token(int(payload["sub"]))
    new_refresh = create_refresh_token(int(payload["sub"]))
    await store_refresh_token(db, int(payload["sub"]), new_refresh)
    response = JSONResponse({"access_token": new_access})
    response.set_cookie("refresh_token", new_refresh, httponly=True, secure=True, samesite="lax")
    return response
```

## Rules
- httpOnly cookies for refresh tokens (XSS can't steal them)
- Never store access tokens in localStorage (XSS risk)
- Refresh token rotation: old token invalidated immediately on use
- Rate limit login: 5 attempts per IP per 15 minutes
- Same error message for wrong email AND wrong password
- Logout must invalidate refresh token in DB
