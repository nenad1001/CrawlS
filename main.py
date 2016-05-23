import threading
from database.connection import  Connection
from database.database import Database
from queue import Queue
from spider import Spider
from domain import *
import atexit


NUMBER_OF_THREADS = 10

thread_queue = Queue()

PROJECT_NAME = input("ENTER PROJECT NAME\n")

br = input("Enter 1 if you want to crawl, enter something else if you want to see already crawled pages\n")


domain = ''

broad_search = False

# Create spiders (will die when main exits)



def create_spiders():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        item = thread_queue.get()
        url = item['url']
        distance = item['distance']
        Spider.crawl_page(threading.current_thread().name, url, distance)
        thread_queue.task_done()


def create_jobs():
    for item in Connection.collection_unvisited.find():
        url = item['url']
        distance = item['distance']
        if Database.check_if_in_visited(url) is False and (domain == get_domain_name(url) or broad_search is True):
            thread_queue.put(item)
            Database.add_url_to_visited(url, distance)
            thread_queue.join()
            create_jobs()

if br == '1':
    in_url = input("ENTER HOMEPAGE (FULL URL)\n")

    broad = input("Do you want broad crawling (outside your domain)? Yes/No\n")

    if broad == 'Yes':
        broad_search = True

    domain = get_domain_name(in_url)

    Spider(PROJECT_NAME, in_url)

    create_spiders()
    create_jobs()
else:
    print('URL' + '  ===================   ' + 'Distance')
    Connection(PROJECT_NAME)
    for item in Connection.collection_visited.find():
        print(item['url'] + ' ' + str(item['distance']))