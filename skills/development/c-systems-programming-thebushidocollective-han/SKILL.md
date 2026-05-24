---
name: c-systems-programming
description: Use when c systems programming including file I/O, processes, signals, and system calls for low-level system interaction.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# C Systems Programming

Systems programming in C provides direct access to operating system resources
through system calls, enabling control over files, processes, signals, and
inter-process communication. This skill covers essential systems programming
patterns for building robust low-level applications.

## File I/O Operations

C provides both standard library I/O (buffered) and system-level I/O
(unbuffered) operations. Understanding when to use each is crucial for
performance and correctness.

### Standard I/O Functions

Standard I/O provides buffering and convenience functions for common operations.

```c
#include <stdio.h>
#include <stdlib.h>

// Reading and writing with standard I/O
int file_copy_stdio(const char *src, const char *dst) {
    FILE *source = fopen(src, "rb");
    if (!source) {
        perror("Failed to open source");
        return -1;
    }

    FILE *dest = fopen(dst, "wb");
    if (!dest) {
        perror("Failed to open destination");
        fclose(source);
        return -1;
    }

    char buffer[4096];
    size_t bytes;
    while ((bytes = fread(buffer, 1, sizeof(buffer), source)) > 0) {
        if (fwrite(buffer, 1, bytes, dest) != bytes) {
            perror("Write failed");
            fclose(source);
            fclose(dest);
            return -1;
        }
    }

    if (ferror(source)) {
        perror("Read failed");
        fclose(source);
        fclose(dest);
        return -1;
    }

    fclose(source);
    fclose(dest);
    return 0;
}
```

### System-Level I/O

System calls provide direct access to kernel I/O operations without buffering.

```c
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

// Reading and writing with system calls
int file_copy_syscall(const char *src, const char *dst) {
    int source_fd = open(src, O_RDONLY);
    if (source_fd == -1) {
        perror("Failed to open source");
        return -1;
    }

    int dest_fd = open(dst, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (dest_fd == -1) {
        perror("Failed to open destination");
        close(source_fd);
        return -1;
    }

    char buffer[4096];
    ssize_t bytes_read, bytes_written;

    while ((bytes_read = read(source_fd, buffer, sizeof(buffer))) > 0) {
        bytes_written = write(dest_fd, buffer, bytes_read);
        if (bytes_written != bytes_read) {
            perror("Write failed");
            close(source_fd);
            close(dest_fd);
            return -1;
        }
    }

    if (bytes_read == -1) {
        perror("Read failed");
        close(source_fd);
        close(dest_fd);
        return -1;
    }

    close(source_fd);
    close(dest_fd);
    return 0;
}
```

## Process Management

Creating and managing processes is fundamental to systems programming. The
`fork()` and `exec()` family of functions enable process creation and execution.

```c
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

// Create child process and execute command
int execute_command(const char *program, char *const argv[]) {
    pid_t pid = fork();

    if (pid == -1) {
        perror("fork failed");
        return -1;
    }

    if (pid == 0) {
        // Child process
        execvp(program, argv);
        // execvp only returns on error
        perror("execvp failed");
        exit(EXIT_FAILURE);
    }

    // Parent process
    int status;
    pid_t waited = waitpid(pid, &status, 0);

    if (waited == -1) {
        perror("waitpid failed");
        return -1;
    }

    if (WIFEXITED(status)) {
        return WEXITSTATUS(status);
    } else if (WIFSIGNALED(status)) {
        fprintf(stderr, "Child terminated by signal %d\n",
                WTERMSIG(status));
        return -1;
    }

    return -1;
}
```

## Signal Handling

Signals provide asynchronous event notification. Proper signal handling is
essential for graceful shutdown and error recovery.

