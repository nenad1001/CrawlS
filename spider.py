from urllib.request import  urlopen
from database.connection import Connection
from database.database import Database
from parser import Parser


class Spider:

    project_name = ''
    base_url = ''

    def __init__(self, project_name, base_url):
        Spider.project_name = project_name
        Spider.base_url = base_url
        self.boot()
        self.crawl_page('Initial spider', Spider.base_url, 0)


    def boot(self):
        Connection(self.project_name)

    @staticmethod
    def crawl_page(thread_name, page_url, distance):
        print(thread_name + '. spider now crawling ' + page_url)
        Spider.add_links_to_queue(Spider.gather_links(page_url), distance)


    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            html_bytes = response.read()
            html_string = html_bytes.decode('utf-8')
            finder = Parser(Spider.base_url, page_url)
            finder.feed(html_string)
        except:
            print('Error: can not crawl page ' + page_url)
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links, distance):
        for url in links:
            if Database.check_if_in_visited(url) is True:
                continue
            if Database.check_if_in_unvisited(url) is True:
                continue
            Database.add_url_to_unvisited(url, distance)
