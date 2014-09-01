__author__ = 'DM_'

from lib.ProxiesFunctions import *
import socket

class ModuleClass:
    """
    if not set ports. just use ports next.
    ports = [21,22,23,53,135,139,445,1433,1521,1720,1723,3306,3389,5900,8080,8443]
    or you need set ports like "21, 22, 80, 445, 8080, 3389" split with ","
    """

    options = {
        'rhosts': '127.0.0.1',
        'ports': '',
        'threads': 10,
        'timeout': 3,
    }

    info = {
        'author': 'DM_',
        'blog': 'http://x0day.me'
    }


    ports = [21,22,23,53,135,139,445,1433,1521,1720,1723,3306,3389,5900,8080,8443]

    def portscan(self, ip, port, timeout, verbose=False):

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            try:
                s.connect((ip, port))
            except KeyboardInterrupt:
                s.close()
                raise
            except Exception, e:
                s.close()
                return False
            s.close()
            color.echo("[*] %s port: %d status: open" % (ip, port), GREEN)
            return True

    def retArgs(self, rhosts, ports, timeout):
        argsLst = []
        for rhost in rhosts:
            for port in ports:
                argsLst.append((rhost, int(port), timeout))
        return argsLst

    def exploit(self):
        rhosts = self.options['rhosts']
        timeout = self.options['timeout']
        ports = len(self.options['ports']) and retList(self.options['ports']) or self.ports
        threads = int(self.options['threads'])

        rhosts = retRhosts(rhosts)
        if rhosts:
            color.echo("[*] all seems fine. go!", GREEN)
        argsLst = self.retArgs(rhosts, ports, timeout)
        threadsDo(self.portscan, threads, argsLst)