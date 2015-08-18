import re
import pandas as pd
from bs4 import BeautifulSoup
import mechanize

data = pd.read_csv('goodreads_bestsellers.csv')

for rownum, row in data.iterrows():
	print row['url']
	br = mechanize.Browser()
	r = br.open(row['url'])
	soup = BeautifulSoup(r.read(), 'html.parser')
	pages = soup.find(itemprop="numberOfPages").get_text()
	print pages
	data.loc[rownum, 'Pages'] = pages


data.to_csv('goodreads_bestsellers.csv', index = False)
