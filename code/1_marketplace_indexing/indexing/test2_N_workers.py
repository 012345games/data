"""
Multiprocessing version of Test2.py
[
Scrape search results for "io games" by search_engine + geolocation
- 5 most popular search engines
- different geolocations using proxies from Free Proxy List
]
"""

import json
import os
import pandas as pd
import sys
import random
import time

import googletrans
from googletrans import Translator

import scraping
import free_proxy_list_if #provide proxies from the Free Proxy List website

import multiprocessing


def worker(id):
	"""worker function"""
	print("Starting worker %d" % (i))
	#google translate API
	translator = Translator()
	#interface with Free Proxy List
	proxy_getter = free_proxy_list_if.FreeProxy()

	#captcha problems with Yandex, Ask.com unaccessible from desktop machine (should be available with proxy)
	#engines = ["google", "baidu", "bing", "yahoo", "ask.com"]
	engines = ["google"]
	RES_PER_SEARCH = 500

	#search from different proxy locations and on different search engines
	while True:
		#retrieve country codes (quite at random, from available proxies)
		df_px = pd.DataFrame(proxy_getter.proxylist)
		country_code_set = df_px[ df_px['code'].str.isalpha() ]['code'].unique()
		random.shuffle(country_code_set)

		#iterate on proxy country codes and search engines
		for proxy_country in country_code_set:
			for engine in engines:
				if engine+'_proxy' + proxy_country +'_'+ str(RES_PER_SEARCH) + "__res.json" in  os.listdir("./output2-v2"):
					print("Skipping ", engine, proxy_country)
					continue
				#launch search
				res = scraping.search_interface(engine, translator, n_res=RES_PER_SEARCH, proxy_if=proxy_getter, proxy_code=proxy_country)
				#dump json
				if res!=None and res!=[]: #dump results (if any)
					with open("./output2-v2/"+engine+'_proxy' + proxy_country +'_'+ str(RES_PER_SEARCH) + "__res.json",'w', encoding='utf-8') as json_file:
						json.dump(res, json_file, ensure_ascii=False)
	return


if __name__ == '__main__':
	if len(sys.argv)!=2:
		sys.exit("Error: missing number of workers")
	n_workers = int(sys.argv[1])
	jobs = []
	for i in range(n_workers):
	    p = multiprocessing.Process(target=worker, args=(i,))
	    jobs.append(p)
	    p.start()

	while True:
		try:
			time.sleep(2.0)
		except KeyboardInterrupt:
			print("\nTerminating (stopping all workers)\n")
			for job in jobs:
				job.terminate()
			sys.exit()
