"""
A collection of classes and interfaces for scraping search results
Currently supported:
    Google
    Baidu
    Bing
    Yahoo
    Ask.com (limited)
Include translation of search keywords
Fetch proxy from Free Proxy List based on Country-Code
"""

from bs4 import BeautifulSoup
from time import sleep
import logging
import requests
import re


import googletrans
from googletrans import Translator

import pandas as pd

CHROME_DEFAULT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

# CHROME_DEFAULT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

N_EMPTY_THRESH = 10 #stop if no results after 10 iterations
# KEYWORDS = "io games"
# KEYWORDS = "free webgames"
KEYWORDS = "online kids games"
# KEYWORDS = "browser games"
# KEYWORDS = "free online games"

#top 30 languages in the world
df_lan =  pd.DataFrame([{'language': 'chinese', 'code':'zh-cn'},
                {'language': 'english', 'code':'en'},
                {'language': 'spanish', 'code':'es'},
                {'language': 'french', 'code':'fr'},
                {'language': 'hindi', 'code':'hi'},
                {'language': 'arabic', 'code':'ar'},
                {'language': 'bengali', 'code':'bn'},
                {'language': 'portuguese', 'code':'pt'},
                {'language': 'russian', 'code':'ru'},
                {'language': 'japanese', 'code':'ja'},
                {'language': 'punjabi', 'code':'pa'},
                {'language': 'indonesian', 'code':'id'},
                {'language': 'german', 'code':'de'},
                {'language': 'korean', 'code':'ko'},
                {'language': 'vietnamese', 'code':'vi'},
                {'language': 'telugu', 'code':'te'},
                {'language': 'marathi', 'code':'mr'},
                {'language': 'tamil', 'code':'ta'},
                {'language': 'urdu', 'code':'ur'},
                {'language': 'italian', 'code':'it'},
                {'language': 'turkish', 'code':'tr'},
                {'language': 'persian', 'code':'fa'},
                {'language': 'gujarati', 'code':'gu'},
                {'language': 'polish', 'code':'pl'},
                {'language': 'ukrainian', 'code':'uk'},
                {'language': 'malayalam', 'code':'ml'},
                {'language': 'kannada', 'code':'kn'},
                {'language': 'thai', 'code':'th'},
                {'language': 'romanian', 'code':'ro'},
                {'language': 'serbian', 'code':'sr'},
                {'language': 'dutch', 'code':'nl'}])


# a generic search bot
class SearchBot:

    def __init__(self, search_term, n_res, proxy=None, timeout=30,
                 user_agent=CHROME_DEFAULT, delay=0):
        self.proxy = proxy
        self.search_term = search_term.rstrip(' ')
        self.res_count = n_res
        self.timeout = timeout
        self.user_agent = user_agent
        self.delay = delay

    def bot_request(self, url):
        if self.proxy!=None:
            print("Url: " + url + " Proxy=" + self.proxy)
        else:
            print("Url: " + url + " No proxy")
        try:
            res = requests.get(url, timeout=30, proxies={'https': self.proxy, 'http': self.proxy},
                               headers={'User-Agent': self.user_agent})
            res.raise_for_status()
        except requests.HTTPError:
            logging.warning('Search page return non-200 status code (%d)' % (res.status_code))
            return None
        except requests.exceptions.Timeout:
            logging.warning('Timeout exceeded')
            return None
        except requests.exceptions.TooManyRedirects:
            logging.warning('Too many redirects')
            return None
        except requests.RequestException:
            logging.warning('Issue retrieving results page')
            return None
        except ConnectionError:
            logging.warning('Connection Error')
            return None
        else:
            print("200 OK. Inspecting HTML (%d KB) ..." % (len(res.text)/1000.0))
            return res

    def __resolve_urls(self, url):
        try:
            #resolve url using much shorter timeout
            final_url = requests.get(url, proxies={'http': self.proxy, 'https': self.proxy},
                                     headers={'User-Agent': self.user_agent}, timeout=self.timeout/10.0).url
        except requests.RequestException:
            return url
        except requests.exceptions.Timeout:
            return url
        except ConnectionError:
            return url
        else:
            return final_url

    def resolve_links(self, results):
        count = 1
        for i in results:
            i['url'] = self.__resolve_urls(i['url'])
            i['rank'] = count
            count += 1
        return results


class BaiduBot(SearchBot):
    def __init__(self, search_term, n_res, proxy=None, timeout=30,
                 user_agent=CHROME_DEFAULT, delay=0):
        super().__init__(search_term, n_res, proxy, timeout=30,
                 user_agent=CHROME_DEFAULT, delay=0)
        self.base_url = 'https://www.baidu.com/s?wd={}&pn={}'

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
#         print(soup.prettify())
        result_containers = soup.find_all('div', {'class': 'c-container'})
        print(soup.prettify())
        results = []
        for result in result_containers:
            title = result.find('h3', {'class': 't'}).get_text()
            url = result.find('a', href=True)['href']
            description = result.find('div', {'class':'c-abstract'})
            if description:
                description = description.get_text()
            results.append({'title': title, 'url': url, 'description': description})
        return results

    def scrape(self):
        results = []
        n_res = 0
        n_empty_res = 0
        while n_res < self.res_count and n_empty_res < N_EMPTY_THRESH:
            html = self.bot_request(self.base_url.format(self.search_term.replace(' ', '%20'), n_res))
            if html==None:
                n_empty_res+=1
                continue #something wrong has occurred
            scrape_results = self.parse_html(html.text)
            for res in scrape_results:
                results.append(res)
            n_res+=len(scrape_results)
            if len(scrape_results)==0:
                n_empty_res+=1
        print("Resolving links...")
        return {'results': self.resolve_links(results)}



