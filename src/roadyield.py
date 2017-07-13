'''
RAET Tutorial Examples for RoadStack
'''
import time
import signal

from collections import deque

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

def closeStack(stack):
    """
    Close RoadStack
    """
    stack.server.close()  # close the UDP socket
    stack.keep.clearAllDir()  # clear persisted data

def threadAlpha(stack,  delay=0.125):
    """
    return generator function threader in closure to run stack
    """
    addJoinRemote(stack, "beta", 7532)
    addJoinRemote(stack, "gamma", 7533)

    timer = ioflo.aid.timing.StoreTimer(store=stack.store, duration=1.5)
    while not timer.expired:
        stack.serviceAll()
        yield
        stack.store.advanceStamp(delay)

    msg = odict([("subject", "Introduction"),
                 ("content", "Hello from alpha")])
    messageAll(stack, msg)

    timer.extend(extension=1.5)
    while not timer.expired:
        stack.serviceAll()
        yield
        stack.store.advanceStamp(delay)

    printAll(stack)
    closeStack(stack)

    return

def threadBeta(stack,  delay=0.125):
    """
    return generator function threader in closure to run stack
    """
    addJoinRemote(stack, "gamma", 7533)

    timer = ioflo.aid.timing.StoreTimer(store=stack.store, duration=1.5)
    while not timer.expired:
        stack.serviceAll()
        yield
        stack.store.advanceStamp(delay)

    msg = odict([("subject", "Introduction"),
                 ("content", "Hello from beta")])
    messageAll(stack, msg)

    timer.extend(extension=1.5)
    while not timer.expired:
        stack.serviceAll()
        yield
        stack.store.advanceStamp(delay)

    printAll(stack)
    closeStack(stack)

    return

def threadGamma(stack,  delay=0.125):
    """
    return generator function threader in closure to run stack
    """
    timer = ioflo.aid.timing.StoreTimer(store=stack.store, duration=1.5)
    while not timer.expired:
        stack.serviceAll()
        yield
        stack.store.advanceStamp(delay)

    msg = odict([("subject", "Introduction"),
                 ("content", "Hello from gamma")])
    messageAll(stack, msg)

    timer.extend(extension=1.5)
    while not timer.expired:
        stack.serviceAll()
        yield
        stack.store.advanceStamp(delay)

    printAll(stack)
    closeStack(stack)

    return

def run(threads, delay=0.125, duration=4.0):
    """
    run generators in threads
    """
    timer = ioflo.aid.timing.Timer(duration=duration)
    while not timer.expired and threads:
        time.sleep(delay)
        agains = []
        for thread in threads:
            try:
                next(thread)
            except StopIteration as  ex:
                pass
            else:
                agains.append(thread)
        threads = list(agains)  # copy


if __name__ == "__main__":
    print("********** Yielded Example Threeway Road *****************\n")

    alpha = createStack('alpha', 7531)
    beta = createStack('beta', 7532)
    gamma = createStack('gamma', 7533)

    delay = 0.125
    threads = [threadAlpha(alpha, delay),
                 threadBeta(beta, delay),
                 threadGamma(gamma, delay)]

    run(threads, delay=delay)
    print("********** Done Yielded Example Threeway Road *****************\n")

