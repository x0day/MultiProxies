#coding=utf-8
__author__ = 'DM_'

from lib.ProxiesFunctions import *
import json
import hashlib

class ModuleClass:

    info = {
        'author': 'DM_',
        'date': '2013/12/1',
        'blog': 'http://www.x0day.me',
        'description': 'check what CMS the site is.',
        'sites': 'a url or a file includes some urls.'
    }

    options = {
        'sites': 'sites.txt',
        'threads': 100,
    }

    def __init__(self):
        self.result = []
        self.cmsjsons = dict()
        self.log = []
        self.req = requests

    def retArgs(self, siteslst, cmsjsons):
        ArgsLst = []
        for site in siteslst:
            for cmsname in cmsjsons:
                for record in cmsjsons[cmsname]:
                    path = record["path"]
                    ArgsLst.append((site, path,))
        return list(set(ArgsLst))

    def retcmsjsons(self, jsonfilepath="db/cms.txt"):
        with open(jsonfilepath) as f:
            cmsjsons = json.loads(f.read())
        f.close()
        return cmsjsons

    def getcmsnamefromresp(self, path, resp, cmsjsons):
        for cmsname in cmsjsons:
            for record in cmsjsons[cmsname]:

                if record["path"] == path:

                    if record.has_key("version"):
                        version = record["version"]
                    else:
                        version = " Not Found."

                    if record.has_key("status_code"):
                        if resp.status_code == record["status_code"]:
                            return (cmsname,version)

                    elif record.has_key("regex"):
                        if re.search(record["regex"], resp.content):
                            print "regex"
                            return (cmsname,version)

                    elif record.has_key("md5"):
                        responsehash = hashlib.md5(resp.content).hexdigest()
                        if str(responsehash) == record["md5"]:
                            return (cmsname,version)
                    else:
                        return None
                    break

    def whatCMS(self, site, path):
        try:
            checkurl = site + path
            color.echo("[*] checking %s \r" % path[0:40].ljust(40," "),None, append=True)
            resp = urlGet(self.req, checkurl)
            result = self.getcmsnamefromresp(path, resp, self.cmsjsons)
            if (result):
                if not (site, result[0]) in self.result:
                    color.echo("[+]%s : %s ver: %s \t" % (site, result[0],result[1]), GREEN)
                    self.result.append((site, result[0]))
                self.log.append((site, path, result[0], result[1]))
        except Exception:
            pass

    def exploit(self):
        self.cmsjsons = self.retcmsjsons('db/cms.txt')
        threadsNum = int(self.options['threads'])
        sites = self.options['sites']
        sitesLst = retSites(sites)

        ArgsLst = self.retArgs(sitesLst, self.cmsjsons)
        threadsDo(self.whatCMS, threadsNum, ArgsLst)

        if len(self.result):
            logByLine(self.result,'output/%s-whatcms.txt' % currentTime("-"))