
import re

def link_crawler(url_start,link_regex):
    """Crawl from the given start URL following links matched by the link_regex"""
    crawl_queue=[url_start]
    while crawl_queue:
