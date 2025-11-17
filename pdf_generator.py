import base64
import io
import json

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from PIL import Image as PILImage

def _base64_to_image(base64_string):
    """Converts a base64 string to a PIL Image object."""
    img_data = base64.b64decode(base64_string)
    return io.BytesIO(img_data)

def generate_pdf_report(data, filename="landscape_design_report.pdf"):
    """
    Generates a PDF report from the final JSON data.
    """
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title Page
    story.append(Paragraph(f"Landscape Design for: {data['summary_report'].split(' for ')[1].split('.')[0]}", styles['h1']))
    story.append(Spacer(1, 0.5 * inch))
    
    # Summary
    story.append(Paragraph("Project Summary", styles['h2']))
    story.append(Paragraph(data['summary_report'], styles['BodyText']))
    story.append(Spacer(1, 0.25 * inch))

    # Selected Theme
    story.append(Paragraph("Selected Theme", styles['h2']))
    story.append(Paragraph(f"<b>{data['theme_selected']['name']}</b>", styles['h3']))
    story.append(Paragraph(data['theme_selected']['description'], styles['BodyText']))
    
    story.append(PageBreak())

    # Before & After
    story.append(Paragraph("Before & After Vision", styles['h2']))
    story.append(Spacer(1, 0.25 * inch))
    
    before_img_data = _base64_to_image(data['before_after']['before_image_base64'])
    after_img_data = _base64_to_image(data['before_after']['after_image_base64'])
    
    # Resize images to fit side-by-side
    img_width = 3 * inch
    
    before_img = Image(before_img_data, width=img_width, height=img_width * 0.75)
    after_img = Image(after_img_data, width=img_width, height=img_width * 0.75)

    table_data = [[before_img, after_img], [Paragraph("<b>Before</b>", styles['Normal']), Paragraph("<b>After</b>", styles['Normal'])]]
    table = Table(table_data, colWidths=[3.25 * inch, 3.25 * inch])
    table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    story.append(table)

    story.append(PageBreak())

    # Overhead Plan
    story.append(Paragraph("Overhead Design", styles['h2']))
    story.append(Spacer(1, 0.25 * inch))
    
    overhead_img_data = _base64_to_image(data['overhead_plan']['rendered_image_base64'])
    overhead_img = Image(overhead_img_data, width=6 * inch, height=6 * inch)
    story.append(overhead_img)
    story.append(Spacer(1, 0.25 * inch))
    
    story.append(Paragraph("Layout Details", styles['h3']))
    plan_text = json.dumps(data['overhead_plan']['json_plan'], indent=2)
    story.append(Paragraph(plan_text.replace('\n', '<br/>'), styles['Code']))

    story.append(PageBreak())
    
    # Materials List
    story.append(Paragraph("Materials & Cost Estimate", styles['h2']))
    story.append(Spacer(1, 0.25 * inch))

    materials_data = [["Type", "Name", "Qty", "Placement", "Cost/Unit", "Sunlight", "Soil Notes"]]
    for item in data['materials']:
        row = [
            item.get('item_type', ''),
            item.get('name', ''),
            str(item.get('quantity', '')),
            item.get('placement', ''),
            item.get('cost_range_per_unit', ''),
            item.get('sunlight_needs', 'N/A'),
            item.get('soil_notes', 'N/A')
        ]
        materials_data.append(row)
        
    mat_table = Table(materials_data)
    mat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(mat_table)

    doc.build(story)
    print(f"\n✅ PDF report generated: {filename}")
