from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_pdf_ticket(event_name, ticket_id, file_path):
    c = canvas.Canvas(file_path, pagesize=letter)
    c.drawString(100, 750, "Event Name: {}".format(event_name))
    c.drawString(100, 730, "Ticket ID: {}".format(ticket_id))
    c.save()

#def generate_pdf_ticket(event_name, ticket_id, file_path):
#    doc = SimpleDocTemplate(file_path, pagesize=letter)
#    styles = getSampleStyleSheet()
#    normal_style = styles['Normal']
#    centered_style = ParagraphStyle(name='Centered', alignment=1)
#
#    data = [
#        ["Event Name:", event_name],
#        ["Ticket ID:", ticket_id],
#    ]
#
#    table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                              ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
#                              ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
#                              ('FONTSIZE', (0, 0), (-1, -1), 12),
#                              ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
#                              ('TOPPADDING', (0, 0), (-1, -1), 12),
#                              ('LEFTPADDING', (0, 0), (-1, -1), 12),
#                              ('RIGHTPADDING', (0, 0), (-1, -1), 12),
#                              ('GRID', (0, 0), (-1, -1), 1, colors.black),
#                              ])
#
#    event_table = Table(data, colWidths=[200, 200], style=table_style)
#    doc.build([event_table])