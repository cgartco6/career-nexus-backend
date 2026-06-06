import io
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

class DocumentCreatorService:
    @staticmethod
    def generate_pdf_document(title: str, clear_text_body: str) -> bytes:
        """Compiles clean, typeset documents dynamically into memory buffers."""
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=letter,
            rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
        )
        
        styles = getSampleStyleSheet()
        
        # Striking Corporate Design Palette Specifications
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontSize=24,
            leading=28,
            textColor='#1A365D', # Deep Navy Blue Accent
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        body_style = ParagraphStyle(
            'DocBody',
            parent=styles['BodyText'],
            fontSize=11,
            leading=16,
            textColor='#2D3748', # Slate Grey Typography
            alignment=TA_JUSTIFY,
            spaceAfter=12
        )
        
        story = [
            Paragraph(title, title_style),
            Spacer(1, 15)
        ]
        
        # Parse text lines into sequential paragraphs
        for line in clear_text_body.split('\n'):
            if line.strip():
                story.append(Paragraph(line.strip(), body_style))
                
        doc.build(story)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()

    @staticmethod
    def compress_artifacts_to_zip(files_dictionary: dict) -> bytes:
        """Combines multiple document components into an optimized ZIP archive stream."""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for filename, file_bytes in files_dictionary.items():
                zip_file.writestr(filename, file_bytes)
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
