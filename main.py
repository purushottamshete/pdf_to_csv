'''
This is a sample Program to Read a PDF file and export the content to csv
'''
import pandas as pd
import PyPDF2
import re

# Open the PDF file
pdf_file = open('example1.pdf', 'rb')

# Read the PDF content and create a list of pages
pdf_reader = PyPDF2.PdfReader(pdf_file)
pages = []
for i in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[i]
    pages.append(page.extract_text())

# Process PDF content line by line
data = []
tour = {}
for row_num, page in enumerate(pages):
    lines = page.split('\n')
    for col_num, line in enumerate(lines):
        day_line = re.search('Day [0-9]$', line)
        if day_line:
            day_num = day_line.string.split(' ')[2]
            tour['Day'] = day_num

        tour_line = re.search('^Tour', line)
        if tour_line:
            tour_name = tour_line.string.split(' ')[2:]
            tour['Tour Name'] = ' '.join(tour_name)
            
        start_time_line = re.search('Start Time:', line)
        if start_time_line:
            start_time = start_time_line.string.split(' ')[3]
            tour['Start Time'] = start_time

        end_time_line = re.search('End Time:*', line)
        if end_time_line:
            end_time = end_time_line.string.split(' ')[3]
            tour['End Time'] = end_time

        duration_line = re.search('Duration:*', line)
        if duration_line:
            duration= duration_line.string.split(' ')[2]
            tour['Duration'] = duration

        if len(tour) == 5:
            data.append(tour)
            tour={"Day": day_num}


# Create the Data Frame
# Save the Excel file
df = pd.DataFrame(data)
print(df)
df.to_csv('example1.csv', index=False)

# Close the PDF file
pdf_file.close()
