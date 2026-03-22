---
name: frappe-core-utils
description: >
  Use when working with utility functions in Frappe v14-v16. Covers
  frappe.utils.* for date/time, number/money, string, validation, and
  file path operations. Prevents reinventing stdlib alternatives that
  break timezone awareness, locale formatting, or multi-tenancy.
  Keywords: frappe.utils, nowdate, flt, cint, fmt_money, getdate,
  add_days, date_diff, validate_email, pretty_date, get_files_path.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "3.0"
---

# Frappe Utility Functions

## Quick Reference — Python

| Need | Function | Returns |
|------|----------|---------|
| Current date | `nowdate()` / `today()` | `datetime.date` |
| Current datetime | `now_datetime()` | `datetime.datetime` |
| Parse date string | `getdate(str)` | `datetime.date` |
| Parse datetime string | `get_datetime(str)` | `datetime.datetime` |
| Add days | `add_days(date, n)` | `datetime.date` |
| Add months | `add_months(date, n)` | `datetime.date` |
| Date difference | `date_diff(end, start)` | `int` (days) |
| Format for user | `format_date(dt)` | `str` (user locale) |
| Relative time | `pretty_date(dt)` | `str` ("2 hours ago") |
| Safe float | `flt(val, precision)` | `float` |
| Safe int | `cint(val)` | `int` |
| Safe string | `cstr(val)` | `str` |
| Safe bool | `sbool(val)` | `bool` |
| Safe division | `safe_div(a, b)` | `float` [v15+] |
| Money format | `fmt_money(amt, currency)` | `str` |
| Money in words | `money_in_words(amt, cur)` | `str` |
| Strip HTML | `strip_html(text)` | `str` |
| List to prose | `comma_and(items)` | `str` ("a, b, and c") |
| Validate email | `validate_email_address(e)` | `str` or `""` |
| Validate URL | `validate_url(url)` | `bool` |
| Parse JSON | `parse_json(s)` | `Any` |
| Files path | `get_files_path(is_private)` | `str` |
| Site path | `get_site_path(*parts)` | `str` |
| Unique list | `unique(seq)` | `list` |
| Hash | `generate_hash(s, length)` | `str` |

> **ALL imports**: `from frappe.utils import nowdate, flt, ...` in controllers/whitelisted methods.
> In **Server Scripts**: Use `frappe.utils.nowdate()` directly — NO import statements allowed.

---

## Decision Tree — "Which function do I use?"

```
Need a date/time value?
├─ Current date → nowdate() or today()
├─ Current datetime → now_datetime()
├─ Parse a string → getdate() or get_datetime()
├─ Add/subtract time → add_days(), add_months(), add_to_date()
├─ Difference → date_diff() (days), month_diff(), time_diff_in_seconds()
├─ Period boundary → get_first_day(), get_last_day(), get_quarter_start()
└─ Display to user → format_date(), format_datetime(), pretty_date()

Need a number?
├─ Convert safely → flt(), cint(), cstr(), sbool()
├─ Round → rounded() (banker's rounding)
├─ Safe divide → safe_div(a, b, default=0) [v15+]
├─ Format money → fmt_money(amount, currency)
└─ Money to words → money_in_words(amount, currency)

Need string processing?
├─ HTML → strip_html(), escape_html(), is_html()
├─ Join list → comma_and(), comma_or(), comma_sep()
├─ Markdown ↔ HTML → to_markdown(), md_to_html()
└─ Mask sensitive → mask_string(input, show_first=4) [v16+]

Need validation?
├─ Email → validate_email_address(email, throw=False)
├─ URL → validate_url(url, valid_schemes=["https"])
├─ Phone → validate_phone_number(phone, throw=False)
├─ JSON → validate_json_string(s)
└─ IBAN → validate_iban(iban) [v16+]

Need file/path?
├─ Public files → get_files_path()
├─ Private files → get_files_path(is_private=True)
├─ Site directory → get_site_path("private", "backups")
├─ Bench root → get_bench_path()
└─ File size → get_file_size(path, format=True)
```