```c
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>

// Global flag for signal handling
static volatile sig_atomic_t keep_running = 1;

// Signal handler for graceful shutdown
void signal_handler(int signum) {
    if (signum == SIGINT || signum == SIGTERM) {
        keep_running = 0;
    }
}

// Setup signal handlers
int setup_signals(void) {
    struct sigaction sa;
    sa.sa_handler = signal_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;

    if (sigaction(SIGINT, &sa, NULL) == -1) {
        perror("sigaction SIGINT");
        return -1;
    }

    if (sigaction(SIGTERM, &sa, NULL) == -1) {
        perror("sigaction SIGTERM");
        return -1;
    }

    return 0;
}

// Main loop with signal handling
void run_with_signals(void) {
    if (setup_signals() == -1) {
        return;
    }

    while (keep_running) {
        // Do work
        sleep(1);
        printf("Working...\n");
    }

    printf("Shutting down gracefully\n");
}
```

## Inter-Process Communication

Pipes enable communication between related processes, commonly used for
command pipelines and parent-child communication.

```c
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>

// Create a pipeline: ls | wc -l
int pipeline_example(void) {
    int pipefd[2];

    if (pipe(pipefd) == -1) {
        perror("pipe");
        return -1;
    }

    pid_t pid1 = fork();
    if (pid1 == -1) {
        perror("fork");
        return -1;
    }

    if (pid1 == 0) {
        // First child: ls
        close(pipefd[0]);  // Close read end
        dup2(pipefd[1], STDOUT_FILENO);
        close(pipefd[1]);
        execlp("ls", "ls", NULL);
        perror("execlp ls");
        exit(EXIT_FAILURE);
    }

    pid_t pid2 = fork();
    if (pid2 == -1) {
        perror("fork");
        return -1;
    }

    if (pid2 == 0) {
        // Second child: wc -l
        close(pipefd[1]);  // Close write end
        dup2(pipefd[0], STDIN_FILENO);
        close(pipefd[0]);
        execlp("wc", "wc", "-l", NULL);
        perror("execlp wc");
        exit(EXIT_FAILURE);
    }

    // Parent
    close(pipefd[0]);
    close(pipefd[1]);

    waitpid(pid1, NULL, 0);
    waitpid(pid2, NULL, 0);

    return 0;
}
```

## File Locking

File locking prevents concurrent access issues in multi-process environments.

```c
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>

// Advisory file locking
int lock_file(int fd, int lock_type) {
    struct flock fl;
    fl.l_type = lock_type;    // F_RDLCK, F_WRLCK, F_UNLCK
    fl.l_whence = SEEK_SET;
    fl.l_start = 0;
    fl.l_len = 0;             // Lock entire file
    fl.l_pid = getpid();

    if (fcntl(fd, F_SETLKW, &fl) == -1) {
        perror("fcntl");
        return -1;
    }

    return 0;
}

// Write to file with exclusive lock
int write_locked(const char *filename, const char *data) {
    int fd = open(filename, O_WRONLY | O_CREAT | O_APPEND, 0644);
    if (fd == -1) {
        perror("open");
        return -1;
    }

    // Acquire exclusive lock
    if (lock_file(fd, F_WRLCK) == -1) {
        close(fd);
        return -1;
    }

    // Write data
    ssize_t written = write(fd, data, strlen(data));
    if (written == -1) {
        perror("write");
        lock_file(fd, F_UNLCK);
        close(fd);
        return -1;
    }

    // Release lock
    lock_file(fd, F_UNLCK);
    close(fd);

    return 0;
}
```

## Directory Operations

Working with directories requires understanding directory streams and entry
manipulation.

```c
#include <dirent.h>
#include <sys/stat.h>
#include <stdio.h>
#include <string.h>

// List all files in directory recursively
void list_directory(const char *path, int indent) {
    DIR *dir = opendir(path);
    if (!dir) {
        perror("opendir");
        return;
    }

    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        // Skip . and ..
        if (strcmp(entry->d_name, ".") == 0 ||
            strcmp(entry->d_name, "..") == 0) {
            continue;
        }

        // Print with indentation
        for (int i = 0; i < indent; i++) {
            printf("  ");
        }
        printf("%s", entry->d_name);

        // Check if directory
        char fullpath[1024];
        snprintf(fullpath, sizeof(fullpath), "%s/%s", path,
                 entry->d_name);

        struct stat statbuf;
        if (stat(fullpath, &statbuf) == 0) {
            if (S_ISDIR(statbuf.st_mode)) {
                printf("/\n");
                list_directory(fullpath, indent + 1);
            } else {
                printf(" (%ld bytes)\n", statbuf.st_size);
            }
        } else {
            printf("\n");
        }
    }

    closedir(dir);
}
```

