---
name: sikhaid-forms
description: Use when creating or modifying forms in SikhAid project. Covers form patterns, validation logic, submission workflows, Firestore integration, error handling, and success feedback.
allowed-tools: Read, Edit, Write
---

# SikhAid Form Patterns

## Form Types in Project

### 1. Contact Form
**Location:** `src/routes/contact/+page.svelte`
**Purpose:** General inquiries and contact requests
**Firestore Collection:** `contact_submissions`

### 2. Volunteer Form
**Location:** `src/routes/volunteering/+page.svelte`
**Purpose:** Volunteer registration and applications
**Firestore Collection:** `volunteer_submissions`

### 3. CSR Partnership Form
**Location:** `src/routes/csr/+page.svelte`
**Purpose:** Corporate Social Responsibility partnership inquiries
**Firestore Collection:** `csr_submissions`

### 4. Donation/Payment Form
**Location:** `src/lib/components/PaymentForm.svelte`
**Purpose:** Donation processing with Razorpay
**Integration:** Razorpay payment gateway

## Standard Form Pattern

### Complete Form Structure
```svelte
<script lang="ts">
  import { addContactSubmission } from '$lib/stores/contact';
  import { addContactToFirestore } from '$lib/firestore';

  // 1. Form data state
  let formData = {
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: ''
  };

  // 2. UI state
  let isSubmitting = false;
  let successMessage = '';
  let errorMessage = '';

  // 3. Field errors
  let errors = {
    name: '',
    email: '',
    phone: ''
  };

  // 4. Validation functions
  function validateName(): boolean {
    if (formData.name.trim().length < 2) {
      errors.name = 'Name must be at least 2 characters';
      return false;
    }
    errors.name = '';
    return true;
  }

  function validateEmail(): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      errors.email = 'Please enter a valid email';
      return false;
    }
    errors.email = '';
    return true;
  }

  function validatePhone(): boolean {
    const phoneRegex = /^[6-9]\d{9}$/;
    if (!phoneRegex.test(formData.phone)) {
      errors.phone = 'Please enter a valid 10-digit mobile number';
      return false;
    }
    errors.phone = '';
    return true;
  }

  function validateForm(): boolean {
    const nameValid = validateName();
    const emailValid = validateEmail();
    const phoneValid = validatePhone();
    return nameValid && emailValid && phoneValid;
  }

  // 5. Submit handler
  async function handleSubmit() {
    // Clear previous messages
    successMessage = '';
    errorMessage = '';

    // Validate
    if (!validateForm()) {
      errorMessage = 'Please fix the errors above';
      return;
    }

    // Start submission
    isSubmitting = true;

    try {
      // Create submission object
      const submission = {
        ...formData,
        timestamp: Date.now()
      };

      // Update store
      addContactSubmission(submission);

      // Save to Firestore
      const docId = await addContactToFirestore(submission);
      console.log('✅ Submission saved:', docId);

      // Success feedback
      successMessage = 'Thank you! We will get back to you soon.';

      // Reset form
      formData = {
        name: '',
        email: '',
        phone: '',
        subject: '',
        message: ''
      };
    } catch (error) {
      console.error('❌ Submission error:', error);
      errorMessage = 'Submission failed. Please try again.';
    } finally {
      isSubmitting = false;
    }
  }
</script>

<!-- 6. Form markup -->
<form on:submit|preventDefault={handleSubmit} class="max-w-lg mx-auto">
  <!-- Name field -->
  <div class="mb-4">
    <label for="name" class="block text-gray-700 font-semibold mb-2">
      Full Name *
    </label>
    <input
      id="name"
      type="text"
      bind:value={formData.name}
      on:blur={validateName}
      class="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-custom"
      class:border-red-500={errors.name}
      required
    />
    {#if errors.name}
      <p class="text-red-500 text-sm mt-1">{errors.name}</p>
    {/if}
  </div>

  <!-- Email field -->
  <div class="mb-4">
    <label for="email" class="block text-gray-700 font-semibold mb-2">
      Email *
    </label>
    <input
      id="email"
      type="email"
      bind:value={formData.email}
      on:blur={validateEmail}
      class="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-custom"
      class:border-red-500={errors.email}
      required
    />
    {#if errors.email}
      <p class="text-red-500 text-sm mt-1">{errors.email}</p>
    {/if}
  </div>

  <!-- Phone field -->
  <div class="mb-4">
    <label for="phone" class="block text-gray-700 font-semibold mb-2">
      Phone *
    </label>
    <input
      id="phone"
      type="tel"
      bind:value={formData.phone}
      on:blur={validatePhone}
      maxlength="10"
      class="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-custom"
      class:border-red-500={errors.phone}
      required
    />
    {#if errors.phone}
      <p class="text-red-500 text-sm mt-1">{errors.phone}</p>
    {/if}
  </div>

  <!-- Subject field -->
  <div class="mb-4">
    <label for="subject" class="block text-gray-700 font-semibold mb-2">
      Subject *
    </label>
    <input
      id="subject"
      type="text"
      bind:value={formData.subject}
      class="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-custom"
      required
    />
  </div>

  <!-- Message field -->
  <div class="mb-6">
    <label for="message" class="block text-gray-700 font-semibold mb-2">
      Message *
    </label>
    <textarea
      id="message"
      bind:value={formData.message}
      rows="5"
      class="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-custom resize-none"
      required
    ></textarea>
  </div>

  <!-- Success message -->
  {#if successMessage}
    <div class="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">
      {successMessage}
    </div>
  {/if}

  <!-- Error message -->
  {#if errorMessage}
    <div class="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
      {errorMessage}
    </div>
  {/if}

  <!-- Submit button -->
  <button
    type="submit"
    disabled={isSubmitting}
    class="w-full bg-orange-custom hover:bg-orange-dark text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-300"
    class:opacity-50={isSubmitting}
    class:cursor-not-allowed={isSubmitting}
  >
    {#if isSubmitting}
      Submitting...
    {:else}
      Submit
    {/if}
  </button>
</form>
```

