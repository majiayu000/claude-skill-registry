---
name: data-architecture
description: Single source of truth patterns, facts.ts structure, type safety, and data helper functions. Use when working with project data or adding new facts.
---

# Data Architecture Skill

## Overview

This project uses a **single source of truth** pattern for all data. All personal information, project details, and configuration data is centralized in typed data files.

## Core Principle: Single Source of Truth

**Rule:** Never hardcode personal data. Always reference data files.

```typescript
// ❌ WRONG - Hardcoded data
const email = "me@omerakben.com";
const name = "Omer Akben";

// ✅ CORRECT - Reference data file
import { facts } from "@/data/facts";
const email = facts.contact.email;
const name = facts.personal.name;
```typescript

## Data File Structure

### Primary Data Files

```typescript
src/data/
├── facts.ts          # Personal info, skills, experience
├── projects.ts       # Project catalog with metadata
└── ...               # Other data files

src/config/
└── assistantFaq.ts   # FAQ and intent libraries
```typescript

## facts.ts Architecture

**Location:** `src/data/facts.ts`

### Structure Overview

```typescript
export const facts = {
  personal: {
    name: string;
    title: string;
    location: LocationInfo;
    bio: string;
    tagline: string;
  },

  contact: {
    email: string;
    phone: string;
    github: string;
    linkedin: string;
    calendly: string;
  },

  professional: {
    experience: Experience[];
    education: Education[];
    skills: Skill[];
    certifications: Certification[];
    workAuthorization: WorkAuthorization; // Added 2025-11-02
  },

  preferences: {
    timezone: string;
    availability: string;
  }
};
```typescript

### Type Definitions

```typescript
interface LocationInfo {
  city: string;
  state: string;
  country: string;
  timezone: string;
}

interface Experience {
  id: string;
  company: string;
  position: string;
  startDate: string;
  endDate: string | 'Present';
  description: string;
  technologies: string[];
  achievements: string[];
}

interface Skill {
  id: string;
  name: string;
  category: SkillCategory;
  level: SkillLevel;
  yearsOfExperience: number;
}

interface WorkAuthorization {
  status: string;
  officialTitle: string;
  sponsorshipRequired: boolean;
  employmentRestrictions: boolean;
  eligibleEmployers: string;
  proofDocument: string;
  summary: string;
}
```typescript

### Work Authorization Data

**Added:** November 2, 2025
**Location:** `facts.professional.workAuthorization`

```typescript
workAuthorization: {
  status: "U.S. Permanent Resident (Green Card)",
  officialTitle: "Lawful Permanent Resident (LPR)",
  sponsorshipRequired: false,
  employmentRestrictions: false,
  eligibleEmployers: "Any U.S. employer",
  proofDocument: "Form I-551 (Permanent Resident Card)",
  summary: "Authorized to work for any U.S. employer without restrictions or sponsorship requirements."
}
```typescript

**Usage:** AI agent references this when answering recruiter questions

## projects.ts Architecture

**Location:** `src/data/projects.ts`

### Structure

```typescript
export interface Project {
  id: string;
  slug: string;
  title: string;
  tagline: string;
  description: string;
  longDescription: string;
  technologies: Technology[];
  category: ProjectCategory;
  featured: boolean;
  showcase: boolean;
  liveUrl?: string;
  githubUrl?: string;
  imageUrl: string;
  metrics?: ProjectMetrics;
  testimonials?: Testimonial[];
}

export const projects: Project[] = [
  // Array of all projects
];
```typescript

### Helper Functions

```typescript
// Get projects by category
export function getProjectsByCategory(category: ProjectCategory): Project[] {
  return projects.filter(p => p.category === category);
}

// Get featured projects
export function getFeaturedProjects(): Project[] {
  return projects.filter(p => p.featured);
}

// Get project by slug
export function getProjectBySlug(slug: string): Project | undefined {
  return projects.find(p => p.slug === slug);
}

// Get all technologies used
export function getAllTechnologies(): Technology[] {
  const techSet = new Set<Technology>();
  projects.forEach(p => p.technologies.forEach(t => techSet.add(t)));
  return Array.from(techSet);
}
```typescript

