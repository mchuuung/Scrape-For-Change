import hashlib
import pandas as pd
import requests as req
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import urllib.request

def extractHTML(url):
    f = open('temphtml.html', 'w')
    page = urllib.request.urlopen(url)
    pagetext = str(page.read())
    f.write(pagetext)
    f.close()

extractHTML('https://www.360blockchaininc.com/')





# Read an Excel file into a pandas DataFrame
# df = pd.read_excel('cryptofundurls.xlsx', sheet_name='Sheet1')
# d = []
# d2 = []
# h = hashlib.sha512("abc".encode('utf-8')) # hash the string 'abc'
# h = h.hexdigest()
# print (h)

# class ParseUrls:
#
#     for value in df['Website URL']:  # Obtain all url's in website column
#         r = req.get(value)  # Response object. Value is set to url of website
#         if 'Last-Modified' in r.headers:  # Checks headers for string
#             url = value
#             contents = r.headers['Last-Modified']  # Sets 'contents' as modified date
#             contents2 = url  # url's where website has been last modified
#             d.append(contents)  # list of modified dates
#             d2.append(contents2)  # list of urls
#         else:
#             print('Will use hash method for: ', value)
#
#             # print('r.content:', r.content) # r.content is binary, r.text is text
#
#     df2 = pd.DataFrame({'Website URL': d2, 'Last-Modified': d})  # df containing strings. needs website url
#     df_new = df.merge(df2, left_on='Website URL', right_on='Website URL',
#                       how='outer')  # requires both df to have website url














    # To convert a dataframe into a worksheet highlighting the header and index:
    # wb = Workbook()
    # ws = wb.active
    #
    # for r in dataframe_to_rows(df_new, index=True, header=True):
    #     ws.append(r)
    #
    # for cell in ws['A'] + ws[1]:
    #     cell.style = 'Pandas'
    #
    # wb.save("pandas_openpyxl.xlsx")
