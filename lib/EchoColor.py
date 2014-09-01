# coding=utf-8
__author__ = 'DM_'

import platform
import ctypes
import sys


USE_WINDOWS_COLOR = False
if platform.system() == "Windows":
    USE_WINDOWS_COLOR = True

    # #########################################
    #windows color.

    BLACK = 0x0
    BLUE = 0x01
    GREEN = 0x02
    CYAN = 0x03
    RED = 0x04
    PURPLE = 0x05
    YELLOW = 0x06
    WHITE = 0x07
    GREY = 0x08
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    def set_cmd_text_color(color, handle=std_out_handle):
        '''set color'''
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool

    def resetColor():
        set_cmd_text_color(RED | GREEN | BLUE)

else:
    # #########################################
    #linux color.

    BLACK = '\033[0m'
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    CYAN = '\033[36m'
    RED = '\033[31m'
    PURPLE = '\033[35m'
    YELLOW = '\033[33m'
    WHITE = '\033[37m'
    GREY = '\033[38m'


class _echocolor():

    def echo(self, mess, color=None, append=False, verbose=False):
        reset = False
        from lib.ProxiesFunctions import isClientVerbose
        from lib.ProxiesFunctions import isColor

        if USE_WINDOWS_COLOR:
            if color and isColor():
                set_cmd_text_color(color | color | color)
                reset = True
        else:
            if color and isColor():
                mess = color + mess + BLACK

        if isClientVerbose() or verbose:
            if append:
                sys.stdout.write(mess)
                sys.stdout.flush()
            else:
                print(mess)

        if reset:
            resetColor()

color = _echocolor()