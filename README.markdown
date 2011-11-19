# fiesta-python

Python wrapper for Fiesta's list management API.

http://fiesta.cc

http://docs.fiesta.cc

## Installation
The quickest way to install this package is with pip:

    pip install git://github.com/fiesta/fiesta-python.git

## Usage

Here is an extremely basic usage example to make sure everything is installed correctly:

```python
from fiesta import FiestaAPI
fiesta = FiestaAPI()
print fiesta.hello()
# Should print {u'hello': u'world'}
```

Here is how you would create a group:

```python
fiesta = FiestaAPI('your-client-id-here', 'your-client-secret-here')
group = FiestaGroup.create(fiesta, default_name='new-group' description='My new group!')
```

Here is how you would add new users to an existing group:

```python
fiesta = FiestaAPI('your-client-id-here', 'your-client-secret-here')
group = FiestaGroup(fiesta, id='MyGroupID')  # Group IDs look something like this: Ar4i3_yFstAyA9AA
new_user = group.add_member('test@example.com', member_display_name="Test User")
```

## Testing

To run the tests, you'll need valid Fiesta client credentials (the tests connect to the Fiesta [API sandbox](http://docs.fiesta.cc/sandbox.html)). Create a file in the `test/` directory called `settings_test.py` with the following contents:

```python
FIESTA_CLIENT_ID = 'your-client-id-here'
FIESTA_CLIENT_SECRET = 'your-client-secret-here'
```

The easiest way to run the tests is to install [nose](http://readthedocs.org/docs/nose/en/latest/) and run `nosetests`.

## License

This project is licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0

## TODO

  * Handle errors!
  * Handle OAuth for user auth
  * Improve tests to cover cases. Mainly to cover tests for the wrapper throwing errors on bad input.

## Credits

  * Jeremy Blanchard ([auzigog](https://github.com/auzigog)) - Initial list management wrapper features, original author of this project.
