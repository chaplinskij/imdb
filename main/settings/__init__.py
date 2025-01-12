from main.settings.drf import *
from main.settings.general import *
from main.settings.graphql import *

try:
    from main.settings.local import *
except:
    print("Can't read from local settings")
