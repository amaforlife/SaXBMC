#!/usr/bin/python
# -*- coding: utf-8 -*-
# *
# *  Copyright (C) 2012-2013 Garrett Brown
# *  Copyright (C) 2010      j48antialias
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# *  Based on code by j48antialias:
# *  https://anarchintosh-projects.googlecode.com/files/addons_xml_generator.py
# *  Modified (Globals, Zip-Part) by b-jesch

""" addons.xml generator """

import os
import sys
import zipfile
import shutil
from xml.dom import minidom

MY_ADDONS = ['repository.saxbmc', 'script.loungeripper', 'service.fritzbox.callmonitor',
             'service.sleepy.watchdog', 'service.tvh.manager', 'service.lgtv.remote', 'service.kn.switchtimer',
             'plugin.program.tvhighlights', 'plugin.service.gto', 'plugin.program.fritzact', 'plugin.video.ipcams']
EXCLUDES = ['.git', '.idea', '.gitattributes']
BASEDIR = '../addons'
WORKINGDIR = os.getcwd()
ZIPDIR = 'zip'
ZIPEXT = '.zip'

# Compatibility with 3.0, 3.1 and 3.2 not supporting u"" literals
if sys.version < '3':
    import codecs

    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x


class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
        Additional creates versioned zipfiles in a zipfolder from a project
        structure.
    """

    def __init__(self):
        # generate files
        self._create_zipfiles()
        self._generate_addons_file()
        self._generate_md5_file()
        # notify user
        print("Finished creating zipfiles, updating addons.xml and md5 files")


    def _create_zipfiles(self):
        os.chdir(BASEDIR)
        addons = os.listdir('.')

        for addon in addons:
            if addon in MY_ADDONS:
                try:
                    _dir = os.path.join(WORKINGDIR, ZIPDIR, addon)
                    if not os.path.exists(_dir): os.makedirs(_dir)
                    _file = os.path.join(_dir, addon)
                    addon_zip = zipfile.ZipFile(_file, 'w')
                    for addon_root, dirs, files in os.walk(addon):
                        dirs[:] = [d for d in dirs if d not in EXCLUDES]
                        for filename in files:
                            if os.path.basename(filename)[0:1] == '.' or os.path.basename(filename)[-3:] == 'pyo' \
                                    or os.path.basename(filename)[-3:] == 'pyc':
                                continue
                            if os.path.basename(filename) == 'changelog.txt':
                                shutil.copyfile(os.path.join(addon_root, filename), os.path.join(_dir, 'changelog.txt'))
                            if os.path.basename(filename) == 'addon.xml':
                                # parse this
                                _xmldoc = minidom.parse(os.path.join(addon_root, filename))
                                _vers = _xmldoc.getElementsByTagName('addon')
                                for _attr in  _vers: _v = _attr.getAttribute('version')
                                print _file, _v

                            addon_zip.write(os.path.join(addon_root, filename), compress_type=zipfile.ZIP_DEFLATED)
                    addon_zip.close()
                    _final = _file + '-' + _v + ZIPEXT
                    if os.path.exists(_final): os.remove(_final)
                    os.rename(_file, _final)

                except Exception as e:
                    # oops
                    print("An error occurred while creating %s file!\n%s" % (_file, e))

    def _generate_addons_file(self):
        os.chdir(BASEDIR)
        addons = os.listdir('.')
        # final addons text
        addons_xml = u("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n")
        # loop thru and add each addons addon.xml file
        for addon in addons:
            if addon in MY_ADDONS:
                try:
                    # skip any file or .svn folder or .git folder
                    if ( not os.path.isdir(addon) or addon == ".svn" or addon == ".git" ): continue
                    _path = os.path.join(addon, "addon.xml")
                    xml_lines = open(_path, "r").read().splitlines()

                    addon_xml = ""
                    for line in xml_lines:
                        # skip encoding format line
                        if (line.find("<?xml") >= 0): continue
                        # add line
                        if sys.version < '3':
                            addon_xml += '\t' + unicode(line.rstrip() + "\n", "UTF-8")
                        else:
                            addon_xml += '\t' + line.rstrip() + "\n"
                    # we succeeded so add to our final addons.xml text
                    addons_xml += addon_xml.rstrip() + "\n\n"
                except Exception, e:
                    # missing or poorly formatted addon.xml
                    print("Excluding %s due reason: %s" % ( _path, e ))

        addons_xml = addons_xml.strip() + u("\n</addons>\n")
        self._save_file(addons_xml.encode("UTF-8"), file="addons.xml")

    def _generate_md5_file(self):
        # create a new md5 hash
        os.chdir(WORKINGDIR)
        try:
            import md5
            m = md5.new(open("addons.xml", "r").read()).hexdigest()
        except ImportError:
            import hashlib
            m = hashlib.md5(open("addons.xml", "r").read().encode("UTF-8")).hexdigest()

        # save file
        try:
            self._save_file(m.encode("UTF-8"), file="addons.xml.md5")
        except Exception as e:
            # oops
            print("An error occurred creating addons.xml.md5 file!\n%s" % e)

    def _save_file(self, data, file):
        try:
            # write data to the file (use b for Python 3)
            open(os.path.join(WORKINGDIR, file), "wb").write(data)
        except Exception as e:
            # oops
            print("An error occurred saving %s file!\n%s" % (file, e))


if (__name__ == "__main__"):
    # start
    Generator()
