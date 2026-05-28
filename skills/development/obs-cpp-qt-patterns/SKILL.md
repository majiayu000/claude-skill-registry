---
name: obs-cpp-qt-patterns
description: C++ and Qt integration patterns for OBS Studio plugins. Covers Qt6 Widgets for settings dialogs, CMAKE_AUTOMOC, OBS frontend API, optional Qt builds with C fallbacks, and modal dialog patterns. Use when adding UI components or C++ features to OBS plugins.
version: 1.0.0
---

# OBS C++ and Qt Patterns

## Purpose

Integrate C++ and Qt6 into OBS Studio plugins for settings dialogs, frontend API access, and rich UI components. Covers CMake configuration, optional Qt builds, and platform fallbacks.

## When NOT to Use

- Cross-compiling → Use **obs-cross-compiling**
- Windows-specific builds → Use **obs-windows-building**
- Audio plugin core logic → Use **obs-audio-plugin-writing**
- Code review → Use **obs-plugin-reviewing**

## Quick Start: Qt Settings Dialog in 5 Steps

### Step 1: Configure CMake for Qt

```cmake
cmake_minimum_required(VERSION 3.28)
project(my-plugin VERSION 1.0.0 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Enable Qt automoc (REQUIRED for Qt classes with Q_OBJECT)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)

# Find Qt6 (optional)
find_package(Qt6 COMPONENTS Widgets QUIET)
if(Qt6_FOUND)
    message(STATUS "Qt6 found - building with settings dialog")
    set(BUILD_WITH_QT ON)
else()
    message(STATUS "Qt6 not found - building without settings dialog")
    set(BUILD_WITH_QT OFF)
endif()
```

### Step 2: Add Qt Sources Conditionally

```cmake
# Core plugin (C)
add_library(${PROJECT_NAME} MODULE
    src/plugin-main.c
    src/my-source.c
)

# Add Qt frontend (C++) if available
if(BUILD_WITH_QT)
    target_sources(${PROJECT_NAME} PRIVATE src/frontend.cpp)
    target_compile_definitions(${PROJECT_NAME} PRIVATE BUILD_WITH_QT)
    target_link_libraries(${PROJECT_NAME} PRIVATE Qt6::Widgets)

    # Link OBS frontend API
    find_package(obs-frontend-api QUIET)
    if(obs-frontend-api_FOUND)
        target_link_libraries(${PROJECT_NAME} PRIVATE OBS::obs-frontend-api)
    endif()
else()
    # Fallback: simple C frontend without dialog
    target_sources(${PROJECT_NAME} PRIVATE src/frontend-simple.c)
endif()
```

### Step 3: Create Settings Dialog Class

```cpp
// settings-dialog.h
#pragma once

#include <QDialog>
#include <QLineEdit>
#include <QSpinBox>
#include <QPushButton>
#include <QVBoxLayout>
#include <QFormLayout>

class SettingsDialog : public QDialog {
    Q_OBJECT

public:
    explicit SettingsDialog(QWidget *parent = nullptr);

    QString host() const { return m_hostEdit->text(); }
    int port() const { return m_portSpin->value(); }

    void setHost(const QString &host) { m_hostEdit->setText(host); }
    void setPort(int port) { m_portSpin->setValue(port); }

private:
    QLineEdit *m_hostEdit;
    QSpinBox *m_portSpin;
};
```

### Step 4: Implement Dialog

```cpp
// settings-dialog.cpp
#include "settings-dialog.h"

SettingsDialog::SettingsDialog(QWidget *parent)
    : QDialog(parent)
{
    setWindowTitle(tr("Plugin Settings"));
    setMinimumWidth(300);

    // Create widgets
    m_hostEdit = new QLineEdit(this);
    m_hostEdit->setPlaceholderText(tr("127.0.0.1"));

    m_portSpin = new QSpinBox(this);
    m_portSpin->setRange(1, 65535);
    m_portSpin->setValue(5000);

    auto *okButton = new QPushButton(tr("OK"), this);
    auto *cancelButton = new QPushButton(tr("Cancel"), this);

    // Layout
    auto *formLayout = new QFormLayout;
    formLayout->addRow(tr("Host:"), m_hostEdit);
    formLayout->addRow(tr("Port:"), m_portSpin);

    auto *buttonLayout = new QHBoxLayout;
    buttonLayout->addStretch();
    buttonLayout->addWidget(okButton);
    buttonLayout->addWidget(cancelButton);

    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->addLayout(formLayout);
    mainLayout->addLayout(buttonLayout);

    // Connections
    connect(okButton, &QPushButton::clicked, this, &QDialog::accept);
    connect(cancelButton, &QPushButton::clicked, this, &QDialog::reject);
}
```

### Step 5: Integrate with OBS Frontend API

