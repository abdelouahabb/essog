Essog
=====

simple tornado-motor e-commerce

I want to thank all those who have helped me: [stackoverflow][1], [tornado][2], [mongodb][3] communities.

Dependecies:
=====

The project is a simple e-commerce (without payement system. since it dont exists here in Algeria), it will depend one some libraries:

 1. [Tornado][4]: of course, the server, the framework ;)
 2. [Motor][5] (of course Pymongo) : for non-blocking access for Mongodb.
 3. [Passlib][6] : for hashing password. (you can use Bcrypt or Scrypt, but i have used windows, so they dident compile on my machine).
 4. [PIL][7]: for pictures operations.
 5. [Python-Amazon-Simple-Product-Api][8]: for making requests to Amazon.
 6. [SimpleEncode][9]: to use strings to encode another string.
 7. [User Agents][10]: to force user to use HTML5

How to run it :
=====
Of course, you **MUST** have Python installed, windows users, come here:

http://python.org/download/releases/2.7.5/


Simple, just run 

    app.py

on linux:

    sudo python app.py

 on windows 

Directly double-clic on **app.py** or **open it with a good editor**  


Go to the url (in your browser) [http://localhost:8000][11]

**How  to download this :o**

simple, just look where it is written **Download Zip** or something similar :p

**How  to download the library tou said that i need it!**

after doanloading the library, just uncompress it, on linux, **right clic in the directory (blank area) and choose something like Open Terminal Here**.

    sudo python setup.py install

or on windows, **Hold shift, right clic on a blank area on your folder (not on your file)** and choose **Open Terminal Here** or something like that

    python setup.py install


  [1]: http://stackoverflow.com/
  [2]: https://groups.google.com/forum/#!forum/python-tornado
  [3]: https://groups.google.com/forum/#!forum/mongodb-user
  [4]: https://github.com/facebook/tornado
  [5]: https://github.com/mongodb/motor
  [6]: https://code.google.com/p/passlib/
  [7]: http://www.pythonware.com/products/pil/
  [8]: https://github.com/yoavaviram/python-amazon-simple-product-api
  [9]: https://code.google.com/p/python-simpleencode/
  [10]: https://github.com/selwin/python-user-agents
  [11]: http://localhost:8000
