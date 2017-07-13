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
                                       tag=odict(inode="", ival='stacker'),
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
    self.stack.value = raet.road.stacking.RoadStack(name=self.tag.value,
                                          ha=(self.host.value, int(self.port.value)),
                                          main=True,
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





