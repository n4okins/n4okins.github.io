import js


class CMD:
    @staticmethod
    def ls(*args):
        return "."


def command_parser(cmd_str: str):
    cmd, *args = cmd_str.split()
    return cmd, args


def command_checker(cmd):
    print("command: ", cmd)
    print(" c-type: ", type(cmd))
    return hasattr(CMD, cmd)


def command_execute(cmd, *args):
    return getattr(CMD, cmd)(*args)


def add_div():
    div = js.document.createElement("div")
    div.innerHTML = "<h1>This element was created from Python</h1>"
    js.document.body.prepend(div)
