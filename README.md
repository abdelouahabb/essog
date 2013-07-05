essog
=====

simple tornado-motor e-commerce

I want to thank all those who have helped me: stackoverflow, tornado, mongodb community.

Dependecies:
=====

The project is a simple e-commerce (without payement system. since it dont exists here in Algeria), it will depend one some libraries:

Tornado: of course, the server, the framework ;)
https://github.com/facebook/tornado

Motor (of course Pymongo) : for non-blocking access for Mongodb.
https://github.com/mongodb/motor

Passlib : for hashing password. (you can use Bcrypt or Scrypt, but i have used windows, so they dident compile on my machine).
https://code.google.com/p/passlib/

PIL: for pictures operations.
http://www.pythonware.com/products/pil/

Python-Amazon-Simple-Product-Api: for making requests to Amazon.
https://github.com/yoavaviram/python-amazon-simple-product-api

SimpleEncode: to use strings to encode another string.
https://code.google.com/p/python-simpleencode/

User Agents: to force user to use HTML5
https://github.com/selwin/python-user-agents
