from bs4 import BeautifulSoup
import requests


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
    :attr headers: Headers sent with requests-- includes user-agent to try and fool anti-bot sites
    '''
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })

    def __init__(self, domain: str):
        self.domain = domain
        self.site_map = []
        self.seen_urls = set()

    def do_crawl(self, url: str):
        '''
        Recursive crawl method to generate JSON site map
        :param url: Current url to peruse for links/images
        '''
        links_on_page = []
        img_on_page = []
        try:
            r = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            # iterate about all anchor tags on current page with href attribute
            for a_tag in soup.findAll('a', href=True):
                # if not a seen link and not outside of domain, add to seen and recurse do_crawl for url (domain + href)
                if a_tag['href'] not in self.seen_urls and not a_tag['href'].startswith('http'):
                    self.seen_urls.add(a_tag['href'])
                    self.do_crawl(self.domain + a_tag['href'] if a_tag['href'].startswith('/') else self.domain + '/' + a_tag['href'])

                # add link (domain + href) to page list
                links_on_page.append(self.domain + a_tag['href'] if a_tag['href'].startswith('/') else self.domain + '/' + a_tag['href'])

            # iterate about all img tags with attribute src, add to page list
            for img_tag in soup.findAll('img', src=True):
                img_on_page.append(self.domain + img_tag['src'])
        except Exception as e:
            print(e)

        page_data = {
            "page_url": url,
            "links": links_on_page,
            "images": img_on_page
        }

        self.site_map.append(page_data)
