---
name: jsont
description: "JSON type-safe encoding and decoding using the OCaml jsont library. Use when Claude needs to: define typed JSON codecs for OCaml record types, parse JSON strings to OCaml values, or serialize OCaml values to JSON, or work with nested JSON structures"
license: ISC
---

# Jsont JSON Encoding/Decoding

## Dependencies

```dune
(libraries jsont jsont.bytesrw)
```

## Core Patterns

### Simple Object Codec

Map a JSON object to an OCaml record using `Jsont.Object.map` with `mem` for required fields:

```ocaml
type header = {
  message_id : string;
  method_ : string;
  timestamp : int;
}

let header_codec =
  Jsont.Object.map ~kind:"header"
    (fun message_id method_ timestamp -> { message_id; method_; timestamp })
  |> Jsont.Object.mem "messageId" Jsont.string ~enc:(fun h -> h.message_id)
  |> Jsont.Object.mem "method" Jsont.string ~enc:(fun h -> h.method_)
  |> Jsont.Object.mem "timestamp" Jsont.int ~enc:(fun h -> h.timestamp)
  |> Jsont.Object.finish
```

### Optional Fields

Use `opt_mem` for optional JSON fields. The constructor receives `'a option`:

```ocaml
type config = {
  name : string;
  timeout : int;  (* default if missing *)
}

let config_codec =
  Jsont.Object.map ~kind:"config"
    (fun name timeout_opt ->
      { name; timeout = Option.value ~default:30 timeout_opt })
  |> Jsont.Object.mem "name" Jsont.string ~enc:(fun c -> c.name)
  |> Jsont.Object.opt_mem "timeout" Jsont.int ~enc:(fun c -> Some c.timeout)
  |> Jsont.Object.finish
```

### Skip Unknown Fields

Use `skip_unknown` before `finish` to ignore extra JSON fields (tolerant parsing):

```ocaml
let tolerant_codec =
  Jsont.Object.map ~kind:"data" (fun id -> { id })
  |> Jsont.Object.mem "id" Jsont.string ~enc:(fun d -> d.id)
  |> Jsont.Object.skip_unknown  (* ignore extra fields *)
  |> Jsont.Object.finish
```

### Nested Objects

Compose codecs for nested structures:

```ocaml
type request = { header : header; payload : payload }

let request_codec payload_codec =
  Jsont.Object.map ~kind:"request" (fun header payload -> { header; payload })
  |> Jsont.Object.mem "header" header_codec ~enc:(fun r -> r.header)
  |> Jsont.Object.mem "payload" payload_codec ~enc:(fun r -> r.payload)
  |> Jsont.Object.finish
```

### Lists

Use `Jsont.list` for JSON arrays:

```ocaml
type response = { items : item list }

let response_codec =
  Jsont.Object.map ~kind:"response" (fun items -> { items })
  |> Jsont.Object.mem "items" (Jsont.list item_codec) ~enc:(fun r -> r.items)
  |> Jsont.Object.finish
```

### String Maps

Use `Jsont.Object.as_string_map` for objects with dynamic keys:

```ocaml
module String_map = Map.Make(String)

(* JSON: {"key1": "value1", "key2": "value2"} *)
let string_map_codec = Jsont.Object.as_string_map Jsont.string

(* JSON: {"group1": [...], "group2": [...]} *)
let groups_codec = Jsont.Object.as_string_map (Jsont.list item_codec)
```

### Empty Object

For payloads that don't carry data:

```ocaml
let empty_payload_codec : unit Jsont.t =
  Jsont.Object.map ~kind:"empty" ()
  |> Jsont.Object.skip_unknown
  |> Jsont.Object.finish
```

### Custom Value Mapping

Use `Jsont.map` to transform between types:

```ocaml
type device_type = Sonos | Meross | Other

let device_from_string =
  Jsont.map ~kind:"device_type"
    ~dec:(function "sonos" -> Sonos | "meross" -> Meross | _ -> Other)
    ~enc:(function Sonos -> "sonos" | Meross -> "meross" | Other -> "other")
    Jsont.string
```

### Polymorphic Decoding with `any`

Handle multiple JSON shapes for backwards compatibility:

```ocaml
(* Device can be string (old format) or object (new format) *)
let device_compat_codec =
  Jsont.any ~kind:"device"
    ~dec_string:device_from_string_codec  (* handles "192.168.1.1" *)
    ~dec_object:device_object_codec       (* handles {"ip": "...", "type": "..."} *)
    ~enc:(fun _ -> device_object_codec)   (* always encode as object *)
    ()
```

### Null Values

Use `Jsont.null` for endpoints returning null:

```ocaml
(* For DELETE endpoints that return null on success *)
match delete http ~sw token endpoint (Jsont.null ()) with
| Ok () -> ...
```

### Generic JSON

Use `Jsont.json` to preserve arbitrary JSON:

```ocaml
type characteristic = {
  iid : int;
  value : Jsont.json option;  (* preserve any JSON value *)
}

let char_codec =
  Jsont.Object.map ~kind:"char" (fun iid value -> { iid; value })
  |> Jsont.Object.mem "iid" Jsont.int ~enc:(fun c -> c.iid)
  |> Jsont.Object.opt_mem "value" Jsont.json ~enc:(fun c -> c.value)
  |> Jsont.Object.finish
```

## Encoding and Decoding

Use `Jsont_bytesrw` for string-based encoding/decoding:

```ocaml
(* Decode JSON string to OCaml value *)
let decode codec s = Jsont_bytesrw.decode_string codec s
(* Returns: ('a, Jsont.Error.t) result *)

(* Encode OCaml value to JSON string *)
let encode codec v =
  match Jsont_bytesrw.encode_string codec v with
  | Ok s -> s
  | Error _ -> "{}"  (* fallback for encoding errors *)

(* Usage *)
match Jsont_bytesrw.decode_string config_codec json_string with
| Ok config -> (* use config *)
| Error e -> (* handle error *)

match Jsont_bytesrw.encode_string config_codec config with
| Ok json_str -> (* send json_str *)
| Error _ -> (* handle error *)
```

## Common Helpers

Define module-level helpers for cleaner code:

```ocaml
let decode codec s = Jsont_bytesrw.decode_string codec s

let encode codec v =
  match Jsont_bytesrw.encode_string codec v with
  | Ok s -> s
  | Error _ -> ""
```

## Base Types Reference

| OCaml Type | Jsont Codec | JSON Type |
|------------|-------------|-----------|
| `string` | `Jsont.string` | string |
| `int` | `Jsont.int` | number |
| `float` | `Jsont.number` | number |
| `bool` | `Jsont.bool` | boolean |
| `'a list` | `Jsont.list codec` | array |
| `'a option` | `Jsont.option codec` | value or null |
| `unit` | `Jsont.null ()` | null |
| generic | `Jsont.json` | any JSON |

## Best Practices

1. **Always use `~kind`**: Provide descriptive kind names for better error messages
2. **Use `skip_unknown` for external APIs**: Be tolerant of extra fields from third-party services
3. **Prefer `opt_mem` with defaults**: Handle missing fields gracefully with `Option.value ~default:`
4. **Compose small codecs**: Build complex structures from simple, reusable codecs
5. **Define helper functions**: Create `decode`/`encode` helpers at module level for cleaner usage
