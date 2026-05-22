---
name: security-review
description: Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, Shopify webhooks, or implementing sensitive features in Go. Provides comprehensive security checklist and Go patterns.
---

# Security Review Skill (Go + Shopify)

This skill ensures all Go code follows security best practices and identifies potential vulnerabilities specific to Go/Fiber/Shopify applications.

## When to Activate

- Implementing authentication or authorization
- Handling user input or file uploads
- Creating new API endpoints (Fiber)
- Adding Shopify webhooks or OAuth
- Working with secrets or credentials
- Implementing payment features
- Storing or transmitting sensitive data
- Integrating third-party APIs
- Database operations

## Critical Security Checklist

### 1. Secrets Management

#### ❌ NEVER Do This
```go
const (
	APIKey       = "sk-proj-xxxxx"  // Hardcoded secret
	ShopifyKey   = "shpat_xxxxx"     // In source code
	DBPassword   = "password123"     // NEVER!
)
```

#### ✅ ALWAYS Do This
```go
func LoadConfig() (*Config, error) {
	shopifyKey := os.Getenv("SHOPIFY_API_KEY")
	if shopifyKey == "" {
		return nil, errors.New("SHOPIFY_API_KEY not configured")
	}

	return &Config{
		ShopifyAPIKey: shopifyKey,
		ShopifySecret: mustGetEnv("SHOPIFY_API_SECRET"),
		DatabaseURL:   mustGetEnv("DATABASE_URL"),
	}, nil
}

func mustGetEnv(key string) string {
	val := os.Getenv(key)
	if val == "" {
		log.Fatalf("%s environment variable not set", key)
	}
	return val
}
```

#### Verification Steps
- [ ] No hardcoded API keys, tokens, or passwords
- [ ] All secrets in environment variables
- [ ] `.env` in .gitignore
- [ ] No secrets in git history (`git log -p | grep -i "password\|api_key"`)
- [ ] Production secrets in hosting platform

### 2. SQL Injection Prevention

#### ❌ NEVER Concatenate SQL
```go
// DANGEROUS - SQL Injection vulnerability
query := fmt.Sprintf("SELECT * FROM users WHERE email = '%s'", userEmail)
db.QueryRow(context.Background(), query)
```

#### ✅ ALWAYS Use Parameterized Queries
```go
// Safe - parameterized query with pgx
query := `SELECT id, email, name FROM users WHERE email = $1`
err := db.QueryRow(ctx, query, userEmail).Scan(&user.ID, &user.Email, &user.Name)
```

#### Verification Steps
- [ ] All database queries use $1, $2 placeholders
- [ ] No string concatenation in SQL
- [ ] No fmt.Sprintf for query building
- [ ] All queries reviewed for injection vulnerabilities

### 3. Shopify Webhook HMAC Verification (CRITICAL)

#### ❌ NEVER Skip HMAC Verification
```go
// DANGEROUS - Processing unverified webhook
func HandleWebhook(w http.ResponseWriter, r *http.Request) {
	var order Order
	json.NewDecoder(r.Body).Decode(&order) // NO VERIFICATION!
	processOrder(order) // Could be forged!
}
```

#### ✅ ALWAYS Verify HMAC First
```go
func VerifyShopifyWebhook(r *http.Request, body []byte, secret string) bool {
	hmacHeader := r.Header.Get("X-Shopify-Hmac-Sha256")
	if hmacHeader == "" {
		return false
	}

	mac := hmac.New(sha256.New, []byte(secret))
	mac.Write(body)
	expectedMAC := base64.StdEncoding.EncodeToString(mac.Sum(nil))

	// Use hmac.Equal for constant-time comparison (prevents timing attacks)
	return hmac.Equal([]byte(hmacHeader), []byte(expectedMAC))
}

func HandleWebhook(w http.ResponseWriter, r *http.Request) {
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Bad request", http.StatusBadRequest)
		return
	}

	// Verify HMAC signature
	secret := os.Getenv("SHOPIFY_WEBHOOK_SECRET")
	if !VerifyShopifyWebhook(r, body, secret) {
		log.Warn("Invalid webhook HMAC signature")
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	// Process webhook asynchronously
	go processWebhookAsync(body)
	w.WriteHeader(http.StatusOK)
}
```

#### Verification Steps
- [ ] All Shopify webhooks verify HMAC
- [ ] OAuth callbacks verify HMAC
- [ ] Constant-time comparison used (hmac.Equal)
- [ ] GDPR webhooks implemented (all 3 required)
- [ ] Webhooks processed asynchronously

