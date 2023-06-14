import re
import requests
import time
import random

REFRESH_INTERVAL_SECS = 600 #10 minutes
class FreeProxy:

    def __init__(self):
        self.proxylisturl = 'https://free-proxy-list.net/'
        self.proxylist = self.refresh_list()
        self.ts = time.time()

    def refresh_list(self):
        print("\n** Refreshing proxy list from https://free-proxy-list.net/ **\n")
        url = 'https://free-proxy-list.net/'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}
        try:
            source = str(requests.get(url, headers=headers, timeout=10).text)
            data = [list(filter(None, i))[0] for i in re.findall('<td class="hm">(.*?)</td>|<td>(.*?)</td>', source)]
            groupings = [dict(zip(['ip', 'port', 'code', 'using_anonymous'], data[i:i+4])) for i in range(0, len(data), 4)]
        except:
            print("Error while updating proxy list\n")
            return None
        return groupings

    def get_proxy(self, code):
        now = time.time()
        #periodically refresh proxy list
        if now-self.ts > REFRESH_INTERVAL_SECS:
            self.ts = now
            new_list = self.refresh_list()
            if new_list!=None:
                self.proxylist = self.refresh_list()
        #select by code, then randomly pick one
        selected_by_code = [x for x in self.proxylist if x['code']==code]
        if selected_by_code == []:
            return None
        else:
            return random.choice(selected_by_code)

if __name__ == "__main__":
    fp = FreeProxy()
    px = fp.get_proxy('US')
    print("A random proxy from US", px)
