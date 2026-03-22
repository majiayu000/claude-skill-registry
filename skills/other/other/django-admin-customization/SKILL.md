---
name: django-admin-customization
description: >
  Customize Django admin: ModelAdmin, inline models, custom actions, list_display,
  list_filter, search, admin site customization, and custom views. Use when the user
  configures Django admin, asks about admin customization, registers models, or needs
  admin-side data management features. Trigger when you see bare admin.site.register()
  calls without ModelAdmin classes.
---

# Django Admin Customization

Build powerful admin interfaces with Django's built-in admin. A well-configured admin
panel eliminates the need for custom CRUD dashboards and gives non-technical users
a safe way to manage data.

## When to Use
- User registers Django models in admin
- User needs custom list views, filters, or search
- User asks about inline editing or custom actions
- User wants to customize the admin site appearance
- User needs admin-only business operations (bulk actions, exports)

## Core Patterns

### ModelAdmin Configuration

```python
from django.contrib import admin
from django.utils.html import format_html

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # List view configuration
    list_display = [
        "title", "author_name", "category", "status",
        "view_count", "colored_status", "created_at",
    ]
    list_display_links = ["title"]
    list_editable = ["status", "category"]
    list_filter = ["status", "category", "created_at"]
    list_per_page = 25
    list_select_related = ["author", "category"]

    # Search
    search_fields = ["title", "body", "author__username", "author__email"]
    search_help_text = "Search by title, body, or author"

    # Detail view
    readonly_fields = ["slug", "view_count", "created_at", "updated_at"]
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["author", "category"]
    filter_horizontal = ["tags"]

    # Fieldsets -- organize detail view into sections
    fieldsets = [
        (None, {
            "fields": ["title", "slug", "body"],
        }),
        ("Classification", {
            "fields": ["category", "tags", "status"],
        }),
        ("Metadata", {
            "classes": ["collapse"],  # Collapsible section
            "fields": ["author", "view_count", "created_at", "updated_at"],
        }),
    ]

    # Date hierarchy for drill-down navigation
    date_hierarchy = "created_at"

    # Ordering
    ordering = ["-created_at"]

    @admin.display(description="Author", ordering="author__last_name")
    def author_name(self, obj):
        return obj.author.get_full_name()

    @admin.display(description="Status")
    def colored_status(self, obj):
        colors = {"draft": "gray", "published": "green", "archived": "red"}
        color = colors.get(obj.status, "black")
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display(),
        )
```

### Inline Models

Edit related objects directly on the parent's admin page.

```python
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0  # No empty forms by default
    readonly_fields = ["author", "created_at"]
    fields = ["author", "text", "is_approved", "created_at"]

    def has_add_permission(self, request, obj=None):
        return False  # Comments are created by users, not admins

class ImageInline(admin.StackedInline):
    model = ArticleImage
    extra = 1
    max_num = 10

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ImageInline, CommentInline]
    list_display = ["title", "status", "comment_count"]

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related("author", "category")
            .annotate(comment_count=Count("comments"))
        )

    @admin.display(description="Comments", ordering="comment_count")
    def comment_count(self, obj):
        return obj.comment_count
```

### Custom Actions

Bulk operations on selected objects from the list view.

```python
from django.contrib import messages
from django.http import HttpResponse
import csv

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    actions = ["publish_selected", "archive_selected", "export_as_csv"]

    @admin.action(description="Publish selected articles")
    def publish_selected(self, request, queryset):
        updated = queryset.filter(status="draft").update(status="published")
        self.message_user(
            request,
            f"{updated} article(s) published.",
            messages.SUCCESS,
        )

    @admin.action(description="Archive selected articles")
    def archive_selected(self, request, queryset):
        updated = queryset.exclude(status="archived").update(status="archived")
        self.message_user(request, f"{updated} article(s) archived.")

    @admin.action(description="Export selected as CSV")
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="articles.csv"'

        writer = csv.writer(response)
        writer.writerow(["Title", "Author", "Status", "Views", "Created"])

        for article in queryset.select_related("author"):
            writer.writerow([
                article.title,
                article.author.get_full_name(),
                article.status,
                article.view_count,
                article.created_at.isoformat(),
            ])

        return response
```

