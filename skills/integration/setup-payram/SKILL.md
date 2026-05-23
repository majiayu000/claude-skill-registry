---
name: setup-payram
description: Configure and validate connectivity to a self-hosted Payram server
---

# Setup Payram

Configure your backend to connect to a self-hosted Payram server and validate the connection.

## Overview

This skill guides you through:

1. Creating the required `.env` configuration
2. Understanding Payram's authentication model
3. Testing connectivity to your Payram instance
4. Troubleshooting common connection issues

## When to Use

- Starting a new Payram integration
- Validating existing Payram configuration
- Troubleshooting connection errors
- Setting up a new environment (staging, production)

## Prerequisites

You must have:

- A self-hosted Payram server deployed and accessible
- Admin access to the Payram dashboard
- An API key generated from the dashboard (Settings → Accounts → API Keys)

## Instructions

### Step 1: Create Environment Configuration

Create a `.env` file in your project root with the following variables:

```bash
# Payram REST base URL (include protocol, no trailing slash)
PAYRAM_BASE_URL=https://your-payram-server.example

# Payram API key (from dashboard Settings → Accounts → API Keys)
PAYRAM_API_KEY=pk_live_your_actual_key_here
```

**Required Variables:**

- `PAYRAM_BASE_URL`: Full URL to your self-hosted Payram instance
- `PAYRAM_API_KEY`: Project-scoped API key from the Payram dashboard

**Important:** Never commit `.env` files to version control. Add `.env` to your `.gitignore`.

### Step 2: Understand Authentication

Payram uses header-based authentication:

```
API-Key: your_api_key_here
```

**NOT** `Authorization: Bearer ...` - this will fail with 401.

The API key must be:

- Sent in the `API-Key` header (case-sensitive)
- Generated for the specific project/workspace you're integrating
- Kept secret and never exposed in client-side code

### Step 3: Test Connectivity

Create a test script to validate your connection. The connection test creates a minimal payment request to verify:

- Network reachability
- API key validity
- Correct authentication setup

#### Node.js/TypeScript (Using Payram SDK)

**Install SDK:**

```bash
npm install payram dotenv
```

**Test Script:**

```typescript
import { Payram, isPayramSDKError } from 'payram';
import dotenv from 'dotenv';

dotenv.config();

const baseUrl = process.env.PAYRAM_BASE_URL;
const apiKey = process.env.PAYRAM_API_KEY;

if (!baseUrl || !apiKey) {
  console.error('❌ Missing PAYRAM_BASE_URL or PAYRAM_API_KEY in .env');
  process.exit(1);
}

async function testConnection() {
  try {
    // Initialize Payram SDK
    const payram = new Payram({
      apiKey,
      baseUrl,
      config: {
        timeoutMs: 10_000,
        maxRetries: 2,
      },
    });

    console.log('🔄 Testing connection to Payram...');
    console.log(`   Base URL: ${baseUrl}`);

    // Create a minimal test payment
    const checkout = await payram.payments.initiatePayment({
      customerEmail: 'test@example.com',
      customerId: 'connectivity-test',
      amountInUSD: 1,
    });

    console.log('✅ Connection successful!');
    console.log(`   Reference ID: ${checkout.reference_id}`);
    console.log(`   Checkout URL: ${checkout.url}`);

    return true;
  } catch (error) {
    console.error('❌ Connection failed');

    if (isPayramSDKError(error)) {
      console.error(`   Status: ${error.status}`);
      console.error(`   Error: ${error.error}`);
      console.error(`   Request ID: ${error.requestId}`);
      console.error(`   Retryable: ${error.isRetryable}`);
    } else {
      console.error(`   Error: ${error instanceof Error ? error.message : String(error)}`);
    }

    return false;
  }
}

testConnection();
```

#### Python (Using requests)

**Install dependencies:**

```bash
pip install requests python-dotenv
```

**Test Script:**

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv('PAYRAM_BASE_URL')
api_key = os.getenv('PAYRAM_API_KEY')

if not base_url or not api_key:
    print('❌ Missing PAYRAM_BASE_URL or PAYRAM_API_KEY in .env')
    exit(1)