### 4. Input Validation

#### ❌ No Validation
```go
func CreateMarket(w http.ResponseWriter, r *http.Request) {
	var req CreateMarketRequest
	json.NewDecoder(r.Body).Decode(&req)

	// No validation - could be empty, malicious, etc.
	market := &Market{Name: req.Name}
	db.Create(market)
}
```

#### ✅ Validate with go-playground/validator
```go
import "github.com/go-playground/validator/v10"

type CreateMarketRequest struct {
	Name        string `json:"name" validate:"required,min=3,max=100"`
	Description string `json:"description" validate:"max=500"`
	Category    string `json:"category" validate:"required,oneof=politics sports finance"`
}

var validate = validator.New()

func CreateMarket(w http.ResponseWriter, r *http.Request) {
	var req CreateMarketRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		respondError(w, http.StatusBadRequest, "Invalid JSON")
		return
	}

	// Validate input
	if err := validate.Struct(req); err != nil {
		respondError(w, http.StatusBadRequest, fmt.Sprintf("Validation failed: %v", err))
		return
	}

	// Now safe to use validated input
	market := &Market{
		Name:        req.Name,
		Description: req.Description,
		Category:    req.Category,
	}
	// ...
}
```

#### Verification Steps
- [ ] All user inputs validated with go-playground/validator
- [ ] File uploads restricted (size, type, extension)
- [ ] No direct use of user input in queries
- [ ] Whitelist validation (not blacklist)
- [ ] Error messages don't leak sensitive info

### 5. Authentication & Authorization

#### JWT Token Validation
```go
import (
	"github.com/gofiber/fiber/v3"
	"github.com/golang-jwt/jwt/v5"
)

func AuthMiddleware(jwtSecret string) fiber.Handler {
	return func(c fiber.Ctx) error {
		authHeader := c.Get("Authorization")
		if authHeader == "" {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
				"error": "missing authorization header",
			})
		}

		tokenString := strings.TrimPrefix(authHeader, "Bearer ")
		if tokenString == authHeader {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
				"error": "invalid authorization format",
			})
		}

		// Parse and validate token
		token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
			// Validate signing method
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
			}
			return []byte(jwtSecret), nil
		})

		if err != nil || !token.Valid {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
				"error": "invalid token",
			})
		}

		// Extract claims and store in Locals
		claims, ok := token.Claims.(jwt.MapClaims)
		if !ok {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
				"error": "invalid claims",
			})
		}

		c.Locals("userID", claims["sub"])
		return c.Next()
	}
}
```

#### Authorization Checks
```go
func DeleteMarket(c fiber.Ctx) error {
	userID := fiber.Locals[string](c, "userID")
	marketID := c.Params("id")

	// Verify ownership
	market, err := repo.FindByID(c.Context(), marketID)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "not found",
		})
	}

	if market.OwnerID != userID {
		return c.Status(fiber.StatusForbidden).JSON(fiber.Map{
			"error": "forbidden",
		})
	}

	// Proceed with deletion
	err = repo.Delete(c.Context(), marketID)
	// ...
	return nil
}
```

#### Verification Steps
- [ ] JWT tokens validated with golang-jwt/jwt
- [ ] Authorization checks before sensitive operations
- [ ] HTTPS enforced (TLS 1.3+)
- [ ] Session management secure
- [ ] Passwords hashed with bcrypt (cost >= 12)

### 6. Password Hashing

#### ❌ NEVER Store Plaintext or Weak Hashing
```go
// WRONG - plaintext
user.Password = password

// WRONG - weak hashing
hash := sha256.Sum256([]byte(password))
```

#### ✅ Use bcrypt
```go
import "golang.org/x/crypto/bcrypt"

func CreateUser(email, password string) error {
	// Hash password with bcrypt (cost 12-14 recommended)
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), 12)
	if err != nil {
		return fmt.Errorf("failed to hash password: %w", err)
	}

	user := &User{
		Email:        email,
		PasswordHash: string(hashedPassword),
	}

	return db.Create(context.Background(), user)
}

func VerifyPassword(hashedPassword, password string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(password))
	return err == nil
}
```

### 7. Race Condition Prevention

#### Run Race Detector
```bash
go test -race ./...
```