### Custom List Filters

```python
from django.utils import timezone
from datetime import timedelta

class ViewCountRangeFilter(admin.SimpleListFilter):
    title = "view count"
    parameter_name = "views"

    def lookups(self, request, model_admin):
        return [
            ("low", "Low (< 100)"),
            ("medium", "Medium (100-1000)"),
            ("high", "High (> 1000)"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "low":
            return queryset.filter(view_count__lt=100)
        if self.value() == "medium":
            return queryset.filter(view_count__gte=100, view_count__lte=1000)
        if self.value() == "high":
            return queryset.filter(view_count__gt=1000)
        return queryset

class RecentFilter(admin.SimpleListFilter):
    title = "recency"
    parameter_name = "recent"

    def lookups(self, request, model_admin):
        return [
            ("today", "Today"),
            ("week", "This week"),
            ("month", "This month"),
        ]

    def queryset(self, request, queryset):
        now = timezone.now()
        ranges = {
            "today": now - timedelta(days=1),
            "week": now - timedelta(weeks=1),
            "month": now - timedelta(days=30),
        }
        if self.value() in ranges:
            return queryset.filter(created_at__gte=ranges[self.value()])
        return queryset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_filter = ["status", "category", ViewCountRangeFilter, RecentFilter]
```

### Admin Site Customization

```python
# admin.py -- customize the default admin site
admin.site.site_header = "My Project Admin"
admin.site.site_title = "My Project"
admin.site.index_title = "Dashboard"

# Custom admin site for multi-tenant or separate admin panels
class AnalyticsAdminSite(admin.AdminSite):
    site_header = "Analytics Dashboard"
    site_title = "Analytics"

    def has_permission(self, request):
        return request.user.is_active and request.user.groups.filter(
            name="analytics"
        ).exists()

analytics_admin = AnalyticsAdminSite(name="analytics_admin")
analytics_admin.register(PageView, PageViewAdmin)

# urls.py
urlpatterns = [
    path("admin/", admin.site.urls),
    path("analytics/", analytics_admin.urls),
]
```

### Overriding Save and Permissions

```python
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.author == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields + ["status", "author"]
        return self.readonly_fields
```

## Anti-Patterns

- **Bare `admin.site.register(Model)`**: Always create a ModelAdmin class. Even a
  minimal one with `list_display` and `search_fields` vastly improves usability.
- **No `list_select_related`**: Admin list views trigger N+1 queries when displaying
  related fields. Always set `list_select_related` or override `get_queryset`.
- **Business logic in admin actions**: Admin actions should call service functions,
  not contain business logic directly. Keep actions thin.
- **No search fields**: Users will need to find records. Always configure
  `search_fields` on models with more than a handful of records.
- **Using `list_editable` without caution**: Editable list fields bypass normal form
  validation. Use sparingly and only for simple status-like fields.

## Quick Reference

| Feature | Configuration |
|---|---|
| Columns | `list_display = ["field1", "field2"]` |
| Editable in list | `list_editable = ["status"]` |
| Sidebar filters | `list_filter = ["status", CustomFilter]` |
| Search | `search_fields = ["title", "author__name"]` |
| Auto-slug | `prepopulated_fields = {"slug": ("title",)}` |
| Sections | `fieldsets = [(name, {"fields": [...]})]` |
| Inline editing | `inlines = [CommentInline]` |
| Bulk actions | `actions = ["my_action"]` |
| Date drill-down | `date_hierarchy = "created_at"` |
| FK autocomplete | `autocomplete_fields = ["author"]` |
| M2M widget | `filter_horizontal = ["tags"]` |
| Per-page count | `list_per_page = 25` |
