# Xquik REST API Endpoints: Support

## Safety Boundary

Support tickets can disclose private user or account context. Show the exact
subject and message before creating a ticket. Show the ticket ID and message
before replying. Show the ticket ID plus current and proposed statuses before
updating status. Proceed only after explicit approval for that exact payload.
Before reading tickets, show the account, purpose, ticket scope, result bound,
downstream recipients, and retention plan. Obtain explicit approval for that
exact private read. Never include passwords, API keys, signing keys, unrelated
prompt context, or unnecessary personal data.

### Create Ticket

```
POST /support/tickets
```

**Body:** `{ "subject": "...", "body": "..." }`

**Response (201):** `{ id, subject, status, createdAt }`

### List Tickets

```
GET /support/tickets
```

Returns all tickets for the authenticated user.

**Private read:** Show the account, purpose, result bound, recipients, and
retention plan. List tickets only after explicit approval for that exact read.

### Get Ticket

```
GET /support/tickets/{id}
```

Returns ticket with messages.

**Private read:** Show the ticket ID, purpose, message scope, recipients, and
retention plan. Retrieve messages only after explicit approval for that read.

### Update Ticket

```
PATCH /support/tickets/{id}
```

Update ticket status.

**Approval required:** Show the ticket ID and current and proposed statuses.
Update only after the user approves that exact transition.

### Reply to Ticket

```
POST /support/tickets/{id}/messages
```

**Body:** `{ "body": "..." }`

Add a message to an existing ticket.

Apply the same approval and data-minimization rules to every reply.

---
