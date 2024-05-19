
from datetime import date
from bs4 import BeautifulSoup
import urllib.request

# functions taken from an open-source GitHub repository:
# https://github.com/garyherd/web-scraping-iso-prices/tree/master


def get_soup_obj(url):
    with urllib.request.urlopen(url) as response:
        html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def format_price(price_str):
    return '{0:.2f}'.format(float(price_str))


def get_NYISO_prices():
    prices = []
    url = 'http://mis.nyiso.com/public/htm/damlbmp/' + \
          str(date.today()).replace('-', '', 2) + 'damlbmp_zone.htm'
    try:
        soup = get_soup_obj(url)
    except:
        return prices

    target_rows = soup.body.table.find_next('table')\
        .find_next('table').select('tr[valign="top"]')

    for row in target_rows:
        columns = row.select('td')
        first_column_contents = columns[0].font.contents
        last_column_contents = columns[-1].font.contents
        if re.match(r'[A-Z]+', first_column_contents[0]):
            prices.append((first_column_contents[0], format_price(last_column_contents[0])))

    return prices