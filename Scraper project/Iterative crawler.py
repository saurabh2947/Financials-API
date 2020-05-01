import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError
import re
import itertools

def download(url, user_agent='wswp', num_retries=2,charset='utf-8'):
    print('Downloading:',url)
    request=urllib.request.Request(url)
    request.add_header('User-agent',user_agent)
    try:
        resp=urllib.request.urlopen(url)
        cs=resp.headers.get_content_charset()
        if not cs:
            cs=charset
        html=resp.read().decode(cs)
    except(URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:',e.reason)
        html=None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html
def crawl_site(url,max_errors=10):
    for page in itertools.count(1):
        pg_url='{}{}'.format(url,page)
        html=download(pg_url,5)
        if html is None:
            num_errors+=1
            print("Reached nothing page {}".format(num_errors))
            if num_errors==max_errors:
                break
            else:
                num_errors=0
def crawl_sitemap(url):
    sitemap=download(url)
    links=re.findall('<loc>(.*?)</loc>',sitemap)
    for link in links:
        print(link)