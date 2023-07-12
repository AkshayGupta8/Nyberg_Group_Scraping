#!/usr/bin/env python

# Scraping and reading the data from the pdf
import tabula as tb
import re
import copy

import PyPDF2
from fitz import Document, Page, Rect
import fitz

import os
import sys

import xlsxwriter

# from newcrop import crop_pdf

test_file = 'index_error.pdf'

data_format = {
    "linkedinURL" : None,
    "name" : None,
    "title" : None,
    "currentEmployer" : None,
    "employedFor" : None,
    "gradYear" : None,
    "university" : None,
    "major" : None,
}

data_col = {
    "linkedinURL" : 5,
    "name" : 0,
    "title" : 1,
    "currentEmployer" : 2,
    "employedFor" : None,
    "gradYear" : 3,
    "university" : 4,
    "major" : None,
}

entry_count = 1 # used for the row
excel = None
excel_sheet = None

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

def extract_data_from_pdf(file_path, output_file):
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
                while (it + count < len(lst)) and (not is_linkedin_string(lst[it + count])) :
                    curr_url = data_entry["linkedinURL"]
                    new_url = lst[it + count]
                    if not curr_url:
                        data_entry["linkedinURL"] = new_url
                    else:
                        data_entry["linkedinURL"] = f"{curr_url}{new_url}"
                    count += 1
                curr_url = data_entry["linkedinURL"]
                # print(f"it + count : {it + count}")
                # print(f"len(lst) : {len(lst)}")
                # print(f"lst[it + count] : {lst[it + count]}")
                if it + count >= len(lst):
                    new_url = ""
                else:
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
    
    # To get the name
    # file_path = "English.pdf"
    doc: Document = fitz.open(file_path)

    # for i in range(len(doc)):
    page: Page = doc[0]
    page.clean_contents()  # https://pymupdf.readthedocs.io/en/latest/faq.html#misplaced-item-insertions-on-pdf-pages

    # Hard-code the rect you need
    max_width = 8.5 * 72
    max_height = 11 * 72
    rect = Rect(max_width * 0.33, 0, 8.5 * 72, 11 * 72)

    text = page.get_textbox(rect)
    text_lst = text.split('\n')
    # print(text_lst)
    # print('=============')
    # print('=============')
    data_entry['name'] = text_lst[1]
    data_entry['title'] = text_lst[2]

    global entry_count

    temp = f"{data_entry['name']}"
    temp = temp.replace(",", "", 1)
    excel_sheet.write(entry_count, data_col['name'], temp)
    new_line = f"{temp}, " # name

    temp = f"{data_entry['title']}"
    temp = temp.replace(",", "", 1)
    excel_sheet.write(entry_count, data_col['title'], temp)
    new_line += f"{temp}, " # title



    temp = f"{data_entry['currentEmployer']}"
    temp = temp.replace(",", "", 1)
    excel_sheet.write(entry_count, data_col['currentEmployer'], temp)
    new_line += f"{temp}, " # currentEmployer
    
    # temp = f"{data_entry['employedFor']}"
    # temp = temp.replace(",", "", 1)
    # new_line += f"{data_entry['employedFor']}, " # employedFor

    temp = f"{data_entry['gradYear']}"
    temp = temp.replace(",", "", 1)
    excel_sheet.write(entry_count, data_col['gradYear'], temp)
    new_line += f"{temp}, " # gradYear

    temp = f"{data_entry['university']}"
    temp = temp.replace(",", "", 1)
    excel_sheet.write(entry_count, data_col['university'], temp)
    new_line += f"{temp}, " # university

    # temp = f"{data_entry['major']}"
    # temp = temp.replace(",", "", 1)
    # new_line += f"{temp}\n" # major

    temp = f"{data_entry['linkedinURL'][:-12]}"
    temp = temp.replace(",", "", 1)
    excel_sheet.write(entry_count, data_col['linkedinURL'], temp)
    new_line += f"{temp}\n" # linkedinURL
    
    entry_count = entry_count + 1
    
    output_file.write(new_line)
    
    # for key, val in data_entry.items():
    #     print(f"{key} : {val}")

    return data_entry


def process_files_in_folder(output_file):
    # Get the current directory
    current_directory = os.getcwd()

    # Define the path to the 'download' folder

    # folder_path = os.path.join(current_directory, 'download')

    folder_path = get_download_folder()

    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print("Folder 'download' not found.")
        return

    print("Resume Scraping is beginning:")
    print("==================================================")
    

    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        # Check if the file has a .pdf extension
        if filename.endswith(".pdf"):
            # Construct the full file path
            file_path = os.path.join(folder_path, filename)

            # Call the extract_data_from_pdf function with the file path
            extract_data_from_pdf(file_path, output_file)
            print(file_path)

        else:
            print(f"Skipping file: {filename} (not a PDF)")

    print("All files processed.")

def get_download_folder():
    if getattr(sys, 'frozen', False):
        # Running as executable
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))

    download_folder = os.path.join(base_path, 'download')
    return download_folder

def get_base_path():
    if getattr(sys, 'frozen', False):
        # Running as executable
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return base_path

def main():
    file_counter = 1
    file_name = 'processed_data_1.csv'

    while os.path.exists(file_name):
        file_counter += 1
        file_name = f'processed_data_{file_counter}.csv'
    

    flag = False
    output_file_path = os.path.join(get_base_path(), file_name)
    with open(output_file_path, 'w') as output_file:
        global excel 
        excel_name = str(output_file_path)
        excel_name = excel_name[:-4]
        excel_name = f"{excel_name}.xlsx"
        excel = xlsxwriter.Workbook(excel_name)
        global excel_sheet 
        excel_sheet = excel.add_worksheet()

        for key, val in data_col.items():
            if val:
                excel_sheet.write(0, data_col[key], key)

        first_line = "Name, " # name
        first_line += "Title, " # title
        first_line += "Current Employer, " # currentEmployer
        # first_line += "Employed Duration, " # employedFor
        first_line += "Graduation Year, " # gradYear
        first_line += "University, " # university
        first_line += "Linkedin URL\n" # linkedinURL
        # first_line += "Major\n" # major

        output_file.write(first_line)
        process_files_in_folder(output_file)
        flag = True
    if flag:
        print("==================================================")
        print(f"A new file '{file_name}' has been created.")
        print(f"A new file '{file_name[:-3]}xlsx' has been created.")
        # global excel
        excel.close()

if __name__ == '__main__':
  main()
