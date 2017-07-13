# -*- coding: utf-8 -*-
"""
Server behaviors

"""
from __future__ import generator_stop

import sys
import os

# Import Python libs
from collections import deque

import raet

# Import ioflo libs
from ioflo.aid.sixing import *
from ioflo.aid import odict
from ioflo.base import doify
from ioflo.aid import getConsole

console = getConsole()

"""
Usage pattern

frame stacker
  do road stack open at enter
  do road stack service
  do road stack close at exit


"""

@doify('RoadStackOpen', ioinits=odict(stack="",
                                      conf=odict(inode="",
                                                 ival=odict([
                                                             ("name", "server"),
                                                             ("host", "0.0.0.0"),
                                                             ("port", 7531)
                                                           ])
                                                 ) ))
def roadStackOpen(self, **kwa):
    """
    Setup and open a road stack

    Ioinit attributes
        stack holds RoadStack instance created here
        conf is configuration data of stack with fields name, host, port

    Context: enter

    Example:
        do road stack open at enter
    """
    self.stack.value = raet.road.stacking.RoadStack(store=self.store,
                                                    name=self.conf.data.name,
                                                    ha=(self.conf.data.host,
                                                        int(self.conf.data.port)),
                                                    main=True,
                                                    mutable=True,
                                                    auto=raet.raeting.AutoMode.always.value)

    console.concise("Opened road stack '{0}' at '{1}'\n".format(
                            self.stack.value.name,
                            self.stack.value.ha,))

@doify('RoadStackService',ioinits=odict(stack=""))
def roadStackService(self, **kwa):
    """
    Service stack given by stack

    Ioinit attributes:
        stack is a RoadStack instance

    Context: recur

    Example:
        do road stack service
    """
    if self.stack.value:
        self.stack.value.serviceAll()


@doify('RoadStackClose', ioinits=odict(stack="",))
def roadStackClose(self, **kwa):
    """
    Close server in stack

    Ioinit attributes:
        stack is a RoadStack instance

    Context: exit

    Example:
        do road stack close at exit
    """
    if self.stack.value:
        self.stack.value.server.close()  # close the UDP socket
        self.stack.value.keep.clearAllDir()

        console.concise("Closed raod stack '{0}' at '{1}'\n".format(
                            self.stack.value.name,
                            self.stack.value.ha))



@doify('RoadStackRemoteAddJoin',ioinits=odict(stack="",
                                              conf=odict(ival=odict([
                                                                    ("name", "remote"),
                                                                    ("host", "localhost"),
                                                                    ("port", 7532)
                                                                    ])
                                              ) ))
def roadStackRemoteAddJoin(self, **kwa):
    """
    Add remote to stack

    Ioinit attributes:
        stack is a RoadStack instance
        conf is configuration data of remote with fields name, host, port

    Context: enter

    Example:
        do road stack remote add at enter
    """
    if self.stack.value:
        stack = self.stack.value
        name = self.conf.data.name
        if name in stack.nameRemotes:
            remote = stack.nameRemotes[name]
        else:
            remote = raet.road.estating.RemoteEstate(stack=stack,
                                                 name=self.conf.data.name,
                                                 ha=(self.conf.data.host,
                                                     int(self.conf.data.port)))
            stack.addRemote(remote)
        stack.join(uid=remote.uid, cascade=True)


@doify('RoadStackMessageAll',ioinits=odict(stack="",
                                              remote=odict(ival="remote"),
                                              message=odict(ival=odict([
                                                             ("subject", "Re"),
                                                             ("content", "Hello World"),
                                                         ])
                                                         ) ))
def roadStackMessageAll(self, **kwa):
    """
    Send message to all remotes

    Ioinit attributes:
        stack is a RoadStack instance
        message is message to send with fields subject and content

    Context: enter

    Example:
        do road stack message all at enter
    """
    if self.stack.value:
        stack = self.stack.value
        msg = odict([("subject", self.message.data.subject),
                     ("content", self.message.data.content)])
        for remote in stack.remotes.values():
            stack.transmit(msg, remote.uid)


@doify('RoadStackPrint',ioinits=odict(stack="") )
def roadStackPrint(self, **kwa):
    """
    Print messages to console

    Ioinit attributes:
        stack is a RoadStack instance

    Context: enter

    Example:
        do road stack show at enter
    """
    if self.stack.value:
        stack = self.stack.value
        print("Stack {0} received:\n".format(stack.name))
        while stack.rxMsgs:
            msg, source = stack.rxMsgs.popleft()
            print("source = '{0}'.\nmsg= {1}\n".format(source, msg))


