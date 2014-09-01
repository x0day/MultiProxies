#coding = utf-8
__author__ = 'DM_'
from lib.ProxiesFunctions import *


class ModuleClass:
    """
    dirscan.
    """

    info = {
        'author': 'DM_',
        'date': '2013/12/1',
        'blog': 'http://x0day.me',
        'description': 'Dir scan.'
    }

    options = {
        'dirdict': 'db/dir/dir.txt',
        'sites':'sites.txt',
        'threads': 100,
        'timeout': 5,
    }

    def __init__(self):
        self.result = []
        self.log = {}
        self.req = requests

    def scan(self, site, checkurl, timeout):
        try:
            color.echo("[*]checking %60s\r" % (checkurl[0:60].ljust(60)), None, append=True)
            scanurl = site + checkurl
            resp = urlHead(self.req, scanurl, timeout=timeout, allow_redirects=False)
            status = resp.status_code

            if not site in self.log.keys():
                self.log[site] = []

            if status in [200, 301, 400, 500]:
                color.echo("[+]%66s~status:%3s" % (scanurl[0:66].ljust(66), status), GREEN, append=True)
                self.result.append((site, scanurl))
                self.log[site].append(scanurl)
        except KeyboardInterrupt:
            raise

        except Exception, e:
            pass

    def retArgs(self, sitesLst, timeout, dirDict):
        ArgsLst = []
        for site in sitesLst:
            if os.path.exists(dirDict):
                lines = open(dirDict).readlines()
                if len(lines):
                    for line in lines:
                        checkurl = line.replace("\n",'')
                        ArgsLst.append((site, checkurl, timeout))
                else:
                    color.echo("[!] no site found in sites' file.", RED)
        return ArgsLst

    def exploit(self):
        sites = self.options['sites']
        threadsNum = int(self.options['threads'])
        timeout = int(self.options['timeout'])
        dirDict = self.options['dirdict']

        sitesLst = retSites(sites)

        ArgsLst = self.retArgs(sitesLst, timeout, dirDict)
        threadsDo(self.scan, threadsNum, ArgsLst)
        for site in self.log.keys():
            logByLine(self.log[site], 'output/%s-%s-dirscan.txt' % (currentTime("-"),
                                                                 site.replace("http://", "").replace("/", "")))
