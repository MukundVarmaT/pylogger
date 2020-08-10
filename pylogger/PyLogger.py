import sys
from . import formatter as fmt

type2fmt = {
    float: fmt.FloatFormatter,
    int: fmt.IntegerFormatter,
}

class PyLogger(object):
    def __init__(self, columns=None, border=True, col_widths=None, bg_colors=None, fg_colors=None, justify=None, def_col_width=None):
        self.border = border
        self.col_widths = col_widths or {}
        self.out = sys.stdout
        self.justify = justify or {}
        self.def_col_width = def_col_width

        if columns is None:
            self.columns = []
        elif isinstance(columns, list):
            self.columns = columns
        else:
            raise ValueError('Invalid "columns" argument')
        
        self.bg_colors = bg_colors or {}
        self.fg_colors = fg_colors or {}

        self.formatters = []

    def __call__(self, *args):
        if len(self.formatters) == 0:
            self.setup(*args)

        row_cells = [*args]

        if len(row_cells) != len(self.formatters):
            raise ValueError('Expected number of columns is {}. Got {}.'.format(len(self.formatters), len(row_cells)))

        line = self.format_row(*row_cells)
        self.print_line(line)

    def format_row(self, *args):
        vals = [self.formatters[col](value, self.bg_colors.get(col, "default"), self.fg_colors.get(col, "default")) for col, value in enumerate(args)]
        row = self.join_row_items(*vals)
        return row

    def setup_formatters(self, *args):
        formatters = []

        for indx, value in enumerate(args):
            fmt_class = type2fmt.get(type(value), fmt.BaseFormatter)
            kwargs = {}
            if self.def_col_width is not None:
                kwargs["col_width"] = self.def_col_width
            elif indx in self.col_widths:
                kwargs['col_width'] = self.col_widths[indx]
            if indx in self.justify:
                kwargs["just"] = self.justify[indx]
            formatter = fmt_class.setup(value, **kwargs)
            formatters.append(formatter)

        self.formatters = formatters

    def setup(self, *args):
        self.setup_formatters(*args)
        if self.columns:
            self.print_header()
        elif self.border:
            self.print_line(self.make_horizontal_border())

    def print_header(self):
        col_names = []
        for coli, col_name in enumerate(self.columns):
            col_width = self.formatters[coli].col_width
            if len(col_name) > col_width:
                col_name = col_name[:col_width - 3] + '...'
            col_name = self.formatters[coli].just(col_name, col_width)
            col_names.append(col_name)

        header = self.join_row_items(*col_names)
        
        if self.border:
            self.print_line(self.make_horizontal_border())
            self.print_line(header)
            self.print_line(self.make_horizontal_border('|'))
        else:
            self.print_line(header)

    def make_horizontal_border(self, corner='+'):
        border = '+'.join('-' * fmr.col_width for fmr in self.formatters)
        return '{0}{1}{0}'.format(corner, border)

    def join_row_items(self, *args):
        if self.border:
            row = '|{}|'.format('|'.join(args))
        else:
            row = '{}'.join(args)
        return row

    def print_line(self, text):
        self.out.write(text)
        self.out.write('\n')
        self.out.flush()