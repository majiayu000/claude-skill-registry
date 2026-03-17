---
description: Print system management including CUPS, Canon Selphy CP1500, print queue, job status, and printer troubleshooting.
auto-activation-keywords:
  - print
  - printer
  - cups
  - selphy
  - canon
  - queue
  - job
  - paper
  - ink
  - ribbon
---

# Print System Skill

Complete reference for Canon Selphy CP1500 printer integration via CUPS on Raspberry Pi 5.

## Quick Reference

| Setting | Value |
|---------|-------|
| Printer Model | Canon Selphy CP1500 |
| Connection | USB |
| Paper Size | 4x6 inch (Postcard) |
| Resolution | 300 DPI |
| Print Quality | Maximum |
| Driver | Gutenprint or CUPS-builtin |

## CUPS Configuration

### Installation
```bash
# Install CUPS
sudo apt-get install cups cups-bsd printer-driver-gutenprint

# Add user to lpadmin group
sudo usermod -a -G lpadmin pi

# Enable web interface (optional)
sudo cupsctl --remote-admin
```

### Printer Setup
```bash
# List available printers
lpstat -p -d

# Add Canon Selphy (after USB connection)
sudo lpadmin -p Canon_Selphy_CP1500 \
  -E \
  -v usb://Canon/SELPHY%20CP1500 \
  -m everywhere

# Set as default
sudo lpadmin -d Canon_Selphy_CP1500

# Set default options
sudo lpadmin -p Canon_Selphy_CP1500 \
  -o media=na_index-4x6_4x6in \
  -o print-quality=5 \
  -o ColorModel=RGB
```

### CUPS Web Interface
- URL: `http://localhost:631`
- Admin: `https://localhost:631/admin`
- Jobs: `https://localhost:631/jobs`

## Print Commands

### Submit Print Job
```bash
# Print file
lp -d Canon_Selphy_CP1500 /path/to/image.jpg

# Print with options
lp -d Canon_Selphy_CP1500 \
  -o media=na_index-4x6_4x6in \
  -o fit-to-page \
  -o print-quality=5 \
  /path/to/composite.jpg

# Print multiple copies
lp -d Canon_Selphy_CP1500 -n 2 /path/to/image.jpg
```

### Job Management
```bash
# List all jobs
lpstat -o

# List jobs for specific printer
lpstat -o Canon_Selphy_CP1500

# Cancel specific job
cancel 123

# Cancel all jobs
cancel -a

# Cancel all jobs for printer
cancel -a Canon_Selphy_CP1500
```

### Printer Status
```bash
# Check printer status
lpstat -p Canon_Selphy_CP1500

# Detailed status
lpstat -t

# Check if printer is accepting jobs
lpstat -a Canon_Selphy_CP1500

# Check printer reasons (errors)
lpstat -p Canon_Selphy_CP1500 -l
```

## Print Job States

| State | Description |
|-------|-------------|
| `pending` | Job queued, waiting |
| `pending-held` | Job held, needs release |
| `processing` | Currently printing |
| `stopped` | Paused |
| `canceled` | User cancelled |
| `aborted` | System aborted (error) |
| `completed` | Successfully printed |

## Error Handling

### Printer State Reasons

| Reason | Meaning | Retryable |
|--------|---------|-----------|
| `none` | No issues | N/A |
| `media-needed` | Out of paper | Yes |
| `toner-low` | Ink/ribbon low | Yes |
| `toner-empty` | Ink/ribbon empty | Yes |
| `cover-open` | Door open | Yes |
| `offline` | Not responding | Yes |
| `paper-jam` | Paper jammed | No (manual) |
| `other` | Unknown issue | Maybe |

### Check Printer Errors
```bash
# Get printer state reasons
lpstat -p Canon_Selphy_CP1500 -l | grep -i reason

# Via CUPS API
curl -s http://localhost:631/printers/Canon_Selphy_CP1500 | grep -i state
```

## Python CUPS Integration

