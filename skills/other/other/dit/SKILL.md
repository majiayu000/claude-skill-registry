---
name: dit
description: Classify HTML pages, forms, and fields using machine learning. Use when the user needs to detect page types (login, error, captcha), identify form types (login, search, registration), or classify form fields (username, password, email) from HTML content or URLs.
---

# dit - HTML Page, Form & Field Classifier

dît (means "found" in Kurdish) classifies HTML pages, forms, and fields using machine learning (LogReg + CRF). Zero external ML dependencies.

It classifies pages (login, error, landing, blog, etc.), detects form types (login, search, registration, password recovery, contact, etc.), and classifies each field (username, password, email, search query, etc.).

## Installation

```bash
go get github.com/happyhackingspace/dit
```

Or install the CLI:

```bash
go install github.com/happyhackingspace/dit/cmd/dit@latest
```

## CLI Usage

```bash
# Classify page type and forms on a URL
dit run https://github.com/login

# Classify forms in a local file
dit run login.html

# With probabilities
dit run https://github.com/login --proba

# Download training data and model from Hugging Face
dit data download

# Train a model
dit train model.json --data-folder data

# Evaluate model accuracy
dit evaluate --data-folder data

# Upload training data and model to Hugging Face
dit data upload
```

## Library Usage (Go)

```go
import "github.com/happyhackingspace/dit"

// Load classifier
c, _ := dit.New()

// Classify page type
page, _ := c.ExtractPageType(htmlString)
fmt.Println(page.Type)  // "login"
fmt.Println(page.Forms) // form classifications included

// Classify forms in HTML
results, _ := c.ExtractForms(htmlString)
for _, r := range results {
    fmt.Println(r.Type)   // "login"
    fmt.Println(r.Fields) // {"username": "username or email", "password": "password"}
}

// With probabilities
pageProba, _ := c.ExtractPageTypeProba(htmlString, 0.05)
formProba, _ := c.ExtractFormsProba(htmlString, 0.05)
```

## Page Types

login, registration, search, checkout, contact, password_reset, landing, product, blog, settings, soft_404, error, captcha, parked, coming_soon, admin, directory_listing, default_page, waf_block, other.

## Form Types

login, search, registration, password/login recovery, contact/comment, join mailing list, order/add to cart, other.

## Field Types

**Authentication**: username, password, password confirmation, email, email confirmation, username or email
**Names**: first name, last name, middle name, full name, organization name, gender
**Address**: country, city, state, address, postal code
**Contact**: phone, fax, url
**Search**: search query, search category
**Content**: comment text, comment title, about me text
**Buttons**: submit button, cancel button, reset button
**Verification**: captcha, honeypot, TOS confirmation, remember me checkbox, receive emails confirmation
**Security**: security question, security answer

Full list of 79 field type codes available in `data/config.json`.

## References

- Repository: https://github.com/HappyHackingSpace/dit
