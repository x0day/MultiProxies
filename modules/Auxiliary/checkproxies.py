#coding = utf-8
__author__ = 'DM_'
from lib.ProxiesFunctions import *
import hashlib

class ModuleClass:
    info = {
        'author': 'DM_',
        'date': '2013/12/1',
        'blog': 'http://x0day.me',
        'description': 'Check the proxies given whether can be used.'
    }

    options = {
        'datadir': 'db/proxies/',
        'threads': 30,
        'checkurl': 'http://www.baidu.com/img/bdlogo.gif',
        'checkhash': '74e5229bc0fff4b0d37a94de0adc1c81',
        'timeout': '5',
    }
    def __init__(self):
        self.req = requests
#        self.lock = threading.Lock()
        self.proxies = []
        self.checked = 0

    def checkProxies(self,
                     proxies,
                     checkurl,
                     checkhash,
                     timeout=5):

        if not 'http://' in proxies:
            proxies = "http://%s" % proxies
        proxies = proxies.replace("\r", '')
        proxies = proxies.replace("\n", '')
        proxies = dict(http=proxies)
        self.checked += 1

        try:
            color.echo("[!]available:%d ~checked:%d checking %s ...    \r" % (len(self.proxies),
                                                                            self.checked,
                                                                            proxies['http']), GREEN, append=True)
            resp = urlGet(self.req, checkurl, proxies=proxies, timeout=timeout)
            html = resp.content

            ResponseHash = hashlib.md5(html).hexdigest()
            if ResponseHash == checkhash:
                self.proxies.append(proxies['http'])
        except Exception, e:
            pass


    def exploit(self):
        datadir = self.options['datadir']
        threadsNum = int(self.options['threads'])
        checkurl = self.options['checkurl']
        checkhash = self.options['checkhash']
        timeout = int(self.options['timeout'])

        allProxies = []
        argsLst = []

        for path in os.listdir(datadir):
            allProxies.extend(open(datadir + path,'r').readlines())
        allProxies = list(set(allProxies))

        color.echo("[*]Find %d proxies." % len(allProxies), CYAN)

        for proxies in allProxies:
            argsLst.append((proxies, checkurl, checkhash, timeout))
        threadsDo(self.checkProxies, threadsNum,argsLst)
        logByLine(self.proxies, 'db/proxies.txt')