from main.settings.general import *

try:
    from main.settings.local import *
except:
    print("Can't read from local settings")