### Usage Pattern

```typescript
import { projects, getFeaturedProjects, getProjectBySlug } from "@/data/projects";

// In component
const featured = getFeaturedProjects();
const project = getProjectBySlug(params.slug);
```typescript

## Type Safety Patterns

### 1. Const Assertions

```typescript
export const SKILL_CATEGORIES = [
  'Frontend',
  'Backend',
  'DevOps',
  'AI/ML',
] as const;

export type SkillCategory = typeof SKILL_CATEGORIES[number];
// Type is: 'Frontend' | 'Backend' | 'DevOps' | 'AI/ML'
```typescript

### Benefits

- Autocomplete in IDE
- Type checking
- Single source for both runtime and types

### 2. Branded Types

```typescript
type ProjectId = string & { readonly __brand: 'ProjectId' };
type UserId = string & { readonly __brand: 'UserId' };

// Prevents mixing up IDs
function getProject(id: ProjectId) { /* ... */ }
function getUser(id: UserId) { /* ... */ }

// TypeScript error: types are incompatible
const projectId: ProjectId = 'proj_123' as ProjectId;
const userId: UserId = 'user_456' as UserId;
getProject(userId); // ❌ Error!
```typescript

### 3. Discriminated Unions

```typescript
type Education =
  | { type: 'degree'; university: string; degree: string; major: string; }
  | { type: 'bootcamp'; program: string; completion: string; }
  | { type: 'certification'; name: string; issuer: string; };

function formatEducation(edu: Education): string {
  switch (edu.type) {
    case 'degree':
      return `${edu.degree} in ${edu.major} from ${edu.university}`;
    case 'bootcamp':
      return `${edu.program}`;
    case 'certification':
      return `${edu.name} by ${edu.issuer}`;
  }
}
```typescript

## Zod Validation Integration

### Schema Definitions

**Location:** `src/lib/agent-tools/schemas.ts`

```typescript
import { z } from 'zod';

export const ContactSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  company: z.string().optional(),
  message: z.string().min(10),
});

export type Contact = z.infer<typeof ContactSchema>;
```typescript

### Runtime Validation

```typescript
// API route handler
export async function POST(request: Request) {
  const body = await request.json();

  // Validate with Zod
  const result = ContactSchema.safeParse(body);

  if (!result.success) {
    return Response.json({
      success: false,
      error: result.error.format(),
    }, { status: 400 });
  }

  // Type-safe data access
  const { name, email, company, message } = result.data;
  // ...
}
```typescript

### Benefits of Zod

- Runtime validation
- Type inference from schemas
- Detailed error messages
- Parse, transform, and validate in one step

## AI Agent Data Integration

### Knowledge Base

**Location:** `src/lib/agent-knowledge-base.ts`

The AI agent consumes data from facts.ts:

```typescript
import { facts } from '@/data/facts';

export const agentKnowledgeBase = `
# Core Identity
Name: ${facts.personal.name}
Title: ${facts.personal.title}
Location: ${facts.personal.location.city}, ${facts.personal.location.state}

# Work Authorization
Status: ${facts.professional.workAuthorization.status}
Sponsorship Required: ${facts.professional.workAuthorization.sponsorshipRequired}

# Skills
${facts.professional.skills.map(s => `- ${s.name} (${s.level})`).join('\n')}

# Contact
Email: ${facts.contact.email}
LinkedIn: ${facts.contact.linkedin}
`;
```typescript

### Benefits

- Single source ensures consistency
- Updates to facts.ts automatically flow to AI
- No hardcoded data in agent prompts

### Tool Implementations

AI agent tools reference data files:

```typescript
// src/app/api/tools/get-contact/route.ts
import { facts } from '@/data/facts';

export async function POST() {
  return Response.json({
    success: true,
    data: {
      email: facts.contact.email,
      linkedin: facts.contact.linkedin,
      github: facts.contact.github,
      calendly: facts.contact.calendly,
    }
  });
}
```typescript