---

## Critical Anti-Patterns

### NEVER use Python stdlib when frappe.utils exists

| NEVER (stdlib) | ALWAYS (frappe.utils) | Why |
|----------------|----------------------|-----|
| `datetime.datetime.now()` | `now_datetime()` | Ignores system timezone |
| `datetime.date.today()` | `nowdate()` | Ignores system timezone |
| `float(val)` | `flt(val, precision)` | Crashes on None/empty |
| `int(val)` | `cint(val)` | Crashes on None/empty |
| `round(val, 2)` | `rounded(val, 2)` | Inconsistent rounding |
| `val1 / val2` | `safe_div(val1, val2)` | ZeroDivisionError [v15+] |
| `json.loads(s)` | `parse_json(s)` | Crashes on None/empty |
| `json.dumps(obj)` | `frappe.as_json(obj)` | Inconsistent serialization |
| `"{:,.2f}".format(a)` | `fmt_money(a, currency)` | Ignores locale/currency |
| `os.path.join(...)` | `get_site_path(...)` | Breaks multi-tenancy |
| `", ".join(items)` | `comma_and(items)` | No localized "and" |
| `dt.strftime(fmt)` | `format_date(dt)` | Ignores user preference |
| `re.sub(r'<.*?>', '', h)` | `strip_html(h)` | Misses edge cases |

### Server Script Sandbox

```python
# ❌ NEVER in Server Scripts
from frappe.utils import nowdate, flt
import json

# ✅ ALWAYS in Server Scripts (no imports allowed)
today = frappe.utils.nowdate()
amount = frappe.utils.flt(doc.amount, 2)
data = frappe.parse_json(doc.json_field)
```

---

## JavaScript Quick Reference

| Need | Function |
|------|----------|
| Escape HTML | `frappe.utils.escape_html(txt)` |
| HTML to text | `frappe.utils.html2text(html)` |
| Check if HTML | `frappe.utils.is_html(txt)` |
| Parse JSON | `frappe.utils.parse_json(str)` |
| Validate URL | `frappe.utils.is_url(txt)` |
| Title case | `frappe.utils.to_title_case(str)` |
| Join with "and" | `frappe.utils.comma_and(list)` |
| Unique array | `frappe.utils.unique(list)` |
| Copy clipboard | `frappe.utils.copy_to_clipboard(txt)` |
| Scroll to element | `frappe.utils.scroll_to(el)` |
| Is mobile | `frappe.utils.is_mobile()` |
| Throttle | `frappe.utils.throttle(fn, delay)` |
| Debounce | `frappe.utils.debounce(fn, delay)` |
| Format value | `frappe.format(value, df, options, doc)` |
| Duration display | `frappe.utils.get_formatted_duration(secs)` |

---

## Version Differences

| Function | v14 | v15 | v16 |
|----------|:---:|:---:|:---:|
| `safe_div()` | -- | Added | Yes |
| `duration_to_seconds()` | -- | Added | Yes |
| `guess_date_format()` | -- | Added | Yes |
| `validate_duration_format()` | -- | Added | Yes |
| `mask_string()` | -- | -- | Added |
| `validate_iban()` | -- | -- | Added |
| `validate_name()` | -- | -- | Added |
| `safe_json_loads()` | -- | -- | Added |
| `groupby_metric()` | -- | -- | Added |
| Core functions | Yes | Yes | Yes |

---

## Reference Files

- [Date/Time Functions](references/date-time-functions.md) — Complete date/time API with signatures
- [Number & Money Functions](references/number-money-functions.md) — flt, fmt_money, rounding
- [String & Validation Functions](references/string-validation-functions.md) — HTML, join, validate
- [JavaScript Utilities](references/javascript-utilities.md) — Client-side frappe.utils.*
- [Anti-patterns](references/anti-patterns.md) — stdlib vs frappe.utils comparison
