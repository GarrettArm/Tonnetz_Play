# harmelapp

Kivy is a platform for making mobile apps, which uses python.  once you build the app for android or iOS, the end user need only install the app (the kivy layer is included in the app).  However, to run a kivy app on desktop, you must install kivy on you machine.  http://kivy.org/#download

i can't give advice on installing kivy on osX or Windows.  on linux, i recommend you create a virtualenv for kivy, as you may need to make package changes not desired for the global OS (i.e., downgrade your cython to 0.21.2, etc.)  See the kivy webpage for install scripts.  Once all the requirements are installed, running the app is as simple as entering the project directory in your virtualenv and running 'python main.py'.

my app is a simple musical instrument.  any further description is moot, since playing the app should be intuitive (else i've done a poor job).

Acknowledgements:

Dan Cartwright produced a editable set of tonnetz files, which inspired much of my design.

Larry Polansky guided me to studying 7-limit just intonation, which played heavily in the early versions on this app.  Unfortunately, the current kivy API (as of 6-1-2105) does not support the necessary functions in an android or iOS build -- I hope to reintroduce 7-limit and greater limits if supported by future versions of the API.
