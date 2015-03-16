# harmelapp

Kivy is a platform for making mobile apps, which uses python.  once you build the app for android or iOS, the end user need only install the app (the kivy layer is included in the app).  However, to run a kivy app on desktop, you must install kivy on you machine.  http://kivy.org/#download

i can't give advice on installing kivy on osX or Windows.  on linux, i recommend you create a virtualenv for kivy, as you will need to downgrade your cython to 0.21.2, etc.  see the kivy webpage for install scripts.  Once all the requirements are installed, running the app is as simple as entering the project directory in your virtualenv and running 'python main.py'.  

my app is a simple musical instrument.  any further description is moot, since playing the app should be intuitive (else i've done a poor job).