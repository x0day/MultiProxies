# coding=utf-8
__author__ = 'DM_'

from lib.Threads import ThreadPool
from lib.EchoColor import *
import lib.socks as socks
import random
import socket
import requests
import time
import re
import os

# ##############################################################################################
# MltProxies HTTP request sources.
#
#
#
# @param req: requests or requests.session()
# @param url: target url.
# @param kwargs: same as requests' kwargs.
#
# return get resp.
#

def urlHead(req, url, **kwargs):
    """
    HTTP HEAD REQUESTS.
    """
    try:
        resp = req.head(url, **kwargs)

    except KeyboardInterrupt:
        raise

    except Exception, e:
        resp = None
    return resp


def urlGet(req, url, **kwargs):
    """
    HTTP GET REQUESTS.
    """
    try:
        resp = req.get(url, **kwargs)

    except KeyboardInterrupt:
        raise

    except Exception, e:
        resp = None
    return resp


def urlPost(req, url, **kwargs):
    """
    HTTP POST REQUESTS.
    """
    try:
        resp = req.post(url, **kwargs)

    except KeyboardInterrupt:
        raise

    except Exception, e:
        resp = None
    return resp


def urlOptions(req, url, **kwargs):
    """
    HTTP OPTIONS REQUESTS.
    """
    try:
        resp = req.options(url, **kwargs)

    except KeyboardInterrupt:
        raise

    except Exception, e:
        resp = None
    return resp


def retRandomProxies(ProxiesfilePath='db\proxies.txt'):
    """
    return a random proxies from db\proxies.txt.
    @param ProxiesfilePath: proxies.txt file path.
    """

    if os.path.exists(ProxiesfilePath):
        proxiesLst = [x for x in open(ProxiesfilePath, 'r')]
        randomProxies = random.sample(proxiesLst, 1)[0]
        if not 'http://' in randomProxies:
            randomProxies = "http://%s" % randomProxies
        proxies = dict(http=randomProxies.replace("\n", ''))
    else:
        proxies = None
    return proxies


def retRandomUA():
    """
    @return:a random user-agent.
    """

    ua = open('db/ua.txt').readlines()
    return ua[random.randrange(0, len(ua))].strip()


def retRandomRobotUA():
    """
    @return:a random robot agent.
    """

    robotua = open('db/robot-ua.txt').readlines()
    return robotua[random.randrange(0, len(robotua))].strip()

# HTTP requests sources over.
###############################################################################################
#IP

#pattern reference:Jeffrey E. F. Friedl
ipPattern = "^([1]?\d\d?|2[0-4]\d|25[0-5])\." \
            "([1]?\d\d?|2[0-4]\d|25[0-5])\." \
            "([1]?\d\d?|2[0-4]\d|25[0-5])\." \
            "([1]?\d\d?|2[0-4]\d|25[0-5])$"

#sample : 192.168.1.1-10
iprangePattern = "^([1]?\d\d?|2[0-4]\d|25[0-5])\." \
                 "([1]?\d\d?|2[0-4]\d|25[0-5])\." \
                 "([1]?\d\d?|2[0-4]\d|25[0-5])\." \
                 "([1]?\d\d?|2[0-4]\d|25[0-5])-([1]?\d\d?|2[0-4]\d|25[0-5])$"


def isip(ip):
    if re.match(ipPattern, ip):
        return True
    else:
        return False


def isiprange(iprange):
    if re.match(iprangePattern, iprange):
        return True
    else:
        return False


def getiplst(host, start=1, end=255):
    """

    @param host: IP, like 192.168.1.1
    @param start: ip start like 1
    @param end: ip end like 255
    @return: a ip list
    """
    iplst = []
    ip_pre = ""
    for pre in host.split('.')[0:3]:
        ip_pre = ip_pre + pre + '.'
    for i in range(start, end):
        iplst.append(ip_pre + str(i))
    return iplst


def retiprangelst(iprange):
    """

    @param iprange: an iprange match iprangePattern
    @return:a ip list with a range given.
    """
    iplst = []
    if re.match(iprangePattern, iprange):
        ips = re.findall(iprangePattern, iprange)[0]
        ip = ips[0] + "." + ips[1] + "." + ips[2] + "." + "1"
        ipstart = int(ips[3])
        ipend = int(ips[4]) + 1
        iplst = getiplst(ip, ipstart, ipend)
        return iplst
    else:
        return None


def retRandomip():
    """


    @return: a random IP.
    """
    return "%d.%d.%d.%d" % (random.randint(11, 190),
                            random.randint(11, 190),
                            random.randint(11, 190),
                            random.randint(11, 190))


def domain2ip(domainName):
    """

    @param domainName: domain name.
    @return: ip.
    """
    #noinspection PyBroadException
    try:
        resultIp = socket.getaddrinfo(domainName, None)[0][4][0]
        return resultIp
    except:
        return None


def ip2int(s):
    """

    @param s: ip
    @return: ip to int.
    """
    l = [int(i) for i in s.split('.')]
    return (l[0] << 24) | (l[1] << 16) | (l[2] << 8) | l[3]


