# import fitz

# def crop_pdf(input_path, output_path):
#     pdf = fitz.open(input_path)

#     for page_num in range(pdf.page_count):
#         page = pdf[page_num]
#         mediabox = page.mediabox
#         page_width = mediabox.x1 - mediabox.x0

#         # Calculate the new crop box dimensions
#         new_left = mediabox.x0 + (page_width / 3)
#         new_mediabox = fitz.Rect(new_left, mediabox.y0, mediabox.x1, mediabox.y1)
        
#         # Apply the new crop box to the page
#         page.set_cropbox(new_mediabox)

#     pdf.save(output_path)
#     pdf.close()

# crop_pdf('English.pdf', 'English_out.pdf')

def crop_pdf(input_path, output_path):
    pdf = fitz.open(input_path)

    for page_num in range(pdf.page_count):
        page = pdf[page_num]
        mediabox = page.mediabox
        page_width = mediabox.x1 - mediabox.x0

        # Calculate the new crop box dimensions
        new_left = mediabox.x0 + (page_width / 3)
        new_mediabox = fitz.Rect(new_left, mediabox.y0, mediabox.x1, mediabox.y1)
        
        # Remove the content outside the crop box
        page.delete_area(new_mediabox)

    pdf.save(output_path)
    pdf.close()

