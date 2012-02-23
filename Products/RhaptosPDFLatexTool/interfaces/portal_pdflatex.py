# Copyright (c) 2003 The Connexions Project, All Rights Reserved
# Written by Brent Hendricks

""" File system import interface"""

from Interface import Attribute
try:
    from Interface import Interface
except ImportError:
    # for Zope versions before 2.6.0
    from Interface import Base as Interface

class portal_pdflatex(Interface):
    """Defines an interface for a tool that converts content to a PDF file"""

    id = Attribute('id','Must be set to "portal_pdflatex"')

    def convertObjectToPDF(object, style, **params):
        """
        Convert the given object to a PDF file, possible using its subjects as necessary
        """

    def convertFSDirToPDF(path, filename, style='', **params):
        """
        Produce a PDF from a directory on the filesystem
        """
    
