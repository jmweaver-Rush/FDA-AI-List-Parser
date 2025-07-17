import os
import re
import pandas as pd
import openpyxl
from bs4 import BeautifulSoup as bs
import requests
from pypdf import PdfReader
import random
import time

product_codes = ['QAS', 'QBS', 'QDQ', 'QFM']
custom_flag = 'Peds_Flag'
save_name = 'list_with_peds_CAD_codes.xlsx'

# Need to use openpyxl to read xlsx as pandas/csv doesn't support hyperlinks
wb = openpyxl.load_workbook('ai-ml-enabled-devices-excel.xlsx')
sheet = wb.active

data = list(sheet.iter_rows(values_only=True))

# convert to dataframe
df = pd.DataFrame(data[1:], columns=data[0])

if len(product_codes) != 0:
    df = df[df['Primary Product Code'].isin(product_codes)].reset_index()

hit_count = [None] * len(df.index)
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

                        # search Summary PDF for specific terms (NLP w/ LLM could be used here in place of regex)
                        if re.findall(r" pediatric|children", text, re.IGNORECASE):
                            hit_count[index] = 1
                        else: hit_count[index] = 0

                        # search for a more specific regex and override to 0 if not intended
                        if re.search(r'\bnot intended\b(?:\W+\w+){1,5}?\W+\bpediatric\b', text, flags=re.IGNORECASE) is not None:
                            print(str(index)+'/'+str(len(df))+': '+k_number + ', explicitly not intended')
                            hit_count[index] = -1

                        if hit_count[index] == 1:
                            print(str(index)+'/'+str(len(df))+': '+k_number + ' likely intended for pediatric or children')
                        elif hit_count[index] == 0:
                            print(str(index)+'/'+str(len(df))+': '+k_number + ', no mention')

                    except:
                        print('Cannot read PDF')
                        hit_count[index] = 999
                else:
                    print('Non-Summary document detected')
                    hit_count[index] = 999

                # Delete temporary PDF
                if os.path.exists(k_number+".pdf"):
                    os.remove(k_number+".pdf")
    else:
        print('Non-K-Sub')
        hit_count[index] = 999
    
print('Add column and save new Excel')
df.insert(len(df.columns), custom_flag, hit_count)
df.to_excel(save_name, index=False)

    







