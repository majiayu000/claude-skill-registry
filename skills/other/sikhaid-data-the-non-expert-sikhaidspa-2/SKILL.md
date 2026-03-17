---
name: sikhaid-data
description: Use when working with data, state management, Firebase, or Firestore in SikhAid project. Covers Svelte stores, data flow patterns, Firebase initialization, Firestore CRUD operations, and data types.
allowed-tools: Read, Edit, Write
---

# SikhAid Data & State Management

## State Management Architecture

### Svelte Stores
**Pattern:** Reactive stores for client-side state management

**Store Types Used:**
- `writable()` - Read/write stores for component state
- No derived stores currently
- No custom stores (plain writable stores)

**Store Locations:**
```
src/lib/stores/
├── donation.ts       # Donation amount state
├── contact.ts        # Contact form submissions
├── volunteering.ts   # Volunteer form submissions
└── csr.ts            # CSR partnership submissions
```

## Store Patterns

### 1. Donation Store
**File:** `src/lib/stores/donation.ts`

**Purpose:** Manage selected donation amount across components

```typescript
import { writable } from 'svelte/store';

export const selectedAmount = writable<number>(0);

export function setDonationAmount(amount: number) {
  selectedAmount.set(amount);

  // Side effect: scroll to payment form
  setTimeout(() => {
    const paymentSection = document.getElementById('payment-form');
    paymentSection?.scrollIntoView({ behavior: 'smooth' });
  }, 100);
}
```

**Usage:**
```svelte
<script lang="ts">
  import { selectedAmount, setDonationAmount } from '$lib/stores/donation';

  // Read value with $ prefix
  $: amount = $selectedAmount;

  // Write value
  function selectAmount(value: number) {
    setDonationAmount(value);
  }
</script>

<div>Selected: ₹{$selectedAmount}</div>
<button on:click={() => selectAmount(1000)}>₹1,000</button>
```

### 2. Contact Submissions Store
**File:** `src/lib/stores/contact.ts`

**Purpose:** Store contact form submissions (in-memory and Firestore)

```typescript
import { writable } from 'svelte/store';

export interface ContactSubmission {
  name: string;
  email: string;
  phone: string;
  subject: string;
  message: string;
  timestamp: number;
}

export const contactSubmissions = writable<ContactSubmission[]>([]);

export function addContactSubmission(submission: ContactSubmission) {
  contactSubmissions.update(submissions => {
    return [...submissions, submission];
  });
}
```

### 3. Volunteering Store
**File:** `src/lib/stores/volunteering.ts`

**Purpose:** Store volunteer applications

```typescript
export interface VolunteerSubmission {
  fullName: string;
  email: string;
  mobile: string;
  gender: string;
  address: string;
  opportunity: string;
  durationMonths: number;
  durationYears: number;
  startDate: string;
  about: string;
  timestamp: number;
}

export const volunteerSubmissions = writable<VolunteerSubmission[]>([]);
```

### 4. CSR Store
**File:** `src/lib/stores/csr.ts`

**Purpose:** Store CSR partnership inquiries

```typescript
export interface CSRSubmission {
  companyName: string;
  contactPerson: string;
  email: string;
  phone: string;
  companySize: string;
  interests: string[];
  message: string;
  timestamp: number;
}

export const csrSubmissions = writable<CSRSubmission[]>([]);
```

## Data Flow Pattern

### Standard Form Submission Flow
```
1. User fills form
   ↓
2. Form validation
   ↓
3. Create submission object with timestamp
   ↓
4. Update Svelte store (addSubmission)
   ↓
5. Write to Firestore (addToFirestore)
   ↓
6. Show success/error feedback
   ↓
7. Reset form (optional)
```

### Example Flow Implementation
```svelte
<script lang="ts">
  import { addContactSubmission } from '$lib/stores/contact';
  import { addContactToFirestore } from '$lib/firestore';

  let formData = { name: '', email: '', phone: '', subject: '', message: '' };
  let isSubmitting = false;
  let successMessage = '';
  let errorMessage = '';

  async function handleSubmit() {
    // 1. Validate
    if (!validateForm()) return;

    isSubmitting = true;
    errorMessage = '';

    try {
      // 2. Create submission object
      const submission = {
        ...formData,
        timestamp: Date.now()
      };

      // 3. Update store
      addContactSubmission(submission);

      // 4. Write to Firestore
      await addContactToFirestore(submission);

      // 5. Success feedback
      successMessage = 'Submission received!';
      formData = { name: '', email: '', phone: '', subject: '', message: '' };
    } catch (error) {
      // 6. Error feedback
      errorMessage = 'Submission failed. Please try again.';
      console.error('❌ Error:', error);
    } finally {
      isSubmitting = false;
    }
  }
</script>
```

