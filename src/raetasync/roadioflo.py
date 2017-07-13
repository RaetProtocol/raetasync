#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Runs ioflo plan from command line shell

Usage:

python3 -mroadioflo -v concise -r -p 0.0625 -n roadioflo -f /Data/Code/public/raetasync/src/raetasync/main.flo -b raetasync.core

"""
import sys
import ioflo.app.run

def main():
    """ Main entry point for ioserve CLI"""
    from raetasync import __version__
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
