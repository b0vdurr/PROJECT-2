import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def createPDF(filename, text, logo_path='logo.png'):
    doc = SimpleDocTemplate(f'PDF_INVOICE/{filename}.pdf', pagesize=A4)
    styles = getSampleStyleSheet()
    body_style = styles['BodyText']
    title_style = ParagraphStyle('Title', parent=styles['Title'], alignment=1, spaceAfter=20)
    section_title_style = ParagraphStyle('SectionTitle', parent=styles['Heading1'], alignment=1, spaceAfter=10)
    
    elements = []
    
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=300, height=100)
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 20))
    
    elements.append(Spacer(1, 10))
    
    elements.append(Paragraph("Order Details", section_title_style))
    order_details = text.get('order_details')
    for detail in order_details:
        elements.append(Paragraph(detail, body_style))
    
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Customer Details", section_title_style))
    customer_data = text.get('customer_details')
    
    customer_table_data = [
        ['Name:', customer_data['name']],
        ['Address:', customer_data['address']],
        ['Postal Code:', customer_data['postal_code']],
        ['City:', customer_data['city']],
        ['KVK Number:', customer_data['kvk_number']],
    ]
    customer_table = Table(customer_table_data, colWidths=[120, 300])
    customer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ]))
    elements.append(customer_table)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Products", section_title_style))
    product_data = text.get('product_details')
    
    product_table_data = [['Product Name', 'Quantity', 'Price', 'VAT (%)', 'VAT Amount']]
    
    total_amount = 0
    for product in product_data:
        vat_amount = round((product['quantity'] * product['price_per_unit_excl_vat']) * (product['vat_percentage'] / 100), 2)
        product_table_data.append([product['name'], product['quantity'], f"€{product['price_per_unit_excl_vat']}", f"{product['vat_percentage']}%", f"€{vat_amount}"])
        total_amount += vat_amount
    
    product_table = Table(product_table_data, colWidths=[180, 80, 80, 80, 80])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ]))
    elements.append(product_table)
    
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Total VAT: €{round(total_amount,2)}", body_style))
    
    doc.build(elements)

def generate_invoice_pdf_from_json(json_file_path):
    if not os.path.exists(json_file_path):
        print(f"Error: The file {json_file_path} does not exist.")
        return
    
    with open(json_file_path, 'r') as file:
        invoice = json.load(file)

    output_filename = os.path.splitext(os.path.basename(json_file_path))[0]
    text = {}

    text['order_details'] = [
        f"Order Number: {invoice['order']['ordernummer']}",
        f"Order Date: {invoice['order']['orderdatum']}",
        f"Payment Term: {invoice['order']['betaaltermijn']}"
    ]
    
    customer_details = {
        'name': invoice['order']['klant']['naam'],
        'address': invoice['order']['klant']['adres'],
        'postal_code': invoice['order']['klant']['postcode'],
        'city': invoice['order']['klant']['stad'],
        'kvk_number': invoice['order']['klant']['KVK-nummer']
    }
    text['customer_details'] = customer_details

    product_details = []
    for product in invoice['order']['producten']:
        product_details.append({
            'name': product['productnaam'],
            'quantity': product['aantal'],
            'price_per_unit_excl_vat': product['prijs_per_stuk_excl_btw'],
            'vat_percentage': product['btw_percentage']
        })
    text['product_details'] = product_details
    
    createPDF(output_filename, text)
    print(f'{output_filename}.pdf is created!')

for file in os.listdir('JSON_ORDER'):
    generate_invoice_pdf_from_json(f'JSON_ORDER/{file}')
