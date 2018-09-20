import pandas as pd
from requests_html import HTMLSession
session = HTMLSession()

# Read an Excel table into a pandas DataFrame
df = pd.read_excel('cryptofundurls.xlsx', sheet_name='Sheet1', index_col=0)

# Convert the DataFrame to a dictionary
list_of_dicts = df.to_dict(orient='records')


def parse_doc():
    """Set response object. Display website url and additional links."""
    for char in list_of_dicts:
            response = session.get(char['Website URL'])
            print(response.headers)
            print(response.url, response.html.links)


parse_doc()
# From within the <ul class = 'sb-rss-feed' </ul> new <li> ... </li> then "Latest" is updated.