from database.connection import Connection
from database.link import Link
from database.link_no_distance import Link_No_Distance


class Database:

    @staticmethod
    def check_if_in_visited(url):
        link_str = Link_No_Distance(url).__dict__
        return Connection.collection_visited.find_one(link_str) is not None

    @staticmethod
    def check_if_in_unvisited(url):
        link_str = Link_No_Distance(url).__dict__
        return Connection.collection_unvisited.find_one(link_str) is not None


    @staticmethod
    def add_url_to_unvisited(url, distance):
        link_str = Link(url, distance + 1).__dict__
        link_no_dist_str = Link_No_Distance(url).__dict__
        if Connection.collection_visited.find_one(link_no_dist_str) is None:
            Connection.collection_unvisited.insert_one(link_str)


    @staticmethod
    def add_url_to_visited(url, distance):
        link_str = Link(url, distance).__dict__
        link_no_dist_str = Link_No_Distance(url).__dict__
        Connection.collection_visited.insert_one(link_str)
        Connection.collection_unvisited.delete_one(link_no_dist_str)

    @staticmethod
    def count_unvisited():
        return Connection.collection_unvisited.count()

    @staticmethod
    def count_visited():
        return Connection.collection_visited.count()