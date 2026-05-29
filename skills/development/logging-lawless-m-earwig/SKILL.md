---
name: Logging
description: UTF-8 file logging with automatic date-based filenames and thread-safe operations for RocsMiddleware services
---

# Logging

## Instructions

When helping users implement logging in RocsMiddleware services, follow these guidelines:

1. **Command-Line Option**: Always include `--log-dir` parameter for specifying log directory path

2. **UTF-8 Encoding**: All log files must use UTF-8 encoding without BOM

3. **Automatic Filename Pattern**: Use `{ProgramName}_YYYY_MM_DD.log` format with automatic date rotation

4. **Directory Path Handling**: Smart detection - if path has no extension or ends with separator, treat as directory and use directory name as base filename

5. **Error Handling**: Include console output before logger initialization since logger may fail. Always check if `_logger` is null in exception handlers.

6. **Log Levels**: Use `LogLevel.Debug` with `--debug` flag, default to `LogLevel.Information`

7. **Thread Safety**: The UTF8Writer uses locking for concurrent writes

8. **Utf8LoggingExtensions.cs**: Copy the reference implementation to project's `Services/` directory - provides UTF8Writer, UTF8LoggerProvider, UTF8Logger, and helper methods

## Examples

### Example 1: Basic Logger Setup
```
User: Help me add logging to my RocsMiddleware service

Claude: I'll set up the standard UTF-8 file logging pattern:
- Add --log-dir command-line option
- Copy Utf8LoggingExtensions.cs to Services/
- Initialize logger with automatic date-based filename
- Add console output before logger initialization for debugging

[Provides implementation using the Logger Initialization pattern from reference material below]
```

### Example 2: Directory Path Handling
```
User: Why isn't my log file being created when I specify --log-dir?

Claude: Let me check the directory path handling. The logger should:
- Detect if path is a directory (no extension or ends with separator)
- Use directory name as base filename
- Add date string and .log extension automatically

Common issue: Old Utf8LoggingExtensions.cs without directory detection logic.
Solution: Copy the updated version from skills folder.

[Provides directory detection implementation from reference material below]
```

### Example 3: Error Handling Before Logger Init
```
User: My program just prints "Error" with no details

Claude: This happens when an exception occurs before logger initialization. I'll add:
- Console.WriteLine at key points (startup, before logger init, after logger init)
- Null check on _logger in exception handler
- Fallback to console output if logger is null

[Provides error handling pattern from reference material below]
```

---

# Reference Implementation Details

The sections below contain proven working code from RocsMiddleware services that the examples above reference.

**Reference Files in This Folder**:
- `Utf8LoggingExtensions.cs` - Complete UTF-8 logger implementation (copy to Services/)

# Standard Logging Pattern

All RocsMiddleware services use a consistent logging approach:

1. **Command-line option**: `--log-dir` parameter specifies the directory path
2. **Automatic filename generation**: `{ProgramName}_YYYY_MM_DD.log`
3. **UTF-8 encoding**: All log files use UTF-8 encoding
4. **Date rotation**: Log files automatically rotate daily based on the date

## Implementation

### Command-Line Option

```csharp
[Option("log-dir", Required = false, HelpText = "Directory for log files")]
public string? LogDir { get; set; }
```

### Logger Initialization

```csharp
// Initialize logger with optional log directory
var logLevel = options.Debug ? LogLevel.Debug : LogLevel.Information;
_logger = {Namespace}.Services.Utf8LoggingExtensions.CreateUtf8Logger(
    "{ProgramName}",
    logLevel,
    options.LogDir);
```

### Example Usage

```bash
dotnet run -- --log-dir "C:\RI Services\Logs\MyProgram" --other-options
```

This creates: `C:\RI Services\Logs\MyProgram\MyProgram_2025_10_16.log`

## Directory Path Handling

The `UTF8Writer.Init()` method automatically detects directory paths and creates properly named log files:

- If path has no extension and ends with a path separator (or exists as a directory), it's treated as a directory
- The directory name becomes the base name for the log file
- Default `.log` extension is added automatically
- Date string in format `YYYY_MM_DD` is inserted before the extension

### Examples

