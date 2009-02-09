#!/usr/bin/python
### compatible with conary 2.0.35
###  greets mkj
### zodman@foresightlinux.org under the WTFPL http://sam.zoy.org/wtfpl/

from conary.conaryclient import ConaryClient, cmdline
from conary import conarycfg
from conary.versions import Label
from conary.errors import TroveNotFound
from conary.conaryclient.update import NoNewTrovesError


class ConaryPk:
    def __init__(self):
        """ Init the configurations """
        # get configs from /etc/conary
        cfg = conarycfg.ConaryConfiguration( readConfigFiles = True)
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
        """ 
            Get label from config or custom installLabel  or convert the installLabel to LabelObject
            @return (object) Label("label1")

        """
        if installLabel:
            return Label(installLabel)
        return self.default_label

    def get_labels_from_config(self):
        """ Get foresight repo-labels from configurations files
            @return list ["label1","label2"]
        """
        labels = []
        for i in self.default_label:
            if "foresight.rpath.org" in i.asString():
                labels.append(i.asString())
        return labels
    def query(self, name):
        """ Do a conary query 
            @return [ ('name', VFS("version"), Flavor("#xxx")), ]
        """
        if name is None or name == "":
            return []
        db = self._get_db()
        try:
            troves = db.findTrove( None ,(name , None, None ))
            #return db.getTroves(troves)
            return troves
        except TroveNotFound:
            return []

    def request_query(self, name, installLabel = None):
        """ Do a conary request query 
            @return [ ('name', VFS("version"), Flavor("#xxx")), ]
        """
        label = self.label( installLabel )
        repos = self._get_repos()
        try:
            troves = repos.findTrove( label ,( name, None ,self.flavor ) )
            #return repos.getTroves(troves)
            return troves
        except TroveNotFound:
            return []

    def get_metadata( self, name , installLabel = None):
        troveTuple = self.request_query( name, installLabel )
        repos = self._get_repos()
        troves = repos.getTroves(troveTuple)
        metadata = None
        for trove in troves:
            if trove:
                metadata = trove.getMetadata()
        return metadata
        
    def remove(self, name):
        return self.update(name, remove = True )

    def update(self, name, installLabel= None, remove  = False ):
        """ Update/remove  a package 
        """
        cli = self.cli
        #get a trove
        troves = self.request_query(name, installLabel)
        for trove in troves:
            trovespec =  self.trove_to_spec( trove, remove )
        try:
            # create a Job
            job = cli.newUpdateJob()
            # Add Update task to Job
            cli.prepareUpdateJob(job, cmdline.parseChangeList(trovespec))
            # Apply the Job
            cli.applyUpdateJob(job)
            # im rulz
            return "Update Success of %s" %  trovespec
        except NoNewTrovesError:
            return "no new Troves Found by %s " % trovespec
    
    def trove_to_spec(self, trove, remove = False ):
        """ Convert a trove to a spec 
            @return (string) "app=myrepo.rpath.org@rpl:devel"
            
        """
        # add a -app=blah.rpath.org@rpl:devel for remove packages
        if remove:
            tmp = '-'
        else:
            tmp = ""
        return tmp + cmdline.toTroveSpec( trove[0], str(trove[1]), None)

if __name__ == "__main__":
    conary = ConaryPk()
    #print conary.query("dpaster")
    #print conary.query("gimpasdas")
    #print conary.request_query("dpaster",'zodyrepo.rpath.org@rpl:devel')
    #print conary.request_query("gimp")
    #print conary.request_query("gimpasdasd")
    #print conary.update("amsn")
    #print conary.get_labels_from_config()
#    print conary.get_metadata("gimp")
    print conary.get_metadata("christine",'zodyrepo.rpath.org@rpl:devel')