## Firebase Integration

### Firebase Initialization
**File:** `src/lib/firebase.ts`

```typescript
import { initializeApp, type FirebaseApp } from 'firebase/app';
import { getFirestore, type Firestore } from 'firebase/firestore';
import { getAuth, type Auth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
};

let app: FirebaseApp | null = null;
let db: Firestore | null = null;
let auth: Auth | null = null;

// Browser-only initialization
if (typeof window !== 'undefined') {
  try {
    app = initializeApp(firebaseConfig);
    db = getFirestore(app);
    auth = getAuth(app);
    console.log('✅ Firebase initialized successfully');
  } catch (error) {
    console.error('❌ Firebase initialization error:', error);
  }
}

export { app, db, auth };
```

**Key Points:**
- Browser-only initialization (`typeof window !== 'undefined'`)
- Environment variables for configuration
- Error handling with console logging
- Exports app, db, and auth instances

## Firestore Operations

### Collections Structure
```
Firestore Database
├── contact_submissions/
│   └── [auto-generated-id]/
│       ├── name: string
│       ├── email: string
│       ├── phone: string
│       ├── subject: string
│       ├── message: string
│       ├── status: 'new' | 'read' | 'resolved'
│       └── timestamp: Firestore Timestamp
│
├── volunteer_submissions/
│   └── [auto-generated-id]/
│       ├── fullName: string
│       ├── email: string
│       ├── mobile: string
│       ├── opportunity: string
│       ├── status: 'new' | 'read' | 'resolved'
│       └── ...
│
└── csr_submissions/
    └── [auto-generated-id]/
        ├── companyName: string
        ├── email: string
        ├── status: 'new' | 'read' | 'resolved'
        └── ...
```

### Firestore Functions
**File:** `src/lib/firestore.ts`

#### Add Contact Submission
```typescript
import { collection, addDoc, Timestamp } from 'firebase/firestore';
import { db } from './firebase';
import type { ContactSubmission } from './stores/contact';

export async function addContactToFirestore(
  submission: ContactSubmission
): Promise<string> {
  if (!db) throw new Error('Firestore not initialized');

  try {
    const docRef = await addDoc(collection(db, 'contact_submissions'), {
      ...submission,
      status: 'new',
      timestamp: Timestamp.fromMillis(submission.timestamp)
    });

    console.log('✅ Contact added to Firestore:', docRef.id);
    return docRef.id;
  } catch (error) {
    console.error('❌ Error adding contact:', error);
    throw error;
  }
}
```

#### Get All Submissions
```typescript
import { collection, getDocs, query, orderBy } from 'firebase/firestore';

export interface FirestoreContactSubmission extends ContactSubmission {
  id?: string;
  status: 'new' | 'read' | 'resolved';
  firestoreTimestamp?: Timestamp;
}

export async function getContactSubmissions(): Promise<FirestoreContactSubmission[]> {
  if (!db) throw new Error('Firestore not initialized');

  try {
    const q = query(
      collection(db, 'contact_submissions'),
      orderBy('timestamp', 'desc')
    );

    const querySnapshot = await getDocs(q);
    const submissions: FirestoreContactSubmission[] = [];

    querySnapshot.forEach((doc) => {
      submissions.push({
        id: doc.id,
        ...doc.data() as FirestoreContactSubmission
      });
    });

    console.log(`📊 Fetched ${submissions.length} contact submissions`);
    return submissions;
  } catch (error) {
    console.error('❌ Error fetching submissions:', error);
    throw error;
  }
}
```

#### Update Submission Status
```typescript
import { doc, updateDoc } from 'firebase/firestore';

export async function updateSubmissionStatus(
  collectionName: string,
  documentId: string,
  status: 'new' | 'read' | 'resolved'
): Promise<void> {
  if (!db) throw new Error('Firestore not initialized');

  try {
    const docRef = doc(db, collectionName, documentId);
    await updateDoc(docRef, { status });

    console.log(`✅ Updated ${documentId} status to ${status}`);
  } catch (error) {
    console.error('❌ Error updating status:', error);
    throw error;
  }
}
```

