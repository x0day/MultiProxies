#coding=utf-8
__author__ = 'DM_'

from lib.ProxiesFunctions import *

class ModuleClass:
    """
    this is a demo module of MultiProxies Web Attack Framework,
    """
    info ={
        "author": "DM_",
        "date": "2014/08/08",
    }

    options = {
        "site": "http://www.x0day.me",
    }

    req = requests

    def exploit(self):
        url = self.options['site']
        resp = urlGet(self.req, url)
        color.echo("[*] this is a demo module. return site's headers.", GREEN)
        if resp:
            color.echo(resp.headers, BLUE)
        else:
            color.echo(" error", RED)
        time.sleep(1)

        color.echo('[*] test "ctrl + c" to stop...', GREEN)

        for x in range(1, 100):
            color.echo("test ... %d\r" % x , GREEN, append=True)
            time.sleep(0.3)