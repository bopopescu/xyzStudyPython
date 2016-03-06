import sys
import traceback

try:
    test = 10 / 0
except Exception as e:
    print e
    traceback.print_exc()
    print sys.exc_info()
