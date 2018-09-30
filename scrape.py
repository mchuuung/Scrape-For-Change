import hashlib
import pandas as pd
import requests as req
import hashlib
import random
import time
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import urllib.request


# Read an Excel file into a pandas DataFrame
df = pd.read_excel('cryptofundurls.xlsx', sheet_name='Sheet1')
d = []
d2 = []
d3 = []
d4 = []


class ParseUrls:

    for value in df['Website URL']:  # Obtain all url's in website column
        r = req.get(value)  # Response object. Value is set to url of website
        if 'Last-Modified' in r.headers:  # Checks headers for string
            url = value
            contents = r.headers['Last-Modified']  # Sets 'contents' as modified date
            contents2 = url  # url's where website has been last modified
            d.append(contents)  # list of modified dates
            d2.append(contents2)  # list of urls
        else:
            # open excel sheet to check if hash value exists
            # df4 = pd.read_excel('pandas_openpyxl.xlsx', sheetname=0)  # can also index sheet by name or fetch all sheets
            # mylist = df['column name'].tolist()




            # if exists, then set that value to current hash, and check against new hash
            # if current hash != new hash, then replace and set new date
            h = hashlib.sha512(r.text.encode('utf-8')) # hash the web page
            h = h.hexdigest()
            url2 = value
            contents3 = url2
            contents4 = h
            d3.append(contents3) # url of hashed websites
            d4.append(h) # hashed values

    df2 = pd.DataFrame({'Website URL': d2, 'Last-Modified': d})  # df containing strings. needs website url
    df3 = pd.DataFrame({'Website URL': d3, 'Hash Value': d4})
    df_new = df.merge(df2, left_on='Website URL', right_on='Website URL', how='outer')  # requires both df to have website url
    df_new2 = df_new.merge(df3, left_on='Website URL', right_on='Website URL', how='outer')
    print(df_new2)

    #  To convert a dataframe into a worksheet highlighting the header and index:
    wb = Workbook()
    ws = wb.active

    for r in dataframe_to_rows(df_new2, index=True, header=True):
        ws.append(r)

    for cell in ws['A'] + ws[1]:
        cell.style = 'Pandas'

    wb.save("cryptofundurls")


ParseUrls()