class BingBot(SearchBot):
    def __init__(self, search_term, n_res, proxy=None, timeout=30,
                 user_agent=CHROME_DEFAULT, delay=0):
        self.base_url = 'http://www.bing.com/search?q={}&first={}'
        super().__init__(search_term, n_res, proxy, timeout=30,
                 user_agent=CHROME_DEFAULT, delay=0)


    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.prettify())
        result_containers = soup.find_all('li', {'class': 'b_algo'})
#         print(result_containers)
        results = []
        for result in result_containers:
            title = result.find('h2').get_text()
#             print(title)
            url = result.find('a', href=True)['href']
            description = result.find('div', {'class':'c-abstract'})
            if description:
                description = description.get_text()
            results.append({'title': title, 'url': url, 'description': description})
        return results

    def scrape(self):
        results = []
        n_res = 0
        n_empty_res = 0
        while n_res < self.res_count and n_empty_res < N_EMPTY_THRESH: 
            html = self.bot_request(self.base_url.format(self.search_term.replace(' ', '+'), n_res))
            if html==None:
                n_empty_res+=1
                continue #something wrong has occurred
            scrape_results = self.parse_html(html.text)
            for res in scrape_results:
                results.append(res)
            n_res+=len(scrape_results)  # here I am setting the next 10 results , n_res is not incrementing one by one
            if len(scrape_results)==0:
                n_empty_res+=1
        return {'results': self.resolve_links(results)}


class YahooBot(SearchBot):
    def __init__(self, search_term, n_res, proxy=None, timeout=30,
                 user_agent=CHROME_DEFAULT, delay=0):
        self.base_url = 'http://www.search.yahoo.com/search?q={}&b={}'
        super().__init__(search_term, n_res, proxy, timeout=30,
                 user_agent=CHROME_DEFAULT, delay=0)


    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.prettify())
        result_containers = soup.find_all('div', {'class': 'dd algo algo-sr Sr'})
        results = []
        for r in result_containers:
            url_container = r.find('span', {'class': 'fz-ms fw-m fc-12th wr-bw lh-17'})
            if url_container:
                url = url_container.get_text()
                description_container = r.find('p', {'class': 'lh-16'})
                if description_container:
                    description = description_container.get_text()
                title_container = r.find('a', {'class': "ac-algo fz-l ac-21th lh-24"})
                if title_container:
                    title = title_container.get_text()
                    if "http%3a%2f%2f"+url in title_container['href']:
                        url="http://"+url
                    if "https%3a%2f%2f"+url in title_container['href']:
                        url="https://"+url
                results.append({'title': title, 'url': url, 'description': description})
        return results

    def scrape(self):
        results = []
        n_res = 0
        n_empty_res = 0
        while n_res < self.res_count and n_empty_res < N_EMPTY_THRESH:
            html = self.bot_request(self.base_url.format(self.search_term.replace(' ', '+'), n_res))
            if html==None:
                n_empty_res+=1
                continue #something wrong has occurred
            scrape_results = self.parse_html(html.text)
            for res in scrape_results:
                results.append(res)
            n_res+=len(scrape_results)
            if len(scrape_results)==0:
                n_empty_res+=1
        return {'results': self.resolve_links(results)}


class GoogleBot(SearchBot): # passing a super class as an argument
    def __init__(self, search_term, n_res, proxy=None, timeout=30,
                 user_agent=CHROME_DEFAULT, delay=0):
        self.base_url = 'http://www.google.com/search?q={}&num={}'
        self.num_results = n_res
        super().__init__(search_term, n_res, proxy, timeout=30,
                 user_agent=CHROME_DEFAULT, delay=0)


    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.prettify())
        result_containers = soup.find_all('div', attrs = {'class': 'g'})
        results = []
        url_list = []
        for r in result_containers:
            url_container = r.find('div', attrs = {'class': 'r'})
            if url_container:
                url = url_container.find('a', href = True)['href']
                title = url_container.find('h3')
                if title:
                    title = title.get_text()
            description_container = r.find('div', attrs = {'class': 's'})
            if description_container:
                description = description_container.find('div')
                if description:
                    description = description.get_text()
                if url and url not in url_list:
                    results.append({'title': title, 'url': url, 'description': description})
                    url_list.append(url)
        return results
        

    def scrape(self):
        results = []
        html = self.bot_request(self.base_url.format(self.search_term.replace(' ', '+'), self.res_count))
        if html==None:
            return [] #something wrong has occurred
        scrape_results = self.parse_html(html.text)
        for res in scrape_results:
            results.append(res)
        return {'results': self.resolve_links(results)}

