#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""parsers.py

Provides functions to generate subcommand parsers for the labbook.py script

- make_blank:        interact with config files

(c) The James Hutton Institute 2017
Author: Leighton Pritchard

Contact: leighton.pritchard@hutton.ac.uk
Leighton Pritchard,
Information and Computing Sciences,
James Hutton Institute,
Errol Road,
Invergowrie,
Dundee,
DD6 9LH,
Scotland,
UK

The MIT License

Copyright (c) 2017 The James Hutton Institute

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import sys

from argparse import ArgumentParser

from . import subcommands


# Build common parser for all subcommands
def build_common_parser():
    """ Returns the common argument parser for the script.

    This parser implements options that are common to all subcommands
    """
    parser_common = ArgumentParser(add_help=False)
    parser_common.add_argument('-l', '--logfile', dest='logfile',
                               action='store', default=None,
                               help='path to logfile')
    parser_common.add_argument('-v', '--verbose', dest='verbose',
                               action='store_true', default=False,
                               help='report progress to STDOUT')
    return parser_common


# Build subcommand parsers
# Each subcommand gets its own parser, and the entry point to the subcommand
# is defined with parser.set_defaults().
# See https://docs.python.org/3.6/library/argparse.html#sub-commands

# Make a blank lab book
def build_parser_make_blank(subparsers, parents=None):
    """Add parser for `make_blank` subcommand to the subparsers

    This parser implements options for making blank lab books.
    """
    parser = subparsers.add_parser('make_blank', parents=parents)
    parser.add_argument('-d', '--date', dest='date',
                        action='store', default=None,
                        help='date for lab book (ISO 8061, YYYY-MM-DD)')
    parser.add_argument('-y', '--yaml', dest='yamlfile',
                        action='store', default=None,
                        help='path to YAML config file')
    parser.add_argument('-o', '--outdir', dest='outdirname',
                        action='store', default=None,
                        help='path to output directory for lab book blank')
    parser.set_defaults(func=subcommands.subcmd_make_blank)
    


# Process command-line
def parse_cmdline():
    """Parse command-line arguments for script.

    The script offers a single main parser, with subcommands for the actions:

    make_blank - create a new blank lab book
    """
    # Main parent parser
    parser_main = ArgumentParser(prog='labbook.py')
    subparsers = parser_main.add_subparsers(title='subcommands',
                                            description='valid subcommands',
                                            help='additional help')

    # Common parser to be included with all the subcommand parsers
    parser_common = build_common_parser()

    # Add subcommand parsers to the main parser's subparsers
    build_parser_make_blank(subparsers, parents=[parser_common])
    print(subparsers)

    # Catch calling the main script with no arguments (which would otherwise
    # not give a help message)
    if len(sys.argv)==1:
        parser_main.print_help()
        sys.exit(1)
    
    # Parse arguments
    return parser_main.parse_args()
