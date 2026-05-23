---
name: Custom CRM Development
description: Building custom CRM systems with careful architecture planning, database design, core features including contact management, deal pipeline, activity tracking, and implementation patterns.
---

# Custom CRM Development

> **Current Level:** Advanced  
> **Domain:** CRM / Backend / Architecture

---

## Overview

Building a custom CRM system requires careful architecture planning. This guide covers database design, core features, and implementation patterns for building scalable CRM systems that meet specific business needs.

## CRM Architecture

```
Frontend (React) → API Gateway → Backend Services → Database
                                      ↓
                              External Integrations
```

**Core Modules:**
- Contact Management
- Company/Account Management
- Deal Pipeline
- Activity Tracking
- Task Management
- Email Integration
- Reporting

## Database Schema

```sql
-- contacts table
CREATE TABLE contacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID REFERENCES companies(id),
  
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  phone VARCHAR(50),
  mobile VARCHAR(50),
  
  title VARCHAR(100),
  department VARCHAR(100),
  
  address_line1 VARCHAR(255),
  address_line2 VARCHAR(255),
  city VARCHAR(100),
  state VARCHAR(100),
  postal_code VARCHAR(20),
  country VARCHAR(100),
  
  lead_source VARCHAR(50),
  lead_status VARCHAR(50),
  lifecycle_stage VARCHAR(50),
  
  owner_id UUID REFERENCES users(id),
  
  custom_fields JSONB,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_email (email),
  INDEX idx_company (company_id),
  INDEX idx_owner (owner_id),
  FULLTEXT idx_search (first_name, last_name, email)
);

-- companies table
CREATE TABLE companies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  name VARCHAR(255) NOT NULL,
  domain VARCHAR(255),
  industry VARCHAR(100),
  employee_count INTEGER,
  annual_revenue DECIMAL(15, 2),
  
  phone VARCHAR(50),
  website VARCHAR(255),
  
  address_line1 VARCHAR(255),
  address_line2 VARCHAR(255),
  city VARCHAR(100),
  state VARCHAR(100),
  postal_code VARCHAR(20),
  country VARCHAR(100),
  
  owner_id UUID REFERENCES users(id),
  
  custom_fields JSONB,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_domain (domain),
  INDEX idx_owner (owner_id),
  FULLTEXT idx_search (name, domain)
);

-- deals table
CREATE TABLE deals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  name VARCHAR(255) NOT NULL,
  amount DECIMAL(15, 2),
  currency VARCHAR(3) DEFAULT 'USD',
  
  stage VARCHAR(50) NOT NULL,
  probability INTEGER DEFAULT 0,
  
  expected_close_date DATE,
  actual_close_date DATE,
  
  contact_id UUID REFERENCES contacts(id),
  company_id UUID REFERENCES companies(id),
  owner_id UUID REFERENCES users(id),
  
  status VARCHAR(50) DEFAULT 'open',
  won_reason TEXT,
  lost_reason TEXT,
  
  custom_fields JSONB,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_stage (stage),
  INDEX idx_owner (owner_id),
  INDEX idx_status (status)
);

-- activities table
CREATE TABLE activities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  type VARCHAR(50) NOT NULL,
  subject VARCHAR(255),
  description TEXT,
  
  contact_id UUID REFERENCES contacts(id),
  company_id UUID REFERENCES companies(id),
  deal_id UUID REFERENCES deals(id),
  
  created_by UUID REFERENCES users(id),
  
  activity_date TIMESTAMP,
  duration INTEGER,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_contact (contact_id),
  INDEX idx_company (company_id),
  INDEX idx_deal (deal_id),
  INDEX idx_date (activity_date)
);

-- tasks table
CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  title VARCHAR(255) NOT NULL,
  description TEXT,
  
  status VARCHAR(50) DEFAULT 'pending',
  priority VARCHAR(50) DEFAULT 'normal',
  
  due_date TIMESTAMP,
  completed_at TIMESTAMP,
  
  contact_id UUID REFERENCES contacts(id),
  company_id UUID REFERENCES companies(id),
  deal_id UUID REFERENCES deals(id),
  
  assigned_to UUID REFERENCES users(id),
  created_by UUID REFERENCES users(id),
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_assigned (assigned_to),
  INDEX idx_status (status),
  INDEX idx_due_date (due_date)
);

-- custom_fields table
CREATE TABLE custom_fields (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  entity_type VARCHAR(50) NOT NULL,
  field_name VARCHAR(100) NOT NULL,
  field_type VARCHAR(50) NOT NULL,
  field_label VARCHAR(255) NOT NULL,
  
  options JSONB,
  required BOOLEAN DEFAULT FALSE,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(entity_type, field_name)
);
```