## Adding New Data

### Step 1: Update Type Definition

```typescript
// src/data/facts.ts
interface Facts {
  personal: PersonalInfo;
  contact: ContactInfo;
  professional: ProfessionalInfo;
  newSection: NewSectionType; // Add new section
}
```typescript

### Step 2: Add Data

```typescript
export const facts: Facts = {
  // ... existing data
  newSection: {
    field1: 'value1',
    field2: 'value2',
  }
};
```typescript

### Step 3: Update AI Knowledge Base

```typescript
// src/lib/agent-knowledge-base.ts
export const agentKnowledgeBase = `
...existing content...

# New Section
${facts.newSection.field1}
${facts.newSection.field2}
`;
```typescript

### Step 4: Add Tests

```typescript
// src/data/facts.test.ts
describe('facts.newSection', () => {
  it('should have required fields', () => {
    expect(facts.newSection.field1).toBeDefined();
    expect(facts.newSection.field2).toBeDefined();
  });
});
```typescript

## Data Validation Patterns

### 1. Email Validation

```typescript
import { z } from 'zod';

const EmailSchema = z.string()
  .email('Invalid email format')
  .toLowerCase()
  .trim();

// Usage
const email = EmailSchema.parse('USER@EXAMPLE.COM');
// Result: 'user@example.com'
```typescript

### 2. URL Validation

```typescript
const UrlSchema = z.string()
  .url('Invalid URL format')
  .refine(url => url.startsWith('https://'), {
    message: 'URL must use HTTPS'
  });
```typescript

### 3. Date Validation

```typescript
const DateSchema = z.string()
  .regex(/^\d{4}-\d{2}-\d{2}$/, 'Date must be YYYY-MM-DD')
  .refine(date => !isNaN(Date.parse(date)), {
    message: 'Invalid date'
  });
```typescript

### 4. Enum Validation

```typescript
const SkillLevelSchema = z.enum([
  'Beginner',
  'Intermediate',
  'Advanced',
  'Expert'
]);

type SkillLevel = z.infer<typeof SkillLevelSchema>;
```typescript

## Helper Function Patterns

### 1. Filter Helpers

```typescript
// Get items by property
export function getByCategory<T extends { category: string }>(
  items: T[],
  category: string
): T[] {
  return items.filter(item => item.category === category);
}

// Get items by multiple criteria
export function getByFilters<T>(
  items: T[],
  filters: Partial<T>
): T[] {
  return items.filter(item => {
    return Object.entries(filters).every(([key, value]) => {
      return item[key as keyof T] === value;
    });
  });
}
```typescript

### 2. Sort Helpers

```typescript
// Sort by date
export function sortByDate<T extends { date: string }>(
  items: T[],
  order: 'asc' | 'desc' = 'desc'
): T[] {
  return [...items].sort((a, b) => {
    const dateA = new Date(a.date).getTime();
    const dateB = new Date(b.date).getTime();
    return order === 'asc' ? dateA - dateB : dateB - dateA;
  });
}

// Sort by property
export function sortBy<T, K extends keyof T>(
  items: T[],
  key: K,
  order: 'asc' | 'desc' = 'asc'
): T[] {
  return [...items].sort((a, b) => {
    if (a[key] < b[key]) return order === 'asc' ? -1 : 1;
    if (a[key] > b[key]) return order === 'asc' ? 1 : -1;
    return 0;
  });
}
```typescript

### 3. Transform Helpers

```typescript
// Group by property
export function groupBy<T, K extends keyof T>(
  items: T[],
  key: K
): Record<string, T[]> {
  return items.reduce((acc, item) => {
    const groupKey = String(item[key]);
    if (!acc[groupKey]) acc[groupKey] = [];
    acc[groupKey].push(item);
    return acc;
  }, {} as Record<string, T[]>);
}

// Map to lookup object
export function toMap<T extends { id: string }>(
  items: T[]
): Record<string, T> {
  return items.reduce((acc, item) => {
    acc[item.id] = item;
    return acc;
  }, {} as Record<string, T>);
}
```typescript