### Using pycups
```python
import cups

# Connect to CUPS
conn = cups.Connection()

# Get printers
printers = conn.getPrinters()
for name, attrs in printers.items():
    print(f"{name}: {attrs['printer-state-message']}")

# Get default printer
default = conn.getDefault()

# Print file
job_id = conn.printFile(
    printer='Canon_Selphy_CP1500',
    filename='/path/to/composite.jpg',
    title='PhotoBooth Print',
    options={
        'media': 'na_index-4x6_4x6in',
        'print-quality': '5',
        'fit-to-page': 'true',
    }
)
print(f"Job ID: {job_id}")

# Check job status
job_attrs = conn.getJobAttributes(job_id)
print(f"State: {job_attrs['job-state']}")
```

### Using subprocess (fallback)
```python
import subprocess

def print_image(image_path: str, copies: int = 1) -> int:
    """Print image via lp command."""
    result = subprocess.run([
        'lp',
        '-d', 'Canon_Selphy_CP1500',
        '-n', str(copies),
        '-o', 'media=na_index-4x6_4x6in',
        '-o', 'print-quality=5',
        '-o', 'fit-to-page',
        image_path
    ], capture_output=True, text=True)

    if result.returncode == 0:
        # Extract job ID from output
        # Output format: "request id is Canon_Selphy_CP1500-123 (1 file(s))"
        job_id = int(result.stdout.split('-')[-1].split()[0])
        return job_id
    else:
        raise PrintError(result.stderr)

def cancel_job(job_id: int) -> bool:
    """Cancel print job."""
    result = subprocess.run(['cancel', str(job_id)], capture_output=True)
    return result.returncode == 0

def get_printer_status() -> dict:
    """Get printer status."""
    result = subprocess.run(
        ['lpstat', '-p', 'Canon_Selphy_CP1500', '-l'],
        capture_output=True, text=True
    )

    status = {'online': False, 'state': 'unknown', 'message': ''}

    if 'idle' in result.stdout.lower():
        status['online'] = True
        status['state'] = 'idle'
    elif 'printing' in result.stdout.lower():
        status['online'] = True
        status['state'] = 'printing'
    elif 'disabled' in result.stdout.lower():
        status['state'] = 'disabled'

    return status
```

## Troubleshooting

### Printer Not Found
```bash
# Check USB connection
lsusb | grep Canon

# Restart CUPS
sudo systemctl restart cups

# Check CUPS error log
tail -50 /var/log/cups/error_log
```

### Jobs Stuck in Queue
```bash
# Check job status
lpstat -o

# Cancel all stuck jobs
cancel -a

# Restart CUPS
sudo systemctl restart cups

# Re-enable printer if disabled
cupsenable Canon_Selphy_CP1500
cupsaccept Canon_Selphy_CP1500
```

### Print Quality Issues
```bash
# Set maximum quality
lpadmin -p Canon_Selphy_CP1500 -o print-quality=5

# Verify paper type matches
lpstat -p Canon_Selphy_CP1500 -l
```

### CUPS Service Issues
```bash
# Check CUPS status
sudo systemctl status cups

# View CUPS logs
tail -100 /var/log/cups/error_log

# Restart CUPS
sudo systemctl restart cups

# Enable CUPS on boot
sudo systemctl enable cups
```

## Print Queue Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PhotoBooth Backend                        │
│                                                             │
│  ┌───────────────┐    ┌───────────────┐    ┌─────────────┐ │
│  │   PrintJob    │───>│ PrintService  │───>│   CUPS      │ │
│  │   Entity      │    │   (pycups)    │    │   Daemon    │ │
│  └───────────────┘    └───────────────┘    └─────────────┘ │
│         │                                         │         │
│         │                                         ▼         │
│         ▼                                  ┌─────────────┐  │
│  ┌───────────────┐                        │   Canon     │  │
│  │   SQLite      │                        │   Selphy    │  │
│  │   (persist)   │                        │   CP1500    │  │
│  └───────────────┘                        └─────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Related Documentation

- `docs/use-cases/UC-005-submit-print-job.md`
- `docs/use-cases/UC-006-monitor-print-status.md`
- `docs/use-cases/UC-201-process-print-queue.md`
- `docs/use-cases/UC-203-auto-retry-print.md`
- `docs/ERROR_CODES.md` - PRINTER_* and CUPS_* errors
