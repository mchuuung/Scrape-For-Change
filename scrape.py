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





class ParseFile:

    def __init__(self, file):
        self.header_dates = []
        self.header_url = []
        self.hash_values = []
        self.hash_url = []
        self.last_modified_url = []
        self.current_date = []
        self.file = file
        self.hash_df = pd.DataFrame
        self.header_df = pd.DataFrame
        self.merge_df = pd.DataFrame
        self.final_df = pd.DataFrame

    def set_file(self, file):
        """Sets file to be parsed"""
        self.file = file
        return self.set_file

    def get_file(self):
        """Parses file that has been set"""
        df = pd.read_excel(self.file) # Read an Excel file into a pandas DataFrame
        for url in df['Website URL']:  # Obtain all url's in website column
            r = req.get(url, verify=False)  # Response object. Value is set to url of website
            if 'Last-Modified' in r.headers:  # Checks headers for string
                header_date = r.headers['Last-Modified']  # Sets 'header_date' as modified date
                website_url = url  # url's where website has been last modified
                self.header_dates.append(header_date)  # list of modified dates
                self.header_url.append(website_url)  # list of urls
            else:
                    h = hashlib.sha512(r.text.encode('utf-8')) # hash the web page
                    h = h.hexdigest()
                    self.hash_values.append(h)
                    self.hash_url.append(url)
                    self.current_date.append(datetime.datetime.now())

    def create_hash_df(self):
        self.hash_df = pd.DataFrame({'Website URL': self.hash_url, 'Last-Modified': self.current_date, "Hash-Value": self.hash_values})  # date of last modified and time
        return self.hash_df

    def create_header_df(self):
        self.header_df = pd.DataFrame({'Website URL': self.header_url, 'Last-Modified': self.header_dates})  # date of last modified and time
        return self.header_df

    def combine_df(self):
        self.merge_df = self.hash_df.astype(str).merge(self.header_df.astype(str), on=['Last-Modified', 'Website URL'], how='outer', suffixes=('_', ''))
        return self.merge_df

    def save_wb(self):
            wb = Workbook()
            ws = wb.active

            for r in dataframe_to_rows(self.merge_df, index=True, header=True):
                ws.append(r)

            for cell in ws['A'] + ws[1]:
                cell.style = 'Pandas'

            wb.save("check.xlsx")

def main():
    file = ParseFile("MasterFile.xlsx")  # instantiate class instance
    file.get_file() # Checks output
    file.create_hash_df()
    file.create_header_df()
    file.combine_df()
    file.save_wb()

    #file.save_wb()
    #file.set_file("cryptofundurls.xlsx") # Checks a new file (use for comparision of hash)
    #print(file.get_file()) # Checks output


main()
