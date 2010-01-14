"""
Initialize PDFLatexTool Product

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU General
Public License Version 2 (GPL).  See LICENSE.txt for details.
"""

import sys
from Products.CMFCore import utils
import PDFLatexTool

this_module = sys.modules[ __name__ ]
product_globals = globals()
tools = ( PDFLatexTool.PDFLatexTool,)

def initialize(context):
    utils.ToolInit('PDFLatex Tool',
                    tools = tools,
                    icon='tool.gif' 
                    ).initialize( context )
