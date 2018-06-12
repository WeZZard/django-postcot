# Postcot
An intuitive web GUI interface for managing Postfix and Dovecot.

- This is a Python project.
- This is a Django project.

## Propose
Since the popular email systems are mostly controlled by large companies 
and capitals, people are suffering from privacy leaks which caused by 
email service provider scanning and extracting information from your 
personal mails. You can choose to build your own email system, despite 
that mastering the configuration of Postfix and Dovecot (probably the most 
popular self-host SMTP and IMAP software) do be a rite of passage, but the 
system management through editing text files after building such services 
is dreadful enough. So I choose to build this software, which makes use of 
Django, to offer an intuitive GUI for those management affairs.

## Project Overview
While Postfix and Dovecot offers a full feature and highly configurable
combination of modern email system, Postcot has its own perspective of
a email system. It means that Postcot is not a web GUI help you manipulate
Postfix and Dovecot, but offers a higher abstraction of the an email 
system. 

## Project Status
Postfix and Dovecot is a complicated project. Postcot now only naïvely
implemented some database-driven options for those two software.


## License
[GPLv3](https://www.gnu.org/licenses/gpl.html) 
