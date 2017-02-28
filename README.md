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

###Init database
run scripts db_create.py then db_init.py
db_create.py : create the database
db_init.py : parse csv files from csv/ to initialize the database with defaults values

```shell
# if you have install flask through virtualenv
# (check first if scripts have execution rights)
./db_create.py
./db_init.py

# if you have install flask through pip
# (recommended to use python3 and pip3)
python db_create.py
python db_init.py
```

###TODO

* refactor database
    * remove resp_id field from User table
    * add field dept in User table
    * refactor some functions to manage new departement and supervisor access
* more
    * reset database (admin action)
    * archive datas / export csv (action admin)
