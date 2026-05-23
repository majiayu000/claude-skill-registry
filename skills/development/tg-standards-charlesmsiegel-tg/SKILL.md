---
name: tg-standards
description: >
  Django development standards for the Tellurium Games World of Darkness application.
  Use when: creating/editing models (characters, items, locations), implementing CRUD views,
  building forms, creating templates, configuring URLs, working with permissions, caching,
  migrations, testing, validation, deployment, or management commands. Triggers on:
  model inheritance patterns, polymorphic models, view mixins, gameline-specific code
  (vampire/werewolf/mage/wraith/changeling/demon/mummy/hunter), tg-card components,
  XP/freebie transactions, ST permissions, character templates, frontend styling.
---

# TG Standards

Django patterns and conventions for the World of Darkness application.

## Decision Tree

**What are you working on?**

| Task | Reference |
|------|-----------|
| Creating/editing a model | [references/models.md](references/models.md) |
| Creating/editing views | [references/views.md](references/views.md) |
| Creating/editing forms | [references/forms.md](references/forms.md) |
| Creating/editing templates | [references/templates.md](references/templates.md) |
| Setting up URLs | [references/urls.md](references/urls.md) |
| Permission checks | [references/permissions.md](references/permissions.md) |
| Data validation, transactions | [references/validation.md](references/validation.md) |
| Database migrations | [references/migrations.md](references/migrations.md) |
| Caching | [references/caching.md](references/caching.md) |
| Writing tests | [references/testing.md](references/testing.md) |
| Deployment | [references/deployment.md](references/deployment.md) |
| Management commands | [references/commands.md](references/commands.md) |
| Character templates | [references/character-templates.md](references/character-templates.md) |
| WoD terminology lookup | [references/domain.md](references/domain.md) |
| Model inventory/status | [references/model-inventory.md](references/model-inventory.md) |

## Core Conventions (Always Apply)

### Model Type Registration
```python
type = "model_name"      # Snake_case, matches URL pattern
gameline = "gameline"    # vtm, wta, mta, wto, ctd, dtf, mtr, htr
```

### URL Namespace Pattern
```
app:gameline:action:model_type
```

### Required Model Methods
```python
def get_absolute_url(self):
    return reverse("app:gameline:detail:model_type", kwargs={"pk": self.pk})

def get_update_url(self):
    return reverse("app:gameline:update:model_type", kwargs={"pk": self.pk})
# get_heading() inherited from core.models.Model - returns f"{gameline}_heading"
```

### Mixin Stacking Order
```python
class MyUpdateView(EditPermissionMixin, MessageMixin, UpdateView): pass
class MyListView(VisibilityFilterMixin, ListView): pass
class MyCreateView(LoginRequiredMixin, MessageMixin, CreateView): pass
```

### Template Classes
Use `tg-card`, `tg-table`, `tg-badge`, `tg-btn` (not Bootstrap defaults).

### Gameline Headings
| Gameline | Class | Data Attr |
|----------|-------|-----------|
| Vampire | `vtm_heading` | `data-gameline="vtm"` |
| Werewolf | `wta_heading` | `data-gameline="wta"` |
| Mage | `mta_heading` | `data-gameline="mta"` |
| Wraith | `wto_heading` | `data-gameline="wto"` |
| Changeling | `ctd_heading` | `data-gameline="ctd"` |
| Demon | `dtf_heading` | `data-gameline="dtf"` |
| Mummy | `mtr_heading` | `data-gameline="mtr"` |
| Hunter | `htr_heading` | `data-gameline="htr"` |

Use `{{ object.get_heading }}` for dynamic class.

### File Location Pattern
| Component | Path |
|-----------|------|
| Model | `app/models/gameline/model_name.py` |
| Views | `app/views/gameline/{list,detail,create,update}.py` |
| Forms | `app/forms/gameline/model_name.py` |
| URLs | `app/urls/gameline/{list,detail,create,update}.py` |
| Templates | `app/templates/app/gameline/model_name/{detail,list,form}.html` |

## Quick Checklist

### New Model
- [ ] Proper base class (Character/Human, ItemModel, LocationModel, or Model)
- [ ] `type` and `gameline` set
- [ ] `__str__`, `get_absolute_url`, `get_update_url`
- [ ] Meta with `verbose_name`, `verbose_name_plural`, `ordering`
- [ ] Migration created

### New View
- [ ] Correct mixin order
- [ ] `select_related`/`prefetch_related` for optimization
- [ ] Form class selection based on permissions in UpdateView

### New Template
- [ ] Extends appropriate base
- [ ] Uses `tg-*` classes
- [ ] Gameline heading on cards
- [ ] Loads `{% load dots sanitize_text %}` if using those filters
