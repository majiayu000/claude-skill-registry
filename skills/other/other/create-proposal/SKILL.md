---
description: Create a PandaDoc proposal for a client
---

## Tool
**Script:** `execution/create_proposal.py`
**Usage:** Automatically generates PandaDoc proposals from structured input

## Process

1. **Gather Information**
   - The user may provide information in one of two formats:
     
     **Option A: Structured Bullet Points** (if user provides organized data)
     - Client First Name
     - Client Last Name
     - Client Email
     - Client Company
     - Project Title
     - 4 Key Problems (brief)
     - 4 Key Benefits (brief)
     - Project Duration
     - Project Value (Total)
     - Platform Costs
     - Investment Breakdown (Month 1, Month 2, Month 3+)
     
     **Option B: Call Transcript** (if user provides a sales call transcript)
     - Extract the following from the transcript:
       - Client information (name, company, email if mentioned)
       - Project context and title
       - 4 main problems/pain points discussed
       - 4 proposed solutions/benefits
       - Any financial terms discussed (duration, value, costs)
     - If any critical information is missing from the transcript, ask the user to provide it
   
   - If information is not already provided in either format, ask the user for the missing details

1b. **Research Client (Optional)**
   - **Goal:** Understand the client's brand voice and current context to personalize the proposal.
   - **Trigger:** If a website URL is provided or can be inferred from the client's email domain (and it's not a generic domain like gmail.com).
   - **Action:**
     - Use `read_url_content` to fetch the client's landing page or "About Us" page.
     - **Analyze**:
       - **Brand Voice:** (e.g., Professional/Corporate, Friendly/Startup, Technical/Niche)
       - **Keywords:** Key terms they use to describe their own value.
       - **Recent Context:** Any recent news or specific focus areas mentioned on the site.
   - **Output:** A brief "Client Research Summary" to be used in the next step.

2. **Generate Content**
   - Using the gathered information **and the Client Research Summary (if available)**, generate the following expanded content:
     - **Problem Expansions**: Expand each of the 4 problems into 1-2 strategic paragraphs (max 50 words each). 
       - **Contextualization:** Use the *Client Research Summary* to mirror their industry terms and brand voice where appropriate.
       - **Tone & Style Guidelines:**
         - Use direct "you" language (not third-person or passive voice)
         - Focus on revenue impact and dollar amounts wherever possible
         - Be specific and actionable rather than abstract
         - Think "revenue ops" mindset - quantify business impact
         - Example: "Right now, your top-of-funnel is converting very poorly to booked meetings. You have no problem generating opportunities; your problem is capitalizing on them. Even a few percentage-point improvement here would lead to many tens of thousands of dollars of additional income"
     - **Benefit Expansions**: Expand each of the 4 benefits into 1-2 implementation-focused paragraphs (max 50 words each).
       - **Tone & Style Guidelines:**
         - Use direct "you" language addressing the client
         - Emphasize ROI, payback period, and financial outcomes
         - Be specific about implementation and expected dollar impact
         - Focus on concrete deliverables and measurable results
     - **Slide Footer**: "Confidential | [Company] Strategic Initiative | [Date]"
     - **Contract Footer Slug**: "[Company]-[ProjectTitle]-[YYYY-MM]"
     - **Created Date**: Current date in YYYY-MM-DD format.

3. **Execute Proposal Creation**
   - **Tool:** `execution/create_proposal.py`
   - **Usage:** Save the JSON to a file and run: `python3 execution/create_proposal.py < input.json`
   - Construct a JSON object with the following structure:
     ```json
     {
       "client": {
         "firstName": "...",
         "lastName": "...",
         "email": "...",
         "company": "..."
       },
       "project": {
         "title": "...",
         "problems": {
           "problem01": "[Expanded Problem 1]",
           "problem02": "[Expanded Problem 2]",
           "problem03": "[Expanded Problem 3]",
           "problem04": "[Expanded Problem 4]"
         },
         "benefits": {
           "benefit01": "[Expanded Benefit 1]",
           "benefit02": "[Expanded Benefit 2]",
           "benefit03": "[Expanded Benefit 3]",
           "benefit04": "[Expanded Benefit 4]"
         },
         "monthOneInvestment": "...",
         "monthTwoInvestment": "...",
         "monthThreeInvestment": "..."
       },
       "generated": {
         "slideFooter": "...",
         "contractFooterSlug": "...",
         "createdDate": "..."
       }
     }
     ```
   - Run the python script:
     ```bash
     # Pass the JSON as a string to the script
     python3 execution/create_proposal.py <<'EOF'
     [JSON_CONTENT]
     EOF
     ```
   - **Note**: Ensure the JSON is valid and properly escaped if necessary.

4. **Send Follow-Up Email**
   - Immediately after proposal creation, send a follow-up email to the client using the template below.
   - Use `gmail.send_email` with `mimeType="text/html"` to send the email in HTML format.
   - **Email Template Structure:**
     - Subject: "Re: [Brief Project Context] Discussion"
     - Opening: Thank them for discussing their challenges/goals
     - Body: Break down the proposed solution into 2-4 numbered sections with clear headers
     - Each section should have:
       - **Bold section header** describing the deliverable (e.g., "1. Tool Consolidation Audit & Migration Plan")
       - Brief description of what it accomplishes
       - "Steps:" subheading followed by bullet points (use `<ul>` and `<li>` HTML tags)
     - Closing: "I'll send you a full proposal for the above shortly. Let me know if you have any questions or want to discuss further."
     - Signature: "Thanks, Nick"
   - **HTML Formatting Requirements:**
     - Use `mimeType="text/html"` parameter
     - Provide both `body` (plain text) and `htmlBody` (HTML version) parameters
     - In HTML: Use `<p>` tags for paragraphs, `<ul>` and `<li>` for bullet lists
     - Bold section headers ONLY using `<strong>` tags (e.g., `<strong>1. Tool Consolidation Audit &amp; Migration Plan</strong>`)
     - Do NOT bold body text or steps - only section headers
     - Avoid RFC 2822 plain text wrapping issues by using HTML format

5. **Notify User**
   - Show the "internalLink" to the user for review and editing in PandaDoc
   - Confirm that the follow-up email was sent successfully
