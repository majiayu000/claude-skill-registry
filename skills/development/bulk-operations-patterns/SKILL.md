---
name: bulk-operations-patterns
description: "Bulk data operations with Excel import/export, batch processing, and validation for ABP Framework. Use when: (1) implementing bulk import/update from Excel/CSV, (2) batch processing with progress tracking, (3) file upload with validation, (4) bulk database operations with InsertManyAsync/UpdateManyAsync."
layer: 3
tech_stack: [dotnet, csharp, abp, efcore]
topics: [excel-import, csv, batch-processing, bulk-insert, progress-tracking]
depends_on: [efcore-patterns]
complements: [abp-framework-patterns]
keywords: [Excel, CSV, InsertManyAsync, UpdateManyAsync, Batch, Progress, ClosedXML]
---

# Bulk Operations Patterns

Master bulk data operations including Excel import/export, batch processing, and efficient database operations in ABP Framework applications.

## When to Use This Skill

- Implementing bulk import from Excel/CSV files
- Processing large datasets with validation
- Bulk database inserts/updates with `InsertManyAsync`/`UpdateManyAsync`
- File upload handling with blob storage
- Progress tracking for long-running operations
- Export data to Excel/CSV formats

## Excel Import Pattern

### 1. DTO for Excel Import

```csharp
// Application.Contracts/{EntityPlural}/BulkImport{Entity}Dto.cs
public class BulkImportProductDto
{
    [ExcelColumnName("Product Code")]
    public string ProductCode { get; set; }

    [ExcelColumnName("Product Name")]
    public string Name { get; set; }

    [ExcelColumnName("Price")]
    public string PriceText { get; set; }  // String for validation

    [ExcelColumnName("Stock")]
    public string StockText { get; set; }

    [ExcelColumnName("Category")]
    public string CategoryName { get; set; }

    // Parsed values (not from Excel)
    [ExcelIgnore]
    public decimal Price { get; set; }

    [ExcelIgnore]
    public int Stock { get; set; }

    [ExcelIgnore]
    public Guid? CategoryId { get; set; }
}
```

### 2. File Upload DTO

```csharp
// Application.Contracts/{EntityPlural}/BulkImportFileDto.cs
public class BulkImportFileDto
{
    [Required]
    public IFormFile File { get; set; }

    public bool ValidateOnly { get; set; } = false;
}

// Allowed extensions
public static class BulkImportFileExtensions
{
    public static readonly string[] Allowed = { ".xlsx", ".xls", ".csv" };
    public const long MaxFileSize = 10 * 1024 * 1024; // 10MB
}
```

### 3. AppService Implementation

