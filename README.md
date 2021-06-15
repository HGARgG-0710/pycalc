# Pycalc

Pycalc is a simple open source cmd calculator written in Python. It has all basic operations(addition, subtraction, division, whole division, taking the remainder of the devision, multiplication and exponentation) and can work with any quantity of numbers. It supports integers and floats. To specify a float number type 'f' before it, to specify a negative number type 'n'.

Example of a negative float number: "fn42.42",
negative integer: "n42".

Also it allows you to get currency exchange values for different currencies and actually USE them in mathematical expressions.
To get more info type "-h" command in the pycalc after installing and starting it.

## Setup

It's easy. Just clone the repository in the needed directory and then run the setup.bat(if you're on Windows) or setup.sh(if you're on Linux or any other platform supporting bash) as an administrator.

It looks a bit like this:

    $ git clone https://github.com/HGARgG-0710/pycalc.git
    $ cd pycalc

Windows (as an Administrator):

    setup.bat

Linux, macOS and others:

    $ sudo setup.sh

## Use

After you have done everything requiered in the "Setup" section, you need to type

    $ pycalc

in your shell. Aaaand... that's it! These are all the steps you need to do to fully install and setup pycalc on your computer. Wish you happy using!

## Updates

The project's not really big and quite spontaneous, so I've dicided to add the system for auto-updating it every time someone starts the app.

But if you had pycalc before, then for this to come into work, you need to manually do:

    $ cd "path/to/pycalc"
    $ git pull

Because, until now it was the only way of updating. Later on, you're gonna get them automatically.

By the way, if you're new to pycalc, then none of this is required and once you've installed it, it'll automatically update every time you start it with:

    $ pycalc

So, don't get scared off if you see any scary git output, probably it's just me cleaning the code or implementing a new feature :)