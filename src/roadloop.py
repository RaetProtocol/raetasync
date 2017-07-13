'''
RAET Tutorial Examples for RoadStack
'''
import time

import ioflo
from ioflo.base.consoling import getConsole


import raet
from raet import raeting
from raet.raeting import AutoMode

console = getConsole()
console.reinit(verbosity=console.Wordage.concise)

def serviceStacks(stacks, duration=1.0, period=0.1):
    '''
    Utility method to service queues. Call from test method.
    '''
    store = ioflo.base.storing.Store(stamp=0.0)
    timer = ioflo.aid.timing.StoreTimer(store=store, duration=duration)
    while not timer.expired:
        for stack in stacks:
            stack.serviceAll()
            stack.store.advanceStamp(period)

        store.advanceStamp(period)
        if all([not stack.transactions for stack in stacks]):
            break
        time.sleep(period)
    console.concise("Perceived service duration = {0} seconds\n".format(timer.elapsed))


def threeway():
    alpha = raet.road.stacking.RoadStack(name='alpha',
                                         ha=('0.0.0.0', 7531),
                                         main=True,
                                         auto=AutoMode.always.value)

    beta = raet.road.stacking.RoadStack(name='beta',
                                        ha=('0.0.0.0', 7532),
                                        main=True,
                                        auto=AutoMode.always.value)

    gamma = raet.road.stacking.RoadStack(name='gamma',
                                        ha=('0.0.0.0', 7533),
                                        main=True,
                                        auto=AutoMode.always.value)


    # joins are bidirectional
    # so beta joining alpha also results in alpha joining beta
    remote = raet.road.estating.RemoteEstate(stack=alpha,
                                             name=beta.name,
                                             ha=beta.ha)
    alpha.addRemote(remote)
    alpha.join(uid=remote.uid, cascade=True)  # alpha and beta join

    remote = raet.road.estating.RemoteEstate(stack=alpha,
                                             name=gamma.name,
                                             ha=gamma.ha)
    alpha.addRemote(remote)
    alpha.join(uid=remote.uid, cascade=True) # alpha and gamma join

    remote = raet.road.estating.RemoteEstate(stack=beta,
                                             name=gamma.name,
                                             ha=gamma.ha)
    beta.addRemote(remote)
    beta.join(uid=remote.uid, cascade=True) # beta and gamma join

    stacks = [alpha, beta, gamma]
    serviceStacks(stacks)
    print("Finished Handshakes\n")

    msg =  {'subject': 'Example message alpha to whoever',
            'content': 'Hi',}
    for remote in alpha.remotes.values():
        alpha.transmit(msg, remote.uid)

    msg =  {'subject': 'Example message beta to whoever',
            'content': 'Hello.',}
    for remote in beta.remotes.values():
        beta.transmit(msg, remote.uid)

    msg =  {'subject': 'Example message gamma to whoever',
            'content': 'Good Day',}
    for remote in gamma.remotes.values():
        gamma.transmit(msg, remote.uid)

    serviceStacks(stacks)
    print("Finished Messages\n")

    for stack in stacks:
        print("Stack {0} received:\n".format(stack.name))
        while stack.rxMsgs:
            msg, source = stack.rxMsgs.popleft()
            print("source = '{0}'.\nmsg= {1}\n".format(source, msg))


    for stack in stacks:
        stack.server.close()  # close the UDP socket
        stack.keep.clearAllDir()  # clear persisted data

    print("Finished\n")


if __name__ == "__main__":
    print("********** Looping Example Threeway Road *****************\n")
    threeway()

