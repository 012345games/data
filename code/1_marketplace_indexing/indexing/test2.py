"""
Scrape search results for "io games" by search_engine + geolocation
- 5 most popular search engines
- different geolocations using proxies from Free Proxy List
"""

import json
import os
import pandas as pd
import sys

import googletrans
from googletrans import Translator

import scraping
import free_proxy_list_if #provide proxies from the Free Proxy List website

N_WORKERS = 10

#google translate API
translator = Translator()

#interface with Free Proxy List
proxy_getter = free_proxy_list_if.FreeProxy()

#captcha problems with Yandex, Ask.com unaccessible from desktop machine (should be available with proxy)
engines = ["google", "baidu", "bing", "yahoo", "ask.com"]
RES_PER_SEARCH = 100

#search from different proxy locations and on different search engines
while True:
	try:
		#retrieve country codes (quite at random, from available proxies)
		df_px = pd.DataFrame(proxy_getter.proxylist)
		country_code_set = df_px[ df_px['code'].str.isalpha() ]['code'].unique()

		#iterate on proxy country codes and search engines
		for proxy_country in country_code_set:
			for engine in engines:
				if engine+'_proxy' + proxy_country +'_100_' + "_res.json" in  os.listdir("./output2"):
					print("Skipping ", engine, proxy_country)
					continue

				res = scraping.search_interface(engine, translator, n_res=RES_PER_SEARCH, proxy_if=proxy_getter, proxy_code=proxy_country)
				if res!=None: #dump results (if any)
					with open("./output2/"+engine+'_proxy' + proxy_country +'_100_' + "_res.json",'w', encoding='utf-8') as json_file:
						json.dump(res, json_file, ensure_ascii=False)
	except KeyboardInterrupt:
		print("\nTerminating...\n")
		sys.exit()
