# Scraping and reading the data from the pdf
import tabula as tb
import pandas as pd
import re

import PyPDF2

test_file = 'Most_Represented_Before_Name.pdf'

data_entry = {
    linkedinURL : None,
    name : None,
    currentTitle : None,
    currentEmployer : None,
    employedFor : None,
    graduatingYear : None
}


def extract_last_number(string):
    # Use regular expressions to find the last number in the string
    matches = re.findall(r'\d+', string)

    if matches:
        last_number = int(matches[-1])  # Convert the last match to an integer
        return last_number
    else:
        return None  # Return None if no numbers are found in the string

def extract_data_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Extract text from the PDF
        text = ''
        for page in reader.pages:
            text += page.extract_text()

        lst = text.split('\n')
        print(lst)

        # for it in range(len(lst)):
        #     if lst[it] == 'Experience' or lst[it] == 'Erfaring':
        #         print(f'last company: {lst[it + 1]}')
        #     if lst[it] == 'Uddannelse' or lst[it] == 'Education':
        #         print(f'University Name: {lst[it + 1]}')
        #         print(f'What was studied: {lst[it + 2]}')
        #         count = 2
        #         grad_year = None
        #         while grad_year == None:
        #             grad_year = extract_last_number(lst[it + count])
        #             count += 1
        #         if count > 3:
        #             new_count = 1
        #             for i in range(3, count):
        #                 print(lst[it + 2 + new_count])
        #         print(f'Graduating year: {grad_year}')


extract_data_from_pdf(test_file)















# # Iterate over the PDF files in the 'download' folder
# folder_path = "download"
# for filename in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, filename)

#     # Check if the current item is a file ending in .pdf
#     if os.path.isfile(file_path) and file_path.lower().endswith('.pdf'):
#         extract_data_from_pdf(file_path)


# Iterating through the files in the 'download' folder
# import os

# folder_path = "download"  # Specify the folder name

# # Get the absolute path of the current directory
# current_directory = os.getcwd()

# # Create the full path to the folder
# folder_full_path = os.path.join(current_directory, folder_path)

# # Iterate over all files in the folder
# for filename in os.listdir(folder_full_path):
#     file_path = os.path.join(folder_full_path, filename)

#     # Check if the current item is a file
#     if os.path.isfile(file_path):
#         # Process the file as needed
#         with open(file_path, "r") as file:
#             # Read the contents of the file
#             file_contents = file.read()

#             # Do something with the file contents
#             print(file_contents)