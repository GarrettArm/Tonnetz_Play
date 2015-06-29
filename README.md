# Tonnetz Play

Kivy is a platform for making mobile apps, which uses python.  Once you build the app for android or iOS, the end user need only install the app (the kivy layer is included in the app).  However, to run a kivy app on desktop, you must install kivy on you machine.  http://kivy.org/#download

I can't give advice on installing kivy on osX or Windows.  On linux, there are a bunch of requirements you'll need to install, so i recommend you create a virtualenv for kivy (i.e., you'll need to downgrade your cython to 0.21.2, etc.)  See the kivy downloads webpage for install scripts.  When all the requirements are installed (and that's a big when), running the app is as simple as entering the project directory in your virtualenv and running 'python main.py'.

There's a compiled android apk in the bin/ directory, if you want a shortcut to installing on android.  I purposely didn't give it any access to anything, including contacts, internet, etc.

My app is a simple musical instrument.  Any further description is moot, since playing the app should be intuitive (else i've done a poor job).
