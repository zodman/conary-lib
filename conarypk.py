#!/usr/bin/python
from conary.conaryclient import ConaryClient
from conary import conarycfg
from conary.versions import Label
from conary.errors import TroveNotFound


class ConaryPk:
    def __init__(self):
        # get configs from /etc/conary
        cfg = conarycfg.ConaryConfiguration(True)
        # get if the machine its x86 or x86_64
        cfg.initializeFlavors()
        self.cfg = cfg

        cli = ConaryClient(cfg)

        # labels enable on /etc/conary/config.d/
        self.default_label = self.cfg.installLabelPath

        # get if x86 or x86_64
        self.flavor = self.cfg.flavor[0]
        # for client
        self.cli = cli
        # for query on system (database)
        self.db = cli.db
        # for request query on repository (repos)
        self.repos = cli.repos

    def _get_db(self):
        return self.db 

    def _get_repos(self):
        return self.repos

    def label(self, installLabel = None):
        if installLabel:
            return Label(installLabel)
        return self.default_label

    def query(self, name):
        """ do a conary query """
        db = self._get_db()
        try:
            troves = db.findTrove( None ,(name , None, None ))
            return db.getTroves(troves)
        except TroveNotFound:
            return []

    def request_query(self, name, installLabel = None):
        """ Do a conary request query """
        label = self.label( installLabel )
        repos = self._get_repos()
        #try:
        troves = repos.findTrove( label ,( name, None ,self.flavor ) )
        return repos.getTroves(troves)
       # except TroveNotFound:
       #     return []

    def get_metadata( self, name , installLabel = None):
        label = self.label(installLabel)
        pass

if __name__ == "__main__":
    conary = ConaryPk()
    print conary.query("gimp")
    print conary.query("gimpasdas")
    print conary.request_query("dpaster",'zodyrepo.rpath.org@rpl:devel')
    print conary.request_query("gimp")