```csharp
public class ProductAppService : ApplicationService, IProductAppService
{
    private readonly IRepository<Product, Guid> _productRepository;
    private readonly IRepository<Category, Guid> _categoryRepository;
    private readonly IBlobContainer<BulkImportFileContainer> _fileContainer;
    private readonly ILogger<ProductAppService> _logger;

    [Authorize(ProductPermissions.Products.Import)]
    public async Task<BulkImportResultDto> BulkImportAsync(BulkImportFileDto input)
    {
        _logger.LogInformation(
            "[{Service}] BulkImportAsync - Started - FileName: {FileName}",
            nameof(ProductAppService), input.File.FileName);

        // Step 1: Validate file
        ValidateFile(input.File);

        // Step 2: Parse Excel
        var items = await ParseExcelAsync(input.File);

        if (!items.Any())
        {
            throw new UserFriendlyException("No data found in file");
        }

        // Step 3: Load reference data
        var categories = await _categoryRepository.GetListAsync();

        // Step 4: Validate all rows
        var validationErrors = await ValidateImportDataAsync(items, categories);

        if (validationErrors.Any())
        {
            return new BulkImportResultDto
            {
                IsSuccess = false,
                TotalRows = items.Count,
                ErrorCount = validationErrors.Count,
                Errors = validationErrors
            };
        }

        if (input.ValidateOnly)
        {
            return new BulkImportResultDto
            {
                IsSuccess = true,
                TotalRows = items.Count,
                Message = "Validation passed. Ready to import."
            };
        }

        // Step 5: Process import
        var result = await ProcessImportAsync(items, categories);

        _logger.LogInformation(
            "[{Service}] BulkImportAsync - Completed - Imported: {Count}",
            nameof(ProductAppService), result.SuccessCount);

        return result;
    }

    private void ValidateFile(IFormFile file)
    {
        var extension = Path.GetExtension(file.FileName).ToLowerInvariant();

        if (!BulkImportFileExtensions.Allowed.Contains(extension))
        {
            throw new UserFriendlyException(
                $"Invalid file type. Allowed: {string.Join(", ", BulkImportFileExtensions.Allowed)}");
        }

        if (file.Length > BulkImportFileExtensions.MaxFileSize)
        {
            throw new UserFriendlyException(
                $"File size exceeds maximum allowed ({BulkImportFileExtensions.MaxFileSize / 1024 / 1024}MB)");
        }
    }

    private async Task<List<BulkImportProductDto>> ParseExcelAsync(IFormFile file)
    {
        using var stream = new MemoryStream();
        await file.CopyToAsync(stream);
        stream.Position = 0;

        // Register encoding provider for older Excel formats
        System.Text.Encoding.RegisterProvider(
            System.Text.CodePagesEncodingProvider.Instance);

        using var importer = new ExcelImporter(stream);
        var sheet = importer.ReadSheet();

        return sheet.ReadRows<BulkImportProductDto>()
            .Where(x => !string.IsNullOrWhiteSpace(x.ProductCode))
            .ToList();
    }

    private async Task<List<BulkImportErrorDto>> ValidateImportDataAsync(
        List<BulkImportProductDto> items,
        List<Category> categories)
    {
        var errors = new List<BulkImportErrorDto>();
        var existingCodes = await GetExistingProductCodesAsync();

        for (int i = 0; i < items.Count; i++)
        {
            var rowNumber = i + 2; // Excel row (1-based + header)
            var item = items[i];

            // Trim inputs
            item.ProductCode = item.ProductCode?.Trim()?.ToUpperInvariant();
            item.Name = item.Name?.Trim();
            item.CategoryName = item.CategoryName?.Trim();

            // Validate required fields
            if (string.IsNullOrWhiteSpace(item.ProductCode))
            {
                errors.Add(new BulkImportErrorDto(rowNumber, "ProductCode", "Product Code is required"));
            }

            if (string.IsNullOrWhiteSpace(item.Name))
            {
                errors.Add(new BulkImportErrorDto(rowNumber, "Name", "Product Name is required"));
            }

            // Validate numeric fields
            if (!decimal.TryParse(item.PriceText, out var price) || price < 0)
            {
                errors.Add(new BulkImportErrorDto(rowNumber, "Price", $"Invalid price: {item.PriceText}"));
            }
            else
            {
                item.Price = Math.Round(price, 2);
            }

            if (!int.TryParse(item.StockText, out var stock) || stock < 0)
            {
                errors.Add(new BulkImportErrorDto(rowNumber, "Stock", $"Invalid stock: {item.StockText}"));
            }
            else
            {
                item.Stock = stock;
            }

            // Validate duplicates within file
            var duplicates = items
                .Select((x, idx) => (Item: x, Index: idx))
                .Where(x => x.Index != i &&
                    x.Item.ProductCode?.ToUpperInvariant() == item.ProductCode)
                .Select(x => $"Row {x.Index + 2}");

            if (duplicates.Any())
            {
                errors.Add(new BulkImportErrorDto(
                    rowNumber,
                    "ProductCode",
                    $"Duplicate in file: {string.Join(", ", duplicates)}"));
            }

            // Validate against existing data
            if (existingCodes.Contains(item.ProductCode))
            {
                errors.Add(new BulkImportErrorDto(
                    rowNumber,
                    "ProductCode",
                    $"Product code already exists: {item.ProductCode}"));
            }

            // Validate category
            if (!string.IsNullOrWhiteSpace(item.CategoryName))
            {
                var category = categories.FirstOrDefault(
                    c => c.Name.Equals(item.CategoryName, StringComparison.OrdinalIgnoreCase));

                if (category == null)
                {
                    errors.Add(new BulkImportErrorDto(
                        rowNumber,
                        "Category",
                        $"Category not found: {item.CategoryName}"));
                }
                else
                {
                    item.CategoryId = category.Id;
                }
            }
        }

        return errors;
    }

    private async Task<HashSet<string>> GetExistingProductCodesAsync()
    {
        var codes = await _productRepository
            .GetQueryableAsync()
            .ContinueWith(q => q.Result
                .Select(p => p.ProductCode.ToUpperInvariant())
                .ToHashSet());

        return codes;
    }

    private async Task<BulkImportResultDto> ProcessImportAsync(
        List<BulkImportProductDto> items,
        List<Category> categories)
    {
        var products = items.Select(item => new Product(
            GuidGenerator.Create(),
            item.ProductCode,
            item.Name,
            item.Price,
            item.Stock)
        {
            CategoryId = item.CategoryId
        }).ToList();

        await _productRepository.InsertManyAsync(products);

        return new BulkImportResultDto
        {
            IsSuccess = true,
            TotalRows = items.Count,
            SuccessCount = products.Count,
            Message = $"Successfully imported {products.Count} products"
        };
    }
}
```

