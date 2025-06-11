import fitz
import os
import uuid

def stamp_pdf(pdf_path, stamp_path, position=(100, 100), scale=0.5, page_number=0):
    doc = fitz.open(pdf_path)
    page = doc[0]

    # Load stamp image and calculate dimensions
    img = fitz.open(stamp_path)
    rect = img[0].rect
    width, height = rect.width * scale, rect.height * scale
    img.close()


    # Load the stamp image
    stamp_rect = fitz.Rect(position[0], position[1], position[0] + width, position[1] + height)
    page.insert_image(stamp_rect, filename=stamp_path, overlay=True)

    output_filename = f"stamped_{uuid.uuid4().hex}.pdf"
    output_path = os.path.join("app/static", output_filename)
    doc.save(output_path)

    return output_path