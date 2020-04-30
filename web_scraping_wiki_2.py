#!/usr/bin/env python3
#  web_scraping_wiki_1.py - web scraping wikipedia
# Author: octarine123
# PEP8 Style compliant according to pystylecode module
# This code is taken from JieJenn's Youtube tutorial titled "Web Scrape Wikipedia Manufacture Companies Table Into a CSV File | Web Scraping with Python"
# https://www.youtube.com/channel/UCvVZ19DRSLIC2-RUOeWx8ug
# Minor modifications have been made from JieJenn's version

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Sources
# https://en.wikipedia.org/wiki/List_of_largest_manufacturing_companies_by_revenue

def fetch():
    global table
    global rows
    global columns
    url_1 = 'https://en.wikipedia.org/wiki/List_of_largest_manufacturing_companies_by_revenue'
    response = requests.get(url_1)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable plainrowheads'}).tbody
    rows = table.find_all('tr')
    columns = [v.text.replace('\n', ' ') for v in rows[0].find_all('th')]

def process():
    df = pd.DataFrame(columns=columns)
    for i in range(1, len(rows)):
        tds = rows[i].find_all('td')

        if len(tds) == 4:
            values = [tds[0].text, tds[1].text,
                      ' ',
                      tds[2].text,
                      tds[3].text.replace('\n', '').replace('\xa0', '')
                      ]
        else:
            values = [td.text.replace('\n', '').replace('\xa0', '') for td in tds]

        df = df.append(pd.Series(values, index=columns), ignore_index=True)

        df.to_csv(r'/home/rob/Documents/Python_code/web_scrape_wikipedia' +
                  '//wiki_manf_companies.csv',
                  index=False)

def main():
    fetch()
    process()


if __name__ == "__main__":
    try:
        main()
        print('Finished')
    except KeyboardInterrupt:
        print('Program aborted.')
        raise SystemExit