def test_connection():
    try:
        print('🔄 Testing connection to Payram...')
        print(f'   Base URL: {base_url}')

        endpoint = f"{base_url}/api/v1/payment"
        headers = {
            'API-Key': api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        payload = {
            'customerEmail': 'test@example.com',
            'customerId': 'connectivity-test',
            'amountInUSD': 1,
        }

        response = requests.post(endpoint, json=payload, headers=headers, timeout=10)

        if response.status_code in [200, 201]:
            data = response.json()
            print('✅ Connection successful!')
            print(f"   Reference ID: {data.get('reference_id', 'N/A')}")
            print(f"   Checkout URL: {data.get('url', 'N/A')}")
            return True
        else:
            print('❌ Connection failed')
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print('❌ Connection failed')
        print(f"   Error: {str(e)}")
        return False

if __name__ == '__main__':
    test_connection()
```

#### Go (Using net/http)

**Test Script:**

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "os"
    "time"

    "github.com/joho/godotenv"
)

type PaymentRequest struct {
    CustomerEmail string  `json:"customerEmail"`
    CustomerID    string  `json:"customerId"`
    AmountInUSD   float64 `json:"amountInUSD"`
}

type PaymentResponse struct {
    ReferenceID string `json:"reference_id"`
    URL         string `json:"url"`
}

func testConnection() bool {
    godotenv.Load()

    baseURL := os.Getenv("PAYRAM_BASE_URL")
    apiKey := os.Getenv("PAYRAM_API_KEY")

    if baseURL == "" || apiKey == "" {
        fmt.Println("❌ Missing PAYRAM_BASE_URL or PAYRAM_API_KEY in .env")
        return false
    }

    fmt.Println("🔄 Testing connection to Payram...")
    fmt.Printf("   Base URL: %s\n", baseURL)

    payload := PaymentRequest{
        CustomerEmail: "test@example.com",
        CustomerID:    "connectivity-test",
        AmountInUSD:   1.0,
    }

    body, _ := json.Marshal(payload)

    client := &http.Client{Timeout: 10 * time.Second}
    req, err := http.NewRequest("POST", baseURL+"/api/v1/payment", bytes.NewBuffer(body))
    if err != nil {
        fmt.Printf("❌ Failed to create request: %v\n", err)
        return false
    }

    req.Header.Set("API-Key", apiKey)
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("Accept", "application/json")

    resp, err := client.Do(req)
    if err != nil {
        fmt.Printf("❌ Connection failed: %v\n", err)
        return false
    }
    defer resp.Body.Close()

    if resp.StatusCode == 200 || resp.StatusCode == 201 {
        var result PaymentResponse
        bodyBytes, _ := io.ReadAll(resp.Body)
        json.Unmarshal(bodyBytes, &result)

        fmt.Println("✅ Connection successful!")
        fmt.Printf("   Reference ID: %s\n", result.ReferenceID)
        fmt.Printf("   Checkout URL: %s\n", result.URL)
        return true
    } else {
        fmt.Printf("❌ Connection failed: Status %d\n", resp.StatusCode)
        bodyBytes, _ := io.ReadAll(resp.Body)
        fmt.Printf("   Response: %s\n", string(bodyBytes))
        return false
    }
}

func main() {
    testConnection()
}
```

#### PHP (Using cURL)

**Test Script:**

```php
<?php
require __DIR__ . '/vendor/autoload.php';

use Dotenv\Dotenv;

$dotenv = Dotenv::createImmutable(__DIR__);
$dotenv->load();

$baseUrl = $_ENV['PAYRAM_BASE_URL'] ?? null;
$apiKey = $_ENV['PAYRAM_API_KEY'] ?? null;

if (!$baseUrl || !$apiKey) {
    echo "❌ Missing PAYRAM_BASE_URL or PAYRAM_API_KEY in .env\n";
    exit(1);
}

function testConnection($baseUrl, $apiKey) {
    echo "🔄 Testing connection to Payram...\n";
    echo "   Base URL: $baseUrl\n";

    $payload = [
        'customerEmail' => 'test@example.com',
        'customerId' => 'connectivity-test',
        'amountInUSD' => 1,
    ];

    $ch = curl_init($baseUrl . '/api/v1/payment');
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => [
            'API-Key: ' . $apiKey,
            'Content-Type: application/json',
            'Accept: application/json',
        ],
        CURLOPT_POSTFIELDS => json_encode($payload),
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 10,
    ]);

    $response = curl_exec($ch);
    $statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);

    if ($error) {
        echo "❌ Connection failed: $error\n";
        return false;
    }

    if ($statusCode === 200 || $statusCode === 201) {
        $data = json_decode($response, true);
        echo "✅ Connection successful!\n";
        echo "   Reference ID: " . ($data['reference_id'] ?? 'N/A') . "\n";
        echo "   Checkout URL: " . ($data['url'] ?? 'N/A') . "\n";
        return true;
    } else {
        echo "❌ Connection failed: Status $statusCode\n";
        echo "   Response: $response\n";
        return false;
    }
}

testConnection($baseUrl, $apiKey);
```

#### Java (Using HttpClient)

**Test Script:**

```java
package com.example.payram;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

import io.github.cdimascio.dotenv.Dotenv;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

public class ConnectionTest {

    public static void main(String[] args) {
        Dotenv dotenv = Dotenv.load();

        String baseUrl = dotenv.get("PAYRAM_BASE_URL");
        String apiKey = dotenv.get("PAYRAM_API_KEY");

        if (baseUrl == null || apiKey == null) {
            System.out.println("❌ Missing PAYRAM_BASE_URL or PAYRAM_API_KEY in .env");
            System.exit(1);
        }

        testConnection(baseUrl, apiKey);
    }

    public static boolean testConnection(String baseUrl, String apiKey) {
        try {
            System.out.println("🔄 Testing connection to Payram...");
            System.out.println("   Base URL: " + baseUrl);

            // Create JSON payload
            ObjectMapper mapper = new ObjectMapper();
            ObjectNode payload = mapper.createObjectNode();
            payload.put("customerEmail", "test@example.com");
            payload.put("customerId", "connectivity-test");
            payload.put("amountInUSD", 1);

            // Build HTTP request
            HttpClient client = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(10))
                .build();

            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/api/v1/payment"))
                .header("API-Key", apiKey)
                .header("Content-Type", "application/json")
                .header("Accept", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(payload)))
                .timeout(Duration.ofSeconds(10))
                .build();

            // Send request
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() == 200 || response.statusCode() == 201) {
                ObjectNode result = (ObjectNode) mapper.readTree(response.body());
                System.out.println("✅ Connection successful!");
                System.out.println("   Reference ID: " + result.get("reference_id").asText());
                System.out.println("   Checkout URL: " + result.get("url").asText());
                return true;
            } else {
                System.out.println("❌ Connection failed: Status " + response.statusCode());
                System.out.println("   Response: " + response.body());
                return false;
            }

        } catch (Exception e) {
            System.out.println("❌ Connection failed: " + e.getMessage());
            return false;
        }
    }
}
```

### Step 4: Interpret Results

**Success (200/201):**

```json
{
  "checkout": {
    "id": "...",
    "url": "https://...",
    ...
  }
}
```

Your configuration is correct and Payram is reachable.

**401 Unauthorized:**

- Check that `API-Key` header is used (not `Authorization`)
- Verify the API key is correct and hasn't been revoked
- Ensure the key is for the correct project/workspace

**404 Not Found:**

- Verify `PAYRAM_BASE_URL` is correct
- Check for typos in the endpoint path
- Confirm Payram is deployed and running

**Network Errors:**

- Verify firewall rules allow outbound HTTPS
- Check DNS resolution of your Payram domain
- Confirm SSL certificates are valid

## Best Practices

1. **Environment Separation**
   - Use different API keys for staging vs production
   - Never share API keys between environments
   - Rotate keys regularly

2. **Security**
   - Store API keys in secure secret management systems (AWS Secrets Manager, Vault, etc.)
   - Never log full API keys
   - Use environment-specific `.env` files (`.env.staging`, `.env.production`)

3. **Error Handling**
   - Always check response status codes
   - Log failures with context but without sensitive data
   - Implement retry logic with exponential backoff for network errors

4. **Validation**
   - Test connectivity before deploying to production
   - Run connectivity tests as part of CI/CD health checks
   - Monitor connection health in production with periodic pings

## Troubleshooting

### "Missing PAYRAM_BASE_URL or PAYRAM_API_KEY"

**Cause:** Environment variables not loaded.

**Solution:**

- Ensure `.env` file exists in project root
- Verify `.env` contains both variables
- Check that your code loads `.env` (e.g., `dotenv.config()` in Node, `load_dotenv()` in Python)

### "401 Unauthorized" or "Authentication Failed"

**Cause:** Invalid or missing API key.

**Solution:**

- Confirm you're using `API-Key` header, not `Authorization`
- Regenerate API key in Payram dashboard if needed
- Check for extra whitespace in `.env` values

### "Network error" or "Connection refused"

**Cause:** Payram server unreachable.

**Solution:**

- Verify `PAYRAM_BASE_URL` includes protocol (https://)
- Check firewall rules and network connectivity
- Confirm Payram service is running (`systemctl status payram`)

### "404 Not Found"

**Cause:** Wrong endpoint or base URL.

**Solution:**

- Remove trailing slashes from `PAYRAM_BASE_URL`
- Verify endpoint path is `/api/v1/payment`
- Check Payram version compatibility

## Related Skills

- `integrate-payments` - After setup, implement payment flows
- `integrate-payouts` - Configure outbound payment capabilities
- `handle-webhooks` - Receive Payram event notifications
