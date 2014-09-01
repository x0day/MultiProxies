# coding=utf-8
__author__ = 'DM_'

from lib.ProxiesFunctions import *
import string

class shodanhqhandle():
    """
    requests session sample.
    """
    def __init__(self):
        self.req = requests.session()
        self.headers = {"user-agent": retRandomUA()}

    def getauthtoken(self, url):
        try:
            resp = urlGet(self.req, url, headers=self.headers)
            if resp:
                html = resp.content
            else:
                html = ""
            token = re.findall(
                '<input id="_authentication_token" name="_authentication_token" type="hidden" value="([\s\S]+?)"',
                html)[0]
            return token
        except KeyboardInterrupt:
            raise
        except Exception, e:
            color.echo("[!] %s" % e, RED)
            return None

    def regedistUser(self, username, password):
        regedistUrl = "http://www.shodanhq.com/account/register"
        try:
            token = self.getauthtoken(regedistUrl)

            postdata = {
                "_authentication_token": token,
                "username": username,
                "email": username + "@yopmail.com",
                "password": password,
                "password_confirm": password,
                "submit": "I+accept.+Create+my+Account."
            }

            urlPost(self.req, "http://www.shodanhq.com/account/register", data=postdata, headers=self.headers)
            return True
        except KeyboardInterrupt:
            raise

        except Exception, e:
            color.echo("[!] %s" % e, RED)
            return False

    def getshodanactivateUrl(self, username):
        try:
            f = yopmail(username)
            html = f.getmailcnt("Activate Your SHODAN Account")
            ActivateUrl = re.findall("URL: <a href='([\s\S]+?)'", html)[0]
            return ActivateUrl
        except KeyboardInterrupt:
            raise

        except Exception, e:
            color.echo("[!] %s" % e, RED)
            return None

    def activateUser(self, username):
        activateUrl = self.getshodanactivateUrl(username)
        try:
            if not activateUrl:
                color.echo("[!]did't received activate url.", RED)
            urlGet(self.req, activateUrl, headers=self.headers)
            return True
        except KeyboardInterrupt:
            raise

        except Exception, e:
            color.echo("[!] %s" % e, RED)
            return False

    def login(self, username, password):
        try:
            loginurl = "http://www.shodanhq.com/account/login"
            token = self.getauthtoken(loginurl)

            postdata = {
                "_authentication_token": token,
                "username": username,
                "password": password,
                "next": "/home",
                "login_submit": "Login"
            }

            resp = urlPost(self.req, loginurl, data=postdata, headers=self.headers)
            return True
        except KeyboardInterrupt:
            raise

        except Exception, e:
            print "[!]%s" % e
            return False


    def getAPIcode(self, username="", password=""):
        try:
            resp = urlGet(self.req, "http://www.shodanhq.com/home", headers=self.headers)
            html = resp.content
            APIcode = re.findall("<h1>API Key</h1>\s<br/>\s([\s\S]+?)\s</div>", html)[0]
            return APIcode

        except KeyboardInterrupt:
            raise

        except Exception, e:
            print "[!]%s" % e
            return None


class ModuleClass():

    options = {
        'password': 'this1sPwd',
        'times': 5,
    }

    info = {
        'author': 'DM_',
        'blog': 'http://x0day.me'
    }

    def exploit(self):
        userslogfile = open("output/%s-shodanhq-usernames.txt" % currentDate, "a")
        APICODESlogfile = open("output/%s-shodanhqAPIs.txt" % currentDate, "a")

        password = self.options['password']
        times = int(self.options['times'])

        for now in xrange(0, times):
            username = string.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', 8)).replace(" ",
                                                                                                                     "")
            shodanhq = shodanhqhandle()

            color.echo("[registering] %s password:%s                       \r" % (username, password), GREEN, append=True)
            shodanhq.regedistUser(username, password)
            color.echo("[  waiting  ] waiting 2 seconds.                   \r", GREEN, append=True)
            time.sleep(2)
            color.echo("[ activating] %s with mail:%s                      \r" % (username, username + "@yopmail.com"), GREEN, append=True)
            shodanhq.activateUser(username)
            color.echo("[  logining ] %s                                   \r" % username, GREEN, append=True)
            shodanhq.login(username, password)
            color.echo("[  APICODE  ] getting, please waiting.             \r", GREEN, append=True)
            APICODE = shodanhq.getAPIcode()
            userslogfile.write(username + " " + password + "\n")
            if APICODE:
                APICODESlogfile.write(APICODE + "\n")
                color.echo("%s                                                     \r" % APICODE, GREEN, append=True)
            time.sleep(2)

