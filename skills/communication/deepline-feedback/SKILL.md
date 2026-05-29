---
name: deepline-feedback
description: "Send feedback or bug reports to the Deepline team, including session transcript and environment info."
disable-model-invocation: false
---

# Deepline Feedback

Send feedback or a bug report to the Deepline team.

## Steps

1. **Get feedback text.** Use the argument if provided (e.g. `/deepline-feedback the waterfall broke`). Otherwise ask the user.

2. **Confirm.** Use AskUserQuestion with a question like:

   > This report will include:
   > - Your feedback: {feedback text}
   > - Environment info (auto-collected)
   > - Current session transcript
   >
   > Send this feedback?

   Options: "Send it" / "Cancel".

3. **If confirmed**, run:
   ```
   deepline provide-feedback --text "{feedback text}" --json
   deepline session send --current-session --json
   ```

4. Tell the user it was sent. If cancelled, do nothing.
