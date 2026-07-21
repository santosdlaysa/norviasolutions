from pathlib import Path
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor

root = Path(__file__).resolve().parents[1]
source = root / 'output' / 'pdf' / 'Norvia_Solutions_Brand_Book_Completo_v1.0.pdf'
out = root / 'output' / 'pdf'

reader = PdfReader(str(source))

def reset_footer(page, page_number):
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    stream = BytesIO()
    canvas = Canvas(stream, pagesize=(width, height))
    canvas.setFillColor(HexColor('#0F1D18'))
    canvas.rect(12*mm, 10*mm, width-24*mm, 19*mm, fill=1, stroke=0)
    canvas.setStrokeColor(HexColor('#7FCB8F'))
    canvas.setLineWidth(0.7)
    canvas.line(25*mm, 24*mm, width-25*mm, 24*mm)
    canvas.setFont('Courier', 6.5)
    canvas.setFillColor(HexColor('#B5D978'))
    canvas.drawString(25*mm, 14*mm, 'ESTUDIO DE SOFTWARE  //  v1.0')
    canvas.setFillColor(HexColor('#9A9A9B'))
    canvas.drawString(17*mm, 8.5*mm, 'NORVIA SOLUTIONS  /  DESIGN SYSTEM 1.0')
    canvas.drawRightString(width-17*mm, 8.5*mm, f'{page_number:02d}')
    canvas.save()
    overlay = PdfReader(BytesIO(stream.getvalue())).pages[0]
    page.merge_page(overlay)

def write_pdf(name, start, end, reset_numbers=False):
    writer = PdfWriter()
    for index in range(start, min(end, len(reader.pages))):
        page = reader.pages[index]
        if reset_numbers:
            reset_footer(page, index - start + 1)
        writer.add_page(page)
    target = out / name
    with target.open('wb') as handle:
        writer.write(handle)
    return target, len(writer.pages)

brand, brand_pages = write_pdf('Norvia_Brand_Book_Marca_v1.0.pdf', 0, 19)
system, system_pages = write_pdf('Norvia_Design_System_v1.0.pdf', 19, len(reader.pages), reset_numbers=True)
print(f'{brand} | {brand_pages} paginas')
print(f'{system} | {system_pages} paginas')
