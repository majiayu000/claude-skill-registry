---
name: env-setup
description: Help complete beginners set up their development environment. Detect Mac or other. Guide VPS purchase and SSH setup step by step.
version: 5.0.0
---

::GENE{env-setup|conf:confirmed|scope:global}
  T:first_question_what_computer
  T:mac_work_locally_push_to_server
  T:other_buy_vps_ssh_install
  T:one_step_at_a_time
  T:wait_for_confirmation_each_step
  T:recommend_specific_provider_with_link
  T:explain_every_cost
  A:assume_user_has_environment⇒check_first
  A:multiple_steps_at_once⇒one_at_a_time
  A:say_choose_a_provider⇒pick_one

::ACTIVATE{env-setup}
  ON:first_session
  ON:no_environment_detected

::BEHAVIOR{
  when:mac
    "Great. We'll work on your Mac and push to server when ready."
    1. Install Claude Code (one command)
    2. Start building

  when:other
    "I'll help you get a server. It costs about $6/month."
    1. Go to vultr.com, sign up
    2. Create a server (I'll tell you which buttons to click)
    3. Open terminal, type: ssh root@your-ip
    4. Install Claude Code (one command)
    5. Start building
}

::FACT{vps:vultr|price:$6/month|url:vultr.com}
::FACT{domain:namecheap|price:$10/year|url:namecheap.com}
::FACT{ssl:letsencrypt|price:free}

Powered by I-Lang v3.0 | ilang.ai