### 4. Result DTOs

```csharp
public class BulkImportResultDto
{
    public bool IsSuccess { get; set; }
    public int TotalRows { get; set; }
    public int SuccessCount { get; set; }
    public int ErrorCount { get; set; }
    public string Message { get; set; }
    public List<BulkImportErrorDto> Errors { get; set; } = new();
}

public class BulkImportErrorDto
{
    public int RowNumber { get; set; }
    public string Field { get; set; }
    public string Message { get; set; }

    public BulkImportErrorDto() { }

    public BulkImportErrorDto(int rowNumber, string field, string message)
    {
        RowNumber = rowNumber;
        Field = field;
        Message = message;
    }
}
```

## Bulk Update Pattern

### 1. Bulk Update from Excel

```csharp
public async Task<BulkImportResultDto> BulkUpdateAsync(BulkImportFileDto input)
{
    _logger.LogInformation("[{Service}] BulkUpdateAsync - Started", nameof(ProductAppService));

    ValidateFile(input.File);
    var items = await ParseExcelAsync(input.File);

    // Load existing products
    var productCodes = items
        .Select(x => x.ProductCode?.Trim()?.ToUpperInvariant())
        .Where(x => !string.IsNullOrEmpty(x))
        .ToList();

    var existingProducts = await _productRepository
        .GetListAsync(p => productCodes.Contains(p.ProductCode.ToUpper()));

    var errors = new List<BulkImportErrorDto>();
    var productsToUpdate = new List<Product>();

    foreach (var (item, index) in items.Select((x, i) => (x, i)))
    {
        var rowNumber = index + 2;
        item.ProductCode = item.ProductCode?.Trim()?.ToUpperInvariant();

        var product = existingProducts.FirstOrDefault(
            p => p.ProductCode.ToUpperInvariant() == item.ProductCode);

        if (product == null)
        {
            errors.Add(new BulkImportErrorDto(
                rowNumber, "ProductCode", $"Product not found: {item.ProductCode}"));
            continue;
        }

        // Update fields if provided
        if (!string.IsNullOrWhiteSpace(item.Name))
        {
            product.SetName(item.Name.Trim());
        }

        if (decimal.TryParse(item.PriceText, out var price))
        {
            product.SetPrice(Math.Round(price, 2));
        }

        if (int.TryParse(item.StockText, out var stock))
        {
            product.SetStock(stock);
        }

        productsToUpdate.Add(product);
    }

    if (errors.Any())
    {
        return new BulkImportResultDto
        {
            IsSuccess = false,
            TotalRows = items.Count,
            ErrorCount = errors.Count,
            Errors = errors
        };
    }

    if (productsToUpdate.Any())
    {
        await _productRepository.UpdateManyAsync(productsToUpdate);
    }

    _logger.LogInformation(
        "[{Service}] BulkUpdateAsync - Completed - Updated: {Count}",
        nameof(ProductAppService), productsToUpdate.Count);

    return new BulkImportResultDto
    {
        IsSuccess = true,
        TotalRows = items.Count,
        SuccessCount = productsToUpdate.Count,
        Message = $"Successfully updated {productsToUpdate.Count} products"
    };
}
```

### 2. Bulk Update from List

```csharp
public async Task<BulkImportResultDto> BulkUpdateFromListAsync(
    List<UpdateProductDto> items)
{
    var ids = items.Select(x => x.Id).ToList();

    var products = await _productRepository
        .GetListAsync(p => ids.Contains(p.Id));

    var productsToUpdate = (
        from product in products
        join item in items on product.Id equals item.Id
        select UpdateProduct(product, item)
    ).ToList();

    await _productRepository.UpdateManyAsync(productsToUpdate);

    return new BulkImportResultDto
    {
        IsSuccess = true,
        SuccessCount = productsToUpdate.Count
    };
}

private Product UpdateProduct(Product product, UpdateProductDto input)
{
    product.SetName(input.Name?.Trim() ?? product.Name);
    product.SetPrice(input.Price ?? product.Price);
    product.SetStock(input.Stock ?? product.Stock);
    return product;
}
```

## Excel Export Pattern

