"""
Scrape search results for "io games" by search_engine + keywords_language
- 4 most popular search engines
- different languages (top 30 languages in the world)
"""

import googletrans
from googletrans import Translator
import scraping
import json
import os


engines = ["google", "baidu", "bing", "yahoo","ask.com"]
# engines = ["google", "baidu", "bing", "yahoo","yandex", "ask.com"] # captcha problems with ask.com and yandex

translator = Translator()
RES_PER_SEARCH = 100
lan = "telugu"


for engine in engines: #search one key word with all the search engines
    if engine+'_'+lan+"_100__res.json" in  os.listdir("./output"): # check if the result already exists
        print(" This is a message from tesSt1.py: Skipping this search because result is already present :", engine, lan)
        continue
        print(engine, lan)
    
    #go to search_interface
    res = scraping.search_interface(engine, translator, n_res=RES_PER_SEARCH, language=lan)
    print("This is what test1.py is going to dump as json")
    print(res)
    if res!=None and res!=[]: #if we get a result from search_interface save as a json file
        with open("./output/"+engine+'_'+lan+'_100_' + "_res.json",'w', encoding='utf-8') as json_file:
            json.dump(res, json_file, ensure_ascii=False)
