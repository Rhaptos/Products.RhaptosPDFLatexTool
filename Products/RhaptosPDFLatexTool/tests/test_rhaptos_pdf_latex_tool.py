#------------------------------------------------------------------------------#
#   test_rhaptos_pdf_latex_tool.py                                             #
#                                                                              #
#       Authors:                                                               #
#       Rajiv Bakulesh Shah <raj@enfoldsystems.com>                            #
#                                                                              #
#           Copyright (c) 2009, Enfold Systems, Inc.                           #
#           All rights reserved.                                               #
#                                                                              #
#               This software is licensed under the Terms and Conditions       #
#               contained within the "LICENSE.txt" file that accompanied       #
#               this software.  Any inquiries concerning the scope or          #
#               enforceability of the license should be addressed to:          #
#                                                                              #
#                   Enfold Systems, Inc.                                       #
#                   4617 Montrose Blvd., Suite C215                            #
#                   Houston, Texas 77006 USA                                   #
#                   p. +1 713.942.2377 | f. +1 832.201.8856                    #
#                   www.enfoldsystems.com                                      #
#                   info@enfoldsystems.com                                     #
#------------------------------------------------------------------------------#
"""Unit tests.
$Id: $
"""


from Products.RhaptosTest import config
import Products.RhaptosPDFLatexTool
config.products_to_load_zcml = [('configure.zcml', Products.RhaptosPDFLatexTool),]
config.products_to_install = ['RhaptosPDFLatexTool']

from Products.CMFCore.utils import getToolByName
from Products.RhaptosTest import base


PATHNAME = './src/Products.RhaptosPDFLatexTool/Products/RhaptosPDFLatexTool/tests/test_dir'
FILENAME = 'test_file.txt'


class TestRhaptosPDFLatexTool(base.RhaptosTestCase):

    def afterSetUp(self):
        self.pdf_latex_tool = getToolByName(self.portal, 'portal_pdflatex')

    def beforeTearDown(self):
        pass

    def test_pdf_latex_tool(self):
        return
        pdf = self.pdf_latex_tool.convertFSDirToPDF(PATHNAME, FILENAME)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRhaptosPDFLatexTool))
    return suite
