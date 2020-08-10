class ForegroundColor:
    pallete = {
        "default" : "\x1b[39m",
        "black" : "\x1b[30m",
        "red" : "\x1b[31m",
        "green" : "\x1b[32m",
        "yellow" : "\x1b[33m",
        "blue" : "\x1b[34m",
        "magenta" : "\x1b[35m",
        "cyan" : "\x1b[36m",
        "lightgray" : "\x1b[37m",
        "darkgray" : "\x1b[90m",
        "lightred" : "\x1b[91m",
        "lightgreen" : "\x1b[92m",
        "lightyellow" : "\x1b[93m",
        "lightblue" : "\x1b[94m",
        "lightmagenta" : "\x1b[95m",
        "lightcyan" : "\x1b[96m",
        "white" : "\x1b[97m",
        "END" : "\033[0m"
    }
    def __call__(self, key, text):
        if key in self.pallete:
            return "{}{}{}".format(self.pallete[key], text, self.pallete["END"])
        else:
            raise ValueError("Invalid color. choose from {}".format(", ".join(list(self.pallete.keys())[:-1])))

class BackgroundColor:
    pallete = {
        "default" : "\x1b[49m",
        "black" : "\x1b[40m",
        "red" : "\x1b[41m",
        "green" : "\x1b[42m",
        "yellow" : "\x1b[43m",
        "blue" : "\x1b[44m",
        "magenta" : "\x1b[45m",
        "cyan" : "\x1b[46m",
        "lightgray" : "\x1b[47m",
        "darkgray" : "\x1b[100m",
        "lightred" : "\x1b[101m",
        "lightgreen" : "\x1b[102m",
        "lightyellow" : "\x1b[103m",
        "lightblue" : "\x1b[104m",
        "lightmagenta" : "\x1b[105m",
        "lightcyan" : "\x1b[106m",
        "white" : "\x1b[107m",
        "END" : "\033[0m"
    }
    def __call__(self, key, text):
        if key in self.pallete:
            return "{}{}{}".format(self.pallete[key], text, self.pallete["END"])
        else:
            raise ValueError("Invalid color. choose from {}".format(", ".join(list(self.pallete.keys())[:-1])))

class BaseFormatter(object):
    def __init__(self, fmt, col_width, just):
        self.fmt = fmt
        self.col_width = col_width
        if just == "l":
            self.just = ljust
        elif just == "c":
            self.just = cjust
        else:
            self.just = rjust
        self.bg = BackgroundColor()
        self.fg = ForegroundColor()

    def __call__(self, value, bg_color, fg_color):
        fmt = self.fmt(value)
        if len(fmt) > self.col_width:
            fmt = fmt[:self.col_width - 3] + '...'
        fmt = self.just(fmt, self.col_width)
        fmt = self.bg(bg_color, self.fg(fg_color, fmt))
        return fmt

    @classmethod
    def setup(cls, value, fmt='{}'.format, col_width=20, just='l'):
        return cls(fmt, col_width, just)

class IntegerFormatter(BaseFormatter):
    @classmethod
    def setup(cls, value, fmt=None, col_width=20, just='r'):
        if fmt is None:
            if len(str(value)) > col_width:
                fmt = '{{:.{}e}}'.format(col_width - 8)
            else:
                fmt = '{}'
            fmt = fmt.format
        return cls(fmt, col_width, just)


class FloatFormatter(BaseFormatter):
    @classmethod
    def setup(cls, value, fmt=None, col_width=20, just='r'):
        if fmt is None:
            value_str = str(value)
            if 'e' in value_str:
                fmt = '{{:.{}e}}'.format(max(0, min(6, col_width - 8)))
            else:
                if '.' in value_str:
                    head, tail = [len(e) for e in value_str.split('.')]
                else:
                    head, tail = len(value_str), 0
                if head >= col_width:
                    fmt = '{{:.{}e}}'.format(max(0, col_width - 8))
                elif len(value_str) > col_width:
                    fmt = '{{:.{}f}}'.format(col_width - head - 1)
                else:
                    precision = min(6, col_width - head - 1)
                    fmt = '{{:.{}f}}'.format(precision)
            fmt = fmt.format
        return cls(fmt, col_width, just)


def ljust(text, n):
    return text.ljust(n)

def rjust(text, n):
    return text.rjust(n)

def cjust(text, n):
    return text.center(n)