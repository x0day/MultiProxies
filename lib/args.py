__author__ = 'DM_'
import argparse

parser = argparse.ArgumentParser(
    epilog="MultiProxies Attack Framework, started from DM_ [at] x0day.me"
)

group = parser.add_mutually_exclusive_group()
group2 = parser.add_mutually_exclusive_group()

group.add_argument('-c',
                   '--console',
                   action="store_true",
                   dest="consoleMode",
                   help="start from console."
)

group.add_argument('-w',
                   '--web',
                   action="store_true",
                   dest="webMode",
                   help="start from web."
)

group2.add_argument('-l',
                    '--list',
                    action="store_true",
                    dest="showLst",
                    help="show modules list."
)

group2.add_argument('-s',
                    '--search',
                    action="store",
                    required=False,
                    dest="search",
                    help="search module with keyword."
)

group2.add_argument('-m',
                    '--module',
                    action="store",
                    required=False,
                    dest="module",
                    help="the module to use."
)

parser.add_argument('-o',
                    '--options',
                    action="store",
                    required=False,
                    type=str,
                    dest="options",
                    help="set the module's options."
)

parser.add_argument('-r',
                    '--run',
                    action="store_true",
                    dest="run",
                    help="start the module."
)

parser.add_argument('-g',
                    '--globals',
                    action="store",
                    dest="globals",
                    help="set the MltProxies globals"
)

args = parser.parse_args()
consoleMode = args.consoleMode
webMode = args.webMode
showLst = args.showLst
search = args.search
module = args.module
options = args.options
run = args.run
globals = args.globals