## Validation Patterns

### Email Validation
```typescript
function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return false;
  }
  return true;
}

// With error message
function validateEmailWithError(email: string): { valid: boolean; error: string } {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email.trim()) {
    return { valid: false, error: 'Email is required' };
  }
  if (!emailRegex.test(email)) {
    return { valid: false, error: 'Please enter a valid email address' };
  }
  return { valid: true, error: '' };
}
```

### Phone Validation (Indian Mobile)
```typescript
function validatePhone(phone: string): boolean {
  // Indian mobile: 10 digits, starts with 6-9
  const phoneRegex = /^[6-9]\d{9}$/;
  return phoneRegex.test(phone);
}

// With detailed errors
function validatePhoneWithError(phone: string): { valid: boolean; error: string } {
  if (!phone.trim()) {
    return { valid: false, error: 'Phone number is required' };
  }
  if (!/^\d+$/.test(phone)) {
    return { valid: false, error: 'Phone must contain only digits' };
  }
  if (phone.length !== 10) {
    return { valid: false, error: 'Phone must be exactly 10 digits' };
  }
  if (!/^[6-9]/.test(phone)) {
    return { valid: false, error: 'Phone must start with 6, 7, 8, or 9' };
  }
  return { valid: true, error: '' };
}
```

### Name Validation
```typescript
function validateName(name: string): boolean {
  return name.trim().length >= 2;
}

// With error message
function validateNameWithError(name: string): { valid: boolean; error: string } {
  const trimmed = name.trim();
  if (!trimmed) {
    return { valid: false, error: 'Name is required' };
  }
  if (trimmed.length < 2) {
    return { valid: false, error: 'Name must be at least 2 characters' };
  }
  if (trimmed.length > 100) {
    return { valid: false, error: 'Name is too long (max 100 characters)' };
  }
  return { valid: true, error: '' };
}
```

### Required Field Validation
```typescript
function validateRequired(value: string, fieldName: string): { valid: boolean; error: string } {
  if (!value.trim()) {
    return { valid: false, error: `${fieldName} is required` };
  }
  return { valid: true, error: '' };
}
```

### Dropdown/Select Validation
```typescript
function validateSelect(value: string, fieldName: string): { valid: boolean; error: string } {
  if (!value || value === '') {
    return { valid: false, error: `Please select a ${fieldName}` };
  }
  return { valid: true, error: '' };
}
```

### Multi-Select Validation
```typescript
function validateMultiSelect(values: string[], fieldName: string): { valid: boolean; error: string } {
  if (values.length === 0) {
    return { valid: false, error: `Please select at least one ${fieldName}` };
  }
  return { valid: true, error: '' };
}
```

## Form Input Components

### Text Input with Validation
```svelte
<div class="mb-4">
  <label for={fieldId} class="block text-gray-700 font-semibold mb-2">
    {label} {#if required}*{/if}
  </label>
  <input
    id={fieldId}
    type="text"
    bind:value={value}
    on:blur={validateField}
    class="w-full px-4 py-3 border border-gray-300 rounded-lg
           focus:outline-none focus:ring-2 focus:ring-orange-custom focus:border-transparent
           transition-all"
    class:border-red-500={error}
    class:focus:ring-red-500={error}
    placeholder={placeholder}
    required={required}
  />
  {#if error}
    <p class="text-red-500 text-sm mt-1">{error}</p>
  {/if}
</div>
```

