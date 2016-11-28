#Projet Python Vacances

##Install Flask

`virtualenv -p /usr/bin/python3 flask`


##Config app

_Be aware you should **NOT** commit you personnal data_

###Mail server
You need to define environment variables to setup the mail address used by the app
By default, configs are defined for gmail client, you have to change config.py if you want to use another provider
```shell
export MAIL_USERNAME='username@host.domain'
export MAIL_PASSWORD='pass'

# you will probably need to reload you bashrc to apply changes
source ~/.bashrc
```

##Setenv proxy 

HTTP_PROXY=http://cache.esiee.fr:3128
HTTPS_PROXY=http://cache.esiee.fr:3128