```cpp
// frontend.cpp
#include <obs-module.h>
#include <obs-frontend-api.h>

#ifdef BUILD_WITH_QT
#include "settings-dialog.h"
#include <QMainWindow>
#endif

extern "C" {

static void on_frontend_event(enum obs_frontend_event event, void *data)
{
    (void)data;

    switch (event) {
    case OBS_FRONTEND_EVENT_FINISHED_LOADING:
        /* OBS UI is ready - safe to create Qt widgets */
        break;
    default:
        break;
    }
}

void frontend_init(void)
{
    obs_frontend_add_event_callback(on_frontend_event, NULL);
}

void frontend_cleanup(void)
{
    obs_frontend_remove_event_callback(on_frontend_event, NULL);
}

void frontend_show_settings(void)
{
#ifdef BUILD_WITH_QT
    QMainWindow *main_window = (QMainWindow *)obs_frontend_get_main_window();

    SettingsDialog dialog(main_window);
    if (dialog.exec() == QDialog::Accepted) {
        /* Save settings */
        const char *host = dialog.host().toUtf8().constData();
        int port = dialog.port();
        /* Apply settings... */
    }
#else
    blog(LOG_INFO, "Settings dialog not available (Qt not built)");
#endif
}

} /* extern "C" */
```

## OBS Frontend API

### Key Functions

| Function                               | Purpose                                |
| -------------------------------------- | -------------------------------------- |
| `obs_frontend_get_main_window()`       | Get OBS main window (as QMainWindow\*) |
| `obs_frontend_add_event_callback()`    | Subscribe to frontend events           |
| `obs_frontend_remove_event_callback()` | Unsubscribe from events                |
| `obs_frontend_add_tools_menu_item()`   | Add item to Tools menu                 |
| `obs_frontend_add_dock()`              | Add dockable panel                     |

### Frontend Events

```cpp
enum obs_frontend_event {
    OBS_FRONTEND_EVENT_STREAMING_STARTING,
    OBS_FRONTEND_EVENT_STREAMING_STARTED,
    OBS_FRONTEND_EVENT_STREAMING_STOPPING,
    OBS_FRONTEND_EVENT_STREAMING_STOPPED,
    OBS_FRONTEND_EVENT_RECORDING_STARTING,
    OBS_FRONTEND_EVENT_RECORDING_STARTED,
    OBS_FRONTEND_EVENT_RECORDING_STOPPING,
    OBS_FRONTEND_EVENT_RECORDING_STOPPED,
    OBS_FRONTEND_EVENT_SCENE_CHANGED,
    OBS_FRONTEND_EVENT_SCENE_LIST_CHANGED,
    OBS_FRONTEND_EVENT_TRANSITION_CHANGED,
    OBS_FRONTEND_EVENT_FINISHED_LOADING,
    OBS_FRONTEND_EVENT_EXIT,
    /* ... more events */
};
```

### Adding Tools Menu Item

```cpp
static void on_tools_menu_clicked(void *data)
{
    (void)data;
    frontend_show_settings();
}

void frontend_init(void)
{
    obs_frontend_add_tools_menu_item(
        obs_module_text("MyPlugin.Settings"),  /* Menu text */
        on_tools_menu_clicked,                  /* Callback */
        NULL                                    /* User data */
    );
}
```

## Qt Optional Build Pattern

### CMake Configuration

```cmake
# Try to find Qt6, but don't fail if missing
find_package(Qt6 COMPONENTS Widgets QUIET)

if(Qt6_FOUND)
    set(BUILD_WITH_QT ON)
    message(STATUS "Qt6 found - building with UI")
else()
    set(BUILD_WITH_QT OFF)
    message(STATUS "Qt6 not found - building without UI")
endif()

# Conditional compilation
if(BUILD_WITH_QT)
    target_sources(${PROJECT_NAME} PRIVATE
        src/frontend.cpp
        src/settings-dialog.cpp
    )
    target_compile_definitions(${PROJECT_NAME} PRIVATE BUILD_WITH_QT)
    target_link_libraries(${PROJECT_NAME} PRIVATE Qt6::Widgets)
else()
    target_sources(${PROJECT_NAME} PRIVATE
        src/frontend-simple.c
    )
endif()
```

### C Fallback (frontend-simple.c)

```c
/* frontend-simple.c - Minimal frontend without Qt
 *
 * Used when Qt is not available (e.g., cross-compilation).
 */

#include <obs-module.h>

void frontend_init(void)
{
    blog(LOG_INFO, "Plugin loaded without Qt UI");
}

void frontend_cleanup(void)
{
    /* Nothing to clean up */
}

void frontend_show_settings(void)
{
    blog(LOG_WARNING, "Settings dialog not available (Qt not built)");
}
```

### Header Pattern

```c
/* frontend.h - Frontend API (C-compatible) */
#pragma once

#ifdef __cplusplus
extern "C" {
#endif

void frontend_init(void);
void frontend_cleanup(void);
void frontend_show_settings(void);

#ifdef __cplusplus
}
#endif
```

## C and C++ Mixing Patterns

### extern "C" Wrapper

```cpp
// In C++ files that expose C API:
extern "C" {

#include <obs-module.h>

void my_cpp_function(void)
{
    // C++ code here
}

} /* extern "C" */
```