### Email Input
```svelte
<div class="mb-4">
  <label for="email" class="block text-gray-700 font-semibold mb-2">
    Email Address *
  </label>
  <input
    id="email"
    type="email"
    bind:value={formData.email}
    on:blur={validateEmail}
    class="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-custom"
    class:border-red-500={errors.email}
    placeholder="your@email.com"
    required
  />
  {#if errors.email}
    <p class="text-red-500 text-sm mt-1">{errors.email}</p>
  {/if}
</div>
```

### Phone Input
```svelte
<div class="mb-4">
  <label for="phone" class="block text-gray-700 font-semibold mb-2">
    Mobile Number *
  </label>
  <div class="flex">
    <span class="inline-flex items-center px-4 bg-gray-100 border border-r-0 border-gray-300 rounded-l-lg text-gray-600">
      +91
    </span>
    <input
      id="phone"
      type="tel"
      bind:value={formData.phone}
      on:blur={validatePhone}
      on:input={(e) => {
        // Only allow digits
        e.target.value = e.target.value.replace(/\D/g, '');
      }}
      maxlength="10"
      class="flex-1 px-4 py-3 border border-gray-300 rounded-r-lg focus:outline-none focus:ring-2 focus:ring-orange-custom"
      class:border-red-500={errors.phone}
      placeholder="9876543210"
      required
    />
  </div>
  {#if errors.phone}
    <p class="text-red-500 text-sm mt-1">{errors.phone}</p>
  {/if}
</div>
```

### Textarea
```svelte
<div class="mb-6">
  <label for="message" class="block text-gray-700 font-semibold mb-2">
    Message *
  </label>
  <textarea
    id="message"
    bind:value={formData.message}
    rows="5"
    class="w-full px-4 py-3 border border-gray-300 rounded-lg
           focus:outline-none focus:ring-2 focus:ring-orange-custom focus:border-transparent
           resize-none"
    placeholder="Tell us more..."
    required
  ></textarea>
  <p class="text-sm text-gray-500 mt-1">
    {formData.message.length} / 500 characters
  </p>
</div>
```

### Select Dropdown
```svelte
<div class="mb-4">
  <label for="opportunity" class="block text-gray-700 font-semibold mb-2">
    Volunteer Opportunity *
  </label>
  <select
    id="opportunity"
    bind:value={formData.opportunity}
    class="w-full px-4 py-3 border border-gray-300 rounded-lg
           focus:outline-none focus:ring-2 focus:ring-orange-custom
           bg-white"
    required
  >
    <option value="">Select an opportunity</option>
    <option value="teaching">Teaching</option>
    <option value="food-distribution">Food Distribution</option>
    <option value="healthcare">Healthcare Support</option>
    <option value="community">Community Outreach</option>
  </select>
</div>
```

### Radio Buttons
```svelte
<div class="mb-4">
  <label class="block text-gray-700 font-semibold mb-3">
    Gender *
  </label>
  <div class="flex gap-4">
    <label class="inline-flex items-center cursor-pointer">
      <input
        type="radio"
        bind:group={formData.gender}
        value="Male"
        class="w-4 h-4 text-orange-custom focus:ring-orange-custom"
        required
      />
      <span class="ml-2">Male</span>
    </label>
    <label class="inline-flex items-center cursor-pointer">
      <input
        type="radio"
        bind:group={formData.gender}
        value="Female"
        class="w-4 h-4 text-orange-custom focus:ring-orange-custom"
      />
      <span class="ml-2">Female</span>
    </label>
    <label class="inline-flex items-center cursor-pointer">
      <input
        type="radio"
        bind:group={formData.gender}
        value="Other"
        class="w-4 h-4 text-orange-custom focus:ring-orange-custom"
      />
      <span class="ml-2">Other</span>
    </label>
  </div>
</div>
```

### Checkboxes (Multi-Select)
```svelte
<div class="mb-4">
  <label class="block text-gray-700 font-semibold mb-3">
    Areas of Interest *
  </label>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
    {#each interestOptions as option}
      <label class="inline-flex items-center cursor-pointer">
        <input
          type="checkbox"
          bind:group={formData.interests}
          value={option}
          class="w-4 h-4 text-orange-custom rounded focus:ring-orange-custom"
        />
        <span class="ml-2">{option}</span>
      </label>
    {/each}
  </div>
  {#if errors.interests}
    <p class="text-red-500 text-sm mt-1">{errors.interests}</p>
  {/if}
</div>
```

### Date Input
```svelte
<div class="mb-4">
  <label for="startDate" class="block text-gray-700 font-semibold mb-2">
    Preferred Start Date *
  </label>
  <input
    id="startDate"
    type="date"
    bind:value={formData.startDate}
    min={new Date().toISOString().split('T')[0]}
    class="w-full px-4 py-3 border border-gray-300 rounded-lg
           focus:outline-none focus:ring-2 focus:ring-orange-custom"
    required
  />
</div>
```