#captcha problems here :(
class YandexBot(SearchBot):
    def __init__(self, search_term, n_res, proxy=None, timeout=30,
                 user_agent=CHROME_DEFAULT, delay=0):
        self.base_url = 'http://yandex.ru/search/?text={}&p={}'
        super().__init__(search_term, n_res, proxy, timeout=30,
                 user_agent=CHROME_DEFAULT, delay=0)


    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.prettify())
        result_containers = soup.find_all('li', {'class': 'b_algo'})
        results = []
        for result in result_containers:
            title = result.find('h2').get_text()
            url = result.find('a', href=True)['href']
            description = result.find('div', {'class':'c-abstract'})
            if description:
                description = description.get_text()
            results.append({'title': title, 'url': url, 'description': description})
        return results

    def scrape(self):
        results = []
        n_res = 0
        n_empty_res = 0
        while n_res < self.res_count and n_empty_res < N_EMPTY_THRESH:
            html = self.bot_request(self.base_url.format(self.search_term.replace(' ', '+'), n_res))
            if html==None:
                n_empty_res+=1
                continue #something wrong has occurred
            scrape_results = self.parse_html(html.text)
            for res in scrape_results:
                results.append(res)
            n_res+=len(scrape_results)
            if len(scrape_results)==0:
                n_empty_res+=1
        return {'results': self.resolve_links(results)}


class AskComBot(SearchBot):
    def __init__(self, search_term, n_res, proxy=None, timeout=30,
                 user_agent=CHROME_DEFAULT, delay=0):
        self.base_url = 'http://ask.com/web?q={}&page={}'
        super().__init__(search_term, n_res, proxy, timeout=30,
                 user_agent=CHROME_DEFAULT, delay=0)


    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.prettify())
        result_containers = soup.find_all('div', {'class': 'PartialSearchResults-item-title'})
        results = []
        title = None
        description = None
        for result in result_containers:
            url = result.find('a')['href']
            title = result.get_text()
            description_container = result.find('p', {'class' :"PartialSearchResults-item-abstract"})
            if description_container:
                description_container.get_text()
            if url:
                results.append({'title': title, 'url': url, 'description': description})
        return results

    def scrape(self):
        results = []
        i = 0
        n_res = 0
        n_empty_res=0
        while n_res < self.res_count and n_empty_res < N_EMPTY_THRESH:
            html = self.bot_request(self.base_url.format(self.search_term.replace(' ', '%20'), i))
            if html==None:
                n_empty_res+=1
                continue #something wrong has occurred
            scrape_results = self.parse_html(html.text)
            for res in scrape_results:
                results.append(res)
            n_res+=len(scrape_results)
            if len(scrape_results)==0:
                n_empty_res+=1
            i+=1
        return {'results': self.resolve_links(results)}


def search_interface(search_engine, translator, n_res=1, default_key=KEYWORDS, language="english", proxy_if=None, proxy_code=None):
    #STEP1
    # if language is not english change the search keywords [iogames, free online games, free web games, free browser games]   language from df_lang defined above, you can add more languages and their codes as well; 31 languages for now
    if language!="english":
        search_word = translator.translate(default_key,
                                           src='en',
                                           dest=df_lan[df_lan['language']==language]['code'].values[0]).text
    else:
        search_word = default_key # if language is english the search keyword will be defualt word

    #STEP2
    # set proxy as requestes by user only for seraches based on location
    http_proxy=None
    if proxy_if!=None and proxy_code!=None:
        proxy = proxy_if.get_proxy(proxy_code)
        if proxy!=None:
            http_proxy = 'http://' + proxy['ip'] + ':' + proxy['port']
            print("Proxy enabled (%s) : %s" % (proxy_code, http_proxy))
        else:
            print("Cannot find any proxy with country code %s. Skipping" % (proxy_code))
            return []
    else:
        print("Proxy disabled") # for searches by languages

    #start search
    if http_proxy!=None:
        print("Search <<" + search_word + ">> with " + search_engine + " (" + str(n_res) + " results) Proxy:" + http_proxy)
    else:
        print("Search <<" + search_word + ">> with " + search_engine + " (" + str(n_res) + " results) No proxy") # lang search
    if search_engine == "ask.com":
        s = AskComBot(search_word, n_res, proxy=http_proxy) # generating a class instance
    elif search_engine == "baidu":
        s = BaiduBot(search_word, n_res, proxy=http_proxy)
    elif search_engine == "google":
        s = GoogleBot(search_word, n_res, proxy=http_proxy)
    elif search_engine == "bing":
        s = BingBot(search_word, n_res, proxy=http_proxy)
    elif search_engine == "yahoo":
        s = YahooBot(search_word, n_res, proxy=http_proxy)
    elif search_engine == "yandex":
        s = YandexBot(search_word, n_res, proxy=http_proxy)
    
    
    res = s.scrape() #instance uses local scrape function with passon on search _word and proxy

    if res == []:
        return None #something went wrong
    return res.get('results')
