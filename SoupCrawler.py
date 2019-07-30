from bs4 import BeautifulSoup
from queue import Queue
import requests
import math


class SoupCrawler:
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
    :attr domain: Domain user requested to crawl
    :attr headers: Headers sent with requests to try to fool sites
    '''
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })

    def __init__(self, domain: str):
        self.domain = domain
        self.site_map = []
        self.seen_urls = set()

    def df_crawl(self, url: str, cur_depth: int = 0, max_depth: int = math.inf):
        '''
        Recursive depth-first crawl method to generate JSON site map
        :param url: Current url to peruse for links/images
        :param cur_depth: Current recursive depth
        :param max_depth: Max recursive depth specified, defaults to inf
        '''
        links_on_page = []
        try:
            r = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(r.text, 'lxml')
            # iterate about all anchor tags on current page with href attribute
            for a_tag in soup.findAll('a', href=True):
                # if not a seen link and not outside of domain, add to seen and recurse do_crawl for url (domain + href)
                if a_tag['href'] not in self.seen_urls and not a_tag['href'].startswith('http'):
                    self.seen_urls.add(a_tag['href'])
                    # only recurse if below max_depth
                    if max_depth and cur_depth < max_depth:
                        self.df_crawl((self.domain + a_tag['href'] if a_tag['href'].startswith('/') else self.domain + '/' + a_tag['href']), cur_depth+1, max_depth)
                    # add formatted link to links_on_page
                    links_on_page.append(self.domain + a_tag['href'] if a_tag['href'].startswith('/') else self.domain + '/' + a_tag['href'])

            img_on_page = self.get_img(soup)

            page_data = {
                "page_url": url,
                "links": links_on_page,
                "images": img_on_page
            }
            self.site_map.append(page_data)
        except Exception as e:
            print(e)

    def bf_crawl(self):
        '''
        Iterative breadth-first crawl method to generate JSON site map
        '''
        q = Queue()
        q.put(self.domain)

        while not q.empty():
            links_on_page = []
            cur_url = q.get()
            try:
                r = requests.get(cur_url, headers=self.headers)
                soup = BeautifulSoup(r.text, 'lxml')
                # iterate about all anchor tags on page with href attribute
                for a_tag in soup.findAll('a', href=True):
                    # if not a seen link and not outside of domain, add to queue
                    if a_tag['href'] not in self.seen_urls and not a_tag['href'].startswith('http'):
                        self.seen_urls.add(a_tag['href'])
                        q.put(self.domain + a_tag['href'] if a_tag['href'].startswith('/') else self.domain + '/' + a_tag['href'])
                        # add formatted link to links_on_page
                        links_on_page.append(self.domain + a_tag['href'] if a_tag['href'].startswith('/') else self.domain + '/' + a_tag['href'])

                img_on_page = self.get_img(soup)

                page_data = {
                    "page_url": cur_url,
                    "links": links_on_page,
                    "images": img_on_page
                }
                self.site_map.append(page_data)
            except Exception as e:
                print(e)

    def get_img(self, soup):
        '''
        Utility to fetch all img src on page
        :param soup: BeautifulSoup object
        :return: List of all img src on page
        '''
        img_on_page = []
        for img_tag in soup.findAll('img', src=True):
            # format src depending on if internal/external url
            if not img_tag['src'].startswith('http'):
                img_on_page.append(self.domain + img_tag['src'] if img_tag['src'].startswith('/') else self.domain + '/' + img_tag['src'])
            else:
                img_on_page.append(img_tag['src'])

        return img_on_page
