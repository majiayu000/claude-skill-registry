---
name: minside
description: Expert context for BIM Verdi's Min Side member portal. Use when working on /min-side/ routes, user authentication, access control, or member features.
---

# Min Side Skill

This skill provides deep context for working on BIM Verdi's authenticated member portal at `/min-side/`.

## Architecture Overview

Min Side is a **SPA-like router** within WordPress:
- Single page template: `template-minside-router.php`
- Routes parsed from URL and mapped to part files
- All routes under `/min-side/` require authentication
- Access control based on account type (profil vs foretak)

## Route System

### URL Structure
```
/min-side/                    → Dashboard
/min-side/{section}/          → Section list/detail
/min-side/{section}/rediger/  → Edit form
/min-side/{section}/registrer/→ Create form
```

### Complete Route Map

| Route | Part File | Access | Description |
|-------|-----------|--------|-------------|
| `dashboard` | `dashboard.php` | All | Main dashboard |
| `profil` | `profil.php` | All | User profile view |
| `profil/rediger` | `profil-rediger.php` | All | Edit profile |
| `profil/passord` | `profil-passord.php` | All | Change password |
| `foretak` | `foretak-detail.php` | Foretak | Company profile |
| `foretak/rediger` | `foretak-rediger.php` | Foretak | Edit company |
| `verktoy` | `verktoy-list.php` | All | Tool list |
| `verktoy/registrer` | `verktoy-registrer.php` | Foretak | Register tool |
| `verktoy/rediger` | `verktoy-rediger.php` | Foretak | Edit tool |
| `kunnskapskilder` | `kunnskapskilder-list.php` | All | Knowledge sources |
| `kunnskapskilder/registrer` | `kunnskapskilder-registrer.php` | Foretak | Register source |
| `kunnskapskilder/rediger` | `kunnskapskilder-rediger.php` | Foretak | Edit source |
| `artikler` | `artikler-list.php` | All | Article list |
| `artikler/skriv` | `artikler-skriv.php` | Foretak | Write article |
| `arrangementer` | `arrangementer-list.php` | All | Events list |
| `prosjektideer` | `prosjektideer-list.php` | Foretak | Project ideas |
| `invitasjoner` | `invitasjoner-list.php` | Hovedkontakt | Invite colleagues |

### Legacy Route Aliases
These old routes redirect to new structure:
- `mine-verktoy` → `verktoy`
- `registrer-verktoy` → `verktoy/registrer`
- `rediger-verktoy` → `verktoy/rediger`
- `rediger-foretak` → `foretak/rediger`
- `rediger-profil` → `profil/rediger`
- `endre-passord` → `profil/passord`
- `skriv-artikkel` → `artikler/skriv`

## Account Types & Access Control

### Two Account Types

| Type | Has Company | Access Level |
|------|-------------|--------------|
| `profil` | No | Limited - can view, limited editing |
| `foretak` | Yes | Full - all features unlocked |

### User Roles

| Role | Description | Has Company |
|------|-------------|-------------|
| `medlem` | Free member | Optional |
| `tilleggskontakt` | Invited by hovedkontakt | Yes |
| `deltaker` | Paying member (standard) | Yes |
| `prosjektdeltaker` | Paying member (mid-tier) | Yes |
| `partner` | Paying member (top tier) | Yes |

**Note:** `deltaker`, `prosjektdeltaker`, `partner` have IDENTICAL capabilities. Difference is business/pricing only.

### Special Role: Hovedkontakt

The **hovedkontakt** (primary contact) is:
- Stored in ACF field `hovedkontaktperson` on the `foretak` post
- Can invite colleagues (`invitasjoner` route)
- Can edit company profile
- NOT a separate role - it's a relationship

## Feature Access Matrix

### Company-Required Features
```php
const COMPANY_REQUIRED_FEATURES = [
    'register_tool',      // Registrere verktøy
    'edit_tool',          // Redigere verktøy
    'write_article',      // Skrive artikler
    'submit_case',        // Sende inn prosjektidéer
    'join_temagruppe',    // Velge temagrupper
    'company_profile',    // Redigere foretaksprofil
    'view_members_full',  // Se fullt medlemsinnhold
];
```

### Open Features (all logged-in users)
```php
const OPEN_FEATURES = [
    'view_dashboard',     // Se Min Side dashboard
    'edit_profile',       // Redigere egen profil
    'view_catalog',       // Se medlemskatalog
    'view_tools',         // Se verktøykatalog
    'register_event',     // Melde seg på arrangementer
    'view_events',        // Se arrangementer
    'connect_company',    // Koble til foretak
];
```

## Key Helper Functions

### URL Functions
```php
// Get base URL
bimverdi_minside_base_url()
// Returns: https://bimverdi.no/min-side

// Generate Min Side URL
bimverdi_minside_url('verktoy/registrer')
// Returns: https://bimverdi.no/min-side/verktoy/registrer/

// Get current route
bimverdi_get_current_route()
// Returns: 'verktoy/registrer'

// Check if on specific route
bimverdi_is_minside_route('verktoy')
// Returns: true if on verktoy or verktoy/*

// Get primary route segment
bimverdi_get_primary_route()
// Returns: 'verktoy' from 'verktoy/registrer'
```

### User/Company Functions
```php
// Check if user has company
bimverdi_user_has_company($user_id = null)
// Returns: bool

// Get user's company ID
bimverdi_get_user_company($user_id = null)
// Returns: int|false (company post ID)

// Check if user is hovedkontakt
bimverdi_is_hovedkontakt($user_id = null, $company_id = null)
// Returns: bool

// Get account type
bimverdi_get_account_type($user_id = null)
// Returns: 'profil' | 'foretak' | 'guest'

// Check if company is active
bimverdi_is_company_active($company_id = null)
// Returns: bool (checks er_aktiv_deltaker ACF field)
```

