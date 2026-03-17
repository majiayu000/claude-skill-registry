# Min Side Expert Context

> Use this skill when working on `/min-side/` routes, user authentication, access control, or member portal features in BIM Verdi.

---

## 1. Architecture Overview

### Router System
Min Side uses a single router template that maps URL paths to part files:

```
template-minside-router.php
    ↓
inc/minside-helpers.php (route definitions)
    ↓
parts/minside/{part-file}.php
```

**Key files:**
- `template-minside-router.php` - Main router template
- `inc/minside-helpers.php` - Route definitions + helper functions
- `header-minside.php` - Authenticated header
- `parts/minside/*.php` - Individual view templates

### Adding a New Route

1. Add route to `bimverdi_get_minside_routes()` in `inc/minside-helpers.php`:
```php
'my-route'       => 'my-route',        // Simple route
'parent/child'   => 'parent-child',    // Nested route
```

2. Create template file: `parts/minside/{part-file}.php`

3. Optionally add to navigation in `bimverdi_get_minside_nav()`

---

## 2. Complete Route Map

### Active Routes (17+)

| URL Path | Part File | Description |
|----------|-----------|-------------|
| `/min-side/` | dashboard.php | Main dashboard |
| `/min-side/profil/` | profil.php | View profile |
| `/min-side/profil/rediger/` | profil-rediger.php | Edit profile |
| `/min-side/profil/passord/` | profil-passord.php | Change password |
| `/min-side/foretak/` | foretak-detail.php | View company |
| `/min-side/foretak/rediger/` | foretak-rediger.php | Edit company (hovedkontakt only) |
| `/min-side/verktoy/` | verktoy-list.php | List tools |
| `/min-side/verktoy/registrer/` | verktoy-registrer.php | Register new tool |
| `/min-side/verktoy/rediger/` | verktoy-rediger.php | Edit tool (?id=X) |
| `/min-side/kunnskapskilder/` | kunnskapskilder-list.php | List knowledge sources |
| `/min-side/kunnskapskilder/registrer/` | kunnskapskilder-registrer.php | Register knowledge source |
| `/min-side/kunnskapskilder/rediger/` | kunnskapskilder-rediger.php | Edit knowledge source |
| `/min-side/artikler/` | artikler-list.php | List articles |
| `/min-side/artikler/skriv/` | artikler-skriv.php | Write new article |
| `/min-side/arrangementer/` | arrangementer-list.php | Events list |
| `/min-side/prosjektideer/` | prosjektideer-list.php | Project ideas list |
| `/min-side/invitasjoner/` | invitasjoner-list.php | Invite colleagues (hovedkontakt only) |

### Legacy Route Aliases
These redirect to new routes for backward compatibility:
- `/min-side/mine-verktoy/` → verktoy-list
- `/min-side/registrer-verktoy/` → verktoy-registrer
- `/min-side/rediger-verktoy/` → verktoy-rediger
- `/min-side/rediger-foretak/` → foretak-rediger
- `/min-side/rediger-profil/` → profil-rediger
- `/min-side/endre-passord/` → profil-passord
- `/min-side/skriv-artikkel/` → artikler-skriv

---

## 3. User Roles & Access Control

### Account Types

| Type | Definition | Access Level |
|------|------------|--------------|
| `profil` | User without company | Limited - can browse, attend events |
| `foretak` | User linked to company | Full - can create content |
| `guest` | Not logged in | No Min Side access |

### WordPress Roles

| Role | Description | Has Company |
|------|-------------|-------------|
| `medlem` | Free member | Optional |
| `tilleggskontakt` | Invited by hovedkontakt | Yes (required) |
| `deltaker` | Paying member (standard) | Yes (required) |
| `prosjektdeltaker` | Paying member (mid-tier) | Yes (required) |
| `partner` | Paying member (top tier) | Yes (required) |

