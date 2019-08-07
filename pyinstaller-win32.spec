# -*- mode: python -*-
# =============================================================================
# @file    pyinstaller-win32.spec
# @brief   Spec file for PyInstaller for Windows
# @author  Michael Hucka
# @license Please see the file named LICENSE in the project directory
# @website https://github.com/caltechlibrary/splitit
# =============================================================================

import imp
import os
import platform
import sys

configuration = Analysis([r'splitit\__main__.py'],
                         pathex = ['.'],
                         binaries = [],
                         hookspath = [],
                         runtime_hooks = [],
                         excludes = [],
                         win_no_prefer_redirects = False,
                         win_private_assemblies = False,
                         cipher = None,
                        )

application_pyz    = PYZ(configuration.pure,
                         configuration.zipped_data,
                         cipher = None,
                        )

executable         = EXE(application_pyz,
                         configuration.scripts,
                         configuration.binaries,
                         configuration.zipfiles,
                         configuration.datas,
                         name = 'SplitIt',
                         icon = r'dev\icons\generated-icons\splitit-icon.ico',
                         debug = False,
                         strip = False,
                         upx = True,
                         runtime_tmpdir = None,
                         console = False,
                        )

app             = BUNDLE(executable,
                         name = 'SplitIt.exe',
                         icon = r'dev\icons\generated-icons\splitit-icon.ico',
                         bundle_identifier = None,
                         info_plist = {'NSHighResolutionCapable': 'True'},
                        )
