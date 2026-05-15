# LogsQL Reference

## Query Structure

```
[filters] [| pipe1] [| pipe2] [| ...]
```

## Special Fields

| Field | Description |
|-------|-------------|
| `_msg` | Log message (default search target) |
| `_time` | Timestamp |
| `_stream` | Stream identifier `{app="nginx",host="h1"}` |

## Filter Types

### Text Filters
```
error                          # word in _msg
"connection refused"           # phrase
err*                           # prefix
~"partial"                     # substring
i(error)                       # case-insensitive
re("err|warn")                 # regexp (RE2)
seq("error", "open file")     # ordered sequence
```

### Field Filters
```
field_name:value               # word match
field_name:"exact phrase"      # phrase match
field_name:="exact_value"      # exact match
field_name:~"substring"        # substring
field_name:re("^[0-9]+$")     # regexp
field_name:in("v1","v2")      # multi-value IN
field_name:*                   # non-empty
field_name:""                  # empty
field_name:>100                # numeric comparison (>, >=, <, <=)
field_name:range[100, 200]     # numeric range
```

### Time Filters
```
_time:5m                       # last 5 minutes
_time:1h                       # last 1 hour
_time:1d                       # last 1 day
_time:2023-04-25               # specific day
_time:[2023-02-01, 2023-03-01) # range
_time:5m offset 1h             # with offset
_time:day_range[08:00, 18:00)  # business hours
_time:week_range[Mon, Fri]     # weekdays
```

### Stream Filters
```
{app="nginx"}                  # exact match
{app=~"api.*"}                 # regexp match
{app!="test"}                  # not equal
{app!~"test.*"}                # negative regexp
```

### Logical Operators
```
q1 AND q2       # explicit AND
q1 q2           # implicit AND (space)
q1 OR q2        # OR
NOT q / !q / -q # NOT
(q1 OR q2) AND q3  # grouping
```
Precedence: NOT > AND > OR

## Pipes

### Field Manipulation
```
| fields f1, f2                # keep only these fields
| delete f1, f2                # remove fields
| copy f1 as f2                # copy
| rename old as new            # rename
| drop_empty_fields            # remove empty fields
```

### Extraction / Parsing
```
| extract '"duration": <duration>,'
| extract_regexp "(?P<ip>([0-9]+\\.){3}[0-9]+)"
| unpack_json
| unpack_json fields (trace_id, user_id)
| unpack_logfmt
| unpack_syslog
```

### Transformation
```
| format "<f1> [<f2>] <_msg>" as result
| replace "password" "***"
| replace_regexp "pattern" "replacement"
| pack_json
| decolorize
| collapse_nums
| math (duration_secs * 1000) as duration_msecs
```

### Filtering / Selection
```
| filter duration > 100        # post-filter (alias: where)
| limit 10                     # limit results (alias: head)
| offset 5                     # skip N results
| first 10 by (field desc)
| last 10 by (field desc)
| sample 100                   # random sample
```

### Aggregation
```
| stats count() as cnt
| stats by (field) count() as cnt
| stats by (_time:1m) count() as rate
| stats by (_time:1m, path) avg(duration) as avg_dur
| stats count() if (status:=200) as ok, count() if (status:>=500) as err
| top 10 by (path, duration)
| uniq by (field)
| facets
```

### Stats Functions
```
count()               sum(f)              avg(f)
min(f)                max(f)              median(f)
quantile(0.95, f)     stddev(f)           rate()
count_uniq(f)         values(f)           uniq_values(f)
any(f)                histogram(f)        sum_len(f)
row_min(f)            row_max(f)
```

### Sorting
```
| sort by (_time)
| sort by (field desc)
| sort by (f1, f2 desc)
```

### Context / Join
```
| stream_context before 3 after 3    # surrounding logs
| join by (trace_id) (other_query)
```

## Math Operations
```
| math (duration_secs * 1000) as ms
| math failed * 100 / total as error_rate
```
Operators: `+`, `-`, `*`, `/`, `%`, `^`
Functions: `abs()`, `ceil()`, `floor()`, `round()`, `exp()`, `ln()`, `max()`, `min()`
