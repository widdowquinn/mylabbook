#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""subcommands.py

Provides subcommand functions for the pdp.py script

- make_blank:        generate new blank lab book

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

import os

from datetime import date

import iso8601
import yaml

titlestr = """\n\n
%% SET TITLE HERE
%%%%%%%%%%%%%%%%%
% Can't use mathematics markup ($whatever$) here.
\\title[{:%d %B %Y}]{{Laboratory Notebook: {:%d %B %Y}}}
\\author{{{}}}
\\date{{{:%d/%m/%y}}}

%% NOTES
%%%%%%%%
%% Quite frequently, a marginfigure will fall off the bottom of the
%% current page, so use:
%% \\begin{{marginfigure}}[-80\baselineskip]
%%   \\includegraphics{{DVB_MIMB_email1}}
%%   \\caption{{Dave B's suggestions for the MIMB paper, part 1}}
%% \\end{{marginfigure}}
"""

docstart="""\n\n
%%%%%%%%%%%%%%%%%%%%%%%
%% DOCUMENT BEGINS HERE
%%%%%%%%%%%%%%%%%%%%%%%
\\begin{document}

%% TITLE
%%%%%%%%%
\\maketitle

%% TABLE OF CONTENTS
%%%%%%%%%%%%%%%%%%%%
\\tableofcontents

%% ABSTRACT
%%%%%%%%%%%
% We can include a short amount of text to describe unusual events or comments, 
% with the \\abstract{} environment.
\\begin{abstract}
\\noindent 
\\begin{itemize}
\\item
\\end{itemize}
\\end{abstract}

%% DONELIST
%%%%%%%%%%%%
% A psychological trick to make me feel better about myself
\\begin{abstract}
\\noindent 
\\begin{itemize}
\\item 
\\end{itemize}
\\end{abstract}
"""

projecthead = """\n\n
%%%%%%%%%%%%
%% PROJECTS
%%%%%%%%%%%%
"""


docend = """\n\n
%%%%%%%%%%%%%%%%%%%%%%
%% DOCUMENT ENDS HERE
%%%%%%%%%%%%%%%%%%%%%%
\\newpage
\\end{document}
"""



def subcmd_make_blank(args, logger):
    """Run `make_blank` subcommand operations.
    """
    # Get the appropriate date. If args.date is provided, use this. Otherwise,
    # use today's date.
    if args.date is not None:
        logger.info("Using passed date: %s", args.date)
        docdate = iso8601.parse_date(args.date).date()
    else:
        logger.info("Using today's date: %s", date.today())
        docdate = date.today()
    lbdate = docdate.isoformat()

    # Identify the YAML template file. Use the passed file first, then check
    # './.labbook.yaml' and finally '~/.labbook.yaml'
    if args.yamlfile is not None:
        yamlpath = args.yamlfile
    elif os.path.isfile('./.labbook.yaml'):
        yamlpath = './.labbook.yaml'
    elif os.path.isfile(os.path.join(os.path.expanduser('~'),
                                     '.labbook.yaml')):
        yamlpath = os.path.join(os.path.expanduser('~'), '.labbook.yaml')
    else:
        logger.error("No template file found (exiting)")
        raise SystemExit(1)
    logger.info("Using YAML template from %s", yamlpath)

    # Load data from the YAML template file
    logger.info("Loading data from %s", yamlpath)
    with open(yamlpath) as yfh:
        yamldata = yaml.load(yfh.read())
    try:
        if not os.path.isfile(yamldata['preflight']):
            logger.error("Preflight LaTeX file %s not found (exiting)",
                         yamldata['preflight'])
            raise SystemExit(1)
    except KeyError:
        logger.error("YAML template does not contain preflight LaTeX (exiting)")
        raise SystemExit(1)
    
    # Generate path to output blank file, creating the intermediate directories
    # if needed.
    outfname = lbdate + '.tex'
    if args.outdirname is None:
        outpath = outfname
    else:
        if not os.path.isdir(args.outdirname):
            logger.info("Creating output directory %s", args.outdirname)
            os.makedirs(args.outdirname, exist_ok=True)
        outpath = os.path.join(args.outdirname, outfname)
    logger.info("Attempting to write lab book blank to %s", outpath)

    # Write the blank notebook
    logger.info("Writing blank notebook to %s", outpath)
    with open(outpath, 'w') as ofh:
        # Write preflight
        logger.info("Writing preflight")
        with open(yamldata['preflight'], 'r') as pfh:
            ofh.write(pfh.read())
        # Write title
        logger.info("Writing title")
        ofh.write(titlestr.format(docdate, docdate, yamldata['author'],
                                  docdate))
        # Start document
        logger.info("Starting document")
        ofh.write(docstart)
        # Loop over projects in YAML file, and write template for each
        logger.info("Writing projects")
        ofh.write(projecthead)
        for project in yamldata['projects']:
            logger.info("Writing headers for project %s: %s, %s",
                        project['number'], project['description'],
                        project['name'])
            ofh.write(build_project_header(project))
        # End document
        logger.info("Ending document")
        ofh.write(docend)
            
    return 0


# Build a header for a passed project
def build_project_header(project):
    """Returns LaTeX header for passed project info (from YAML)

    The header is commented out, for the user to uncomment when preparing
    their lab book.
    """
    # Construct main header components
    main = ["\n\n%% {1}, {2}",
              "%{3}",
              "%\\section{{{0} {1}, {2}: }}"]
    rule = '%' * (len(project['name'] + project['description']) + 4)
    main = '\n\n' + '\n'.join(main).format(project['number'],
                                           project['description'],
                                           project['name'],
                                           rule,
                                           project['activity'])
    outstr = [main]

    # Add subsection header components
    if 'subsections' in project:
        for subsect in project['subsections']:
            rule = '=' * (len(subsect['name']) + 2)
            outstr.append("\n% {0}".format(subsect['name']))
            outstr.append("%{0}".format(rule))
            outstr.append("%\\subsection{{{0}: }}".format(subsect['name']))

    # Build the header string
    return  '\n'.join(outstr)