| Input `--log-dir`                    | Output Log File                                                    |
|--------------------------------------|---------------------------------------------------------------------|
| `C:\Logs\MyProgram`                  | `C:\Logs\MyProgram\MyProgram_2025_10_16.log`                       |
| `C:\Logs\MyProgram\`                 | `C:\Logs\MyProgram\MyProgram_2025_10_16.log`                       |
| `C:\Logs\MyProgram\custom.log`       | `C:\Logs\MyProgram\custom_2025_10_16.log`                          |
| `C:\Logs\MyProgram\custom`           | `C:\Logs\MyProgram\custom_2025_10_16.log` (adds .log extension)   |

## UTF8LoggingExtensions.cs

All services include a `Services/Utf8LoggingExtensions.cs` file that provides:

- `UTF8Writer` class: Low-level UTF-8 file writer with thread-safe locking
- `UTF8LoggerProvider`: Custom logger provider for Microsoft.Extensions.Logging
- `UTF8Logger`: ILogger implementation that writes to UTF-8 files
- `CreateUtf8Logger()`: Helper method to create a configured logger instance
- `ConfigureUtf8Logging()`: Extension method for ILoggingBuilder

## Error Handling

### Before Logger Initialization

Since the logger may fail to initialize, always include console output for early errors:

```csharp
public static async Task Main(string[] args)
{
    try
    {
        Console.WriteLine("{ProgramName} starting...");

        // Parse command line
        CommandLineOptions? options = null;
        Parser.Default.ParseArguments<CommandLineOptions>(args)
            .WithParsed(opts => options = opts)
            .WithNotParsed(errors =>
            {
                Console.WriteLine("Failed to parse command line arguments");
                Environment.Exit(1);
            });

        if (options == null)
        {
            Console.WriteLine("Failed to parse command line options");
            Environment.Exit(1);
            return;
        }

        Console.WriteLine($"Initializing logger with log-dir: {options.LogDir ?? "(null)"}");

        // Initialize logger
        _logger = {Namespace}.Services.Utf8LoggingExtensions.CreateUtf8Logger(
            "{ProgramName}",
            options.Debug ? LogLevel.Debug : LogLevel.Information,
            options.LogDir);

        Console.WriteLine("Logger initialized");

        _logger.LogInformation("{ProgramName} starting");

        // ... rest of program
    }
    catch (Exception ex)
    {
        if (_logger != null)
        {
            _logger.LogError(ex, "{ProgramName} failed: {Message}", ex.Message);
        }
        else
        {
            Console.WriteLine($"{ProgramName} failed: {ex.Message}");
            Console.WriteLine(ex.StackTrace);
        }
        Environment.Exit(1);
    }
}
```

## Log Levels

Standard log levels used across all services:

- `LogLevel.Debug`: Verbose diagnostic information (use `--debug` flag)
- `LogLevel.Information`: General informational messages (default)
- `LogLevel.Warning`: Warning messages for non-critical issues
- `LogLevel.Error`: Error messages for failures

## Real-World Examples

### PriceExtractor
```bash
dotnet run -- --pqdir "R:\Outputs\Parquets\poller" --pg "R:\JsonParams\x3rocs_db.json" --log-dir "C:\RI Services\Logs\PriceExtractor" --full
```

Creates: `C:\RI Services\Logs\PriceExtractor\PriceExtractor_2025_10_16.log`

### PriceDiscountUploader
```bash
dotnet run -- --pg "R:/JsonParams/x3rocs_db.json" --log-dir "R:/Logs/PriceDiscounter" --elastic https://rocs-stage-es.ramsden-international.com/ --debug --sphkey1 425073
```

Creates: `R:/Logs/PriceDiscounter/PriceDiscounter_2025_10_16.log`

## Benefits

1. **Consistent naming**: All services follow the same `{ProgramName}_YYYY_MM_DD.log` pattern
2. **Automatic rotation**: Daily log files without manual intervention
3. **UTF-8 encoding**: Proper support for international characters
4. **Directory-aware**: Smart handling of directory vs. file paths
5. **Optional logging**: Works without `--log-dir` (console only)
6. **Thread-safe**: Multiple threads can log simultaneously

## Common Issues

### No Log File Created

**Symptom**: Program runs but no log file appears in the specified directory.

**Causes**:
1. Old version of `Utf8LoggingExtensions.cs` without directory path handling
2. Logger initialization failing silently

**Solution**:
- Copy `Utf8LoggingExtensions.cs` from this skills folder to your project's `Services/` directory
- Add console debug output before logger initialization (see Error Handling section above)
- Check that the `UTF8Writer.Init()` method includes directory detection logic

### Program Exits with "Error" and No Details

**Symptom**: Program outputs just "Error" with no stack trace or details.

**Causes**:
1. Exception thrown before logger is initialized
2. Exception handler trying to use null logger

**Solution**:
- Add console output at key points (see Error Handling section)
- Wrap exception handler to check if `_logger` is null before using it
- Check log file was actually created and contains error details

## Related Files

- `Utf8LoggingExtensions.cs`: Reference implementation included in this folder - copy to your project's `Services/` directory
- Command-line parsing: Uses `CommandLineParser` library
- All services in RocsMiddleware follow this pattern

## Notes

- Log files are created on-demand when the first log message is written
- If `--log-dir` is not specified, logging goes to console only (if enabled)
- Parent directories are created automatically if they don't exist
- Log files are UTF-8 encoded without BOM
- The logger uses Microsoft.Extensions.Logging interfaces for compatibility
