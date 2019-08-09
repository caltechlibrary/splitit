'''Split It!: Reformat spreadsheet of inventory results from Caltech.tind.io

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2019 by the California Institute of Technology.  This code is
open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

import csv
import os
from   os import path
import plac
import sys
from   sys import exit as exit

import splitit
from splitit.debug import set_debug, log
from splitit.exceptions import *
from splitit.files import readable, writable, file_in_use, is_csv
from splitit.files import file_to_open, file_to_save
from splitit.messages import MessageHandlerCLI


# Main program.
# .............................................................................

@plac.annotations(
    no_gui     = ('do not use GUI dialogs to ask for files (default: do)', 'flag',   'G'),
    input_csv  = ('input file to be reformatted',                          'option', 'i'),
    output_csv = ('output file where results should be written',           'option', 'o'),
    no_color   = ('do not color-code terminal output',                     'flag',   'C'),
    quiet      = ('only print important messages while working',           'flag',   'q'),
    version    = ('print version info and exit',                           'flag',   'V'),
    debug      = ('turn on debug tracing & exception catching',            'flag',   '@'),
)

def main(no_gui = False, input_csv = 'I', output_csv = 'O', no_color = False,
         quiet = False, version = False, debug = False):
    '''Split It!

If the options -i and/or -o (or /i and /o on Windows) are not supplied, this
program will use GUI file dialogs to ask the user for the input and/or output
files (respectively) unless the option -G (/G on Windows) is used.

If the -G option (/G on Windows) is supplied to prevent the use of the GUI,
then this program must be invoked with two command-line options and values:
-i and -o (or /i and /o on Windows).  The -i option (/i on Windows) should be
followed by the path to an input file in CSV format that contains the content
to be reformatted; the -o option (/o on Windows) should be followed by the
path to a new, reformatted CSV file that should be written with the output.
Here is an example:

  splitit -i downloaded.csv -o inventory.csv

Additional command-line arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If given the -q option (/q on Windows), this program will not print its usual
informational messages while it is working.  It will only print messages for
warnings or errors.  By default, messages are also color-coded.  If given the
option -C (/C on Windows), this program will not color the text of messages
it prints.  (This latter option is useful when running the program within
subshells inside other environments such as Emacs.)

If given the -V option (/V on Windows), this program will print the version
and other information, and exit without doing anything else.

If given the -@ option (/@ on Windows), this program will print additional
diagnostic output as it runs; in addition, it will start the Python debugger
(pdb) when an exception occurs, instead of simply exiting.

Command-line arguments summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

    # Initial setup -----------------------------------------------------------

    say = MessageHandlerCLI(not no_color, quiet)
    prefix = '/' if sys.platform.startswith('win') else '-'
    hint = '(Hint: use {}h for help.)'.format(prefix)
    use_gui = not no_gui

    # Preprocess arguments and handle early exits -----------------------------

    if debug:
        set_debug(True)
    if version:
        print_version()
        exit()

    if input_csv == 'I' and use_gui:
        input_csv = file_to_open(splitit.__title__ + ': open input CSV file',
                                 wildcard = 'CSV file (*.csv)|*.csv|Any file (*.*)|*.*')
        if input_csv is None:
            exit('Quitting.')
    else:
        exit(say.error_text('Must supply input file using -i. {}'.format(hint)))
    if not readable(input_csv):
        exit(say.error_text('Cannot read file: {}'.format(input_csv)))
    elif not is_csv(input_csv):
        exit(say.error_text('File does not appear to contain CSV: {}'.format(input_csv)))

    if output_csv == 'O' and use_gui:
        output_csv = file_to_save(splitit.__title__ + ': save output file')
        if output_csv is None:
            exit('Quitting.')
    else:
        exit(say.error_text('Must supply output file using -o. {}'.format(hint)))
    if path.exists(output_csv):
        if file_in_use(output_csv):
            exit(say.error_text('File is open by another application: {}'.format(output_csv)))
        elif not writable(output_csv):
            exit(say.error_text('Unable to write to file: {}'.format(output_csv)))
    else:
        dest_dir = path.dirname(output_csv) or os.getcwd()
        if not writable(dest_dir):
            exit(say.error_text('Cannot write to folder: {}'.format(dest_dir)))

    # Do the real work --------------------------------------------------------

    # Example of possible input:
    #
    # 574524,35047011136967,on shelf,,QA7 .A664 1991,
    # 501345,350470002009169; 35047010046266,on shelf; on shelf,,QA7 .A67 1983,

    try:
        say.info('┏━━━━━━━━━━━━━━━━━┓')
        say.info('┃    Split It!    ┃')
        say.info('┗━━━━━━━━━━━━━━━━━┛')

        # Read it, massage it, write it.
        say.info('Reading input from "{}"'.format(input_csv))
        input_rows = []
        with open(input_csv, newline = '', encoding = 'utf8') as csvfile:
            input_rows = list(csv.reader(csvfile))

        # Simple-minded approach to splitting compound results
        output_rows = []
        for row in input_rows:
            if ';' in row[1]:
                new_rows = []
                for index, part in enumerate(row[1].split(';')):
                    new_rows.append([row[0], part.strip()])
                for index, part in enumerate(row[2].split(';')):
                    new_rows[index].append(part.strip())
                for index in range(0, len(new_rows)):
                    new_rows[index].append(row[3].strip())
                    new_rows[index].append(row[4].strip())
                    new_rows[index].append(row[5].strip())
                output_rows += new_rows
            else:
                output_rows.append(row)

        say.info('Writing to "{}"'.format(output_csv))
        with open(output_csv, 'w') as csvfile:
            wr = csv.writer(csvfile)
            wr.writerows(output_rows)
    except (KeyboardInterrupt, UserCancelled) as ex:
        if __debug__: log('received {}', ex.__name__)
        exit(say.info_text('Quitting.'))
    except Exception as ex:
        if debug:
            import traceback
            say.error('{}\n{}'.format(str(ex), traceback.format_exc()))
            import pdb; pdb.set_trace()
        else:
            exit(say.error_text(str(ex)))
    say.info('Done.')


# Helper functions.
# .............................................................................

def print_version():
    print('{} version {}'.format(splitit.__title__, splitit.__version__))
    print('Author: {}'.format(splitit.__author__))
    print('URL: {}'.format(splitit.__url__))
    print('License: {}'.format(splitit.__license__))


# Main entry point.
# .............................................................................

# On windows, we want plac to use slash intead of hyphen for cmd-line options.
if sys.platform.startswith('win'):
    main.prefix_chars = '/'

# The following allows users to invoke this using "python3 -m splitit".
if __name__ == '__main__':
    plac.call(main)