## Contact Management

```typescript
// services/contact.service.ts
export class ContactService {
  async createContact(data: CreateContactDto): Promise<Contact> {
    // Check for duplicates
    const existing = await this.findDuplicates(data.email);
    if (existing.length > 0) {
      throw new Error('Contact with this email already exists');
    }

    const contact = await db.contact.create({
      data: {
        ...data,
        lifecycleStage: 'lead'
      }
    });

    // Create activity
    await activityService.createActivity({
      type: 'contact_created',
      contactId: contact.id,
      createdBy: data.ownerId
    });

    return contact;
  }

  async updateContact(id: string, updates: Partial<Contact>): Promise<Contact> {
    const contact = await db.contact.update({
      where: { id },
      data: {
        ...updates,
        updatedAt: new Date()
      }
    });

    // Track changes
    await this.trackChanges(id, updates);

    return contact;
  }

  async findDuplicates(email: string): Promise<Contact[]> {
    return db.contact.findMany({
      where: {
        email: {
          equals: email,
          mode: 'insensitive'
        }
      }
    });
  }

  async mergeContacts(primaryId: string, duplicateId: string): Promise<Contact> {
    const [primary, duplicate] = await Promise.all([
      db.contact.findUnique({ where: { id: primaryId } }),
      db.contact.findUnique({ where: { id: duplicateId } })
    ]);

    if (!primary || !duplicate) {
      throw new Error('Contact not found');
    }

    // Merge data
    const merged = {
      ...primary,
      ...Object.fromEntries(
        Object.entries(duplicate).filter(([_, v]) => v != null && v !== '')
      )
    };

    // Update primary contact
    const updated = await db.contact.update({
      where: { id: primaryId },
      data: merged
    });

    // Transfer relationships
    await this.transferRelationships(duplicateId, primaryId);

    // Delete duplicate
    await db.contact.delete({ where: { id: duplicateId } });

    return updated;
  }

  private async transferRelationships(fromId: string, toId: string): Promise<void> {
    await Promise.all([
      db.activity.updateMany({
        where: { contactId: fromId },
        data: { contactId: toId }
      }),
      db.task.updateMany({
        where: { contactId: fromId },
        data: { contactId: toId }
      }),
      db.deal.updateMany({
        where: { contactId: fromId },
        data: { contactId: toId }
      })
    ]);
  }

  private async trackChanges(contactId: string, changes: any): Promise<void> {
    await db.contactHistory.create({
      data: {
        contactId,
        changes: JSON.stringify(changes),
        changedAt: new Date()
      }
    });
  }
}

interface CreateContactDto {
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  companyId?: string;
  ownerId: string;
  customFields?: Record<string, any>;
}
```

## Deal Pipeline

```typescript
// services/deal.service.ts
export class DealService {
  async createDeal(data: CreateDealDto): Promise<Deal> {
    const deal = await db.deal.create({
      data: {
        ...data,
        stage: 'qualification',
        probability: 10,
        status: 'open'
      }
    });

    // Create initial activity
    await activityService.createActivity({
      type: 'deal_created',
      dealId: deal.id,
      createdBy: data.ownerId
    });

    return deal;
  }

  async updateDealStage(dealId: string, stage: string): Promise<Deal> {
    const stageProbability = this.getStageProbability(stage);

    const deal = await db.deal.update({
      where: { id: dealId },
      data: {
        stage,
        probability: stageProbability,
        updatedAt: new Date()
      }
    });

    // Log stage change
    await activityService.createActivity({
      type: 'deal_stage_changed',
      dealId,
      description: `Stage changed to ${stage}`
    });

    return deal;
  }

  async closeDeal(dealId: string, won: boolean, reason?: string): Promise<Deal> {
    return db.deal.update({
      where: { id: dealId },
      data: {
        status: won ? 'won' : 'lost',
        actualCloseDate: new Date(),
        wonReason: won ? reason : undefined,
        lostReason: !won ? reason : undefined,
        probability: won ? 100 : 0
      }
    });
  }

  private getStageProbability(stage: string): number {
    const probabilities: Record<string, number> = {
      'qualification': 10,
      'needs_analysis': 20,
      'proposal': 50,
      'negotiation': 75,
      'closed_won': 100,
      'closed_lost': 0
    };

    return probabilities[stage] || 0;
  }
}

interface CreateDealDto {
  name: string;
  amount: number;
  contactId?: string;
  companyId?: string;
  ownerId: string;
  expectedCloseDate?: Date;
}
```