**Important:** `deltaker`, `prosjektdeltaker`, and `partner` have IDENTICAL capabilities. The difference is business/pricing only.

### Hovedkontakt vs Tilleggskontakt

| Capability | Tilleggskontakt | Hovedkontakt |
|------------|-----------------|--------------|
| Create tools | Yes | Yes |
| Write articles | Yes | Yes |
| Register knowledge sources | Yes | Yes |
| Submit project ideas | Yes | Yes |
| Edit own content | Yes | Yes |
| Delete content | No (admin) | No (admin) |
| Edit company profile | **No** | **Yes** |
| View team members | Yes | Yes |
| Remove team members | No | **Yes** |
| Transfer hovedkontakt | No | **Yes** |
| Invite colleagues | No | **Yes** |

### Feature Access Control

**Requires Company (`foretak` account type):**
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

**Open to All Logged-In Users:**
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

---

## 4. Helper Functions

### URL Helpers
```php
// Get Min Side base URL
bimverdi_minside_base_url();  // Returns: https://site.com/min-side

// Generate Min Side URL
bimverdi_minside_url('verktoy');           // /min-side/verktoy/
bimverdi_minside_url('verktoy/rediger', ['id' => 123]);  // /min-side/verktoy/rediger/?id=123

// Get current route
bimverdi_get_current_route();  // Returns: 'verktoy/rediger'

// Check if on specific route
bimverdi_is_minside_route('verktoy');      // true for /verktoy/ and /verktoy/rediger/
bimverdi_is_minside_route(['profil', 'foretak']);  // Multiple routes

// Get primary route segment
bimverdi_get_primary_route();  // 'verktoy' from 'verktoy/rediger'
```

### Company & User Helpers
```php
// Check if user has company
bimverdi_user_has_company($user_id);  // Returns: bool

// Get user's company ID
bimverdi_get_user_company($user_id);  // Returns: int|false

// Check if user is hovedkontakt
bimverdi_is_hovedkontakt($user_id, $company_id);  // Returns: bool

// Check if company is active/approved
bimverdi_is_company_active($company_id);  // Returns: bool

// Get account type
bimverdi_get_account_type($user_id);  // Returns: 'profil', 'foretak', or 'guest'
```

### Access Control Helpers
```php
// Check feature access
bimverdi_can_access('register_tool');  // Returns: bool

// Render locked feature UI
BIMVerdi_Access_Control::render_locked_ui('register_tool', 'Custom message');

// Render locked card component
bimverdi_locked_card('Title', 'Description', 'icon-name', 'feature');

// Render "connect to company" CTA
bimverdi_connect_company_cta();
```

### Navigation Helper
```php
// Get navigation structure
$nav = bimverdi_get_minside_nav();
// Returns array with: label, url, icon, badge, routes
```

---

## 5. Company ID Storage (Legacy Migration)

User's company is stored in user_meta. Check these keys **in order**:

1. `bimverdi_company_id` (new standard)
2. `bim_verdi_company_id` (legacy)
3. ACF field `tilknyttet_foretak` (fallback)

**Always use the helper function** `bimverdi_get_user_company()` which handles all three.

---

## 6. ACF Field Reference

### Foretak (Company) - CPT: `foretak`
```php
get_field('hovedkontaktperson', $company_id);  // User ID of primary contact
get_field('bv_rolle', $company_id);            // Deltaker|Prosjektdeltaker|Partner|Ikke deltaker
get_field('organisasjonsnummer', $company_id); // Norwegian org number
get_field('bedriftsnavn', $company_id);        // Company name (or post_title)
get_field('beskrivelse', $company_id);         // Company description
get_field('logo', $company_id);                // Attachment ID
get_field('adresse', $company_id);             // Street address
get_field('postnummer', $company_id);          // Postal code
get_field('poststed', $company_id);            // City
get_field('land', $company_id);                // Country
get_field('telefon', $company_id);             // Phone
get_field('epost', $company_id);               // Email
get_field('nettside', $company_id);            // Website URL
```

