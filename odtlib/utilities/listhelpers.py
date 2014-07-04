from odtlib import text

def check_paragraph_input(para, style):
    if isinstance(para, str):
        return text.Paragraph(para, style=style)
    if not isinstance(para, text.Paragraph):
        raise ValueError('Input to the paragraph list must be strings or Paragraph objects')
    return para