def retRhosts(rhosts):
    """
    @param rhosts: ip, ipfile, iprange
    """
    iplst = []
    if isip(rhosts):
        iplst.append(rhosts)

    elif isiprange(rhosts):
        iplst = retiprangelst(rhosts)

    elif os.path.exists(rhosts):
        lines = rhosts.readlines()
        for line in lines:
            if re.match(ipPattern, line):
                iplst.append(line)
            elif re.match(iprangePattern, line):
                iplst.append(retiprangelst(line))
    else:
        return None
    return iplst


##################################################################################
##url

urlregex = re.compile(
    # reference:django url regex
    # but a little changed.
    # modified by DM_.

    r'^(?P<scheme>socks4|socks5|http|https)?://'  #scheme
    r'(?P<netloc>(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
    r'(?:\:)?(?P<port>\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)


def urlCheck(url):
    """
    check url, and if match urlregex, return scheme, netloc, port.
    scheme is http, port is 80
    """
    checkurl = ''
    port = lambda x: x and int(x) or 80

    if isUrl(url):
        checkurl = url
    elif isUrl("http://%s/" % url):
        checkurl = "http://%s/" % url
    else:
        return None

    r = urlregex.search(checkurl).groupdict()
    return checkurl, r['scheme'], r['netloc'], port(r['port'])


def isUrl(url):
    """

    @param url: anything to check if match urlregex,
    """
    if url and urlregex.match(url):
        return True
    else:
        return False


def retSites(sites):
    """

    @param sites: url or url file,
    """
    sitesLst = []
    if os.path.exists(sites):
        lines = open(sites).readlines()
        if len(lines):
            for line in lines:
                site = line.replace("\n", "")
                sitesLst.append(site)

    elif isUrl(sites):
        sitesLst.append(sites)

    elif isUrl("http://%s/" % sites):
        sitesLst.append("http://%s/" % sites)
    else:
        return None
    return sitesLst

###################################################################################
#DATA
#
#return current date.
currentDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))

#return current time.
currentTime = lambda x: time.strftime('%Y-%m-%d_%H' + x + '%M' + x + '%S', time.localtime(time.time()))


def retPwds(username):
    pattern = "^\w+$"

    passLst = [
        '',
        '1',
        '12',
        '123',
        '1234',
        '12345',
        '123456',
        '!@#',
        '@123',
        '@123.com',
        '163',
        '@163',
        '@163.com',
        'a',
        'ab',
        'abc',
        'qwe',
        'qwert',
        '8',
        '88',
        '888',
        '999',
        '666',
        '2008',
        '2009',
        '2010',
        '2011',
        '2012',
        '2013',
        '2014',
        '@2008',
        '@2009',
        '@2010',
        '@2011',
        '@2012',
        '@2013',
        '@2014'
        "654321",
        "123123",
        "123456789",
        "5201314",
        "1314520",
        "woaini",
        "makelove",
        "112233",
        "qwert",
        "1q2w3e",
        "qwer",
        "qazwsx",
        "54321",
    ]

    passwords = []

    if re.match(pattern, username):
        for password in passLst:
            passwords.append(username + password)
    passwords.extend(passLst)
    return passwords


def logByLine(LogSource, LogFilePath=None, mode="w"):
    """

    @param LogSource: list
    @param LogFilePath: logfile path
    @param mode: open mode
    """
    LogCnt = ''

    if not LogFilePath:
        LogFilePath = "output/" + currentTime("-") + ".txt"
    if type(LogSource) == type(list()):
        for line in LogSource:
            if isinstance(line, tuple):
                lines = ""
                for x in line:
                    x = x.replace("\n", "")
                    x = x.replace("\r", "")
                    lines += x
                    lines += " "
                line = lines
            else:
                line = line.replace("\n", "")
                line = line.replace("\r", "")
            LogCnt += line + '\n'
    LogCnt += "\n\n"
    LogFile = open(LogFilePath, mode)
    LogFile.write(LogCnt)
    print
    color.echo("[*] saved logfile to %s" % LogFilePath, CYAN)
    LogFile.close()


def isTrue(check):
    """
    用于判断用户输入是否为真项
    各种反人类的输入判断可以加在这里，比如 "zheshizhendea"
    """
    if str(check).lower() in ['true', 'yes', 'ok', '1', 'on']:
        return True
    else:
        return False


def isFalse(check):
    """
    用于判断用户输入是否为假项
    各种反人类的输入判断可以加在这里，比如 "zheshijiade,baichi"
    """
    if str(check).lower() in ['false', 'no', '0', 'off']:
        return True
    else:
        return False


def retList(lists):
    return lists.split(",")


#####################################################################
#threads

