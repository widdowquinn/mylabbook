# README.md - labbook

This repository contains helper tools for maintaining my electronic institute lab book. This work was prompted by the second major change to timesheet recording, since the system was introduced. It is intended to make generation and analysis of my work and the time recorded in timesheets easier for me - not for the institute.

## Design

### Overview

#### Make blank lab books

The lab book is written as a LaTeX file. The helper script should generate a blank notebook with the current date, using a template file to guide content, if the following command is executed:

```
labbook.py make_blank
```

To specify a particular date, we want to accept an argument:

```
labbook.py make_blank -d 2017-07-01
labbook.py make_blank --date 2017-07-01
```

The template file will be in `YAML` format (see below) and will be searched for in (in order):

```
./labbook.yaml
~/labbook.yaml
```

or should be passed with the `-y` or `--yaml` argument, e.g.

```
labbook.py make_blank -y tuftenotebook.yaml
```

#### Future extensions

A long-term goal is to provide useful functions (such as searching for keywords) as additional commands to the `labbook.py` program, e.g.

```
labbook.py search <directory>
```

would check the dated lab book source files for keywords, and report back the appropriate section content in human-readable form (as an improvement on the current *ad hoc* `grep` solution.

It might be nice to enable conversions, say to Markdown, with something like:

```
labbook.py convert <input LaTeX> -o <output file> -f <format>
```

We may also be able to have the script manage interaction with a GitHub or other repository (perhaps private?)

```
mylabbook.py git --initialise
mylabbook.py git --commit
```

with the remote repo being defined in the YAML file.

#### Definition of `\section{}`s

We define the content of the lab book in the template file to conform to institute time-sheets - recording time against the current designations of project numbers and titles. These are represented as `\section{}`s in the resulting lab book.

#### Continuity

The format of the lab-book is intended to continue the existing form, based on the Tufte notebook style. To enable this, we allow for definition of a `preflight` set of headers in the template file. For my notebook, this will define the customisations such as margin figures, and fancy verbatim output.

#### Extracting timesheet data

We aim to extract times for a single sheet in tabular form, for easy transfer (by hand) into the institute's eBis system, e.g.:

```
labbook.py timesheet <file>
```

But we would also want to be able to specify a single directory, and report a summary for all lab book files beneath that directory e.g.

```
labbook.py timesheet <directory>
```

or a list of files:

```
labbook.py timesheet <file1> <file2> <file3> <...>
```

#### Naming convention

For the purposes of parsing out directory contents, etc., we will assume that all lab book source files have the form:

```
YYYY-MM-DD.tex
```

with the appropriate date specified in [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601)

### `YAML` congifuration

The `YAML` template will have the following top-level keys:

- `preflight`: path to the preflight LaTeX source (headers/packages etc) for direct inclusion in the lab book document.
- `author`: name of the lab book author
- `project`: sequence of project information

Each `project` will have the following top-level information