#### Add Volunteer Submission
```typescript
export async function addVolunteerToFirestore(
  submission: VolunteerSubmission
): Promise<string> {
  if (!db) throw new Error('Firestore not initialized');

  try {
    const docRef = await addDoc(collection(db, 'volunteer_submissions'), {
      ...submission,
      status: 'new',
      timestamp: Timestamp.fromMillis(submission.timestamp)
    });

    console.log('✅ Volunteer added:', docRef.id);
    return docRef.id;
  } catch (error) {
    console.error('❌ Error adding volunteer:', error);
    throw error;
  }
}
```

#### Get Volunteer Submissions
```typescript
export async function getVolunteerSubmissions(): Promise<FirestoreVolunteerSubmission[]> {
  if (!db) throw new Error('Firestore not initialized');

  try {
    const q = query(
      collection(db, 'volunteer_submissions'),
      orderBy('timestamp', 'desc')
    );

    const querySnapshot = await getDocs(q);
    const submissions: FirestoreVolunteerSubmission[] = [];

    querySnapshot.forEach((doc) => {
      submissions.push({
        id: doc.id,
        ...doc.data() as FirestoreVolunteerSubmission
      });
    });

    return submissions;
  } catch (error) {
    console.error('❌ Error fetching volunteers:', error);
    throw error;
  }
}
```

### CSR Functions (Similar Pattern)
- `addCSRToFirestore()` - Add CSR submission
- `getCSRSubmissions()` - Get all CSR submissions
- Both follow same pattern as contact/volunteer

## Static Data Management

### Campaigns Data
**File:** `src/lib/data/campaigns.js`

**Structure:**
```javascript
export const campaigns = [
  {
    slug: 'langar-aid',
    title: 'Langar Aid',
    subtitle: 'Free Meals for All',
    shortDescription: 'Serving nutritious meals...',
    fullDescription: 'Detailed description...',
    image: '/images/campaign.jpg',
    category: 'hunger-relief',
    status: 'ongoing', // 'ongoing' | 'completed' | 'seasonal'
    impactStats: [
      { label: 'Meals Served', value: '100,000+', icon: 'mdi:food' }
    ],
    howItWorks: [
      { step: 1, title: 'Step Title', description: 'Step description' }
    ],
    gallery: [
      { src: '/images/gallery1.jpg', alt: 'Description' }
    ]
  },
  // More campaigns...
];
```

**Usage:**
```svelte
<script lang="ts">
  import { campaigns } from '$lib/data/campaigns';
  import type { Campaign } from '$lib/types/campaign';

  // Filter campaigns
  $: ongoingCampaigns = campaigns.filter(c => c.status === 'ongoing');

  // Find by slug
  $: campaign = campaigns.find(c => c.slug === 'langar-aid');
</script>

{#each ongoingCampaigns as campaign}
  <div>{campaign.title}</div>
{/each}
```

### Blog Data
**File:** `src/lib/data/blogs.js`

**Structure:**
```javascript
export const blogs = [
  {
    slug: 'post-slug',
    title: 'Blog Post Title',
    excerpt: 'Short excerpt...',
    content: 'Full blog content...',
    author: 'Author Name',
    date: '2024-01-15',
    image: '/images/blog.jpg',
    category: 'community'
  },
  // More blog posts...
];
```

## TypeScript Types & Interfaces

### Campaign Types
**File:** `src/lib/types/campaign.ts`

```typescript
export interface Campaign {
  slug: string;
  title: string;
  subtitle: string;
  shortDescription: string;
  fullDescription: string;
  image: string;
  category: string;
  status: 'ongoing' | 'completed' | 'seasonal';
  impactStats: ImpactStat[];
  howItWorks: HowItWorksStep[];
  gallery: GalleryImage[];
}

export interface ImpactStat {
  label: string;
  value: string;
  icon: string;
}

export interface HowItWorksStep {
  step: number;
  title: string;
  description: string;
}

export interface GalleryImage {
  src: string;
  alt: string;
}
```

### Store Types (Defined in store files)

