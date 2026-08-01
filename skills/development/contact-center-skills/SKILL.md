---
name: contact-center-skills
description: POST {{baseUrl}}/contactcenter/skills
---

# Create a skill

POST {{baseUrl}}/contact_center/skills


<p>
Create a
<a href="https://support.zoom.us/hc/en-us/articles/4423986613261">
skill
</a>
 for skill-based routing. Skills are agent traits that ensure they are the right person to handle a customer interaction.
</p>



<p>

<strong>
Scopes:
</strong>

<code>
contact_center_skill:write:admin
</code>

</p>



<p>

<strong>

<a href="https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits">
Rate Limit Label
</a>
:
</strong>

<code>
Light
</code>

</p>





### Request Body
```
{&quot;skill_category_id&quot;=&gt;&quot;&lt;string&gt;&quot;, &quot;skill_name&quot;=&gt;&quot;&lt;string&gt;&quot;}
```

### HEADERS
| Key | Datatype | Required | Description |
| `Content-Type` | string |  |  |
| `Accept` | string |  |  |


### RESPONSES

**status**: `Created`
```
{&quot;skill_id&quot;:&quot;\u003cstring\u003e&quot;,&quot;skill_name&quot;:&quot;\u003cstring\u003e&quot;,&quot;skill_type&quot;:&quot;proficiency&quot;,&quot;max_proficiency_level&quot;:3,&quot;skill_category_name&quot;:&quot;\u003cstring\u003e&quot;,&quot;skill_category_id&quot;:&quot;\u003cstring\u003e&quot;,&quot;modified_by&quot;:&quot;\u003cstring\u003e&quot;,&quot;last_modified_time&quot;:&quot;\u003cdateTime\u003e&quot;}
```