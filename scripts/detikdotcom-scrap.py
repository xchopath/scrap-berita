#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json

KEYWORD = 'GANTENG'

headers = {
	'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36'
}

search = requests.get("https://www.detik.com/search/searchall?query=" + str(KEYWORD), headers=headers)

soup = BeautifulSoup(search.text, "lxml")
list_berita = soup.find_all("article")

for berita in list_berita:
	soup = BeautifulSoup(str(berita), "lxml")
	link = soup.find('a')['href']
	try:
		open_link = requests.get(link, headers=headers)
		soup = BeautifulSoup(open_link.text, "lxml")
		title = soup.find('meta', attrs={'property':'og:title'})['content']
		published = soup.find('meta', attrs={'name':'pubdate'})['content']
		author = soup.find('meta', attrs={'name':'author'})['content']
		url = soup.find('meta', attrs={'property':'og:url'})['content']
		img = soup.find('meta', attrs={'property':'og:image'})['content']
		content = soup.find("div", {"class": "itp_bodycontent"})
		content = str(content).replace("<", " <")
		content = BeautifulSoup(content, "lxml")
		content = content.text
		content = ' '.join(content.split())
		output = {"title": title, "content": content, "date": published, "author": author, "url": url, "image": img, "source": "DETIK.COM"}
		print(json.dumps(output))
	except:
		print("ERROR:", link)
