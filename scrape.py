import hashlib
import pandas as pd
import requests as req
import hashlib
import numpy
import random
import datetime
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import urllib.request
from functools import reduce


# Read an Excel file into a pandas DataFrame
df = pd.read_excel('cryptofundurls.xlsx', sheet_name='Sheet')
last_modified_dates = []
last_modified_websites = []
d3 = []
d4 = []
d5 = []
f_name = []

class ParseUrls:

    for value in df['Website URL']:  # Obtain all url's in website column
        r = req.get(value, verify=False)  # Response object. Value is set to url of website
        if 'Last-Modified' in r.headers:  # Checks headers for string
            contents = r.headers['Last-Modified']  # Sets 'contents' as modified date
            website_url = value  # url's where website has been last modified
            last_modified_dates.append(contents)  # list of modified dates
            last_modified_websites.append(website_url)  # list of urls
        else:
                h = hashlib.sha512(r.text.encode('utf-8')) # hash the web page
                h = h.hexdigest()
                d4.append(h)
                contents3 = value
                d3.append(contents3)
                d5.append(datetime.datetime.now())




    df4 = pd.DataFrame({'Website URL': d3, 'Last-Modified': d5})  # date of last modified and time


    last_modified_df = pd.DataFrame({'Website URL': last_modified_websites, 'Last-Modified': last_modified_dates})  # df containing strings. needs website url

    new_df = df.astype(str).merge(last_modified_df.astype(str), on=['Website URL'], how='inner', suffixes=('_', ''))
    final_df = new_df.astype(str).merge(df4.astype(str), on=['Last-Modified','Website URL'], how='outer', suffixes=('_', ''))  # inplace=True. good

    print(final_df)# screenshot 2


    #  To convert a dataframe into a worksheet highlighting the header and index:
    # wb = Workbook()
    # ws = wb.active
    #
    # for r in dataframe_to_rows(final_df, index=True, header=True):
    #     ws.append(r)
    #
    # for cell in ws['A'] + ws[1]:
    #     cell.style = 'Pandas'
    #
    # wb.save("cryptofundurls.xlsx")


ParseUrls()