### Verktøy (Tool) - CPT: `verktoy`
```php
get_field('tilknyttet_foretak', $tool_id);     // Company ID that owns the tool
get_field('eier_leverandor', $tool_id);        // Owner/vendor company
get_field('logo', $tool_id);                   // Tool logo
get_field('vendor', $tool_id);                 // Vendor name
get_field('type_verktoey', $tool_id);          // Tool type
get_field('plattform', $tool_id);              // Platform(s)
```

### Kunnskapskilde (Knowledge Source) - CPT: `kunnskapskilde`
```php
get_field('registrert_av', $kilde_id);         // User ID who registered
get_field('tilknyttet_bedrift', $kilde_id);    // Company ID
get_field('kunnskapskilde_navn', $kilde_id);   // Name
get_field('kildetype', $kilde_id);             // Type (standard, veileder, etc.)
get_field('utgiver', $kilde_id);               // Publisher
get_field('ekstern_lenke', $kilde_id);         // External URL
get_field('kort_beskrivelse', $kilde_id);      // Short description
```

### Arrangement (Event) - CPT: `arrangement`
```php
get_field('arrangement_dato', $event_id);      // Date
get_field('tidspunkt_start', $event_id);       // Start time
get_field('tidspunkt_slutt', $event_id);       // End time
get_field('arrangement_type', $event_id);      // Type (digitalt, fysisk, hybrid)
get_field('sted_by', $event_id);               // City
get_field('sted_adresse', $event_id);          // Address
get_field('pamelding_url', $event_id);         // Registration URL
get_field('maks_deltakere', $event_id);        // Max participants
```

### Prosjektidé (Project Idea) - CPT: `case`
```php
get_field('temagruppe', $idea_id);             // Related theme group
```

### User Fields
```php
get_field('tilknyttet_foretak', 'user_' . $user_id);  // Company ID
```

---

## 7. CPT Constants

Defined in `bim-verdi-core/includes/class-content-types.php`:

```php
BV_CPT_COMPANY       = 'foretak'       // Member companies
BV_CPT_TOOL          = 'verktoy'       // Software tools
BV_CPT_EVENT         = 'arrangement'   // Events/meetings
BV_CPT_REGISTRATION  = 'pamelding'     // Event registrations
BV_CPT_IDEA          = 'case'          // Project ideas (private)
BV_CPT_PROJECT       = 'prosjekt'      // Pilot projects
BV_CPT_THEME_GROUP   = 'theme_group'   // Temagrupper
BV_CPT_ARTICLE       = 'artikkel'      // Member articles
```

---

## 8. Gravity Forms

### Form IDs
- **Form 10:** Email signup (Step 1) - Email verification flow
- **Form 11:** Account activation (Step 2) - Name + password

### Form Handlers
Located in `mu-plugins/bimverdi-email-verification.php` and `bimverdi-gforms-setup.php`.

### Usage in Templates
Forms are embedded via PHP or shortcode in registration flows, not typically in Min Side views.

---

## 9. Design System Rules

**Always follow** `claude/UI-CONTRACT.md` when building Min Side templates.

### Key Principles
1. **P1:** Whitespace + dividers as primary structure (no "boxes everywhere")
2. **P2:** Clickability must be explicit (only buttons/links are interactive)
3. **P3:** Information ≠ handling (info in borderless sections, actions in buttons)
4. **P4:** Show only what exists (hide empty fields)
5. **P5:** Rolig, consistent enterprise style (minimal visual noise)

### Layout Widths
- Standard content: `max-width: 1200-1280px`
- Form pages: `max-width: 960px`
- Spacing scale: 8px increments

### Color Palette
```
Text Primary:    #1A1A1A   text-[#1A1A1A]
Text Secondary:  #5A5A5A   text-[#5A5A5A]
Dividers:        #D6D1C6   border-[#D6D1C6]
Background:      #F7F5EF   bg-[#F7F5EF]
CTA/Orange:      #FF8B5E   bg-[#FF8B5E]
```

