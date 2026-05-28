---
name: filament-resource-generator
description: Automated Filament resource generation with correct namespace imports (Schemas vs Forms), Vietnamese labels, standard structure, Observer patterns, ImagesRelationManager integration. USE WHEN user says 'tạo resource mới', 'create new resource', 'generate Filament resource', 'scaffold admin resource', or wants to add new entity to admin panel.
---

# Filament Resource Generator - Quick Workflow

Generate standardized Filament resources with correct namespaces, Vietnamese labels, and Observer patterns.

## When to Activate This Skill

- User says "tạo resource mới cho [Model]"
- User says "create new resource"
- User wants to "scaffold admin panel"
- Adding new entity to Filament admin

---

## Quick Workflow

### 1. Gather Requirements

Ask user:
- **Model name** (singular): Product, Category, Article
- **Has images?** Gallery or single featured image?
- **Relationships?** BelongsTo, BelongsToMany
- **Need ordering?** Drag-drop reordering (requires `order` column)
- **SEO fields?** Usually yes (slug, meta_title, meta_description)

### 2. Generate Resource

```bash
php artisan make:filament-resource Product --generate
```

**Creates:**
```
app/Filament/Resources/Products/
├── ProductResource.php
├── Pages/
│   ├── ListProducts.php
│   ├── CreateProduct.php
│   └── EditProduct.php
```

### 3. Update Resource

**Critical namespaces:**
```php
// Layout components → Schemas
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Grid;
use Filament\Schemas\Components\Section;

// Form fields → Forms
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\Toggle;

// Schema (NOT Form!)
use Filament\Schemas\Schema;
```

**Vietnamese labels:**
```php
protected static ?string $navigationLabel = 'Sản phẩm';
protected static ?string $modelLabel = 'Sản phẩm';
protected static ?string $pluralModelLabel = 'Các sản phẩm';
protected static ?string $navigationIcon = 'heroicon-o-shopping-bag';
```

**Navigation badge:**
```php
public static function getNavigationBadge(): ?string
{
    return (string) static::getModel()::where('active', true)->count();
}
```

### 4. Implement Form & Table

```php
// Form with Tabs
public static function form(Schema $schema): Schema {
    return $schema->schema([
        Tabs::make()->tabs([
            Tabs\Tab::make('Thông tin')->schema([
                TextInput::make('name')->label('Tên')->required(),
                Select::make('category_id')->label('Danh mục')->relationship('category', 'name'),
                Toggle::make('active')->label('Hiển thị')->default(true),
            ]),
        ])->columnSpanFull(),
    ]);
}

// Table with eager loading
public static function table(Table $table): Table {
    return $table
        ->modifyQueryUsing(fn($q) => $q->with(['category']))
        ->reorderable('order')  // If has order column
        ->columns([
            TextColumn::make('name')->label('Tên')->searchable(),
            ToggleColumn::make('active')->label('Hiển thị'),
        ])
        ->recordActions([EditAction::make()->iconButton()]);
}
```

### 5. Create Observer

```php
class ProductObserver {
    public function creating(Product $p): void {
        if (empty($p->slug)) $p->slug = Str::slug($p->name);
        if (empty($p->meta_title)) $p->meta_title = $p->name;
        if ($p->order === null) $p->order = (Product::max('order') ?? 0) + 1;
    }
}

// AppServiceProvider::boot()
Product::observe(ProductObserver::class);
```

### 6. Add Images (Optional)

```php
// Model
public function images(): MorphMany {
    return $this->morphMany(Image::class, 'model');
}

// Resource
public static function getRelations(): array {
    return [ImagesRelationManager::class];
}
```

---

## Checklist

Before declaring resource complete:

- [ ] Correct namespaces (Schemas vs Forms)
- [ ] Vietnamese labels (100%)
- [ ] Form with Tabs/Grid structure
- [ ] Table with eager loading
- [ ] Reorderable if order column
- [ ] ImagesRelationManager if images
- [ ] Observer for SEO + order
- [ ] Observer registered in AppServiceProvider
- [ ] Navigation badge showing count
- [ ] Tested create/edit/delete

---

## Key Principles

1. **Namespace correctness**: `Schemas` for layouts, `Forms` for fields
2. **Vietnamese first**: All labels tiếng Việt
3. **Observer patterns**: SEO auto-generated, hidden from form
4. **Eager loading**: Always `modifyQueryUsing()` for relations
5. **Standard structure**: Tabs → Grid → Fields

---

## References

**Detailed implementations:** `read .claude/skills/filament/filament-resource-generator/references/detailed-implementation.md`
**Complete guide:** `read .claude/skills/filament/filament-resource-generator/CLAUDE.md`

**Related:** filament-rules, image-management, filament-form-debugger