## Testing Data Integrity

### Unit Tests

```typescript
// src/data/facts.test.ts
import { facts } from './facts';

describe('facts.ts data integrity', () => {
  it('should have valid email', () => {
    expect(facts.contact.email).toMatch(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/);
  });

  it('should have all required skills', () => {
    expect(facts.professional.skills.length).toBeGreaterThan(0);
    facts.professional.skills.forEach(skill => {
      expect(skill.name).toBeTruthy();
      expect(skill.category).toBeTruthy();
      expect(skill.level).toBeTruthy();
    });
  });

  it('should have valid work authorization', () => {
    const { workAuthorization } = facts.professional;
    expect(workAuthorization.status).toBeTruthy();
    expect(typeof workAuthorization.sponsorshipRequired).toBe('boolean');
    expect(typeof workAuthorization.employmentRestrictions).toBe('boolean');
  });
});
```typescript

### Zod Schema Tests

```typescript
import { ContactSchema } from './schemas';

describe('ContactSchema validation', () => {
  it('should accept valid contact', () => {
    const valid = {
      name: 'John Doe',
      email: 'john@example.com',
      message: 'Hello, this is a test message.',
    };

    const result = ContactSchema.safeParse(valid);
    expect(result.success).toBe(true);
  });

  it('should reject invalid email', () => {
    const invalid = {
      name: 'John Doe',
      email: 'not-an-email',
      message: 'Hello, world',
    };

    const result = ContactSchema.safeParse(invalid);
    expect(result.success).toBe(false);
  });
});
```typescript

## Common Mistakes

### Mistake 1: Hardcoding Data

```typescript
// ❌ WRONG
function Header() {
  return <h1>Omer Akben - AI Engineer</h1>;
}

// ✅ CORRECT
import { facts } from '@/data/facts';

function Header() {
  return <h1>{facts.personal.name} - {facts.personal.title}</h1>;
}
```typescript

### Mistake 2: Inconsistent Data Format

```typescript
// ❌ WRONG - Different date formats
{
  startDate: '2024-01-01',
  endDate: 'January 2024',
}

// ✅ CORRECT - Consistent ISO format
{
  startDate: '2024-01-01',
  endDate: '2024-01-31',
}
```typescript

### Mistake 3: No Validation

```typescript
// ❌ WRONG - Assumes data is valid
const user = JSON.parse(request.body);
saveUser(user);

// ✅ CORRECT - Validate first
const result = UserSchema.safeParse(JSON.parse(request.body));
if (result.success) {
  saveUser(result.data);
}
```typescript

## Data Update Checklist

When adding or updating data:

- [ ] Update type definitions first
- [ ] Add/modify data in facts.ts or projects.ts
- [ ] Update AI knowledge base if needed
- [ ] Add helper functions if beneficial
- [ ] Write unit tests for new data
- [ ] Verify AI agent responses still accurate
- [ ] Check that related tools still work
- [ ] Update documentation if structure changed

## Quick Reference

```typescript
// Import data
import { facts } from '@/data/facts';
import { projects, getProjectBySlug } from '@/data/projects';

// Access data
const email = facts.contact.email;
const name = facts.personal.name;
const project = getProjectBySlug('portfolio');

// Validate with Zod
const result = Schema.safeParse(data);
if (result.success) {
  // Use result.data
}

// Helper pattern
export function getFiltered<T>(items: T[], predicate: (item: T) => boolean): T[] {
  return items.filter(predicate);
}
```typescript

## Related Files

- `src/data/facts.ts` - Single source of truth for personal data
- `src/data/projects.ts` - Project catalog with helpers
- `src/lib/agent-knowledge-base.ts` - AI agent data integration
- `src/lib/agent-tools/schemas.ts` - Zod validation schemas
- `src/config/assistantFaq.ts` - FAQ and intent libraries
