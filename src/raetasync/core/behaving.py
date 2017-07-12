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
et
# Import ioflo libs
from ioflo.aid.sixing import *
from ioflo.aid import odict
from ioflo.aio import WireLog
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
                                       name=odict(inode="", ival='server'),
                                       host=odict(inode="", ival='0.0.0.0'),
                                       port=odict(inode="", ival=7531),))
def roadStackOpen(self, **kwa):
    """
    Setup and open a road stack

    Ioinit attributes
        stack holds RoadStack instance created here
        name is name of server
        host is server host string
        port is server port

    Context: enter

    Example:
        do road stack open at enter
    """
    name = self.name.value
    host = self.host.value
    port = int(self.port.value)  # ensure int

    stack = raet.road.stacking.RoadStack(name=name,
                                          ha=(host, port),
                                          main=True,
                                          auto=AutoMode.always.value)

    self.stack.value = stack

    console.concise("Opened road stack '{0}' at '{1}'\n".format(
                            stack.name,
                            stack.eha,))

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
    if self.server.value:
        self.server.value.serviceAll()


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
        self.stack.server.close()  # close the UDP socket
        self.stack.keep.clearAllDir()

        console.concise("Closed server '{0}' at '{1}'\n".format(
                            self.valet.name,
                            self.valet.value.servant.eha))





