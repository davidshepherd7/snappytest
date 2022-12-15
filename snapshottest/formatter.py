from .formatters import default_formatters


class Formatter(object):
    formatters = default_formatters()

    def __init__(self, imports=None):
        self.htchar = ' '*4
        self.lfchar = '\n'
        self.indent = 0
        self.imports = imports

    def __call__(self, value, **args):
        return self.format(value, self.indent)

    def format(self, value, indent):
        formatter = self.get_formatter(value)
        for module, import_name in formatter.get_imports():
            self.imports[module].add(import_name)
        return formatter.format(value, indent, self)

    @classmethod
    def normalize(cls, value):
        formatter = Formatter.get_formatter(value)
        return formatter.normalize(value, cls)

    @classmethod
    def get_formatter(cls, value):
        for formatter in cls.formatters:
            if formatter.can_format(value):
                return formatter

        # This should never happen as GenericFormatter is registered by default.
        raise RuntimeError("No formatter found for value")

    @classmethod
    def register_formatter(cls, formatter):
        cls.formatters = [formatter, *cls.formatters]
