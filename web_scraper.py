import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

import pypdf2
from urllib2 import Request, urlopen
from pyPdf import PdfFileWriter, PdfFileReader
from StringIO import StringIO

def get_report(url):
    response = requests.get(url)
    page = BeautifulSoup(response.text, 'html.parser')
    
    try:
        doc_base = 'http://documents.worldbank.org'
        doc_path = page.find('li', class_ = 'textdoc').find('a').attrs['href']
        doc_url = doc_base + doc_path
        
        response = requests.get(doc_url)
        page = BeautifulSoup(response.text, 'html.parser')
        return page.getText()
    
    except:
        return ''

# Start from the Main Web Page of the Integrity Vice Presidency (INT)
base_url = 'http://www.worldbank.org/en/about/unit/integrity-vice-presidency/redacted-investigation-reports'
response = requests.get(base_url)
page = BeautifulSoup(response.text, 'html.parser')

div_list = page.find_all('div', id = 'n02v11-content')

list_of_reports = []

# Loop over all the months, for which reports made publicly available\n",
for div in div_list:
    reporting_month = div.find('h4', class_ = 'sub mrg-b-3').text
    
    # Loop Over all the reports published in the particular month\n",
    for a in div.find_all('a'):
        next_url = a.attrs['href']

        # Get relevant project information into a dictionary\n",
        d = {}
        d['project'] = a.text
        d['report']  = get_report(next_url)

        # Append the relevant project information to the larger list\n",
        list_of_reports.append(d)

# Final DataFrame with the Project Name and text of the Project Investigation Report
df_reports = pd.DataFrame(list_of_reports)
