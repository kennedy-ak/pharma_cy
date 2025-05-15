# Step 1: Install required dependencies
# pip install reportlab

# Step 2: Add PDF generation utility in a new file called utils.py
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.conf import settings
import os
from datetime import datetime

def generate_invoice_pdf(sale):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    subtitle_style = styles["Heading2"]
    normal_style = styles["Normal"]
    
    # Custom styles
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,  # Center alignment
    )
    
    # Add pharmacy name/header
    elements.append(Paragraph("Pharmacy Management System", header_style))
    elements.append(Spacer(1, 0.25*inch))
    elements.append(Paragraph(f"INVOICE #{sale.id}", subtitle_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Add sale details
    elements.append(Paragraph(f"Date: {sale.transaction_date.strftime('%Y-%m-%d %H:%M')}", normal_style))
    elements.append(Paragraph(f"Payment Method: {sale.payment_method.name if sale.payment_method else 'Unknown'}", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Create items table
    data = [['Drug', 'Quantity', 'Unit Price', 'Total']]
    for item in sale.items.all():
        data.append([
            item.drug.name,
            str(item.quantity),
            f"${item.price_at_sale:.2f}",
            f"${item.get_total():.2f}"
        ])
    
    # Add total row
    data.append(['', '', 'Grand Total:', f"${sale.total_amount:.2f}"])
    
    # Create the table
    table = Table(data, colWidths=[2.5*inch, 1*inch, 1.5*inch, 1.5*inch])
    
    # Style the table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.white),
        ('GRID', (0, 0), (-1, -2), 1, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, -1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
        ('GRID', (-2, -1), (-1, -1), 1, colors.black),
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
    ])
    table.setStyle(table_style)
    elements.append(table)
    
    # Add footer
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("Thank you for your purchase!", normal_style))
    elements.append(Paragraph(f"Invoice generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
    
    # Build PDF
    doc.build(elements)
    
    # Return PDF as response
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

# Step 3: Add a view to generate and download the PDF
def download_invoice(request, pk):
    from .models import Sale
    from django.http import HttpResponse
    
    sale = get_object_or_404(Sale, pk=pk)
    pdf = generate_invoice_pdf(sale)
    
    # Create response with PDF
    response = HttpResponse(content_type='application/pdf')
    filename = f"invoice_{sale.id}_{sale.transaction_date.strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write(pdf)
    
    return response