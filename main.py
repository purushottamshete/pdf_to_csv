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
        #sheet.cell(row=row_num+1, column=col_num+1, value=line)
        #print(line)
        day_line = re.search('Day [0-9]$', line)
        if day_line:
            #print(day_line.string)
            day_num = day_line.string.split(' ')[2]
            #print(f'Day: {day_num}')
            tour['Day'] = day_num

        tour_line = re.search('^Tour', line)
        if tour_line:
            #print(tour_line.string)
            tour_name = tour_line.string.split(' ')[2:]
            #print(f"Tour Name: {' '.join(tour_name)}")
            tour['Tour Name'] = " ".join(tour_name)
            
        start_time_line = re.search('Start Time:', line)
        if start_time_line:
            #print(start_time_line.string.split(' '))
            start_time = start_time_line.string.split(' ')[3]
            #print(f"Start Time: {start_time}")
            tour['Start Time'] = start_time

        end_time_line = re.search('End Time:*', line)
        if end_time_line:
            #print(end_time_line.string)
            end_time = end_time_line.string.split(' ')[3]
            #print(f"End Time: {end_time}")
            tour['End Time'] = end_time

        duration_line = re.search('Duration:*', line)
        if duration_line:
            #print(duration_line.string)
            duration= duration_line.string.split(' ')[2]
            #print(f"Duration: {duration}")
            tour['Duration'] = duration


        if len(tour) == 5:
            #print('writing to to the list')
            tour = {
                "Day": day_num,
                "Tour Name": tour_name,
                "Start Time": start_time,
                "End Time": end_time,
                "Duration" : duration,
            }
            data.append(tour)
            tour={"Day": day_num}


# Create the Data Frame
# Save the Excel file
df = pd.DataFrame(data)
print(df)
df.to_csv('example1.csv', index=False)

# Close the PDF file
pdf_file.close()
