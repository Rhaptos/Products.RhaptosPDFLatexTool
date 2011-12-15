"""
RhaptosPDFLatexTool

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU General Public
License Version 2 (GPL).  See LICENSE.txt for details.
"""

import os
import re
import commands
import zLOG
import AccessControl
import tempfile
import shutil
import subprocess
from OFS.SimpleItem import SimpleItem
from OFS.Image import getImageInfo
from Globals import InitializeClass, package_home
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import View, ManagePortal
from Products.CNXMLDocument import XMLService

from interfaces.portal_pdflatex import portal_pdflatex as IPDFLatexTool
from cStringIO import StringIO

from datetime import datetime   # for logging only

class PDFLatexError(Exception):
    pass

class PDFLatexTool(UniqueObject, SimpleItem):

    __implements__ = (IPDFLatexTool)

    id = 'portal_pdflatex'
    meta_type = 'PDFLatex Tool'
    security = AccessControl.ClassSecurityInfo()

    manage_options=(( {'label':'Overview', 'action':'manage_overview'},
                      )
                    + SimpleItem.manage_options
                    )

    ##   ZMI methods
    security.declareProtected(ManagePortal, 'manage_overview')
    manage_overview = PageTemplateFile('zpt/explainPDFLatexTool', globals() )

    def convertObjectToPDF(self, object, style, **params):
        """
        Convert the given object to a PDF file, possible using its subjects as necessary
        """
        fs_tool = getToolByName(self, 'portal_fsimport')

        tempdir = tempfile.mkdtemp()
        fs_tool.exportToFS(tempdir, object)

        export = object.module_export_cnxml()
        if type(export) is unicode:
            export = export.encode('utf-8')
        export_file = open(os.path.join(tempdir, object.getId(), 'export.cnxml'), 'wb')
        export_file.write(export)
        export_file.close()
        
        zLOG.LOG('RhaptosPDFLatexTool',0, "module printing convertObjectToPDF")
        pdf = self.convertFSDirToPDF(os.path.join(tempdir, object.getId()), 'export.cnxml', style, **params)
        shutil.rmtree(tempdir)
        return pdf


    def convertFSDirToPDF(self, path, filename, style = '', **params):
        """
        Produce a PDF from a directory on the filesystem
        """
        # canonical name for module_export_template file
        os.rename(os.path.join(path, filename), os.path.join(path, 'module.mxt'))

        ## this might want to be refactored with Collection.triggerPrint at some point

        # look up makefile params on print tool
        # we don't visit a remote server, so this is not quite correct: we assume a local AsyncPrint for config
        # if not available, use Makefile-encoded values
        printtool = getToolByName(self,'rhaptos_print')
        portal = self.portal_url.getPortalObject()
        
        host = printtool.getHost()
        if host.startswith('http://'):
            host = host[7:]

        project_name = portal.Title()
        project_short_name = project_name
        if project_name == 'Connexions':
              project_name = 'The Connexions Project'

        env = os.environ
        env['HOST'] = host
        env['PROJECT_NAME'] = project_name
        env['PROJECT_SHORT_NAME'] = project_short_name
        env['EPUB_DIR'] = printtool.getEpubDir()
        env['PRINT_STYLE'] = style

        script_location = 'SCRIPTSDIR' in env and env['SCRIPTSDIR'] or '.'

        # Should be setup inside zope.conf on Zope client
        if not env.has_key('PRINT_DIR'):
            # BBB
            makefile = printtool.getMakefile()
            makefiledir = os.path.dirname(makefile)
            env['PRINT_DIR'] = makefiledir
        else:
            makefiledir = env['PRINT_DIR']
        
        makefile = "%s/module_print.mak" % makefiledir

        # copy makefile into tempdir
        shutil.copy(makefile, path)

        # call makefile
        f = open(os.path.join(path, 'make.log'), 'w', 0)
        now = datetime.now()
        zLOG.LOG('RhaptosPDFLatexTool',0, "module printing starts in tempdir %s at %s" % (path, now) )
        f.write(now.isoformat()+"\n")
        subprocess.call(['sh', '%s/module2pdf.sh' % script_location, 'module.pdf'], cwd=path, env=env,
                        stdout=f, stderr=subprocess.STDOUT)
        f.write(now.isoformat()+"\n")
        f.close()

        # evaluate result
        foundPDF = True
        try:
            # read the PDF (if it doesn't exist, fail)
            f = open(os.path.join(path, 'module.pdf'))
            pdf = f.read()
            f.close()
        except IOError:
            foundPDF = False
            #log("-----> could not print %s; pdf probably missing" % self.collectionId)
            raise PDFLatexError, "No output file"

        # check for good PDF here. if not, do we set some property on callback object?
        # all our bad PDFs seem to have the problem of not ending on %%EOF so we check that
        # it's a nice light-weight check
        if not (foundPDF and ( pdf.endswith("%%EOF\n") or pdf.endswith("%%EOF\n\n") ) ):
            raise PDFLatexError, "Bad output file"

        zLOG.LOG('RhaptosPDFLatexTool',0, "module printing finished successfully in tempdir %s at %s in %s" % (path, now, datetime.now()-now) )
        return pdf

    ## note: there used to be here a Python version of what the makefile now does; check the history

InitializeClass(PDFLatexTool)
