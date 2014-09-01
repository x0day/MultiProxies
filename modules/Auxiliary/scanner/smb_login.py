#coding=utf-8

__author__ = 'DM_'

from lib.ProxiesFunctions import *
from impacket.smbconnection import *
from impacket.smb3structs import *


class ModuleClass:

    """
    this module is based on impacket like patator_v0.5.py, please install impacket module first.
    and this module will test hashes first if hashes was given.
    and if no username and password or hashes given, this module will act as a smb_version scanner.
    just like this:
    -----------------------------------------------
    MultiProxies> smb_login)reload
    [*] reloading module.
    MultiProxies> smb_login)options
     ... snip ...
    MultiProxies> smb_login)info
     ... snip ...
    MultiProxies> smb_login)set username =
    username =>
    MultiProxies> smb_login)set password =
    password =>
    MultiProxies> smb_login)set rhosts 192.168.190.132
    rhosts => 192.168.190.132
    MultiProxies> smb_login)exploit
    [*] Xxx xx xx xx:yy:zz 201x starting to exploit..

    [+] 192.168.x.x SERVER-5xxxx  Windows Server 2003 3790 Service Pack 2
    [!] exploit finished.
    MultiProxies> smb_login)
    """

    options = {
        'rhosts': '127.0.0.1',
        'username': 'admin',
        'password': 'admin',
        'domain': '',
        'hashes': '',
        'timeout': 3,
        'threads': 10,
    }

    info = {
        "author": "DM_",
        "site": "http://x0day.me",
        "package required": "impacket"
    }

    dialects = SMB2_DIALECT_21

    def test_connection(self, rhost, domain, username, password, lmhash, nthash, timeout):
        try:
            if portscan(rhost, 445, timeout=timeout):
                smbConnection = SMBConnection(rhost, rhost)
                smbConnection.login(username, password, domain, lmhash, nthash)
                remotehost = smbConnection.getRemoteHost()
                servername = smbConnection.getServerName()
                serverdomain = smbConnection.getServerDomain()
                serveros = smbConnection.getServerOS()
                if password or (lmhash and nthash):
                    password_echo = password and "password: %s" % password or "hashes: %s:%s" % (lmhash, nthash)
                    username_echo = "username: %s" % username

                else:
                    password_echo = ""
                    username_echo = ""

                color.echo("[+] %s %s %s %s %s %s" % (
                    remotehost,
                    servername,
                    serverdomain,
                    serveros,
                    username_echo, password_echo), GREEN, verbose=True)
                smbConnection.logoff()
            else:
                pass

        except SessionError as e:
            color.echo("[!] %s" % e.getErrorString()[1], RED)

        except KeyboardInterrupt:
            raise

        except Exception, e:
            pass

    def retArgs(self, rhosts, domain, username, password, lmhash, nthash, timeout):
        argsLst = []
        for rhost in rhosts:
            argsLst.append((rhost, domain, username, password, lmhash, nthash, timeout))
        return argsLst

    def exploit(self):
        rhosts = self.options['rhosts']
        username = self.options['username']
        password = self.options['password']
        domain = self.options['domain']
        hashes = self.options['hashes']
        timeout = int(self.options['timeout'])
        threads = int(self.options['threads'])

        if hashes is not None and len(hashes):
            lmhash, nthash = hashes.split(":")
            password = ""

        else:
            lmhash = ''
            nthash = ''

        rhosts = retRhosts(rhosts)
        if rhosts:
            color.echo('[*] all seems fine. go!', GREEN)
            argsLst = self.retArgs(rhosts, domain, username, password, lmhash, nthash, timeout)
            threadsDo(self.test_connection,threads, argsLst)