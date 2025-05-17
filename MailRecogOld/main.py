# Should this always be running? 
    # Do we have to reinitiate everything every time we want to run?

# For now lets go with the reinit approach
# TODO Fix server staying open
import subprocess
import os
import sys
sys.tracebacklimit = 0

def main():
    os.system("python ./ServerTry/server.py &")
    os.system("python ./ServerTry/client.py")
    return 0 


main()