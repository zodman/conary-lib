#!/usr/bin/python
from conary.conaryclient import ConaryClient
from conary.versions import Label
from conary.errors import TroveNotFound


class ConaryPk:
    def __init__(self, installlabel):

        self.default_label = Label(installlabel)
        cli = ConaryClient()
        self.cli = cli
        self.db = cli.db
        self.repos = cli.repos

    def _get_db(self):
        return self.db 

    def _get_repos(self):
        return self.repos

    def _set_label(self, installLabel=None):
        if installLabel:
            self.label = Label(installLabel)

    def _get_label(self):
        try:
            return self.label
        except AttributeError:
            return self.default_label

    def get_label(self, installLabel = None):
        if installLabel:
            self._set_label(installLabel)
        
        return self._get_label()

        
    def query(self, name):
        """ do a conary query """
        db = self._get_db()
        try:
            troves = db.findTrove(None,(name,None,None))
            return db.getTroves(troves)
        except:
            return []

    def request_query(self, name, installLabel = None):
        """ Do a conary request query """
        label = self.get_label( installLabel )
        repos = self._get_repos()
        try:
            troves = repos.findTrove(label, (name,None,None))
            return repos.getTroves(troves)
        except TroveNotFound:
            return []

    def get_metadata( self, name , installLabel = None):
        self._set_repos(installLabel)
        repos = self._get_repos()

if __name__ == "__main__":
    conary = ConaryPk('foresight.rpath.org@fl:2')
   # print conary.query("gimp")
   # print conary.query("gimpasdas")
   # print conary.request_query("dpaster",'zodyrepo.rpath.org@rpl:devel')
    print conary.request_query("dpaster")