### Button Component
Use `bimverdi_button()` from `parts/components/button.php`:
```php
bimverdi_button([
    'text' => 'Lagre',
    'variant' => 'primary',  // primary, secondary, tertiary, danger
    'size' => 'medium',      // small, medium, large
    'icon' => 'save',        // Lucide icon name
    'href' => '/url',        // Makes it a link
]);
```

### Icons
Use **Lucide icons** (https://lucide.dev):
- `layout-dashboard` - Dashboard
- `wrench` - Tools
- `file-text` - Articles
- `lightbulb` - Ideas
- `calendar` - Events
- `building-2` - Company
- `user-plus` - Invitations
- `chevron-right` - Navigate

---

## 10. Temagrupper (Theme Groups)

**Important:** Temagrupper are linked to **foretak (companies)**, NOT individual users.

- All users linked to a foretak can view the company's temagrupper
- Only hovedkontakt can change temagruppe memberships
- Temagruppe selection is a company-level setting

---

## 11. Common Patterns

### Access Check in Template
```php
<?php
// At top of template part
$user_id = get_current_user_id();
$company_id = bimverdi_get_user_company($user_id);

// Require company
if (!$company_id) {
    bimverdi_connect_company_cta();
    return;
}

// Require hovedkontakt
if (!bimverdi_is_hovedkontakt($user_id, $company_id)) {
    wp_redirect(bimverdi_minside_url('foretak'));
    exit;
}
?>
```

### Page Header Component
```php
get_template_part('parts/components/page-header', null, [
    'title' => 'Page Title',
    'description' => 'Optional subtitle text',
    'icon' => 'wrench',  // Lucide icon
    'actions' => [
        [
            'text' => 'Primary Action',
            'href' => '/url',
            'variant' => 'primary',
            'icon' => 'plus',
        ],
    ],
]);
```

### Breadcrumb Navigation
```php
<nav class="text-sm mb-6" aria-label="Brødsmulesti">
    <ol class="flex items-center gap-2 text-[#5A5A5A]">
        <li><a href="<?php echo bimverdi_minside_url(); ?>" class="hover:text-[#1A1A1A]">Min side</a></li>
        <li><span class="text-[#D6D1C6]">/</span></li>
        <li><a href="<?php echo bimverdi_minside_url('parent'); ?>" class="hover:text-[#1A1A1A]">Parent</a></li>
        <li><span class="text-[#D6D1C6]">/</span></li>
        <li class="text-[#1A1A1A] font-medium">Current Page</li>
    </ol>
</nav>
```

### Data Table Pattern
```php
<div class="overflow-x-auto">
    <table class="w-full">
        <thead>
            <tr class="border-b border-[#D6D1C6]">
                <th class="text-left py-3 px-4 text-xs font-medium text-[#5A5A5A] uppercase tracking-wide">Column</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-[#E5E2DB]">
            <tr class="hover:bg-[#F7F5EF]/50">
                <td class="py-4 px-4">Content</td>
            </tr>
        </tbody>
    </table>
</div>
```

---

## 12. Debug Mode

Add `?debug_router=1` to any Min Side URL (admin only) to see:
- Request URI
- Current Route
- Part File
- Query Var

---

## 13. Files Quick Reference

| Purpose | File Path |
|---------|-----------|
| Router template | `template-minside-router.php` |
| Route definitions | `inc/minside-helpers.php` |
| Access control | `mu-plugins/bimverdi-access-control.php` |
| Role definitions | `mu-plugins/bimverdi-custom-roles.php` |
| Authenticated header | `header-minside.php` |
| View templates | `parts/minside/*.php` |
| Button component | `parts/components/button.php` |
| Page header | `parts/components/page-header.php` |
| Design rules | `claude/UI-CONTRACT.md` |
