This project is clone of [libmpsse](http://code.google.com/p/libmpsse) with some updates and fixes.

### Build on linux
1. Install libftdi, swig
2. From src directory run `autoconf && ./configure && make`

### Build on OSX
1. Install MacPorts
2. Install Xcode command line tools
3. run `sudo port install libftdi swig-python`
4. From src directory run `autoconf && ./configure && make`

### Build on Windows
1. Install MinGW with msys shell
2. In msys shell run `mingw-get install mingw32-automake mingw32-autotools mingw32-autoconf`
3. Install [ftdi for mingw](http://code.google.com/p/picusb/downloads/list)
4. Install Python2.7 to default directory (C:\Python27)
5. From src directory run (using msys shell) `autoconf && ./configure && make`


For more details see original project wiki
