---
name: east-node-io
description: "I/O platform functions for the East language on Node.js. Use when writing East programs that need SQL databases (SQLite, PostgreSQL, MySQL), NoSQL databases (Redis, MongoDB), S3 storage, file transfers (FTP, SFTP), file format parsing (XLSX, XML), or compression (Gzip, Zip, Tar). Triggers for: (1) Writing East programs with @elaraai/east-node-io, (2) Database operations with SQL.SQLite, SQL.Postgres, SQL.MySQL, NoSQL.Redis, NoSQL.MongoDB, (3) Cloud storage with Storage.S3, (4) File transfers with Transfer.FTP, Transfer.SFTP, (5) Format parsing with Format.XLSX, Format.XML, (6) Compression with Compression.Gzip, Compression.Zip, Compression.Tar."
---

# East Node IO

I/O platform functions for the East language on Node.js. Enables East programs to interact with databases, cloud storage, file transfers, and data formats.

## Quick Start

```typescript
import { East, StringType, NullType } from "@elaraai/east";
import { SQL, Storage } from "@elaraai/east-node-io";

const queryDatabase = East.function([StringType], NullType, ($, userId) => {
    const config = $.let({
        host: "localhost",
        port: 5432n,
        database: "myapp",
        user: "postgres",
        password: "secret",
        ssl: East.variant('none', null),
        maxConnections: East.variant('none', null),
    });

    const conn = $.let(SQL.Postgres.connect(config));
    $(SQL.Postgres.query(conn, "SELECT * FROM users WHERE id = $1", [East.variant("Integer", 42n)]));
    $(SQL.Postgres.close(conn));
});

// Compile with specific module Implementation
const compiled = East.compileAsync(queryDatabase.toIR(), SQL.Postgres.Implementation);
await compiled("user123");
```

## Decision Tree: Which Module to Use

```
Task → What do you need?
    │
    ├─ SQL Database
    │   ├─ SQL.SQLite (embedded, placeholder: ?)
    │   │   └─ .connect(), .query(), .close()
    │   ├─ SQL.Postgres (placeholder: $1, $2, ...)
    │   │   └─ .connect(), .query(), .close()
    │   └─ SQL.MySQL (placeholder: ?)
    │       └─ .connect(), .query(), .close()
    │
    ├─ NoSQL Database
    │   ├─ NoSQL.Redis (key-value cache)
    │   │   └─ .connect(), .get(), .set(), .setex(), .del(), .close()
    │   └─ NoSQL.MongoDB (document store)
    │       └─ .connect(), .insertOne(), .findOne(), .find(), .updateOne(), .deleteOne(), .close()
    │
    ├─ Storage.S3 (S3-compatible object storage)
    │   └─ .putObject(), .getObject(), .deleteObject(), .headObject(), .listObjects(), .presignUrl()
    │
    ├─ Transfer (file transfers)
    │   ├─ Transfer.FTP
    │   │   └─ .connect(), .put(), .get(), .list(), .delete(), .close()
    │   └─ Transfer.SFTP
    │       └─ .connect(), .put(), .get(), .list(), .delete(), .close()
    │
    ├─ Format (file parsing)
    │   ├─ Format.XLSX (Excel spreadsheets)
    │   │   └─ .read(), .write(), .info()
    │   └─ Format.XML
    │       └─ .parse(), .serialize()
    │
    └─ Compression
        ├─ Compression.Gzip (single file)
        │   └─ .compress(), .decompress()
        ├─ Compression.Zip (archive)
        │   └─ .compress(), .decompress()
        └─ Compression.Tar (archive)
            └─ .create(), .extract()
```

## Compiling East Programs

**Use specific module implementations:**
```typescript
// Single module
const compiled = East.compileAsync(myFunction.toIR(), SQL.Postgres.Implementation);

// Multiple modules
const compiled = East.compileAsync(
    myFunction.toIR(),
    [...SQL.Postgres.Implementation, ...Storage.S3.Implementation]
);
```

## Reference Documentation

- **[API Reference](./reference/api.md)** - Complete function signatures, types, and arguments for all modules
- **[Examples](./reference/examples.md)** - Working code examples by use case

## Available Modules

| Module | Import | Purpose |
|--------|--------|---------|
| SQL.SQLite | `import { SQL } from "@elaraai/east-node-io"` | SQLite database (placeholder: `?`) |
| SQL.Postgres | `import { SQL } from "@elaraai/east-node-io"` | PostgreSQL database (placeholder: `$1`, `$2`) |
| SQL.MySQL | `import { SQL } from "@elaraai/east-node-io"` | MySQL database (placeholder: `?`) |
| Storage.S3 | `import { Storage } from "@elaraai/east-node-io"` | S3 and S3-compatible storage |
| Transfer.FTP | `import { Transfer } from "@elaraai/east-node-io"` | FTP file transfers |
| Transfer.SFTP | `import { Transfer } from "@elaraai/east-node-io"` | SFTP file transfers |
| NoSQL.Redis | `import { NoSQL } from "@elaraai/east-node-io"` | Redis key-value store |
| NoSQL.MongoDB | `import { NoSQL } from "@elaraai/east-node-io"` | MongoDB document database |
| Format.XLSX | `import { Format } from "@elaraai/east-node-io"` | Excel spreadsheet parsing |
| Format.XML | `import { Format } from "@elaraai/east-node-io"` | XML parsing and serialization |
| Compression.Gzip | `import { Compression } from "@elaraai/east-node-io"` | Gzip compression |
| Compression.Zip | `import { Compression } from "@elaraai/east-node-io"` | ZIP archive creation/extraction |
| Compression.Tar | `import { Compression } from "@elaraai/east-node-io"` | TAR archive creation/extraction |

## Accessing Types

```typescript
import { SQL, Storage, NoSQL, Format } from "@elaraai/east-node-io";

// Access types via Module.SubModule.Types.TypeName
const postgresConfig = SQL.Postgres.Types.Config;
const sqlResult = SQL.Postgres.Types.Result;
const s3Config = Storage.S3.Types.Config;
const redisConfig = NoSQL.Redis.Types.Config;
const xlsxSheet = Format.XLSX.Types.Sheet;
```

## Connection Pattern

All connection-based modules follow the same pattern:

```typescript
// 1. Create config
const config = $.let({ /* connection options */ });

// 2. Connect
const conn = $.let(Module.connect(config));

// 3. Perform operations
$(Module.operation(conn, ...args));

// 4. Close connection
$(Module.close(conn));
```
