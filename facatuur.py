import json
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

NOT_ALLOWED_SYMBOLS = r'\/:*?"<>|:;.'

def createPDF(filename, text, style_name='BodyText'):
    doc = SimpleDocTemplate('PDF_INVOICE/'+filename + '.pdf', pagesize=A4)
    styles = getSampleStyleSheet()
    style = styles[style_name]
    elements = []
    paragraphs = text.split("\n")
    for para in paragraphs:
        p = Paragraph(para, style)
        elements.append(p)
        elements.append(Spacer(1, 12))
    doc.build(elements)

def generate_invoice_pdf_from_json(json_file_path):
    if not os.path.exists(json_file_path):
        print(f"Error: The file {json_file_path} does not exist.")
        return
    with open(json_file_path, 'r') as file:
        invoice = json.load(file)

    output_filename = os.path.splitext(os.path.basename(json_file_path))[0]
    text_lines = []
    

 
    text_lines.append(f"Order Number: {invoice['order']['ordernummer']}")
    text_lines.append(f"Order Date: {invoice['order']['orderdatum']}")
    text_lines.append(f"Payment Term: {invoice['order']['betaaltermijn']}")
    text_lines.append(f"\nCustomer Details:")
    klant = invoice['order']['klant']
    text_lines.append(f"Name: {klant['naam']}")
    text_lines.append(f"Address: {klant['adres']}")
    text_lines.append(f"Postal Code: {klant['postcode']}")
    text_lines.append(f"City: {klant['stad']}")
    text_lines.append(f"KVK Number: {klant['KVK-nummer']}")
    
    text_lines.append("\nProducts:")
    for product in invoice['order']['producten']:
        text_lines.append(f"Product: {product['productnaam']}")
        text_lines.append(f"Quantity: {product['aantal']}")
        text_lines.append(f"Price (excl. VAT): €{product['prijs_per_stuk_excl_btw']}")
        text_lines.append(f"VAT Percentage: {product['btw_percentage']}%\n")
        text_lines.append(f'BTW Percentage: {round((product['aantal'] * product['prijs_per_stuk_excl_btw']) * (product['btw_percentage']/100),2)}')
    text = "\n".join(text_lines)

    createPDF(output_filename, text)
    print(f'{output_filename}.pdf is created!')
    
for file in os.listdir('JSON_ORDER'):
    generate_invoice_pdf_from_json('JSON_ORDER/'+ file)




