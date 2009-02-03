
from conary.conaryclient import ConaryClient
from conary.version import Label


class ConaryPk:
    def __init__(self, label = None):
        if label:
            self.label = Label(label)
        cli = ConaryClient()
        self.db = cli.db
        self.repos = cli.repos

    def get_db(self):
        return self.db 

    def get_repos(self):
        return self.repos

    def query(self, name):
        pass 
