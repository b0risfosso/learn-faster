import sys
import pdfplumber
from PyPDF2 import PdfWriter, PdfReader
import difflib


def split_pdf(input_file, output_file, start_page, end_page):
    with open(input_file, 'rb') as file:
        reader = PdfReader(file)
        writer = PdfWriter()

        # Validate page range
        if start_page < 1 or end_page > len(reader.pages) or start_page > end_page:
            print("Invalid page range.")
            return

        # Extract pages and add them to the output file
        for page_num in range(start_page - 1, end_page):
            page = reader.pages[page_num]
            writer.add_page(page)

        # Write the output to a new PDF file
        with open(output_file, 'wb') as output:
            writer.write(output)

        print("PDF pages extracted successfully.")


def convert_to_text(input_file, output_file):
    with pdfplumber.open(input_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

        with open(output_file, 'w', encoding='utf-8') as output:
            output.write(text)

        print("PDF converted to text successfully.")



sys.setrecursionlimit(100000)
# Example usage
input_file = '/Users/b/Downloads/Lehninger principles of biochemistry 8th.pdf'
output_file = 'biochem chapter 1.pdf'
start_page = 99
end_page = 245

#split_pdf(input_file, output_file, start_page, end_page)

#output_text_file = 'biochem chapter 1.txt'
#convert_to_text(output_file, output_text_file)



def compare_pdf_text(input_pdf, input_text):
    differences = []

    # Read the PDF file
    with pdfplumber.open(input_pdf) as pdf:
        pdf_text = " ".join([page.extract_text() for page in pdf.pages])
    
    print(pdf_text)

    # Read the text file
    with open(input_text, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split text into sentences
    pdf_sentences = pdf_text.split(".")
    text_sentences = text.split(".")

    # Compare sentences
    matcher = difflib.SequenceMatcher(None, pdf_sentences, text_sentences)
    for tag, i, j, _, _ in matcher.get_opcodes():
        if tag == 'delete':
            differences.extend(pdf_sentences[i:j])

    return differences


def compare_text_pdf(input_pdf, input_text):
    differences = []

    # Read the PDF file
    with pdfplumber.open(input_pdf) as pdf:
        pdf_text = " ".join([page.extract_text() for page in pdf.pages])

    # Read the text file
    with open(input_text, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split text into sentences
    pdf_sentences = pdf_text.split(".")
    text_sentences = text.split(".")

    # Compare sentences
    matcher = difflib.SequenceMatcher(None, text_sentences, pdf_sentences)
    for tag, i, j, _, _ in matcher.get_opcodes():
        if tag == 'delete':
            differences.extend(text_sentences[i:j])

    return differences


# Example usage
input_pdf = 'output.pdf'
input_text = 'output.txt'
print("pass 1")
differences = compare_pdf_text(input_pdf, input_text)
for difference in differences:
    print(difference)

print("pass 2")

differences = compare_text_pdf(input_pdf, input_text)
for difference in differences:
    print(difference)


print("pass 3")