r"""
___  ___      _ _   _______              _
|  \/  |     | | | (_) ___ \            (_)
| .  . |_   _| | |_ _| |_/ / __ _____  ___  ___  ___
| |\/| | | | | | __| |  __/ '__/ _ \ \/ / |/ _ \/ __|
| |  | | |_| | | |_| | |  | | | (_) >  <| |  __/\__ \
\_|  |_/\__,_|_|\__|_\_|  |_|  \___/_/\_\_|\___||___/

"""

__author__ = 'DM_'
__version__ = '3.0.1'

from lib.Database import updateDB, AllModules, DataBaseModulesLst, AllModulesLst
from lib.EchoColor import *
from lib.Console import *
from lib.args import *

import sys

DebugMode = False

def printBanner(Client):
    color.echo(__doc__, BLUE)
    color.echo("=# ", CYAN, True)
    color.echo("author:DM_ / blog:http://x0day.me", GREEN)
    color.echo("=# ", CYAN, True)
    color.echo("version::%s" % __version__.ljust(10), GREY)
    color.echo("=# ", CYAN, False)
    color.echo("=# ", CYAN, True)
    color.echo("Modules::%d " % (len(AllModulesLst)), BLUE, True)
    color.echo("Exploit::%d " % len(AllModules['Exploit']), RED, True)
    color.echo("Auxiliary::%d" % len(AllModules['Auxiliary']), YELLOW, False)


def runConsole():
    printBanner(Client)
    print
    while not DebugMode:
        try:
            Client.cmdloop()

        except KeyboardInterrupt:
            Client.prompt = ""
            print
            UserInput = raw_input("[!] back to main Menu of MultiProxies or exited?[Y/n]):")
            if UserInput.lower() in ['y', '']:
                Client.prompt = "MultiProxies>"
            elif UserInput.lower() in ['n']:
                exit()
            else:
                color.echo("[!]Wrong input!", RED)

def runWeb():
    """
    may add in future.
    """
    color.echo("[!] maybe will in 4.0.0 .. may be.", GREEN)
    pass

if __name__ == '__main__':
    AllModulesLst.sort()
    DataBaseModulesLst.sort()
    if not AllModulesLst == DataBaseModulesLst:
        color.echo("[!] maybe some new modules comes in. please try to updatedb.", RED)
        userInput = raw_input('try to updatedb ?[Y/n]:')
        if userInput.lower() in ['', 'y']:
            updateDB()

    if consoleMode:
        runConsole()

    elif webMode:
        runWeb()

    else:
        if showLst:
            print
            Client.do_show("")
            sys.exit()

        elif search:
            print
            Client.do_search(search)
            sys.exit()

        elif module:
            moduleName = returnModuleName(module)
            if moduleName:
                Module = ExecModule(moduleName)

                if globals:
                    from lib.ProxiesFunctions import setGlobals
                    setGlobals(globals)

                if options:
                    from lib.ProxiesFunctions import setOptions
                    optionsCorrect = setOptions(Module, options)
                    if optionsCorrect and run:
                        Module.do_exploit("")
                elif run:
                    Module.do_exploit("")
                else:
                    if Module.nextStatus is True:
                        print
                        color.echo("[*] options:", CYAN)
                        Module.do_options("")
                        print
                        color.echo("[*] info:", CYAN)
                        Module.do_info("")
                        sys.exit()

            else:
                color.echo("[!] the module %s is not available." % module, RED)
        else:
            printBanner(Client)
            print
            parser.print_help()
