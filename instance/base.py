"""
These are the default settings. Out-of-the-box, this should "just work".
Override these by creating a `settings.py` file in this folder (`instance`) and customizing like this::
    SECRET_KEY = 'ARealSecret'
    DB_CONNECTION_STRING = 'MyRealPassword'
    ...
"""
class Config(object):
    SECRET_KEY = 'SECRET'
    DB_CONNECTION_STRING = 'sqlite:///career.db'
