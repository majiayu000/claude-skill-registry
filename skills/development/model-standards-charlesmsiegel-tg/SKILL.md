---
name: model-standards
description: Code standards and templates for Django models, views, forms, templates, and URLs in this World of Darkness application. Use when creating new models (characters, items, locations), implementing reference/lookup models (factions, clans, disciplines), building CRUD views, designing forms, setting up URL patterns, or ensuring gameline consistency. Triggers on file creation/editing in characters/, items/, locations/ apps or when implementing polymorphic inheritance patterns.
---

# Model Standards

Project-specific Django patterns for the World of Darkness application. These standards ensure consistency across gamelines.

## Workflow Decision Tree

**Creating a new polymorphic model?**
→ See [references/model-templates.md](references/model-templates.md) for Character/Item/Location inheritance patterns

**Setting up CRUD views?**
→ See [references/view-templates.md](references/view-templates.md) for mixin order and permission patterns

**Building forms?**
→ See [references/form-templates.md](references/form-templates.md) for ModelForm and formset patterns

**Creating templates?**
→ See [references/template-patterns.md](references/template-patterns.md) for inheritance and includes

**Configuring URLs?**
→ See [references/url-patterns.md](references/url-patterns.md) for namespace hierarchy

**Checking what's implemented?**
→ See [references/model-inventory.md](references/model-inventory.md) for full model status

## Project-Specific Conventions

### Model Type Registration

Every polymorphic model MUST set:
```python
type = "model_name"      # Snake_case, matches URL pattern
gameline = "gameline"    # Lowercase: vampire, werewolf, mage, wraith, changeling, demon, mummy, hunter
```

### URL Namespace Pattern

```
app:gameline:action:model_type
```
Example: `characters:vampire:detail:vampire`

### Required Model Methods

```python
def get_absolute_url(self):
    return reverse("app:gameline:detail:model_type", kwargs={"pk": self.pk})

def get_update_url(self):
    return reverse("app:gameline:update:model_type", kwargs={"pk": self.pk})
```

**Note:** `get_heading()` is inherited from `core.models.Model` and returns `f"{gameline}_heading"` automatically. Do NOT override it unless the model needs special behavior.

### Gameline Heading Classes

| Gameline | Class | Color |
|----------|-------|-------|
| Vampire | `vtm_heading` | Dark Red |
| Werewolf | `wta_heading` | Green |
| Mage | `mta_heading` | Purple |
| Wraith | `wto_heading` | Gray |
| Changeling | `ctd_heading` | Teal |
| Demon | `dtf_heading` | Dark Red |
| Mummy | `mtr_heading` | Gold |
| Hunter | `htr_heading` | Orange |

### Mixin Stacking Order (left to right)

```python
# Update views
class MyView(EditPermissionMixin, MessageMixin, UpdateView): pass

# List views  
class MyListView(VisibilityFilterMixin, ListView): pass

# Create views
class MyCreateView(LoginRequiredMixin, MessageMixin, CreateView): pass

# ST-only views
class MySTView(STRequiredMixin, MessageMixin, CreateView): pass
```

### Reference Model Inheritance

Do NOT redefine fields inherited from `core.models.Model`:
- `name`, `description`, `owner`, `chronicle`, `status`, `display`
- `sources` (M2M) - use `add_source(book_title, page_number)` method

## File Location Patterns

| Component | Path |
|-----------|------|
| Model | `app/models/gameline/model_name.py` |
| Views | `app/views/gameline/{list,detail,create,update}.py` |
| Forms | `app/forms/gameline/model_name.py` |
| URLs | `app/urls/gameline/{list,detail,create,update}.py` |
| Templates | `app/templates/app/gameline/model_name/{detail,list,form}.html` |
| Display Includes | `app/templates/app/gameline/model_name/display_includes/` |

## Implementation Checklist

### Model Layer
- [ ] Proper base class inheritance (Character/Human, ItemModel, LocationModel, or Model)
- [ ] `type` and `gameline` attributes set
- [ ] `__str__`, `get_absolute_url`, `get_update_url` methods (get_heading is inherited)
- [ ] Meta class with `verbose_name`, `verbose_name_plural`, `ordering`
- [ ] Migration created and applied

### URL Layer
- [ ] List, detail, create, update URL patterns
- [ ] Registered in gameline router
- [ ] Names follow `app:gameline:action:model_name` convention

### View Layer
- [ ] Correct mixin stacking order
- [ ] `select_related`/`prefetch_related` optimization
- [ ] Form class selection based on permissions in UpdateView

### Form Layer
- [ ] Creation form with user-filtered querysets
- [ ] Limited edit form for owners (non-ST users)

### Template Layer
- [ ] Extends appropriate base (`characters/core/human/detail.html`, etc.)
- [ ] Uses `tg-card`, `tg-table` classes (not Bootstrap defaults)
- [ ] Gameline heading class on cards
