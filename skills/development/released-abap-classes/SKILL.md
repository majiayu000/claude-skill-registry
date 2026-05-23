---
name: released-abap-classes
description: Find released ABAP classes for ABAP Cloud Development. Use when user asks about ABAP classes for specific functionality like email, UUID generation, time/date handling, JSON/XML processing, RAP, string processing, random numbers, regex, Base64, HTTP calls, unit testing, PDF rendering, parallel processing, application logs, or any other ABAP Cloud class lookup.
---

# Released ABAP Classes

Reference for released ABAP classes available in ABAP for Cloud Development (SAP BTP ABAP Environment).

## Quick Reference by Category

| Category | Key Classes |
|----------|-------------|
| **Console Output** | `IF_OO_ADT_CLASSRUN`, `CL_DEMO_CLASSRUN`, `CL_XCO_CP_ADT_SIMPLE_CLASSRUN` |
| **UUID** | `CL_SYSTEM_UUID`, `XCO_CP`, `XCO_CP_UUID` |
| **Time & Date** | `CL_ABAP_CONTEXT_INFO`, `XCO_CP_TIME`, `CL_ABAP_TSTMP`, `CL_ABAP_UTCLONG`, `CL_ABAP_DATFM`, `CL_ABAP_TIMEFM` |
| **Calendar** | `CL_FHC_CALENDAR_RUNTIME`, `CL_SCAL_UTILS` |
| **String Processing** | `CL_ABAP_CHAR_UTILITIES`, `CL_ABAP_STRING_UTILITIES`, `XCO_CP` |
| **Numbers/Math** | `CL_ABAP_MATH`, `CL_ABAP_DECFLOAT`, `CL_ABAP_BIGINT`, `CL_ABAP_RATIONAL` |
| **Random Numbers** | `CL_ABAP_RANDOM_*` (INT, INT8, FLOAT, PACKED, DECFLOAT16/34), `CL_ABAP_PROB_DISTRIBUTION` |
| **Regular Expressions** | `CL_ABAP_REGEX`, `CL_ABAP_MATCHER` |
| **Codepage/Binary** | `CL_ABAP_CONV_CODEPAGE`, `CL_ABAP_GZIP*`, `CL_WEB_HTTP_UTILITY` |
| **JSON/XML** | `XCO_CP_JSON`, `/UI2/CL_JSON`, `CL_SXML_*`, `CL_IXML_*` |
| **Email** | `CL_BCS_MAIL_MESSAGE` |
| **HTTP Calls** | `CL_WEB_HTTP_CLIENT_MANAGER`, `CL_HTTP_DESTINATION_PROVIDER` |
| **RAP** | `CL_ABAP_BEHV_AUX`, `CL_ABAP_BEHAVIOR_HANDLER`, `CL_ABAP_BEHAVIOR_SAVER` |
| **RTTS** | `CL_ABAP_TYPEDESCR` and hierarchy |
| **Dynamic Programming** | `CL_ABAP_DYN_PRG`, `CL_ABAP_CORRESPONDING` |
| **User Info** | `CL_ABAP_CONTEXT_INFO`, `XCO_CP=>sy->user()` |
| **Unit Testing** | `CL_ABAP_UNIT_ASSERT`, `CL_OSQL_TEST_ENVIRONMENT`, `CL_CDS_TEST_ENVIRONMENT` |
| **Parallel Processing** | `CL_ABAP_PARALLEL` |
| **Application Log** | `CL_BALI_LOG` |
| **Background Jobs** | `CL_BGMC_PROCESS_FACTORY` |
| **Locking** | `CL_ABAP_LOCK_OBJECT_FACTORY` |
| **XLSX** | `XCO_CP_XLSX` |
| **Zip Files** | `CL_ABAP_ZIP` |
| **PDF Rendering** | `CL_FP_ADS_UTIL` |

## Common Use Cases

### Get Current Date/Time in UTC
```abap
"Using CL_ABAP_CONTEXT_INFO
DATA(sys_date) = cl_abap_context_info=>get_system_date( ).  "e.g. 20240101
DATA(sys_time) = cl_abap_context_info=>get_system_time( ).  "e.g. 152450

"Using XCO (various formats)
DATA(date_utc) = xco_cp=>sy->date( xco_cp_time=>time_zone->utc )->as( xco_cp_time=>format->abap )->value.
DATA(time_utc) = xco_cp=>sy->time( xco_cp_time=>time_zone->utc )->as( xco_cp_time=>format->iso_8601_extended )->value.
DATA(moment_utc) = xco_cp=>sy->moment( xco_cp_time=>time_zone->utc )->as( xco_cp_time=>format->iso_8601_extended )->value.
```

