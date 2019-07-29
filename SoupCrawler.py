from bs4 import BeautifulSoup
from pprint import pprint
import requests


class SoupCrawler():
    '''
    Class to handle domain crawling logic
    :attr site_map: List of dicts representing the domain site map, format:
        [
            {
                "page_url": <a_url>,
                "links": <all_links_on_page>,
                "images": <all_img_src_on_page>
            },
            ...
        ]
    :attr seen_urls: Set to hold all already seen urls to avoid cycles
    '''
    site_map = []
    seen_urls = set()

    def __init__(self, domain: str):
        '''
        Constructor
        :param domain: Domain user requested to crawl
        '''
        self.domain = domain

    def do_crawl(self, url: str):
        '''
        Recursive crawl method to generate JSON site map
        :param url: Current url to peruse for links/images
        '''
        links_on_page = []
        img_on_page = []
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        # iterate about all anchor tags on current page with href attribute
        for a_tag in soup.findAll('a', href=True):
            # if not a seen link, add to seen and try do_crawl for url (domain + href)
            if a_tag['href'] not in self.seen_urls and a_tag['href'].startswith('/'):
                self.seen_urls.add(a_tag['href'])
                try:
                    self.do_crawl(self.domain + a_tag['href'])
                except requests.exceptions.InvalidSchema:
                    pass
            # add link (domain + href) to page list
            links_on_page.append(self.domain + a_tag['href'])

        # iterate about all img tags with attribute src, add to page list
        for img_tag in soup.findAll('img', src=True):
            img_on_page.append(self.domain + img_tag['src'])

        page_data = {
            "page_url": url,
            "links": ','.join(links_on_page),
            "images": ','.join(img_on_page)
        }
        self.site_map.append(page_data)
