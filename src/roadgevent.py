'''
RAET Tutorial Examples for RoadStack
'''
import time
import signal

import ioflo
from ioflo.aid import odict
from ioflo.base.consoling import getConsole


import raet
from raet import raeting
from raet.raeting import AutoMode

import gevent  # do not have to monkey patch raet io

console = getConsole()
console.reinit(verbosity=console.Wordage.concise)


def createStack(name, port):
    """
    Create and return RoadStack with name port
    """
    store = ioflo.base.storing.Store(stamp=0.0)
    stack = raet.road.stacking.RoadStack(store=store,
                                         name=name,
                                         ha=('0.0.0.0', port),
                                         main=True,
                                         mutable=True,
                                         auto=AutoMode.always.value)
    return stack

def addJoinRemote(stack, name, port):
    """
    Create and add remote with name port to stack
    """
    if name in stack.nameRemotes:
        remote = stack.nameRemotes[name]
    else:
        remote = raet.road.estating.RemoteEstate(stack=stack,
                                             name=name,
                                             ha=("localhost", int(port)))
        stack.addRemote(remote)
    stack.join(uid=remote.uid, cascade=True)

def messageAll(stack, msg):
    """
    Send message to all remotes
    """
    for remote in stack.remotes.values():
        stack.transmit(msg, remote.uid)

def printAll(stack):
    """
    Print out all received messages
    """
    print("Stack {0} received:\n".format(stack.name))
    while stack.rxMsgs:
        msg, source = stack.rxMsgs.popleft()
        print("source = '{0}'.\nmsg= {1}\n".format(source, msg))

def serviceStack(stack, duration=4.0):
    """
    Service RoadStack with gevented process
    """
    timer = ioflo.aid.timing.StoreTimer(store=stack.store, duration=duration)
    while not timer.expired:
        stack.serviceAll()
        gevent.sleep(0.125)
        stack.store.advanceStamp(0.125)

def closeStack(stack):
    """
    Close RoadStack
    """
    stack.server.close()  # close the UDP socket
    stack.keep.clearAllDir()  # clear persisted data

if __name__ == "__main__":
    print("********** Gevent Example Threeway Road *****************\n")
    gevent.signal(signal.SIGQUIT, gevent.kill)

    alpha = createStack('alpha', 7531)
    beta = createStack('beta', 7532)
    gamma = createStack('gamma', 7533)

    addJoinRemote(alpha, "beta", 7532)
    addJoinRemote(alpha, "gamma", 7533)
    addJoinRemote(beta, "gamma", 7533)

    alphaThread = gevent.spawn(serviceStack, alpha)
    betaThread = gevent.spawn(serviceStack, beta)
    gammaThread = gevent.spawn(serviceStack, gamma)

    gevent.sleep(1.5)
    print("Queing messages\n")

    msg = odict([("subject", "Introduction"),
                 ("content", "Hello from alpha")])
    messageAll(alpha, msg)

    msg = odict([("subject", "Introduction"),
                 ("content", "Hello from beta")])
    messageAll(beta, msg)

    msg = odict([("subject", "Introduction"),
                 ("content", "Hello from gamma")])
    messageAll(gamma, msg)

    gevent.sleep(1.5)

    printAll(alpha)
    printAll(beta)
    printAll(gamma)

    gevent.joinall([alphaThread, betaThread, gammaThread])

    closeStack(alpha)
    closeStack(beta)
    closeStack(gamma)
