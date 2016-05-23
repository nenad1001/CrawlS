from pymongo import MongoClient

class Connection:
    db = None
    collection_unvisited = None
    collection_visited = None

    def __init__(self, project_name):
        client = MongoClient()
        Connection.db = client['crawler']

        Connection.collection_unvisited = Connection.db['unvisited_' + project_name]
        Connection.collection_visited = Connection.db['visited_' + project_name]
