# fiesta-python

Python wrapper for Fiesta's list management API.

http://fiesta.cc

http://docs.fiesta.cc



## Installation
The quickest way to installt his package is with pip:

    pip install git://github.com/fiesta/fiesta-python.git

## Usage

Here is an extremely basic usage example to make sure everything is installed correctly:

    from fiesta import FiestaAPI
    fiesta = FiestaAPI()
    print fiesta.hello()
    # Should print {u'hello': u'world'}

Here is how you would create a group:

    fromt fiesta import FiestaAPI
    fiesta = FiestaAPI('my-client-id-here', 'my-client-secret-here')
    group = fiesta.group.create(description='My new group!')


## Authentication
Note that this library currently assumes that client is a *trusted client*. See the
[authentication docs](http://docs.fiesta.cc/authentication.html) for more information. We're hoping that someone who
is actively using the the OAuth authentication will help extend the library to handle those use cases. Pull requests
are welcomed!



## TODO

  * Handle errors!
  * Handle OAuth for non-trusted clients