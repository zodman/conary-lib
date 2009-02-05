#!/usr/bin/python
### compatible with conary 2.0.35
###  greets mkj
### zodman@foresightlinux.org under the WTFPL http://sam.zoy.org/wtfpl/

from conary.conaryclient import ConaryClient, cmdline
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
        """ get the database for do querys """
        return self.db 

    def _get_repos(self):
        """ get repos for do request query """
        return self.repos

    def label(self, installLabel = None):
        """ get label from config or custom installLabel """
        if installLabel:
            return Label(installLabel)
        return self.default_label

    def query(self, name):
        """ do a conary query """
        db = self._get_db()
        try:
            troves = db.findTrove( None ,(name , None, None ))
            #return db.getTroves(troves)
            return troves
        except TroveNotFound:
            return []

    def request_query(self, name, installLabel = None):
        """ Do a conary request query """
        label = self.label( installLabel )
        repos = self._get_repos()
        try:
            troves = repos.findTrove( label ,( name, None ,self.flavor ) )
            #return repos.getTroves(troves)
            return troves
        except TroveNotFound:
            return []

    def get_metadata( self, name , installLabel = None):
        pass
        
    def update(self, name, installLabel= None):
        cli = self.cli
        #get a trove
        troves = conary.request_query(name, installLabel)
        for trove in troves:
            trovespec =  self.trove_to_spec( trove )
        # create a Job
        job = cli.newUpdateJob()
        cli.prepareUpdateJob(job, cmdline.parseChangeList(trovespec))
        cli.applyUpdateJob(job)
        return "Update Success of %s" %  trovespec
    
    def trove_to_spec(self, trove ):
        return cmdline.toTroveSpec( trove[0], str(trove[1]), None)

if __name__ == "__main__":
    conary = ConaryPk()
    #print conary.query("gimp")
    #print conary.query("gimpasdas")
    #print conary.request_query("dpaster",'zodyrepo.rpath.org@rpl:devel')
    #print conary.request_query("gimp")
    #print conary.request_query("gimpasdasd")
    #print conary.update("pastebinit")
    print conary.update("iftop","zodyrepo.rpath.org@rpl:devel")

