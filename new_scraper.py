from PyPDF2 import PdfReader, PdfWriter

def crop_pdf(input_path, output_path):
    with open(input_path, 'rb') as file:
        pdf = PdfReader(file)
        output_pdf = PdfWriter()
        
        for page_num in range(len(pdf)):
            page = pdf.getPage(page_num)
            
            # Calculate the crop box coordinates
            media_box = page.mediaBox
            left = media_box.getLowerLeft_x()
            bottom = media_box.getLowerLeft_y()
            right = media_box.getUpperRight_x()
            top = media_box.getUpperRight_y()
            
            # Crop the page by removing the left 1/3
            new_left = left + (right - left) / 3
            page.mediaBox.lowerLeft = (new_left, bottom)
            
            # Add the modified page to the output PDF
            output_pdf.addPage(page)
            
        # Write the output PDF to a file
        with open(output_path, 'wb') as output_file:
            output_pdf.write(output_file)

crop_pdf('English.pdf', 'English_out.pdf')