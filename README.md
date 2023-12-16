# pycalc

Pycalc is a simple open source cmd calculator written in Python.
To run it, all one requires it is Git and Python >= 3.6. 

It can do: 

1. arithmetic (float and negative numbers too); 
2. currency exchanges; 
3. various commands (including variable definition). 

For details, when using type "--help" or "-h" in the calculator, it will give you all the commands and actions available. 

## Setup

For all platforms: 

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

To run, type: 

```bash
$ pycalc
```

(You can exit the app with the "-e" or "--exit" commands)

## Updates

The project's not really big and quite spontaneous, so I've decided to add the system for auto-updating it every time someone starts the app.

But if you had pycalc before, then for this to come into work, you need to manually do:

```bash
$ cd path/to/pycalc
$ git pull
```

<!-- * This thing had previously been in the above 'bash' -->
<!-- $ pip install forex-python -->

Because, until now it was the only way of updating. 

<!-- * Old remark... -->
<!-- (+forex-python for currency-exchange, if it isn't installed already).  -->

Later on, you're gonna get them automatically when running the app.

If one is new to pycalc, then none of this is required and once you've installed it, it'll automatically update every time you start it with:

    $ pycalc
