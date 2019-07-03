import colorama
import attr
from boltons.dictutils import subdict

colorama.init(autoreset=True)


@attr.s
class Printer:
    """Advanced printer

    # Usage

    ```
    from printer import Printer

    print = Printer()
    ```

    You can then use print as usual


    # Added Features

    ## Indenting


    `print.indent()`

    All following prints will be indented one level. Default level size is 4.

    `print.dedent()`

    Decrease indenting one level

    `print.reset_indent()`

    Go back to indent level 0

    ## Color

    `print.set_color('red')`

    Set color of following prints

    `print.reset_color('red')`

    Reset coloring

    ## Iterables

    `print.iter(iterable)`

    Print items one by one, with newlines inbetween.

    """

    _indent_size = attr.ib(default=4, init=False)
    _indent_level = attr.ib(default=0, init=False)
    _color = attr.ib(default=None, init=False)

    def __init__(self):
        self._indent_level = 0
        self._color = None

    def __call__(self, s, **options):
        standard_print_options = ['sep', 'end', 'file', 'flush']
        print_options = subdict(options, keep=standard_print_options)
        printer_options = subdict(options, drop=standard_print_options)
        print(self._print(s, **printer_options), **print_options)

    def indent(self):
        """Raise level of indentation"""
        self._indent_level += 1

    def dedent(self):
        """Decrease level of indentation"""
        self._indent_level = max(self._indent_level - 1, 0)

    def reset_indent(self):
        """Reset level of indentation"""
        self._indent_level = 0

    def set_color(self, color):
        """Set print color"""
        self._color = color

    def reset_color(self):
        """Reset print color"""
        self._color = None

    def iter(self, iterable, **kwargs):
        for i in iterable:
            self.print(i, **kwargs)

    def _print(self, s, prefix=None, color=None, **kwargs):
        """Substitute normal print"""
        prefix = prefix or ''
        color = color or self._color
        color = getattr(colorama.Fore, color.upper()) if color else ''
        return f'{color + " "*self._indent_size*self._indent_level}{prefix}{str(s)}'
