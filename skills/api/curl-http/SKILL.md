---
name: curl-http
description: API testing with curl and httpie for HTTP requests. Use when user asks to "test API", "make HTTP request", "curl POST", "send request", "test endpoint", "debug API", or make any HTTP calls from command line.
---

# curl & HTTPie

Command-line HTTP clients for API testing.

## curl Basics

### GET Request

```bash
curl https://api.example.com/users
curl -s https://api.example.com/users  # Silent
curl -i https://api.example.com/users  # Include headers
```

### POST Request

```bash
# JSON body
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com"}'

# From file
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d @data.json
```

### Headers & Auth

```bash
# Custom header
curl -H "Authorization: Bearer token123" https://api.example.com

# Basic auth
curl -u username:password https://api.example.com

# Multiple headers
curl -H "Content-Type: application/json" \
     -H "X-API-Key: key123" \
     https://api.example.com
```

### Other Methods

```bash
# PUT
curl -X PUT https://api.example.com/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated"}'

# PATCH
curl -X PATCH https://api.example.com/users/1 \
  -d '{"status":"active"}'

# DELETE
curl -X DELETE https://api.example.com/users/1
```

### File Upload

```bash
# Form upload
curl -X POST https://api.example.com/upload \
  -F "file=@photo.jpg" \
  -F "description=My photo"

# Binary
curl -X POST https://api.example.com/upload \
  --data-binary @file.bin \
  -H "Content-Type: application/octet-stream"
```

### Useful Options

```bash
-v          # Verbose (debug)
-s          # Silent
-o file     # Output to file
-O          # Save with remote filename
-L          # Follow redirects
-k          # Ignore SSL errors
-w '\n'     # Add newline after output
--max-time 10  # Timeout in seconds
```

## HTTPie (Friendlier Alternative)

### GET Request

```bash
http https://api.example.com/users
http GET api.example.com/users  # Explicit GET
```

### POST Request

```bash
# JSON (default)
http POST api.example.com/users name=John email=john@example.com

# String vs other types
http POST api.example.com/users name=John age:=30 active:=true
```

### Headers & Auth

```bash
# Header
http api.example.com Authorization:"Bearer token"

# Basic auth
http -a user:pass api.example.com

# Bearer auth
http api.example.com "Authorization: Bearer token"
```

### Output Control

```bash
http -h api.example.com   # Headers only
http -b api.example.com   # Body only
http -p Hh api.example.com  # Request headers
```

## Common Patterns

### Test Response Code

```bash
# curl
status=$(curl -s -o /dev/null -w "%{http_code}" https://api.example.com)
echo "Status: $status"

# Check if successful
if curl -s -f https://api.example.com > /dev/null; then
  echo "Success"
fi
```

### Pretty Print JSON

```bash
curl -s https://api.example.com | jq .
curl -s https://api.example.com | python -m json.tool
```

### Save Response & Headers

```bash
curl -D headers.txt -o response.json https://api.example.com
```

### Retry on Failure

```bash
curl --retry 3 --retry-delay 2 https://api.example.com
```

### Timing Info

```bash
curl -w "Time: %{time_total}s\n" -o /dev/null -s https://api.example.com
```

### GraphQL

```bash
curl -X POST https://api.example.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { id name } }"}'
```

## Debug

```bash
# Verbose output
curl -v https://api.example.com

# Trace (very detailed)
curl --trace - https://api.example.com

# Show only response headers
curl -I https://api.example.com
```