## API Design

```typescript
// routes/crm.routes.ts
import { Router } from 'express';

const router = Router();

// Contacts
router.get('/contacts', async (req, res) => {
  const contacts = await contactService.getContacts(req.query);
  res.json(contacts);
});

router.post('/contacts', async (req, res) => {
  const contact = await contactService.createContact(req.body);
  res.status(201).json(contact);
});

router.get('/contacts/:id', async (req, res) => {
  const contact = await contactService.getContact(req.params.id);
  res.json(contact);
});

router.patch('/contacts/:id', async (req, res) => {
  const contact = await contactService.updateContact(req.params.id, req.body);
  res.json(contact);
});

router.delete('/contacts/:id', async (req, res) => {
  await contactService.deleteContact(req.params.id);
  res.status(204).send();
});

// Deals
router.get('/deals', async (req, res) => {
  const deals = await dealService.getDeals(req.query);
  res.json(deals);
});

router.post('/deals', async (req, res) => {
  const deal = await dealService.createDeal(req.body);
  res.status(201).json(deal);
});

router.patch('/deals/:id/stage', async (req, res) => {
  const deal = await dealService.updateDealStage(req.params.id, req.body.stage);
  res.json(deal);
});

export default router;
```

## Best Practices

1. **Data Validation** - Validate all input data
2. **Duplicate Detection** - Implement duplicate detection
3. **Activity Tracking** - Track all important activities
4. **Custom Fields** - Support custom fields
5. **Permissions** - Implement role-based access
6. **API Design** - Follow REST principles
7. **Performance** - Optimize database queries
8. **Search** - Implement full-text search
9. **Audit Trail** - Track all changes
10. **Mobile** - Design mobile-friendly APIs

---

## Quick Start

### CRM Data Model

```typescript
interface Contact {
  id: string
  firstName: string
  lastName: string
  email: string
  company?: Company
  deals: Deal[]
  activities: Activity[]
}

interface Deal {
  id: string
  name: string
  value: number
  stage: string
  probability: number
  contact: Contact
  expectedCloseDate?: Date
}

interface Activity {
  id: string
  type: 'call' | 'email' | 'meeting' | 'note'
  subject: string
  description: string
  contact: Contact
  createdAt: Date
}
```

---

## Production Checklist

- [ ] **Architecture**: CRM architecture designed
- [ ] **Data Model**: Flexible data model
- [ ] **Contact Management**: Contact management
- [ ] **Deal Pipeline**: Deal pipeline
- [ ] **Activity Tracking**: Activity tracking
- [ ] **Custom Fields**: Support custom fields
- [ ] **Search**: Full-text search
- [ ] **Reporting**: CRM reports
- [ ] **Integration**: External integrations
- [ ] **Security**: Access control
- [ ] **Documentation**: Document CRM structure
- [ ] **Testing**: Test CRM functionality

---

## Anti-patterns

### ❌ Don't: Rigid Schema

```typescript
// ❌ Bad - Fixed schema
interface Contact {
  field1: string
  field2: string
  // Can't add custom fields!
}
```

```typescript
// ✅ Good - Flexible schema
interface Contact {
  id: string
  customFields: Record<string, any>  // Flexible
}
```

### ❌ Don't: No Data Validation

```typescript
// ❌ Bad - No validation
await db.contacts.create({ data: contact })
// Invalid data possible!
```

```typescript
// ✅ Good - Validate
const validated = validateContact(contact)
await db.contacts.create({ data: validated })
```

---

## Integration Points

- **Contact Management** (`32-crm-integration/contact-management/`) - Contact patterns
- **Sales Pipeline** (`32-crm-integration/sales-pipeline/`) - Pipeline patterns
- **Lead Management** (`32-crm-integration/lead-management/`) - Lead patterns

---

## Further Reading

- [CRM Best Practices](https://www.salesforce.com/resources/articles/crm-best-practices/)
- [CRM Architecture](https://www.hubspot.com/crm)

## Resources
- [Database Design](https://www.postgresql.org/docs/current/ddl.html)
- [REST API Design](https://restfulapi.net/)
