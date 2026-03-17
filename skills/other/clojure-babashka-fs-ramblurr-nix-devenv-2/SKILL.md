---
name: clojure-babashka-fs
description: File system operations with babashka.fs. Use when working with file I/O, directory traversal, path manipulation, file copying/moving, temp files, archives (zip/gzip), or file metadata.
---

# babashka.fs

Cross-platform file system utilities for Clojure. Built on java.nio, works in JVM Clojure and babashka (built-in since v0.2.9).

## Setup

deps.edn:
```clojure
babashka/fs {:mvn/version "0.5.27"}
```

Leiningen:
```clojure
[babashka/fs "0.5.27"]
```

See https://clojars.org/babashka/fs for the latest version.

Note: Built into babashka, no dependency needed if using bb.

## Quick Start

```clojure
(require '[babashka.fs :as fs])

;; Check file types
(fs/directory? ".")          ;; => true
(fs/exists? "project.clj")   ;; => true
(fs/regular-file? "README")  ;; => true

;; Path manipulation
(str (fs/path "src" "app" "core.clj"))
;; => "src/app/core.clj"

(str (fs/absolutize "."))
;; => "/home/user/project"

;; List directory
(map str (fs/list-dir "src"))
;; => ("src/app" "src/test")

;; Find files
(map str (fs/glob "." "**/*.clj"))
;; => ("src/app/core.clj" "test/app/core_test.clj")
```

## Common Operations

### Path Creation and Manipulation

```clojure
;; Build paths
(fs/path "home" "user" "file.txt")     ;; => #object[java.nio.file.Path]
(fs/file "home" "user" "file.txt")     ;; => #object[java.io.File]

;; Expand home directory
(fs/expand-home "~/projects")
;; => #object[java.nio.file.Path "/home/user/projects"]

;; Get components
(fs/file-name "/path/to/file.txt")     ;; => "file.txt"
(fs/parent "/path/to/file.txt")        ;; => #object[Path "/path/to"]
(fs/extension "file.clj")              ;; => "clj"
(split-ext "file.tar.gz")              ;; => ["file.tar" "gz"]
(strip-ext "file.clj")                 ;; => "file"

;; Normalize and resolve
(fs/normalize "path/./to/../file")     ;; => "path/file"
(fs/absolutize "src")                  ;; => "/home/user/project/src"
(fs/canonicalize "src")                ;; => resolves symlinks + normalizes
(fs/real-path "src")                   ;; => like canonicalize, requires existence
```

### Directory Listing and Searching

```clojure
;; List immediate children
(fs/list-dir "src")
;; => [#object[Path "src/core.clj"] #object[Path "src/util.clj"]]

;; List with glob filter
(fs/list-dir "src" "*.clj")
;; => [#object[Path "src/core.clj"]]

;; Glob search (recursive)
(fs/glob "." "**/*.clj")               ;; all .clj files
(fs/glob "." "**{.clj,.cljc}")        ;; .clj OR .cljc files

;; Match search (more control)
(fs/match "." "regex:.*\\.clj" {:recursive true})

;; Find files in PATH
(fs/which "java")
;; => #object[Path "/usr/bin/java"]

(fs/exec-paths)  ;; all PATH directories as Paths
```

### File Operations

```clojure
;; Copy
(fs/copy "src.txt" "dest.txt")
(fs/copy "src.txt" "dest.txt" {:replace-existing true})
(fs/copy-tree "src-dir" "dest-dir")    ;; recursive copy

;; Move
(fs/move "old.txt" "new.txt")
(fs/move "old.txt" "new.txt" {:replace-existing true})

;; Delete
(fs/delete "file.txt")                 ;; throws if not exists
(fs/delete-if-exists "file.txt")       ;; safe delete
(fs/delete-tree "dir")                 ;; recursive delete (rm -rf)
(fs/delete-tree "dir" {:force true})   ;; delete read-only files too
```

### Creating Files and Directories

```clojure
;; Directories
(fs/create-dir "newdir")               ;; single dir, parent must exist
(fs/create-dirs "path/to/newdir")      ;; like mkdir -p

;; Files
(fs/create-file "empty.txt")

;; Temporary
(fs/create-temp-dir)
(fs/create-temp-dir {:prefix "myapp-"})
(fs/create-temp-file)
(fs/create-temp-file {:prefix "log-" :suffix ".txt"})

;; With auto-cleanup
(fs/with-temp-dir [tmp]
  (fs/create-file (fs/path tmp "work.txt"))
  ;; ... do work ...
  ) ;; tmp deleted here
```

### Reading and Writing

