# -*- coding: utf-8 -*-
"""
Server behaviors

"""
from __future__ import generator_stop

import sys
import os

# Import Python libs
from collections import deque


# Import ioflo libs
from ioflo.aid.sixing import *
from ioflo.aid import odict
from ioflo.aio import WireLog
from ioflo.base import doify
from ioflo.aid import getConsole


console = getConsole()

"""
Usage pattern

frame server
  do road server open at enter
  do road server service
  do road server close at exit


"""

@doify('RoadServerOpen', ioinits=odict(port=odict(inode="", ival=8080),
                                          keepDirPath="",
                                          temp="",))
def roadServerOpen(self, buffer=False, **kwa):
    """
    Setup and open a rest server

    Ioinit attributes
        temp is Flag if True use temporary directory

    Parameters:
        buffer is boolean If True then create wire log buffer for Valet

    Context: enter

    Example:
        do road server open at enter
    """
    if buffer:
        wlog = WireLog(buffify=True, same=True)
        result = wlog.reopen()
    else:
        wlog = None

    port = int(self.port.value)
    test = True if self.test.value else False  # use to load test environment


    if test:
        priming.setupTest()
    else:
        keepDirPath = self.keepDirPath.value if self.keepDirPath.value else None  # None is default
        keepDirPath = os.path.abspath(os.path.expanduser(keepDirPath))
        dbDirPath = self.dbDirPath.value if self.dbDirPath.value else None  # None is default
        dbDirPath = os.path.abspath(os.path.expanduser(dbDirPath))
        priming.setup(keepDirPath=keepDirPath, dbDirPath=dbDirPath)

    self.dbDirPath.value = dbing.gDbDirPath
    self.keepDirPath.value = keeping.gKeepDirPath

    app = falcon.API()  # falcon.API instances are callable WSGI apps
    ending.loadEnds(app, store=self.store)

    self.valet.value = Valet(port=port,
                             bufsize=131072,
                             wlog=wlog,
                             store=self.store,
                             app=app,
                             )

    result = self.valet.value.servant.reopen()
    if not result:
        console.terse("Error opening server '{0}' at '{1}'\n".format(
                            self.valet.name,
                            self.valet.value.servant.eha))
        return


    console.concise("Opened server '{0}' at '{1}'\n".format(
                            self.valet.name,
                            self.valet.value.servant.eha,))

@doify('BluepeaServerService',ioinits=odict(valet=""))
def bluepeaServerService(self, **kwa):
    """
    Service server given by valet

    Ioinit attributes:
        valet is a Valet instance

    Context: recur

    Example:
        do bluepea server service
    """
    if self.valet.value:
        self.valet.value.serviceAll()


@doify('BluepeaServerClose', ioinits=odict(valet="",))
def bluepeaServerClose(self, **kwa):
    """
    Close server in valet

    Ioinit attributes:
        valet is a Valet instance

    Context: exit

    Example:
        do bluepea server close at exit
    """
    if self.valet.value:
        self.valet.value.servant.close()

        console.concise("Closed server '{0}' at '{1}'\n".format(
                            self.valet.name,
                            self.valet.value.servant.eha))





