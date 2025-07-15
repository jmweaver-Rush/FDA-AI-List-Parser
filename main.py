import os
import re
import pandas as pd
import openpyxl
from bs4 import BeautifulSoup as bs
import requests
from pypdf import PdfReader
import random
import time

# Need to use openpyxl to read xlsx as pandas/csv doesn't support hyperlinks
wb = openpyxl.load_workbook('ai-ml-enabled-devices-excel.xlsx')
sheet = wb.active

data = list(sheet.iter_rows(values_only=True))

# convert to dataframe
df = pd.DataFrame(data[1:], columns=data[0])

peds_count = [None] * len(df.index)
for index, row in df.iterrows():
    
    #extract hyperlink url and submission k-number
    url = row['Submission Number'].split('"')[1]
    k_number = row['Submission Number'].split('"')[-2]

    # sleep to avoid accessing too many pages too quickly (temp block)
    time.sleep(random.uniform(1, 2))

    # access webpage, parse with BeautifulSoup, find all links
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    links = soup.find_all('a')

    # From all links, check for PDF link and download
    # Summary PDF *should* be the only PDF on each page
    if k_number.startswith('K'):
        for link in links:
            if ('.pdf' in link.get('href', [])):
                if link.get_text() == 'Summary':

                    # Get response object for link
                    time.sleep(random.uniform(1, 2))
                    response = requests.get(link.get('href'))

                    # Write content in PDF file
                    pdf = open(k_number+".pdf", 'wb')
                    pdf.write(response.content)
                    pdf.close()

                    # try loop in case of corrupt PDF
                    try:
                        reader = PdfReader(k_number+".pdf")
                        text = ""

                        for page in reader.pages:
                            text += page.extract_text()

                        # NLP w/ LLM could be used here in place of regex

                        # search Summary PDF for specific terms
                        if re.findall(r" pediatric|children", text, re.IGNORECASE):
                            print(str(index)+'/'+str(len(df))+': '+k_number + ' mentions pediatric or children')
                            peds_count[index] = 1
                        else:
                            print(str(index)+'/'+str(len(df))+': '+k_number + ', no peds')
                            peds_count[index] = 0
                    except:
                        print('Cannot read PDF')
                        peds_count[index] = 999
                else:
                    print('Non-Summary document detected')
                    peds_count[index] = 999

                # Delete temporary PDF
                if os.path.exists(k_number+".pdf"):
                    os.remove(k_number+".pdf")
    else:
        print('Non-K-Sub')
        peds_count[index] = 999
    
print('Add column and save new Excel')
df.insert(len(df.columns), 'Peds_Flag', peds_count)
df.to_excel('list_with_peds.xlsx', index=False)

    