## Error Handling in System Calls

Proper error handling is critical in systems programming. System calls
indicate errors through return values and `errno`.

```c
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

// Robust file operation with error handling
int safe_file_operation(const char *filename) {
    int fd = open(filename, O_RDONLY);
    if (fd == -1) {
        switch (errno) {
            case ENOENT:
                fprintf(stderr, "File not found: %s\n", filename);
                break;
            case EACCES:
                fprintf(stderr, "Permission denied: %s\n", filename);
                break;
            default:
                fprintf(stderr, "Error opening %s: %s\n",
                        filename, strerror(errno));
        }
        return -1;
    }

    char buffer[1024];
    ssize_t bytes_read;

    while ((bytes_read = read(fd, buffer, sizeof(buffer))) > 0) {
        // Process data
        write(STDOUT_FILENO, buffer, bytes_read);
    }

    if (bytes_read == -1) {
        fprintf(stderr, "Error reading: %s\n", strerror(errno));
        close(fd);
        return -1;
    }

    if (close(fd) == -1) {
        fprintf(stderr, "Error closing file: %s\n", strerror(errno));
        return -1;
    }

    return 0;
}
```

## Best Practices

1. Always check return values from system calls and handle errors appropriately
2. Use `errno` and `strerror()` for detailed error reporting
3. Close file descriptors and free resources in all code paths including errors
4. Use `sigaction()` instead of deprecated `signal()` for signal handling
5. Avoid blocking operations in signal handlers; use `sig_atomic_t` flags
6. Prefer standard I/O for buffered operations; use syscalls for direct control
7. Use advisory locks consistently across all processes accessing shared files
8. Set appropriate file permissions using umask or explicit mode bits
9. Handle `EINTR` errors by retrying interrupted system calls when appropriate
10. Use `waitpid()` to prevent zombie processes and handle child termination

## Common Pitfalls

1. Forgetting to check return values from system calls leading to silent errors
2. Using `signal()` instead of `sigaction()`, missing important control flags
3. Performing complex operations in signal handlers causing race conditions
4. Not closing file descriptors in error paths, causing resource leaks
5. Mixing buffered and unbuffered I/O on same file, causing data corruption
6. Forgetting to wait for child processes, creating zombie processes
7. Using unsafe functions in signal handlers (printf, malloc, etc.)
8. Not handling `EINTR` errors, causing premature operation termination
9. Ignoring race conditions in file operations without proper locking
10. Using `kill()` without checking if process exists, sending signals to wrong
    processes

## When to Use C Systems Programming

Use C systems programming when you need:

- Direct access to operating system resources and kernel interfaces
- Maximum control over process execution and resource management
- Low-level I/O operations without buffering overhead
- Building system utilities, daemons, or services
- Inter-process communication using pipes, signals, or shared memory
- Fine-grained control over file operations and permissions
- Signal handling for graceful shutdown and error recovery
- High-performance applications requiring minimal overhead
- Interfacing with legacy systems or porting Unix utilities
- Understanding how higher-level abstractions work under the hood

## Resources

- [Advanced Programming in the UNIX Environment](https://www.apuebook.com/)
- [The Linux Programming Interface](https://man7.org/tlpi/)
- [POSIX Standards Documentation](https://pubs.opengroup.org/onlinepubs/9699919799/)
- [Linux System Programming](https://www.oreilly.com/library/view/linux-system-programming/9781449341527/)
