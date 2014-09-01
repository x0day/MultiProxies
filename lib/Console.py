#coding=utf-8
__author__ = 'DM_'

from lib.EchoColor import *
from lib.Database import *
from lib.Module import useModule
from cmd import Cmd
import time


helpline = lambda title, COLOR : color.echo("+%s+" % (title.center(76, "-")), COLOR, verbose=True)
helpinfo  = lambda command, info, COLOR: color.echo("|%-10s|%65s|" % (command.center(10, " "), info.center(65, " ")), COLOR, verbose=True)

mltHelpInfos = [
    ["help", "Displays this help information."],
    ["exit", "Exit from MultiProxies."],
    ["use", "use <ID><ModuleName> ,use the module given."],
    ["show", "show[all,exploit,auxiliary] ,show the list of module's type."],
    ["search", "search <keyword> ,search keyword in modules' name."],
    ["updatedb", "update the database when new module comes in."],
    ["setg", "set the global var. setg [option] [value]"],
    ["usetg", "disable the global var."],
]

mltModuleHelpInfos = [
    ["help", "Displays this help information."],
    ["exit", "Exit from MultiProxies."],
    ["use", "use <ID><ModuleName> ,use the module given."],
    ["show", "show[all,exploit,auxiliary] ,show the list of module's type."],
    ["search", "search <keyword> ,search keyword in modules' name."],
    ["updatedb", "update the database when new module comes in."],
    ["setg", "set the global var. setg [option] [value]"],
    ["usetg", "disable the global var."],
    ["reload", "reload the module."],
    ["set", "set [option] [value]."],
    ["options", "display the module's options."],
    ["info", "display the module's information."],
    ["exploit", "start to exploit the target."],
    ["back", "back to the last module's view."],
]

def MltPMainHelp():
    print
    title = "MultiProxies Start HELP MENU"
    helpline(title , YELLOW)
    helpinfo("COMMAND", "DESCRIPTION", YELLOW)
    color.echo("|%s|" % "".center(76, " "), CYAN, verbose=True)

    for line in mltHelpInfos:
        helpinfo(line[0], line[1], CYAN)
    helpline("-", YELLOW)
    print


def MltPModuleHelp():
    print
    title = "MultiProxies Module HELP MENU"
    helpline(title , YELLOW)
    helpinfo("COMMAND", "DESCRIPTION", YELLOW)
    color.echo("|%s|" % "".center(76, " "), CYAN, verbose=True)

    for line in mltModuleHelpInfos:
        helpinfo(line[0], line[1], CYAN)
    helpline("-", YELLOW)
    print


def updateFromClient(params, globals):
    for key in params.keys():
        if key in globals.keys():
            params[key] = globals[key]

def returnLowerCases(lst):
    """

    :param lst: the list or dic to handler.
    :return: low case list or dic.
    """
    if type(lst) == type(list()):
        TmpLst = lst[:]
        for i in xrange(len(lst)):
            TmpLst[i] = lst[i].lower()
        return TmpLst
    if type(lst) == type(dict()):
        dct = dict()
        for k in lst:
            dct[k.lower()] = lst[k]
        return dct


def printModuleDict(ModulesDict):
    color.echo("+" + "ID".center(6, "-") + "+" +
                "ModuleName".center(58, "-") + "+" +
                "TYPE".center(10, "-") + "+", YELLOW)
    for i in xrange(0, len(ModulesDict)):
        color.echo("%s%-6s%s%56s%s%9s%s" % ("|", str(ModulesDict[i][0]).center(6), #ID
                                           "|", ModulesDict[i][1].ljust(58), #NAME
                                           "|", ModulesDict[i][3].ljust(10), #TYPE
                                           "|"), color=BLUE, verbose=True)
    color.echo('+' + "-" * 76 + "+", YELLOW)
    print


class BasicConsole(Cmd):
    def __init__(self):
        Cmd.__init__(self)

    def do_exit(self, arg):
        exit()

    def emptyline(self):
        pass

    def do_EOF(self, arg):
        return True

    def default(self, line):
        try:
            os.system(line)
        except KeyboardInterrupt:
            print
            pass

    def do_show(self, ModulesType):
        """
        param ModulesType: 模块类型
        """
        if ModulesType.lower() in ['', 'all', 'exploit', 'auxiliary']:
            if ModulesType.lower() in ['all', '']:
                ModulesType = ''
            ModulesLst = showModulesDict(ModulesType)
            printModuleDict(ModulesLst)
        else:
            color.echo("[!] error! USAGE:show [all|exploit|auxiliary]", RED, verbose=True)
            print


    def do_search(self, KeyWord):
        OutDict = ""
        if KeyWord: \
            OutDict = searchFromDB(KeyWord)
        else:
            color.echo("[!] Please give a keyword. USAGE:search [keyword]", RED, verbose=True)
            print
        if OutDict:
            printModuleDict(OutDict)
        else:
            print
            color.echo("[!] no modules match %s" % KeyWord, RED, verbose=True)


    def do_use(self, module):
        if len(module) and module != '':
            moduleName = returnModuleName(module)
            if moduleName:
                i = ExecModule(moduleName)
                i.cmdloop()
            else:
                print
                color.echo("[!] This modules is not available!", RED, verbose=True)
                print
        else:
            print
            color.echo('[!] please select a module name.  USEAGE:use [module name].  eg:use DemoModule', RED, verbose=True)
            print


    def do_updatedb(self, arg):
        print
        color.echo("[*] updating the database....", GREEN, verbose=True)
        updateDB()
        color.echo("[+] update finished!", GREEN, verbose=True)
        print


    def do_help(self, arg):
        print
        MltPMainHelp()


