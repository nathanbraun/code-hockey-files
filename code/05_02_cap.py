from bs4 import BeautifulSoup as Soup
import requests
from pandas import DataFrame

response = requests.get('https://www.hockeybuzz.com/cap-central/')

print(response.text)

soup = Soup(response.text)

# soup is a nested tag, so call find_all on it
tables = soup.find_all('table')

len(tables)

# 6 of them, need to play around to find the one we want
cap_table = tables[3]  # it's this one

# cap_table another nested tag, so call find_all again
rows = cap_table.find_all('tr')

# this is a header row
rows[0]

# data rows
first_data_row = rows[1]
first_data_row

# get columns from first_data_row
first_data_row.find_all('td')

# comprehension to get raw data out -- each x is simple tag
[str(x.string) for x in first_data_row.find_all('td')]

# put it in a function
def parse_row(row):
    """
    Take in a tr tag and get the data out of it in the form of a list of
    strings.
    """
    return [str(x.string) for x in row.find_all('td')]

# call function
list_of_parsed_rows = [parse_row(row) for row in rows[1:]]

# put it in a dataframe
df = DataFrame(list_of_parsed_rows)
df.head()

# clean up formatting
df.columns = ['team', 'forwards', 'defense', 'goalies', 'signed', 'needed',
              'payroll', 'cap', 'space', 'space_per_player']

df.head()

# could do
df['cap'].head()
df['cap'] = df['cap'].str.replace('$','').str.replace(',','')
df['cap'].head()

# that's fine - but should be on lookout for better ways

# start over, get rid of , and $ when scraping

def parse_row_plus(row):
    """
    Take in a tr tag and get the data out of it in the form of a list of
    strings.
    """
    return [str(x.string)
            .replace('$','')
            .replace(',','') for x in row.find_all('td')]

df2 = DataFrame([parse_row_plus(row) for row in rows[1:]])
df2.columns = ['team', 'forwards', 'defense', 'goalies', 'signed', 'needed',
               'payroll', 'cap', 'space', 'space_per_player']

df2.head()

# error
# df2['payroll']/1000000

int_cols = [x for x in df2.columns if x != 'team']

df2[int_cols] = df2[int_cols].astype(int)

df2['payroll'].head()/1000000

