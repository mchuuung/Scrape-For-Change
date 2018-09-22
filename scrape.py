import pandas as pd
import requests as req
import numpy as np
import openpyxl

# Read an Excel file into a pandas DataFrame
df = pd.read_excel('cryptofundurls.xlsx', sheet_name='Sheet1')
df['Last-Modified'] = np.nan  # Sets all rows as empty
d = []
d2 = []


for value in df['Website URL']:  # Obtain all url's in website column
    r = req.get(value) # Response object
    if 'Last-Modified' in r.headers: # Checks headers for string
        url = value
        # print(url) # url's where website has been last modified
        contents = r.headers['Last-Modified'] # Sets 'contents' as modified date
        contents2 = url # url's where website has been last modified
        d.append(contents) # list of modified dates
        d2.append(contents2) # list of urls
df2 = pd.DataFrame({'Website URL': d2, 'Last-Modified': d})  # df containing strings. needs website url
# print(df2)
# df['Last-Modified'] = pd.Series(d) # adds column based upon index that started at 0
df_new = df.merge(df2, left_on='Website URL', right_on='Website URL', how='outer')  # requires both df to have website url
print (df_new)
# print(r.headers)









# To convert a dataframe into a worksheet highlighting the header and index:
# wb = Workbook()
# ws = wb.active
#
# for r in dataframe_to_rows(df, index=True, header=True):
#     ws.append(r)
#
# for cell in ws['A'] + ws[1]:
#     cell.style = 'Pandas'
#
# wb.save("pandas_openpyxl.xlsx")
