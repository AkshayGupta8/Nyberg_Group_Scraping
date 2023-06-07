from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import RectangleObject

def crop_left_third(input_pdf, output_pdf):
    with open(input_pdf, 'rb') as file:
        pdf = PdfFileReader(file)
        writer = PdfFileWriter()

        for page_num in range(pdf.getNumPages()):
            page = pdf.getPage(page_num)
            width = page.mediaBox.getWidth()
            height = page.mediaBox.getHeight()

            # Calculate the dimensions of the right 2/3 of the page
            right_third_width = width * 1 / 3

            # Create a new crop box with the right 2/3 dimensions
            crop_box = RectangleObject(
                [right_third_width, 0, width, height],
                # inheritable=True
            )
            page.cropBox = crop_box
            page.mediaBox = crop_box

            writer.addPage(page)

        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

    print(f"Cropped PDF saved to {output_pdf}")
crop_left_third('English.pdf', 'English_out.pdf')