from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
import string

def install(self):
    """Add the tool"""
    out = StringIO()

    # Add the tool
    urltool = getToolByName(self, 'portal_url')
    portal = urltool.getPortalObject();
    try:
        portal.manage_delObjects('portal_pdflatex')
        out.write("Removed old portal_pdflatex tool\n")
    except:
        pass  # we don't care if it fails
    portal.manage_addProduct['RhaptosPDFLatexTool'].manage_addTool('PDFLatex Tool', None)

    # Register skins
    
    
    out.write("Adding PDFLatex Tool\n")

    return out.getvalue()
