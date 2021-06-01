# mobile-bank-app
A bank application using the python django framework
To use this application, Key open your terminal or bash 
Run the following commands
# python3 manage.py makemigrations
This is to makemigrations of the models and forms into the mysqlite database
next command is 
# python3 manage.py migrate
This is to effect the changes

The last command is 
# python3 manage.py runserver

This is to start the local server host http://127.0.0.1:8000.

# Application Description:
## This python-django application is an application that integrates the django built authentication system.
### A user can only check account balances when authenticated. Unless the user is a registered user on the application, a visiting user can not use the application
### User must be authenticated to use the bank application , like a real bank
### user can deposit and withdraw amount from this application.
#### a user can not withdraw more than their account balance.



