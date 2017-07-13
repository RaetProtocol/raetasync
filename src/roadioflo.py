#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Runs ioflo plan from command line shell

Usage:

$ cd /data/code/public/raetasync/src/
$ python3 roadioflo.py -v concise -r -p 0.0625 -n raetflo -f /Data/Code/public/raetasync/src/raetflo/main.flo -b raetflo.core

"""
import sys
import ioflo.app.run

def main():
    """ Main entry point for ioserve CLI"""
    from raetflo import __version__
    args = ioflo.app.run.parseArgs(version=__version__)  # inject  version here

    ioflo.app.run.run(  name=args.name,
                        period=float(args.period),
                        real=args.realtime,
                        retro=args.retrograde,
                        filepath=args.filename,
                        behaviors=args.behaviors,
                        mode=args.parsemode,
                        username=args.username,
                        password=args.password,
                        verbose=args.verbose,
                        consolepath=args.console,
                        statistics=args.statistics)

if __name__ == '__main__':
    main()
