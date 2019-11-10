import uuid
import datetime

from .env import HN_DB


# The url for connecting to our database
dbHostURL = 'http://{host}'.format(
    host = HN_DB,
)

