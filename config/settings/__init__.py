from config.settings.drf import *
from config.settings.general import *
from config.settings.graphql import *

try:
    from config.settings.local import *
except:
    print("Can't read from local settings")
