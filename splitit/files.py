'''
files.py: utilities for working with files.

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
import io
import os
from   os import path
import re
import shutil
import string
import sys
import subprocess
import warnings
import webbrowser

import splitit
from splitit.debug import log


# Constants.
# .............................................................................

_SPLITIT_REG_PATH = r'Software\Caltech Library\Splitit\Settings'


# Main functions.
# .............................................................................

def readable(dest):
    '''Returns True if the given 'dest' is accessible and readable.'''
    return os.access(dest, os.F_OK | os.R_OK)


def writable(dest):
    '''Returns True if the destination is writable.'''
    return os.access(dest, os.F_OK | os.W_OK)


def module_path():
    '''Returns the absolute path to our module installation directory.'''
    # The path returned by module.__path__ is to the directory containing
    # the __init__.py file.
    return path.abspath(splitit.__path__[0])


def splitit_path():
    '''Returns the path to where Splitit is installed.'''
    # The path returned by module.__path__ is to the directory containing
    # the __init__.py file.  What we want here is the path to the installation
    # of the Splitit binary.
    if sys.platform.startswith('win'):
        from winreg import OpenKey, CloseKey, QueryValueEx, HKEY_LOCAL_MACHINE, KEY_READ
        try:
            if __debug__: log('Reading Windows registry entry')
            key = OpenKey(HKEY_LOCAL_MACHINE, _SPLITIT_REG_PATH)
            value, regtype = QueryValueEx(key, 'Path')
            CloseKey(key)
            if __debug__: log('Path to windows installation: {}'.format(value))
            return value
        except WindowsError:
            # Kind of a problem. Punt and return a default value.
            return path.abspath('C:\Program Files\Splitit')
    else:
        return path.abspath(path.join(module_path(), '..'))


def desktop_path():
    '''Returns the path to the user's desktop directory.'''
    if sys.platform.startswith('win'):
        return path.join(path.join(os.environ['USERPROFILE']), 'Desktop')
    else:
        return path.join(path.join(path.expanduser('~')), 'Desktop')


def files_in_directory(dir, extensions = None):
    if not path.isdir(dir):
        return []
    if not readable(dir):
        return []
    files = []
    for item in os.listdir(dir):
        full_path = path.join(dir, item)
        if path.isfile(full_path) and readable(full_path):
            if extensions and filename_extension(item) in extensions:
                files.append(full_path)
    return sorted(files)


def filename_basename(file):
    parts = file.rpartition('.')
    if len(parts) > 1:
        return ''.join(parts[:-1]).rstrip('.')
    else:
        return file


def filename_extension(file):
    parts = file.rpartition('.')
    if len(parts) > 1:
        return parts[-1].lower()
    else:
        return ''


def alt_extension(filepath, ext):
    '''Returns the 'filepath' with the extension replaced by 'ext'.  The
    extension given in 'ext' should NOT have a leading period: that is, it
    should be "foo", not ".foo".'''
    return path.splitext(filepath)[0] + '.' + ext


def filter_by_extensions(item_list, endings):
    if not item_list:
        return []
    if not endings:
        return item_list
    results = item_list
    for ending in endings:
        results = list(filter(lambda name: ending not in name.lower(), results))
    return results


def is_url(string):
    '''Return True if the 'string' looks like a URL, False otherwise.'''
    return re.match(r'^[a-zA-Z]+:/', string)


# The following originally came from an answer posted by user "domenukk"
# to Stack Overflow: https://stackoverflow.com/a/54564813/743730

def is_csv(infile):
    '''Return True if the given file is probably a CSV file.'''
    try:
        with open(infile, newline='') as csvfile:
            start = csvfile.read(4096)
            # isprintable does not allow newlines, printable does not allow umlauts...
            if not all([c in string.printable or c.isprintable() for c in start]):
                return False
            dialect = csv.Sniffer().sniff(start)
            return True
    except csv.Error:
        # Could not get a csv dialect -> probably not a csv.
        return False


def relative(file):
    '''Returns a path that is relative to the current directory.  If the
    relative path would require more than one parent step (i.e., ../../*
    instead of ../*) then it will return an absolute path instead.  If the
    argument is actuall a file path, it will return it unchanged.'''
    if is_url(file):
        return file
    candidate = path.relpath(file, os.getcwd())
    if not candidate.startswith('../..'):
        return candidate
    else:
        return path.realpath(candidate)


def make_dir(dir_path):
    '''Creates directory 'dir_path' (including intermediate directories).'''
    if path.isdir(dir_path):
        if __debug__: log('Reusing existing directory {}', dir_path)
        return
    else:
        if __debug__: log('Creating directory {}', dir_path)
        # If this gets an exception, let it bubble up to caller.
        os.makedirs(dir_path)


def rename_existing(file):
    '''Renames 'file' to 'file.bak'.'''

    def rename(f):
        backup = f + '.bak'
        # If we fail, we just give up instead of throwing an exception.
        try:
            os.rename(f, backup)
            if __debug__: log('renamed {} to {}', file, backup)
        except:
            try:
                delete_existing(backup)
                os.rename(f, backup)
            except:
                if __debug__: log('failed to delete {}', backup)
                if __debug__: log('failed to rename {} to {}', file, backup)

    if path.exists(file):
        rename(file)
        return
    full_path = path.join(os.getcwd(), file)
    if path.exists(full_path):
        rename(full_path)
        return


def delete_existing(file):
    '''Delete the given file.'''
    # Check if it's actually a directory.
    if path.isdir(file):
        if __debug__: log('doing rmtree on directory {}', file)
        try:
            shutil.rmtree(file)
        except:
            if __debug__: log('unable to rmtree {}; will try renaming', file)
            try:
                rename_existing(file)
            except:
                if __debug__: log('unable to rmtree or rename {}', file)
    else:
        if __debug__: log('doing os.remove on file {}', file)
        os.remove(file)


def copy_file(src, dst):
    '''Copy a file from "src" to "dst".'''
    if __debug__: log('copying file {} to {}', src, dst)
    shutil.copy2(src, dst, follow_symlinks = True)


def file_in_use(file):
    if not path.exists(file):
        return False
    if sys.platform.startswith('win'):
        # This is a hack, and it really only works for this purpose on Windows.
        try:
            os.rename(file, file)
            return False
        except:
            return True
    return False


def open_file(file):
    '''Open document with default application in Python.'''
    # Code originally from https://stackoverflow.com/a/435669/743730
    if __debug__: log('opening file {}', file)
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', file))
    elif os.name == 'nt':
        os.startfile(file)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', file))


def open_url(url):
    '''Open the given 'url' in a web browser using the current platform's
    default approach.'''
    if __debug__: log('opening url {}', url)
    webbrowser.open(url)
