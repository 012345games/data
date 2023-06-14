"""
Multiprocessing version of Test1.py
[
Scrape search results for "io games" by search_engine + keywords_language
- 4 most popular search engines
- different languages (top 30 languages in the world)
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

import multiprocessing

RES_PER_SEARCH = 1000

def worker(id):
	"""worker function"""
	print("Starting worker %d" % (i))
	#google translate API
	translator = Translator()

	#captcha problems with Yandex, Ask.com unaccessible from desktop machine (should be available with proxy)
	engines = ["google", "baidu", "bing", "yahoo"]

	#randomize lan order to avoid collisions
	lans = [x for x in scraping.df_lan['language']]
	random.shuffle(lans)

	#search with no proxy and using different search engines and languages
	for lan in scraping.df_lan['language']:
		#randomize engine order
		random.shuffle(engines)

		for engine in engines:
			if engine+'_'+lan+'_' + str(RES_PER_SEARCH) + "__res.json" in  os.listdir("./output"):
				print("Skipping ", engine, lan)
				continue
			print(engine, lan)
			#launch search
			res = scraping.search_interface(engine, translator, n_res=RES_PER_SEARCH, language=lan)
			#dump json
			if res!=None and res!=[]: #dump results (if any)
				with open("./output/"+engine+'_'+lan+'_' + str(RES_PER_SEARCH) + "__res.json",'w', encoding='utf-8') as json_file:
					json.dump(res, json_file, ensure_ascii=False)



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
