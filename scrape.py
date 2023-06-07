# Scraping and reading the data from the pdf
import tabula as tb
import pandas as pd
import re
import copy

import PyPDF2

from newcrop import crop_pdf

test_file = 'Long_Education.pdf'

data_format = {
    "linkedinURL" : None,
    "name" : None,
    "currentTitle" : None,
    "currentEmployer" : None,
    "employedFor" : None,
    "gradYear" : None,
    "university" : None,
    "major" : None,
}


def extract_last_number(string):
    # Use regular expressions to find the last number in the string
    matches = re.findall(r'\d+', string)

    if matches:
        last_number = int(matches[-1])  # Convert the last match to an integer
        return last_number
    else:
        return None  # Return None if no numbers are found in the string

def is_linkedin_string(string):
    return string.endswith('(LinkedIn)')

def extract_data_from_pdf(file_path):
    data_entry = copy.deepcopy(data_format)

    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)


        # Extract text from the PDF
        text = ''
        for page in reader.pages:
            text += page.extract_text()

        lst = text.split('\n')

        for it in range(len(lst)):
            if lst[it] == "Kontakt" or lst[it] == "Contact" or lst[it] == "Coordonnées":
                count = 1
                while not is_linkedin_string(lst[it + count]) :
                    curr_url = data_entry["linkedinURL"]
                    new_url = lst[it + count]
                    if not curr_url:
                        data_entry["linkedinURL"] = new_url
                    else:
                        data_entry["linkedinURL"] = f"{curr_url}{new_url}"
                    count += 1
                curr_url = data_entry["linkedinURL"]
                new_url = lst[it + count]
                if not curr_url:
                    data_entry["linkedinURL"] = new_url
                else:
                    data_entry["linkedinURL"] = f"{curr_url}{new_url}"

            if lst[it] == 'Experience' or lst[it] == 'Erfaring':
                data_entry["currentEmployer"] = lst[it + 1]
                # p rint(f'last company: {lst[it + 1]}')
            if lst[it] == 'Uddannelse' or lst[it] == 'Education':
                data_entry["university"] = lst[it + 1]
                # p rint(f'University Name: {lst[it + 1]}')
                data_entry["major"] = lst[it + 2]
                # pr int(f'What was studied: {lst[it + 2]}')
                count = 2
                gradYear = None
                new_count = 1
                while gradYear == None:
                    gradYear = extract_last_number(lst[it + count])
                    count += 1
                    # pr int(f"it : {it}")
                    # pri nt(f"new_count : {new_count}")
                    # pri nt(f"count : {count}")
                    if count > 3:
                        major = data_entry['major']
                        additional_major = lst[it + 2 + new_count]
                        data_entry["major"] = f"{major} {additional_major}"
                        new_count += 1
                        # pr int(lst[it + 2 + new_count])
                    data_entry["gradYear"] = gradYear
                    # pri nt(f'Graduating year: {grad_year}')

        # pr nt(lst)

        # for key, val in data_entry.items():
        #     pr int(f"{key} : {val}")
    
    # cropped_file_path = f"cropped_{file_path}"
    # crop_pdf(file_path, cropped_file_path)
    cropped_file_path = f"English_out.pdf"

    with open(cropped_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)


        # Extract text from the PDF
        text = ''
        for page in reader.pages:
            text += page.extract_text()

        lst = text.split('\n')

        # for it in range(len(lst)):
        print(lst)

    return data_entry



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
#             pri nt(file_contents)