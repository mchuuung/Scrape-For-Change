import pandas as pd
from requests_html import HTMLSession
session = HTMLSession()

# Read an Excel table into a pandas DataFrame
df = pd.read_excel('cryptofundurls.xlsx', sheet_name='Sheet1')

# Convert the DataFrame to a dictionary
list_of_dicts = df.to_dict(orient='records')


def parse_doc():
    """Set response object. Display website url and additional links."""
    for item in list_of_dicts: # 23 times
        r = session.get(item['Website URL'])
        if 'Last-Modified' in r.headers: # 4 times
            for key in range(len(list_of_dicts)): # 23 times
                list_of_dicts[key].update({'Last-Modified': r.headers['Last-Modified']})
                print(list_of_dicts[key])



parse_doc()
# From within the <ul class = 'sb-rss-feed' </ul> new <li> ... </li> then "Latest" is updated.

#         else:
#             list_of_dicts[key].update({'Last-Modified': 'N/A'})