```clojure
;; Read
(fs/read-all-bytes "file.bin")         ;; => byte[]
(fs/read-all-lines "file.txt")         ;; => ["line1" "line2"]

;; Write
(fs/write-bytes "out.bin" byte-array)
(fs/write-lines "out.txt" ["line1" "line2"])
(fs/write-lines "out.txt" ["more"] {:append true})

;; Update in place
(fs/update-file "config.edn"
  #(str/replace % "localhost" "prod.example.com"))
```

### File Metadata

```clojure
;; Timestamps
(fs/creation-time "file.txt")          ;; => FileTime
(fs/last-modified-time "file.txt")     ;; => FileTime
(fs/file-time->millis (fs/last-modified-time "file.txt"))

;; Set timestamps
(fs/set-last-modified-time "file.txt" (System/currentTimeMillis))

;; Size
(fs/size "file.txt")                   ;; => bytes

;; Permissions (Unix/Linux)
(fs/posix-file-permissions "file.sh")
(fs/posix->str (fs/posix-file-permissions "file.sh"))
;; => "rwxr-xr-x"
(fs/set-posix-file-permissions "file.sh" "rwx------")

;; Owner
(str (fs/owner "file.txt"))            ;; => "username"
```

### Archives

```clojure
;; Zip
(fs/zip "archive.zip" ["file1.txt" "dir/file2.txt"])
(fs/zip "archive.zip" ["src"] {:root "src"})  ;; elide "src/" in archive

;; Unzip
(fs/unzip "archive.zip")               ;; extract to current dir
(fs/unzip "archive.zip" "dest-dir")
(fs/unzip "archive.zip" "dest-dir" {:replace-existing true})

;; Gzip
(fs/gzip "file.txt")                   ;; creates file.txt.gz
(fs/gzip "file.txt" {:out-file "archive.gz"})

;; Gunzip
(fs/gunzip "file.txt.gz")              ;; extracts to current dir
(fs/gunzip "file.txt.gz" "dest-dir")
```

### Symbolic Links

```clojure
;; Check
(fs/sym-link? "link")                  ;; => true/false

;; Create
(fs/create-sym-link "link" "target")
(fs/create-link "hardlink" "existing") ;; hard link

;; Read target
(fs/read-link "link")                  ;; => Path to target
```

## Advanced Patterns

### Walking File Trees

```clojure
;; Low-level tree walker
(fs/walk-file-tree "src"
  {:pre-visit-dir (fn [dir attrs]
                    (println "Entering" dir)
                    :continue)
   :visit-file (fn [file attrs]
                 (println "File:" file)
                 :continue)})

;; Find modified files
(fs/modified-since "build/last-build-marker"
                   (fs/glob "src" "**/*.clj"))
;; => seq of files newer than marker
```

### XDG Directories

```clojure
;; Standard user directories
(fs/xdg-config-home)       ;; => ~/.config
(fs/xdg-config-home "myapp") ;; => ~/.config/myapp
(fs/xdg-data-home)         ;; => ~/.local/share
(fs/xdg-cache-home)        ;; => ~/.cache
(fs/xdg-state-home)        ;; => ~/.local/state

;; Respects XDG_CONFIG_HOME etc. env vars
```

### Cross-Platform Paths

```clojure
;; Use forward slashes on all platforms
(fs/unixify "C:\\Users\\name\\file.txt")
;; => "C:/Users/name/file.txt"

;; Separators
fs/file-separator  ;; "/" or "\\" depending on OS
fs/path-separator  ;; ":" or ";" for PATH-like strings

;; Platform detection
(fs/windows?)      ;; => true on Windows
```

## Key Gotchas

1. **Empty string means cwd**: `(fs/list-dir "")` is same as `(fs/list-dir ".")`. Most functions treat `""` as current directory.

2. **Symlink following**: Many functions accept `:nofollow-links` or `:follow-links` options. Default behavior varies:
   - Most operations follow symlinks by default
   - Tree walking does NOT follow symlinks unless `:follow-links true`
   - See [README](references/API.md) for function-specific defaults

3. **creation-time is unreliable**: Behavior varies by OS and Java version. On Linux it often returns modified time. See [API notes](references/API.md#creation-time).

4. **glob patterns use java.nio syntax**:
   - `*` matches within directory (not across `/`)
   - `**` matches across directories
   - `{.clj,.cljc}` for alternation
   - See [FileSystem#getPathMatcher](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/nio/file/FileSystem.html#getPathMatcher(java.lang.String))

5. **Paths vs Files**: Functions return `java.nio.file.Path` objects. Use `str` to convert to string, or `fs/file` to convert to `java.io.File`.

6. **Maps are closed by default in newer glob**: Recent versions of fs set `{:hidden false}` by default unless pattern starts with `.`

## References

- [Complete API Reference](references/API.md) - All functions with detailed docs
- GitHub: https://github.com/babashka/fs
- Clojars: https://clojars.org/babashka/fs
