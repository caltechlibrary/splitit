'''
messages: message-printing utilities for Split It!

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2019 by the California Institute of Technology.  This code is
open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

import sys

try:
    from termcolor import colored
    if sys.platform.startswith('win'):
        import colorama
        colorama.init()
except:
    pass

import splitit
from splitit.exceptions import *


# Exported classes.
# .............................................................................
# The basic principle of writing the classes (like this one) that get used
# elsewhere is that they should take the information they need.  This means,
# for example, that 'use_color' is handed to the CLI version of this object,
# not to the base class class, even though use_color is something that may be
# relevant to more than one of the main classes.  This is a matter of
# separation of concerns and information hiding.

class MessageHandlerBase():
    '''Base class for message-printing classes in Split It!'''

    def __init__(self):
        pass


class MessageHandlerCLI(MessageHandlerBase):
    '''Class for printing console messages and asking the user questions.'''

    def __init__(self, use_color, quiet):
        super().__init__()
        self._colorize = use_color
        self._quiet = quiet


    def use_color(self):
        return self._colorize


    def be_quiet(self):
        return self._quiet


    def info_text(self, text, details = ''):
        '''Prints an informational message.'''
        if not self.be_quiet():
            return color(text, 'info', self._colorize)


    def info(self, text, details = ''):
        '''Prints an informational message.'''
        if not self.be_quiet():
            msg(self.info_text(text, details))


    def warn_text(self, text, details = ''):
        '''Prints a nonfatal, noncritical warning message.'''
        return color('Warning: ' + text, 'warn', self._colorize)


    def warn(self, text, details = ''):
        '''Prints a nonfatal, noncritical warning message.'''
        msg(self.warn_text(text, details))


    def error_text(self, text, details = ''):
        '''Prints a message reporting a critical error.'''
        return color('Error: ' + text, 'error', self._colorize)


    def error(self, text, details = ''):
        '''Prints a message reporting a critical error.'''
        msg(self.error_text(text, details))


    def fatal_text(self, text, details = ''):
        '''Prints a message reporting a fatal error.  This method does not
        exit the program; it leaves that to the caller in case the caller
        needs to perform additional tasks before exiting.
        '''
        return color('FATAL: ' + text, ['error', 'bold'], self._colorize)


    def fatal(self, text, details = ''):
        '''Prints a message reporting a fatal error.  This method does not
        exit the program; it leaves that to the caller in case the caller
        needs to perform additional tasks before exiting.
        '''
        msg(self.fatal_text(text, details))


    def yes_no(self, question):
        '''Asks a yes/no question of the user, on the command line.'''
        return input("{} (y/n) ".format(question)).startswith(('y', 'Y'))


    def msg_text(self, text, flags = None):
        return color(text, flags, self._colorize)


    def msg(self, text, flags = None):
        msg(self.msg_text(text, flags))


# Message utility funcions.
# .............................................................................

def msg(text, flags = None, colorize = True):
    '''Like the standard print(), but flushes the output immediately and
    colorizes the output by default. Flushing immediately is useful when
    piping the output of a script, because Python by default will buffer the
    output in that situation and this makes it very difficult to see what is
    happening in real time.
    '''
    if colorize and 'termcolor' in sys.modules:
        sys.stdout.write(color(text, flags) + '\n')
        sys.stdout.flush()
    else:
        sys.stdout.write(text + '\n')
        sys.stdout.flush()


def color(text, flags = None, colorize = True):
    '''Color-code the 'text' according to 'flags' if 'colorize' is True.
    'flags' can be a single string or a list of strings, as follows.
    Explicit colors (when not using a severity color code):
       'white', 'blue', 'grey', 'cyan', 'magenta'
    Additional color codes reserved for message severities:
       'info'  = informational (green)
       'warn'  = warning (yellow)
       'error' = severe error (red)
    Optional color modifiers:
       'underline', 'bold', 'reverse', 'dark'
    '''
    (prefix, color_name, attributes) = _color_codes(flags)
    if colorize:
        if attributes and color_name:
            return colored(text, color_name, attrs = attributes)
        elif color_name:
            return colored(text, color_name)
        elif attributes:
            return colored(text, attrs = attributes)
        else:
            return text
    elif prefix:
        return prefix + ': ' + str(text)
    else:
        return text


# Internal utilities.
# .............................................................................

def _print_header(text, flags, quiet = False, colorize = True):
    if not quiet:
        msg('')
        msg('{:-^78}'.format(' ' + text + ' '), flags, colorize)
        msg('')


def _color_codes(flags):
    color_name  = ''
    prefix = ''
    if type(flags) is not list:
        flags = [flags]
    if sys.platform.startswith('win'):
        attrib = [] if 'dark' in flags else ['bold']
    else:
        attrib = []
    if 'error' in flags:
        prefix = 'ERROR'
        color_name = 'red'
    if 'warning' in flags or 'warn' in flags:
        prefix = 'WARNING'
        color_name = 'yellow'
    if 'info' in flags:
        color_name = 'green'
    if 'white' in flags:
        color_name = 'white'
    if 'blue' in flags:
        color_name = 'blue'
    if 'grey' in flags or 'gray' in flags:
        color_name = 'grey'
    if 'cyan' in flags:
        color_name = 'cyan'
    if 'magenta' in flags:
        color_name = 'magenta'
    if 'underline' in flags:
        attrib.append('underline')
    if 'bold' in flags:
        attrib.append('bold')
    if 'reverse' in flags:
        attrib.append('reverse')
    if 'dark' in flags:
        attrib.append('dark')
    return (prefix, color_name, attrib)
