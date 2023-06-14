"""
Load html files (saved webpages from manual searches) and scrape results
Based on code from ./../scraping.py
Google only
"""

import os
from bs4 import BeautifulSoup
import requests
import json

CHROME_DEFAULT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

def __resolve_urls(url):
    try:
        #resolve url using much shorter timeout
        final_url = requests.get(url,
                                 headers={'User-Agent': CHROME_DEFAULT}, timeout=10.0).url
    except requests.RequestException:
        return url
    except requests.exceptions.Timeout:
        return url
    except ConnectionError:
        return url
    else:
        return final_url

def resolve_links(results, global_n_res):
    print("Resolving links...")
    count = 1
    for i in results:
        i['url'] = __resolve_urls(i['url'])
        i['rank'] = count+global_n_res
        count += 1
    return results

#google search html parser
def parse_html(html_file):
    print("Parsing html file", html_file, " ...")
    soup = BeautifulSoup(open(html_file), 'html.parser')
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

#scrape results from single html file
def scrape(html_file, global_n_res):
    results = []
    scrape_results = parse_html(html_file)
    for res in scrape_results:
        results.append(res)
    return {'results': resolve_links(results, global_n_res)}


if __name__ == "__main__":
    res = []
    lan = 'english'
    engine = 'google'
    n_res = 0
    #load all html files in the working directory
    for html_file in sorted([x for x in os.listdir('.') if ".html" in x]):
        res_buf = scrape(html_file, n_res)['results']
        n_res+=len(res_buf)
        res.extend(res_buf)
    #dump to json
    if res!=[]:
        with open("./../output/"+engine+'_'+lan+'_' + str(len(res)) + '_' + "_res.json",'w', encoding='utf-8') as json_file:
            json.dump(res, json_file, ensure_ascii=False)