## Form Submission Workflow

### Standard Submission Flow
```svelte
<script lang="ts">
  async function handleSubmit() {
    // 1. Clear previous messages
    successMessage = '';
    errorMessage = '';

    // 2. Validate all fields
    if (!validateForm()) {
      errorMessage = 'Please fix the errors above';
      return;
    }

    // 3. Set loading state
    isSubmitting = true;

    try {
      // 4. Create submission object with timestamp
      const submission = {
        ...formData,
        timestamp: Date.now()
      };

      // 5. Update local store (optional, for immediate UI feedback)
      addSubmission(submission);

      // 6. Save to Firestore
      const docId = await addToFirestore(submission);
      console.log('✅ Saved with ID:', docId);

      // 7. Show success message
      successMessage = 'Thank you! Your submission has been received.';

      // 8. Reset form (optional)
      resetForm();

      // 9. Optional: Redirect after delay
      setTimeout(() => {
        goto('/thank-you');
      }, 2000);
    } catch (error) {
      // 10. Handle errors
      console.error('❌ Submission error:', error);
      errorMessage = 'Something went wrong. Please try again.';
    } finally {
      // 11. Clear loading state
      isSubmitting = false;
    }
  }

  function resetForm() {
    formData = { /* reset to initial values */ };
    errors = { /* clear all errors */ };
  }
</script>
```

## Success & Error Messages

### Success Message Component
```svelte
{#if successMessage}
  <div class="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg flex items-start animate-fade-in">
    <Icon icon="mdi:check-circle" class="text-2xl mr-3 flex-shrink-0" />
    <div>
      <p class="font-semibold">Success!</p>
      <p class="text-sm">{successMessage}</p>
    </div>
  </div>
{/if}
```

### Error Message Component
```svelte
{#if errorMessage}
  <div class="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg flex items-start animate-fade-in">
    <Icon icon="mdi:alert-circle" class="text-2xl mr-3 flex-shrink-0" />
    <div>
      <p class="font-semibold">Error</p>
      <p class="text-sm">{errorMessage}</p>
    </div>
  </div>
{/if}
```

### Inline Field Errors
```svelte
{#if errors.fieldName}
  <p class="text-red-500 text-sm mt-1 flex items-center">
    <Icon icon="mdi:alert-circle-outline" class="mr-1" />
    {errors.fieldName}
  </p>
{/if}
```

## Submit Button States

### Standard Submit Button
```svelte
<button
  type="submit"
  disabled={isSubmitting}
  class="w-full bg-orange-custom hover:bg-orange-dark text-white font-semibold
         py-3 px-6 rounded-lg transition-all duration-300
         shadow-md hover:shadow-lg"
  class:opacity-50={isSubmitting}
  class:cursor-not-allowed={isSubmitting}
>
  {#if isSubmitting}
    <Icon icon="mdi:loading" class="inline-block animate-spin mr-2" />
    Submitting...
  {:else}
    Submit
  {/if}
</button>
```

### Button with Success State
```svelte
<button
  type="submit"
  disabled={isSubmitting || isSuccess}
  class="w-full font-semibold py-3 px-6 rounded-lg transition-all duration-300"
  class:bg-orange-custom={!isSuccess}
  class:hover:bg-orange-dark={!isSuccess}
  class:bg-green-500={isSuccess}
  class:opacity-50={isSubmitting}
>
  {#if isSubmitting}
    <Icon icon="mdi:loading" class="inline-block animate-spin mr-2" />
    Submitting...
  {:else if isSuccess}
    <Icon icon="mdi:check" class="inline-block mr-2" />
    Submitted!
  {:else}
    Submit
  {/if}
</button>
```

## Form Accessibility

### Accessible Form Markup
```svelte
<form on:submit|preventDefault={handleSubmit} aria-label="Contact form">
  <div class="mb-4">
    <label for="name" class="block text-gray-700 font-semibold mb-2">
      Full Name *
      <span class="sr-only">required</span>
    </label>
    <input
      id="name"
      type="text"
      bind:value={formData.name}
      aria-required="true"
      aria-invalid={!!errors.name}
      aria-describedby={errors.name ? 'name-error' : undefined}
      class="w-full px-4 py-3 border rounded-lg"
      required
    />
    {#if errors.name}
      <p id="name-error" class="text-red-500 text-sm mt-1" role="alert">
        {errors.name}
      </p>
    {/if}
  </div>
</form>
```

## When to Use This Skill
- Creating new forms
- Adding form validation
- Implementing submission workflows
- Handling form errors
- Integrating with Firestore
- Improving form UX
- Adding accessibility features

## Related Skills
- `sikhaid-data` - Stores and Firestore operations
- `sikhaid-components` - Component patterns
- `sikhaid-styling` - Form styling and design
- `sikhaid-payment` - Payment form specifics