```typescript
// Contact
export interface ContactSubmission {
  name: string;
  email: string;
  phone: string;
  subject: string;
  message: string;
  timestamp: number;
}

// Volunteer
export interface VolunteerSubmission {
  fullName: string;
  email: string;
  mobile: string;
  gender: string;
  address: string;
  opportunity: string;
  durationMonths: number;
  durationYears: number;
  startDate: string;
  about: string;
  timestamp: number;
}

// CSR
export interface CSRSubmission {
  companyName: string;
  contactPerson: string;
  email: string;
  phone: string;
  companySize: string;
  interests: string[];
  message: string;
  timestamp: number;
}
```

### Firestore Extended Types

```typescript
import type { Timestamp } from 'firebase/firestore';

export interface FirestoreContactSubmission extends ContactSubmission {
  id?: string;
  status: 'new' | 'read' | 'resolved';
  firestoreTimestamp?: Timestamp;
}

export interface FirestoreVolunteerSubmission extends VolunteerSubmission {
  id?: string;
  status: 'new' | 'read' | 'resolved';
  firestoreTimestamp?: Timestamp;
}

export interface FirestoreCSRSubmission extends CSRSubmission {
  id?: string;
  status: 'new' | 'read' | 'resolved';
  firestoreTimestamp?: Timestamp;
}
```

## Data Loading in Components

### Loading Firestore Data (Admin Panel)
```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  import {
    getContactSubmissions,
    type FirestoreContactSubmission
  } from '$lib/firestore';

  let submissions: FirestoreContactSubmission[] = [];
  let isLoading = true;
  let error = '';

  onMount(async () => {
    try {
      submissions = await getContactSubmissions();
      isLoading = false;
    } catch (err) {
      error = 'Failed to load submissions';
      isLoading = false;
    }
  });
</script>

{#if isLoading}
  <div>Loading...</div>
{:else if error}
  <div class="text-red-500">{error}</div>
{:else}
  {#each submissions as submission}
    <div>{submission.name}</div>
  {/each}
{/if}
```

### Using Static Data
```svelte
<script lang="ts">
  import { campaigns } from '$lib/data/campaigns';

  // No onMount needed - data is already available
  $: featuredCampaigns = campaigns.filter(c => c.featured);
</script>

{#each featuredCampaigns as campaign}
  <div>{campaign.title}</div>
{/each}
```

## Store Subscription Patterns

### Auto-subscribing with $ Prefix
```svelte
<script lang="ts">
  import { selectedAmount } from '$lib/stores/donation';

  // Automatic subscription
  $: amount = $selectedAmount;
</script>

<div>Amount: ₹{$selectedAmount}</div>
```

### Manual Subscribe/Unsubscribe
```svelte
<script lang="ts">
  import { onDestroy } from 'svelte';
  import { contactSubmissions } from '$lib/stores/contact';

  let submissions = [];

  const unsubscribe = contactSubmissions.subscribe(value => {
    submissions = value;
  });

  onDestroy(() => {
    unsubscribe();
  });
</script>
```

## Common Data Patterns

### Filtering Arrays
```svelte
<script lang="ts">
  import { campaigns } from '$lib/data/campaigns';

  let selectedCategory = 'all';

  $: filteredCampaigns = selectedCategory === 'all'
    ? campaigns
    : campaigns.filter(c => c.category === selectedCategory);
</script>
```

### Searching
```svelte
<script lang="ts">
  let searchQuery = '';
  let campaigns = [...];

  $: searchResults = campaigns.filter(campaign =>
    campaign.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    campaign.shortDescription.toLowerCase().includes(searchQuery.toLowerCase())
  );
</script>
```

### Sorting
```svelte
<script lang="ts">
  let submissions = [...];
  let sortBy = 'timestamp'; // 'timestamp' | 'name' | 'status'

  $: sortedSubmissions = [...submissions].sort((a, b) => {
    if (sortBy === 'timestamp') {
      return b.timestamp - a.timestamp; // Newest first
    }
    if (sortBy === 'name') {
      return a.name.localeCompare(b.name);
    }
    return 0;
  });
</script>
```

## When to Use This Skill
- Working with Svelte stores
- Integrating Firebase/Firestore
- Managing form submissions
- Loading or filtering data
- Creating new data types
- Implementing CRUD operations
- Understanding data flow in the app

## Related Skills
- `sikhaid-forms` - Form submission patterns
- `sikhaid-components` - Component state management
- `sikhaid-overview` - Firebase configuration