```csharp
public async Task<FileDto> ExportToExcelAsync(ProductFilter filter)
{
    _logger.LogInformation("[{Service}] ExportToExcelAsync - Started", nameof(ProductAppService));

    var products = await GetFilteredProductsAsync(filter);

    var exportData = products.Select(p => new ProductExportDto
    {
        ProductCode = p.ProductCode,
        Name = p.Name,
        Price = p.Price,
        Stock = p.Stock,
        CategoryName = p.Category?.Name,
        CreatedAt = p.CreationTime
    }).ToList();

    using var stream = new MemoryStream();

    // Using ExcelMapper for export
    var excel = new ExcelMapper();
    excel.Save(stream, exportData, "Products");

    var fileName = $"Products_{DateTime.Now:yyyyMMdd_HHmmss}.xlsx";

    // Save to blob storage
    await _fileContainer.SaveAsync(fileName, stream.ToArray());

    return new FileDto
    {
        FileName = fileName,
        Content = stream.ToArray(),
        ContentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    };
}
```

## Blob Storage for Templates

```csharp
// File container definition
[BlobContainerName("bulk-import-templates")]
public class BulkImportTemplateContainer { }

// Get template
public async Task<FileDto> GetImportTemplateAsync()
{
    const string templateFileName = "ProductImportTemplate.xlsx";

    var content = await _fileContainer.GetAllBytesAsync(templateFileName);

    if (content == null)
    {
        throw new UserFriendlyException("Import template not found");
    }

    return new FileDto
    {
        FileName = templateFileName,
        Content = content,
        ContentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    };
}
```

## Batch Processing with Progress

```csharp
public async Task<BulkImportResultDto> ProcessLargeBatchAsync(
    List<CreateProductDto> items,
    IProgress<int> progress = null)
{
    const int batchSize = 100;
    var batches = items.Chunk(batchSize).ToList();
    var totalProcessed = 0;
    var errors = new List<BulkImportErrorDto>();

    foreach (var (batch, batchIndex) in batches.Select((b, i) => (b, i)))
    {
        try
        {
            var products = batch.Select(item => new Product(
                GuidGenerator.Create(),
                item.ProductCode,
                item.Name,
                item.Price,
                item.Stock
            )).ToList();

            await _productRepository.InsertManyAsync(products);

            totalProcessed += batch.Length;
            progress?.Report((int)((double)totalProcessed / items.Count * 100));

            _logger.LogInformation(
                "Processed batch {BatchIndex}/{TotalBatches}, Total: {Total}",
                batchIndex + 1, batches.Count, totalProcessed);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to process batch {BatchIndex}", batchIndex);
            errors.Add(new BulkImportErrorDto(
                batchIndex * batchSize,
                "Batch",
                $"Batch {batchIndex + 1} failed: {ex.Message}"));
        }
    }

    return new BulkImportResultDto
    {
        IsSuccess = !errors.Any(),
        TotalRows = items.Count,
        SuccessCount = totalProcessed,
        ErrorCount = errors.Count,
        Errors = errors
    };
}
```

## Controller Implementation

```csharp
[Route("api/products")]
public class ProductController : AbpController
{
    private readonly IProductAppService _productAppService;

    [HttpPost("bulk-import")]
    [Consumes("multipart/form-data")]
    public async Task<BulkImportResultDto> BulkImportAsync(
        [FromForm] BulkImportFileDto input)
    {
        return await _productAppService.BulkImportAsync(input);
    }

    [HttpPost("bulk-update")]
    [Consumes("multipart/form-data")]
    public async Task<BulkImportResultDto> BulkUpdateAsync(
        [FromForm] BulkImportFileDto input)
    {
        return await _productAppService.BulkUpdateAsync(input);
    }

    [HttpGet("export")]
    public async Task<IActionResult> ExportAsync([FromQuery] ProductFilter filter)
    {
        var file = await _productAppService.ExportToExcelAsync(filter);
        return File(file.Content, file.ContentType, file.FileName);
    }

    [HttpGet("import-template")]
    public async Task<IActionResult> GetTemplateAsync()
    {
        var file = await _productAppService.GetImportTemplateAsync();
        return File(file.Content, file.ContentType, file.FileName);
    }
}
```

## Best Practices

1. **Always validate first** - Parse and validate all rows before any database operations
2. **Use transactions** - ABP's UoW handles this automatically for `InsertManyAsync`/`UpdateManyAsync`
3. **Batch large operations** - Process in chunks of 100-500 records
4. **Report progress** - Use `IProgress<T>` for long-running operations
5. **Log comprehensively** - Log start, end, batch progress, and errors
6. **Provide templates** - Store import templates in blob storage
7. **Validate duplicates** - Check both within file and against existing data
8. **Trim inputs** - Always trim and normalize string inputs
9. **Handle encoding** - Register `CodePagesEncodingProvider` for older Excel formats
10. **Return detailed errors** - Include row number and field for each validation error

## References

- [Excel Import Templates](references/excel-templates.md)
- [Validation Patterns](references/validation-patterns.md)
