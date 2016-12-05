#Projet Python Vacances

##Install Flask

`virtualenv -p /usr/bin/python3 flask`

##Setenv proxy 

HTTP_PROXY=http://cache.esiee.fr:3128
HTTPS_PROXY=http://cache.esiee.fr:3128

##À installer

###Install Flask

`virtualenv -p /usr/bin/python3 flask`

###Modules (à installer avec pip3)

* ldap3
* flask_sqlalchemy
* flask_wtf
* sqlalchemy
* sqlalchemy-migrate
* flask-mail
* flask-bootstrap
* flask-login

###TODO

* templates views for mails (.txt and .html)
* session for current user login-in
* error page for wrong password on login
* organize imports
* move db methods from app/models.py to app/utils/db_methods.py (keep only models on app/models.py)
* db init script
* unit tests
* more 
    * reset database (admin action)
    * archive datas / export csv (action admin)

