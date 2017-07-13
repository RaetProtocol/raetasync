'''
RAET Tutorial Examples for RoadStack
'''
import time

from ioflo.aid import getConsole

import raet

console = getConsole()
console.reinit(verbosity=console.Wordage.concise)


if __name__ == "__main__":
    print("********** Looping Example Threeway Road *****************\n")
    threeway()