class MultiProxiesClient(BasicConsole):
    prompt = "MultiProxies>"

    globals = dict()
    globals['default'] = dict()
    globals['user'] = dict()

    def __init__(self):
        BasicConsole.__init__(self)

    def do_setg(self, arg):
        options = arg.split("=")

        if len(options) < 2:
            options = arg.split(" ")

        if len(options) == 2:
            Key = options[0].strip()
            Value = options[1].strip()
            if Key:
                if Key in Client.globals['default'].keys():
                    Client.globals['default'][Key] = Value.strip()
                else:
                    Client.globals['user'][Key] = Value.strip()

                if self.prompt != "MultiProxies>":
                    updateFromClient(self.moduleParams, Client.globals['user'])
                print
                color.echo('%s => %s' % (Key, Value), CYAN, verbose=True)
                print
            else:
                print
                color.echo("[!] Usage: setg [option] [value]", RED, verbose=True)
                print
        else:
            if len(Client.globals['user'].keys()):
                print
                color.echo("[*] User globals:", GREEN, verbose=True)
                Dict = Client.globals['user']
                items = Dict.keys()
                items.sort()
                color.echo('+' + 'Item'.center(25, '-') + ':' + 'Info'.center(50, '-') + "+", BLUE, verbose=True)
                for item in items:
                    color.echo("%s%-25s%s%50s%s" % ("|", str(item).center(25, ' '), ":",
                                                    str(Dict[item]).center(50, ' '), "|"), CYAN, verbose=True)
                color.echo('+' + '-' * 76 + '+', BLUE, verbose=True)
                print

            if len(Client.globals['default'].keys()):
                print
                color.echo("[*] MltProxies globals:", GREEN, verbose=True)
                Dict = Client.globals['default']
                items = Dict.keys()
                items.sort()
                color.echo('+' + 'Item'.center(25, '-') + ':' + 'Info'.center(50, '-') + "+", BLUE, verbose=True)
                for item in items:
                    color.echo("%s%-25s%s%50s%s" % ("|", str(item).center(25, ' '), ":",
                                                    str(Dict[item]).center(50, ' '), "|"), CYAN, verbose=True)
                color.echo('+' + '-' * 76 + '+', BLUE, verbose=True)
                print


    def do_usetg(self, key):
        Key = key.strip()
        if Key in Client.globals['user'].keys():
            Client.globals['user'].pop(Key)

        elif Key in Client.globals['default'].keys():
            Client.globals['default'][Key] = ""

        elif len(key):
            color.echo("[!] %s is not in globals." % Key)

        else:
            color.echo("[!] please give a key name.", RED)

