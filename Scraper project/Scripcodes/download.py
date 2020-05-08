import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError
import re
import itertools
from string import ascii_lowercase

def download(url,user_agent='wswp',tries=1):
    print('Downloading... {}'.format(url))
    request=urllib.request.Request(url)
    request.add_header('User-agent',user_agent)
    ctr=0
    while (ctr<tries):
        try:
            html=urllib.request.urlopen(url).read()
            return str(html)
        except (URLError, HTTPError, ContentTooShortError) as e:
            print('Error: {} (try: {})'.format(e.reason,ctr+1))
            if hasattr(e,'code') and 500<=e.code<600:
                ctr+=1
                continue
            break

def search_codes(url):
    html=str(download(url))
    k=re.findall(r'<td>(\d\d\d\d\d\d)</td>',html)
    return k