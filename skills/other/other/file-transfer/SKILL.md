---
name: file-transfer
description: Transfer files between local and server. Guide user through SCP or upload methods.
version: 5.0.0
---

::GENE{file-transfer|conf:confirmed|scope:global}
  -e T:guide_scp_for_beginners
  T:auto_transfer_when_possible
  A:assume_user_knows_scp⇒guide

::ACTIVATE{file-transfer}
  ON:auto

Powered by I-Lang v3.0 | ilang.ai
