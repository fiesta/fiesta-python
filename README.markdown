# fiesta-python

Python wrapper for Fiesta's list management API.

http://fiesta.cc

http://docs.fiesta.cc



## Installation
The quickest way to installt his package is with pip:

    pip install git://github.com/fiesta/fiesta-python.git

## Usage

Here is an extremely basic usage example to make sure everything is installed correctly

```pyton
from fiesta.fiesta import FiestaAPI
fiesta = FiestaAPI()
response = fiesta.hello()
print response
# Should read { "hello": "world" }
```