### Access Control Functions
```php
// Check feature access
bimverdi_can_access('register_tool')
// Returns: bool

// Render locked UI
BIMVerdi_Access_Control::render_locked_ui('register_tool', 'Custom message')
// Returns: HTML for locked feature card

// Render connect company CTA
bimverdi_connect_company_cta()
// Outputs: Banner prompting user to connect company
```

## Company ID Storage (Legacy Migration)

User's company is stored in user_meta. Check in this order:
1. `bimverdi_company_id` (new standard)
2. `bim_verdi_company_id` (legacy)
3. ACF field `tilknyttet_foretak` (fallback)

**Always use `bimverdi_get_user_company()` - it handles all fallbacks.**

## Navigation Structure

Navigation is generated by `bimverdi_get_minside_nav()`:

```php
$nav = [
    'dashboard' => [
        'label' => 'Dashboard',
        'url' => '/min-side/',
        'icon' => 'layout-dashboard',
        'routes' => ['dashboard', ''],
    ],
    'verktoy' => [
        'label' => 'Mine verktøy',
        'url' => '/min-side/verktoy/',
        'icon' => 'wrench',
        'badge' => 3,  // Count of user's tools
        'routes' => ['verktoy', 'verktoy/registrer', 'verktoy/rediger'],
    ],
    // ... etc
];
```

Icons are Lucide icons.

## Adding a New Min Side Route

### Step 1: Add Route Mapping
In `inc/minside-helpers.php`, add to `bimverdi_get_minside_routes()`:
```php
'nytt-omrade'           => 'nytt-omrade-list',
'nytt-omrade/registrer' => 'nytt-omrade-registrer',
'nytt-omrade/rediger'   => 'nytt-omrade-rediger',
```

### Step 2: Create Part File
Create `parts/minside/nytt-omrade-list.php`:
```php
<?php
/**
 * Min Side: Nytt område - List
 */

// Access check
if (!bimverdi_can_access('your_feature')) {
    bimverdi_connect_company_cta();
    return;
}

$user_id = get_current_user_id();
$company_id = bimverdi_get_user_company($user_id);
?>

<div class="bv-minside-section">
    <!-- Your content -->
</div>
```

### Step 3: Add to Navigation (optional)
In `bimverdi_get_minside_nav()`:
```php
'nytt-omrade' => [
    'label' => 'Nytt område',
    'url' => bimverdi_minside_url('nytt-omrade'),
    'icon' => 'icon-name',
    'routes' => ['nytt-omrade', 'nytt-omrade/registrer', 'nytt-omrade/rediger'],
],
```

### Step 4: Add Access Control (if company-required)
In `bimverdi-access-control.php`, add to `COMPANY_REQUIRED_FEATURES`:
```php
'your_feature',
```

## Template Structure

### Part File Pattern
```php
<?php
/**
 * Min Side: [Section] - [View Type]
 *
 * @package BimVerdi_Theme
 */

// 1. Access check
if (!bimverdi_can_access('feature_name')) {
    // Show locked UI or CTA
    return;
}

// 2. Get data
$user_id = get_current_user_id();
$company_id = bimverdi_get_user_company($user_id);

// 3. Query posts/data
$items = get_posts([...]);

// 4. Render
?>
<div class="space-y-6">
    <?php get_template_part('parts/components/page-header', null, [
        'title' => 'Tittel',
        'actions' => [...],
    ]); ?>

    <!-- Content -->
</div>
```

### Common Components Used
- `parts/components/page-header.php` - Page title + actions
- `parts/components/button.php` - `bimverdi_button()`
- `parts/components/data-table.php` - Tabular data
- `parts/components/empty-state.php` - No items message

## Debugging

Add `?debug_router=1` to any Min Side URL (admin only) to see:
- Current route
- Matched part file
- User access info

## Common Patterns

### List Page with Empty State
```php
<?php if (empty($items)): ?>
    <div class="bv-empty-state">
        <p>Ingen elementer ennå.</p>
        <?php if (bimverdi_can_access('create_feature')): ?>
            <a href="<?php echo bimverdi_minside_url('section/registrer'); ?>"
               class="bv-btn bv-btn--primary">
                Opprett ny
            </a>
        <?php endif; ?>
    </div>
<?php else: ?>
    <!-- List items -->
<?php endif; ?>
```

### Edit Form with ID Parameter
```php
$item_id = isset($_GET['id']) ? intval($_GET['id']) : 0;

if (!$item_id) {
    wp_redirect(bimverdi_minside_url('section'));
    exit;
}

// Verify ownership
$item = get_post($item_id);
$item_company = get_field('tilknyttet_foretak', $item_id);

if ($item_company != $company_id) {
    // Not authorized
    return;
}
```

### Gravity Forms Integration
```php
// In registrer template
gravity_form(
    $form_id,
    $display_title = false,
    $display_description = false,
    $display_inactive = false,
    $field_values = [
        'foretak_id' => $company_id,
        'user_id' => $user_id,
    ]
);
```

## Files Reference

| File | Purpose |
|------|---------|
| `template-minside-router.php` | Main router template |
| `inc/minside-helpers.php` | All helper functions |
| `mu-plugins/bimverdi-access-control.php` | Access control class |
| `mu-plugins/bimverdi-custom-roles.php` | Role definitions |
| `parts/minside/*.php` | Individual route templates |
| `header-minside.php` | Min Side header with nav |