### C Header in C++

```cpp
// Always use extern "C" when including C headers from C++
extern "C" {
#include <obs-module.h>
#include <obs-frontend-api.h>
}

// Now safe to use C++ features
#include <QString>
```

### Plugin Main (C with C++ Features)

```c
/* plugin-main.c - C module entry point */

#include <obs-module.h>
#include "frontend.h"  /* C-compatible header */

OBS_DECLARE_MODULE()
OBS_MODULE_USE_DEFAULT_LOCALE("my-plugin", "en-US")

bool obs_module_load(void)
{
    obs_register_source(&my_source);

    /* Initialize frontend (may be C or C++) */
    frontend_init();

    return true;
}

void obs_module_unload(void)
{
    frontend_cleanup();
}
```

## CMAKE_AUTOMOC Explained

### What AUTOMOC Does

- Scans C++ files for `Q_OBJECT` macro
- Runs Qt's `moc` (Meta-Object Compiler) automatically
- Generates `moc_*.cpp` files for signal/slot support

### Required Settings

```cmake
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)  # For .ui files

# AUTOMOC requires C++ targets
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
```

### Common Issues

| Issue                           | Cause              | Solution                |
| ------------------------------- | ------------------ | ----------------------- |
| "undefined reference to vtable" | Missing Q_OBJECT   | Add Q_OBJECT to class   |
| "moc not found"                 | Qt not in PATH     | Use find_package(Qt6)   |
| "undefined signal/slot"         | AUTOMOC didn't run | Ensure .h is in SOURCES |

## Threading with Qt

### Safe Thread Communication

```cpp
// worker-thread.cpp
#include <QThread>
#include <QObject>

class WorkerThread : public QThread {
    Q_OBJECT

signals:
    void resultReady(const QString &result);

protected:
    void run() override {
        QString result = doWork();
        emit resultReady(result);  /* Signal is thread-safe */
    }

private:
    QString doWork() {
        /* Heavy work here */
        return "Done";
    }
};

// Usage from main thread:
WorkerThread *thread = new WorkerThread;
connect(thread, &WorkerThread::resultReady, this, &MyClass::handleResult);
connect(thread, &WorkerThread::finished, thread, &QObject::deleteLater);
thread->start();
```

### Qt Event Loop Integration

```cpp
// Don't block OBS main thread - use async patterns
void MyDialog::onButtonClicked()
{
    // WRONG: Blocks OBS UI
    // QThread::sleep(5);

    // CORRECT: Use QTimer or worker thread
    QTimer::singleShot(0, this, [this]() {
        // Runs after current event processing
        doSomething();
    });
}
```

## FORBIDDEN Patterns

| Pattern                                 | Problem              | Solution                     |
| --------------------------------------- | -------------------- | ---------------------------- |
| Blocking in UI callbacks                | Freezes OBS          | Use worker threads           |
| Missing Q_OBJECT                        | Signals/slots fail   | Add Q_OBJECT macro           |
| Qt widgets in audio thread              | Crash                | Only UI in main thread       |
| Mixing Qt versions                      | ABI issues           | Stick to Qt6 only            |
| Missing AUTOMOC                         | Link errors          | Enable CMAKE_AUTOMOC         |
| Direct obs_frontend calls without check | Crash if no frontend | Check obs-frontend-api_FOUND |

## Platform-Specific UI Fallbacks

### Windows Native Dialog

```c
/* settings-dialog-win32.c - Fallback when Qt unavailable */
#ifdef _WIN32
#include <windows.h>
#include <commctrl.h>

void show_settings_dialog_win32(void *parent)
{
    MessageBoxW((HWND)parent,
                L"Settings dialog requires Qt.\nPlease install Qt6.",
                L"Plugin Settings",
                MB_OK | MB_ICONINFORMATION);
}
#endif
```

### CMake Platform Selection

```cmake
if(NOT BUILD_WITH_QT)
    if(WIN32)
        target_sources(${PROJECT_NAME} PRIVATE
            src/settings-dialog-win32.c
        )
    else()
        target_sources(${PROJECT_NAME} PRIVATE
            src/frontend-simple.c
        )
    endif()
endif()
```

## External Documentation

### Context7

```
mcp__context7__query-docs
libraryId: "/obsproject/obs-studio"
query: "Qt frontend API settings dialog"
```

### Official References

- **OBS Frontend API**: https://docs.obsproject.com/reference-frontend-api
- **Qt6 Widgets**: https://doc.qt.io/qt-6/qtwidgets-index.html
- **CMake AUTOMOC**: https://cmake.org/cmake/help/latest/prop_tgt/AUTOMOC.html

## Related Skills

- **obs-windows-building** - Windows-specific builds
- **obs-cross-compiling** - Cross-compilation (may not have Qt)
- **obs-plugin-developing** - Plugin architecture overview
- **obs-audio-plugin-writing** - Audio plugin implementation

## Related Agent

Use **obs-plugin-expert** for coordinated guidance across all OBS plugin skills.
