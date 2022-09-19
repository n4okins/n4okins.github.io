import js
import random

__globals__ = globals()
__display__ = __globals__["__display__"]


class CMD:
    @staticmethod
    def ls(*args):
        return "."

    @staticmethod
    def echo(*args):
        return " ".join(args)

    @staticmethod
    def random(*args):
        __display__.innerHTML = f"<h1>{random.randint(0, 1000)}</h1>"


def command_parser(cmd_str: str):
    if cmd_str == "":
        return "", ["", ""]
    else:
        cmd, *args = cmd_str.split()
        return cmd, args


def command_checker(cmd):
    return hasattr(CMD, cmd)


def command_execute(cmd, *args):
    return getattr(CMD, cmd)(*args)

