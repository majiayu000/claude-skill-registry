---
name: ssl-certificates
description: Let's Encrypt, certbot, auto-renewal, wildcard DNS challenge, SSL troubleshooting with Cloudflare proxy
---

# Skill: SSL Certificates — Let's Encrypt + Cloudflare

## Quando Usar
- Certificado expirado ou prestes a expirar em qualquer domínio do servidor
- Novo domínio/subdomínio precisa de HTTPS (ex: novo preview, novo projeto)
- Renovação automática parou de funcionar (`certbot renew` falhando)
- Nginx retornando erro SSL (handshake fail, mixed content, HSTS problem)

## Contexto

**Domínios ativos neste servidor:**
| Domínio | Proxy CF | Tipo Cert |
|---------|----------|-----------|
| api.myapp.example.com, frontend.example.com | ✅ | Standard |
| myapp.example.com, www. | ✅ | Standard |
| work8.example.com | ✅ | Standard |
| portfolio.example.com | ✅ | Standard |
| neuralnets.example.com | ✅ | Standard |
| app.portfolio.example.com | ✅ | Standard |
| *.preview.myapp.example.com | ✅ | **Wildcard DNS-01** |

**Paths críticos:**