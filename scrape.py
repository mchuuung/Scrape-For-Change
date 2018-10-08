import pandas as pd
import requests as req
import hashlib
import datetime
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


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
        self.df = pd.DataFrame
        self.hash_frame = pd.DataFrame
        self.check_hash_against = []
        self.check_hash_url = []
        self.check_hash_date =[]
        self.checked_hash_df = pd.DataFrame
        self.current_df = pd.DataFrame

    def set_file(self, file):
        """Sets file to be parsed"""
        self.file = file
        return self.set_file

    def set_df(self):
        self.current_df = pd.read_excel(self.file)


    def get_file(self):
        """Parses initial file. Sends http request to determine if 'Last-Modified' is given.
        Appends 'Last-Modified' date if given, else sets current date and hash of website."""
        self.df = pd.read_excel(self.file) # Read an Excel file into a pandas DataFrame
        for url in self.df['Website URL']:  # Obtain all url's in website column
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

    def combine_df2(self):
        self.merge_df2 = self.df.astype(str).merge(self.merge_df.astype(str), on=[ 'Website URL'],how='left', suffixes=('_', ''))
        self.merge_df2 = self.merge_df2.drop(columns=["Last-Modified_", "Hash-Value_"])
        return self.merge_df2

    def merge_df3(self):
        self.final_df = self.merge_df2.astype(str).merge(self.checked_hash_df.astype(str), on='Hash-Value', how='left', suffixes=('_', ''))
        self.final_df = self.final_df.drop(columns=["Last-Modified_"])
        self.final_df = self.final_df.astype(str)
        return self.final_df

    def save_wb(self, save_file, use_df):
            self.save_to_file = save_file
            self.use_df = use_df
            wb = Workbook()
            ws = wb.active

            for r in dataframe_to_rows(self.use_df, index=True, header=True):
                ws.append(r)

            for cell in ws['A'] + ws[1]:
                cell.style = 'Pandas'

            wb.save(self.save_to_file)

    def check_hash(self):
        """Need to fix last mod changign even when hash values are the same.
        Also different hash values occuring, but last mod becoming 'nan' as opposed to current date. """
        self.hash_frame = pd.read_excel(self.file) # Read data into pandas DF
        for hash_val in self.hash_frame['Hash-Value']:  # Obtain all hashes in Hash-Value column
            if not hash_val != hash_val: # Where hash-value is given
                print(hash_val)
        #         self.check_hash_against.append(hash_val)
        #         self.check_hash_date.append(datetime.datetime.now())
        # 
        # self.checked_hash_df = pd.DataFrame({'Last-Modified': self.check_hash_date,"Hash-Value": self.check_hash_against})
        # return self.checked_hash_df



def main():
    file = ParseFile("MasterFile.xlsx")  # instantiate class instance
    file.get_file()
    file.create_hash_df()
    file.create_header_df()
    file.combine_df()
    # file.save_wb("check.xlsx", file.merge_df)
    # file.set_file("check.xlsx")
    file.combine_df2()
    # file.save_wb("check3.xlsx", file.merge_df2) # master unaffected till here
    file.set_file("MasterFile.xlsx") # current working file
    file.check_hash() # Checks current hash value from MasterFile
    file.merge_df3() # Merges checkfile with masterfile into official list
    file.save_wb('OfficialList.xlsx', file.final_df)




    #file.save_wb()
    #file.set_file("cryptofundurls.xlsx") # Checks a new file (use for comparision of hash)
    #print(file.get_file()) # Checks output


main()
