import os.path

import fitz
from fitz import Document, Page, Rect

# For visualizing the rects that PyMuPDF uses compared to what you see in the PDF

file_path = "English.pdf"
doc: Document = fitz.open(file_path)

for i in range(len(doc)):
    page: Page = doc[i]
    page.clean_contents()  # https://pymupdf.readthedocs.io/en/latest/faq.html#misplaced-item-insertions-on-pdf-pages

    # Hard-code the rect you need
    max_width = 8.5 * 72
    max_height = 11 * 72
    rect = Rect(max_width * 0.33, 0, 8.5 * 72, 11 * 72)

    text = page.get_textbox(rect)

    print(text)
