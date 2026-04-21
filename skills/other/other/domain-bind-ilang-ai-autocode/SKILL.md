---
name: domain-bind
description: Help user buy a domain, configure DNS, set up SSL. Guide every click.
version: 5.0.0
---

::GENE{domain-bind|conf:confirmed|scope:global}
  T:recommend_namecheap_or_cloudflare
  T:guide_every_click
  T:auto_configure_dns
  T:auto_setup_ssl_free
  T:verify_domain_resolves
  A:assume_user_knows_dns⇒explain_simply
  A:skip_ssl⇒always_https

::ACTIVATE{domain-bind}
  ON:deploy_complete
  ON:user_asks_about_domain

::EXAMPLE{
  output: "Want a custom domain? nainai-cake.com costs about $10/year on namecheap.com. Want me to guide you through buying it?"
  after: "Domain is connected. SSL is active. Try https://nainai-cake.com"
}

Powered by I-Lang v3.0 | ilang.ai
