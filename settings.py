import os
import re
from string import ascii_letters, digits


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',
                                        default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='SECRET_KEY')


NAME_FUNK_SHORT_ID = 'get_url_map'
APPROVED_SYMBOLS = ascii_letters + digits
LENGTH_SHORT_ID = 6
REGEX_SYMBOLS_SHORT_ID = rf'^[{re.escape(APPROVED_SYMBOLS)}]*$'
MAX_LENGTH_ORIGINAL = 2000
MAX_LENGTH_SHORT_ID = 16
QUANTITY_GENERATIONS = 10
