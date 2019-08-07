'''
exceptions.py: exceptions defined by Split It!

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2019 by the California Institute of Technology.  This code is
open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

class UserCancelled(Exception):
    '''The user elected to cancel/quit the program.'''
    pass

class NoContent(Exception):
    '''No content found at the given location.'''
    pass

class CorruptedContent(Exception):
    '''Content corruption has been detected.'''
    pass

class InternalError(Exception):
    '''Unrecoverable problem involving eprints2bags itself.'''
    pass