class ExecModule(MultiProxiesClient):

    def __init__(self, Module):
        MultiProxiesClient.__init__(self)
        self.Module, self.ModuleName, self.ModulePath = Module
        self.nextStatus = True

        try:
            self.moduleHandle = useModule(self.ModuleName)
            self.moduleHandle.load()
            self.moduleParams = self.moduleHandle.moduleParams
            self.moduleInfo = self.moduleHandle.moduleInfo
            self.moduleDoc = self.moduleHandle.moduleDoc
            updateFromClient(self.moduleParams, Client.globals['user'])
            self.prompt = 'MultiProxies> ' + self.Module + ")"
            self.nextStatus = True

        except ImportError, errmsg:
            self.nextStatus = False
            color.echo("[!] %s : %s" % (self.ModulePath, errmsg), RED, verbose=True)
            color.echo('[!] maybe you need to install the packages above.', RED, verbose=True)
            self.prompt = 'MultiProxies> ' + self.Module + " [error] )"

        except Exception, e:
            self.nextStatus = False
            color.echo("[!] %s : %s" % (self.ModulePath, e), RED, verbose=True)
            color.echo("[!] please check the module file code and reload.", RED, verbose=True)
            self.prompt = 'MultiProxies> ' + self.Module + " [error] )"

    def updateFromClient(self, params, globals):
        for key in params.keys():
            if key in globals['user'].keys():
                params[key] = globals['user'][key]

    def do_reload(self,arg):
        try:
            color.echo('[*] reloading module.', YELLOW, verbose=True)
            self.moduleHandle.reload()
            self.moduleParams = self.moduleHandle.moduleParams
            self.moduleInfo = self.moduleHandle.moduleInfo
            self.moduleDoc = self.moduleHandle.moduleDoc
            updateFromClient(self.moduleParams, Client.globals['user'])
            self.prompt = 'MultiProxies> ' + self.Module + ")"
            self.nextStatus = True

        except Exception, e:
            color.echo("[!] %s : %s" % (self.ModulePath, e), RED, verbose=True)
            color.echo("[!] please check the module file code and reload.", RED, verbose=True)
            self.prompt = 'MultiProxies> ' + self.Module + " [error] )"

    def do_set(self, arg):
        options = arg.split("=")
        if len(options) < 2:
            options = arg.split(" ")
        if len(options) > 1:
            Key = options[0].strip()
            Value = options[1].strip()
            if Key in returnLowerCases(self.moduleParams):
                self.moduleParams[Key] = Value.strip()
                print
                color.echo('%s => %s' % (Key, Value), CYAN, verbose=True)
                print

            else:
                print
                color.echo("[!] error! Please use 'options' to show options key in this module.", RED, verbose=True)
                return False
        else:
            print
            color.echo("[!] Usage: set [option] [value]", RED, verbose=True)
            print

    def do_options(self, arg):
        try:
            if self.nextStatus is True and (self.moduleParams):
                Dict = self.moduleParams
                items = Dict.keys()
                items.sort()
                color.echo('+' + 'Item'.center(25, '-') + ':' + 'Info'.center(50, '-') + "+", BLUE, verbose=True)
                for item in items:
                    color.echo("%s%-25s%s%50s%s" % ("|", str(item).center(25, ' '), ":",
                                                    str(Dict[item]).center(50, ' '), "|"), CYAN, verbose=True)
                color.echo('+' + '-' * 76 + '+', BLUE, verbose=True)
                print
        except Exception,e:
            print
            color.echo("[!] %s" % e, RED, verbose=True)
            print
            return False


    def do_info(self, arg):
        try:
            if self.nextStatus is True and (self.moduleInfo):
                Dict = self.moduleInfo
                items = Dict.keys()
                items.sort()
                color.echo('+' + 'Item'.center(25, '-') + ':' + 'Info'.center(50, '-') + "+", BLUE, verbose=True)
                for item in items:
                    color.echo("%s%-25s%s%50s%s" % ("|", str(item).center(25, ' '), ":",
                                                    str(Dict[item]).center(50, ' '), "|"), CYAN, verbose=True)
                color.echo('+' + '-' * 76 + '+', BLUE, verbose=True)
                print
                if self.moduleDoc:
                    color.echo(self.moduleDoc, GREEN, verbose=True)
                    print
                color.echo("[*] path : %s" % self.ModulePath, CYAN, verbose=True)
        except Exception, e:
            print
            color.echo("[!] %s" % e, RED, verbose=True)
            print
            return False

    def do_exploit(self, arg):
        proxies = Client.globals['default']['proxies']
        from lib.ProxiesFunctions import urlCheck
        from lib.ProxiesFunctions import setProxy, unsetProxy
        from lib.ProxiesFunctions import isFalse

        try:
            checkproxies = urlCheck(proxies)
            if checkproxies is not None:
                setProxy(checkproxies[1], checkproxies[2], checkproxies[3])
                color.echo("[*] proxies : %s" % proxies, GREEN ,verbose=True)

            elif isFalse(proxies):
                color.echo("[*] proxies removed.", RED, verbose=True)
                unsetProxy()

            elif len(proxies) > 0:
                color.echo("[!] proxies : %s ." % proxies, RED, verbose=True)
                color.echo("[!] only http/socks4/socks5/. eg: socks5://127.0.0.1:8080/", RED, verbose=True)


            print
            print "[*] %s starting to exploit.." % time.ctime()
            print
            self.moduleHandle.moduleParams = self.moduleParams
            self.moduleHandle.run()

        except KeyboardInterrupt:
            print
            color.echo('[!] Interrupt detected.', RED, verbose=True)
            # return

        except Exception, e:
            color.echo("[!] %s : %s" % (self.ModulePath, e), RED, verbose=True)
            color.echo("[!] please check the module file code and reload.", RED, verbose=True)


        print
        print "[!] exploit finished."

    def do_help(self, arg):
        MltPModuleHelp()

    def do_back(self, arg):
        if self.ModuleName in sys.modules:
            del sys.modules[self.ModuleName]
        return True

Client = MultiProxiesClient()
Client.globals['default']['proxies'] = ""
Client.globals['default']['color'] = "true"
Client.globals['default']['verbose'] = "true"