import pandas as pd
import requests as req
import numpy as np
import json
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


# Read an Excel file into a pandas DataFrame
df = pd.read_excel('cryptofundurls.xlsx', sheet_name='Sheet1')
df['Last-Modified'] = np.nan  # Sets all rows as empty


def parse_doc():
    """Set response object. Display website url and additional links."""
    for value in df.get('Website URL'):  # Obtain all values in website column
        r = req.head(value)
        rh = dict(r.headers)
        if 'Last-Modified' in r.headers:
            df.set_index('Last-Modified')
            # df['Last-Modified'].merge((r.headers['Last-Modified'].to_frame()), left_index=True) # Sets entire column to last date
            print(rh['Last-Modified']) # prints as dictionary
            df['Last-Modified'] = pd.DataFrame({'Last-Modified': rh})

        print(df)

            # print(json.dumps(rh)) # dumps takes an object and produces a string


    # print(df)
    # print(r.headers['Last-Modified'])

parse_doc()


# To convert a dataframe into a worksheet highlighting the header and index:
wb = Workbook()
ws = wb.active

for r in dataframe_to_rows(df, index=True, header=True):
    ws.append(r)

for cell in ws['A'] + ws[1]:
    cell.style = 'Pandas'

wb.save("pandas_openpyxl.xlsx")
