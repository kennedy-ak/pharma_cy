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
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.5*inch,
        rightMargin=0.5*inch
    )
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Enhanced custom styles
    main_header_style = ParagraphStyle(
        'MainHeaderStyle',
        parent=styles['Normal'],
        fontSize=18,
        alignment=1,  # Center alignment
        fontName='Helvetica-Bold',
        textColor=colors.darkblue,
        spaceAfter=5
    )
    
    pharmacy_name_style = ParagraphStyle(
        'PharmacyNameStyle',
        parent=styles['Normal'],
        fontSize=12,
        alignment=1,  # Center alignment
        fontName='Helvetica',
        textColor=colors.darkgreen,
        spaceAfter=8
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1,  # Center alignment
        fontName='Helvetica',
        textColor=colors.black,
        spaceAfter=3
    )
    
    receipt_header_style = ParagraphStyle(
        'ReceiptHeaderStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=0,  # Left alignment
        fontName='Helvetica-Bold',
        textColor=colors.darkred,
        spaceBefore=10,
        spaceAfter=8
    )
    
    item_style = ParagraphStyle(
        'ItemStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=0,  # Left alignment
        fontName='Courier',
        spaceAfter=2
    )
    
    summary_style = ParagraphStyle(
        'SummaryStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=0,  # Left alignment
        fontName='Courier-Bold',
        spaceAfter=2
    )
    
    total_style = ParagraphStyle(
        'TotalStyle',
        parent=styles['Normal'],
        fontSize=12,
        alignment=0,  # Left alignment
        fontName='Helvetica-Bold',
        textColor=colors.darkred,
        spaceBefore=5,
        spaceAfter=5
    )
    
    payment_style = ParagraphStyle(
        'PaymentStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=0,  # Left alignment
        fontName='Courier',
        textColor=colors.darkblue,
        spaceAfter=2
    )
    
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=11,
        alignment=1,  # Center alignment
        fontName='Helvetica-Bold',
        textColor=colors.darkgreen,
        spaceBefore=15,
        spaceAfter=8
    )
    
    barcode_style = ParagraphStyle(
        'BarcodeStyle',
        parent=styles['Normal'],
        fontSize=14,
        alignment=1,  # Center alignment
        fontName='Courier-Bold',
        textColor=colors.black,
        spaceBefore=5,
        spaceAfter=3
    )
    
    # Add a decorative border effect
    elements.append(Paragraph("=" * 60, contact_style))
    
    # Pharmacy Header with enhanced styling
    elements.append(Paragraph("🏥 PHARMACY", main_header_style))
    elements.append(Paragraph("Local Pharmacy Shop", pharmacy_name_style))
    elements.append(Spacer(1, 0.05*inch))
    
    # Contact information in a box-like format
    elements.append(Paragraph("📞 (888) 888 8888", contact_style))
    elements.append(Paragraph(f"🏪 Store# {sale.id:08d}", contact_style))
    elements.append(Paragraph("📍 38343, Drugs Road", contact_style))
    elements.append(Paragraph("   Akporman - Accra, Ghana", contact_style))
    
    elements.append(Paragraph("=" * 60, contact_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Transaction details with enhanced formatting
    cashier_line = f"👤 Cashier: #Admin    📅 {sale.transaction_date.strftime('%m/%d/%Y   %I:%M %p')}"
    elements.append(Paragraph(cashier_line, receipt_header_style))
    elements.append(Paragraph("-" * 60, contact_style))
    
    # Items section with better formatting
    elements.append(Paragraph("🛒 PURCHASED ITEMS", receipt_header_style))
    
    total_items = 0
    for item in sale.items.all():
        total_items += item.quantity
        # Create a more structured item line
        item_line = f"{item.quantity}x {item.drug.name:<25} ₵{item.get_total():.2f}"
        elements.append(Paragraph(item_line, item_style))
    
    elements.append(Paragraph("-" * 60, contact_style))
    
    # Summary section with enhanced styling
    from decimal import Decimal
    subtotal = sale.total_amount
    local_tax = subtotal * Decimal('0.06')  # 6% local tax
    sales_tax = subtotal * Decimal('0.03')  # 3% sales tax
    total = subtotal + local_tax + sales_tax
    
    elements.append(Paragraph("💰 PAYMENT SUMMARY", receipt_header_style))
    elements.append(Paragraph(f"{total_items} ITEMS    Subtotal      ₵{subtotal:.2f}", summary_style))
    elements.append(Paragraph(f"            Local Tax (6%) ₵{local_tax:.2f}", summary_style))
    elements.append(Paragraph(f"            Sales Tax (3%) ₵{sales_tax:.2f}", summary_style))
    elements.append(Paragraph("=" * 40, summary_style))
    elements.append(Paragraph(f"            💳 TOTAL       ₵{total:.2f}", total_style))
    
    payment_method = sale.payment_method.name if sale.payment_method else 'CASH'
    elements.append(Paragraph(f"            ✅ Paid by {payment_method.upper()}: ₵{total:.2f}", payment_style))
    
    if payment_method.upper() != 'CASH':
        elements.append(Spacer(1, 0.05*inch))
        elements.append(Paragraph(f"💳 {payment_method.upper()}  ****-****-****-9999", payment_style))
        elements.append(Paragraph(f"📱 APP  #{sale.id:07d}", payment_style))
        elements.append(Paragraph(f"🔗 REF  #{sale.id + 8809521}", payment_style))
        elements.append(Paragraph("✓ CARD PRESENT", payment_style))
    
    elements.append(Spacer(1, 0.05*inch))
    elements.append(Paragraph(f"💰 Tendered      ₵{sale.amount_tendered:.2f}", payment_style))
    elements.append(Paragraph(f"💸 Change        ₵{sale.get_change():.2f}", payment_style))
    
    elements.append(Paragraph("=" * 60, contact_style))
    
    # Enhanced footer
    elements.append(Paragraph("🙏 THANKS FOR SHOPPING WITH US! 🙏", footer_style))
    elements.append(Paragraph("Visit us again soon!", contact_style))
    
    # Enhanced barcode section
    elements.append(Spacer(1, 0.1*inch))
    barcode_number = f"1872442780848082{sale.id}"
    elements.append(Paragraph("┃┃┃┃ ┃┃┃┃ ┃┃┃┃ ┃┃┃┃", barcode_style))
    elements.append(Paragraph(barcode_number, contact_style))
    
    elements.append(Paragraph("=" * 60, contact_style))
    
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
    from django.shortcuts import get_object_or_404
    
    sale = get_object_or_404(Sale, pk=pk)
    pdf = generate_invoice_pdf(sale)
    
    # Create response with PDF
    response = HttpResponse(content_type='application/pdf')
    filename = f"invoice_{sale.id}_{sale.transaction_date.strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write(pdf)
    
    return response


# utils.py
def send_sms(phone_number, message):
    # Connect to your SMS API here (e.g., Twilio, Hubtel, etc.)
    print(f"Sending SMS to {phone_number}: {message}")  # placeholder
