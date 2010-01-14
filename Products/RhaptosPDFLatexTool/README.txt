RhaptosPDFLatexTool

  This Zope Product is part of the Rhaptos system
  (http://software.cnx.rice.edu)

  RhaptosPDFLatexTool provides a CMF tool for exporting a Rhaptos
  modules as a PDF file.  It accomplishes this by dumping the module
  to the filesystem, converting its CNXML to LaTeX and running the
  pdflatex command.

Requirements

  * LaTeX: including the following packages:
        - pdflatex
        - cjk-latex
        - tetex-extra
        - latex-ucs
        - latex-ucs-contrib
        - hbf-kanji48

  * Ghostscript (gs)

  * gif2png

Future plans

  - This is too much effort to be run in-process.  This code should be
    its own server process that can manage PDF generation requests and
    even cache results.  This will also enable us to enqueue
    long-running PDF jobs (like courses), sending an email to the
    requester when it is complete
