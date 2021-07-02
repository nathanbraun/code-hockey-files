from bs4 import BeautifulSoup as Soup

table_html = """
<html>
  <table>
    <tr>
     <th>Name</th>
     <th>Date</th>
     <th>Team</th>
     <th>Opp</th>
     <th>Shots</th>
     <th>Goals</th>
    </tr>
    <tr>
     <th>Sidney Crosby</th>
     <th>2019-10-03</th>
     <th>PIT</th>
     <th>BUF</th>
     <th>4</th>
     <th>1</th>
    </tr>
    <tr>
     <td>Alexander Ovechkin</td>
     <td>2019-10-05</td>
     <th>WAS</th>
     <th>CAR</th>
     <th>9</th>
     <th>2</th>
    </tr>
  </table>
<html>
"""

html_soup = Soup(table_html)

tr_tag = html_soup.find('tr')
tr_tag
type(tr_tag)

table_tag = html_soup.find('table')
type(table_tag)

td_tag = html_soup.find('td')
td_tag
type(td_tag)

td_tag
td_tag.string
str(td_tag.string)

tr_tag.find_all('th')

[str(x.string) for x in tr_tag.find_all('th')]

all_td_tags = table_tag.find_all('td')
all_td_tags

all_rows = table_tag.find_all('tr')
first_data_row = all_rows[1]  # 0 is header
first_data_row.find_all('td')

all_td_and_th_tags = table_tag.find_all(('td', 'th'))
all_td_and_th_tags

[str(x.string) for x in all_td_tags]

all_rows = table_tag.find_all('tr')
list_of_td_lists = [x.find_all('td') for x in all_rows[1:]]
list_of_td_lists
