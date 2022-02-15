# Pycalc

Pycalc is a simple open source cmd calculator written in Python. It has all basic arithmetic operations(addition, subtraction, division, whole division, taking the remainder of the devision, multiplication and exponentation) and can work with any quantity of numbers. It supports integers and floats. To specify a float number type 'f' before it, to specify a negative number type 'n'.

Examples of a negative float number: "fn42.42" or "fn111,1",
negative integer: "n42".

Also it allows you to get currency exchange values for different currencies and actually USE them in arithmetic expressions.
To get more info type "-h" command in the pycalc after installing and starting it.

## Setup

It's simple enough. Just clone the repository in the required directory after which run the setup.bat(Windows) or setup.sh(Linux, similiar platforms supporting bash) as an administrator.

It looks a bit like this:

```bash
$ cd path/to/
$ git clone https://github.com/HGARgG-0710/pycalc.git
$ cd pycalc
```

Windows (as an Administrator):

```batch
setup.bat
```

Linux, macOS and others:

```bash
$ sudo setup.sh
```

## Use

After you have done everything requiered in the "Setup" section, you need to type

```bash
$ pycalc
```

in your shell. And that's it. These are all the steps you need to make to fully install and setup pycalc on your computer. Wish you happy using!

(You can exit the app with the "-e" or "--exit" commands)

## Updates

The project's not really big and quite spontaneous, so I've dicided to add the system for auto-updating it every time someone starts the app.

But if you had pycalc before, then for this to come into work, you need to manually do:

```bash
$ cd path/to/pycalc
$ git pull
```

Because, until now it was the only way of updating. Later on, you're gonna get them automatically.

By the way, if you're new to pycalc, then none of this is required and once you've installed it, it'll automatically update every time you start it with:

    $ pycalc

So, don't panic if you see any scary git output, probably it's just me cleaning the code or implementing a new feature. :D