def threadsDo(ThreadsFun, ThreadsNum, ArgsLst):
    """

    :param ThreadsFun: function
    :param ThreadsNum: threads num.
    :param ArgsLst: args list.
    if function accepts a parameter.
    the ArgsLst format is like this (attention ","):
    [(arg1,),(arg2,),(arg3,) ...]

    if function accepts some parameters.
    the ArgsLst format is like this:
    [(arg11,arg12),(arg21,arg22),(arg31,arg32) ...]
    [(arg11,arg12,arg13),(arg21,arg22,arg23),(arg31,arg32,arg33) ...]
    ...
    """
    tp = ThreadPool(ThreadsNum)
    for Args in ArgsLst:
        tp.add_job(ThreadsFun, Args)
    tp.start()
    try:
        tp.wait_for_complete()
    except KeyboardInterrupt:
        tp.stop()


###########################################################################
###module
def setOptions(Module, options):
    status = True
    opt_status = lambda x: type(x) == type(None) and True or False
    opts = options.split("&")
    if Module.nextStatus is True:
        for opt in opts:
            status &= opt_status(Module.do_set(opt))
        Module.do_options("")
        return status
    else:
        return False


def setGlobals(options):
    from lib.Console import Client

    opts = options.split("&")
    for opt in opts:
        Client.do_setg(opt)


#######################################################################
###socks proxy.
_orgsocket = socket.socket
_orgcreateconnection = socket.create_connection
_orggetaddrinfo = socket.getaddrinfo


def setProxy(scheme, ip, port):
    """
    reference : https://pypi.python.org/pypi/GoogleScraper/0.0.2.dev1
    @scraping.py line:311

    + getaddrinfo function.
    modified by DM_

    @param scheme: socks4,socks5
    @param ip: ip
    @param port: port.

    """

    def create_connection(address, timeout=None, source_address=None):
        sock = socks.socksocket()
        sock.connect(address)
        return sock

    def getaddrinfo(*args):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]


    pmapping = {
        'socks4': 1,
        'socks5': 2,
        'http': 3
    }
    # Patch the socket module  # rdns is by default on true. Never use rnds=False with TOR, otherwise you are screwed!
    socks.setdefaultproxy(pmapping.get(scheme), ip, port, rdns=True)
    socks.wrapmodule(socket)
    socket.socket = socks.socksocket  ##add for socket. if not then can only use requests or other modules but socket.
    socket.create_connection = create_connection
    socket.getaddrinfo = getaddrinfo


def unsetProxy():
    socket.socket = _orgsocket
    socket.create_connection = _orgcreateconnection
    socket.getaddrinfo = _orggetaddrinfo


#########################################################################################
##Client Globals
def isClientVerbose():
    from lib.Console import Client

    if (Client.globals['default']['verbose']).lower() in ["true", "yes", "on", "ok", "1"]:
        return True
    else:
        return False


def isColor():
    from lib.Console import Client

    if (Client.globals['default']['color']).lower() in ["true", "yes", "on", "ok", "1"]:
        return True
    else:
        return False


###########################################################################
### others
def portscan(ip, port, timeout, verbose=True):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        result = s.connect((ip, port))
    except KeyboardInterrupt:
        s.close()
        raise
    except Exception, e:
        s.close()
        return False
    s.close()
    color.echo("[*] %s port: %d status: open" % (ip, port), GREEN, verbose=verbose)
    return True


class yopmail():
    def __init__(self, user):
        """

        :param user: username
        """
        self.headers = {"user-agent": retRandomUA()}
        self.user = user
        self.req = requests
        self.maildict = dict()
        self.maillst = self._getmaillst()

    def _getmaillst(self):
        loginurl = "http://m.yopmail.com/en/inbox.php?login=%s&yp=DAQL0AwV0ZwD2BGD1AmHjAj&yj=TZmR1AQL2AwpkBGVlAQRkAj&v=2.4" % self.user
        resp = urlGet(self.req, loginurl, headers=self.headers)
        if resp:
            html = resp.content
        else:
            html = ""
        try:
            maillst = re.findall('<div   class="um"><a class="lm_m" href="(?P<from>[\s\S]+?)">'
                                 '<span class="lmfd"><span class="lmh">(?P<time>[\s\S]+?)</span>'
                                 '<span  class="lmf">(?P<titile>[\s\S]+?)</span></span>'
                                 '<span class="lms_m">([\s\S]+?)</span>'
                                 '</a></div>', html)
        except:
            maillst = []

        for lst in maillst:
            maillink = "http://m.yopmail.com/" + lst[0]
            mailtime = lst[1]
            mailfrom = lst[2]
            mailtitle = lst[3]
            self.maildict[mailtitle] = dict()
            self.maildict[mailtitle]['from'] = mailfrom
            self.maildict[mailtitle]['link'] = maillink
            self.maildict[mailtitle]['time'] = mailtime

    def getmailcnt(self, title):
        if title in self.maildict.keys():
            link = self.maildict[title]["link"]

            try:
                resp = urlGet(self.req, link, headers=self.headers)
                html = resp.content

                mailcnt = re.findall('<div style=" overflow:scroll; width:100%; "  class="f20">([\s\S]+?)</div>', html)[
                    0]
            except:
                mailcnt = ""

            return mailcnt
