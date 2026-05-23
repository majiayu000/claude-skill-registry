---
name: docuware
description: DocuWare document management integration patterns. Use when working with DocuWare connector, webhooks, document imports, or app/Services/DocuWare/.
---

**Name:** DocuWare Integration
**Description:** DocuWare document management integration patterns. Use when working with DocuWare connector, webhooks, document imports, or app/Services/DocuWare/.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Services/DocuWare/**/*.php, docuware, document-management, webhook, import

## Rules

- Uses `codebar-ag/laravel-docuware` package (not raw Saloon)
- Connector: `CodebarAg\DocuWare\Connectors\DocuWareConnector` with `ConfigWithCredentials`
- Credentials via `config('laravel-docuware.credentials.*')` — never `env()` directly
- DocuWareService wraps the connector in `app/Services/DocuWare/DocuWareService.php`
- Key methods: `fetchDocument()`, `downloadAndStore()`, `mapToInvoiceData()`, `processImport()`
- Accept optional connector in constructor for testability
- Field mapping defined in `config/docuware-fields.php`
- Always check for DocuWare credentials before making API calls
- Handle download failures gracefully (log warning, continue without file)
- Use `DB::transaction()` for model creation + import status update
- Duplicate detection: skip if same `source_document_id` already exists
- Activity logging at each stage (webhook received, processing started/completed/failed)

## Webhook Flow

1. `POST /api/docuware/webhook` receives payload
2. HMAC signature verification via `VerifyDocuWareSignature` middleware
3. Create `DocumentImport` record with status `pending`
4. Dispatch `ProcessDocuWareImport` queued job
5. Job: fetch metadata, download document, create model, update import status

## Import Lifecycle

- `DocumentImport` model tracks: `pending` → `processing` → `completed` / `failed`
- Use `DB::transaction()` when creating model and updating import status together

## Examples

```php
// DocuWareService — optional connector for testability
class DocuWareService
{
    public function __construct(?DocuWareConnector $connector = null)
    {
        $this->connector = $connector ?? new DocuWareConnector();
    }

    public function processImport(DocumentImport $import): void
    {
        if (! config('laravel-docuware.credentials.api_url')) {
            throw new DocuWareNotConfiguredException();
        }

        $import->update(['status' => 'processing']);

        try {
            DB::transaction(function () use ($import) {
                $document = $this->fetchDocument($import->source_document_id);
                $data = $this->mapToInvoiceData($document);
                $model = Invoice::create($data);
                $import->update(['status' => 'completed', 'importable_id' => $model->id]);
                activity()->performedOn($import)->log('Document import completed.');
            });
        } catch (Throwable $e) {
            Log::warning('DocuWare download failed.', ['import_id' => $import->id]);
            $import->update(['status' => 'failed']);
            throw $e;
        }
    }
}
```

```php
// Duplicate detection before processing
if (DocumentImport::where('source_document_id', $payload['id'])->exists()) {
    return response()->json(['status' => 'skipped'], 200);
}
```

## Anti-Patterns

- Using `env()` directly for DocuWare credentials — use `config()`
- Making API calls without checking credentials first
- Not using `DB::transaction()` when creating models and updating import status
- Swallowing download failures — log and handle gracefully
- Missing activity logging at import lifecycle stages
- Processing imports without duplicate detection on `source_document_id`

## References

- [codebar-ag/laravel-docuware](https://github.com/codebar-ag/laravel-docuware)
- Related: `Services/SKILL.md` — service class conventions
- Related: `Jobs/SKILL.md` — queued job for ProcessDocuWareImport
