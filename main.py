import pdfplumber
import re

def extract_info_from_pdf(pdf):
    extracted_info = {}
    with pdfplumber.open(pdf) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        lines = text.split('\n')
        next_value_is_empty = False
        for line in lines:

            if next_value_is_empty:
                if ':' not in line:
                    extracted_info[key] = line.strip()
                    next_value_is_empty = False

            if line.count(":") > 0:
                part_line = re.split(r"(?<!EXP)(?<!TAGGED)(?<!CERT)(?<!#)\s", line)
                key = ""
                for item in part_line:
                    if ':' in item:
                        key = item.strip()[:-1].strip()
                        extracted_info[key] = 'Empty'
                        next_value_is_empty = True
                    else:
                        extracted_info[key] = item.strip()

            else:
                if line in extracted_info.values():
                    continue
                else:
                    key = line
                    extracted_info[key] = "Empty"

        return extracted_info

def compare_lists(info, next):
    keys1 = list(info.keys())
    keys2 = list(next.keys())
    print(keys1==keys2)

pdf_path = "test_task.pdf"

sample_dict = extract_info_from_pdf(pdf_path)
second_dict = extract_info_from_pdf(pdf_path)

print(sample_dict)

compare_lists(sample_dict, second_dict)