### Send Email
```abap
TRY.
    DATA(mail) = cl_bcs_mail_message=>create_instance( ).
    mail->set_sender( 'sender@example.com' ).
    mail->add_recipient( 'recipient@example.com' ).
    mail->set_subject( 'Subject' ).
    mail->set_main( cl_bcs_mail_textpart=>create_instance(
      iv_content      = '<h1>Hello</h1><p>Message body.</p>'
      iv_content_type = 'text/html' ) ).
    mail->send( IMPORTING et_status = DATA(status) ).
  CATCH cx_bcs_mail INTO DATA(error).
ENDTRY.
```

### Generate UUID
```abap
"CL_SYSTEM_UUID
DATA(uuid_x16) = cl_system_uuid=>create_uuid_x16_static( ).
DATA(uuid_c36) = cl_system_uuid=>create_uuid_c36_static( ).

"XCO
DATA(uuid) = xco_cp=>uuid( )->value.
DATA(uuid_c36_xco) = xco_cp=>uuid( )->as( xco_cp_uuid=>format->c36 )->value.
```

### JSON Processing
```abap
"ABAP -> JSON
DATA(json) = xco_cp_json=>data->from_abap( some_structure )->to_string( ).

"JSON -> ABAP
xco_cp_json=>data->from_string( json_string )->write_to( REF #( target_structure ) ).

"Using /UI2/CL_JSON
DATA(json2) = /ui2/cl_json=>serialize( data = some_data ).
/ui2/cl_json=>deserialize( EXPORTING json = json2 CHANGING data = target ).
```

### HTTP Client Call
```abap
TRY.
    DATA(dest) = cl_http_destination_provider=>create_by_url( 'https://api.example.com' ).
    DATA(client) = cl_web_http_client_manager=>create_by_http_destination( dest ).
    DATA(request) = client->get_http_request( ).
    DATA(response) = client->execute( if_web_http_client=>get ).
    DATA(status) = response->get_status( ).
    DATA(body) = response->get_text( ).
  CATCH cx_web_http_client_error cx_http_dest_provider_error INTO DATA(error).
ENDTRY.
```

### Get Current User
```abap
"Using CL_ABAP_CONTEXT_INFO
DATA(user_alias) = cl_abap_context_info=>get_user_alias( ).
DATA(user_name) = cl_abap_context_info=>get_user_formatted_name( ).

"Using XCO
DATA(user) = xco_cp=>sy->user( )->name.
```

## Detailed Reference

For comprehensive code examples and all available classes, read:
- [references/Released_ABAP_Classes.md](references/Released_ABAP_Classes.md)

### Reference File Structure

The reference file is organized into these sections (use grep patterns to search):

| Section | Search Pattern |
|---------|---------------|
| Console Output | `Running a Class and Displaying Output` |
| UUID | `Creating and Transforming UUIDs` |
| SY Components | `XCO Representations of SY Components` |
| RAP | `## RAP` |
| Transactional Consistency | `Transactional Consistency` |
| Numbers/Calculations | `Numbers and Calculations` |
| String Processing | `String Processing` |
| Codepages/Binary | `Handling Codepages and Binary` |
| Regular Expressions | `Regular Expressions` |
| Time and Date | `Time and Date` |
| Calendar | `Calendar-Related Information` |
| RTTS | `Runtime Type Services` |
| Assignments | `## Assignments` |
| Structure Components | `Non-Initial Structure Components` |
| Table Comparison | `Comparing Content of Compatible` |
| Dynamic Programming | `Dynamic Programming` |
| Current User | `Getting the Current User Name` |
| XML/JSON | `XML/JSON` |
| Repository Objects | `ABAP Repository Object Information` |
| Generating Objects | `Generating ABAP Repository Objects` |
| Call Stack | `Call Stack` |
| Email | `Sending Emails` |
| Tenant Info | `Tenant Information` |
| Exceptions | `Exception Classes` |
| Parallel Processing | `Parallel Processing` |
| Application Log | `Application Log` |
| Background Jobs | `Running Code in the Background` |
| Locking | `## Locking` |
| HTTP Calls | `Calling Services` |
| XLSX | `Reading and Writing XLSX Content` |
| Zip Files | `Zip Files` |
| Unit Testing | `ABAP Unit` |
| Units of Measurement | `Units of Measurement` |
| ATC | `Programmatic ABAP Test Cockpit` |
| Number Ranges | `Handling Number Ranges` |
| Releasing APIs | `Releasing APIs` |
| Application Jobs | `Application Jobs` |
| Generative AI | `Generative AI` |
| Transport Requests | `Programmatically Creating and Releasing Transport` |
| HTML/XML Cleanup | `Repairing and Cleaning up HTML` |
| IDE Actions | `Creating and Using IDE Actions` |
| PDF Rendering | `Output Management` |
| CSV Export | `Writing Internal Table Content to CSV` |
| Garbage Collection | `Triggering Garbage Collection` |
