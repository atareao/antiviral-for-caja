#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#       antiviral-caja-extension.py
#
#       Copyright 2010 Lorenzo Carbonell <atareao@zorita>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import gi
import sys
try:
    gi.require_version('Gtk', '3.0')
    # gi.require_version('Caja', '3.0')
    sys.path.insert(1, '/opt/extras.ubuntu.com/antiviral/share/antiviral')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import Caja as FileBrowser
from gi.repository import GObject
import os
import urllib
import locale
from antiviral import Antiviral

try:
    current_locale, encoding = locale.getdefaultlocale()
    language = gettext.translation(
        'antiviral-caja-extension',
        '/usr/share/locale-langpack',
        [current_locale])
    language.install()
    print(language)
    if sys.version_info[0] == 3:
        _ = language.gettext
    else:
        _ = language.ugettext
except Exception as e:
    print(e)
    _ = str


def get_files(files_in):
    files = []
    for file_in in files_in:
        print(file_in)
        file_in = urllib.unquote(file_in.get_uri()[7:])
        print(file_in)
        if os.path.isdir(file_in):
            files.append(file_in)
    return files

########################################################################

"""
Antiviral menu
"""


class AntiviralMenuProvider(GObject.GObject, FileBrowser.MenuProvider):
    """Implements the 'Replace in Filenames' extension to the FileBrowser
    right-click menu"""

    def __init__(self):
        """FileBrowser crashes if a plugin doesn't implement the
         __init__ method"""
        pass

    def get_file_items(self, window, sel_items):
        """Adds the 'Replace in Filenames' menu item to the FileBrowser
        right-click menu,
           connects its 'activate' signal to the 'run' method passing the
            selected Directory/File"""
        sel_items = get_files(sel_items)
        if not len(sel_items) > 0:
            return
        item = FileBrowser.MenuItem(
            name='AntiviralMenuProvider::Gtk-antiviral-tools',
            label=_('Scan folder'),
            tip=_('Scan this folder'),
            icon='Gtk-find-and-replace')
        item.connect('activate', self.addfolders, sel_items)
        return item,

    def addfolders(self, menu, selected):
        GObject.threads_init()
        Antiviral(from_filebrowser=True, folders=selected)


if __name__ == '__main__':
    GObject.threads_init()
    av = Antiviral()
    Gtk.main()
