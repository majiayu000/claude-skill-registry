---
name: printing-guide
description: Reference for Epson thermal printer integration. Use when working with receipt printing, printer connection, or the ePOS SDK.
user-invocable: false
---

# Epson Printer Integration Guide

This POS system integrates with Epson thermal receipt printers via the ePOS SDK.

## Architecture

### Files
- `resources/js/epos-2.20.0.js` - Epson ePOS SDK library (253KB)
- `resources/js/store/modules/printing.js` - Vuex module for print management
- `resources/js/store/modules/epos.js` - Device connection management
- `resources/js/printing.js` - Legacy printing utilities

### Connection Details
- **IP Address**: `192.168.200.80`
- **Port**: `8008`
- **Protocol**: ePOS Device Service

## Vuex Store Structure

### State
```javascript
state: {
    ePosDev: null,           // ePOS device instance
    printer: null,           // Printer object
    printingNotification: false,
    printingAttempts: 0,
    printing: {
        order: null,         // Current order being printed
        invoice: null,       // Current invoice being printed
    },
    printingHistory: []
}
```

### Key Actions

```javascript
// Connect to printer
this.$store.dispatch('setEpsonDevice')

// Print an order (kitchen ticket)
this.$store.dispatch('setPrintingOrder', order)

// Print an invoice (receipt)
this.$store.dispatch('setPrintingInvoice', invoice)
```

## Connection Flow

```javascript
// In printing.js store module

setEpsonDevice({ commit, state }) {
    const ePosDev = new epson.ePOSDevice();

    ePosDev.connect('192.168.200.80', 8008, (result) => {
        if (result === 'OK' || result === 'SSL_CONNECT_OK') {
            ePosDev.createDevice('local_printer',
                ePosDev.DEVICE_TYPE_PRINTER,
                { crypto: false, buffer: false },
                (printer, code) => {
                    if (code === 'OK') {
                        printer.timeout = 60000;
                        commit('setEpsonDevice', { ePosDev, printer });
                    }
                }
            );
        }
    });
}
```

## Receipt Formatting

### Order Ticket (Kitchen)
```javascript
// Header
printer.addTextAlign(printer.ALIGN_CENTER);
printer.addTextSize(1, 2);
printer.addTextStyle(false, false, true, printer.COLOR_1);
printer.addText('TABLE NAME\n\n');

// Time
printer.addTextSize(1, 1);
printer.addText(` Vreme: ${time}\n`);

// Items
printer.addTextSize(1, 2);
printer.addText(' —————————————————\n');
items.forEach(item => {
    printer.addText(` ${item.qty} x ${item.name}\n`);
});

// Cut
printer.addFeedLine(1);
printer.addCut(printer.CUT_FEED);
```

### Invoice Receipt
```javascript
// Header
printer.addText('PREDRAČUN\n');  // "Bill" in Serbian

// Items with prices
items.forEach(item => {
    printer.addText(formatLine(item.name, item.total));
});

// Totals
printer.addText('—————————————————\n');
printer.addText(formatLine('UKUPNO:', total));
printer.addText(formatLine('PDV (20%):', tax));

// Receipt number
printer.addText(`\nBroj: ${receiptNumber}\n`);

// Cut
printer.addCut(printer.CUT_FEED);
```

## Helper Functions

```javascript
// Right-align text with spacing
function printerTextBetween(left, right, width = 48) {
    const spaces = width - left.length - right.length;
    return left + ' '.repeat(spaces) + right;
}

// Format price
function formatPrice(price) {
    return new Intl.NumberFormat('de-DE').format(price);
}
```

## Error Handling

```javascript
// Sentry integration for error tracking
import * as Sentry from '@sentry/vue';

printer.onreceive = (response) => {
    if (!response.success) {
        Sentry.captureException(new Error('Print failed'));
        commit('setPrintingNotification', true);
    }
};

// Retry logic
if (state.printingAttempts < 3) {
    commit('incrementPrintingAttempts');
    dispatch('setEpsonDevice');
}
```

## Printer Commands Reference

```javascript
// Text formatting
printer.addTextAlign(printer.ALIGN_LEFT | ALIGN_CENTER | ALIGN_RIGHT);
printer.addTextSize(width, height);  // 1-8 each
printer.addTextStyle(reverse, underline, bold, color);

// Line spacing
printer.addTextLineSpace(pixels);  // Default ~30
printer.addFeedLine(lines);

// Paper cutting
printer.addCut(printer.CUT_FEED);     // Feed then cut
printer.addCut(printer.CUT_NO_FEED);  // Cut without feed

// Send to printer
printer.send();
```

## Troubleshooting

1. **Printer not connecting**: Check IP/port, ensure printer is on network
2. **Print jobs stuck**: Call `disconnect()` and reconnect
3. **Garbled text**: Ensure UTF-8 encoding for Serbian characters
4. **Slow printing**: Check `buffer: false` setting

## Real-time Notifications

The printing module shows a notification when:
- Print job is in progress
- Print job fails (with retry option)
- Timeout after 30 seconds