#### Use Mutexes for Shared State
```go
type SafeCounter struct {
	mu    sync.RWMutex
	count map[string]int
}

func (c *SafeCounter) Increment(key string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.count[key]++
}

func (c *SafeCounter) Value(key string) int {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return c.count[key]
}
```

### 8. Error Handling (Don't Leak Info)

#### ❌ Leaking Internal Details
```go
// WRONG - exposes internal error details to user
http.Error(w, fmt.Sprintf("Database error: %v", err), http.StatusInternalServerError)
```

#### ✅ Generic Error Messages
```go
// CORRECT - log detailed error, return generic message
log.Error("Database connection failed", "error", err, "table", "markets")
http.Error(w, "Internal server error", http.StatusInternalServerError)
```

### 9. Logging Security

#### ❌ Logging Sensitive Data
```go
// WRONG - logs passwords, tokens
log.Printf("User login: email=%s password=%s", email, password)
log.Printf("Request: %+v", r.Header) // Contains auth tokens!
```

#### ✅ Sanitized Logging
```go
import "log/slog"

// CORRECT - structured logging without sensitive data
slog.Info("User login attempt",
	"email", maskEmail(email),
	"ip", r.RemoteAddr,
)

// Never log: passwords, API keys, tokens, credit cards, SSNs
```

## Security Scanning Commands

```bash
# Check for security vulnerabilities
gosec ./...

# Check for vulnerable dependencies
go list -json -m all | nancy sleuth

# Comprehensive vulnerability scan
trivy fs --scanners vuln,secret,misconfig .

# Run security-focused linters
golangci-lint run --enable=gosec,gocritic,bodyclose,errcheck

# Check for secrets in files
grep -r "api[_-]?key\|password\|secret\|token" --include="*.go" .

# Check for Shopify secrets
grep -r "shpat_\|shpca_\|shpss_" --include="*.go" .

# Test for race conditions
go test -race ./...
```

## Pre-Deployment Security Checklist

Before deploying to production:

### Code Security
- [ ] gosec ./... passes with no critical issues
- [ ] go test -race ./... passes
- [ ] All secrets in environment variables
- [ ] No hardcoded credentials in code or git history
- [ ] Input validation on all endpoints
- [ ] Error messages don't leak sensitive info

### Shopify Security
- [ ] Webhook HMAC verification implemented
- [ ] OAuth HMAC verification implemented
- [ ] All 3 GDPR webhooks implemented
- [ ] Shop domain validation
- [ ] Session tokens validated
- [ ] No Shopify secrets in frontend code

### Database Security
- [ ] All queries parameterized ($1, $2, etc.)
- [ ] Database connection uses TLS
- [ ] Connection strings in environment variables
- [ ] No SQL injection vulnerabilities

### Authentication/Authorization
- [ ] JWT tokens validated properly
- [ ] Passwords hashed with bcrypt (cost >= 12)
- [ ] Authorization checks on all protected routes
- [ ] HTTPS enforced

### Dependencies
- [ ] nancy scan clean (no vulnerable dependencies)
- [ ] go.mod dependencies up to date
- [ ] No known CVEs in dependencies

## Common Vulnerabilities (OWASP Top 10 for Go)

1. **SQL Injection** - Use parameterized queries ($1, $2)
2. **Command Injection** - Avoid exec.Command with user input
3. **Hardcoded Secrets** - All secrets in environment variables
4. **Missing Error Checks** - Always check errors (never `_`)
5. **Race Conditions** - Use mutexes, test with -race
6. **Weak Crypto** - bcrypt for passwords, not MD5/SHA256
7. **HMAC Verification** - Verify Shopify webhooks/OAuth
8. **Input Validation** - Use go-playground/validator
9. **JWT Validation** - Validate signature and expiry
10. **Logging Sensitive Data** - Sanitize logs (slog/zap)

## Security Resources

- **Go Security Guide**: https://go.dev/doc/security/
- **OWASP Go**: https://owasp.org/www-project-go-secure-coding-practices-guide/
- **Shopify Security**: https://shopify.dev/docs/apps/launch/security
- **gosec**: https://github.com/securego/gosec
- **CWE Top 25**: https://cwe.mitre.org/top25/

---

**Remember**: Security is not optional, especially for Shopify apps handling merchant data. One vulnerability can compromise the entire app and result in app suspension.

For comprehensive security review, use the `security-reviewer` agent which provides detailed vulnerability analysis and remediation.
