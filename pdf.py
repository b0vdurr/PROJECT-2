from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
NOT_ALLOWED_SYMBOLS='\/:*?"<>|:;.'
def createPDF(filename,text,style_name='BodyText'):
    doc = SimpleDocTemplate(filename + '.pdf', pagesize=A4)

    styles = getSampleStyleSheet()
    style = styles[style_name]
    elements = []

    paragraphs = text.split("\n\n")
    for para in paragraphs:
        p = Paragraph(para, style)
        elements.append(p)
        elements.append(Spacer(1, 12))
    doc.build(elements)

while True:
    filename=input('Enter name of your file (WITHOUT EXTENSION):\n')
    for letter in filename:
        if letter in NOT_ALLOWED_SYMBOLS:
            print(f"{letter} can't be used in the name of the file!")
            continue
    text=input('Enter text:\n')
    createPDF(filename,text)
    print(f'{filename}.pdf is created!')