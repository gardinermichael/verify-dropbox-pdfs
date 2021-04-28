import csv
import urllib.request
import time
import PyPDF2
import re
import pprint

with open('Donors with Links!  - Sheet1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    pp = pprint.PrettyPrinter(indent=4)
    line_count = 0
    error_list_rows = []
    error_list_full = []

    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}\n')
            line_count += 1
        else:
            line_count += 1
            # print(f'\nRow {line_count}/455: {", ".join(row)}')
            dropbox_url = row[3][:-1] + '1'
            u = urllib.request.urlopen(dropbox_url)
            data = u.read()
            u.close()

            search_string_first = row[0]
            search_string_last = row[1]
            pdf_filename = f'pdfs/{search_string_last}.{search_string_first}.pdf'

            with open(pdf_filename, "wb") as f :
                f.write(data)
            pdf = PyPDF2.PdfFileReader(pdf_filename)
            number_of_pages = pdf.getNumPages()

            for i in range(0, number_of_pages):
                page = pdf.getPage(i)
                text = page.extractText() 
                search_results_first = re.search(search_string_first, text)
                search_results_last = re.search(search_string_last, text)

                if search_results_first and search_results_last:
                    print(str(line_count) + '/455 OK')
                else:
                    print('Error on Row ' + str(line_count) + '/455')
                    error_list_rows.append(line_count)
                    error_list_full.append({
                        f'Row {line_count}': row
                    })

            # time.sleep(1)
        
    print(f'\nProcessed {line_count} lines.')
    print(f'\nError List Full:\n')
    print(error_list_rows)
    print(f'\nError List Full:\n')
    pp.pprint(error_list_full)
