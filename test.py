import PyPDF2
import textract

def read_right_column_top_words(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf = PyPDF2.PdfFileReader(file)

        # Assuming the right column is the second column
        column_index = 1

        # Extract the text from the right column of the first page
        page = pdf.getPage(0)
        page_text = page.extract_text()
        lines = page_text.strip().split('\n')

        # Calculate the number of lines in the right column
        num_lines = len(lines) // 2

        # Get the top lines from the right column
        top_lines = lines[:num_lines]

        # Join the lines into a single string
        top_text = ' '.join(top_lines)

        # Split the text into words
        words = top_text.split()

        return words

# def read_right_column_top_words(pdf_path):
#     with open(pdf_path, 'rb') as file:
#         pdf = PyPDF2.PdfFileReader(file)

#         # Assuming the right column is the second column
#         column_index = 1

#         # Extract the text from the right column of the first page
#         page = pdf.getPage(0)
#         page_text = page.extract_text()
#         text_lines = page_text.strip().split('\n')

#         # print(text_lines)

#         # Get the top lines from the right column
#         top_lines = text_lines[:len(text_lines) // 2]

#         # Join the lines into a single string
#         top_text = ' '.join(top_lines)

#         # Use Textract to extract words from the text
#         words = textract.process(
#             input_bytes=top_text.encode(),
#             method='tesseract',
#             encoding='utf-8',
#             language='eng',
#             psm=6,  # Assume a single uniform block of text
#             config='--psm 6',
#         ).decode().split()
#         # words = 'lskjfd'
#         return words
    
print(read_right_column_top_words('English.pdf'))